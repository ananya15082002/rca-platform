#!/usr/bin/env python3
"""
Debug Logs Fetching
"""
import os
import sys
import requests
import json
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
load_dotenv()

def test_logs_fetching():
    """Test logs fetching from Coralogix"""
    from app.ingestion import fetch_logs, get_5min_window_epoch
    import datetime
    import pytz
    
    IST = pytz.timezone('Asia/Kolkata')
    
    print("🧪 Testing Logs Fetching from Coralogix...")
    
    # Test with a recent time window
    now = datetime.datetime.now(IST)
    start_utc, end_utc, start_str, end_str = get_5min_window_epoch(now)
    
    print(f"Time window: {start_str} to {end_str}")
    print(f"Epoch: {start_utc} to {end_utc}")
    
    # Test with a sample trace ID
    test_trace_id = "1234567890abcdef1234567890abcdef"
    
    print(f"\n📤 Fetching logs for trace ID: {test_trace_id}")
    
    logs_data = fetch_logs(test_trace_id, start_utc, end_utc)
    
    print(f"Logs response type: {type(logs_data)}")
    
    if logs_data:
        if isinstance(logs_data, dict):
            print(f"Logs data keys: {list(logs_data.keys())}")
            logs_list = logs_data.get("data", [])
            print(f"Logs count: {len(logs_list)}")
            if logs_list:
                print(f"Sample log: {logs_list[0]}")
        elif isinstance(logs_data, list):
            print(f"Logs count: {len(logs_data)}")
            if logs_data:
                print(f"Sample log: {logs_data[0]}")
    else:
        print("❌ No logs data returned")
    
    # Test with a real trace ID from the logs
    real_trace_id = "a1b2c3d4e5f678901234567890123456"
    print(f"\n📤 Fetching logs for real trace ID: {real_trace_id}")
    
    logs_data2 = fetch_logs(real_trace_id, start_utc, end_utc)
    
    if logs_data2:
        if isinstance(logs_data2, dict):
            logs_list2 = logs_data2.get("data", [])
            print(f"Real logs count: {len(logs_list2)}")
        elif isinstance(logs_data2, list):
            print(f"Real logs count: {len(logs_data2)}")
    else:
        print("❌ No logs found for real trace ID")

if __name__ == "__main__":
    test_logs_fetching() 