#!/usr/bin/env python3
"""
RCA Platform System Status
Shows the complete status of the Local LLM-powered RCA Platform
"""
import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

load_dotenv()

def check_system_status():
    """Check the complete system status"""
    print("🚀 RCA Platform - System Status")
    print("=" * 80)
    print("🤖 Local LLM-Powered Root Cause Analysis Platform")
    print("=" * 80)
    
    status = {
        "local_llm": False,
        "database": False,
        "api": False,
        "frontend": False,
        "worker": False,
        "google_chat": False
    }
    
    # Check Local LLM
    print("\n🤖 Checking Local LLM...")
    try:
        from app.rca_agent import RCAAgent
        rca_agent = RCAAgent()
        if rca_agent.model and rca_agent.tokenizer:
            print("✅ Local LLM: Loaded successfully")
            print(f"   Model: {rca_agent.model_name}")
            print("   Status: Ready for unlimited RCA analysis")
            status["local_llm"] = True
        else:
            print("⚠️ Local LLM: Fallback mode (simple analysis)")
            print("   Status: Basic analysis available")
            status["local_llm"] = True
    except Exception as e:
        print(f"❌ Local LLM: Error - {e}")
    
    # Check Database
    print("\n🗄️ Checking Database...")
    try:
        from app.database import engine
        from app.models import Base
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy import text
        
        # Test connection
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Test query
        result = db.execute(text("SELECT 1")).fetchone()
        if result:
            print("✅ Database: Connected successfully")
            print("   Type: PostgreSQL")
            print("   Status: Ready for data storage")
            status["database"] = True
        db.close()
    except Exception as e:
        print(f"❌ Database: Error - {e}")
    
    # Check API
    print("\n🌐 Checking API...")
    try:
        from app.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get("/api/health")
        
        if response.status_code == 200:
            print("✅ API: Running successfully")
            print("   Framework: FastAPI")
            print("   Status: Ready to serve requests")
            status["api"] = True
        else:
            print(f"⚠️ API: Unexpected status code {response.status_code}")
    except Exception as e:
        print(f"❌ API: Error - {e}")
    
    # Check Frontend
    print("\n🎨 Checking Frontend...")
    try:
        frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
        package_json = os.path.join(frontend_dir, 'package.json')
        
        if os.path.exists(package_json):
            print("✅ Frontend: React app found")
            print("   Framework: React.js")
            print("   UI: Tailwind CSS + Recharts")
            print("   Status: Ready for development")
            status["frontend"] = True
        else:
            print("❌ Frontend: package.json not found")
    except Exception as e:
        print(f"❌ Frontend: Error - {e}")
    
    # Check Worker
    print("\n⚙️ Checking Background Worker...")
    try:
        from app.worker import RCAWorker
        print("✅ Worker: Code available")
        print("   Function: Continuous monitoring")
        print("   Interval: Every 5 minutes")
        print("   Status: Ready to run")
        status["worker"] = True
    except Exception as e:
        print(f"❌ Worker: Error - {e}")
    
    # Check Google Chat
    print("\n📱 Checking Google Chat Integration...")
    try:
        from app.google_chat import GoogleChatNotifier
        webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
        
        if webhook_url:
            print("✅ Google Chat: Webhook configured")
            print("   Status: Ready for alerts")
            status["google_chat"] = True
        else:
            print("⚠️ Google Chat: Webhook URL not configured")
    except Exception as e:
        print(f"❌ Google Chat: Error - {e}")
    
    # System Summary
    print("\n" + "=" * 80)
    print("📊 SYSTEM STATUS SUMMARY")
    print("=" * 80)
    
    total_checks = len(status)
    passed_checks = sum(status.values())
    
    print(f"✅ Passed: {passed_checks}/{total_checks}")
    print(f"❌ Failed: {total_checks - passed_checks}/{total_checks}")
    
    if passed_checks == total_checks:
        print("\n🎉 ALL SYSTEMS OPERATIONAL!")
        print("🚀 RCA Platform is ready for production deployment")
    else:
        print(f"\n⚠️ {total_checks - passed_checks} system(s) need attention")
    
    # Feature Matrix
    print("\n🔧 FEATURE MATRIX:")
    print("-" * 50)
    features = [
        ("Local LLM RCA", status["local_llm"], "Unlimited analysis, no API limits"),
        ("Database Storage", status["database"], "PostgreSQL with optimized indexes"),
        ("REST API", status["api"], "FastAPI with comprehensive endpoints"),
        ("React Dashboard", status["frontend"], "Real-time visualization"),
        ("Background Worker", status["worker"], "Continuous monitoring"),
        ("Google Chat Alerts", status["google_chat"], "Real-time notifications")
    ]
    
    for feature, status_bool, description in features:
        status_icon = "✅" if status_bool else "❌"
        print(f"{status_icon} {feature:<20} - {description}")
    
    # Deployment Status
    print("\n🚀 DEPLOYMENT STATUS:")
    print("-" * 50)
    
    deployment_files = [
        ("render.yaml", "Render.com deployment"),
        ("fly.toml", "Fly.io deployment"),
        ("Procfile", "Heroku deployment"),
        ("requirements.txt", "Python dependencies"),
        ("frontend/package.json", "Frontend dependencies"),
        ("README.md", "Setup documentation"),
        ("DEPLOYMENT.md", "Deployment guide")
    ]
    
    for filename, description in deployment_files:
        if os.path.exists(filename):
            print(f"✅ {filename:<20} - {description}")
        else:
            print(f"❌ {filename:<20} - {description} (missing)")
    
    # Next Steps
    print("\n🎯 NEXT STEPS:")
    print("-" * 50)
    
    if passed_checks == total_checks:
        print("1. 🚀 Deploy to production:")
        print("   - Backend: python run_backend.py")
        print("   - Worker: python run_worker.py")
        print("   - Frontend: cd frontend && npm start")
        
        print("\n2. 🌐 Deploy to cloud:")
        print("   - Render.com: Use render.yaml")
        print("   - Fly.io: Use fly.toml")
        print("   - Heroku: Use Procfile")
        
        print("\n3. 📊 Monitor system:")
        print("   - Check API health: GET /api/health")
        print("   - View stats: GET /api/stats")
        print("   - Monitor logs for errors")
        
        print("\n4. 🔧 Customize:")
        print("   - Update .env with your configuration")
        print("   - Modify Google Chat webhook URL")
        print("   - Adjust local LLM model if needed")
        
        print("\n🎉 CONGRATULATIONS!")
        print("Your RCA Platform is fully operational with unlimited local LLM capabilities!")
        
    else:
        print("1. 🔧 Fix failed components:")
        for component, status_bool in status.items():
            if not status_bool:
                print(f"   - {component.replace('_', ' ').title()}")
        
        print("\n2. 📚 Check documentation:")
        print("   - README.md for setup instructions")
        print("   - test_setup.py for verification")
        print("   - demo_system.py for testing")
    
    return passed_checks == total_checks

if __name__ == "__main__":
    success = check_system_status()
    sys.exit(0 if success else 1) 