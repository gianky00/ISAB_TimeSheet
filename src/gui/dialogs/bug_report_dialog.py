import logging
import os
from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from src.core.bug_reporter import BugReporter
from src.core.config_manager import get_version

logger = logging.getLogger(__name__)


class ReportWorker(QThread):
    """Worker thread per generare il report senza bloccare la UI."""

    finished = pyqtSignal(bool, str, str)  # success, message, file_path

    def __init__(self, include_logs: bool):
        super().__init__()
        self.include_logs = include_logs

    def run(self):
        if self.include_logs:
            path, msg = BugReporter.collect_diagnostics()
            if path:
                self.finished.emit(True, msg, str(path))
            else:
                self.finished.emit(False, msg, "")
        else:
            self.finished.emit(False, "Invio solo testo non supportato.", "")


class BugReportDialog(QDialog):
    """Dialog per consentire all'utente di segnalare un bug."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Segnala un Problema")
        self.resize(550, 450)
        self.setup_ui()
        self.worker = None

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Style pulsanti (Hardcoded backup se stylesheet globale fallisce, ma usa colori standard app)
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
        lbl_info.setStyleSheet("font-size: 14px; color: #424242; margin-bottom: 10px;")
        lbl_info.setWordWrap(True)
        layout.addWidget(lbl_info)

        # Text Area
        self.txt_description = QTextEdit()
        self.txt_description.setPlaceholderText(
            "Es: Ho cliccato su Scarica PDL e l'app si è chiusa... Stavo lavorando sul cantiere X..."
        )
        self.txt_description.setStyleSheet(
            "background-color: white; border: 1px solid #BDBDBD; border-radius: 4px; padding: 8px;"
        )
        layout.addWidget(self.txt_description)

        # Options
        self.chk_include_logs = QCheckBox(
            "Includi file di log e screenshot di errore (Consigliato)"
        )
        self.chk_include_logs.setChecked(True)
        self.chk_include_logs.setStyleSheet("margin-top: 10px; font-weight: 500;")
        layout.addWidget(self.chk_include_logs)

        # Progress
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setRange(0, 0)  # Indeterminate
        self.progress.setStyleSheet(
            "QProgressBar { background: #E0E0E0; border: none; height: 6px; margin-top: 10px; } QProgressBar::chunk { background: #009688; }"
        )
        layout.addWidget(self.progress)

        # Buttons Area
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_cancel = QPushButton("Annulla")
        self.btn_cancel.setStyleSheet(
            "background-color: #757575; color: white; border-radius: 6px; padding: 10px 20px;"
        )
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_send = QPushButton("Invia con Outlook")
        self.btn_send.clicked.connect(self.start_generation)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_send)

        layout.addLayout(btn_layout)

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
        self.progress.setVisible(True)
        self.progress.setFormat("Generazione pacchetto diagnostico...")

        # Start Worker
        self.worker = ReportWorker(self.chk_include_logs.isChecked())
        self.worker.finished.connect(self.on_report_generated)
        self.worker.start()

    def on_report_generated(self, success: bool, msg: str, file_path: str):
        self.progress.setVisible(False)
        self.txt_description.setDisabled(False)
        self.btn_send.setDisabled(False)
        self.btn_cancel.setDisabled(False)

        if not success:
            QMessageBox.critical(self, "Errore Generazione", msg)
            return

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
                "Il report è stato generato. Per favore, scegli dove salvarlo e invialo manualmente.",
            )
            self.save_manually(file_path)

    def open_outlook(self, attachment_path: str, description: str) -> bool:
        """Apre una nuova mail in Outlook con destinatario, oggetto e allegato precompilati."""
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

            # Formati stringa
            date_display = now.strftime(
                "%d/%m/%Y %H:%M"
            )  # Es: 25/01/2026 12:30 (No underscore)
            date_file = now.strftime("%d-%m-%Y_%H-%M")  # Es: 25-01-2026_12-30 (Safe)

            rand_hex = f"{random.randint(0, 0xFFFF):04X}"
            ticket_id_suffix = f"TKT-{rand_hex}"

            # Stringhe complete
            # Oggetto: [Segnalazione Bug] SyncroJob v1.7.2 - 25/01/2026 12:38 TKT-34C8
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
            # Recupero Cliente (Fonte Ufficiale: License Validator come Footer)
            cliente_info = "ISAB S.R.L."
            try:
                from src.core.license_validator import get_license_info

                lic_data = get_license_info()
                if lic_data and "Cliente" in lic_data:
                    cliente_info = lic_data["Cliente"]
            except ImportError:
                # Fallback on config if validator missing
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

            # Costruzione Body HTML Layout 2 Colonne PULITO (No Giallo)
            css_table_cell = (
                "padding: 8px 12px; border-bottom: 1px solid #e0e0e0; color: #333;"
            )
            css_table_header = "padding: 8px 12px; border-bottom: 2px solid #009688; font-weight: 600; color: #009688; text-align: left;"

            html_body = f"""
            <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; max-width: 900px; font-size: 14px;">
                <h2 style="color: #009688; border-bottom: 2px solid #009688; padding-bottom: 10px; margin-top: 0; display: inline-block;">
                    Segnalazione Bug SyncroJob
                </h2>

                <!-- CONTAINER TABLE -->
                <table style="width: 100%; border-collapse: separate; border-spacing: 0; margin-top: 20px;">
                    <tr>
                        <!-- LEFT COLUMN: METADATA -->
                        <td style="width: 320px; vertical-align: top; padding-right: 30px;">
                            <table style="border-collapse: collapse; width: 100%; font-size: 13px;">
                                <tr>
                                    <th style="{css_table_header}" colspan="2">DETTAGLI SISTEMA</th>
                                </tr>
                                <tr>
                                    <td style="{css_table_cell} font-weight: 600;">Ticket ID</td>
                                    <td style="{css_table_cell} font-family: monospace; color: #d63384; font-weight: bold;">{ticket_id_suffix}</td>
                                </tr>
                                <tr>
                                    <td style="{css_table_cell} font-weight: 600;">Data/Ora</td>
                                    <td style="{css_table_cell}">{date_display}</td>
                                </tr>
                                <tr>
                                    <td style="{css_table_cell} font-weight: 600;">Versione</td>
                                    <td style="{css_table_cell}">{current_ver}</td>
                                </tr>
                                <tr>
                                    <td style="{css_table_cell} font-weight: 600;">Utente</td>
                                    <td style="{css_table_cell}">{current_user}</td>
                                </tr>
                                <tr>
                                    <td style="{css_table_cell} font-weight: 600;">Host</td>
                                    <td style="{css_table_cell}">{hostname}</td>
                                </tr>
                                <tr>
                                    <td style="{css_table_cell} font-weight: 600;">Cliente</td>
                                    <td style="{css_table_cell}">{cliente_info}</td>
                                </tr>
                                <tr>
                                    <td style="{css_table_cell} font-weight: 600;">HW ID</td>
                                    <td style="{css_table_cell} font-family: monospace; font-size: 12px;">{hw_id}</td>
                                </tr>
                            </table>
                        </td>

                        <!-- RIGHT COLUMN: DESCRIPTION -->
                        <td style="vertical-align: top;">
                            <h3 style="color: #444; margin-top: 0; margin-bottom: 15px; font-size: 16px; border-bottom: 2px solid #ddd; padding-bottom: 8px;">
                                Descrizione Problema
                            </h3>
                            <div style="font-size: 14px; line-height: 1.6; color: #222; min-height: 150px;">
                                {description.replace(chr(10), '<br>')}
                            </div>
                        </td>
                    </tr>
                </table>

                <!-- TECH INFO FOOTER -->
                <div style="margin-top: 40px; padding-top: 15px; border-top: 1px solid #eee; font-size: 12px; color: #666;">
                    <strong>Contenuto Allegato Tecnico:</strong> Log applicativi, Stacktrace errori critici, Configurazione ambiente, Screenshots.<br>
                    File: <code>{os.path.basename(final_zip_path)}</code>
                </div>
            </div>
            """

            mail.HTMLBody = html_body

            if os.path.exists(final_zip_path):
                mail.Attachments.Add(str(final_zip_path))

            mail.Display()  # Mostra la finestra all'utente
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
                    f"Report salvato in:\n{dest_path}\n\nInvia questo file a gianky.allegretti@gmail.com",
                )
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Errore Salva", f"Errore: {e}")
