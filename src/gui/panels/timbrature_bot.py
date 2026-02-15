"""
SyncroJob - Timbrature Bot Panel
Pannello per il bot Timbrature (Controlli e Log).
"""

import traceback
from typing import Any

from PyQt6.QtCore import QDate, QTimer, pyqtSignal
from PyQt6.QtWidgets import QGroupBox, QVBoxLayout

from src.core import config_manager
from src.gui.panels.base import BaseBotPanel, BotWorker
from src.gui.widgets import BotParametersWidget
from src.gui.widgets.toast import ToastManager


class TimbratureBotPanel(BaseBotPanel):
    """Pannello per il bot Timbrature (Controlli e Log)."""

    data_updated = pyqtSignal()
    status_changed = pyqtSignal(str, str)  # status, message
    autopilot_changed = pyqtSignal()  # NEW: Segnale per aggiornamento UI real-time

    def __init__(self, parent=None):
        super().__init__(
            bot_id="timbrature",
            bot_name="Timbrature",
            bot_description="Scarica e gestisci le timbrature del personale",
            parent=parent,
        )
        self._is_loading = False  # Protezione caricamento
        self._setup_content()
        # Defer data loading
        QTimer.singleShot(10, self._safe_load_data)

    def _safe_load_data(self):
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"❌ Error loading data for TimbratureBotPanel: {e}")
            traceback.print_exc()

    def _setup_content(self):
        """Configura il contenuto specifico del pannello."""
        params_group = QGroupBox("Parametri")
        params_layout = QVBoxLayout(params_group)

        # Widget atomico
        self.params_widget = BotParametersWidget(show_date_range=True, show_dest_path=False)
        self.params_widget.settings_requested.connect(self._open_settings)
        self.params_widget.changed.connect(self._save_data)
        params_layout.addWidget(self.params_widget)

        self.content_layout.addWidget(params_group)

        # Scheduler rimosso: ora la pianificazione si gestisce dall'Autopilot nella Dashboard

    def _open_settings(self):
        main_window = self.window()
        if main_window and hasattr(main_window, "show_settings"):
            main_window.show_settings()

    def refresh_fornitori(self):
        """Ricarica i fornitori nel pannello timbrature."""
        if hasattr(self, "params_widget"):
            self.params_widget.refresh_fornitori()

    def _load_saved_data(self):
        self._is_loading = True  # Inizio blocco salvataggio
        try:
            self.refresh_fornitori()
            config = config_manager.load_config()

            self.params_widget.set_fornitore(config.get("last_timbrature_fornitore", ""))

            # Default dates: ALWAYS Yesterday
            yesterday = QDate.currentDate().addDays(-1)
            self.params_widget.set_dates(yesterday.toString("dd.MM.yyyy"), yesterday.toString("dd.MM.yyyy"))
        finally:
            self._is_loading = False  # Fine blocco salvataggio

    def _save_data(self):
        # Protezione: Se stiamo caricando, NON salvare (evita sovrascrittura con default)
        if getattr(self, "_is_loading", False):
            return

        if not hasattr(self, "params_widget"):
            return

        date_da, date_a = self.params_widget.get_dates()
        config_manager.set_config_value("last_timbrature_fornitore", self.params_widget.get_fornitore())
        config_manager.set_config_value("last_timbrature_date_da", date_da)
        config_manager.set_config_value("last_timbrature_date_a", date_a)

    def validate_ready(self) -> tuple[bool, str]:
        """Verifica se il pannello è pronto per l'avvio del bot."""
        username, password = self.get_credentials()
        if not username or not password:
            return False, "Credenziali ISAB mancanti."
        if not self.params_widget.get_fornitore():
            return False, "Nessun fornitore selezionato."
        return True, ""

    def _on_start(self, params_override: dict[str, Any] | None = None):
        """Avvia il bot Timbrature."""
        self.log_widget.append(f"DEBUG: Start requested. Override={params_override}")
        super()._on_start(params_override)

        # FIX RACE CONDITION: Se i dati non sono ancora caricati (es. avvio immediato da Palette), caricali ora.
        if hasattr(self, "params_widget") and not self.params_widget.get_fornitore():
            self.log_widget.append("DEBUG: Forcing data load (Race Condition Fix)")
            self._load_saved_data()

        username, password = self.get_credentials()

        fornitore = self.params_widget.get_fornitore()
        data_da, data_a = self.params_widget.get_dates()

        # OVERRIDES
        if params_override:
            if "fornitore" in params_override:
                fornitore = params_override["fornitore"]
            if "data_da" in params_override:
                data_da = params_override["data_da"]
            if "data_a" in params_override:
                data_a = params_override["data_a"]
            if "data_range" in params_override:  # Supporto per singolo campo range
                # Se necessario gestire logica qui
                pass

        self.log_widget.append(f"DEBUG: Params -> Fornitore: {fornitore}, Utente: {username}")

        if not all([username, password, fornitore]):
            self.log_widget.append(
                f"DEBUG: Missing Params! User: {bool(username)}, Pwd: {bool(password)}, Forn: {bool(fornitore)}"
            )

            # If running externally, maybe we can fallback to default config if UI is empty?
            # But normally params_override or UI should provide it.
            ToastManager.instance().show("Verifica i parametri (Fornitore mancante).", "warning")
            self._update_status("#C62828", "Parametri incompleti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        # Only save checks if NOT running external override to avoid overwriting user prefs with temp runs
        if not params_override:
            self._save_data()

        from src.bots import create_bot

        config = config_manager.load_config()
        self.log_widget.append("DEBUG: Creating bot...")
        bot = create_bot(
            "timbrature",
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=config_manager.get_download_path(),
            data_da=data_da,
            data_a=data_a,
            fornitore=fornitore,
        )

        if not bot:
            self.log_widget.append("DEBUG: Bot creation failed!")
            ToastManager.instance().show("Errore creazione bot.", "error")
            return

        bot_data = {"fornitore": fornitore, "data_da": data_da, "data_a": data_a}

        # Get telegram service safely
        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        self.worker = BotWorker(bot, bot_data, telegram_service=tg_service)
        self.worker.log_signal.connect(self._on_log)
        self.worker.status_signal.connect(self._on_status)
        self.worker.finished_signal.connect(self._on_worker_finished_custom)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append(f"Avvio bot Timbrature ({fornitore})")
        self.worker.start()
        self.bot_started.emit()

    def _on_worker_finished_custom(self, success: bool):
        super()._on_worker_finished(success)
        if success:
            self.data_updated.emit()
