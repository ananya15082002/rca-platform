#!/usr/bin/env python3
"""
Clean Database - Remove any dummy data and ensure only live data
"""
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
load_dotenv()

def clean_database():
    """Clean all database records to ensure only live data"""
    from app.database import SessionLocal, engine
    from app.models import Base, ErrorMetric, Trace, Span, Log, RCAReport
    from sqlalchemy import text
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("🧹 Cleaning database...")
        
        # Delete all records
        db.query(RCAReport).delete()
        db.query(Log).delete()
        db.query(Span).delete()
        db.query(Trace).delete()
        db.query(ErrorMetric).delete()
        
        db.commit()
        
        print("✅ Database cleaned successfully!")
        print("📊 Database is now ready for live data only")
        
        # Verify clean state
        error_count = db.query(ErrorMetric).count()
        trace_count = db.query(Trace).count()
        log_count = db.query(Log).count()
        rca_count = db.query(RCAReport).count()
        
        print(f"📈 Current records: {error_count} errors, {trace_count} traces, {log_count} logs, {rca_count} RCA reports")
        
    except Exception as e:
        print(f"❌ Error cleaning database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clean_database() 