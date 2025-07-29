#!/usr/bin/env python3
"""
Test Current Timing
"""
import os
import sys
import datetime
import pytz
import requests
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
load_dotenv()

def test_current_timing():
    """Test the current timing by triggering a cycle"""
    IST = pytz.timezone('Asia/Kolkata')
    
    print("🧪 Testing Current Timing...")
    
    # Current time
    now = datetime.datetime.now(IST)
    print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')} IST")
    
    # Trigger a cycle
    try:
        response = requests.post('http://localhost:8000/api/trigger-cycle', timeout=30)
        if response.status_code == 200:
            print("✅ Cycle triggered successfully")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Failed to trigger cycle: {response.status_code}")
    except Exception as e:
        print(f"❌ Error triggering cycle: {e}")

if __name__ == "__main__":
    test_current_timing() 