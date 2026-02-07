"""
SyncroJob - Bot Parameters Widget
Widget riutilizzabile per i parametri comuni dei bot (Fornitore, Date, Percorso).
"""

from contextlib import suppress

from PyQt6.QtCore import QDate, QSize, pyqtSignal
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
from src.core.constants import Icons
from src.utils.helpers import get_asset_path, get_colored_icon

from .calendar_date_edit import CalendarDateEdit


class BotParametersWidget(QWidget):
    """
    Widget che raggruppa i parametri comuni per i bot:
    - Selezione Fornitore
    - Selezione Data (singola o range)
    - Percorso di destinazione
    """

    settings_requested = pyqtSignal()
    changed = pyqtSignal()

    def __init__(self, show_date_range: bool = False, show_dest_path: bool = True, parent=None):
        super().__init__(parent)
        self.show_date_range = show_date_range
        self.show_dest_path = show_dest_path
        self._setup_ui()
        self.refresh_fornitori()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # --- Riga Unica: Fornitore, Date, Destinazione ---
        self.main_row_layout = QHBoxLayout()

        # Fornitore
        self.main_row_layout.addWidget(QLabel("Fornitore:"))
        self.fornitore_combo = QComboBox()
        self.fornitore_combo.setMinimumHeight(40)
        self.fornitore_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.fornitore_combo.currentIndexChanged.connect(self.changed.emit)
        self.main_row_layout.addWidget(self.fornitore_combo)

        # Pulsante Settings
        self.settings_btn = QPushButton()
        self.settings_btn.setIcon(get_colored_icon(get_asset_path(Icons.SETTINGS_DARK), "#000000"))
        self.settings_btn.setIconSize(QSize(24, 24))
        self.settings_btn.setFixedSize(40, 40)
        self.settings_btn.setToolTip("Gestisci fornitori")
        self.settings_btn.clicked.connect(self.settings_requested.emit)
        self.settings_btn.setStyleSheet(self._get_icon_btn_style())
        self.main_row_layout.addWidget(self.settings_btn)

        self.main_row_layout.addSpacing(20)

        # Data Da
        self.main_row_layout.addWidget(QLabel("Data Da:"))
        self.date_da = CalendarDateEdit()
        self.date_da.dateChanged.connect(self.changed.emit)
        self.main_row_layout.addWidget(self.date_da)

        # Data A (opzionale)
        if self.show_date_range:
            self.main_row_layout.addSpacing(15)
            self.main_row_layout.addWidget(QLabel("Data A:"))
            self.date_a = CalendarDateEdit()
            self.date_a.dateChanged.connect(self.changed.emit)
            self.main_row_layout.addWidget(self.date_a)

        # Destinazione (opzionale) - Ora nella stessa riga
        if self.show_dest_path:
            self.main_row_layout.addSpacing(20)
            self.main_row_layout.addWidget(QLabel("Destinazione:"))

            self.dest_path_edit = QLineEdit()
            self.dest_path_edit.setPlaceholderText("Download utente (default)")
            self.dest_path_edit.setReadOnly(True)
            self.dest_path_edit.setMinimumWidth(200)  # Ridotto un po' per stare in riga
            self.dest_path_edit.textChanged.connect(self.changed.emit)
            self.main_row_layout.addWidget(self.dest_path_edit)

            self.browse_btn = QPushButton()
            self.browse_btn.setIcon(get_colored_icon(get_asset_path(Icons.FOLDER), "#000000"))
            self.browse_btn.setIconSize(QSize(24, 24))
            self.browse_btn.setFixedSize(40, 40)
            self.browse_btn.clicked.connect(self._browse_path)
            self.browse_btn.setStyleSheet(self._get_icon_btn_style())
            self.main_row_layout.addWidget(self.browse_btn)

        self.main_row_layout.addStretch()
        layout.addLayout(self.main_row_layout)

    def add_widget_to_row(self, widget):
        """
        Aggiunge un widget personalizzato alla riga dei parametri (prima dello stretch).

        Args:
            widget: Il widget QWidget da aggiungere.
        """
        # Rimuovi lo stretch finale temporaneamente
        item = self.main_row_layout.takeAt(self.main_row_layout.count() - 1)

        self.main_row_layout.addSpacing(15)
        self.main_row_layout.addWidget(widget)

        # Rimetti lo stretch
        if item:
            self.main_row_layout.addItem(item)

    def _get_icon_btn_style(self) -> str:
        """Restituisce lo stile QSS per i pulsanti icona."""
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
        """Metodo placeholder per l'aggiornamento della larghezza (non più necessario)."""

    def _browse_path(self):
        """Apre il dialogo di selezione cartella per il percorso di destinazione."""
        path = QFileDialog.getExistingDirectory(self, "Seleziona cartella destinazione")
        if path:
            self.dest_path_edit.setText(path)

    def refresh_fornitori(self):
        """Ricarica l'elenco dei fornitori dalla configurazione globale."""
        fornitori = config_manager.load_config().get("fornitori", [])
        current = self.fornitore_combo.currentText()

        self.fornitore_combo.clear()
        if fornitori:
            self.fornitore_combo.addItems(fornitori)
            index = self.fornitore_combo.findText(current)
            if index >= 0:
                self.fornitore_combo.setCurrentIndex(index)

    # --- Getters / Setters ---
    def get_fornitore(self) -> str:
        """Restituisce il fornitore attualmente selezionato."""
        return self.fornitore_combo.currentText()

    def set_fornitore(self, fornitore: str):
        """Imposta il fornitore selezionato."""
        index = self.fornitore_combo.findText(fornitore)
        if index >= 0:
            self.fornitore_combo.setCurrentIndex(index)

    def get_dates(self) -> tuple[str, str | None]:
        """Restituisce le date selezionate come tuple di stringhe dd.mm.yyyy."""
        date_da = self.date_da.date().toString("dd.MM.yyyy")
        date_a = self.date_a.date().toString("dd.MM.yyyy") if self.show_date_range else None
        return date_da, date_a

    def set_dates(self, date_da_str: str, date_a_str: str | None = None):
        """
        Imposta le date del widget.

        Args:
            date_da_str: Stringa data inizio (dd.mm.yyyy)
            date_a_str: Stringa data fine opzionale (dd.mm.yyyy)
        """
        with suppress(Exception):
            d, m, y = map(int, date_da_str.split("."))
            self.date_da.setDate(QDate(y, m, d))
            if self.show_date_range and date_a_str:
                d, m, y = map(int, date_a_str.split("."))
                self.date_a.setDate(QDate(y, m, d))

    def get_dest_path(self) -> str:
        """Restituisce il percorso di destinazione selezionato."""
        return self.dest_path_edit.text() if self.show_dest_path else ""

    def set_dest_path(self, path: str):
        """Imposta il percorso di destinazione."""
        if self.show_dest_path:
            self.dest_path_edit.setText(path)
