from typing import Any

from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from src.core import config_manager
from src.core.constants import Icons
from src.gui.panels.settings.shared import create_group_box, style_button
from src.utils.helpers import get_asset_path, get_colored_icon, open_folder


class DiagPage(QWidget):
    """Pagina Diagnostica e Licenza."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        diag_group = create_group_box("Diagnostica & Licenza")
        diag_layout = QHBoxLayout(diag_group)
        diag_layout.setSpacing(15)

        diag_label = QLabel("Gestione file di log e licenza:")
        diag_label.setStyleSheet("font-size: 14px;")
        diag_layout.addWidget(diag_label)

        diag_layout.addStretch()

        open_folder_btn = QPushButton("  Apri Cartella Dati")
        open_folder_btn.setIcon(get_colored_icon(get_asset_path(Icons.FOLDER), "#000000"))
        open_folder_btn.clicked.connect(self._open_data_folder)
        style_button(open_folder_btn)
        diag_layout.addWidget(open_folder_btn)

        layout.addWidget(diag_group)
        layout.addStretch()

    def _open_data_folder(self) -> None:
        """Apre la cartella dei dati dell'applicazione."""
        path = config_manager.CONFIG_DIR
        open_folder(str(path))

    def load_from_config(self, config: dict[str, Any]) -> None:
        """Carica le impostazioni diagnostiche dalla configurazione (non implementato)."""
        pass  # Nulla da caricare per ora

    def save_to_config(self, config_manager: Any) -> None:
        """Salva le impostazioni diagnostiche nella configurazione (non implementato)."""
        pass  # Nulla da salvare
