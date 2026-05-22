"""SyncroJob - Audit Filter Bar.

Widget per la configurazione dei filtri di ricerca e visualizzazione all'interno dell'Audit Log.
"""

from collections.abc import Sequence
from datetime import date as dt_date, datetime
from typing import Any, Final, cast

from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtWidgets import (
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
    """Barra dei filtri per l'Audit Log con design Enterprise."""

    filters_applied = Signal(dict)

    LEVEL_INFO_IDX: Final[int] = 1
    LEVEL_WARN_IDX: Final[int] = 2
    LEVEL_ERR_IDX: Final[int] = 3

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza la classe."""
        super().__init__(parent, elevation=8)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura il layout orizzontale e inizializza i widget dei filtri."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        self._setup_date_range(layout)
        self._add_divider(layout)
        self._setup_category_level(layout)
        self._setup_search(layout)

        layout.addStretch()
        self._setup_apply_button(layout)

    def _setup_date_range(self, layout: QHBoxLayout) -> None:
        """Configura i selettori di intervallo temporale."""
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

    def _add_divider(self, layout: QHBoxLayout) -> None:
        """Aggiunge un separatore verticale."""
        v_line = QFrame()
        v_line.setFrameShape(QFrame.Shape.VLine)
        v_line.setFrameShadow(QFrame.Shadow.Plain)
        v_line.setStyleSheet(f"color: {COLORS['border_light']};")
        layout.addWidget(v_line)

    def _setup_category_level(self, layout: QHBoxLayout) -> None:
        """Configura i menu a tendina per categoria e livello."""
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

    def _setup_search(self, layout: QHBoxLayout) -> None:
        """Configura il campo di ricerca testuale."""
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

    def _setup_apply_button(self, layout: QHBoxLayout) -> None:
        """Inizializza il pulsante di applicazione filtri."""
        self.apply_btn = ModernButton(
            "FILTRA",
            variant=ModernButton.Variant.PRIMARY,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.SEARCH),
        )
        self.apply_btn.clicked.connect(self._emit_filters)
        layout.addWidget(self.apply_btn, alignment=Qt.AlignmentFlag.AlignBottom)

    def set_categories(self, categories: Sequence[str]) -> None:
        """Popola il menu a tendina delle categorie."""
        self.cat_combo.clear()
        self.cat_combo.addItem("Tutte")
        self.cat_combo.addItems(categories)

    def _emit_filters(self) -> None:
        """Raccoglie i valori correnti dei filtri ed emette il segnale 'filters_applied'."""
        lvl_idx = self.level_combo.currentIndex()
        levels = self._get_levels_from_index(lvl_idx)

        self.filters_applied.emit(
            {
                "date_from": self.date_from.date().toPython(),
                "date_to": self.date_to.date().toPython(),
                "category": self.cat_combo.currentText(),
                "levels": levels,
                "search_text": self.search_edit.text().strip(),
            }
        )

    def _get_levels_from_index(self, index: int) -> list[str] | None:
        """Mappa l'indice del combo livello ai valori del database."""
        if index == self.LEVEL_INFO_IDX:
            return ["low"]
        if index == self.LEVEL_WARN_IDX:
            return ["medium"]
        if index == self.LEVEL_ERR_IDX:
            return ["high"]
        return None

    def set_enabled_dates(self, enabled: bool) -> None:
        """Abilita o disabilita i campiùdi selezione data."""
        self.date_from.setEnabled(enabled)
        self.date_to.setEnabled(enabled)

    def get_filters(self) -> dict[str, Any]:
        """Restituisce i parametri di filtraggio correnti per le query."""
        start_dt = datetime.combine(cast("dt_date", self.date_from.date().toPython()), datetime.min.time())
        end_dt = datetime.combine(cast("dt_date", self.date_to.date().toPython()), datetime.max.time())
        lvl_idx = self.level_combo.currentIndex()
        levels = self._get_levels_from_index(lvl_idx)

        return {
            "start_date": start_dt,
            "end_date": end_dt,
            "category": self.cat_combo.currentText(),
            "levels": levels,
            "search_text": self.search_edit.text().strip(),
        }
