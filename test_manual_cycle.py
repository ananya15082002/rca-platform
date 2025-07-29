#!/usr/bin/env python3
"""
Test Manual Cycle for Specific Time Window
"""
import os
import sys
import datetime
import pytz
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
load_dotenv()

from app.ingestion import run_ingestion_cycle
from app.worker import RCAWorker

def test_manual_cycle():
    """Test manual cycle for a specific time window"""
    IST = pytz.timezone('Asia/Kolkata')
    
    # Test with a time window where we know there were errors (2:30-2:35)
    test_time = datetime.datetime(2025, 7, 30, 2, 35, 0, tzinfo=IST)
    
    print(f"🧪 Testing manual cycle for time window ending at: {test_time.strftime('%Y-%m-%d %H:%M:%S')} IST")
    
    # Create worker instance
    worker = RCAWorker()
    
    # Temporarily modify the worker's run_cycle to use our test time
    original_run_cycle = worker.run_cycle
    
    def test_run_cycle():
        """Modified run_cycle that uses our test time"""
        try:
            # Use test time as the END of the 5-minute window
            correlation_data_list = run_ingestion_cycle(test_time)
            
            if not correlation_data_list:
                print("No error cards found in this cycle")
                return
            
            print(f"📊 Processing {len(correlation_data_list)} error cards...")
            
            for idx, correlation_data in enumerate(correlation_data_list, 1):
                print(f"--- Processing Error Card {idx}/{len(correlation_data_list)} ---")
                
                # Save error metric
                error_metric = worker.save_error_metric(correlation_data['error_card'])
                if not error_metric:
                    continue
                
                # Save traces
                trace_ids_hex = correlation_data.get('trace_ids_hex', [])
                if trace_ids_hex:
                    worker.save_traces(error_metric.id, trace_ids_hex)
                else:
                    print("⚠ No traces found")
                
                # Save spans
                span_metadata = correlation_data.get('span_metadata', [])
                if span_metadata:
                    worker.save_spans(error_metric.id, span_metadata)
                else:
                    print("⚠ No spans found")
                
                # Save logs
                logs_dict = correlation_data.get('logs', {})
                log_count = 0
                if logs_dict:
                    log_count = worker.save_logs(error_metric.id, logs_dict)
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
                rca_summary = worker.rca_agent.analyze_error_card(correlation_data_for_rca)
                
                # Save RCA report
                rca_report = worker.save_rca_report(error_metric.id, rca_summary)
                
                # Send Google Chat alert
                print("📤 Sending Google Chat alert...")
                try:
                    worker.chat_notifier.send_error_alert(
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
    
    # Replace the run_cycle method temporarily
    worker.run_cycle = test_run_cycle
    
    # Run cycle for this specific time
    try:
        worker.run_cycle()
        print("✅ Manual cycle completed successfully")
    except Exception as e:
        print(f"❌ Error in manual cycle: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_manual_cycle() 