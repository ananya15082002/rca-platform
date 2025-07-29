#!/usr/bin/env python3
"""
Test Full Ingestion Cycle
"""
import os
import sys
import datetime
import pytz
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
load_dotenv()

def test_full_cycle():
    """Test a full ingestion cycle"""
    from app.ingestion import run_ingestion_cycle, get_next_5min_boundary
    from app.worker import RCAWorker
    
    print("🧪 Testing Full Ingestion Cycle...")
    
    # Get next 5-minute boundary
    next_boundary = get_next_5min_boundary()
    print(f"Next boundary: {next_boundary}")
    
    # Run ingestion cycle
    correlation_data_list = run_ingestion_cycle(next_boundary)
    
    if not correlation_data_list:
        print("ℹ No error cards found")
        return
    
    print(f"\n📊 Found {len(correlation_data_list)} error cards")
    
    # Process each correlation data
    worker = RCAWorker()
    
    for i, correlation_data in enumerate(correlation_data_list, 1):
        print(f"\n--- Processing Error Card {i}/{len(correlation_data_list)} ---")
        
        error_card = correlation_data["error_card"]
        trace_ids = correlation_data.get("trace_ids_hex", [])
        span_metadata = correlation_data.get("span_metadata", [])
        logs_dict = correlation_data.get("logs", {})
        
        print(f"Error: {error_card['env']} | {error_card['service']}")
        print(f"Trace IDs: {len(trace_ids)}")
        print(f"Span metadata: {len(span_metadata)}")
        print(f"Logs dict keys: {list(logs_dict.keys())}")
        
        total_logs = sum(len(logs) for logs in logs_dict.values())
        print(f"Total logs: {total_logs}")
        
        if trace_ids:
            print(f"Sample trace IDs: {trace_ids[:3]}")
        
        if span_metadata:
            print(f"Sample span: {span_metadata[0] if span_metadata else 'None'}")
        
        # Process with worker
        try:
            result = worker.process_correlation_data(correlation_data)
            print(f"✓ Worker result: {result}")
        except Exception as e:
            print(f"✗ Worker error: {e}")

if __name__ == "__main__":
    test_full_cycle() 