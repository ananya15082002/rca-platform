#!/usr/bin/env python3
"""
Test Timing Logic
"""
import os
import sys
import datetime
import pytz
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
load_dotenv()

def test_timing_logic():
    """Test the timing logic to ensure it processes the last 5 minutes correctly"""
    from app.ingestion import get_5min_window_epoch, get_next_5min_boundary
    
    IST = pytz.timezone('Asia/Kolkata')
    
    print("🧪 Testing Timing Logic...")
    
    # Current time
    now = datetime.datetime.now(IST)
    print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')} IST")
    
    # Next boundary
    next_boundary = get_next_5min_boundary()
    print(f"Next 5-minute boundary: {next_boundary.strftime('%Y-%m-%d %H:%M:%S')} IST")
    
    # Test window calculation
    start_utc, end_utc, start_str, end_str = get_5min_window_epoch(now)
    print(f"Window for current time: {start_str} to {end_str}")
    
    # Calculate what the window should be (last 5 minutes)
    expected_start = now - datetime.timedelta(minutes=5)
    expected_start_str = expected_start.strftime('%Y-%m-%d %H:%M:%S')
    expected_end_str = now.strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"Expected window: {expected_start_str} to {expected_end_str}")
    
    # Verify the window is correct
    if start_str == expected_start_str and end_str == expected_end_str:
        print("✅ Timing logic is correct!")
        print(f"✅ Processing last 5 minutes: {start_str} to {end_str}")
    else:
        print("❌ Timing logic is incorrect!")
        print(f"Expected: {expected_start_str} to {expected_end_str}")
        print(f"Actual: {start_str} to {end_str}")
    
    # Test with a specific time
    test_time = datetime.datetime(2025, 7, 30, 2, 15, 30, tzinfo=IST)
    print(f"\nTest with specific time: {test_time.strftime('%Y-%m-%d %H:%M:%S')} IST")
    
    start_utc2, end_utc2, start_str2, end_str2 = get_5min_window_epoch(test_time)
    print(f"Window: {start_str2} to {end_str2}")
    
    # Should be 2:10:30 to 2:15:30
    expected_start2 = test_time - datetime.timedelta(minutes=5)
    expected_start_str2 = expected_start2.strftime('%Y-%m-%d %H:%M:%S')
    expected_end_str2 = test_time.strftime('%Y-%m-%d %H:%M:%S')
    
    if start_str2 == expected_start_str2 and end_str2 == expected_end_str2:
        print("✅ Specific time test passed!")
    else:
        print("❌ Specific time test failed!")
        print(f"Expected: {expected_start_str2} to {expected_end_str2}")
        print(f"Actual: {start_str2} to {end_str2}")

if __name__ == "__main__":
    test_timing_logic() 