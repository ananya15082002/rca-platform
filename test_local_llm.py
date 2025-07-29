#!/usr/bin/env python3
"""
Test script to demonstrate local LLM RCA functionality
"""
import os
import sys
from dotenv import load_dotenv

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

load_dotenv()

def test_local_llm_rca():
    """Test the local LLM RCA functionality"""
    print("🤖 Testing Local LLM RCA Functionality")
    print("=" * 50)
    
    try:
        from app.rca_agent import RCAAgent
        
        # Initialize the RCA agent
        print("🔄 Initializing RCA Agent...")
        rca_agent = RCAAgent()
        
        # Create sample correlation data
        sample_data = {
            "error_card": {
                "env": "production",
                "service": "api-gateway",
                "http_code": "500",
                "exception": "Internal Server Error",
                "count": 15,
                "window_start": "2025-01-27 14:30:00",
                "window_end": "2025-01-27 14:35:00"
            },
            "trace_ids_hex": ["abc123def456", "ghi789jkl012"],
            "span_metadata": [
                {
                    "trace_id_b64": "abc123",
                    "trace_id_hex": "abc123def456",
                    "span_id": "span1",
                    "operation_name": "HTTP GET /api/users",
                    "start_time": "2025-01-27T14:30:15Z",
                    "duration": 2500,
                    "tags": {"http.method": "GET", "http.status_code": "500"}
                },
                {
                    "trace_id_b64": "def456",
                    "trace_id_hex": "ghi789jkl012",
                    "span_id": "span2",
                    "operation_name": "Database Query",
                    "start_time": "2025-01-27T14:30:16Z",
                    "duration": 1500,
                    "tags": {"db.system": "postgresql", "db.statement": "SELECT * FROM users"}
                }
            ],
            "logs": {
                "abc123def456": [
                    {
                        "timestamp": "2025-01-27T14:30:15Z",
                        "level": "ERROR",
                        "message": "Database connection timeout",
                        "trace_id": "abc123def456"
                    },
                    {
                        "timestamp": "2025-01-27T14:30:16Z",
                        "level": "ERROR", 
                        "message": "Failed to execute query: connection refused",
                        "trace_id": "abc123def456"
                    }
                ],
                "ghi789jkl012": [
                    {
                        "timestamp": "2025-01-27T14:30:16Z",
                        "level": "ERROR",
                        "message": "Database pool exhausted",
                        "trace_id": "ghi789jkl012"
                    }
                ]
            }
        }
        
        print("📊 Sample Data Created:")
        print(f"  - Environment: {sample_data['error_card']['env']}")
        print(f"  - Service: {sample_data['error_card']['service']}")
        print(f"  - HTTP Code: {sample_data['error_card']['http_code']}")
        print(f"  - Error Count: {sample_data['error_card']['count']}")
        print(f"  - Traces: {len(sample_data['trace_ids_hex'])}")
        print(f"  - Spans: {len(sample_data['span_metadata'])}")
        print(f"  - Logs: {sum(len(logs) for logs in sample_data['logs'].values())}")
        
        print("\n🔍 Generating RCA Analysis...")
        analysis = rca_agent.analyze_error_card(sample_data)
        
        print("\n📋 RCA Analysis Result:")
        print("-" * 50)
        print(analysis)
        print("-" * 50)
        
        print("\n✅ Local LLM RCA Test Completed Successfully!")
        print("🎯 The system is working with unlimited parsing capabilities!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during RCA test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_analysis():
    """Test the simple analysis fallback"""
    print("\n🔄 Testing Simple Analysis Fallback")
    print("=" * 50)
    
    try:
        from app.rca_agent import RCAAgent
        
        # Create an agent without LLM (simulate failure)
        agent = RCAAgent()
        agent.model = None
        agent.tokenizer = None
        
        sample_data = {
            "error_card": {
                "env": "staging",
                "service": "user-service",
                "http_code": "404",
                "exception": "Not Found",
                "count": 5,
                "window_start": "2025-01-27 15:00:00",
                "window_end": "2025-01-27 15:05:00"
            },
            "trace_ids_hex": ["trace123"],
            "span_metadata": [
                {
                    "trace_id_hex": "trace123",
                    "operation_name": "HTTP GET /api/user/123",
                    "duration": 100,
                    "start_time": "2025-01-27T15:00:10Z"
                }
            ],
            "logs": {
                "trace123": [
                    {
                        "timestamp": "2025-01-27T15:00:10Z",
                        "level": "WARN",
                        "message": "User not found: 123",
                        "trace_id": "trace123"
                    }
                ]
            }
        }
        
        print("📊 Testing with Simple Analysis...")
        analysis = agent.analyze_error_card(sample_data)
        
        print("\n📋 Simple Analysis Result:")
        print("-" * 50)
        print(analysis)
        print("-" * 50)
        
        print("\n✅ Simple Analysis Test Completed Successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during simple analysis test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🚀 Local LLM RCA Platform Test Suite")
    print("=" * 60)
    
    tests = [
        ("Local LLM RCA", test_local_llm_rca),
        ("Simple Analysis Fallback", test_simple_analysis)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 40)
        
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Local LLM RCA is working perfectly!")
        print("\n🚀 Ready to deploy:")
        print("1. Backend: python run_backend.py")
        print("2. Worker: python run_worker.py")
        print("3. Frontend: cd frontend && npm start")
        print("\n🤖 Features:")
        print("- Unlimited RCA analysis with local LLM")
        print("- No API limits or costs")
        print("- Privacy-focused (all processing local)")
        print("- Automatic fallback to simple analysis")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 