from PyQt6.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from src.core.constants import Icons
from src.gui.widgets.sidebar_button import SidebarButton
from src.utils.helpers import get_asset_path, get_colored_icon


class SidebarWidget(QFrame):
    """Widget della sidebar per la navigazione principale, collassabile."""

    navigation_requested = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebarFrame")
        self._is_collapsed = False  # Partenza espansa per setup, poi collassiamo

        # Larghezze
        self.expanded_width = 210  # Leggermente più stretto
        self.collapsed_width = 70

        self.setFixedWidth(self.expanded_width)
        self.setStyleSheet(
            """
            QFrame#sidebarFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4b6cb7, stop:1 #182848);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
            }
            QLabel { color: white; background: transparent; }
            /* Stile per il pulsante toggle */
            QPushButton#toggleBtn {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton#toggleBtn:hover {
                background: rgba(255, 255, 255, 0.2);
            }
        """
        )

        # Aggiungi ombra per profondità
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(5)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)

        self._setup_ui()

        # Collassa di default all'avvio
        QTimer.singleShot(0, self._toggle_sidebar)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 20, 5, 20)
        layout.setSpacing(8)

        # Header con Toggle e Logo
        header_container = QFrame()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(10)

        self.toggle_btn = QPushButton()
        self.toggle_btn.setIcon(get_colored_icon(get_asset_path(Icons.MENU), "#ffffff"))
        self.toggle_btn.setIconSize(QSize(20, 20))
        self.toggle_btn.setObjectName("toggleBtn")
        self.toggle_btn.setFixedSize(38, 38)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.clicked.connect(self._toggle_sidebar)

        self.logo_label = QLabel("SyncroJob")
        self.logo_label.setObjectName("logoLabel")
        self.logo_label.setStyleSheet(
            "font-size: 20px; font-weight: 900; letter-spacing: 1px; color: #ffffff; border: none; margin-left: 2px;"
        )

        header_layout.addWidget(self.toggle_btn, 0, Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(self.logo_label)
        header_layout.addStretch()

        layout.addWidget(header_container)

        # Separatore
        self.separator = QFrame()
        self.separator.setObjectName("sidebarSeparator")
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setStyleSheet("color: rgba(255,255,255,0.3);")
        layout.addWidget(self.separator)

        layout.addSpacing(15)

        # Pulsanti navigazione
        self.btn_home = SidebarButton("Home", get_asset_path(Icons.HOME))
        self.btn_home.setChecked(True)
        layout.addWidget(self.btn_home)

        self.btn_automazioni = SidebarButton("Automazioni", get_asset_path(Icons.CPU))
        layout.addWidget(self.btn_automazioni)

        self.btn_database = SidebarButton("Database", get_asset_path(Icons.DATABASE))
        layout.addWidget(self.btn_database)

        layout.addStretch()

        self.btn_lyra = SidebarButton("Lyra AI", get_asset_path(Icons.SPARKLES))
        layout.addWidget(self.btn_lyra)

        self.btn_notifications = SidebarButton("Notifiche", get_asset_path(Icons.BELL))
        layout.addWidget(self.btn_notifications)

        self.btn_help = SidebarButton("Guida", get_asset_path(Icons.HELP))
        layout.addWidget(self.btn_help)

        layout.addSpacing(10)

        # Impostazioni
        self.btn_settings = SidebarButton(
            "Impostazioni", get_asset_path(Icons.SETTINGS)
        )
        layout.addWidget(self.btn_settings)

        # Map buttons to indices
        self.nav_buttons = [
            self.btn_home,
            self.btn_automazioni,
            self.btn_lyra,
            self.btn_database,
            self.btn_settings,
            self.btn_help,
            self.btn_notifications,
        ]

        # Connect signals
        for i, btn in enumerate(self.nav_buttons):
            btn.clicked.connect(lambda _, idx=i: self._handle_click(idx))

    def _handle_click(self, index):
        self.navigation_requested.emit(index)
        # Opzionale: se collassato e si clicca, rimane collassato (solo icone)

    def _toggle_sidebar(self):
        """Espande o collassa la sidebar."""
        self._is_collapsed = not self._is_collapsed
        target_width = (
            self.collapsed_width if self._is_collapsed else self.expanded_width
        )

        self.setFixedWidth(target_width)

        # Gestione visibilità elementi
        self.logo_label.setVisible(not self._is_collapsed)
        self.separator.setVisible(not self._is_collapsed)

        # Aggiorna pulsanti
        for btn in self.nav_buttons:
            btn.set_collapsed(self._is_collapsed)

    def set_active_button(self, index: int):
        """Aggiorna lo stato checked dei pulsanti."""
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
