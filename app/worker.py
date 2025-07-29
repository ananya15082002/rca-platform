#!/usr/bin/env python3
"""
RCA Worker - Background worker for continuous ingestion and analysis
"""
import os
import sys
import time
import datetime
import pytz
from dotenv import load_dotenv

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
load_dotenv()

from app.ingestion import run_ingestion_cycle
from app.database import get_db
from app.models import ErrorMetric, Trace, Span, Log, RCAReport
from app.google_chat import GoogleChatNotifier

# Import simplified RCA agent for Railway
try:
    from app.rca_agent import RCAAgent
    print("✓ Using full LLM RCA agent")
except ImportError:
    from app.rca_agent_simple import SimpleRCAAgent
    RCAAgent = SimpleRCAAgent
    print("✓ Using simplified RCA agent for Railway")

class RCAWorker:
    def __init__(self):
        self.ist = pytz.timezone('Asia/Kolkata')
        self.rca_agent = RCAAgent()
        self.chat_notifier = GoogleChatNotifier()
    
    def save_error_metric(self, error_card):
        """Save error metric to database"""
        try:
            with get_db() as db:
                error_metric = ErrorMetric(
                    env=error_card.get('env', ''),
                    service=error_card.get('service', ''),
                    span_kind=error_card.get('span_kind', ''),
                    http_code=error_card.get('http_code', ''),
                    exception=error_card.get('exception', ''),
                    root_name=error_card.get('root_name', ''),
                    count=error_card.get('count', 0),
                    window_start=error_card.get('window_start'),
                    window_end=error_card.get('window_end')
                )
                db.add(error_metric)
                db.commit()
                db.refresh(error_metric)
                print(f"✓ Saved error metric: {error_metric.id}")
                return error_metric
        except Exception as e:
            print(f"Error saving error metric: {e}")
            return None
    
    def save_traces(self, error_metric_id, trace_ids_hex):
        """Save traces to database"""
        try:
            with get_db() as db:
                for trace_id_hex in trace_ids_hex:
                    trace = Trace(
                        error_metric_id=error_metric_id,
                        trace_id_hex=trace_id_hex,
                        trace_id_b64=trace_id_hex  # Simplified for Railway
                    )
                    db.add(trace)
                db.commit()
                print(f"✓ Saved {len(trace_ids_hex)} traces")
        except Exception as e:
            print(f"Error saving traces: {e}")
    
    def save_spans(self, error_metric_id, span_metadata):
        """Save spans to database"""
        try:
            with get_db() as db:
                for span in span_metadata:
                    # Parse start_time correctly
                    start_time = None
                    if span.get("start_time"):
                        try:
                            start_time = datetime.datetime.fromisoformat(
                                span.get("start_time").replace('Z', '+00:00')
                            )
                        except:
                            start_time = None
                    
                    span_record = Span(
                        error_metric_id=error_metric_id,
                        trace_id_hex=span.get("trace_id_hex"),
                        span_id=span.get("span_id"),
                        operation_name=span.get("operation_name"),
                        start_time=start_time,
                        duration=span.get("duration"),
                        tags=span.get("tags", {})
                    )
                    db.add(span_record)
                db.commit()
                print(f"✓ Saved {len(span_metadata)} spans")
        except Exception as e:
            print(f"Error saving spans: {e}")
    
    def save_logs(self, error_metric_id, logs_dict):
        """Save logs to database"""
        try:
            with get_db() as db:
                log_count = 0
                for trace_id_hex, logs in logs_dict.items():
                    for log in logs:
                        log_record = Log(
                            error_metric_id=error_metric_id,
                            trace_id_hex=trace_id_hex,
                            log_data=log
                        )
                        db.add(log_record)
                        log_count += 1
                db.commit()
                print(f"✓ Saved {log_count} logs")
                return log_count
        except Exception as e:
            print(f"Error saving logs: {e}")
            return 0
    
    def save_rca_report(self, error_metric_id, rca_summary):
        """Save RCA report to database"""
        try:
            with get_db() as db:
                rca_report = RCAReport(
                    error_metric_id=error_metric_id,
                    analysis_summary=rca_summary,
                    correlation_data={}  # Simplified for Railway
                )
                db.add(rca_report)
                db.commit()
                db.refresh(rca_report)
                print(f"✓ Saved RCA report: {rca_report.id}")
                return rca_report
        except Exception as e:
            print(f"Error saving RCA report: {e}")
            return None
    
    def run_cycle(self):
        """Run one ingestion cycle"""
        try:
            # Use current time as the END of the 5-minute window
            window_end_dt = datetime.datetime.now(self.ist)
            correlation_data_list = run_ingestion_cycle(window_end_dt)
            
            if not correlation_data_list:
                print("No error cards found in this cycle")
                return
            
            print(f"📊 Processing {len(correlation_data_list)} error cards...")
            
            for idx, correlation_data in enumerate(correlation_data_list, 1):
                print(f"--- Processing Error Card {idx}/{len(correlation_data_list)} ---")
                
                # Save error metric
                error_metric = self.save_error_metric(correlation_data['error_card'])
                if not error_metric:
                    continue
                
                # Save traces
                trace_ids_hex = correlation_data.get('trace_ids_hex', [])
                if trace_ids_hex:
                    self.save_traces(error_metric.id, trace_ids_hex)
                else:
                    print("⚠ No traces found")
                
                # Save spans
                span_metadata = correlation_data.get('span_metadata', [])
                if span_metadata:
                    self.save_spans(error_metric.id, span_metadata)
                else:
                    print("⚠ No spans found")
                
                # Save logs
                logs_dict = correlation_data.get('logs', {})
                log_count = 0
                if logs_dict:
                    log_count = self.save_logs(error_metric.id, logs_dict)
                else:
                    print("⚠ No logs found")
                
                # Generate RCA analysis
                print("🤖 Generating RCA analysis...")
                correlation_data_for_rca = {
                    'error_card': correlation_data['error_card'],
                    'trace_ids_hex': correlation_data.get('trace_ids_hex', []),
                    'span_metadata': correlation_data.get('span_metadata', []),
                    'logs': correlation_data.get('logs', {})
                }
                rca_summary = self.rca_agent.analyze_error_card(correlation_data_for_rca)
                
                # Save RCA report
                rca_report = self.save_rca_report(error_metric.id, rca_summary)
                
                # Send Google Chat alert
                print("📤 Sending Google Chat alert...")
                try:
                    self.chat_notifier.send_error_alert(
                        correlation_data['error_card'],
                        rca_summary,
                        error_metric.id
                    )
                    print(f"✓ Google Chat alert sent successfully for error {error_metric.id}")
                except Exception as e:
                    print(f"Error sending Google Chat alert: {e}")
                
                # Log completion
                completion_data = {
                    'error_metric_id': error_metric.id,
                    'rca_id': rca_report.id if rca_report else None,
                    'trace_count': len(trace_ids_hex),
                    'span_count': len(span_metadata),
                    'log_count': log_count,
                    'rca_summary': rca_summary
                }
                print(f"✓ Completed processing: {completion_data}")
            
            print("✅ RCA cycle completed successfully")
            
        except Exception as e:
            print(f"Error in RCA cycle: {e}")
    
    def run_continuous(self):
        """Run continuous ingestion cycles"""
        print("🚀 Starting RCA Worker...")
        
        # Run initial cycle
        self.run_cycle()
        
        while True:
            try:
                # Calculate time until next 5-minute boundary
                now = datetime.datetime.now(self.ist)
                next_boundary = now.replace(second=0, microsecond=0)
                next_boundary = next_boundary + datetime.timedelta(minutes=5 - (now.minute % 5))
                
                wait_seconds = (next_boundary - now).total_seconds()
                print(f"⏰ Waiting {int(wait_seconds)} seconds until next cycle...")
                time.sleep(wait_seconds)
                
                print(f"🔄 Starting RCA cycle at {datetime.datetime.now(self.ist).strftime('%Y-%m-%d %H:%M:%S')} IST")
                self.run_cycle()
                
            except KeyboardInterrupt:
                print("\n🛑 RCA Worker stopped by user")
                break
            except Exception as e:
                print(f"Error in continuous cycle: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

if __name__ == "__main__":
    worker = RCAWorker()
    worker.run_continuous() 