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
    # Core
    "get_logger",
    "configure_logging",
    "set_level",
    # Context
    "with_context",
    "LoggingContext",
    "generate_trace_id",
    "generate_span_id",
    "get_context",
    "get_current_trace_id",
    "get_current_span_id",
    "set_audit_id",
    "get_current_audit_id",
    # Decorators
    "measure_time",
    "log_entry_exit",
    # Metrics
    "get_tracker",
    "PerformanceTracker",
    # Sampling
    "get_sampler",
    "ContextAwareSampler",
    # Viewer
    "LogViewer",
    "query_logs",
    "view_trace",
    "health_report",
    # Sinks
    "get_bot_sink",
    "get_metrics_sink",
    "get_aggregated_sink",
    # Analytics
    "AnomalyDetector",
    "PatternDetector",
    "HealthScorer",
    "Anomaly",
    "Pattern",
    "AnalyticsReport",
    "generate_analytics_report",
    "get_health_score",
    "get_anomalies",
    "get_patterns",
    # Alerts
    "AlertManager",
    "AlertConfig",
    "get_alert_manager",
]
