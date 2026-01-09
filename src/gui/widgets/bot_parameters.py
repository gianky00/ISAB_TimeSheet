"""
SyncroJob - Bot Parameters Widget
Widget riutilizzabile per i parametri comuni dei bot (Fornitore, Date, Percorso).
"""

from typing import Optional

from PyQt6.QtCore import QDate, QSize, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.gui.old_widgets import CalendarDateEdit
from src.utils.helpers import get_asset_path


class BotParametersWidget(QWidget):
    """
    Widget che raggruppa i parametri comuni per i bot:
    - Selezione Fornitore
    - Selezione Data (singola o range)
    - Percorso di destinazione
    """

    settings_requested = pyqtSignal()
    changed = pyqtSignal()

    def __init__(
        self,
        show_date_range: bool = False,
        show_dest_path: bool = True,
        parent=None
    ):
        super().__init__(parent)
        self.show_date_range = show_date_range
        self.show_dest_path = show_dest_path
        self._setup_ui()
        self.refresh_fornitori()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # --- Riga 1: Fornitore e Date ---
        row1 = QHBoxLayout()

        # Fornitore
        row1.addWidget(QLabel("Fornitore:"))
        self.fornitore_combo = QComboBox()
        self.fornitore_combo.setMinimumHeight(40)
        self.fornitore_combo.currentIndexChanged.connect(self.changed.emit)
        row1.addWidget(self.fornitore_combo)

        # Pulsante Settings
        self.settings_btn = QPushButton()
        self.settings_btn.setIcon(QIcon(get_asset_path("assets/icons/settings.svg")))
        self.settings_btn.setIconSize(QSize(24, 24))
        self.settings_btn.setFixedSize(40, 40)
        self.settings_btn.setToolTip("Gestisci fornitori")
        self.settings_btn.clicked.connect(self.settings_requested.emit)
        self.settings_btn.setStyleSheet(self._get_icon_btn_style())
        row1.addWidget(self.settings_btn)

        row1.addSpacing(20)

        # Data Da
        row1.addWidget(QLabel("Data Da:"))
        self.date_da = CalendarDateEdit()
        self.date_da.dateChanged.connect(self.changed.emit)
        row1.addWidget(self.date_da)

        # Data A (opzionale)
        if self.show_date_range:
            row1.addSpacing(15)
            row1.addWidget(QLabel("Data A:"))
            self.date_a = CalendarDateEdit()
            self.date_a.dateChanged.connect(self.changed.emit)
            row1.addWidget(self.date_a)

        row1.addStretch()
        layout.addLayout(row1)

        # --- Riga 2: Percorso Destinazione (opzionale) ---
        if self.show_dest_path:
            row2 = QHBoxLayout()
            row2.addWidget(QLabel("Destinazione:"))

            self.dest_path_edit = QLineEdit()
            self.dest_path_edit.setPlaceholderText("Download utente (default)")
            self.dest_path_edit.setReadOnly(True)
            self.dest_path_edit.setMinimumWidth(350)
            self.dest_path_edit.textChanged.connect(self._update_dest_width)
            self.dest_path_edit.textChanged.connect(self.changed.emit)
            row2.addWidget(self.dest_path_edit)

            self.browse_btn = QPushButton()
            self.browse_btn.setIcon(QIcon(get_asset_path("assets/icons/folder.svg")))
            self.browse_btn.setIconSize(QSize(24, 24))
            self.browse_btn.setFixedSize(40, 40)
            self.browse_btn.clicked.connect(self._browse_path)
            self.browse_btn.setStyleSheet(self._get_icon_btn_style())
            row2.addWidget(self.browse_btn)

            row2.addStretch()
            layout.addLayout(row2)

    def _get_icon_btn_style(self) -> str:
        return """
            QPushButton {
                background-color: #f8f9fa;
                color: #212529;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 2px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #ced4da;
            }
        """

    def _update_dest_width(self):
        if not self.show_dest_path:
            return
        text = self.dest_path_edit.text() or self.dest_path_edit.placeholderText()
        w = self.dest_path_edit.fontMetrics().horizontalAdvance(text) + 60
        self.dest_path_edit.setFixedWidth(max(350, min(w, 600)))

    def _browse_path(self):
        path = QFileDialog.getExistingDirectory(self, "Seleziona cartella destinazione")
        if path:
            self.dest_path_edit.setText(path)

    def refresh_fornitori(self):
        """Ricarica l'elenco dei fornitori."""
        config = config_manager.load_config()
        fornitori = config.get("fornitori", [])
        current = self.fornitore_combo.currentText()

        self.fornitore_combo.clear()
        if fornitori:
            self.fornitore_combo.addItems(fornitori)
            index = self.fornitore_combo.findText(current)
            if index >= 0:
                self.fornitore_combo.setCurrentIndex(index)

    # --- Getters / Setters ---
    def get_fornitore(self) -> str:
        return self.fornitore_combo.currentText()

    def set_fornitore(self, fornitore: str):
        index = self.fornitore_combo.findText(fornitore)
        if index >= 0:
            self.fornitore_combo.setCurrentIndex(index)

    def get_dates(self) -> tuple[str, Optional[str]]:
        date_da = self.date_da.date().toString("dd.MM.yyyy")
        date_a = self.date_a.date().toString("dd.MM.yyyy") if self.show_date_range else None
        return date_da, date_a

    def set_dates(self, date_da_str: str, date_a_str: Optional[str] = None):
        try:
            d, m, y = map(int, date_da_str.split("."))
            self.date_da.setDate(QDate(y, m, d))
            if self.show_date_range and date_a_str:
                d, m, y = map(int, date_a_str.split("."))
                self.date_a.setDate(QDate(y, m, d))
        except:
            pass

    def get_dest_path(self) -> str:
        return self.dest_path_edit.text() if self.show_dest_path else ""

    def set_dest_path(self, path: str):
        if self.show_dest_path:
            self.dest_path_edit.setText(path)
