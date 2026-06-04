"""SyncroJob - Audit Manager Facade.

Modulo di compatibilit  che delega al nuovo package modulare src.application.services.audit.
"""

from src.application.services.audit.manager import AuditManager
from src.application.services.audit.models import Severity, Status
from src.application.services.audit.signals import AuditSignals
from src.application.services.paths import CONFIG_DIR

__all__ = ["CONFIG_DIR", "AuditManager", "AuditSignals", "Severity", "Status"]
