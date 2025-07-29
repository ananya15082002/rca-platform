#!/usr/bin/env python3
"""
Test Google Chat Integration
"""
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
load_dotenv()

def test_google_chat():
    """Test Google Chat webhook integration"""
    from app.google_chat import GoogleChatNotifier
    
    print("🧪 Testing Google Chat Integration...")
    
    # Test data
    test_error_card = {
        "env": "production",
        "service": "payment-gateway",
        "http_code": "500",
        "exception": "DatabaseConnectionTimeout",
        "count": 25,
        "window_start": "2025-07-30 01:25:00",
        "window_end": "2025-07-30 01:30:00"
    }
    
    test_rca_summary = "Root cause analysis indicates a database connection timeout issue affecting the payment gateway service. The error occurred during peak transaction processing, suggesting either database server overload or network connectivity issues between the application and database cluster."
    
    test_error_id = "test-error-123"
    
    # Test the integration
    notifier = GoogleChatNotifier()
    
    print(f"📤 Sending test alert to Google Chat...")
    print(f"Webhook URL: {notifier.webhook_url}")
    print(f"Dashboard URL: {notifier.dashboard_base_url}")
    
    success = notifier.send_error_alert(test_error_card, test_rca_summary, test_error_id)
    
    if success:
        print("✅ Google Chat integration test successful!")
        print("📱 Check your Google Chat space for the test alert")
    else:
        print("❌ Google Chat integration test failed")
        print("🔧 Please check your webhook URL configuration")

if __name__ == "__main__":
    test_google_chat() 