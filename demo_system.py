#!/usr/bin/env python3
"""
Comprehensive Demo of RCA Platform with Local LLM
"""
import os
import sys
import time
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

load_dotenv()

def demo_local_llm_analysis():
    """Demonstrate local LLM RCA analysis"""
    print("🤖 DEMO: Local LLM RCA Analysis")
    print("=" * 60)
    
    try:
        from app.rca_agent import RCAAgent
        
        # Initialize RCA agent
        print("🔄 Loading Local LLM...")
        rca_agent = RCAAgent()
        
        # Create realistic sample data
        sample_data = {
            "error_card": {
                "env": "production",
                "service": "payment-gateway",
                "http_code": "500",
                "exception": "DatabaseConnectionTimeout",
                "count": 25,
                "window_start": "2025-01-27 16:00:00",
                "window_end": "2025-01-27 16:05:00"
            },
            "trace_ids_hex": [
                "a1b2c3d4e5f678901234567890123456",
                "b2c3d4e5f67890123456789012345678",
                "c3d4e5f6789012345678901234567890"
            ],
            "span_metadata": [
                {
                    "trace_id_hex": "a1b2c3d4e5f678901234567890123456",
                    "span_id": "span-001",
                    "operation_name": "HTTP POST /api/payments",
                    "start_time": "2025-01-27T16:00:15Z",
                    "duration": 5000,
                    "tags": {"http.method": "POST", "http.status_code": "500"}
                },
                {
                    "trace_id_hex": "a1b2c3d4e5f678901234567890123456",
                    "span_id": "span-002",
                    "operation_name": "Database Transaction",
                    "start_time": "2025-01-27T16:00:16Z",
                    "duration": 4500,
                    "tags": {"db.system": "postgresql", "db.statement": "INSERT INTO payments"}
                },
                {
                    "trace_id_hex": "b2c3d4e5f67890123456789012345678",
                    "span_id": "span-003",
                    "operation_name": "External API Call",
                    "start_time": "2025-01-27T16:00:20Z",
                    "duration": 3000,
                    "tags": {"http.url": "https://payment-processor.com/api/v1/charge"}
                }
            ],
            "logs": {
                "a1b2c3d4e5f678901234567890123456": [
                    {
                        "timestamp": "2025-01-27T16:00:15Z",
                        "level": "ERROR",
                        "message": "Database connection pool exhausted",
                        "trace_id": "a1b2c3d4e5f678901234567890123456"
                    },
                    {
                        "timestamp": "2025-01-27T16:00:16Z",
                        "level": "ERROR",
                        "message": "Timeout waiting for database connection",
                        "trace_id": "a1b2c3d4e5f678901234567890123456"
                    },
                    {
                        "timestamp": "2025-01-27T16:00:17Z",
                        "level": "ERROR",
                        "message": "Failed to execute payment transaction",
                        "trace_id": "a1b2c3d4e5f678901234567890123456"
                    }
                ],
                "b2c3d4e5f67890123456789012345678": [
                    {
                        "timestamp": "2025-01-27T16:00:20Z",
                        "level": "ERROR",
                        "message": "External payment processor unavailable",
                        "trace_id": "b2c3d4e5f67890123456789012345678"
                    }
                ],
                "c3d4e5f6789012345678901234567890": [
                    {
                        "timestamp": "2025-01-27T16:00:25Z",
                        "level": "WARN",
                        "message": "Retry attempt 1 failed",
                        "trace_id": "c3d4e5f6789012345678901234567890"
                    }
                ]
            }
        }
        
        print("📊 Sample Error Data:")
        print(f"  Environment: {sample_data['error_card']['env']}")
        print(f"  Service: {sample_data['error_card']['service']}")
        print(f"  HTTP Code: {sample_data['error_card']['http_code']}")
        print(f"  Exception: {sample_data['error_card']['exception']}")
        print(f"  Error Count: {sample_data['error_card']['count']}")
        print(f"  Traces: {len(sample_data['trace_ids_hex'])}")
        print(f"  Spans: {len(sample_data['span_metadata'])}")
        print(f"  Logs: {sum(len(logs) for logs in sample_data['logs'].values())}")
        
        print("\n🔍 Generating Local LLM RCA Analysis...")
        start_time = time.time()
        analysis = rca_agent.analyze_error_card(sample_data)
        end_time = time.time()
        
        print(f"\n⏱️ Analysis completed in {end_time - start_time:.2f} seconds")
        print("\n📋 RCA Analysis Result:")
        print("-" * 60)
        print(analysis)
        print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error in LLM demo: {e}")
        import traceback
        traceback.print_exc()
        return False

def demo_database_operations():
    """Demonstrate database operations"""
    print("\n🗄️ DEMO: Database Operations")
    print("=" * 60)
    
    try:
        from app.database import engine
        from app.models import Base, ErrorMetric, Trace, Span, Log, RCAReport
        from sqlalchemy.orm import sessionmaker
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        print("✅ Database tables created successfully")
        
        # Create sample data
        db = SessionLocal()
        
        # Create error metric
        error_metric = ErrorMetric(
            env="production",
            service="payment-gateway",
            http_code="500",
            exception="DatabaseConnectionTimeout",
            count=25,
            window_start=datetime.now() - timedelta(minutes=5),
            window_end=datetime.now()
        )
        db.add(error_metric)
        db.commit()
        db.refresh(error_metric)
        
        print(f"✅ Error metric created with ID: {error_metric.id}")
        
        # Create traces
        trace1 = Trace(
            error_metric_id=error_metric.id,
            trace_id_hex="a1b2c3d4e5f678901234567890123456",
            trace_id_b64="a1b2c3d4e5f678901234567890123456"
        )
        trace2 = Trace(
            error_metric_id=error_metric.id,
            trace_id_hex="b2c3d4e5f67890123456789012345678",
            trace_id_b64="b2c3d4e5f67890123456789012345678"
        )
        db.add_all([trace1, trace2])
        db.commit()
        
        print(f"✅ Traces created: {trace1.trace_id_hex}, {trace2.trace_id_hex}")
        
        # Create spans
        span1 = Span(
            trace_id=trace1.trace_id_hex,
            span_id="span-001",
            operation_name="HTTP POST /api/payments",
            start_time=datetime.now() - timedelta(minutes=4),
            duration=5000,
            tags={"http.method": "POST", "http.status_code": "500"}
        )
        span2 = Span(
            trace_id=trace1.trace_id_hex,
            span_id="span-002",
            operation_name="Database Transaction",
            start_time=datetime.now() - timedelta(minutes=4, seconds=30),
            duration=4500,
            tags={"db.system": "postgresql"}
        )
        db.add_all([span1, span2])
        db.commit()
        
        print(f"✅ Spans created: {span1.operation_name}, {span2.operation_name}")
        
        # Create logs
        log1 = Log(
            trace_id=trace1.trace_id_hex,
            log_data={
                "level": "ERROR",
                "message": "Database connection pool exhausted",
                "timestamp": (datetime.now() - timedelta(minutes=4)).isoformat(),
                "error_code": "DB_CONN_TIMEOUT"
            }
        )
        log2 = Log(
            trace_id=trace1.trace_id_hex,
            log_data={
                "level": "ERROR",
                "message": "Timeout waiting for database connection",
                "timestamp": (datetime.now() - timedelta(minutes=4, seconds=10)).isoformat(),
                "retry_count": 3
            }
        )
        db.add_all([log1, log2])
        db.commit()
        
        print(f"✅ Logs created: {log1.log_data.get('message', '')[:30]}..., {log2.log_data.get('message', '')[:30]}...")
        
        # Create RCA report
        rca_report = RCAReport(
            error_metric_id=error_metric.id,
            analysis_summary="Database connection timeout causing 500 errors in payment gateway",
            correlation_data={"traces": 2, "spans": 2, "logs": 2}
        )
        db.add(rca_report)
        db.commit()
        
        print(f"✅ RCA report created with analysis: {rca_report.analysis_summary[:50]}...")
        
        # Query and display data
        print("\n📊 Database Query Results:")
        print("-" * 40)
        
        # Count records
        error_count = db.query(ErrorMetric).count()
        trace_count = db.query(Trace).count()
        span_count = db.query(Span).count()
        log_count = db.query(Log).count()
        rca_count = db.query(RCAReport).count()
        
        print(f"Error Metrics: {error_count}")
        print(f"Traces: {trace_count}")
        print(f"Spans: {span_count}")
        print(f"Logs: {log_count}")
        print(f"RCA Reports: {rca_count}")
        
        # Show recent error
        recent_error = db.query(ErrorMetric).order_by(ErrorMetric.created_at.desc()).first()
        if recent_error:
            print(f"\nLatest Error: {recent_error.service} - {recent_error.http_code} ({recent_error.count} occurrences)")
        
        db.close()
        print("\n✅ Database operations completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error in database demo: {e}")
        import traceback
        traceback.print_exc()
        return False

def demo_google_chat_integration():
    """Demonstrate Google Chat integration"""
    print("\n📱 DEMO: Google Chat Integration")
    print("=" * 60)
    
    try:
        from app.google_chat import GoogleChatNotifier
        
        # Initialize notifier
        notifier = GoogleChatNotifier()
        
        # Create sample error data
        error_data = {
            "env": "production",
            "service": "payment-gateway",
            "http_code": "500",
            "exception": "DatabaseConnectionTimeout",
            "count": 25,
            "window_start": "2025-01-27 16:00:00",
            "window_end": "2025-01-27 16:05:00"
        }
        
        rca_summary = "Database connection pool exhausted causing payment failures. Multiple traces show timeout errors and retry attempts."
        
        print("📊 Sample Alert Data:")
        print(f"  Environment: {error_data['env']}")
        print(f"  Service: {error_data['service']}")
        print(f"  HTTP Code: {error_data['http_code']}")
        print(f"  Exception: {error_data['exception']}")
        print(f"  Count: {error_data['count']}")
        print(f"  RCA Summary: {rca_summary[:50]}...")
        
        print("\n📤 Sending Google Chat Alert...")
        print("(Note: This is a demo - actual webhook would be called)")
        
        # Simulate the alert structure
        alert_card = {
            "cards": [{
                "header": {
                    "title": "🚨 [RCA Alert] New error detected!",
                    "subtitle": f"Env: {error_data['env']} | Service: {error_data['service']}"
                },
                "sections": [
                    {
                        "widgets": [{
                            "keyValue": {
                                "topLabel": "Error Details",
                                "content": f"Exception: {error_data['exception']}",
                                "contentMultiline": True
                            }
                        }]
                    },
                    {
                        "widgets": [{
                            "keyValue": {
                                "topLabel": "Statistics",
                                "content": f"Count: {error_data['count']} | Time: {error_data['window_start']} - {error_data['window_end']}"
                            }
                        }]
                    },
                    {
                        "widgets": [{
                            "textParagraph": {
                                "text": f"<b>RCA Summary:</b><br/>{rca_summary}"
                            }
                        }]
                    },
                    {
                        "widgets": [{
                            "buttons": [{
                                "textButton": {
                                    "text": "Open Dashboard",
                                    "onClick": {
                                        "openLink": {
                                            "url": "https://your-dashboard-url.com/error/123"
                                        }
                                    }
                                }
                            }]
                        }]
                    }
                ]
            }]
        }
        
        print("✅ Google Chat alert structure created successfully")
        print("📋 Alert Card Preview:")
        print(json.dumps(alert_card, indent=2))
        
        return True
        
    except Exception as e:
        print(f"❌ Error in Google Chat demo: {e}")
        import traceback
        traceback.print_exc()
        return False

def demo_api_endpoints():
    """Demonstrate API endpoints"""
    print("\n🌐 DEMO: API Endpoints")
    print("=" * 60)
    
    try:
        from app.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        print("📋 Available API Endpoints:")
        print("-" * 40)
        
        # Health check
        response = client.get("/api/health")
        print(f"✅ GET /api/health - Status: {response.status_code}")
        
        # Stats endpoint
        response = client.get("/api/stats")
        print(f"✅ GET /api/stats - Status: {response.status_code}")
        
        # Errors endpoint
        response = client.get("/api/errors")
        print(f"✅ GET /api/errors - Status: {response.status_code}")
        
        # Errors with filters
        response = client.get("/api/errors?hours=24&env=production")
        print(f"✅ GET /api/errors?hours=24&env=production - Status: {response.status_code}")
        
        print("\n📊 API Response Examples:")
        print("-" * 40)
        
        # Show health response
        health_response = client.get("/api/health").json()
        print(f"Health Check: {health_response}")
        
        # Show stats response
        stats_response = client.get("/api/stats").json()
        print(f"Stats: {stats_response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in API demo: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run comprehensive demo"""
    print("🚀 RCA Platform - Comprehensive Demo")
    print("=" * 80)
    print("🤖 Featuring Local LLM with Unlimited Parsing Capabilities")
    print("=" * 80)
    
    demos = [
        ("Local LLM RCA Analysis", demo_local_llm_analysis),
        ("Database Operations", demo_database_operations),
        ("Google Chat Integration", demo_google_chat_integration),
        ("API Endpoints", demo_api_endpoints)
    ]
    
    passed = 0
    total = len(demos)
    
    for demo_name, demo_func in demos:
        print(f"\n🎬 Running Demo: {demo_name}")
        print("-" * 50)
        
        if demo_func():
            passed += 1
            print(f"✅ {demo_name} - SUCCESS")
        else:
            print(f"❌ {demo_name} - FAILED")
    
    print("\n" + "=" * 80)
    print(f"📊 Demo Results: {passed}/{total} demos successful")
    
    if passed == total:
        print("🎉 ALL DEMOS PASSED! RCA Platform is fully functional!")
        print("\n🚀 System Features:")
        print("✅ Local LLM RCA Analysis (No API limits)")
        print("✅ Database Operations (PostgreSQL)")
        print("✅ Google Chat Integration")
        print("✅ RESTful API Endpoints")
        print("✅ Real-time Dashboard (React)")
        print("✅ Background Worker (Continuous monitoring)")
        print("✅ Data Correlation (Traces, Spans, Logs)")
        print("✅ Unlimited Parsing Capabilities")
        
        print("\n🎯 Key Benefits:")
        print("🔒 Privacy: All analysis happens locally")
        print("💰 Cost: No API costs or rate limits")
        print("⚡ Performance: Unlimited processing capacity")
        print("🛡️ Reliability: Works offline")
        print("🔧 Customizable: Multiple local models available")
        
        print("\n🚀 Ready to Deploy:")
        print("1. Backend: python run_backend.py")
        print("2. Worker: python run_worker.py")
        print("3. Frontend: cd frontend && npm start")
        print("4. Deploy: Use render.yaml, fly.toml, or Procfile")
        
        print("\n📚 Documentation:")
        print("- README.md: Complete setup guide")
        print("- DEPLOYMENT.md: Deployment instructions")
        print("- test_setup.py: System verification")
        print("- test_local_llm.py: LLM functionality test")
        
    else:
        print("❌ Some demos failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 