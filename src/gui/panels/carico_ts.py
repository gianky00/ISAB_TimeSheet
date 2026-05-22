"""SyncroJob - Carico TS Panel.

Pannello per il bot Carico TS.
"""

from __future__ import annotations

import traceback
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from src.core import config_manager
from src.core.constants import Icons
from src.gui.controllers.bot_worker import BotWorker
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.base import BaseBotPanel
from src.gui.styles import STATUS_COLORS
from src.gui.widgets import EditableDataTable
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path

if TYPE_CHECKING:
    from src.bots.base.base_bot import BaseBot


class CaricoTSPanel(BaseBotPanel):
    """Pannello per l'automazione del caricamento dei TimeSheet (Carico TS).

    Gestisce l'input dei dati e l'avvio del bot CaricoTSBot.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza il pannello Carico TS.

        Args:
          parent: Widget genitore.
        """
        super().__init__(
            bot_id="carico_ts",
            bot_name="Carico TS",
            bot_description="Upload automatico dei Timesheet sul portale ISAB",
            parent=parent,
        )

        self.clear_btn: ModernButton
        self.data_table: EditableDataTable

        self._setup_content()
        self._data_loaded = False
        # Il caricamento dati viene differito a showEvent

    def showEvent(self, event: Any) -> None:
        """Esegue il primo caricamento dati solo quando il pannello diventa visibile."""
        super().showEvent(event)
        if not self._data_loaded:
            self._data_loaded = True
            QTimer.singleShot(10, self._safe_load_data)

    def get_bot_class(self) -> type[BaseBot]:
        """Restituisce la classe CaricoTSBot associata."""
        from src.bots.portale_fornitori.carico_ts.bot import CaricoTSBot

        return CaricoTSBot

    def _safe_load_data(self) -> None:
        """Carica i dati dai file di configurazione in modo sicuro."""
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"[ERROR] Error loading data for CaricoTSPanel: {e}")
            traceback.print_exc()

    def _setup_content(self) -> None:
        """Inizializza e posiziona i componenti UI del pannello (Tabella e Parametri)."""
        from src.gui.styles.ui_effects import UIEffectsManager
        from src.gui.styles.widget_styles import CARD_SHADOW_BLUR, CARD_SHADOW_COLOR, CARD_STYLE

        params_container = QWidget()
        params_container.setStyleSheet(CARD_STYLE)
        UIEffectsManager.apply_shadow(params_container, blur=CARD_SHADOW_BLUR, color=CARD_SHADOW_COLOR)
        UIEffectsManager.animate_fade(params_container, duration=400)

        self.params_layout = QVBoxLayout(params_container)
        self.params_layout.setContentsMargins(15, 15, 15, 15)
        self.params_layout.setSpacing(5)

        self._setup_toolbar()
        self._setup_table()

        self.content_layout.addWidget(params_container)

    def _setup_toolbar(self) -> None:
        """Configura la toolbar sopra la tabella."""
        table_toolbar = QHBoxLayout()
        table_toolbar.setContentsMargins(10, 0, 10, 0)
        table_toolbar.addStretch()

        self.clear_btn = ModernButton(
            "Pulisci Tabella",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.TRASH),
        )
        self.clear_btn.clicked.connect(self._clear_table)
        table_toolbar.addWidget(self.clear_btn)

        self.params_layout.addLayout(table_toolbar)

    def _setup_table(self) -> None:
        """Configura la tabella dati principale."""
        # Tabella con tutte le colonne del database Carico TS
        self.data_table = EditableDataTable(self.get_bot_class().get_columns())
        self.data_table.setMinimumHeight(250)
        self.data_table.data_changed.connect(self._save_data)
        self.params_layout.addWidget(self.data_table)

    def _load_saved_data(self) -> None:
        """Carica l'ultima tabella TS salvata nella configurazione."""
        self._is_loading = True
        try:
            saved_data = config_manager.load_config().get("last_carico_ts_data", [])
            if saved_data:
                self.data_table.set_data(saved_data)
        finally:
            self._is_loading = False

    def _save_data(self) -> None:
        """Salva i dati della tabella nella configurazione globale."""
        from PySide6.QtWidgets import QApplication

        if QApplication.closingDown():
            return
        if getattr(self, "_is_loading", False):
            return
        config_manager.set_config_value("last_carico_ts_data", self.data_table.get_data())

    def _clear_table(self) -> None:
        """Svuota la tabella dati previa conferma."""
        if ConfirmationDialog.confirm(self, "Conferma", "Svuotare la tabella?"):
            self.data_table.clear()
            self._save_data()

    def validate_ready(self) -> tuple[bool, str]:
        """Verifica la presenza di credenziali e dati prima dell'avvio.

        Returns:
          tuple: (bool pronto, messaggio errore).
        """
        username, password = self.get_credentials()
        if not username or not password:
            return False, "Credenziali ISAB mancanti."
        if not self.data_table.get_data():
            return False, "Nessun dato inserito in tabella."
        return True, ""

    def _on_start(self, params_override: dict[str, Any] | None = None) -> None:
        """Prepara e avvia il thread per il bot Carico TS."""
        super()._on_start(params_override)
        username, password = self.get_credentials()
        rows = self.data_table.get_data()

        if params_override and "rows" in params_override:
            rows = params_override["rows"]

        if not all([username, password]) or not rows:
            ToastManager.instance().show("Verifica parametri e dati.", "warning")
            self._update_status(STATUS_COLORS["error"], "Parametri incompleti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        if not params_override:
            self._save_data()

        from src.core.config_manager import load_config

        config = load_config()

        main_win: Any = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        # Configura i parametri per il BotWorker (avvio asincrono)
        bot_params = {
            "username": username,
            "password": password,
            "headless": config.get("browser_headless", False),
            "timeout": config.get("browser_timeout", 30),
        }

        # Dati da elaborare
        bot_data = rows

        # Inizializza il worker (nessuna importazione pesante Selenium qui)
        self.worker = BotWorker(
            bot_id="carico_ts",
            bot_params=bot_params,
            data=bot_data,
            telegram_service=tg_service,
        )

        self._setup_worker_connections(self.worker)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append("Avvio bot Carico TS...")
        self.worker.start()
        self.bot_started.emit()
