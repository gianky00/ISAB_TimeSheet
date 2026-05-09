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

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()
        # Force compact height
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Bar Container with modern Card style (using ModernCard for elevation/hover)
        self.container = ModernCard(elevation=10)
        self.container.setObjectName("filterBar")

        layout = QHBoxLayout(self.container)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)

        # --- SEZIONE RICERCA ---
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

        # Vertical Divider
        v_line = QFrame()
        v_line.setFrameShape(QFrame.Shape.VLine)
        v_line.setFrameShadow(QFrame.Shadow.Plain)
        v_line.setStyleSheet(f"color: {COLORS['border_light']};")
        layout.addWidget(v_line)

        # --- FILTRI COMBO ---
        filter_group = QHBoxLayout()
        filter_group.setSpacing(12)

        # Gruppo
        group_v = QVBoxLayout()
        group_v.setSpacing(4)
        lbl_group = QLabel("GRUPPO")
        lbl_group.setStyleSheet(LABEL_MUTED)
        self.group_filter = FilterComboBox()
        self.group_filter.addItem("Tutti")
        self.group_filter.setMinimumWidth(80)
        self.group_filter.setStyleSheet(COMBOBOX_STYLE)
        group_v.addWidget(lbl_group)
        group_v.addWidget(self.group_filter)
        filter_group.addLayout(group_v)

        # Sito
        site_v = QVBoxLayout()
        site_v.setSpacing(4)
        lbl_site = QLabel("SITO")
        lbl_site.setStyleSheet(LABEL_MUTED)
        self.site_filter = FilterComboBox()
        self.site_filter.addItems(["Tutti i siti", "IGCC", "ISAB Nord", "ISAB Sud"])
        self.site_filter.setMinimumWidth(110)
        self.site_filter.setStyleSheet(COMBOBOX_STYLE)
        site_v.addWidget(lbl_site)
        site_v.addWidget(self.site_filter)
        filter_group.addLayout(site_v)

        # Area
        area_v = QVBoxLayout()
        area_v.setSpacing(4)
        lbl_area = QLabel("AREA")
        lbl_area.setStyleSheet(LABEL_MUTED)
        self.area_filter = FilterComboBox()
        self.area_filter.addItem("Tutte")
        self.area_filter.setMinimumWidth(120)
        self.area_filter.setStyleSheet(COMBOBOX_STYLE)
        area_v.addWidget(lbl_area)
        area_v.addWidget(self.area_filter)
        filter_group.addLayout(area_v)

        # Unità
        unit_v = QVBoxLayout()
        unit_v.setSpacing(4)
        lbl_unit = QLabel("UNITÀ")
        lbl_unit.setStyleSheet(LABEL_MUTED)
        self.unit_filter = FilterComboBox()
        self.unit_filter.addItem("Tutte")
        self.unit_filter.setMinimumWidth(100)
        self.unit_filter.setStyleSheet(COMBOBOX_STYLE)
        unit_v.addWidget(lbl_unit)
        unit_v.addWidget(self.unit_filter)
        filter_group.addLayout(unit_v)

        layout.addLayout(filter_group)
        layout.addStretch()

        # --- INFO & STATUS ---
        info_v = QVBoxLayout()
        info_v.setSpacing(4)
        info_v.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.lbl_sync_status = QLabel("Ultimo Sync: --")
        self.lbl_sync_status.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")

        # Action Buttons Row
        actions_h = QHBoxLayout()
        actions_h.setSpacing(8)

        # Reset
        self.clear_btn = ModernButton("", variant=ModernButton.Variant.GHOST, size=ModernButton.Size.SMALL)
        self.clear_btn.setIcon(get_colored_icon(get_asset_path(Icons.RESET), COLORS["text_muted"]))

        # Update Bot
        self.btn_bot_update = ModernButton(
            "AGGIORNA",
            variant=ModernButton.Variant.PRIMARY,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.REFRESH),
        )

        # Export
        self.export_btn = ModernButton(
            "EXPORT",
            variant=ModernButton.Variant.SUCCESS,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.EXCEL),
        )

        actions_h.addWidget(self.clear_btn)
        actions_h.addWidget(self.export_btn)
        actions_h.addWidget(self.btn_bot_update)

        info_v.addWidget(self.lbl_sync_status)
        info_v.addLayout(actions_h)
        layout.addLayout(info_v)

        main_layout.addWidget(self.container)

        # Connessioni
        self.group_filter.currentTextChanged.connect(self.filter_changed.emit)
        self.site_filter.currentTextChanged.connect(self.site_changed.emit)
        self.area_filter.currentTextChanged.connect(self.area_changed.emit)
        self.unit_filter.currentTextChanged.connect(self.filter_changed.emit)
        self.btn_bot_update.clicked.connect(self.update_clicked.emit)
        self.clear_btn.clicked.connect(self.reset_clicked.emit)
        self.export_btn.clicked.connect(self.export_clicked.emit)

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
