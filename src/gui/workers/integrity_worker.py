"""SyncroJob - Shared Integrity Worker.

Worker riutilizzabile per la verifica dell'integrità dei log di audit.
"""

import logging

from PySide6.QtCore import QObject, QRunnable, Signal

from src.core.audit_manager import AuditManager

logger = logging.getLogger(__name__)


class IntegrityWorkerSignals(QObject):
    """Segnali emessi dal worker di verifica integrità dei log."""

    finished = Signal(bool)


class IntegrityWorker(QRunnable):
    """Worker per la verifica asincrona dell'hash di integrità del database di audit."""

    def __init__(self, manager: AuditManager) -> None:
        """Inizializza il worker comunicando con l'AuditManager."""
        super().__init__()
        self.manager = manager
        self.signals = IntegrityWorkerSignals()

    def run(self) -> None:
        """Esegue il controllo crittografico dell'integrità."""
        try:
            valid = self.manager.verify_integrity()
            self.signals.finished.emit(valid)
        except Exception:
            logger.exception("Errore durante la verifica integrità")
            self.signals.finished.emit(False)
