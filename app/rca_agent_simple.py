"""
Simplified RCA Agent for Railway Deployment
Uses rule-based analysis instead of heavy LLM dependencies
"""
import os
from typing import Dict, Any

class SimpleRCAAgent:
    def __init__(self):
        self.name = "Simple RCA Agent"
    
    def analyze_error_card(self, correlation_data: Dict[str, Any]) -> str:
        """
        Analyze an error card's correlation data and generate RCA summary
        """
        error_card = correlation_data.get("error_card", {})
        trace_ids = correlation_data.get("trace_ids_hex", [])
        span_metadata = correlation_data.get("span_metadata", [])
        logs = correlation_data.get("logs", {})
        
        # Extract key information
        service = error_card.get("service", "Unknown")
        env = error_card.get("env", "Unknown")
        exception = error_card.get("exception", "Unknown")
        http_code = error_card.get("http_code", "Unknown")
        count = error_card.get("count", 0)
        
        # Rule-based analysis
        analysis = self._rule_based_analysis(service, env, exception, http_code, count, len(trace_ids), len(span_metadata))
        
        return analysis
    
    def _rule_based_analysis(self, service: str, env: str, exception: str, http_code: str, count: int, trace_count: int, span_count: int) -> str:
        """
        Perform rule-based RCA analysis
        """
        # Determine severity
        if http_code in ["500", "502", "503", "504"]:
            severity = "HIGH"
            primary_cause = "Server-side error"
        elif http_code in ["400", "401", "403", "404"]:
            severity = "MEDIUM"
            primary_cause = "Client-side error"
        else:
            severity = "LOW"
            primary_cause = "Unknown error"
        
        # Generate recommendations based on patterns
        recommendations = []
        
        if "timeout" in exception.lower() or "504" in str(http_code):
            recommendations.append("Check network connectivity and service dependencies")
            recommendations.append("Review timeout configurations")
            recommendations.append("Monitor external API response times")
        
        if "500" in str(http_code):
            recommendations.append("Check server logs for detailed error information")
            recommendations.append("Verify service connectivity and dependencies")
            recommendations.append("Review recent deployments or configuration changes")
        
        if "authorization" in exception.lower() or "401" in str(http_code) or "403" in str(http_code):
            recommendations.append("Verify authentication and authorization settings")
            recommendations.append("Check API keys and tokens")
            recommendations.append("Review access control policies")
        
        if trace_count == 0:
            recommendations.append("Enable distributed tracing for better debugging")
        
        if span_count == 0:
            recommendations.append("Check if spans are being generated correctly")
        
        # Default recommendations
        if not recommendations:
            recommendations = [
                "Check server logs for detailed error information",
                "Verify service connectivity and dependencies", 
                "Review recent deployments or configuration changes",
                "Monitor system resources (CPU, memory, disk)"
            ]
        
        # Build analysis summary
        analysis = f"""## Root Cause Analysis

**Primary Root Cause**: {primary_cause}
**Severity**: {severity}

**Evidence**:
- Service: {service}
- Environment: {env}
- Exception: {exception}
- HTTP Code: {http_code}
- Error Count: {count}
- Traces found: {trace_count}
- Spans found: {span_count}

**Recommendations**:
"""
        
        for i, rec in enumerate(recommendations, 1):
            analysis += f"{i}. {rec}\n"
        
        return analysis 