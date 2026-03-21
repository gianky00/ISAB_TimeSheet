"""
SyncroJob - Report Worker
Thread worker per la generazione asincrona dei report.
Gestisce l'integrazione con Outlook nel thread dedicato.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from PyQt6.QtCore import QThread, pyqtSignal

from src.core.dipendenti.report_service import ReportService
from src.core.report_history import ReportHistory

logger = logging.getLogger(__name__)

class ReportWorker(QThread):
    """Worker per l'esecuzione asincrona del workflow di reporting."""

    finished_signal = pyqtSignal(bool, str, dict) # success, message, data

    def __init__(self):
        super().__init__()

    def run(self):
        """Esegue il ciclo completo di generazione report."""
        try:
            # 1. Raccolta dati (CORE)
            report_data = ReportService.gather_report_data()
            if not report_data["warning_list"] and not report_data["expired_list"]:
                self.finished_signal.emit(True, "Nessun dato da segnalare", report_data)
                return

            # 2. Generazione HTML (CORE)
            body_html = ReportService.build_report_html(report_data)

            # 3. Generazione Excel (CORE/Pandas)
            excel_path = ReportService.create_report_excel(
                report_data["warning_list"], report_data["expired_list"]
            )

            # 4. Invio/Display Outlook (Win32 COM)
            success, msg = self._handle_outlook(body_html, excel_path, report_data)
            self.finished_signal.emit(success, msg, report_data)

        except Exception as e:
            logger.error(f"ReportWorker Error: {e}", exc_info=True)
            self.finished_signal.emit(False, str(e), {})

    def _handle_outlook(self, body_html: str, excel_path: Path | None, report_data: dict[str, Any]) -> tuple[bool, str]:
        """Gestisce l'automazione Outlook."""
        subject = f"Report Monitoraggio Accessi in ISAB - {datetime.now().strftime('%d/%m/%Y')}"

        if os.name == "nt":
            try:
                import pythoncom
                import win32com.client

                from src.core.constants import Emails

                pythoncom.CoInitialize()
                try:
                    outlook = win32com.client.Dispatch("Outlook.Application")
                    mail = outlook.CreateItem(0)
                    mail.To = Emails.ACCESSI_TO
                    mail.CC = Emails.ACCESSI_CC
                    mail.Subject = subject
                    mail.HTMLBody = body_html
                    if excel_path and excel_path.exists():
                        mail.Attachments.Add(str(excel_path))
                    mail.Display()

                    ReportHistory.save_report(report_data["warning_list"], report_data["expired_list"])
                    return True, "Report generato in Outlook con allegato Excel"
                finally:
                    pythoncom.CoUninitialize()
            except Exception as e:
                logger.warning(f"Outlook automation error: {e}")

        # Fallback Browser (ritorno info alla GUI per apertura finale)
        return False, "Outlook non disponibile: generata anteprima browser"
