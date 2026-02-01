"""
SyncroJob - Enhanced Bug Report Dialog

Dialog per segnalazione bug con opzioni avanzate:
- Opzioni configurabili (log enterprise, analytics, audit)
- Preview contenuto ZIP
- Integrazione Outlook
"""

import logging
import os
from pathlib import Path
from typing import List, Optional

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
)

from src.core.bug_reporter import BugReporter
from src.core.config_manager import get_version

logger = logging.getLogger(__name__)


class ReportWorker(QThread):
    """Worker thread per generare il report senza bloccare la UI."""

    finished = pyqtSignal(bool, str, str, list)  # success, message, file_path, files

    def __init__(
        self,
        include_logs: bool,
        include_analytics: bool,
        include_audit: bool,
        trace_id: Optional[str] = None,
    ):
        super().__init__()
        self.include_logs = include_logs
        self.include_analytics = include_analytics
        self.include_audit = include_audit
        self.trace_id = trace_id

    def run(self):
        path, msg, files = BugReporter.collect_diagnostics(
            include_enterprise_logs=self.include_logs,
            include_analytics=self.include_analytics,
            include_audit=self.include_audit,
            trace_id=self.trace_id if self.trace_id else None,
        )
        if path:
            self.finished.emit(True, msg, str(path), files)
        else:
            self.finished.emit(False, msg, "", [])


class BugReportDialog(QDialog):
    """Dialog per consentire all'utente di segnalare un bug."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Segnala un Problema")
        self.resize(600, 550)
        self.setup_ui()
        self.worker = None
        self._update_size_estimate()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Style
        btn_style = """
            QPushButton {
                background-color: #009688;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
                min-width: 120px;
            }
            QPushButton:hover { background-color: #00897B; }
            QPushButton:pressed { background-color: #00796B; }
            QPushButton:disabled { background-color: #BDBDBD; color: #757575; }
        """
        self.setStyleSheet(btn_style)

        # Header
        lbl_info = QLabel(
            "Descrivi il problema riscontrato con il maggior dettaglio possibile.\n"
            "Se possibile, indica i passaggi per riprodurlo."
        )
        lbl_info.setStyleSheet("font-size: 14px; color: #424242; margin-bottom: 5px;")
        lbl_info.setWordWrap(True)
        layout.addWidget(lbl_info)

        # Text Area
        self.txt_description = QTextEdit()
        self.txt_description.setPlaceholderText(
            "Es: Ho cliccato su Scarica PDL e l'app si è chiusa... "
            "Stavo lavorando sul cantiere X..."
        )
        self.txt_description.setStyleSheet(
            "background-color: white; border: 1px solid #BDBDBD; "
            "border-radius: 4px; padding: 8px; min-height: 100px;"
        )
        self.txt_description.setMaximumHeight(120)
        layout.addWidget(self.txt_description)

        # Options Group
        options_group = QGroupBox("Contenuto Report")
        options_group.setStyleSheet(
            "QGroupBox { font-weight: 600; color: #424242; margin-top: 10px; }"
        )
        options_layout = QVBoxLayout(options_group)
        options_layout.setSpacing(8)

        self.chk_include_logs = QCheckBox("Includi Log Enterprise (app.json, app.log)")
        self.chk_include_logs.setChecked(True)
        self.chk_include_logs.toggled.connect(self._update_size_estimate)
        options_layout.addWidget(self.chk_include_logs)

        self.chk_include_analytics = QCheckBox(
            "Includi Analytics Report (anomalie, health score)"
        )
        self.chk_include_analytics.setChecked(True)
        self.chk_include_analytics.toggled.connect(self._update_size_estimate)
        options_layout.addWidget(self.chk_include_analytics)

        self.chk_include_audit = QCheckBox("Includi Audit Trail (ultime 50 azioni)")
        self.chk_include_audit.setChecked(True)
        self.chk_include_audit.toggled.connect(self._update_size_estimate)
        options_layout.addWidget(self.chk_include_audit)

        # Trace ID (optional)
        trace_layout = QHBoxLayout()
        trace_layout.setSpacing(8)
        lbl_trace = QLabel("Trace ID (opzionale):")
        lbl_trace.setStyleSheet("color: #666; font-size: 12px;")
        self.txt_trace_id = QLineEdit()
        self.txt_trace_id.setPlaceholderText("Es: abc123def456")
        self.txt_trace_id.setStyleSheet(
            "background: white; border: 1px solid #ddd; border-radius: 4px; "
            "padding: 4px 8px; font-family: monospace;"
        )
        self.txt_trace_id.setMaximumWidth(200)
        trace_layout.addWidget(lbl_trace)
        trace_layout.addWidget(self.txt_trace_id)
        trace_layout.addStretch()
        options_layout.addLayout(trace_layout)

        layout.addWidget(options_group)

        # Size Estimate
        self.lbl_size = QLabel("Dimensione stimata: ~50 KB")
        self.lbl_size.setStyleSheet("color: #666; font-size: 12px; margin-top: 5px;")
        layout.addWidget(self.lbl_size)

        # Privacy Warning
        warning_frame = QFrame()
        warning_frame.setStyleSheet(
            "background-color: #FFF3E0; border: 1px solid #FFB74D; "
            "border-radius: 6px; padding: 8px;"
        )
        warning_layout = QHBoxLayout(warning_frame)
        warning_layout.setContentsMargins(8, 8, 8, 8)
        lbl_warning = QLabel(
            "⚠️ Il report potrebbe contenere informazioni sensibili. "
            "Verifica il contenuto prima di inviare."
        )
        lbl_warning.setStyleSheet("color: #E65100; font-size: 12px;")
        lbl_warning.setWordWrap(True)
        warning_layout.addWidget(lbl_warning)
        layout.addWidget(warning_frame)

        # Progress
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setRange(0, 0)  # Indeterminate
        self.progress.setStyleSheet(
            "QProgressBar { background: #E0E0E0; border: none; height: 6px; } "
            "QProgressBar::chunk { background: #009688; }"
        )
        layout.addWidget(self.progress)

        # Preview Area (initially hidden)
        self.preview_group = QGroupBox("File inclusi nel report")
        self.preview_group.setVisible(False)
        preview_layout = QVBoxLayout(self.preview_group)
        self.preview_scroll = QScrollArea()
        self.preview_scroll.setWidgetResizable(True)
        self.preview_scroll.setMaximumHeight(100)
        self.preview_content = QLabel()
        self.preview_content.setStyleSheet(
            "font-family: monospace; font-size: 11px; color: #555;"
        )
        self.preview_content.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.preview_scroll.setWidget(self.preview_content)
        preview_layout.addWidget(self.preview_scroll)
        layout.addWidget(self.preview_group)

        # Buttons Area
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_cancel = QPushButton("Annulla")
        self.btn_cancel.setStyleSheet(
            "background-color: #757575; color: white; "
            "border-radius: 6px; padding: 10px 20px;"
        )
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_send = QPushButton("Genera e Invia")
        self.btn_send.clicked.connect(self.start_generation)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_send)

        layout.addLayout(btn_layout)

    def _update_size_estimate(self):
        """Aggiorna stima dimensione ZIP."""
        try:
            size = BugReporter.get_estimated_size(
                include_enterprise_logs=self.chk_include_logs.isChecked(),
                include_analytics=self.chk_include_analytics.isChecked(),
                include_audit=self.chk_include_audit.isChecked(),
            )
            self.lbl_size.setText(f"Dimensione stimata: {size}")
        except Exception:
            self.lbl_size.setText("Dimensione stimata: ~50 KB")

    def start_generation(self):
        desc = self.txt_description.toPlainText().strip()
        if len(desc) < 10:
            QMessageBox.warning(
                self,
                "Attenzione",
                "La descrizione è troppo breve. Per favore fornisci più dettagli.",
            )
            return

        # Disable UI
        self.txt_description.setDisabled(True)
        self.btn_send.setDisabled(True)
        self.btn_cancel.setDisabled(True)
        self.chk_include_logs.setDisabled(True)
        self.chk_include_analytics.setDisabled(True)
        self.chk_include_audit.setDisabled(True)
        self.txt_trace_id.setDisabled(True)
        self.progress.setVisible(True)

        # Get trace ID if provided
        trace_id = self.txt_trace_id.text().strip() or None

        # Start Worker
        self.worker = ReportWorker(
            include_logs=self.chk_include_logs.isChecked(),
            include_analytics=self.chk_include_analytics.isChecked(),
            include_audit=self.chk_include_audit.isChecked(),
            trace_id=trace_id,
        )
        self.worker.finished.connect(self.on_report_generated)
        self.worker.start()

    def on_report_generated(
        self, success: bool, msg: str, file_path: str, files: List[str]
    ):
        self.progress.setVisible(False)
        self._enable_ui()

        if not success:
            QMessageBox.critical(self, "Errore Generazione", msg)
            return

        # Show preview
        if files:
            self.preview_group.setVisible(True)
            self.preview_content.setText("\n".join(f"📄 {f}" for f in files))

        desc = self.txt_description.toPlainText().strip()

        # Tenta invio con Outlook
        if self.open_outlook(file_path, desc):
            self.accept()
        else:
            # Fallback manuale
            QMessageBox.warning(
                self,
                "Outlook non disponibile",
                "Impossibile aprire Outlook automaticamente.\n"
                "Il report è stato generato. Per favore, scegli dove salvarlo "
                "e invialo manualmente.",
            )
            self.save_manually(file_path)

    def _enable_ui(self):
        """Riabilita controlli UI."""
        self.txt_description.setDisabled(False)
        self.btn_send.setDisabled(False)
        self.btn_cancel.setDisabled(False)
        self.chk_include_logs.setDisabled(False)
        self.chk_include_analytics.setDisabled(False)
        self.chk_include_audit.setDisabled(False)
        self.txt_trace_id.setDisabled(False)

    def open_outlook(self, attachment_path: str, description: str) -> bool:
        """Apre una nuova mail in Outlook con destinatario, oggetto e allegato."""
        try:
            import getpass
            import platform
            import random
            from datetime import datetime

            import win32com.client as win32

            from src.core import config_manager

            # Check se Outlook è installato/accessibile
            try:
                outlook = win32.Dispatch("Outlook.Application")
            except Exception:
                return False

            # Genera Ticket ID Univoco
            now = datetime.now()
            date_display = now.strftime("%d/%m/%Y %H:%M")
            date_file = now.strftime("%d-%m-%Y_%H-%M")
            rand_hex = f"{random.randint(0, 0xFFFF):04X}"
            ticket_id_suffix = f"TKT-{rand_hex}"

            email_subject_suffix = f"{date_display} {ticket_id_suffix}"
            full_ticket_file = f"{date_file}_{ticket_id_suffix}"

            current_ver = get_version()
            current_user = getpass.getuser().upper()
            hostname = platform.node().upper()

            # Recupero Info Hardware
            hw_id = "UNKNOWN"
            try:
                import uuid

                hw_id = str(uuid.getnode())
            except Exception:
                pass

            # Recupero Cliente
            cliente_info = "ISAB S.R.L."
            try:
                from src.core.license_validator import get_license_info

                lic_data = get_license_info()
                if lic_data and "Cliente" in lic_data:
                    cliente_info = lic_data["Cliente"]
            except ImportError:
                config = config_manager.load_config()
                cliente_info = config.get("customer_name", "ISAB S.R.L.")

            mail = outlook.CreateItem(0)
            mail.To = "gianky.allegretti@gmail.com"
            mail.Subject = (
                f"[Segnalazione Bug] SyncroJob v{current_ver} - {email_subject_suffix}"
            )

            # Rename ZIP
            final_zip_path = attachment_path
            try:
                dir_name = os.path.dirname(attachment_path)
                new_name = f"{full_ticket_file}.zip"
                new_path = os.path.join(dir_name, new_name)
                if os.path.exists(new_path):
                    os.remove(new_path)
                os.rename(attachment_path, new_path)
                final_zip_path = new_path
            except Exception as e:
                logger.error(f"Errore rinomina ZIP: {e}")

            # Costruzione Body HTML
            css_cell = (
                "padding: 8px 12px; border-bottom: 1px solid #e0e0e0; color: #333;"
            )
            css_header = (
                "padding: 8px 12px; border-bottom: 2px solid #009688; "
                "font-weight: 600; color: #009688; text-align: left;"
            )

            html_body = f"""
            <div style="font-family: 'Segoe UI', Tahoma, sans-serif; color: #333; max-width: 900px; font-size: 14px;">
                <h2 style="color: #009688; border-bottom: 2px solid #009688; padding-bottom: 10px; margin-top: 0; display: inline-block;">
                    Segnalazione Bug SyncroJob
                </h2>

                <table style="width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 20px;">
                    <tr>
                        <td style="width: 320px; vertical-align: top; padding-right: 30px;">
                            <table style="border-collapse: collapse; width: 100%; font-size: 13px;">
                                <tr>
                                    <th style="{css_header}" colspan="2">DETTAGLI SISTEMA</th>
                                </tr>
                                <tr>
                                    <td style="{css_cell} font-weight: 600;">Ticket ID</td>
                                    <td style="{css_cell} font-family: monospace; color: #d63384; font-weight: bold;">{ticket_id_suffix}</td>
                                </tr>
                                <tr>
                                    <td style="{css_cell} font-weight: 600;">Data/Ora</td>
                                    <td style="{css_cell}">{date_display}</td>
                                </tr>
                                <tr>
                                    <td style="{css_cell} font-weight: 600;">Versione</td>
                                    <td style="{css_cell}">{current_ver}</td>
                                </tr>
                                <tr>
                                    <td style="{css_cell} font-weight: 600;">Utente</td>
                                    <td style="{css_cell}">{current_user}</td>
                                </tr>
                                <tr>
                                    <td style="{css_cell} font-weight: 600;">Host</td>
                                    <td style="{css_cell}">{hostname}</td>
                                </tr>
                                <tr>
                                    <td style="{css_cell} font-weight: 600;">Cliente</td>
                                    <td style="{css_cell}">{cliente_info}</td>
                                </tr>
                                <tr>
                                    <td style="{css_cell} font-weight: 600;">HW ID</td>
                                    <td style="{css_cell} font-family: monospace; font-size: 12px;">{hw_id}</td>
                                </tr>
                            </table>
                        </td>

                        <td style="vertical-align: top;">
                            <h3 style="color: #444; margin-top: 0; margin-bottom: 15px; font-size: 16px; border-bottom: 2px solid #ddd; padding-bottom: 8px;">
                                Descrizione Problema
                            </h3>
                            <div style="font-size: 14px; line-height: 1.6; color: #222; min-height: 150px;">
                                {description.replace(chr(10), "<br>")}
                            </div>
                        </td>
                    </tr>
                </table>

                <div style="margin-top: 40px; padding-top: 15px; border-top: 1px solid #eee; font-size: 12px; color: #666;">
                    <strong>Contenuto Allegato:</strong> Log enterprise, Analytics report, Audit trail, Info sistema, Screenshot errori.<br>
                    File: <code>{os.path.basename(final_zip_path)}</code>
                </div>
            </div>
            """

            mail.HTMLBody = html_body

            if os.path.exists(final_zip_path):
                mail.Attachments.Add(str(final_zip_path))

            mail.Display()
            return True
        except Exception as e:
            logger.error(f"Errore automazione Outlook: {e}")
            return False

    def save_manually(self, source_path: str):
        """Fallback per salvare lo ZIP se Outlook fallisce."""
        initial_name = Path(source_path).name
        desktop = Path(os.path.expanduser("~/Desktop"))
        dest_path, _ = QFileDialog.getSaveFileName(
            self, "Salva Report", str(desktop / initial_name), "ZIP Files (*.zip)"
        )
        if dest_path:
            try:
                import shutil

                shutil.copy2(source_path, dest_path)
                QMessageBox.information(
                    self,
                    "Salvato",
                    f"Report salvato in:\n{dest_path}\n\n"
                    "Invia questo file a gianky.allegretti@gmail.com",
                )
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Errore Salva", f"Errore: {e}")
