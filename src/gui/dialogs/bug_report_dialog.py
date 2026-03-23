"""
SyncroJob - Bug Report Dialog
Interfaccia avanzata per la raccolta diagnostica e la segnalazione di anomalie tecniche.
Gestisce la creazione di pacchetti ZIP contenenti log, analytics e audit trail, con integrazione Outlook.
"""

import logging
import os
from contextlib import suppress
from pathlib import Path

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QScrollArea,
    QVBoxLayout,
)

from src.core.bug_reporter import BugReporter
from src.core.config_manager import get_version
from src.gui.design.colors import get_palette
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import (
    PrimaryButton,
    StandardCheckBox,
    StandardGroupBox,
    StandardInput,
    StandardProgressBar,
    StandardTextEdit,
)

logger = logging.getLogger(__name__)


class ReportWorker(QThread):
    """
    Worker thread dedicato alla generazione del report diagnostico.
    Esegue la raccolta dei file e la compressione ZIP in background per non bloccare l'interfaccia utente.
    """

    finished = pyqtSignal(bool, str, str, list)
    """Segnale emesso al termine: (successo, messaggio, percorso_zip, lista_file_inclusi)."""

    def __init__(  # noqa: ANN204
        self,
        include_logs: bool,
        include_analytics: bool,
        include_audit: bool,
        trace_id: str | None = None,
    ):
        """
        Inizializza il worker con le opzioni di inclusione.

        Args:
            include_logs: Se includere i file log dell'applicazione.
            include_analytics: Se includere i report di analisi anomalie.
            include_audit: Se includere la traccia delle azioni utente.
            trace_id: ID opzionale per isolare una specifica transazione nei log.
        """
        super().__init__()
        self.include_logs = include_logs
        self.include_analytics = include_analytics
        self.include_audit = include_audit
        self.trace_id = trace_id

    def run(self):  # noqa: ANN201
        """Esegue il processo di raccolta diagnostica richiamando il core BugReporter."""
        path, msg, files = BugReporter.collect_diagnostics(
            include_enterprise_logs=self.include_logs,
            include_analytics=self.include_analytics,
            include_audit=self.include_audit,
            trace_id=self.trace_id or None,
        )
        if path:
            self.finished.emit(True, msg, str(path), files)
        else:
            self.finished.emit(False, msg, "", [])


class BugReportDialog(QDialog):
    """
    Dialog interattivo per la segnalazione di bug.
    Permette all'utente di descrivere il problema e scegliere quali dati diagnostici inviare.
    Supporta l'invio automatico tramite Outlook o il salvataggio manuale del file ZIP.
    """

    def __init__(self, parent=None):  # noqa: ANN001, ANN204
        """
        Inizializza il dialogo e configura l'interfaccia utente.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.setWindowTitle("Segnala un Problema")
        self.resize(600, 550)
        self.setup_ui()
        self.worker = None
        self._update_size_estimate()

    def setup_ui(self):  # noqa: ANN201, PLR0915
        """Configura il layout, i campi di testo, le checkbox delle opzioni e i pulsanti di azione."""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        palette = get_palette()

        # Style
        btn_style = f"""
            QPushButton {{
                background-color: {palette.primary}; color: {palette.on_primary}; border: none;
                padding: 10px 20px; border-radius: 6px; font-weight: 600; min-width: 120px;
            }}
            QPushButton:hover {{ background-color: {palette.primary_variant}; }}
            QPushButton:pressed {{ background-color: {palette.primary_variant}; }}
            QPushButton:disabled {{ background-color: {palette.disabled}; color: {COLORS["text_light"]}; }}
        """
        self.setStyleSheet(btn_style)

        # Header
        lbl_info = QLabel(
            "Descrivi il problema riscontrato con il maggior dettaglio possibile.\n"
            "Se possibile, indica i passaggi per riprodurlo."
        )
        lbl_info.setStyleSheet(f"font-size: 14px; color: {palette.on_surface}; margin-bottom: 5px;")
        lbl_info.setWordWrap(True)
        layout.addWidget(lbl_info)

        # Text Area
        self.txt_description = StandardTextEdit()
        self.txt_description.setPlaceholderText(
            "Es: Ho cliccato su Scarica PDL e l'app si è chiusa... Stavo lavorando sul cantiere X..."
        )
        self.txt_description.setStyleSheet(
            f"background-color: {palette.surface}; border: 1px solid {palette.border}; "
            "border-radius: 4px; padding: 8px; min-height: 100px;"
        )
        self.txt_description.setMaximumHeight(120)
        layout.addWidget(self.txt_description)

        # Options Group
        options_group = StandardGroupBox("Contenuto Report")
        options_group.setStyleSheet(
            f"QGroupBox {{ font-weight: 600; color: {palette.on_surface}; margin-top: 10px; }}"
        )
        options_layout = QVBoxLayout(options_group)
        options_layout.setSpacing(8)

        self.chk_include_logs = StandardCheckBox("Includi Log Enterprise (app.json, app.log)")
        self.chk_include_logs.setChecked(True)
        self.chk_include_logs.toggled.connect(self._update_size_estimate)
        options_layout.addWidget(self.chk_include_logs)

        self.chk_include_analytics = StandardCheckBox("Includi Analytics Report (anomalie, health score)")
        self.chk_include_analytics.setChecked(True)
        self.chk_include_analytics.toggled.connect(self._update_size_estimate)
        options_layout.addWidget(self.chk_include_analytics)

        self.chk_include_audit = StandardCheckBox("Includi Audit Trail (ultime 50 azioni)")
        self.chk_include_audit.setChecked(True)
        self.chk_include_audit.toggled.connect(self._update_size_estimate)
        options_layout.addWidget(self.chk_include_audit)

        # Trace ID (optional)
        trace_layout = QHBoxLayout()
        trace_layout.setSpacing(8)
        lbl_trace = QLabel("Trace ID (opzionale):")
        lbl_trace.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px;")
        self.txt_trace_id = StandardInput()
        self.txt_trace_id.setPlaceholderText("Es: abc123def456")
        self.txt_trace_id.setStyleSheet(
            f"background: {palette.surface}; border: 1px solid {palette.border}; border-radius: 4px; "
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
        self.lbl_size.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px; margin-top: 5px;")
        layout.addWidget(self.lbl_size)

        # Privacy Warning
        warning_frame = QFrame()
        warning_frame.setStyleSheet(
            f"background-color: {COLORS['bg_warning_pastel']}; border: 1px solid {COLORS['warning_light']}; border-radius: 6px; padding: 8px;"
        )
        warning_layout = QHBoxLayout(warning_frame)
        warning_layout.setContentsMargins(8, 8, 8, 8)
        lbl_warning = QLabel(
            "⚠️ Il report potrebbe contenere informazioni sensibili. Verifica il contenuto prima di inviare."
        )
        lbl_warning.setStyleSheet(f"color: {COLORS['warning_orange']}; font-size: 12px;")
        lbl_warning.setWordWrap(True)
        warning_layout.addWidget(lbl_warning)
        layout.addWidget(warning_frame)

        # Progress
        self.progress = StandardProgressBar()
        self.progress.setVisible(False)
        self.progress.setRange(0, 0)
        self.progress.setStyleSheet(
            f"QProgressBar {{ background: {palette.border}; border: none; height: 6px; }} "
            f"QProgressBar::chunk {{ background: {palette.primary}; }}"
        )
        layout.addWidget(self.progress)

        # Preview Area (initially hidden)
        self.preview_group = StandardGroupBox("File inclusi nel report")
        self.preview_group.setVisible(False)
        preview_layout = QVBoxLayout(self.preview_group)
        self.preview_scroll = QScrollArea()
        self.preview_scroll.setWidgetResizable(True)
        self.preview_scroll.setMaximumHeight(100)
        self.preview_content = QLabel()
        self.preview_content.setStyleSheet(
            f"font-family: monospace; font-size: 11px; color: {COLORS['text_muted']};"
        )
        self.preview_content.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.preview_scroll.setWidget(self.preview_content)
        preview_layout.addWidget(self.preview_scroll)
        layout.addWidget(self.preview_group)

        # Buttons Area
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_cancel = PrimaryButton("Annulla")
        self.btn_cancel.setStyleSheet(
            f"background-color: {COLORS['text_muted']}; color: white; border-radius: 6px; padding: 10px 20px;"
        )
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_send = PrimaryButton("Genera e Invia")
        self.btn_send.clicked.connect(self.start_generation)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_send)

        layout.addLayout(btn_layout)

    def _update_size_estimate(self):  # noqa: ANN202
        """Aggiorna dinamicamente la stima della dimensione del file ZIP finale."""
        try:
            size = BugReporter.get_estimated_size(
                include_enterprise_logs=self.chk_include_logs.isChecked(),
                include_analytics=self.chk_include_analytics.isChecked(),
                include_audit=self.chk_include_audit.isChecked(),
            )
            self.lbl_size.setText(f"Dimensione stimata: {size}")
        except Exception:
            self.lbl_size.setText("Dimensione stimata: ~50 KB")

    def start_generation(self):  # noqa: ANN201
        """Valida l'input e avvia il thread worker per la generazione del report."""
        desc = self.txt_description.toPlainText().strip()
        if len(desc) < 10:  # noqa: PLR2004
            QMessageBox.warning(
                self, "Attenzione", "La descrizione è troppo breve. Per favore fornisci più dettagli."
            )
            return

        # Disabilita UI
        self.txt_description.setDisabled(True)
        self.btn_send.setDisabled(True)
        self.btn_cancel.setDisabled(True)
        self.chk_include_logs.setDisabled(True)
        self.chk_include_analytics.setDisabled(True)
        self.chk_include_audit.setDisabled(True)
        self.txt_trace_id.setDisabled(True)
        self.progress.setVisible(True)

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

    def on_report_generated(self, success: bool, msg: str, file_path: str, files: list[str]):  # noqa: ANN201
        """
        Gestisce il completamento della generazione del report.
        Tenta l'invio tramite Outlook o propone il salvataggio manuale.
        """
        self.progress.setVisible(False)
        self._enable_ui()

        if not success:
            QMessageBox.critical(self, "Errore Generazione", msg)
            return

        if files:
            self.preview_group.setVisible(True)
            self.preview_content.setText("\n".join(f"📄 {f}" for f in files))

        desc = self.txt_description.toPlainText().strip()

        # Tenta invio con Outlook
        if self.open_outlook(file_path, desc):
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Outlook non disponibile",
                "Il report è stato generato. Per favore, scegli dove salvarlo e invialo manualmente.",
            )
            self.save_manually(file_path)

    def _enable_ui(self):  # noqa: ANN202
        """Riabilita i controlli dell'interfaccia utente al termine delle operazioni asincrone."""
        self.txt_description.setDisabled(False)
        self.btn_send.setDisabled(False)
        self.btn_cancel.setDisabled(False)
        self.chk_include_logs.setDisabled(False)
        self.chk_include_analytics.setDisabled(False)
        self.chk_include_audit.setDisabled(False)
        self.txt_trace_id.setDisabled(False)

    def open_outlook(self, attachment_path: str, description: str) -> bool:  # noqa: PLR0915
        """
        Apre una nuova mail in Outlook con destinatario, oggetto precompilato e allegato ZIP.
        Utilizza automazione COM via win32com.

        Args:
            attachment_path: Percorso del file ZIP da allegare.
            description: Descrizione del bug inserita dall'utente.

        Returns:
            bool: True se Outlook è stato aperto correttamente.
        """
        try:
            import getpass  # noqa: PLC0415
            import platform  # noqa: PLC0415
            import secrets  # noqa: PLC0415
            from datetime import UTC, datetime  # noqa: PLC0415

            import win32com.client as win32  # noqa: PLC0415

            try:
                outlook = win32.Dispatch("Outlook.Application")
            except Exception:
                return False

            now = datetime.now(UTC).astimezone()
            date_display = now.strftime("%d/%m/%Y %H:%M")
            date_file = now.strftime("%d-%m-%Y_%H-%M")
            rand_hex = f"{secrets.randbelow(0x10000):04X}"
            ticket_id_suffix = f"TKT-{rand_hex}"
            email_subject_suffix = f"{date_display} {ticket_id_suffix}"
            full_ticket_file = f"{date_file}_{ticket_id_suffix}"

            current_ver = get_version()
            current_user = getpass.getuser().upper()
            platform.node().upper()

            with suppress(Exception):
                import uuid  # noqa: PLC0415

                str(uuid.getnode())

            cliente_info = "ISAB S.R.L."
            with suppress(Exception):
                from src.core.constants import Emails  # noqa: PLC0415
                from src.core.license_validator import get_license_info  # noqa: PLC0415

                lic_data = get_license_info()
                if lic_data and "Cliente" in lic_data:
                    cliente_info = lic_data["Cliente"]

                mail = outlook.CreateItem(0)
                mail.To = Emails.SUPPORT
                mail.Subject = f"[Segnalazione Bug] SyncroJob v{current_ver} - {email_subject_suffix}"
                # Rinomina ZIP per includere Ticket ID
            final_zip_path = attachment_path
            with suppress(Exception):
                dir_name = os.path.dirname(attachment_path)
                new_path = os.path.join(dir_name, f"{full_ticket_file}.zip")
                if Path(new_path).exists():
                    Path(new_path).unlink()
                os.rename(attachment_path, new_path)
                final_zip_path = new_path

            palette = get_palette()
            css_cell = (
                f"padding: 8px 12px; border-bottom: 1px solid {palette.border}; color: {palette.on_surface};"
            )
            css_header = f"padding: 8px 12px; border-bottom: 2px solid {palette.primary}; font-weight: 600; color: {palette.primary};"

            html_body = f"""
            <div style="font-family: 'Segoe UI', sans-serif; color: {palette.on_surface}; max-width: 900px;">
                <h2 style="color: {palette.primary};">Segnalazione Bug SyncroJob</h2>
                <table style="width: 100%; border-collapse: separate; margin-top: 20px;">
                    <tr>
                        <td style="width: 320px; vertical-align: top;">
                            <table style="width: 100%; font-size: 13px;">
                                <tr><th style="{css_header}" colspan="2">DETTAGLI SISTEMA</th></tr>
                                <tr><td style="{css_cell} font-weight:600;">Ticket ID</td><td style="{css_cell}">{ticket_id_suffix}</td></tr>
                                <tr><td style="{css_cell} font-weight:600;">Versione</td><td style="{css_cell}">{current_ver}</td></tr>
                                <tr><td style="{css_cell} font-weight:600;">Utente</td><td style="{css_cell}">{current_user}</td></tr>
                                <tr><td style="{css_cell} font-weight:600;">Cliente</td><td style="{css_cell}">{cliente_info}</td></tr>
                            </table>
                        </td>
                        <td style="vertical-align: top; padding-left: 20px;">
                            <h3 style="border-bottom: 2px solid {palette.border};">Descrizione Problema</h3>
                            <div style="line-height: 1.6;">{description.replace(chr(10), "<br>")}</div>
                        </td>
                    </tr>
                </table>
            </div>
            """
            mail.HTMLBody = html_body
            if Path(final_zip_path).exists():
                mail.Attachments.Add(final_zip_path)
            mail.Display()
            return True  # noqa: TRY300
        except Exception as e:
            logger.error(f"Errore automazione Outlook: {e}")  # noqa: TRY400
            return False

    def save_manually(self, source_path: str):  # noqa: ANN201
        """
        Fallback per consentire all'utente di salvare il report ZIP in una posizione scelta manualmente.

        Args:
            source_path: Percorso del file ZIP temporaneo generato.
        """
        initial_name = Path(source_path).name
        desktop = Path(os.path.expanduser("~/Desktop"))
        dest_path, _ = QFileDialog.getSaveFileName(
            self, "Salva Report", str(desktop / initial_name), "ZIP Files (*.zip)"
        )
        if dest_path:
            try:
                import shutil  # noqa: PLC0415

                shutil.copy2(source_path, dest_path)
                QMessageBox.information(self, "Salvato", f"Report salvato in:\n{dest_path}")
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Errore Salva", f"Errore: {e}")
