# mypy: disable-error-code="no-untyped-def, no-untyped-call, unused-ignore, arg-type"
"""
SyncroJob - Bug Report Dialog
Interfaccia avanzata per la raccolta diagnostica e la segnalazione di anomalie tecniche.
Gestisce la creazione di pacchetti ZIP contenenti log, analytics e audit trail, con integrazione Outlook.
"""

import getpass  # noqa: I001
import logging
import os
import secrets
import shutil
from typing import Any
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path

import win32com.client as win32
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core.bug_reporter import BugReporter
from src.core.paths import get_version
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

    finished = Signal(bool, str, str, list)
    """Segnale emesso al termine: (successo, messaggio, percorso_zip, lista_file_inclusi)."""

    def __init__(
        self,
        include_logs: bool,
        include_analytics: bool,
        include_audit: bool,
        trace_id: str | None = None,
    ) -> None:
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

    def run(self) -> None:
        """Esegue il processo di raccolta diagnostica richiamando il core BugReporter."""
        path, msg, files = BugReporter.collect_diagnostics(
            include_structured_logs=self.include_logs,
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

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il dialogo e configura l'interfaccia utente.

        Args:
          parent: Widget genitore.
        """
        super().__init__(parent)
        self.setWindowTitle("Segnala un Problema")
        dialog_width = 600
        dialog_height = 550
        self.resize(dialog_width, dialog_height)
        self.setup_ui()
        self.worker: ReportWorker | None = None
        self._update_size_estimate()

    def setup_ui(self) -> None:
        """Configura il layout principale richiamando i vari helper di sezione."""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        palette = get_palette()
        self._setup_global_styles(palette)

        self._setup_header_section(layout, palette)
        self._setup_description_area(layout, palette)
        self._setup_options_group(layout, palette)

        self.lbl_size = QLabel("Dimensione stimata: ~50 KB")
        self.lbl_size.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 12px; margin-top: 5px;")
        layout.addWidget(self.lbl_size)

        self._setup_status_section(layout, palette)
        self._setup_buttons_area(layout)

    def _setup_global_styles(self, palette: Any) -> None:
        """Applica lo stile globale CSS al dialogo."""
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

    def _setup_header_section(self, layout: QVBoxLayout, palette: Any) -> None:
        """Configura l'intestazione informativa."""
        lbl_info = QLabel(
            "Descrivi il problema riscontrato con il maggior dettaglio possibile.\n"
            "Se possibile, indica i passaggi per riprodurlo."
        )
        lbl_info.setStyleSheet(f"font-size: 14px; color: {palette.on_surface}; margin-bottom: 5px;")
        lbl_info.setWordWrap(True)
        layout.addWidget(lbl_info)

    def _setup_description_area(self, layout: QVBoxLayout, palette: Any) -> None:
        """Configura l'area di testo per la descrizione del bug."""
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

    def _setup_options_group(self, layout: QVBoxLayout, palette: Any) -> None:
        """Configura il gruppo delle opzioni di diagnostica."""
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

    def _setup_status_section(self, layout: QVBoxLayout, palette: Any) -> None:
        """Configura gli avvisi sulla privacy e la barra di progresso."""
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

        self.progress = StandardProgressBar()
        self.progress.setVisible(False)
        self.progress.setRange(0, 0)
        self.progress.setStyleSheet(
            f"QProgressBar {{ background: {palette.border}; border: none; height: 6px; }} "
            f"QProgressBar::chunk {{ background: {palette.primary}; }}"
        )
        layout.addWidget(self.progress)

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

    def _setup_buttons_area(self, layout: QVBoxLayout) -> None:
        """Configura l'area dei pulsanti di chiusura e invio."""
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

    def _update_size_estimate(self) -> None:
        """Aggiorna dinamicamente la stima della dimensione del file ZIP finale."""
        try:
            size = BugReporter.get_estimated_size(
                include_structured_logs=self.chk_include_logs.isChecked(),
                include_analytics=self.chk_include_analytics.isChecked(),
                include_audit=self.chk_include_audit.isChecked(),
            )
            self.lbl_size.setText(f"Dimensione stimata: {size}")
        except Exception:
            self.lbl_size.setText("Dimensione stimata: ~50 KB")

    def start_generation(self) -> None:
        """Valida l'input e avvia il thread worker per la generazione del report."""
        desc = self.txt_description.toPlainText().strip()
        min_desc_len = 10
        if len(desc) < min_desc_len:
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

    def on_report_generated(self, success: bool, msg: str, file_path: str, files: list[str]) -> None:
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
            self.preview_content.setText("\n".join(f"   {f}" for f in files))

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

    def _enable_ui(self) -> None:
        """Riabilita i controlli dell'interfaccia utente al termine delle operazioni asincrone."""
        self.txt_description.setDisabled(False)
        self.btn_send.setDisabled(False)
        self.btn_cancel.setDisabled(False)
        self.chk_include_logs.setDisabled(False)
        self.chk_include_analytics.setDisabled(False)
        self.chk_include_audit.setDisabled(False)
        self.txt_trace_id.setDisabled(False)

    def open_outlook(self, attachment_path: str, description: str) -> bool:
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
            try:
                outlook = win32.Dispatch("Outlook.Application")
            except Exception:
                logger.warning("Outlook application not found or accessible via COM.")
                return False

            metadata = self._prepare_ticket_metadata()
            final_zip_path = self._rename_zip_with_ticket(attachment_path, metadata["full_ticket_file"])
            cliente_info = self._get_client_info()

            from src.core.constants import Emails
            mail = outlook.CreateItem(0)
            mail.To = Emails.SUPPORT
            mail.Subject = f"[Segnalazione Bug] SyncroJob v{metadata['version']} - {metadata['subject_suffix']}"
            mail.HTMLBody = self._generate_html_body(description, metadata, cliente_info)

            if Path(final_zip_path).exists():
                mail.Attachments.Add(final_zip_path)
            mail.Display()
        except Exception:
            logger.exception("Errore automazione Outlook")
            return False
        else:
            return True

    def _prepare_ticket_metadata(self) -> dict[str, Any]:
        """Prepara i metadati del ticket per la mail e il file."""
        now = datetime.now(UTC).astimezone()
        rand_max = 0x10000
        rand_hex = f"{secrets.randbelow(rand_max):04X}"
        ticket_id = f"TKT-{rand_hex}"

        return {
            "ticket_id": ticket_id,
            "version": get_version(),
            "user": getpass.getuser().upper(),
            "date_display": now.strftime("%d/%m/%Y %H:%M"),
            "date_file": now.strftime("%d-%m-%Y_%H-%M"),
            "subject_suffix": f"{now.strftime('%d/%m/%Y %H:%M')} {ticket_id}",
            "full_ticket_file": f"{now.strftime('%d-%m-%Y_%H-%M')}_{ticket_id}"
        }

    def _get_client_info(self) -> str:
        """Recupera le informazioni sul cliente dalla licenza."""
        cliente_info = "ISAB S.R.L."
        with suppress(Exception):
            from src.core.license_validator import get_license_info
            lic_data = get_license_info()
            if lic_data and "Cliente" in lic_data:
                cliente_info = lic_data["Cliente"]
        return cliente_info

    def _rename_zip_with_ticket(self, attachment_path: str, full_ticket_file: str) -> str:
        """Rinomina lo ZIP temporaneo per includere l'ID del ticket."""
        with suppress(Exception):
            dir_name = os.path.dirname(attachment_path)
            new_path = os.path.join(dir_name, f"{full_ticket_file}.zip")
            if Path(new_path).exists():
                Path(new_path).unlink()
            os.rename(attachment_path, new_path)
            return new_path
        return attachment_path

    def _generate_html_body(self, description: str, meta: dict[str, Any], cliente: str) -> str:
        """Genera il corpo HTML professionale per la mail di Outlook."""
        palette = get_palette()
        css_cell = f"padding: 8px 12px; border-bottom: 1px solid {palette.border}; color: {palette.on_surface};"
        css_header = f"padding: 8px 12px; border-bottom: 2px solid {palette.primary}; font-weight: 600; color: {palette.primary};"

        return f"""
        <div style="font-family: 'Segoe UI', sans-serif; color: {palette.on_surface}; max-width: 900px;">
          <h2 style="color: {palette.primary};">Segnalazione Bug SyncroJob</h2>
          <table style="width: 100%; border-collapse: separate; margin-top: 20px;">
            <tr>
              <td style="width: 320px; vertical-align: top;">
                <table style="width: 100%; font-size: 13px;">
                  <tr><th style="{css_header}" colspan="2">DETTAGLI SISTEMA</th></tr>
                  <tr><td style="{css_cell} font-weight:600;">Ticket ID</td><td style="{css_cell}">{meta['ticket_id']}</td></tr>
                  <tr><td style="{css_cell} font-weight:600;">Versione</td><td style="{css_cell}">{meta['version']}</td></tr>
                  <tr><td style="{css_cell} font-weight:600;">Utente</td><td style="{css_cell}">{meta['user']}</td></tr>
                  <tr><td style="{css_cell} font-weight:600;">Cliente</td><td style="{css_cell}">{cliente}</td></tr>
                </table>
              </td>
              <td style="vertical-align: top; padding-left: 20px;">
                <h3 style="border-bottom: 2px solid {palette.border};">Descrizione Problema</h3>
                <div style="line-height: 1.6;">{description.replace(chr(10), '<br>')}</div>
              </td>
            </tr>
          </table>
        </div>
        """

    def save_manually(self, source_path: str) -> None:
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
                shutil.copy2(source_path, dest_path)
                QMessageBox.information(self, "Salvato", f"Report salvato in:\n{dest_path}")
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Errore Salva", f"Errore: {e}")
