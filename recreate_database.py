#!/usr/bin/env python3
"""
Recreate Database with Updated Schema
"""
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
load_dotenv()

from app.database import engine, Base
from app.models import ErrorMetric, Trace, Span, Log, RCAReport

def recreate_database():
    """Drop and recreate all tables with updated schema"""
    print("🗑️  Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("🏗️  Creating new tables with updated schema...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database recreated successfully!")
    print("📊 New schema includes:")
    print("   - ErrorMetric: error_metrics table")
    print("   - Trace: traces table (with error_metric_id, trace_id_hex)")
    print("   - Span: spans table (with error_metric_id, trace_id_hex)")
    print("   - Log: logs table (with error_metric_id, trace_id_hex)")
    print("   - RCAReport: rca_reports table")

if __name__ == "__main__":
    recreate_database() 