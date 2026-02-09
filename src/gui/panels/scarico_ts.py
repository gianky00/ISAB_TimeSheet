"""
SyncroJob - Scarico TS Panel
Pannello per il bot Scarico TS.
"""

import traceback
from typing import Any

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QCheckBox, QGroupBox, QHBoxLayout, QVBoxLayout

from src.core import config_manager
from src.core.constants import Icons
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.base import BaseBotPanel, BotWorker
from src.gui.widgets import BotParametersWidget, EditableDataTable
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path


class ScaricaTSPanel(BaseBotPanel):
    """Pannello per il bot Scarico TS."""

    def __init__(self, parent=None):
        super().__init__(
            bot_id="scarico_ts",
            bot_name="Scarico TS",
            bot_description="Tasto destro per aggiungere/rimuovere righe. Modifica i valori direttamente nelle celle.",
            parent=parent,
        )
        self._setup_content()
        # Defer data loading to speed up startup
        QTimer.singleShot(10, self._safe_load_data)

    def _safe_load_data(self):
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"❌ Error loading data for ScaricaTSPanel: {e}")
            traceback.print_exc()

    def _setup_content(self):
        """Configura il contenuto specifico del pannello."""
        params_group = QGroupBox("Parametri")
        params_layout = QVBoxLayout(params_group)
        params_layout.setSpacing(10)

        # Usiamo il widget atomico per i parametri comuni
        self.params_widget = BotParametersWidget(show_date_range=False, show_dest_path=True)
        self.params_widget.settings_requested.connect(self._open_settings)
        self.params_widget.changed.connect(self._save_data)
        params_layout.addWidget(self.params_widget)

        # Parametri specifici: Flag Elabora TS
        self.elabora_ts_check = QCheckBox("Elabora TS")
        self.elabora_ts_check.stateChanged.connect(self._save_data)
        self.params_widget.add_widget_to_row(self.elabora_ts_check)

        params_layout.addSpacing(10)

        # Tabella
        table_toolbar = QHBoxLayout()
        table_toolbar.addStretch()
        self.clear_btn = ModernButton(
            "Pulisci Tabella",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.TRASH),  # ModernButton handles coloring now
        )
        self.clear_btn.clicked.connect(self._clear_table)
        table_toolbar.addWidget(self.clear_btn)
        params_layout.addLayout(table_toolbar)

        self.data_table = EditableDataTable([{"name": "Numero OdA", "type": "text"}])
        self.data_table.setMinimumHeight(250)
        self.data_table.data_changed.connect(self._save_data)
        params_layout.addWidget(self.data_table)

        self.content_layout.addWidget(params_group)

    def _open_settings(self):
        """Apre le impostazioni."""
        main_window = self.window()
        if main_window and hasattr(main_window, "show_settings"):
            main_window.show_settings()

    def refresh_fornitori(self):
        """Ricarica i fornitori nel pannello Scarica TS."""
        self.params_widget.refresh_fornitori()

    def _load_saved_data(self):
        """Carica i dati salvati."""
        config = config_manager.load_config()
        self.refresh_fornitori()

        # Usa il widget per i parametri comuni
        self.params_widget.set_fornitore(config.get("last_ts_fornitore", ""))
        self.params_widget.set_dates(config.get("last_ts_date", "01.01.2025"))
        self.params_widget.set_dest_path(config.get("path_scarico_ts", ""))

        # Carica dati specifici
        saved_data = config.get("last_ts_data", [])
        if saved_data:
            self.data_table.set_data(saved_data)

        self.elabora_ts_check.setChecked(config.get("elabora_ts", False))

    def _save_data(self):
        """Salva i dati correnti."""
        if not hasattr(self, "params_widget"):
            return

        date_da, _ = self.params_widget.get_dates()
        config_manager.set_config_value("last_ts_data", self.data_table.get_data())
        config_manager.set_config_value("last_ts_date", date_da)
        config_manager.set_config_value("last_ts_fornitore", self.params_widget.get_fornitore())
        config_manager.set_config_value("path_scarico_ts", self.params_widget.get_dest_path())
        config_manager.set_config_value("elabora_ts", self.elabora_ts_check.isChecked())

    def _clear_table(self):
        """Pulisce la tabella."""
        if ConfirmationDialog.confirm(self, "Conferma", "Svuotare la tabella?"):
            self.data_table.set_data([])
            self._save_data()

    def get_bot_instance(self):
        """Crea e restituisce un'istanza di ScaricaTSBot."""
        from src.bots import create_bot

        username, password = self.get_credentials()
        data_da, _ = self.params_widget.get_dates()
        config = config_manager.load_config()
        return create_bot(
            "scarico_ts",
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=self.params_widget.get_dest_path(),
            data_da=data_da,
            fornitore=self.params_widget.get_fornitore(),
            elabora_ts=self.elabora_ts_check.isChecked(),
        )

    def validate_ready(self) -> tuple[bool, str]:
        """Verifica che il pannello Scarica TS sia pronto per l'esecuzione."""
        if not self.data_table.get_data():
            return False, "Nessun dato OdA inserito in tabella."
        return True, ""

    def _on_start(self, params_override: dict[str, Any] | None = None):
        """Avvia il bot."""
        # Chiamiamo super senza argomenti (il BaseBotPanel._on_start che abbiamo appena modificato
        # si aspetta params_override ma qui non serve passarglielo, serve solo per il log/stato).
        super()._on_start(params_override)

        _username, _password = self.get_credentials()
        data = self.data_table.get_data()
        fornitore = self.params_widget.get_fornitore()

        # Default behavior: get dates from UI
        data_da, _ = self.params_widget.get_dates()

        # Handle Overrides
        if params_override:
            if "data_da" in params_override:
                data_da = params_override["data_da"]
                self.log_widget.append(f"ℹ️ Override Data Inizio: {data_da}")

            # Single Shot Execution Override
            if "single_item" in params_override:
                item = params_override["single_item"]  # Expect dict like {"Numero OdA": "...", ...}
                if item:
                    data = [item]
                    self.log_widget.append(f"ℹ️ Esecuzione singola per: {item.get('Numero OdA', 'N/D')}")

        if not params_override:
            self._save_data()

        bot = self.get_bot_instance()

        if not bot:
            self.log_widget.append("❌ Errore creazione bot (parametri mancanti?)")
            self._update_status("#C62828", "Errore avvio")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        bot_data = {
            "rows": data,
            "data_da": data_da,
            "fornitore": fornitore,
            "elabora_ts": self.elabora_ts_check.isChecked(),
        }

        # Get telegram service safely
        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        self.worker = BotWorker(bot, bot_data, telegram_service=tg_service)
        self.worker.log_signal.connect(self._on_log)
        self.worker.status_signal.connect(self._on_status)
        self.worker.finished_signal.connect(self._on_worker_finished)
        self.worker.request_input_signal.connect(self._ask_user_input)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append(f"Avvio bot Scarico TS ({fornitore})")
        self.worker.start()
        self.bot_started.emit()
