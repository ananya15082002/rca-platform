from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
import datetime
import pytz

from app.database import get_db, engine
from app.models import Base, ErrorMetric, Trace, Span, Log, RCAReport
from app.ingestion import run_ingestion_cycle, get_next_5min_boundary

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="RCA Platform API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "RCA Platform API", "status": "running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.now().isoformat()}

@app.get("/api/errors")
async def get_errors(
    db: Session = Depends(get_db),
    hours: int = Query(24, description="Number of hours to look back"),
    env: Optional[str] = Query(None, description="Filter by environment"),
    service: Optional[str] = Query(None, description="Filter by service")
):
    """Get error metrics for the last N hours"""
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(hours=hours)
    
    query = db.query(ErrorMetric).filter(
        ErrorMetric.window_start >= start_time,
        ErrorMetric.window_start <= end_time
    )
    
    if env:
        query = query.filter(ErrorMetric.env == env)
    if service:
        query = query.filter(ErrorMetric.service == service)
    
    errors = query.order_by(desc(ErrorMetric.window_start)).all()
    
    return {
        "errors": [
            {
                "id": error.id,
                "env": error.env,
                "service": error.service,
                "span_kind": error.span_kind,
                "http_code": error.http_code,
                "exception": error.exception,
                "root_name": error.root_name,
                "count": error.count,
                "window_start": error.window_start.isoformat(),
                "window_end": error.window_end.isoformat(),
                "created_at": error.created_at.isoformat()
            }
            for error in errors
        ],
        "total": len(errors)
    }

@app.get("/api/errors/{error_id}")
async def get_error_details(error_id: str, db: Session = Depends(get_db)):
    """Get detailed information for a specific error"""
    error = db.query(ErrorMetric).filter(ErrorMetric.id == error_id).first()
    if not error:
        raise HTTPException(status_code=404, detail="Error not found")
    
    # Get traces
    traces = db.query(Trace).filter(Trace.error_metric_id == error_id).all()
    
    # Get spans for this error
    spans = db.query(Span).filter(Span.error_metric_id == error_id).all()
    
    # Get logs for this error
    logs = db.query(Log).filter(Log.error_metric_id == error_id).all()
    
    # Get RCA report
    rca_report = db.query(RCAReport).filter(RCAReport.error_metric_id == error_id).first()
    
    return {
        "error": {
            "id": error.id,
            "env": error.env,
            "service": error.service,
            "span_kind": error.span_kind,
            "http_code": error.http_code,
            "exception": error.exception,
            "root_name": error.root_name,
            "count": error.count,
            "window_start": error.window_start.isoformat(),
            "window_end": error.window_end.isoformat(),
            "created_at": error.created_at.isoformat()
        },
        "traces": [
            {
                "id": trace.id,
                "trace_id_hex": trace.trace_id_hex,
                "trace_id_b64": trace.trace_id_b64,
                "created_at": trace.created_at.isoformat()
            }
            for trace in traces
        ],
        "spans": [
            {
                "id": span.id,
                "trace_id_hex": span.trace_id_hex,
                "span_id": span.span_id,
                "operation_name": span.operation_name,
                "start_time": span.start_time.isoformat() if span.start_time else None,
                "duration": span.duration,
                "tags": span.tags,
                "created_at": span.created_at.isoformat()
            }
            for span in spans
        ],
        "logs": [
            {
                "id": log.id,
                "trace_id_hex": log.trace_id_hex,
                "log_data": log.log_data,
                "created_at": log.created_at.isoformat()
            }
            for log in logs
        ],
        "rca_report": {
            "id": rca_report.id,
            "analysis_summary": rca_report.analysis_summary,
            "correlation_data": rca_report.correlation_data,
            "created_at": rca_report.created_at.isoformat()
        } if rca_report else None
    }

@app.get("/api/errors/{error_id}/download")
async def download_error_data(error_id: str, db: Session = Depends(get_db)):
    """Download complete correlation data for an error as JSON"""
    error = db.query(ErrorMetric).filter(ErrorMetric.id == error_id).first()
    if not error:
        raise HTTPException(status_code=404, detail="Error not found")
    
    # Get all related data
    traces = db.query(Trace).filter(Trace.error_metric_id == error_id).all()
    trace_ids = [trace.trace_id_hex for trace in traces if trace.trace_id_hex]
    
    spans = []
    logs = []
    if trace_ids:
        spans = db.query(Span).filter(Span.trace_id.in_(trace_ids)).all()
        logs = db.query(Log).filter(Log.trace_id.in_(trace_ids)).all()
    
    rca_report = db.query(RCAReport).filter(RCAReport.error_metric_id == error_id).first()
    
    # Build correlation data structure
    correlation_data = {
        "error_card": {
            "env": error.env,
            "service": error.service,
            "span_kind": error.span_kind,
            "http_code": error.http_code,
            "exception": error.exception,
            "root_name": error.root_name,
            "count": error.count,
            "window_start": error.window_start.strftime("%Y-%m-%d %H:%M:%S"),
            "window_end": error.window_end.strftime("%Y-%m-%d %H:%M:%S")
        },
        "trace_ids_hex": trace_ids,
        "span_metadata": [
            {
                "trace_id_hex": span.trace_id,
                "span_id": span.span_id,
                "operation_name": span.operation_name,
                "start_time": span.start_time.timestamp() if span.start_time else None,
                "duration": span.duration,
                "tags": span.tags
            }
            for span in spans
        ],
        "logs": {}
    }
    
    # Group logs by trace_id
    for log in logs:
        if log.trace_id not in correlation_data["logs"]:
            correlation_data["logs"][log.trace_id] = []
        correlation_data["logs"][log.trace_id].append(log.log_data)
    
    if rca_report:
        correlation_data["rca_analysis"] = {
            "summary": rca_report.analysis_summary,
            "correlation_data": rca_report.correlation_data
        }
    
    return correlation_data

@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get platform statistics"""
    # Total errors in last 24 hours
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(hours=24)
    
    total_errors = db.query(func.count(ErrorMetric.id)).filter(
        ErrorMetric.window_start >= start_time
    ).scalar()
    
    # Errors by environment
    env_stats = db.query(
        ErrorMetric.env,
        func.count(ErrorMetric.id).label('count')
    ).filter(
        ErrorMetric.window_start >= start_time
    ).group_by(ErrorMetric.env).all()
    
    # Errors by service
    service_stats = db.query(
        ErrorMetric.service,
        func.count(ErrorMetric.id).label('count')
    ).filter(
        ErrorMetric.window_start >= start_time
    ).group_by(ErrorMetric.service).order_by(desc('count')).limit(10).all()
    
    # Total traces and logs
    total_traces = db.query(func.count(Trace.id)).scalar()
    total_logs = db.query(func.count(Log.id)).scalar()
    total_rca_reports = db.query(func.count(RCAReport.id)).scalar()
    
    return {
        "last_24_hours": {
            "total_errors": total_errors,
            "environments": [{"env": env, "count": count} for env, count in env_stats],
            "top_services": [{"service": service, "count": count} for service, count in service_stats]
        },
        "total_data": {
            "traces": total_traces,
            "logs": total_logs,
            "rca_reports": total_rca_reports
        }
    }

@app.post("/api/trigger-cycle")
async def trigger_manual_cycle():
    """Manually trigger an ingestion cycle (for testing)"""
    try:
        next_boundary = get_next_5min_boundary()
        correlation_data = run_ingestion_cycle(next_boundary)
        return {
            "message": "Manual cycle triggered successfully",
            "error_cards_found": len(correlation_data),
            "next_boundary": next_boundary.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error triggering cycle: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 