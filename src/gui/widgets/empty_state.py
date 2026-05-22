"""SyncroJob - Empty State Widget.

Visualizzazione elegante quando una ricerca o una tabella non contengono dati.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon


class EmptyStateWidget(QWidget):
    """Mostra un'icona stilizzata e un messaggio quando non ci sono dati.

    Inizializza la classe.
    """

    def __init__(
        self,
        title: str = "Nessun dato trovato",
        message: str = "Prova a cambiare i filtri o ad aggiornare il database.",
        icon_key: str = Icons.SEARCH,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._setup_ui(title, message, icon_key)

    def _setup_ui(self, title: str, message: str, icon_key: str) -> None:
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)

        # Icona
        self.icon_lbl = QLabel()
        pix = get_colored_icon(get_asset_path(icon_key), COLORS["text_light"]).pixmap(64, 64)
        self.icon_lbl.setPixmap(pix)
        self.icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.icon_lbl)

        # Titolo
        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet(f"""
      font-size: 18px;
      font-weight: bold;
      color: {COLORS["text_dark"]};
    """)

        self.title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_lbl)

        # Messaggio
        self.msg_lbl = QLabel(message)
        self.msg_lbl.setStyleSheet(f"""
      font-size: 13px;
      color: {COLORS["text_muted"]};
    """)

        self.msg_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.msg_lbl.setWordWrap(True)
        self.msg_lbl.setMaximumWidth(300)
        layout.addWidget(self.msg_lbl)

        # Trasparenza di fondo
        self.setStyleSheet("background: transparent;")
