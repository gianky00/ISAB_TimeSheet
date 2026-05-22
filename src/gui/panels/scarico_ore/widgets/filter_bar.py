"""
SyncroJob - Scarico Ore Filter Bar
Componente UI per la visualizzazione delle statistiche e dei filtri di ricerca.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.styles import COLORS, LABEL_MUTED, LINEEDIT_STYLE
from src.gui.widgets import ModernButton
from src.gui.widgets.core_widgets import SearchInput
from src.gui.widgets.modern_card import ModernCard
from src.utils.helpers import get_asset_path


class ScaricoOreFilterBar(ModernCard):
    """Barra superiore con statistiche righe, ore e input di ricerca."""

    search_requested = Signal(str)
    update_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(elevation=10, parent=parent)
        self.setObjectName("filterBar")
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        # 1. Stats Area
        stats_h = QHBoxLayout()
        stats_h.setSpacing(20)

        self.lbl_count = self._create_stat_vbox("RIGHE VISIBILI", COLORS["text_dark"], stats_h)
        self.lbl_selection = self._create_stat_vbox("SELEZIONATO", COLORS["primary_blue"], stats_h)
        self.lbl_total_hours = self._create_stat_vbox("TOTALE ORE", COLORS["teal_accent"], stats_h, bold=True)
        layout.addLayout(stats_h)

        # Divisore
        v_line = QFrame()
        v_line.setFrameShape(QFrame.Shape.VLine)
        v_line.setFrameShadow(QFrame.Shadow.Plain)
        v_line.setStyleSheet(f"color: {COLORS['border_light']};")
        layout.addWidget(v_line)

        # 2. Search Area
        search_v = QVBoxLayout()
        search_v.setSpacing(4)
        lbl_search = QLabel("CERCA PERSONALE / ODA")
        lbl_search.setStyleSheet(LABEL_MUTED)
        self.search_input = SearchInput()
        self.search_input.setPlaceholderText("Filtra dati (Premi Invio)...")
        self.search_input.setMinimumWidth(300)
        self.search_input.setStyleSheet(LINEEDIT_STYLE)
        self.search_input.returnPressed.connect(lambda: self.search_requested.emit(self.search_input.text()))
        search_v.addWidget(lbl_search)
        search_v.addWidget(self.search_input)
        layout.addLayout(search_v)

        layout.addStretch()

        # 3. Info & Actions
        info_v = QVBoxLayout()
        info_v.setSpacing(4)
        info_v.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.status_label = QLabel("Inizializzazione...")
        self.status_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
        self.status_label.setTextFormat(Qt.TextFormat.RichText)

        self.update_btn = ModernButton(
            "SINCRONIZZA",
            variant=ModernButton.Variant.PRIMARY,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.REFRESH),
        )
        self.update_btn.clicked.connect(lambda: self.update_requested.emit())

        btn_h = QHBoxLayout()
        btn_h.setSpacing(5)
        btn_h.addWidget(self.update_btn)

        info_v.addWidget(self.status_label)
        info_v.addLayout(btn_h)
        layout.addLayout(info_v)

    def _create_stat_vbox(
        self, title: str, color: str, parent_layout: QHBoxLayout, bold: bool = False
    ) -> QLabel:
        vbox = QVBoxLayout()
        vbox.setSpacing(4)
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(LABEL_MUTED)

        weight = "800" if bold else "700"
        lbl_value = QLabel("0")
        lbl_value.setStyleSheet(f"color: {color}; font-weight: {weight}; font-size: 14px;")

        vbox.addWidget(lbl_title)
        vbox.addWidget(lbl_value)
        parent_layout.addLayout(vbox)
        return lbl_value

    def set_stats(self, visible_rows: int, selection_total: str, total_hours: str) -> None:
        """Aggiorna i valori delle statistiche."""
        self.lbl_count.setText(str(visible_rows))
        self.lbl_selection.setText(selection_total)
        self.lbl_total_hours.setText(total_hours)
