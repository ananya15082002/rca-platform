import os
import requests
import json
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class GoogleChatNotifier:
    def __init__(self):
        self.webhook_url = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")
        self.dashboard_base_url = os.getenv("DASHBOARD_BASE_URL", "https://your-deployment-url.com")
    
    def send_error_alert(self, error_card: Dict[str, Any], rca_summary: str, error_id: str):
        """
        Send an error alert to Google Chat
        """
        if not self.webhook_url:
            print("Warning: Google Chat webhook URL not configured")
            return False
        
        try:
            # Create the card message
            card = self._create_error_card(error_card, rca_summary, error_id)
            
            # Send to Google Chat
            response = requests.post(
                self.webhook_url,
                json=card,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✓ Google Chat alert sent successfully for error {error_id}")
                return True
            else:
                print(f"✗ Failed to send Google Chat alert: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Error sending Google Chat alert: {str(e)}")
            return False
    
    def _create_error_card(self, error_card: Dict[str, Any], rca_summary: str, error_id: str) -> Dict[str, Any]:
        """
        Create a Google Chat card for error alerts
        """
        env = error_card.get("env", "UNSET")
        service = error_card.get("service", "unknown")
        http_code = error_card.get("http_code", "unknown")
        exception = error_card.get("exception", "unknown")
        count = error_card.get("count", 0)
        window_start = error_card.get("window_start", "")
        window_end = error_card.get("window_end", "")
        
        # Truncate RCA summary for card display
        rca_preview = rca_summary[:200] + "..." if len(rca_summary) > 200 else rca_summary
        
        dashboard_url = f"{self.dashboard_base_url}/dashboard?highlight={error_id}"
        
        return {
            "cards": [{
                "header": {
                    "title": "🚨 [RCA Alert] New error detected!",
                    "subtitle": f"Environment: {env} | Service: {service}",
                    "imageUrl": "https://img.icons8.com/color/48/000000/warning-shield.png"
                },
                "sections": [
                    {
                        "widgets": [
                            {
                                "keyValue": {
                                    "topLabel": "Environment",
                                    "content": env
                                }
                            },
                            {
                                "keyValue": {
                                    "topLabel": "Service",
                                    "content": service
                                }
                            },
                            {
                                "keyValue": {
                                    "topLabel": "Exception",
                                    "content": exception
                                }
                            },
                            {
                                "keyValue": {
                                    "topLabel": "Count",
                                    "content": str(count)
                                }
                            },
                            {
                                "keyValue": {
                                    "topLabel": "Time Window",
                                    "content": f"{window_start} - {window_end}"
                                }
                            }
                        ]
                    },
                    {
                        "widgets": [
                            {
                                "textParagraph": {
                                    "text": f"<b>RCA Summary:</b><br/>{rca_preview}"
                                }
                            }
                        ]
                    },
                    {
                        "widgets": [
                            {
                                "buttons": [
                                    {
                                        "textButton": {
                                            "text": "View Error Details",
                                            "onClick": {
                                                "openLink": {
                                                    "url": dashboard_url
                                                }
                                            }
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }]
        } 