"""
SyncroJob - Ricerca PDL Panel
Pannello per il bot Ricerca PDL (SafeWork).
"""

import traceback
from typing import Any, Dict, Optional

from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import QCheckBox, QComboBox, QGroupBox, QHBoxLayout, QLabel, QVBoxLayout

from src.core import config_manager
from src.gui.panels.base import BaseBotPanel, BotWorker
from src.gui.widgets.toast import ToastManager


class RicercaPDLPanel(BaseBotPanel):
    """
    Pannello per la ricerca ed esportazione massiva dei PDL da SafeWork.
    """

    data_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(
            bot_id="pdl_search",
            bot_name="Ricerca PDL",
            bot_description="Ricerca ed esporta i PDL da SafeWork nel database locale.",
            parent=parent,
        )
        self._setup_content()
        QTimer.singleShot(10, self._load_saved_data)

    def _setup_content(self):
        params_group = QGroupBox("Parametri di Ricerca")
        params_layout = QVBoxLayout(params_group)
        params_layout.setSpacing(15)

        # Riga unica per Flag e Sito
        top_row = QHBoxLayout()

        # 1. Flag Escludi Chiusi
        self.exclude_closed_check = QCheckBox(
            "Escludi permessi chiusi, scaduti o eliminati"
        )
        self.exclude_closed_check.setChecked(True)
        self.exclude_closed_check.stateChanged.connect(self._save_data)
        top_row.addWidget(self.exclude_closed_check)

        top_row.addSpacing(20)

        # 2. Selezione Sito
        top_row.addWidget(QLabel("Sito:"))
        self.site_combo = QComboBox()
        self.site_combo.addItems(["Seleziona tutto", "IGCC", "ISAB Nord", "ISAB Sud"])
        self.site_combo.setMinimumWidth(150)
        self.site_combo.currentTextChanged.connect(self._save_data)
        top_row.addWidget(self.site_combo)

        top_row.addStretch()
        params_layout.addLayout(top_row)

        self.content_layout.addWidget(params_group)
        self.content_layout.addStretch()

    def _load_saved_data(self):
        config = config_manager.load_config()
        self.exclude_closed_check.setChecked(
            config.get("pdl_search_exclude_closed", True)
        )
        saved_site = config.get("pdl_search_site", "Seleziona tutto")
        self.site_combo.setCurrentText(saved_site)

    def _save_data(self):
        config_manager.set_config_value(
            "pdl_search_exclude_closed", self.exclude_closed_check.isChecked()
        )
        config_manager.set_config_value(
            "pdl_search_site", self.site_combo.currentText()
        )

    def get_bot_instance(self):
        from src.bots.safework.pdl.search_bot import SafeWorkPDLSearchBot

        username, password = self.get_credentials()
        config = config_manager.load_config()

        return SafeWorkPDLSearchBot(
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=config_manager.get_download_path(),
        )

    def _on_start(self):
        """Avvia il bot Ricerca PDL."""
        super()._on_start()
        username, password = self.get_credentials()

        if not username or not password:
            ToastManager.instance().show(
                "Configura le credenziali SafeWork nelle Impostazioni.", "warning"
            )
            self._update_status("#C62828", "Credenziali mancanti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        bot = self.get_bot_instance()
        if not bot:
            return

        bot_data = {
            "exclude_closed": self.exclude_closed_check.isChecked(),
            "site_selection": self.site_combo.currentText(),
        }

        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        self.worker = BotWorker(bot, [bot_data], telegram_service=tg_service)
        self.worker.log_signal.connect(self._on_log)
        self.worker.status_signal.connect(self._on_status)
        self.worker.finished_signal.connect(self._on_worker_finished)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append("Avvio Ricerca PDL SafeWork...")
        self.worker.start()
        self.bot_started.emit()

    def get_credentials(self) -> tuple:
        """Override: Recupera credenziali SafeWork."""
        # Prende il default da safework_accounts
        config = config_manager.load_config()
        accounts = config.get("safework_accounts", [])
        if not accounts:
            return "", ""

        # Cerca il default
        default_acc = next((a for a in accounts if a.get("default")), accounts[0])
        return default_acc.get("username", ""), default_acc.get("password", "")

    def _on_worker_finished(self, success: bool):
        super()._on_worker_finished(success)
        if success:
            self.data_updated.emit()
