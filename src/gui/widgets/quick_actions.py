from typing import Any

from PySide6.QtCore import QPoint, QSize, Qt, Signal
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QMenu,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.core.config_manager import get_config_value
from src.core.constants import Icons
from src.gui.dialogs.quick_actions_config import QuickActionsConfigDialog
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon

from .quick_actions_registry import AVAILABLE_ACTIONS


class ActionChip(QPushButton):
    """
    Pulsante 'Chip' per azione rapida.
    """

    def __init__(self, text: str, icon_path: str, color: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setText(f" {text}")  # Spazio per icona
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setIcon(get_colored_icon(get_asset_path(icon_path), color))
        self.setIconSize(QSize(18, 18))
        self.setFixedHeight(38)  # Slightly reduced height

        # Style moderno & Coerente -> Hover NEUTRO (Grigio chiaro)
        self.setStyleSheet(
            f"""
      QPushButton {{
        background-color: {COLORS["bg_white"]};
        color: {COLORS["text_dark"]};
        border: 1px solid {COLORS["border_light"]};
        border-radius: 19px;
        padding: 0 15px;
        font-weight: 600;
        font-size: 13px;
        text-align: left;
      }}
      QPushButton:hover {{
        background-color: {COLORS["bg_hover"]};
        border-color: {COLORS["border_medium"]};
        color: {COLORS["text_dark"]};
      }}
      QPushButton:pressed {{
        background-color: {COLORS["bg_alt"]};
      }}
    """
        )


class QuickActions(QWidget):
    """
    Toolbar orizzontale scrollabile con azioni rapide configurabili.
    """

    action_clicked = Signal(str)  # Emits action key

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)  # Spazio minimo tra titolo e pulsanti

        title = QLabel("Azioni Rapide")
        title.setStyleSheet(
            f"font-size: 16px; font-weight: bold; color: {COLORS['text_dark']}; margin-bottom: 0px;"
        )
        layout.addWidget(title)

        # Grid Layout per 2 righe (no scroll)
        self.chips_widget = QWidget()
        self.chips_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.chips_layout = QGridLayout(self.chips_widget)
        self.chips_layout.setContentsMargins(0, 4, 0, 0)  # Margine minimo sopra i pulsanti
        self.chips_layout.setSpacing(8)  # Spazio tra i pulsanti
        self.chips_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        layout.addWidget(self.chips_widget)
        layout.addStretch()

        # Context Menu Policy
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

        self.refresh_actions()

    def _show_context_menu(self, pos: QPoint) -> None:
        """Mostra menu contestuale per personalizzare."""
        menu = QMenu(self)

        # Stile light theme per il menu contestuale
        menu.setStyleSheet(
            f"""
      QMenu {{
        background-color: {COLORS["bg_white"]};
        color: {COLORS["text_dark"]};
        border: 1px solid {COLORS["border_light"]};
        border-radius: 6px;
        padding: 5px;
      }}
      QMenu::item {{
        padding: 8px 20px;
        border-radius: 4px;
        background-color: transparent;
      }}
      QMenu::item:selected {{
        background-color: {COLORS["bg_hover"]};
        color: {COLORS["text_dark"]};
      }}
      QMenu::item:pressed {{
        background-color: {COLORS["bg_alt"]};
      }}
    """
        )

        action_cfg = menu.addAction(
            get_colored_icon(get_asset_path(Icons.SETTINGS), COLORS["text_muted"]),
            "Personalizza Azioni...",
        )

        action = menu.exec(self.mapToGlobal(pos))

        if action == action_cfg:
            dlg = QuickActionsConfigDialog(self)
            if dlg.exec():
                self.refresh_actions()

    def refresh_actions(self) -> None:
        """Ricarica le azioni dalla configurazione e le dispone su max 2 righe."""
        # Clean existing chips
        while self.chips_layout.count() > 0:
            item = self.chips_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

        # Load from config or USE DEFAULT if empty
        saved_keys = get_config_value("quick_actions", [])
        if not saved_keys:
            # Default set if nothing configured
            saved_keys = [
                "nav_dettagli_oda",
                "nav_scarico_ts",
                "nav_carico_ts",
                "pf_timbrature",
            ]

        # Calcola quanti pulsanti per riga (max 5 per riga per evitare scroll orizzontale)
        num_actions = len(saved_keys)
        max_buttons_per_row = 5  # Limite per evitare scroll orizzontale

        buttons_per_row = min(num_actions, max_buttons_per_row)

        row = 0
        col = 0

        for key in saved_keys:
            if key in AVAILABLE_ACTIONS:
                meta = AVAILABLE_ACTIONS[key]
                btn = ActionChip(str(meta["text"]), str(meta["icon"]), str(meta["color"]), self)
                # Usa una closure corretta per catturare il valore di key
                btn.clicked.connect(self._create_action_handler(key))

                # Aggiungi al grid
                self.chips_layout.addWidget(btn, row, col)

                col += 1
                if col >= buttons_per_row:
                    col = 0
                    row += 1
                    # Nessun limite di righe, l'utente pu  vedere tutte le azioni configurate

    def _create_action_handler(self, key: str) -> Any:
        """Crea un handler per il click che cattura correttamente il valore di key."""
        return lambda: self.action_clicked.emit(key)
