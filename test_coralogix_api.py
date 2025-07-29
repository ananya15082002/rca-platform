#!/usr/bin/env python3
"""
Test Coralogix API Directly
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def test_coralogix_api():
    """Test Coralogix API directly"""
    LOGS_API_URL = os.getenv('LOGS_API_URL', "http://observability-prod.fxtrt.io:3130/api/logs/select/logsql/query")
    
    print("🧪 Testing Coralogix API Directly...")
    print(f"API URL: {LOGS_API_URL}")
    
    # Test with a simple query
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # Test 1: Simple time-based query
    query_string = '{} _time:[1753819321,1753819621)'
    payload = [
        ("query", query_string),
        ("limit", "10")
    ]
    
    print(f"\n📤 Test 1: Simple time query")
    print(f"Query: {query_string}")
    
    try:
        resp = requests.post(LOGS_API_URL, data=payload, headers=headers, timeout=30)
        print(f"Status Code: {resp.status_code}")
        print(f"Response Headers: {dict(resp.headers)}")
        
        if resp.status_code == 200:
            try:
                result = resp.json()
                print(f"JSON Response: {json.dumps(result, indent=2)}")
            except Exception as e:
                print(f"Text Response: {resp.text[:500]}")
        else:
            print(f"Error Response: {resp.text}")
            
    except Exception as e:
        print(f"Request failed: {e}")
    
    # Test 2: Query with trace_id
    query_string2 = '{} _time:[1753819321,1753819621) (trace_id:"1234567890abcdef1234567890abcdef" OR trace.id:"1234567890abcdef1234567890abcdef")'
    payload2 = [
        ("query", query_string2),
        ("limit", "10")
    ]
    
    print(f"\n📤 Test 2: Query with trace_id")
    print(f"Query: {query_string2}")
    
    try:
        resp2 = requests.post(LOGS_API_URL, data=payload2, headers=headers, timeout=30)
        print(f"Status Code: {resp2.status_code}")
        
        if resp2.status_code == 200:
            try:
                result2 = resp2.json()
                print(f"JSON Response: {json.dumps(result2, indent=2)}")
            except Exception as e:
                print(f"Text Response: {resp2.text[:500]}")
        else:
            print(f"Error Response: {resp2.text}")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_coralogix_api() 