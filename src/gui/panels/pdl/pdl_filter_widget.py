from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS, COMBOBOX_STYLE, LABEL_MUTED, LINEEDIT_STYLE
from src.gui.widgets.core_widgets import FilterComboBox, SearchInput
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.modern_card import ModernCard
from src.utils.helpers import get_asset_path, get_colored_icon


class PDLFilterWidget(QWidget):
    """Widget contenente i filtri e i pulsanti di azione per il pannello PDL."""

    filter_changed = Signal()
    site_changed = Signal(str)
    area_changed = Signal(str)
    update_clicked = Signal()
    reset_clicked = Signal()
    export_clicked = Signal()

    # Dichiarazione attributi per MyPy (creati dinamicamente in _setup_combo_filters)
    group_filter: FilterComboBox
    site_filter: FilterComboBox
    area_filter: FilterComboBox
    unit_filter: FilterComboBox
    search_input: SearchInput
    btn_bot_update: ModernButton
    clear_btn: ModernButton
    export_btn: ModernButton
    lbl_sync_status: QLabel

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()
        # Force compact height
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def _setup_ui(self) -> None:
        """Inizializza il layout principale del widget filtri."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.container = ModernCard(elevation=10)
        self.container.setObjectName("filterBar")
        layout = QHBoxLayout(self.container)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        self._setup_search_section(layout)
        self._add_divider(layout)
        self._setup_combo_filters(layout)
        layout.addStretch()
        self._setup_actions_section(layout)

        main_layout.addWidget(self.container)
        self._connect_signals()

    def _setup_search_section(self, layout: QHBoxLayout) -> None:
        """Configura la sezione di ricerca testuale."""
        search_container = QVBoxLayout()
        search_container.setSpacing(4)
        search_label = QLabel("CERCA PDL")
        search_label.setStyleSheet(LABEL_MUTED)
        self.search_input = SearchInput()
        self.search_input.setPlaceholderText("N°, Area, Richiedente...")
        self.search_input.setMinimumWidth(200)
        self.search_input.setStyleSheet(LINEEDIT_STYLE)

        search_container.addWidget(search_label)
        search_container.addWidget(self.search_input)
        layout.addLayout(search_container)

    def _add_divider(self, layout: QHBoxLayout) -> None:
        """Aggiunge un divisore verticale tra le sezioni."""
        v_line = QFrame()
        v_line.setFrameShape(QFrame.Shape.VLine)
        v_line.setFrameShadow(QFrame.Shadow.Plain)
        v_line.setStyleSheet(f"color: {COLORS['border_light']};")
        layout.addWidget(v_line)

    def _setup_combo_filters(self, layout: QHBoxLayout) -> None:
        """Configura i filtri a tendina (Gruppo, Sito, Area, Unità)."""
        filter_group = QHBoxLayout()
        filter_group.setSpacing(12)

        # Configurazione helper per le combo
        configs = [
            ("GRUPPO", "group_filter", 80, ["Tutti"]),
            ("SITO", "site_filter", 110, ["Tutti i siti", "IGCC", "ISAB Nord", "ISAB Sud"]),
            ("AREA", "area_filter", 120, ["Tutte"]),
            ("UNITÀ", "unit_filter", 100, ["Tutte"]),
        ]

        for label, attr_name, min_width, items in configs:
            v_box = QVBoxLayout()
            v_box.setSpacing(4)
            lbl = QLabel(label)
            lbl.setStyleSheet(LABEL_MUTED)
            combo = FilterComboBox()
            combo.addItems(items)
            combo.setMinimumWidth(min_width)
            combo.setStyleSheet(COMBOBOX_STYLE)
            setattr(self, attr_name, combo)
            v_box.addWidget(lbl)
            v_box.addWidget(combo)
            filter_group.addLayout(v_box)

        layout.addLayout(filter_group)

    def _setup_actions_section(self, layout: QHBoxLayout) -> None:
        """Configura la sezione delle azioni (Reset, Export, Update)."""
        info_v = QVBoxLayout()
        info_v.setSpacing(4)
        info_v.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lbl_sync_status = QLabel("Ultimo Sync: --")
        self.lbl_sync_status.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")

        actions_h = QHBoxLayout()
        actions_h.setSpacing(8)

        # Reset
        self.clear_btn = ModernButton("", variant=ModernButton.Variant.GHOST, size=ModernButton.Size.SMALL)
        self.clear_btn.setIcon(get_colored_icon(get_asset_path(Icons.RESET), COLORS["text_muted"]))

        # Export
        self.export_btn = ModernButton(
            "EXPORT",
            variant=ModernButton.Variant.SUCCESS,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.EXCEL),
        )

        # Update
        self.btn_bot_update = ModernButton(
            "AGGIORNA",
            variant=ModernButton.Variant.PRIMARY,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.REFRESH),
        )

        actions_h.addWidget(self.clear_btn)
        actions_h.addWidget(self.export_btn)
        actions_h.addWidget(self.btn_bot_update)

        info_v.addWidget(self.lbl_sync_status)
        info_v.addLayout(actions_h)
        layout.addLayout(info_v)

    def _connect_signals(self) -> None:
        """Connette i segnali dei widget alle azioni del pannello."""
        self.group_filter.currentTextChanged.connect(lambda _: self.filter_changed.emit())
        self.site_filter.currentTextChanged.connect(self.site_changed.emit)
        self.area_filter.currentTextChanged.connect(self.area_changed.emit)
        self.unit_filter.currentTextChanged.connect(lambda _: self.filter_changed.emit())
        self.btn_bot_update.clicked.connect(lambda: self.update_clicked.emit())
        self.clear_btn.clicked.connect(lambda: self.reset_clicked.emit())
        self.export_btn.clicked.connect(lambda: self.export_clicked.emit())

    def get_filters(self) -> dict[str, str]:
        """
        Recupera i valori correnti di tutti i filtri.

        Returns:
            dict: Mappa dei filtri (search, group, site, area, unit).
        """
        return {
            "search": self.search_input.text().lower(),
            "group": self.group_filter.currentText(),
            "site": self.site_filter.currentText(),
            "area": self.area_filter.currentText(),
            "unit": self.unit_filter.currentText(),
        }
