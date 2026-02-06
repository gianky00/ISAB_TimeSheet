from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QWidget,
)

from src.core.constants import Icons
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path, get_colored_icon


class PDLFilterWidget(QWidget):
    """Widget contenente i filtri e i pulsanti di azione per il pannello PDL."""

    filter_changed = pyqtSignal()
    site_changed = pyqtSignal(str)
    area_changed = pyqtSignal(str)
    update_clicked = pyqtSignal()
    reset_clicked = pyqtSignal()
    export_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        # Force compact height
        from PyQt6.QtWidgets import QSizePolicy

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca ovunque...")
        self.search_input.setMaximumWidth(250)
        layout.addWidget(self.search_input)

        layout.addWidget(QLabel("Gruppo:"))
        self.group_filter = QComboBox()
        self.group_filter.addItem("Tutti")
        self.group_filter.setMinimumWidth(80)
        layout.addWidget(self.group_filter)

        layout.addWidget(QLabel("Sito:"))
        self.site_filter = QComboBox()
        self.site_filter.addItems(["Tutti i siti", "IGCC", "ISAB Nord", "ISAB Sud"])
        layout.addWidget(self.site_filter)

        layout.addWidget(QLabel("Area:"))
        self.area_filter = QComboBox()
        self.area_filter.addItem("Tutte")
        self.area_filter.setMinimumWidth(100)
        layout.addWidget(self.area_filter)

        layout.addWidget(QLabel("Unità:"))
        self.unit_filter = QComboBox()
        self.unit_filter.addItem("Tutte")
        self.unit_filter.setMinimumWidth(80)
        layout.addWidget(self.unit_filter)

        layout.addStretch()

        # Sync Status
        self.lbl_sync_status = QLabel("")
        self.lbl_sync_status.setStyleSheet(
            "color: #555; font-size: 11px; margin-right: 15px;"
        )
        layout.addWidget(self.lbl_sync_status)

        # Update Bot Button
        self.btn_bot_update = ModernButton(
            "Aggiorna",
            variant=ModernButton.Variant.PRIMARY,
            icon=get_asset_path(Icons.REFRESH),
        )
        layout.addWidget(self.btn_bot_update)

        # Clear Filters
        self.clear_btn = ModernButton(
            "RESETTA FILTRI",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.SMALL,
        )
        self.clear_btn.setIcon(get_colored_icon(get_asset_path(Icons.RESET), "#FFFFFF"))
        self.clear_btn.setToolTip("Resetta Filtri")
        layout.addWidget(self.clear_btn)

        # Export Excel
        self.export_btn = ModernButton(
            "ESPORTA",
            variant=ModernButton.Variant.SUCCESS,
            size=ModernButton.Size.SMALL,
        )
        self.export_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.EXCEL), "#FFFFFF")
        )
        self.export_btn.setToolTip("Esporta Excel")
        layout.addWidget(self.export_btn)

        # Connessioni
        self.group_filter.currentTextChanged.connect(self.filter_changed.emit)
        self.site_filter.currentTextChanged.connect(self.site_changed.emit)
        self.area_filter.currentTextChanged.connect(self.area_changed.emit)
        self.unit_filter.currentTextChanged.connect(self.filter_changed.emit)
        self.btn_bot_update.clicked.connect(self.update_clicked.emit)
        self.clear_btn.clicked.connect(self.reset_clicked.emit)
        self.export_btn.clicked.connect(self.export_clicked.emit)

    def get_filters(self):
        return {
            "search": self.search_input.text().lower(),
            "group": self.group_filter.currentText(),
            "site": self.site_filter.currentText(),
            "area": self.area_filter.currentText(),
            "unit": self.unit_filter.currentText(),
        }
