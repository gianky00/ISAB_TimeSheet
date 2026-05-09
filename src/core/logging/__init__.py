"""
SyncroJob - Enterprise Logging System
AI-ready structured logging con context propagation e performance monitoring.
"""

from .alert_manager import AlertConfig, AlertManager, get_alert_manager
from .analytics import (
    AnalyticsReport,
    Anomaly,
    AnomalyDetector,
    HealthScorer,
    Pattern,
    PatternDetector,
    generate_analytics_report,
    get_anomalies,
    get_health_score,
    get_patterns,
)
from .context import (
    LoggingContext,
    generate_span_id,
    generate_trace_id,
    get_context,
    get_current_audit_id,
    get_current_span_id,
    get_current_trace_id,
    set_audit_id,
    with_context,
)
from .decorators import log_entry_exit, measure_time
from .logger import configure_logging, get_logger, set_level
from .metrics import PerformanceTracker, get_tracker
from .sampling import ContextAwareSampler, get_sampler
from .sinks import get_aggregated_sink, get_bot_sink, get_metrics_sink
from .viewer import LogViewer, health_report, query_logs, view_trace

__all__ = [
    "AlertConfig",
    # Alerts
    "AlertManager",
    "AnalyticsReport",
    "Anomaly",
    # Analytics
    "AnomalyDetector",
    "ContextAwareSampler",
    "HealthScorer",
    # Viewer
    "LogViewer",
    "LoggingContext",
    "Pattern",
    "PatternDetector",
    "PerformanceTracker",
    "configure_logging",
    "generate_analytics_report",
    "generate_span_id",
    "generate_trace_id",
    "get_aggregated_sink",
    "get_alert_manager",
    "get_anomalies",
    # Sinks
    "get_bot_sink",
    "get_context",
    "get_current_audit_id",
    "get_current_span_id",
    "get_current_trace_id",
    "get_health_score",
    # Core
    "get_logger",
    "get_metrics_sink",
    "get_patterns",
    # Sampling
    "get_sampler",
    # Metrics
    "get_tracker",
    "health_report",
    "log_entry_exit",
    # Decorators
    "measure_time",
    "query_logs",
    "set_audit_id",
    "set_level",
    "view_trace",
    # Context
    "with_context",
]
