"""
SyncroJob - Audit Manager Facade
Modulo di compatibilità che delega al nuovo package modulare src.core.audit.
"""

from src.core.audit.manager import AuditManager
from src.core.audit.models import Severity, Status
from src.core.audit.signals import AuditSignals
from src.core.config_manager import CONFIG_DIR

__all__ = ["CONFIG_DIR", "AuditManager", "AuditSignals", "Severity", "Status"]
