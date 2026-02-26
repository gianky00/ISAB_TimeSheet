"""
SyncroJob - Telegram Tab (Next-Gen)
Pannello per la configurazione del bridge Telegram strutturato a Card.
"""

from typing import Any

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path, get_colored_icon


class SettingCard(QFrame):
    """
    Container a card con ombra e stile moderno per un gruppo di impostazioni.
    Fornisce coerenza visiva in tutto il pannello.
    """

    def __init__(self, title: str, subtitle: str, icon_key: str, content_widget: QWidget) -> None:
        """
        Inizializza la card di impostazione.

        Args:
            title: Titolo principale.
            subtitle: Descrizione breve.
            icon_key: Chiave icona in Icons.
            content_widget: Widget contenuto.
        """
        super().__init__()
        self.setObjectName("settingCard")
        self.setStyleSheet("""
            QFrame#settingCard {
                background-color: white;
                border: 1px solid #ECEFF1;
                border-radius: 15px;
            }
        """)

        # Shadow Effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 20))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(get_colored_icon(get_asset_path(icon_key), "#009688").pixmap(24, 24))
        header_layout.addWidget(icon_lbl)

        text_container = QVBoxLayout()
        text_container.setSpacing(2)
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #263238;")
        subtitle_lbl = QLabel(subtitle)
        subtitle_lbl.setStyleSheet("font-size: 12px; font-weight: 500; color: #90A4AE;")
        text_container.addWidget(title_lbl)
        text_container.addWidget(subtitle_lbl)
        header_layout.addLayout(text_container)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Separatore
        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: #F5F7F9;")
        layout.addWidget(line)

        # Contenuto
        layout.addWidget(content_widget)
        content_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)


class TelegramTab(QWidget):
    """
    Tab dedicato all'integrazione con il bot Telegram.
    Gestisce token, chat ID e fornisce strumenti di test per la connettività remota.
    """

    settings_changed = pyqtSignal()
    """Segnale emesso quando le credenziali Telegram vengono modificate."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il tab di Telegram.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura il layout a card per credenziali e test di connettività."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scroll Area
        self.scroll_container = QScrollArea()
        self.scroll_container.setWidgetResizable(True)
        self.scroll_container.setStyleSheet("background: transparent; border: none;")

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.cards_layout = QVBoxLayout(scroll_content)
        self.cards_layout.setContentsMargins(30, 30, 30, 30)
        self.cards_layout.setSpacing(25)

        # 1. Credentials Card
        creds_widget = QWidget()
        creds_layout = QVBoxLayout(creds_widget)
        creds_layout.setContentsMargins(0, 10, 0, 0)
        creds_layout.setSpacing(15)

        self.token_edit = QLineEdit()
        self.token_edit.setPlaceholderText("Inserisci Bot Token (7123456789:ABC...)")
        self.token_edit.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.token_edit.textChanged.connect(self.settings_changed.emit)

        self.chat_id_edit = QLineEdit()
        self.chat_id_edit.setPlaceholderText("Inserisci Chat ID (es. 123456789)")
        self.chat_id_edit.textChanged.connect(self.settings_changed.emit)

        creds_layout.addWidget(QLabel("Bot API Token:"))
        creds_layout.addWidget(self.token_edit)
        creds_layout.addWidget(QLabel("Chat ID Destinatario:"))
        creds_layout.addWidget(self.chat_id_edit)

        self.cards_layout.addWidget(SettingCard(
            "Accesso API Telegram",
            "Configura le credenziali del bot per il controllo remoto.",
            Icons.SEND, creds_widget
        ))

        # 2. Connectivity Card
        conn_widget = QWidget()
        conn_layout = QVBoxLayout(conn_widget)
        conn_layout.setContentsMargins(0, 10, 0, 0)
        conn_layout.setSpacing(15)

        self.btn_test = ModernButton("Invia Messaggio di Test", icon=get_asset_path(Icons.SEND))
        self.lbl_status = QLabel("Stato: Servizio non configurato")
        self.lbl_status.setStyleSheet("color: #78909C; font-weight: 600;")

        conn_layout.addWidget(self.btn_test)
        conn_layout.addWidget(self.lbl_status)

        self.cards_layout.addWidget(SettingCard(
            "Test Connettività",
            "Verifica che il bot possa inviare notifiche correttamente.",
            Icons.SPARKLES, conn_widget
        ))

        self.cards_layout.addStretch()
        self.scroll_container.setWidget(scroll_content)
        main_layout.addWidget(self.scroll_container)

    def load_from_config(self, config: dict[str, Any]) -> None:
        """
        Carica i parametri Telegram dalla configurazione attuale.

        Args:
            config: Dizionario di configurazione.
        """
        self.token_edit.setText(config.get("telegram_token", ""))
        self.chat_id_edit.setText(config.get("telegram_chat_id", ""))

    def save_to_config(self, config_manager: Any) -> None:
        """
        Salva i parametri Telegram nel gestore di configurazione.

        Args:
            config_manager: Riferimento al manager globale.
        """
        config_manager.set_config_value("telegram_token", self.token_edit.text().strip())
        config_manager.set_config_value("telegram_chat_id", self.chat_id_edit.text().strip())
