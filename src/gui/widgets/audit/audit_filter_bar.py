"""
SyncroJob - Audit Filter Bar
Widget per la configurazione dei filtri di ricerca e visualizzazione all'interno dell'Audit Log.
"""

from collections.abc import Sequence
from typing import Any

from PyQt6.QtCore import QDate, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS, COMBOBOX_STYLE, LABEL_MUTED, LINEEDIT_STYLE
from src.gui.widgets.calendar_date_edit import CalendarDateEdit
from src.gui.widgets.core_widgets import (
    FilterComboBox,
    SearchInput,
)
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.modern_card import ModernCard
from src.utils.helpers import get_asset_path


class AuditFilterBar(ModernCard):
    """
    Barra dei filtri per l'Audit Log con design Enterprise.
    """

    filters_applied = pyqtSignal(dict)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent, elevation=8)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura il layout orizzontale e inizializza i widget dei filtri."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        # 1. Date Range
        range_h = QHBoxLayout()
        range_h.setSpacing(8)

        v_da = QVBoxLayout()
        v_da.setSpacing(4)
        lbl_da = QLabel("DAL")
        lbl_da.setStyleSheet(LABEL_MUTED)
        self.date_from = CalendarDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-7))
        self.date_from.setMinimumWidth(120)
        self.date_from.setStyleSheet(COMBOBOX_STYLE)
        v_da.addWidget(lbl_da)
        v_da.addWidget(self.date_from)
        range_h.addLayout(v_da)

        v_a = QVBoxLayout()
        v_a.setSpacing(4)
        lbl_a = QLabel("AL")
        lbl_a.setStyleSheet(LABEL_MUTED)
        self.date_to = CalendarDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setMinimumWidth(120)
        self.date_to.setStyleSheet(COMBOBOX_STYLE)
        v_a.addWidget(lbl_a)
        v_a.addWidget(self.date_to)
        range_h.addLayout(v_a)

        layout.addLayout(range_h)

        # Vertical Divider
        v_line1 = QFrame()
        v_line1.setFrameShape(QFrame.Shape.VLine)
        v_line1.setFrameShadow(QFrame.Shadow.Plain)
        v_line1.setStyleSheet(f"color: {COLORS['border_light']};")
        layout.addWidget(v_line1)

        # 2. Categoria & Livello
        filter_group = QHBoxLayout()
        filter_group.setSpacing(12)

        cat_v = QVBoxLayout()
        cat_v.setSpacing(4)
        lbl_cat = QLabel("CATEGORIA")
        lbl_cat.setStyleSheet(LABEL_MUTED)
        self.cat_combo = FilterComboBox()
        self.cat_combo.addItem("Tutte")
        self.cat_combo.setMinimumWidth(140)
        self.cat_combo.setStyleSheet(COMBOBOX_STYLE)
        cat_v.addWidget(lbl_cat)
        cat_v.addWidget(self.cat_combo)
        filter_group.addLayout(cat_v)

        lvl_v = QVBoxLayout()
        lvl_v.setSpacing(4)
        lbl_lvl = QLabel("LIVELLO")
        lbl_lvl.setStyleSheet(LABEL_MUTED)
        self.level_combo = FilterComboBox()
        self.level_combo.addItems(["Tutti", "Info (Low)", "Warning (Med)", "Error (High)"])
        self.level_combo.setMinimumWidth(130)
        self.level_combo.setStyleSheet(COMBOBOX_STYLE)
        lvl_v.addWidget(lbl_lvl)
        lvl_v.addWidget(self.level_combo)
        filter_group.addLayout(lvl_v)

        layout.addLayout(filter_group)

        # 3. Search
        search_v = QVBoxLayout()
        search_v.setSpacing(4)
        lbl_search = QLabel("TESTO")
        lbl_search.setStyleSheet(LABEL_MUTED)
        self.search_edit = SearchInput()
        self.search_edit.setPlaceholderText("Cerca nei log...")
        self.search_edit.setMinimumWidth(200)
        self.search_edit.setStyleSheet(LINEEDIT_STYLE)
        search_v.addWidget(lbl_search)
        search_v.addWidget(self.search_edit)
        layout.addLayout(search_v)

        layout.addStretch()

        # 4. Btn Applica
        self.apply_btn = ModernButton(
            "FILTRA",
            variant=ModernButton.Variant.PRIMARY,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.SEARCH),
        )
        self.apply_btn.clicked.connect(self._emit_filters)
        layout.addWidget(self.apply_btn, alignment=Qt.AlignmentFlag.AlignBottom)

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
