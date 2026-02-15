"""
SyncroJob - Prenota BP Panel
Pannello per il bot Prenota BP.
"""

from typing import Any

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout

from src.core import config_manager
from src.core.constants import Icons
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.base import BaseBotPanel, BotWorker
from src.gui.widgets import BotParametersWidget, EditableDataTable
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path


class PrenotaBPPanel(BaseBotPanel):
    """Pannello per il bot Prenota BP."""

    def __init__(self, parent=None):
        super().__init__(
            bot_id="prenota_bp",
            bot_name="Prenota BP",
            bot_description="Gestisce la prenotazione dei Badge Provvisori sul portale.",
            parent=parent,
        )
        self._setup_content()
        # Defer data loading
        QTimer.singleShot(10, self._safe_load_data)

    def _safe_load_data(self):
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"❌ Error loading data for PrenotaBPPanel: {e}")

    def _setup_content(self):
        """Configura il contenuto specifico del pannello."""
        params_group = QGroupBox("Parametri Prenotazione")
        params_layout = QVBoxLayout(params_group)
        params_layout.setSpacing(10)

        # Widget atomico per i parametri - Abilitato date range
        self.params_widget = BotParametersWidget(show_date_range=True, show_dest_path=False)
        self.params_widget.settings_requested.connect(self._open_settings)
        self.params_widget.changed.connect(self._save_data)
        params_layout.addWidget(self.params_widget)

        params_layout.addSpacing(10)

        table_toolbar = QHBoxLayout()
        table_toolbar.addStretch()
        self.clear_btn = ModernButton(
            "Pulisci Tabella",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.TRASH),
            parent=self,
        )
        self.clear_btn.clicked.connect(self._clear_table)
        table_toolbar.addWidget(self.clear_btn)
        params_layout.addLayout(table_toolbar)

        # Definiamo le nuove colonne: NUMERO BP e NOTE DI RITIRO
        columns = [
            {"name": "NUMERO BP", "type": "text"},
            {"name": "NOTE DI RITIRO", "type": "text"},
        ]
        self.data_table = EditableDataTable(columns)
        self.data_table.setMinimumHeight(200)
        self.data_table.data_changed.connect(self._save_data)
        params_layout.addWidget(self.data_table)

        self.content_layout.addWidget(params_group)

    def _open_settings(self):
        """Apre le impostazioni."""
        main_window = self.window()
        if main_window is not None and hasattr(main_window, "show_settings"):
            main_window.show_settings()  # dynamic dispatch via hasattr

    def _load_saved_data(self):
        config = config_manager.load_config()
        saved_data = config.get("last_prenota_bp_data", [])
        if saved_data:
            self.data_table.set_data(saved_data)

        # Usiamo set_dates (metodo corretto di BotParametersWidget)
        date_da = config.get("last_prenota_date_from", "01.01.2024")
        date_a = config.get("last_prenota_date_to", "31.12.2025")
        self.params_widget.set_dates(date_da, date_a)

    def _save_data(self):
        data = self.data_table.get_data()
        config_manager.set_config_value("last_prenota_bp_data", data)

        # Usiamo get_dates (metodo corretto di BotParametersWidget)
        date_da, date_a = self.params_widget.get_dates()
        config_manager.set_config_value("last_prenota_date_from", date_da)
        config_manager.set_config_value("last_prenota_date_to", date_a)

    def _clear_table(self):
        if ConfirmationDialog.confirm(self, "Conferma", "Cancellare tutti i dati dalla lista?"):
            self.data_table.set_data([])
            self._save_data()

    def _on_start(self, params_override: dict[str, Any] | None = None):
        """Override: Prepara e avvia le worker specifico."""
        super()._on_start(params_override)  # Call base to handle logs/status logic

        # Validazione form
        ready, msg = self.validate_ready()
        if not ready:
            ConfirmationDialog.show_warning(self, "Attenzione", msg)
            self._update_status("#C62828", "Validazione fallita")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        # Recupera dati e configura bot
        from src.bots.portale_fornitori.prenota_bp.bot import PrenotaBPBot

        username, password = self.get_credentials()
        config = config_manager.load_config()

        fornitore = self.params_widget.get_fornitore()
        date_da, date_a = self.params_widget.get_dates()

        # Handle Overrides
        rows = self.data_table.get_data()
        if params_override:
            if "fornitore" in params_override:
                fornitore = params_override["fornitore"]
            if "data_da" in params_override:
                date_da = params_override["data_da"]
            if "data_a" in params_override:
                date_a = params_override["data_a"]

            # Single Shot
            if "single_item" in params_override:
                item = params_override["single_item"]
                if item:
                    rows = [item]
                    self.log_widget.append(f"ℹ️ Esecuzione singola per BP: {item.get('numero_bp', 'N/D')}")

        # Get dates from widget
        date_da, date_a_opt = self.params_widget.get_dates()
        date_a = date_a_opt or ""

        bot = PrenotaBPBot(
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            fornitore=fornitore,
            data_da=date_da,
            data_a=date_a,
        )

        bot_data = {
            "rows": rows,
            "fornitore": fornitore,
            "data_da": date_da,
            "data_a": date_a,
        }

        # Get telegram service safely
        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        self.worker = BotWorker(bot, bot_data, telegram_service=tg_service)

        self.worker.log_signal.connect(self._on_log)
        self.worker.status_signal.connect(self._on_status)
        self.worker.finished_signal.connect(self._on_worker_finished)

        # UI Update
        self._update_status("#0d6efd", "Esecuzione...")
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append("Avvio bot Prenota BP...")
        self.worker.start()
        self.bot_started.emit()
