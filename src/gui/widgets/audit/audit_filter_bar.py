"""
SyncroJob - Audit Filter Bar
Widget per la configurazione dei filtri di ricerca e visualizzazione all'interno dell'Audit Log.
"""

from collections.abc import Sequence
from typing import Any

from PyQt6.QtCore import QDate, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)

from src.core.constants import Icons
from src.gui.widgets.calendar_date_edit import CalendarDateEdit
from src.utils.helpers import get_asset_path, get_colored_icon


class AuditFilterBar(QFrame):
    """
    Barra dei filtri per l'Audit Log.
    Permette di filtrare i log per range temporale, categoria, livello di severità e ricerca testuale.
    """

    filters_applied = pyqtSignal(dict)
    """Segnale emesso quando l'utente clicca su 'Filtra', contenente il dizionario dei parametri."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza la barra dei filtri.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.setStyleSheet("background-color: #f8f9fa; border-radius: 6px; border: 1px solid #dee2e6;")
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura il layout orizzontale e inizializza i widget dei filtri."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Date Range
        self.date_from = CalendarDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-7))
        self.date_from.setDisplayFormat("dd/MM/yyyy")
        self.date_from.setMinimumWidth(180)
        self.date_from.setMaximumWidth(220)

        self.date_to = CalendarDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setDisplayFormat("dd/MM/yyyy")
        self.date_to.setMinimumWidth(180)
        self.date_to.setMaximumWidth(220)

        layout.addWidget(QLabel("Dal:"))
        layout.addWidget(self.date_from)
        layout.addWidget(QLabel("Al:"))
        layout.addWidget(self.date_to)

        # Categoria
        self.cat_combo = QComboBox()
        self.cat_combo.addItem("Tutte")
        self.cat_combo.setFixedWidth(150)
        layout.addWidget(self.cat_combo)

        # Livello
        self.level_combo = QComboBox()
        self.level_combo.addItems(["Tutti", "Info (Low)", "Warning (Med)", "Error (High)"])
        self.level_combo.setFixedWidth(130)
        layout.addWidget(self.level_combo)

        # Search
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Cerca nei log...")
        self.search_edit.setStyleSheet("border: 1px solid #ced4da; border-radius: 4px; padding: 4px;")
        layout.addWidget(self.search_edit)

        # Btn Applica
        apply_btn = QPushButton("Filtra")
        apply_btn.setIcon(get_colored_icon(get_asset_path(Icons.SEARCH), "#ffffff"))
        apply_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #0d6efd; color: white; border: none;
                border-radius: 4px; padding: 6px 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #0b5ed7; }
        """
        )
        apply_btn.clicked.connect(self._emit_filters)
        layout.addWidget(apply_btn)

    def set_categories(self, categories: Sequence[str]) -> None:
        """
        Popola il menu a tendina delle categorie.

        Args:
            categories: Lista di stringhe rappresentanti le categorie di log disponibili.
        """
        self.cat_combo.clear()
        self.cat_combo.addItem("Tutte")
        self.cat_combo.addItems(categories)

    def _emit_filters(self) -> None:
        """Raccoglie i valori correnti dei filtri ed emette il segnale 'filters_applied'."""
        lvl_idx = self.level_combo.currentIndex()
        levels = None
        if lvl_idx == 1:
            levels = ["low"]
        elif lvl_idx == 2:
            levels = ["medium"]
        elif lvl_idx == 3:
            levels = ["high"]

        self.filters_applied.emit(
            {
                "date_from": self.date_from.date().toPyDate(),
                "date_to": self.date_to.date().toPyDate(),
                "category": self.cat_combo.currentText(),
                "levels": levels,
                "search_text": self.search_edit.text().strip(),
            }
        )

    def set_enabled_dates(self, enabled: bool) -> None:
        """
        Abilita o disabilita i campi di selezione data.

        Args:
            enabled: Stato di abilitazione.
        """
        self.date_from.setEnabled(enabled)
        self.date_to.setEnabled(enabled)

    def get_filters(self) -> dict[str, Any]:
        """
        Restituisce i parametri di filtraggio correnti in un formato pronto per le query.

        Returns:
            dict: Dizionario contenente date convertite in datetime, categoria, livelli e testo di ricerca.
        """
        from datetime import datetime

        start_dt = datetime.combine(self.date_from.date().toPyDate(), datetime.min.time())
        end_dt = datetime.combine(self.date_to.date().toPyDate(), datetime.max.time())
        lvl_idx = self.level_combo.currentIndex()
        levels = None
        if lvl_idx == 1:
            levels = ["low"]
        elif lvl_idx == 2:
            levels = ["medium"]
        elif lvl_idx == 3:
            levels = ["high"]

        return {
            "start_date": start_dt,
            "end_date": end_dt,
            "category": self.cat_combo.currentText(),
            "levels": levels,
            "search_text": self.search_edit.text().strip(),
        }
