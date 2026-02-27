from src.gui.widgets.core_widgets import PrimaryButton, SecondaryButton, SearchInput, FilterComboBox, StandardTable, DangerButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS, LABEL_MUTED, LINEEDIT_STYLE
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.modern_card import ModernCard
from src.utils.helpers import get_asset_path


class OdaFilterWidget(QWidget):
    """Widget contenente i filtri e i pulsanti di azione per il pannello Storico OdA."""

    search_changed = pyqtSignal(str)
    update_clicked = pyqtSignal()
    import_clicked = pyqtSignal()
    export_clicked = pyqtSignal()

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
        search_label = QLabel("CERCA ODA / FORNITORE")
        search_label.setStyleSheet(LABEL_MUTED)
        self.search_input = SearchInput()
        self.search_input.setPlaceholderText("OdA, Fornitore, Descrizione...")
        self.search_input.setMinimumWidth(350)
        self.search_input.setStyleSheet(LINEEDIT_STYLE)
        self.search_input.textChanged.connect(self.search_changed.emit)

        search_container.addWidget(search_label)
        search_container.addWidget(self.search_input)
        layout.addLayout(search_container)

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

        # Import Excel Button
        self.btn_import = ModernButton(
            "IMPORTA",
            variant=ModernButton.Variant.GHOST,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.UPLOAD),
        )
        self.btn_import.clicked.connect(self.import_clicked.emit)

        # Update Bot Button
        self.btn_bot_update = ModernButton(
            "AGGIORNA",
            variant=ModernButton.Variant.PRIMARY,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.REFRESH),
        )
        self.btn_bot_update.clicked.connect(self.update_clicked.emit)

        # Export Excel
        self.export_btn = ModernButton(
            "EXPORT",
            variant=ModernButton.Variant.SUCCESS,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.EXCEL),
        )
        self.export_btn.setToolTip("Esporta Excel")
        self.export_btn.clicked.connect(self.export_clicked.emit)

        actions_h.addWidget(self.btn_import)
        actions_h.addWidget(self.export_btn)
        actions_h.addWidget(self.btn_bot_update)

        info_v.addWidget(self.lbl_sync_status)
        info_v.addLayout(actions_h)
        layout.addLayout(info_v)

        main_layout.addWidget(self.container)

    def set_sync_status(self, status: str) -> None:
        """Aggiorna il testo dell'indicatore di stato sincronizzazione."""
        self.lbl_sync_status.setText(status)
