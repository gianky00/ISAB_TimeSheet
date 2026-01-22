from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.core.config_manager import get_config_value
from src.core.constants import Icons
from src.utils.helpers import get_asset_path, get_colored_icon


class ActionChip(QPushButton):
    """
    Pulsante 'Chip' per azione rapida.
    """

    def __init__(self, text, icon_path, color, parent=None):
        super().__init__(parent)
        self.setText(f"  {text}")  # Spazio per icona
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setIcon(get_colored_icon(get_asset_path(icon_path), color))
        self.setIconSize(QSize(18, 18))
        self.setFixedHeight(38)  # Slightly reduced height

        # Style moderno & Coerente -> Hover NEUTRO (Grigio chiaro)
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #ffffff;
                color: #495057;
                border: 1px solid #dee2e6;
                border-radius: 19px;
                padding: 0 15px;
                font-weight: 600;
                font-size: 13px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                border-color: #ced4da;
                color: #212529;
            }
            QPushButton:pressed {
                background-color: #e9ecef;
            }
        """
        )


# Registry of all available actions with 3-level hierarchy
# Path format: [Level1, Level2] - excludes the action text itself
# Level 1 & 2 are non-selectable groups, Level 3 items are selectable
AVAILABLE_ACTIONS = {
    # ============================================================
    # PRIMO LIVELLO: Automazioni > SECONDO LIVELLO: Portale Fornitori
    # ============================================================
    "nav_dettagli_oda": {
        "text": "Dettagli OdA",
        "icon": Icons.LIST,
        "color": "#6610f2",
        "path": ["Automazioni", "Portale Fornitori"],
    },
    "nav_scarico_ts": {
        "text": "Scarico TS",
        "icon": Icons.DOWNLOAD,
        "color": "#0d6efd",
        "path": ["Automazioni", "Portale Fornitori"],
    },
    "nav_carico_ts": {
        "text": "Carico TS",
        "icon": Icons.UPLOAD,
        "color": "#20c997",
        "path": ["Automazioni", "Portale Fornitori"],
    },
    "pf_timbrature": {
        "text": "Timbrature",
        "icon": Icons.CLOCK,
        "color": "#fd7e14",
        "path": ["Automazioni", "Portale Fornitori"],
    },
    "pf_prenota_bp": {
        "text": "Prenota BP",
        "icon": Icons.CALENDAR,
        "color": "#198754",
        "path": ["Automazioni", "Portale Fornitori"],
    },
    # ============================================================
    # PRIMO LIVELLO: DataBase > SECONDO LIVELLO: Strumentale
    # ============================================================
    "nav_sub_strumentale_0": {
        "text": "Preventivi",
        "icon": Icons.FOLDER,
        "color": "#fd7e14",
        "path": ["DataBase", "Strumentale"],
    },
    "nav_sub_strumentale_1": {
        "text": "Giornaliere",
        "icon": Icons.FOLDER,
        "color": "#fd7e14",
        "path": ["DataBase", "Strumentale"],
    },
    "nav_sub_strumentale_2": {
        "text": "Attività Programmate",
        "icon": Icons.CALENDAR,
        "color": "#fd7e14",
        "path": ["DataBase", "Strumentale"],
    },
    "nav_sub_strumentale_3": {
        "text": "Certificati Campione",
        "icon": Icons.FILE_TEXT,
        "color": "#fd7e14",
        "path": ["DataBase", "Strumentale"],
    },
    "nav_sub_strumentale_4": {
        "text": "Analisi KPI",
        "icon": Icons.BAR_CHART,
        "color": "#fd7e14",
        "path": ["DataBase", "Strumentale"],
    },
    # ============================================================
    # PRIMO LIVELLO: DataBase > SECONDO LIVELLO: DataEase
    # ============================================================
    "nav_page_5": {
        "text": "DataEase",
        "icon": Icons.DOWNLOAD,
        "color": "#fd7e14",
        "path": ["DataBase"],
    },
    # ============================================================
    # PRIMO LIVELLO: DataBase > SECONDO LIVELLO: PDL
    # ============================================================
    "nav_page_6": {
        "text": "PDL",
        "icon": Icons.PDL,
        "color": "#fd7e14",
        "path": ["DataBase"],
    },
    "nav_page_11": {
        "text": "Dipendenti",
        "icon": Icons.DIPENDENTI,
        "color": "#fd7e14",
        "path": ["DataBase"],
    },
    "nav_storico_oda": {
        "text": "Storico OdA",
        "icon": Icons.FILE_TEXT,
        "color": "#fd7e14",
        "path": ["DataBase"],
    },
    # ============================================================
    # PRIMO LIVELLO: Lyra AI (selectable root)
    # ============================================================
    "nav_page_2": {
        "text": "Lyra AI",
        "icon": Icons.SPARKLES,
        "color": "#6f42c1",
        "path": [],
    },
    # ============================================================
    # PRIMO LIVELLO: Notifiche > SECONDO LIVELLO: Audit
    # ============================================================
    "nav_sub_notifiche_1": {
        "text": "Audit",
        "icon": Icons.SHIELD,
        "color": "#ffc107",
        "path": ["Notifiche"],
    },
    # ============================================================
    # PRIMO LIVELLO: Impostazioni > SECONDO LIVELLO: Items
    # ============================================================
    "settings_configurazione": {
        "text": "Configurazione",
        "icon": Icons.SETTINGS,
        "color": "#adb5bd",
        "path": ["Impostazioni"],
    },
    "settings_backup_cloud": {
        "text": "Backup Cloud",
        "icon": Icons.CLOUD,
        "color": "#adb5bd",
        "path": ["Impostazioni"],
    },
    "settings_statistiche": {
        "text": "Statistiche",
        "icon": Icons.BAR_CHART,
        "color": "#adb5bd",
        "path": ["Impostazioni"],
    },
    "settings_telegram": {
        "text": "Telegram",
        "icon": Icons.MESSAGE_SQUARE,
        "color": "#adb5bd",
        "path": ["Impostazioni"],
    },
    # ============================================================
    # PRIMO LIVELLO: Guida (selectable root)
    # ============================================================
    "nav_page_8": {
        "text": "Guida",
        "icon": Icons.HELP,
        "color": "#0dcaf0",
        "path": [],
    },
}


class QuickActions(QWidget):
    """
    Toolbar orizzontale scrollabile con azioni rapide configurabili.
    """

    action_clicked = pyqtSignal(str)  # Emits action key

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)  # Spazio minimo tra titolo e pulsanti

        title = QLabel("Azioni Rapide")
        title.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #495057; margin-bottom: 0px;"
        )
        layout.addWidget(title)

        # Grid Layout per 2 righe (no scroll)
        self.chips_widget = QWidget()
        self.chips_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.chips_layout = QGridLayout(self.chips_widget)
        self.chips_layout.setContentsMargins(
            0, 4, 0, 0
        )  # Margine minimo sopra i pulsanti
        self.chips_layout.setSpacing(8)  # Spazio tra i pulsanti
        self.chips_layout.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )

        layout.addWidget(self.chips_widget)
        layout.addStretch()

        # Context Menu Policy
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

        self.refresh_actions()

    def _show_context_menu(self, pos):
        """Mostra menu contestuale per personalizzare."""
        from PyQt6.QtWidgets import QMenu

        from src.gui.dialogs.quick_actions_config import QuickActionsConfigDialog

        menu = QMenu(self)

        # Stile light theme per il menu contestuale
        menu.setStyleSheet(
            """
            QMenu {
                background-color: #ffffff;
                color: #212529;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 20px;
                border-radius: 4px;
                background-color: transparent;
            }
            QMenu::item:selected {
                background-color: #f8f9fa;
                color: #212529;
            }
            QMenu::item:pressed {
                background-color: #e9ecef;
            }
        """
        )

        action_cfg = menu.addAction(
            get_colored_icon(get_asset_path(Icons.SETTINGS), "#495057"),
            "Personalizza Azioni...",
        )

        action = menu.exec(self.mapToGlobal(pos))

        if action == action_cfg:
            dlg = QuickActionsConfigDialog(self)
            if dlg.exec():
                self.refresh_actions()

    def refresh_actions(self):
        """Ricarica le azioni dalla configurazione e le dispone su max 2 righe."""
        # Clean existing chips
        while self.chips_layout.count() > 0:
            item = self.chips_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Load from config or USE DEFAULT if empty
        saved_keys = get_config_value("quick_actions", [])
        if not saved_keys:
            # Default set if nothing configured
            saved_keys = [
                "nav_page_2",
                "nav_dettagli_oda",
                "nav_scarico_ts",
                "nav_carico_ts",
            ]

        # Calcola quanti pulsanti per riga (max 5 per riga per evitare scroll orizzontale)
        num_actions = len(saved_keys)
        MAX_BUTTONS_PER_ROW = 5  # Limite per evitare scroll orizzontale

        if num_actions <= MAX_BUTTONS_PER_ROW:
            # Se ci sono 5 o meno, una riga sola
            buttons_per_row = num_actions
        else:
            # Più di 5, distribuisci su righe multiple, max 5 per riga
            buttons_per_row = MAX_BUTTONS_PER_ROW

        row = 0
        col = 0

        for key in saved_keys:
            if key in AVAILABLE_ACTIONS:
                meta = AVAILABLE_ACTIONS[key]
                btn = ActionChip(meta["text"], meta["icon"], meta["color"], self)
                # Usa una closure corretta per catturare il valore di key
                btn.clicked.connect(self._create_action_handler(key))

                # Aggiungi al grid
                self.chips_layout.addWidget(btn, row, col)

                col += 1
                if col >= buttons_per_row:
                    col = 0
                    row += 1
                    # Nessun limite di righe, l'utente può vedere tutte le azioni configurate

    def _create_action_handler(self, key):
        """Crea un handler per il click che cattura correttamente il valore di key."""
        return lambda: self.action_clicked.emit(key)
