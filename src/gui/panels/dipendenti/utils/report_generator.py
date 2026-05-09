"""
SyncroJob - Report Generator (Refactored)
Controller GUI asincrono per il workflow dei report dipendenti.
Delega le operazioni pesanti al ReportWorker per non bloccare la UI.
"""

import logging
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMessageBox

from src.gui.widgets.toast import ToastManager
from src.gui.workers.report_worker import ReportWorker

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Gestisce l'orchestrazione asincrona dei report dipendenti."""

    _worker: ReportWorker | None = None

    @staticmethod
    def generate_email_report(parent_widget: Any = None) -> None:
        """Avvia la generazione del report in background."""
        if ReportGenerator._worker and ReportGenerator._worker.isRunning():
            ToastManager.instance().show("Generazione report già in corso...", "warning")
            return

        ReportGenerator._worker = ReportWorker()  # Senza parent perchè statico
        ReportGenerator._worker.finished_signal.connect(
            lambda success, msg, data: ReportGenerator._on_report_finished(parent_widget, success, msg, data)
        )
        ReportGenerator._worker.finished.connect(ReportGenerator._worker.deleteLater)

        ToastManager.instance().show("Preparazione report in corso...", "info")
        ReportGenerator._worker.start()

    @staticmethod
    def _on_report_finished(parent_widget: Any, success: bool, message: str, data: dict[str, Any]) -> None:
        """Callback al completamento del worker."""
        if not success:
            if "Outlook non disponibile" in message:
                ReportGenerator._fallback_browser(message, data)
            else:
                logger.error(f"Errore generazione report: {message}")
                if parent_widget:
                    QMessageBox.critical(
                        parent_widget, "Errore", f"Impossibile generare il report:\n{message}"
                    )
            return

        if message == "Nessun dato da segnalare":
            if parent_widget:
                QMessageBox.information(
                    parent_widget,
                    "Nessun dipendente",
                    "Ottimo! Non ci sono dipendenti in scadenza o scaduti.",
                )
            return

        ToastManager.instance().show(message, "success")

    @staticmethod
    def _fallback_browser(message: str, data: dict[str, Any]) -> None:
        """Gestisce l'apertura del report nel browser se Outlook fallisce."""
        from src.core.dipendenti.report_service import ReportService

        try:
            body_html = ReportService.build_report_html(data)
            tmp_path = (
                Path(os.environ["TEMP"])
                / f"report_isab_{datetime.now(UTC).astimezone().strftime('%H%M%S')}.html"
            )
            tmp_path.write_text(body_html, encoding="utf-8")

            QDesktopServices.openUrl(QUrl.fromLocalFile(str(tmp_path)))

            from src.core.report_history import ReportHistory

            ReportHistory.save_report(data["warning_list"], data["expired_list"])

            ToastManager.instance().show(message, "warning", duration=4000)
        except Exception as e:
            logger.exception("Errore fallback report browser", exc=e)
            ToastManager.instance().show("Impossibile aprire il report nel browser", "error")
