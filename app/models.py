from sqlalchemy import Column, Integer, String, DateTime, Float, Text, JSON, Index
from sqlalchemy.sql import func
from app.database import Base
import uuid

class ErrorMetric(Base):
    __tablename__ = "error_metrics"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    env = Column(String, nullable=True)
    service = Column(String, nullable=True)
    span_kind = Column(String, nullable=True)
    http_code = Column(String, nullable=True)
    exception = Column(String, nullable=True)
    root_name = Column(String, nullable=True)
    count = Column(Float, nullable=False)
    window_start = Column(DateTime, nullable=False)
    window_end = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index('idx_error_metrics_timestamp', 'window_start', 'window_end'),
        Index('idx_error_metrics_env_service', 'env', 'service'),
    )

class Trace(Base):
    __tablename__ = "traces"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    error_metric_id = Column(String, nullable=False)
    trace_id_b64 = Column(String, nullable=True)
    trace_id_hex = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index('idx_traces_error_metric', 'error_metric_id'),
        Index('idx_traces_trace_id', 'trace_id_hex'),
    )

class Span(Base):
    __tablename__ = "spans"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    error_metric_id = Column(String, nullable=False)
    trace_id_hex = Column(String, nullable=True)
    span_id = Column(String, nullable=True)
    operation_name = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)
    tags = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index('idx_spans_error_metric', 'error_metric_id'),
        Index('idx_spans_trace_id', 'trace_id_hex'),
        Index('idx_spans_start_time', 'start_time'),
    )

class Log(Base):
    __tablename__ = "logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    error_metric_id = Column(String, nullable=False)
    trace_id_hex = Column(String, nullable=True)
    log_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index('idx_logs_error_metric', 'error_metric_id'),
        Index('idx_logs_trace_id', 'trace_id_hex'),
        Index('idx_logs_created_at', 'created_at'),
    )

class RCAReport(Base):
    __tablename__ = "rca_reports"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    error_metric_id = Column(String, nullable=False)
    analysis_summary = Column(Text, nullable=True)
    correlation_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    __table_args__ = (
        Index('idx_rca_error_metric', 'error_metric_id'),
        Index('idx_rca_created_at', 'created_at'),
    ) 