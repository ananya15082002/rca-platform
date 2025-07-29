import os
import json
from typing import Dict, Any, Optional
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from dotenv import load_dotenv

load_dotenv()

class RCAAgent:
    def __init__(self):
        # Use a local model that's good for analysis tasks
        self.model_name = "microsoft/DialoGPT-medium"  # Good for conversational analysis
        # Alternative models you can use:
        # "gpt2" - Smaller, faster
        # "microsoft/DialoGPT-large" - Better quality but slower
        # "EleutherAI/gpt-neo-125M" - Good balance
        
        print(f"🤖 Loading local LLM: {self.model_name}")
        
        try:
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            print("✅ Local LLM loaded successfully")
            
        except Exception as e:
            print(f"⚠️ Warning: Could not load local LLM: {e}")
            print("🔄 Falling back to simple text analysis")
            self.model = None
            self.tokenizer = None
    
    def analyze_error_card(self, correlation_data: Dict[str, Any]) -> str:
        """
        Analyze an error card's correlation data and generate RCA summary
        """
        error_card = correlation_data.get("error_card", {})
        trace_ids = correlation_data.get("trace_ids_hex", [])
        span_metadata = correlation_data.get("span_metadata", [])
        logs = correlation_data.get("logs", {})
        
        # Prepare the analysis prompt
        prompt = self._build_analysis_prompt(error_card, trace_ids, span_metadata, logs)
        
        try:
            if self.model and self.tokenizer:
                # Use local LLM for analysis
                return self._generate_with_local_llm(prompt)
            else:
                # Fallback to simple analysis
                return self._simple_analysis(error_card, trace_ids, span_metadata, logs)
                
        except Exception as e:
            return f"Error during RCA analysis: {str(e)}"
    
    def _generate_with_local_llm(self, prompt: str) -> str:
        """
        Generate RCA analysis using local LLM
        """
        try:
            # Prepare input for the model
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncation=True, max_length=1024)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 500,  # Generate up to 500 more tokens
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode the generated text
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract the generated part (remove the input prompt)
            response = generated_text[len(prompt):].strip()
            
            if not response:
                return self._simple_analysis_from_prompt(prompt)
            
            return response
            
        except Exception as e:
            print(f"⚠️ Local LLM generation failed: {e}")
            return self._simple_analysis_from_prompt(prompt)
    
    def _simple_analysis_from_prompt(self, prompt: str) -> str:
        """
        Simple analysis based on the prompt content
        """
        lines = prompt.split('\n')
        analysis_parts = []
        
        # Extract key information from the prompt
        error_info = {}
        for line in lines:
            if 'Environment:' in line:
                error_info['env'] = line.split('Environment:')[1].strip()
            elif 'Service:' in line:
                error_info['service'] = line.split('Service:')[1].strip()
            elif 'HTTP Code:' in line:
                error_info['http_code'] = line.split('HTTP Code:')[1].strip()
            elif 'Exception:' in line:
                error_info['exception'] = line.split('Exception:')[1].strip()
            elif 'Number of Traces:' in line:
                error_info['traces'] = line.split('Number of Traces:')[1].strip()
            elif 'Number of Spans:' in line:
                error_info['spans'] = line.split('Number of Spans:')[1].strip()
        
        # Generate simple analysis
        analysis_parts.append("## Root Cause Analysis")
        analysis_parts.append("")
        
        if error_info.get('http_code') == '500':
            analysis_parts.append("**Primary Root Cause**: Internal Server Error (500)")
            analysis_parts.append("This indicates a server-side issue that needs immediate attention.")
        elif error_info.get('http_code') == '404':
            analysis_parts.append("**Primary Root Cause**: Not Found Error (404)")
            analysis_parts.append("The requested resource was not found on the server.")
        else:
            analysis_parts.append(f"**Primary Root Cause**: {error_info.get('http_code', 'Unknown')} Error")
            analysis_parts.append("An error occurred during request processing.")
        
        analysis_parts.append("")
        analysis_parts.append("**Evidence**:")
        analysis_parts.append(f"- Service: {error_info.get('service', 'Unknown')}")
        analysis_parts.append(f"- Environment: {error_info.get('env', 'Unknown')}")
        analysis_parts.append(f"- Exception: {error_info.get('exception', 'Unknown')}")
        analysis_parts.append(f"- Traces found: {error_info.get('traces', '0')}")
        analysis_parts.append(f"- Spans found: {error_info.get('spans', '0')}")
        
        analysis_parts.append("")
        analysis_parts.append("**Recommendations**:")
        analysis_parts.append("1. Check server logs for detailed error information")
        analysis_parts.append("2. Verify service connectivity and dependencies")
        analysis_parts.append("3. Review recent deployments or configuration changes")
        analysis_parts.append("4. Monitor system resources (CPU, memory, disk)")
        
        return "\n".join(analysis_parts)
    
    def _simple_analysis(self, error_card: Dict, trace_ids: list, span_metadata: list, logs: Dict) -> str:
        """
        Simple analysis without LLM
        """
        env = error_card.get("env", "UNSET")
        service = error_card.get("service", "unknown")
        http_code = error_card.get("http_code", "unknown")
        exception = error_card.get("exception", "unknown")
        count = error_card.get("count", 0)
        
        analysis = f"""
## Root Cause Analysis

**Error Summary:**
- Environment: {env}
- Service: {service}
- HTTP Code: {http_code}
- Exception: {exception}
- Error Count: {count}
- Traces Found: {len(trace_ids)}
- Spans Found: {len(span_metadata)}
- Logs Found: {sum(len(logs_list) for logs_list in logs.values())}

**Primary Root Cause**: {http_code} Error in {service}
This indicates a server-side issue that requires investigation.

**Evidence:**
- Multiple traces ({len(trace_ids)}) indicate distributed system involvement
- Span data ({len(span_metadata)} spans) shows request flow through services
- Log correlation provides additional context for debugging

**Recommendations:**
1. Check {service} logs for detailed error messages
2. Verify service dependencies and connectivity
3. Review recent deployments or configuration changes
4. Monitor system resources and performance metrics
5. Investigate related traces for root cause patterns

**Data Quality**: {'Good' if len(trace_ids) > 0 and len(span_metadata) > 0 else 'Limited - missing trace/span data'}
"""
        
        return analysis.strip()
    
    def _build_analysis_prompt(self, error_card: Dict, trace_ids: list, span_metadata: list, logs: Dict) -> str:
        """
        Build a comprehensive prompt for RCA analysis
        """
        env = error_card.get("env", "UNSET")
        service = error_card.get("service", "unknown")
        http_code = error_card.get("http_code", "unknown")
        exception = error_card.get("exception", "unknown")
        count = error_card.get("count", 0)
        window_start = error_card.get("window_start", "")
        window_end = error_card.get("window_end", "")
        
        prompt = f"""
Analyze this error and provide root cause analysis:

Error Details:
- Environment: {env}
- Service: {service}
- HTTP Code: {http_code}
- Exception: {exception}
- Error Count: {count}
- Time Window: {window_start} to {window_end}

Trace Information:
- Number of Traces: {len(trace_ids)}
- Trace IDs: {', '.join(trace_ids) if trace_ids else 'None found'}

Span Information:
- Number of Spans: {len(span_metadata)}
"""

        if span_metadata:
            prompt += "\nSpan Details:\n"
            for i, span in enumerate(span_metadata[:5]):  # Limit to first 5 spans
                prompt += f"""
Span {i+1}:
- Operation: {span.get('operation_name', 'unknown')}
- Duration: {span.get('duration', 'unknown')}ms
- Start Time: {span.get('start_time', 'unknown')}
"""
        
        prompt += "\nLog Information:\n"
        total_logs = 0
        for trace_id, log_list in logs.items():
            log_count = len(log_list)
            total_logs += log_count
            prompt += f"- Trace {trace_id}: {log_count} logs\n"
        
        if total_logs == 0:
            prompt += "- No logs found for any traces\n"
        
        prompt += """

Please provide a comprehensive root cause analysis including:
1. Primary Root Cause
2. Contributing Factors
3. Evidence from traces/logs
4. Immediate recommendations
5. Data quality assessment

Analysis:
"""
        
        return prompt 