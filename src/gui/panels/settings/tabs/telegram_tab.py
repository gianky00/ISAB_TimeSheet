"""
SyncroJob - Telegram & AI Tab
Pannello per la configurazione del controllo remoto tramite Telegram e dell'integrazione con Gemini AI.
Gestisce l'inserimento sicuro dei token, il pairing dei dispositivi e i test di connettività.
"""

from typing import Any

import requests
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.secrets_manager import SecretsManager
from src.gui.panels.settings.shared import create_group_box, style_button, style_input
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path, get_colored_icon


class TelegramTab(QWidget):
    """
    Tab dedicato alle integrazioni esterne.
    Permette di configurare:
    - Bot Telegram per notifiche push e comandi remoti.
    - Gemini API Key per le funzionalità di intelligenza artificiale (AI Coach).
    Utilizza SecretsManager per la persistenza sicura delle credenziali.
    """

    request_help = pyqtSignal(str)
    """Segnale emesso per richiedere l'apertura della guida alla configurazione."""

    settings_changed = pyqtSignal()
    """Segnale emesso quando i campi token o key vengono modificati."""

    def __init__(self, parent=None):
        """
        Inizializza il tab Telegram.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Configura l'interfaccia utente con form per token e pulsanti di test."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header_layout = QHBoxLayout()
        info = QLabel("Controllo Remoto Telegram")
        info.setStyleSheet("font-size: 20px; font-weight: bold; color: #212529;")
        header_layout.addWidget(info)
        header_layout.addStretch()

        help_btn = QPushButton("Guida alla configurazione")
        help_btn.setIcon(get_colored_icon(get_asset_path(Icons.HELP), "#000000"))
        help_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        help_btn.clicked.connect(lambda: self.request_help.emit("Configurazione Telegram"))
        help_btn.setStyleSheet("background-color: #e7f1ff; color: #0d6efd; border: 1px solid #0d6efd; border-radius: 6px; padding: 8px 15px; font-weight: bold;")
        header_layout.addWidget(help_btn)
        layout.addLayout(header_layout)

        desc = QLabel("Controlla SyncroJob dal tuo smartphone. Avvia bot, controlla lo stato e ricevi notifiche.")
        desc.setStyleSheet("color: #6c757d; font-size: 14px;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        # Configurazione Bot
        group = create_group_box("Configurazione Bot")
        gl = QFormLayout(group)
        gl.setSpacing(15)

        self.tg_token_edit = QLineEdit()
        self.tg_token_edit.setPlaceholderText("Inserisci il Token fornito da @BotFather")
        self.tg_token_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.tg_token_edit.setMinimumHeight(40)
        self.tg_token_edit.textChanged.connect(self.settings_changed.emit)
        style_input(self.tg_token_edit)

        tg_token_layout = QHBoxLayout()
        tg_token_layout.addWidget(self.tg_token_edit)
        self.test_tg_btn = QPushButton("Test")
        self.test_tg_btn.setFixedSize(60, 40)
        self.test_tg_btn.clicked.connect(self._test_telegram_connection)
        style_button(self.test_tg_btn)
        tg_token_layout.addWidget(self.test_tg_btn)
        gl.addRow("API Token:", tg_token_layout)

        self.tg_chat_id_edit = QLineEdit()
        self.tg_chat_id_edit.setPlaceholderText("In attesa del primo messaggio...")
        self.tg_chat_id_edit.setReadOnly(True)
        self.tg_chat_id_edit.setMinimumHeight(40)
        style_input(self.tg_chat_id_edit)

        tg_id_layout = QHBoxLayout()
        tg_id_layout.addWidget(self.tg_chat_id_edit)
        self.tg_reset_btn = QPushButton(" Scollega Dispositivo")
        self.tg_reset_btn.setIcon(get_colored_icon(get_asset_path(Icons.TRASH), "#dc3545"))
        self.tg_reset_btn.setFixedWidth(180)
        self.tg_reset_btn.setMinimumHeight(40)
        self.tg_reset_btn.clicked.connect(self._reset_telegram_pairing)
        self.tg_reset_btn.setStyleSheet("background-color: white; border: 2px solid #dc3545; border-radius: 6px; color: #dc3545; font-weight: bold; padding: 5px;")
        tg_id_layout.addWidget(self.tg_reset_btn)
        gl.addRow("Chat ID Autorizzato:", tg_id_layout)

        # Gemini API Key
        self.gemini_api_key_edit = QLineEdit()
        self.gemini_api_key_edit.setPlaceholderText("Inserisci la Gemini API Key")
        self.gemini_api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.gemini_api_key_edit.setMinimumHeight(40)
        self.gemini_api_key_edit.textChanged.connect(self.settings_changed.emit)
        style_input(self.gemini_api_key_edit)

        gemini_layout = QHBoxLayout()
        gemini_layout.addWidget(self.gemini_api_key_edit)
        self.gemini_toggle_btn = QPushButton()
        self.gemini_toggle_btn.setIcon(get_colored_icon(get_asset_path(Icons.EYE), "#000000"))
        self.gemini_toggle_btn.setFixedSize(40, 40)
        self.gemini_toggle_btn.clicked.connect(self._toggle_gemini_visibility)
        gemini_layout.addWidget(self.gemini_toggle_btn)

        self.test_gemini_btn = QPushButton("Test")
        self.test_gemini_btn.setFixedSize(60, 40)
        self.test_gemini_btn.clicked.connect(self._test_gemini_connection)
        style_button(self.test_gemini_btn)
        gemini_layout.addWidget(self.test_gemini_btn)
        gl.addRow("Gemini API Key:", gemini_layout)

        layout.addWidget(group)
        layout.addStretch()

    def _toggle_gemini_visibility(self):
        """Alterna la visualizzazione in chiaro/asterischi per la API Key di Gemini."""
        if self.gemini_api_key_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.gemini_api_key_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.gemini_toggle_btn.setIcon(get_colored_icon(get_asset_path(Icons.LOCK), "#000000"))
        else:
            self.gemini_api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.gemini_toggle_btn.setIcon(get_colored_icon(get_asset_path(Icons.EYE), "#000000"))

    def _reset_telegram_pairing(self):
        """Rimuove l'ID della chat autorizzata previa conferma dell'utente."""
        if not self.tg_chat_id_edit.text():
            return
        res = QMessageBox.question(self, "Scollega Telegram", "Scollegare il dispositivo?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if res == QMessageBox.StandardButton.Yes:
            self.tg_chat_id_edit.clear()
            self.settings_changed.emit()
            ToastManager.instance().show("Dispositivo scollegato. Salva per applicare.", "warning")

    def _test_telegram_connection(self):
        """Interroga le API di Telegram per verificare la validità del Token inserito."""
        token = self.tg_token_edit.text().strip()
        if not token:
            QMessageBox.warning(self, "Errore", "Inserisci un token Telegram.")
            return
        try:
            resp = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
            if resp.ok and resp.json().get("ok"):
                ToastManager.instance().show("Connessione Telegram OK!", "success")
            else:
                QMessageBox.critical(self, "Errore", "Token non valido o errore di connessione.")
        except Exception:
            QMessageBox.critical(self, "Errore", "Token non valido o errore di connessione.")

    def _test_gemini_connection(self):
        """Verifica la validità della API Key di Gemini (Simulazione)."""
        key = self.gemini_api_key_edit.text().strip()
        if not key:
            QMessageBox.warning(self, "Errore", "Inserisci una API Key.")
            return
        ToastManager.instance().show("Connessione Gemini simulata OK!", "success")

    def load_from_config(self, config: dict[str, Any]):
        """
        Carica i token e le chiavi dalla configurazione o dal gestore segreti di sistema.

        Args:
            config: Dizionario delle impostazioni caricato.
        """
        token = SecretsManager.get_credential("telegram", "token") or config.get("telegram_token", "")
        self.tg_token_edit.setText(token)
        self.tg_chat_id_edit.setText(config.get("telegram_chat_id", ""))
        gemini_key = SecretsManager.get_credential("gemini", "api_key") or config.get("gemini_api_key", "")
        self.gemini_api_key_edit.setText(gemini_key)

    def save_to_config(self, config_manager_instance):
        """
        Salva i dati sensibili in modo sicuro nel portachiavi di sistema se disponibile.

        Args:
            config_manager_instance: Riferimento al gestore configurazione per i dati non sensibili.
        """
        tg_token = self.tg_token_edit.text().strip()
        gemini_key = self.gemini_api_key_edit.text().strip()

        if SecretsManager.is_available():
            SecretsManager.store_credential("telegram", "token", tg_token)
            SecretsManager.store_credential("gemini", "api_key", gemini_key)
            config_manager_instance.set_config_value("telegram_token", "")
            config_manager_instance.set_config_value("gemini_api_key", "")
        else:
            config_manager_instance.set_config_value("telegram_token", tg_token)
            config_manager_instance.set_config_value("gemini_api_key", gemini_key)

        config_manager_instance.set_config_value("telegram_chat_id", self.tg_chat_id_edit.text().strip())
