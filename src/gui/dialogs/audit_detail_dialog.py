import json
from contextlib import suppress
from datetime import datetime

from src.gui.widgets.core_widgets import (PrimaryButton, SecondaryButton, DangerButton, GhostButton, IconButton, SearchInput, StandardInput, StandardTextEdit, FilterComboBox, StandardCheckBox, StandardSpinBox, StandardTable, StandardListWidget, StandardTreeWidget, StandardGroupBox, StandardProgressBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon


class AuditDetailDialog(QDialog):
    """Dialog per visualizzare i dettagli completi di un log."""

    def __init__(self, log_data, parent=None):
        super().__init__(parent)
        self.log_data = log_data
        self.setWindowTitle("Dettagli Audit Log")
        self.setMinimumSize(700, 600)
        self._setup_ui(log_data)

    def _setup_ui(self, data):
        layout = QVBoxLayout(self)

        # Header Info
        ts = data.get("timestamp", "-")
        with suppress(ValueError):
            dt = datetime.fromisoformat(ts)
            ts = dt.strftime("%d/%m/%Y %H:%M:%S")

        dur_ms = data.get("duration_ms", 0) or 0
        dur_str = f"{dur_ms}ms" if dur_ms < 1000 else f"{dur_ms / 1000:.2f}s"

        err_code = data.get("error_code") or "Nessuno"
        module = data.get("module") or "Generico"

        info_text = f"""
        <table style="font-size: 14px; margin-bottom: 10px;" cellspacing="5">
            <tr><td><b>Data:</b></td><td>{ts}</td><td><b>Modulo:</b></td><td>{module}</td></tr>
            <tr><td><b>Utente:</b></td><td>{data.get("user_id", "-")}</td><td><b>Durata:</b></td><td>{dur_str}</td></tr>
            <tr><td><b>Azione:</b></td><td>{data.get("action", "-")}</td><td><b>Cod. Errore:</b></td><td>{err_code}</td></tr>
            <tr><td><b>Entità:</b></td><td>{data.get("entity", "-")}</td><td><b>Stato:</b></td><td>{data.get("status", "-")}</td></tr>
        </table>
        """
        lbl = QLabel(info_text)
        lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(lbl)

        # JSON Viewer
        layout.addWidget(QLabel("<b>Dettagli Tecnici (JSON):</b>"))

        self.text_edit = StandardTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet(
            f"font-family: Consolas, monospace; font-size: 13px; background-color: {COLORS['bg_light']}; color: {COLORS['text_dark']};"
        )

        try:
            params_str = data.get("params", "{}")
            params_json = json.loads(params_str) if isinstance(params_str, str) else params_str

            pretty_json = json.dumps(params_json, indent=4, ensure_ascii=False)
            self.text_edit.setText(pretty_json)
        except (json.JSONDecodeError, TypeError):
            self.text_edit.setText(str(data.get("params", "-")))

        layout.addWidget(self.text_edit)

        # Buttons Bar
        btn_layout = QHBoxLayout()

        # Copia JSON
        btn_copy = PrimaryButton("Copia JSON")
        btn_copy.setIcon(get_colored_icon(get_asset_path(Icons.FILE_TEXT), COLORS["text_dark"]))
        btn_copy.clicked.connect(self._copy_to_clipboard)
        btn_copy.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {COLORS['bg_alt']}; border: 1px solid {COLORS['border_medium']};
                padding: 8px 15px; border-radius: 4px; font-weight: 600; color: {COLORS['text_dark']};
            }}
            QPushButton:hover {{ background-color: {COLORS['bg_hover']}; }}
        """
        )
        btn_layout.addWidget(btn_copy)

        btn_layout.addStretch()

        # Chiudi
        btn_close = PrimaryButton("Chiudi")
        btn_close.clicked.connect(self.accept)
        btn_close.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {COLORS['text_muted']}; color: white; border: none;
                padding: 8px 15px; border-radius: 4px; font-weight: bold;
            }}
            QPushButton:hover {{ opacity: 0.8; }}
        """
        )
        btn_layout.addWidget(btn_close)

        layout.addLayout(btn_layout)

    def _copy_to_clipboard(self):
        cb = QGuiApplication.clipboard()
        if cb:
            cb.setText(self.text_edit.toPlainText())
            QMessageBox.information(self, "Copiato", "Dettagli copiati negli appunti!")
        else:
            QMessageBox.warning(self, "Errore", "Impossibile accedere agli appunti.")
