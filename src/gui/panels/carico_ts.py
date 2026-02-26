"""
SyncroJob - Carico TS Panel
Pannello per il bot Carico TS.
"""

import traceback
from typing import Any

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from src.core import config_manager
from src.core.constants import Icons
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.base import BaseBotPanel, BotWorker
from src.gui.styles import STATUS_COLORS
from src.gui.widgets import EditableDataTable
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path


class CaricoTSPanel(BaseBotPanel):
    """
    Pannello per l'automazione del caricamento dei TimeSheet (Carico TS).
    Gestisce l'input dei dati e l'avvio del bot CaricoTSBot.
    """

    def __init__(self, parent=None):
        """
        Inizializza il pannello Carico TS.

        Args:
            parent: Widget genitore.
        """
        super().__init__(
            bot_id="carico_ts",
            bot_name="Carico TS",
            bot_description="Upload automatico dei Timesheet sul portale ISAB",
            parent=parent,
        )
        self._setup_content()
        # Defer data loading
        QTimer.singleShot(10, self._safe_load_data)

    def get_bot_class(self):
        """Restituisce la classe CaricoTSBot associata."""
        from src.bots.portale_fornitori.carico_ts.bot import CaricoTSBot

        return CaricoTSBot

    def _safe_load_data(self):
        """Carica i dati dai file di configurazione in modo sicuro."""
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"❌ Error loading data for CaricoTSPanel: {e}")
            traceback.print_exc()

    def _setup_content(self):
        """Inizializza e posiziona i componenti UI del pannello (Tabella e Parametri)."""
        # Sezione Parametri (Senza QGroupBox per favorire il design Floating Card)
        params_container = QWidget()
        params_layout = QVBoxLayout(params_container)
        params_layout.setContentsMargins(0, 0, 0, 0)
        params_layout.setSpacing(5)

        # Toolbar per la tabella
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

        params_layout.addLayout(table_toolbar)

        # Tabella con tutte le colonne del database Carico TS
        self.data_table = EditableDataTable(
            [
                {"name": "Numero OdA", "type": "text"},
                {"name": "Posizione OdA", "type": "text"},
                {"name": "Codice Fiscale", "type": "text"},
                {"name": "Ingresso", "type": "text"},
                {"name": "Uscita", "type": "text"},
                {"name": "Tipo Prestazione", "type": "text"},
                {"name": "C", "type": "text"},
                {"name": "M", "type": "text"},
                {"name": "Str D", "type": "text"},
                {"name": "Str N", "type": "text"},
                {"name": "Str F D", "type": "text"},
                {"name": "Str F N", "type": "text"},
                {"name": "Sq", "type": "text"},
                {"name": "Nota D", "type": "text"},
                {"name": "Nota S", "type": "text"},
                {"name": "F S", "type": "text"},
                {"name": "G T", "type": "text"},
            ]
        )
        self.data_table.setMinimumHeight(250)
        self.data_table.data_changed.connect(self._save_data)
        params_layout.addWidget(self.data_table)

        self.content_layout.addWidget(params_container)

    def _load_saved_data(self):
        """Carica l'ultima tabella TS salvata nella configurazione."""
        saved_data = config_manager.load_config().get("last_carico_ts_data", [])
        if saved_data:
            self.data_table.set_data(saved_data)

    def _clear_table(self):
        """Svuota la tabella dei dati previa conferma."""
        if ConfirmationDialog.confirm(self, "Conferma", "Sei sicuro di voler cancellare tutte le righe?"):
            self.data_table.clear()
            self._save_data()

    def validate_ready(self) -> tuple[bool, str]:
        """
        Verifica che siano presenti credenziali e dati validi.

        Returns:
            tuple: (bool successo, str messaggio errore)
        """
        username, password = self.get_credentials()
        if not username or not password:
            return False, "Credenziali ISAB mancanti."

        data = self.data_table.get_data()
        if not data:
            return False, "Nessuna riga di dati Timesheet inserita."

        return True, ""

    def _save_data(self):
        """Salva i dati della tabella nella configurazione persistente."""
        data = self.data_table.get_data()
        config_manager.set_config_value("last_carico_ts_data", data)

    def _on_start(self, params_override: dict[str, Any] | None = None):
        """Avvia l'esecuzione del bot Carico TS gestendo il worker."""
        super()._on_start(params_override)
        username, password = self.get_credentials()

        if not username or not password:
            ToastManager.instance().show("Configura le credenziali ISAB nelle Impostazioni.", "warning")
            self._update_status(STATUS_COLORS["error"], "Credenziali mancanti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        data = self.data_table.get_data()
        if not data:
            ToastManager.instance().show(
                "Inserisci almeno una riga con i dati del Timesheet da caricare.",
                "warning",
            )
            self._update_status(STATUS_COLORS["error"], "Dati mancanti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        # Crea e avvia il worker
        from src.bots import create_bot

        config = config_manager.load_config()
        bot = create_bot(
            "carico_ts",
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=config_manager.get_download_path(),
        )

        if not bot:
            ToastManager.instance().show("Impossibile creare il bot.", "error")
            return

        # Get telegram service safely
        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        worker = BotWorker(bot, {"rows": data}, telegram_service=tg_service)
        self.worker = worker
        self._setup_worker_connections(worker)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        self.log_widget.clear()
        self.log_widget.append("Avvio bot Carico TS...")

        worker.start()
        self.bot_started.emit()
