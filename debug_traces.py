#!/usr/bin/env python3
"""
Debug Trace Extraction
"""
import os
import sys
import requests
import json
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
load_dotenv()

def test_trace_extraction():
    """Test trace extraction from CubeAPM"""
    from app.ingestion import build_trace_url, extract_trace_ids_and_spans
    
    print("🧪 Testing Trace Extraction...")
    
    # Test with a recent error card
    test_card = {
        "env": "UNSET",
        "service": "prod-ucp-app-gateway",
        "http_code": "500",
        "exception": "500",
        "window_start": "2025-07-30 01:25:00",
        "window_end": "2025-07-30 01:30:00"
    }
    
    trace_url = build_trace_url(test_card, test_card['window_start'], test_card['window_end'])
    print(f"Trace URL: {trace_url}")
    
    try:
        r = requests.get(trace_url, timeout=30)
        traces_bundle = r.json()
        
        print(f"Response status: {r.status_code}")
        print(f"Response type: {type(traces_bundle)}")
        
        if isinstance(traces_bundle, dict):
            print(f"Response keys: {list(traces_bundle.keys())}")
            if 'data' in traces_bundle:
                print(f"Data type: {type(traces_bundle['data'])}")
                print(f"Data length: {len(traces_bundle['data']) if isinstance(traces_bundle['data'], list) else 'N/A'}")
        
        trace_ids_b64, trace_ids_hex, span_metadata = extract_trace_ids_and_spans(traces_bundle)
        
        print(f"\nExtraction Results:")
        print(f"Trace IDs (base64): {len(trace_ids_b64)}")
        print(f"Trace IDs (hex): {len(trace_ids_hex)}")
        print(f"Span metadata: {len(span_metadata)}")
        
        if trace_ids_hex:
            print(f"Sample trace IDs: {list(trace_ids_hex)[:3]}")
        
        if span_metadata:
            print(f"Sample span: {span_metadata[0] if span_metadata else 'None'}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_trace_extraction() 