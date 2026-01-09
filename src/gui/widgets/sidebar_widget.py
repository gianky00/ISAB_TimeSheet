from datetime import datetime

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout

from src.core import config_manager
from src.core.license_validator import get_license_info
from src.core.version import __version__
from src.gui.widgets.sidebar_button import SidebarButton


class SidebarWidget(QFrame):
    """Widget della sidebar per la navigazione principale."""

    navigation_requested = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebarFrame")
        self.setFixedWidth(240)
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
        layout.addWidget(self.logo_label)

        self.subtitle = QLabel("Work & Sync Manager")
        self.subtitle.setObjectName("subtitleLabel")
        layout.addWidget(self.subtitle)

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

        # License Info
        self.license_label = QLabel(self._get_license_text())
        self.license_label.setObjectName("licenseLabel")
        self.license_label.setWordWrap(True)
        layout.addWidget(self.license_label)

        # Separatore
        separator2 = QFrame()
        separator2.setObjectName("sidebarSeparator")
        separator2.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(separator2)

        layout.addSpacing(10)

        # Impostazioni
        self.btn_settings = SidebarButton("Impostazioni", "⚙️")
        layout.addWidget(self.btn_settings)

        # Versione
        version_label = QLabel(f"v{__version__}")
        version_label.setObjectName("versionLabel")
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

    def _get_license_text(self) -> str:
        license_info = get_license_info()
        if license_info:
            client = license_info.get("Cliente", "N/D")
            expiry = license_info.get("Scadenza Licenza", "N/D")
            config = config_manager.load_config()
            last_login = config.get("last_login_date", "N/D")

            # Update last login date
            now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
            config_manager.set_config_value("last_login_date", now_str)

            return (
                f"Licenza: {client}\nScadenza: {expiry}\nUltimo accesso: {last_login}"
            )
        return "Licenza non trovata"

    def set_active_button(self, index: int):
        """Aggiorna lo stato checked dei pulsanti."""
        for i, btn in enumerate(self.nav_buttons):
            btn.blockSignals(True)
            btn.setChecked(i == index)
            btn.blockSignals(False)
