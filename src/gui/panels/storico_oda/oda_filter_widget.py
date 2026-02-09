from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QWidget,
)

from src.core.constants import Icons
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path, get_colored_icon


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
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca per OdA, Fornitore o Descrizione...")
        self.search_input.setMinimumWidth(300)
        self.search_input.textChanged.connect(lambda text: self.search_changed.emit(text))
        layout.addWidget(self.search_input)

        layout.addStretch()

        # Sync Status
        self.lbl_sync_status = QLabel("")
        self.lbl_sync_status.setStyleSheet("color: #555; font-size: 11px; margin-right: 15px;")
        layout.addWidget(self.lbl_sync_status)

        # Update Bot Button
        self.btn_bot_update = ModernButton(
            "Aggiorna",
            variant=ModernButton.Variant.PRIMARY,
            icon=get_asset_path(Icons.REFRESH),
        )
        self.btn_bot_update.clicked.connect(lambda: self.update_clicked.emit())
        layout.addWidget(self.btn_bot_update)

        # Import Excel Button
        self.btn_import = ModernButton(
            "Importa Excel",
            variant=ModernButton.Variant.GHOST,
            icon=get_asset_path(Icons.UPLOAD),
        )
        self.btn_import.clicked.connect(lambda: self.import_clicked.emit())
        layout.addWidget(self.btn_import)

        # Export Excel
        self.export_btn = ModernButton(
            "",
            variant=ModernButton.Variant.GHOST,
            size=ModernButton.Size.SMALL,
        )
        self.export_btn.setIcon(get_colored_icon(get_asset_path(Icons.EXCEL), "#555"))
        self.export_btn.setToolTip("Esporta Excel")
        self.export_btn.clicked.connect(lambda: self.export_clicked.emit())
        layout.addWidget(self.export_btn)

    def set_sync_status(self, status: str) -> None:
        self.lbl_sync_status.setText(status)
