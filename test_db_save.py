#!/usr/bin/env python3
"""
Test Database Save Functionality
"""
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
load_dotenv()

def test_db_save():
    """Test database save functionality"""
    from app.database import SessionLocal
    from app.models import ErrorMetric, Trace, Log, RCAReport
    from app.worker import RCAWorker
    
    print("🧪 Testing Database Save...")
    
    # Create worker instance
    worker = RCAWorker()
    
    # Test data
    test_error_card = {
        "env": "test-env",
        "service": "test-service",
        "span_kind": "server",
        "http_code": "500",
        "exception": "TestException",
        "root_name": "test-operation",
        "count": 1.0,
        "window_start": "2025-07-30 01:50:00",
        "window_end": "2025-07-30 01:55:00"
    }
    
    test_trace_ids = ["test-trace-1", "test-trace-2", "test-trace-3"]
    test_logs = {
        "test-trace-1": [{"level": "ERROR", "message": "Test log 1"}],
        "test-trace-2": [{"level": "ERROR", "message": "Test log 2"}]
    }
    
    db = SessionLocal()
    try:
        # Test error metric save
        error_id = worker.save_error_metric(db, test_error_card)
        print(f"✓ Saved error metric: {error_id}")
        
        # Test trace save
        worker.save_traces(db, error_id, test_trace_ids)
        print(f"✓ Saved {len(test_trace_ids)} traces")
        
        # Test log save
        worker.save_logs(db, test_logs)
        print(f"✓ Saved logs")
        
        # Verify in database
        error_count = db.query(ErrorMetric).filter_by(id=error_id).count()
        trace_count = db.query(Trace).filter_by(error_metric_id=error_id).count()
        log_count = db.query(Log).count()
        
        print(f"\nDatabase Verification:")
        print(f"Error metrics: {error_count}")
        print(f"Traces: {trace_count}")
        print(f"Logs: {log_count}")
        
        # Clean up test data
        db.query(Trace).filter_by(error_metric_id=error_id).delete()
        db.query(Log).delete()
        db.query(ErrorMetric).filter_by(id=error_id).delete()
        db.commit()
        print("✓ Cleaned up test data")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_db_save() 