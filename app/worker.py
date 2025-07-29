import asyncio
import datetime
import pytz
from app.ingestion import run_ingestion_cycle
from app.database import get_db
from app.models import ErrorMetric, Trace, Span, Log, RCAReport
from app.rca_agent import RCAAgent
from app.google_chat import GoogleChatNotifier

class RCAWorker:
    def __init__(self):
        self.ist = pytz.timezone('Asia/Kolkata')
        self.rca_agent = RCAAgent()
        self.chat_notifier = GoogleChatNotifier()
        
    def save_error_metric(self, card):
        """Save error metric to database"""
        db = next(get_db())
        try:
            error_metric = ErrorMetric(
                env=card.get('env'),
                service=card.get('service'),
                span_kind=card.get('span_kind'),
                http_code=card.get('http_code'),
                exception=card.get('exception'),
                root_name=card.get('root_name'),
                count=card.get('count'),
                window_start=card.get('window_start'),
                window_end=card.get('window_end')
            )
            db.add(error_metric)
            db.commit()
            db.refresh(error_metric)
            print(f"✓ Saved error metric: {error_metric.id}")
            return error_metric
        except Exception as e:
            print(f"Error saving error metric: {e}")
            db.rollback()
            return None
        finally:
            db.close()
    
    def save_traces(self, error_metric_id, trace_ids_hex):
        """Save traces to database"""
        db = next(get_db())
        try:
            for trace_id in trace_ids_hex:
                trace = Trace(
                    error_metric_id=error_metric_id,
                    trace_id_hex=trace_id
                )
                db.add(trace)
            db.commit()
            print(f"✓ Saved {len(trace_ids_hex)} traces")
        except Exception as e:
            print(f"Error saving traces: {e}")
            db.rollback()
        finally:
            db.close()
    
    def save_spans(self, error_metric_id, span_metadata):
        """Save spans to database"""
        db = next(get_db())
        try:
            for span_data in span_metadata:
                span = Span(
                    error_metric_id=error_metric_id,
                    trace_id_hex=span_data.get('trace_id_hex'),
                    span_id=span_data.get('span_id'),
                    operation_name=span_data.get('operation_name'),
                    start_time=datetime.datetime.fromisoformat(span_data.get("start_time").replace('Z', '+00:00')) if span_data.get("start_time") else None,
                    duration=span_data.get('duration'),
                    tags=span_data.get('tags')
                )
                db.add(span)
            db.commit()
            print(f"✓ Saved {len(span_metadata)} spans")
        except Exception as e:
            print(f"Error saving spans: {e}")
            db.rollback()
        finally:
            db.close()
    
    def save_logs(self, error_metric_id, logs_dict):
        """Save logs to database"""
        db = next(get_db())
        try:
            total_logs = 0
            for trace_id, logs_list in logs_dict.items():
                for log_data in logs_list:
                    log = Log(
                        error_metric_id=error_metric_id,
                        trace_id_hex=trace_id,
                        log_data=log_data
                    )
                    db.add(log)
                    total_logs += 1
            db.commit()
            print(f"✓ Saved {total_logs} logs")
            return total_logs
        except Exception as e:
            print(f"Error saving logs: {e}")
            db.rollback()
            return 0
        finally:
            db.close()
    
    def save_rca_report(self, error_metric_id, rca_summary):
        """Save RCA report to database"""
        db = next(get_db())
        try:
            rca_report = RCAReport(
                error_metric_id=error_metric_id,
                analysis_summary=rca_summary
            )
            db.add(rca_report)
            db.commit()
            db.refresh(rca_report)
            print(f"✓ Saved RCA report: {rca_report.id}")
            return rca_report
        except Exception as e:
            print(f"Error saving RCA report: {e}")
            db.rollback()
            return None
        finally:
            db.close()
    
    def run_cycle(self):
        """Run one complete RCA cycle"""
        try:
            # Use current time as the END of the 5-minute window to process the last 5 minutes
            current_time = datetime.datetime.now(self.ist)
            
            # Run ingestion cycle with current time as window end
            correlation_data_list = run_ingestion_cycle(current_time)
            
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
                correlation_data = {
                    'error_card': correlation_data['error_card'],
                    'trace_ids_hex': correlation_data.get('trace_ids_hex', []),
                    'span_metadata': correlation_data.get('span_metadata', []),
                    'logs': correlation_data.get('logs', {})
                }
                rca_summary = self.rca_agent.analyze_error_card(correlation_data)
                
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
        """Run continuous RCA cycles every 5 minutes"""
        print("🚀 Starting RCA Background Worker...")
        
        # Run first cycle immediately
        print("🔄 Running initial cycle...")
        self.run_cycle()
        
        while True:
            try:
                # Calculate time until next 5-minute boundary
                now = datetime.datetime.now(self.ist)
                next_boundary = now.replace(second=0, microsecond=0)
                next_boundary = next_boundary.replace(minute=((next_boundary.minute // 5) + 1) * 5)
                if next_boundary.minute == 60:
                    next_boundary = next_boundary.replace(hour=next_boundary.hour + 1, minute=0)
                
                wait_seconds = (next_boundary - now).total_seconds()
                if wait_seconds > 0:
                    print(f"⏰ Waiting {int(wait_seconds)} seconds until next cycle...")
                    asyncio.sleep(wait_seconds)
                
                print(f"🔄 Starting RCA cycle at {next_boundary.strftime('%Y-%m-%d %H:%M:%S')} IST")
                self.run_cycle()
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping RCA Worker...")
                break
            except Exception as e:
                print(f"Error in continuous cycle: {e}")
                asyncio.sleep(60)  # Wait 1 minute before retrying 