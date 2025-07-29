import requests 
import os
import json
import time
import pytz
import datetime
import base64
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()

# ---- CONFIG ----
IST = pytz.timezone('Asia/Kolkata')
METRIC_URL = os.getenv('METRIC_URL', 'http://observability-prod.fxtrt.io:3130/api/metrics/api/v1/query_range')
TRACE_BASE_URL = os.getenv('TRACE_BASE_URL', "https://cubeapm-newrelic-prod.fxtrt.io/api/traces/api/v1/search")
LOGS_API_URL = os.getenv('LOGS_API_URL', "http://observability-prod.fxtrt.io:3130/api/logs/select/logsql/query")

def to_epoch(s):
    return int(time.mktime(time.strptime(s, "%Y-%m-%d %H:%M:%S")))

def get_next_5min_boundary():
    """Return epoch seconds of next 5-min boundary (IST)."""
    now = datetime.datetime.now(IST)
    minute = ((now.minute // 5) + 1) * 5
    if minute == 60:
        # Move to next hour
        boundary = now.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)
    else:
        boundary = now.replace(minute=minute, second=0, microsecond=0)
    return boundary

def get_5min_window_epoch(window_end_dt):
    """Given a datetime (window_end), return window_start, window_end (as epoch, IST string)."""
    window_start = window_end_dt - datetime.timedelta(minutes=5)
    start_utc = int(window_start.astimezone(pytz.utc).timestamp())
    end_utc = int(window_end_dt.astimezone(pytz.utc).timestamp())
    return start_utc, end_utc, window_start.strftime("%Y-%m-%d %H:%M:%S"), window_end_dt.strftime("%Y-%m-%d %H:%M:%S")

def fetch_error_metrics(start_epoch, end_epoch, start_str, end_str):
    query = 'sum(increase(cube_apm_calls_total{span_kind=~"server|consumer",http_code=~"5.."}[5m])) by (env,service,root_name,http_code,exception,span_kind)'
    data = {
        "query": query,
        "start": start_epoch,
        "end": end_epoch,
        "step": "60"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = requests.post(METRIC_URL, data=data, headers=headers, timeout=30)
    r.raise_for_status()
    result = r.json()
    filtered = [
        {
            "env": m["metric"].get("env"),
            "service": m["metric"].get("service"),
            "span_kind": m["metric"].get("span_kind"),
            "http_code": m["metric"].get("http_code"),
            "exception": m["metric"].get("exception"),
            "root_name": m["metric"].get("root_name"),
            "count": float(m["values"][-1][1]),
            "window_start": start_str,
            "window_end": end_str
        }
        for m in result.get("data", {}).get("result", [])
        if float(m["values"][-1][1]) > 0
    ]
    return filtered

def base64_to_hex(trace_id_b64):
    try:
        raw = base64.b64decode(trace_id_b64 + "=" * (-len(trace_id_b64) % 4))
        return raw.hex()
    except Exception:
        return None

def build_trace_url(card, window_start, window_end):
    query_param = '"span_kind":in("server","consumer")'
    params = {
        "query": query_param,
        "sortBy": "",
        "index": "-",
        "env": card['env'],
        "service": card['service'],
        "host": "-",
        "version": "-",
        "category": "",
        "rootName": "",
        "spanName": "",
        "spanKind": "-",
        "start": to_epoch(window_start),
        "end": to_epoch(window_end),
        "status_code": card.get("http_code", ""),
        "exception": card.get("exception", ""),
        "limit": 100
    }
    query_string = f"query={query_param}"
    for k, v in params.items():
        if k != "query":
            query_string += f"&{k}={requests.utils.quote(str(v))}"
    return f"{TRACE_BASE_URL}?{query_string}"

def extract_trace_ids_and_spans(trace_bundle):
    trace_ids_b64 = set()
    trace_ids_hex = set()
    span_metadata = []
    if isinstance(trace_bundle, list):
        for t in trace_bundle:
            trace = t.get("trace")
            if not trace or not isinstance(trace, dict):
                continue
            for span in trace.get("spans", []):
                tid = span.get("trace_id")
                if tid:
                    trace_ids_b64.add(tid)
                    h = base64_to_hex(tid)
                    if h: trace_ids_hex.add(h)
                span_metadata.append({
                    "trace_id_b64": tid,
                    "trace_id_hex": h if tid else None,
                    "span_id": span.get("span_id"),
                    "operation_name": span.get("operation_name"),
                    "start_time": span.get("start_time"),
                    "duration": span.get("duration"),
                    "tags": span.get("tags"),
                })
    return list(trace_ids_b64), list(trace_ids_hex), span_metadata

def fetch_logs(trace_id, start_epoch, end_epoch, limit=1000):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    query_string = (
        f'{{}} _time:[{start_epoch},{end_epoch}) '
        f'(trace_id:="{trace_id}" OR trace.id:="{trace_id}")'
    )
    payload = [
        ("query", query_string),
        ("limit", str(limit))
    ]
    try:
        resp = requests.post(LOGS_API_URL, data=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        try:
            return resp.json()
        except Exception:
            # fallback: NDJSON/stream style
            lines = resp.text.splitlines()
            ndjson_objs = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                try:
                    ndjson_objs.append(json.loads(line))
                except Exception:
                    pass
            return ndjson_objs if ndjson_objs else None
    except Exception as e:
        return None

def run_ingestion_cycle(window_end_dt):
    """Run one 5-minute cycle (from window_end_dt - 5 min to window_end_dt)"""
    start_utc, end_utc, start_str, end_str = get_5min_window_epoch(window_end_dt)
    print(f"\n[Cycle] Fetching error metrics for {start_str} to {end_str} (IST)")
    error_cards = fetch_error_metrics(start_utc, end_utc, start_str, end_str)
    print(f"Found {len(error_cards)} error cards.\n")
    correlation_data_list = []

    for idx, card in enumerate(error_cards, 1):
        print(f"\n[Card {idx}] {card['env']} | {card['service']} | {card['window_start']} - {card['window_end']}")
        trace_url = build_trace_url(card, card['window_start'], card['window_end'])
        print(f"Trace URL: {trace_url}")
        try:
            r = requests.get(trace_url, timeout=30)
            traces_bundle = r.json()
            trace_ids_b64, trace_ids_hex, span_metadata = extract_trace_ids_and_spans(traces_bundle)
            print(f"Traces found: {len(trace_ids_hex)}")
        except Exception as e:
            print(f"[WARN] Could not fetch/parse traces for this card: {e}")
            trace_ids_hex, span_metadata = [], []
        
        trace_logs_dict = {}
        log_count_total = 0
        for trace_id in trace_ids_hex:
            logs_data = fetch_logs(trace_id, start_utc, end_utc)
            found = False
            logs_list = []
            if logs_data:
                if isinstance(logs_data, dict):
                    logs_list = logs_data.get("data", [])
                    if logs_list and isinstance(logs_list, list) and len(logs_list) > 0:
                        found = True
                elif isinstance(logs_data, list) and len(logs_data) > 0:
                    logs_list = logs_data
                    found = True
            trace_logs_dict[trace_id] = logs_list if found else []
            log_count_total += len(logs_list) if found else 0

        correlation_data = {
            "error_card": card,
            "trace_ids_hex": trace_ids_hex,
            "span_metadata": span_metadata,
            "logs": trace_logs_dict
        }
        correlation_data_list.append(correlation_data)
        print(f"[✓] Correlation completed for card {idx}")

    return correlation_data_list 