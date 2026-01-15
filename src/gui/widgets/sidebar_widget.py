from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout

from src.core.version import __version__
from src.gui.widgets.sidebar_button import SidebarButton


class SidebarWidget(QFrame):
    """Widget della sidebar per la navigazione principale."""

    navigation_requested = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebarFrame")
        self.setFixedWidth(210)
        # FORCE STYLE TO ENSURE TEXT VISIBILITY (as in original main_window.py)
        self.setStyleSheet(
            """
            QFrame#sidebarFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-right: 1px solid rgba(0,0,0,0.1);
            }
            QLabel { color: white; background: transparent; }
        """
        )
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 20, 15, 20)
        layout.setSpacing(10)

        # Logo/Titolo
        self.logo_label = QLabel("🚀 SyncroJob")
        self.logo_label.setObjectName("logoLabel")
        self.logo_label.setStyleSheet(
            "font-size: 24px; font-weight: 800; margin-bottom: 5px;"
        )
        layout.addWidget(self.logo_label)

        # Separatore
        separator = QFrame()
        separator.setObjectName("sidebarSeparator")
        separator.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(separator)

        layout.addSpacing(15)

        # Pulsanti navigazione
        self.btn_home = SidebarButton("Home", "🏠")
        self.btn_home.setChecked(True)
        layout.addWidget(self.btn_home)

        self.btn_automazioni = SidebarButton("Automazioni", "🤖")
        layout.addWidget(self.btn_automazioni)

        self.btn_database = SidebarButton("Database", "🗄️")
        layout.addWidget(self.btn_database)

        layout.addStretch()

        self.btn_lyra = SidebarButton("Lyra AI", "✨")
        layout.addWidget(self.btn_lyra)

        self.btn_notifications = SidebarButton("Notifiche", "🔔")
        layout.addWidget(self.btn_notifications)

        self.btn_help = SidebarButton("Guida", "❓")
        layout.addWidget(self.btn_help)

        layout.addSpacing(10)

        # Impostazioni
        self.btn_settings = SidebarButton("Impostazioni", "⚙️")
        layout.addWidget(self.btn_settings)

        # Versione
        version_label = QLabel(f"v{__version__}")
        version_label.setObjectName("versionLabel")
        version_label.setStyleSheet("font-size: 14px; color: rgba(255, 255, 255, 0.7);")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

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
            btn.clicked.connect(lambda _, idx=i: self.navigation_requested.emit(idx))

    def set_active_button(self, index: int):
        """Aggiorna lo stato checked dei pulsanti."""
        for i, btn in enumerate(self.nav_buttons):
            # Non bloccare i segnali altrimenti l'aggiornamento dello stile non parte
            btn.setChecked(i == index)
