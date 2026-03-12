"""
SyncroJob - Timbrature Bot Panel
Interfaccia operativa dedicata all'automazione del download e della gestione delle timbrature del personale.
Permette di selezionare il fornitore, definire il periodo temporale e monitorare l'avanzamento dello scarico dati dal portale.
Integra segnali per l'aggiornamento dinamico delle statistiche e della dashboard.
"""

import traceback
from typing import TYPE_CHECKING, Any

from PyQt6.QtCore import QDate, QTimer, pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from src.core import config_manager
from src.gui.panels.base import BaseBotPanel, BotWorker
from src.gui.styles import STATUS_COLORS
from src.gui.widgets import BotParametersWidget
from src.gui.widgets.toast import ToastManager

if TYPE_CHECKING:
    from src.bots.base.base_bot import BaseBot


class TimbratureBotPanel(BaseBotPanel):
    """
    Pannello operativo per il bot Timbrature.
    Gestisce la configurazione dei parametri di ricerca (fornitore e date) e il ciclo di vita del worker Selenium.
    Emette segnali per notificare il completamento delle operazioni e i cambi di stato dell'Autopilot.
    """

    data_updated = pyqtSignal()
    """Segnale emesso quando i dati delle timbrature sono stati aggiornati con successo."""

    status_changed = pyqtSignal(str, str)
    """Segnale emesso quando cambia lo stato del bot (stato, messaggio)."""

    autopilot_changed = pyqtSignal()
    """Segnale emesso per richiedere l'aggiornamento real-time della UI in modalità Autopilot."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il pannello e prepara il caricamento dei dati salvati.

        Args:
            parent: Widget genitore.
        """
        super().__init__(
            bot_id="timbrature",
            bot_name="Timbrature",
            bot_description="Scarica e gestisci le timbrature del personale",
            parent=parent,
        )
        self._is_loading = False
        self._setup_content()
        QTimer.singleShot(10, self._safe_load_data)

    def get_bot_class(self) -> type["BaseBot"]:
        """Restituisce la classe bot specifica per la gestione delle timbrature."""
        from src.bots.portale_fornitori.timbrature.bot import TimbratureBot

        return TimbratureBot

    def _safe_load_data(self) -> None:
        """Tenta il caricamento delle ultime impostazioni dal file di configurazione."""
        try:
            self._load_saved_data()
        except Exception as e:
            print(f"[ERROR] Error loading data for TimbratureBotPanel: {e}")
            traceback.print_exc()

    def _setup_content(self) -> None:
        """Costruisce il layout dei parametri con supporto al range di date."""
        # Sezione Parametri (Senza QGroupBox per favorire il design Floating Card)
        params_container = QWidget()
        params_layout = QVBoxLayout(params_container)
        params_layout.setContentsMargins(0, 0, 0, 0)

        self.params_widget = BotParametersWidget(show_date_range=True, show_dest_path=False)
        self.params_widget.settings_requested.connect(self._open_settings)
        self.params_widget.changed.connect(self._save_data)
        params_layout.addWidget(self.params_widget)

        self.content_layout.addWidget(params_container)

        # Aggiungiamo uno stretch per "spingere" i parametri in alto e creare
        # lo spazio bianco richiesto dove normalmente risiede la tabella.
        self.content_layout.addStretch()

    def _open_settings(self) -> None:
        """Richiede l'apertura del pannello impostazioni generale."""
        main_window = self.window()
        if main_window and hasattr(main_window, "show_settings"):
            main_window.show_settings()

    def refresh_fornitori(self) -> None:
        """Ricarica l'elenco dei fornitori disponibili nel selettore del widget parametri."""
        if hasattr(self, "params_widget"):
            self.params_widget.refresh_fornitori()

    def _load_saved_data(self) -> None:
        """Ripristina il fornitore salvato e imposta le date di default alla giornata di ieri."""
        self._is_loading = True
        try:
            self.refresh_fornitori()
            config = config_manager.load_config()
            self.params_widget.set_fornitore(config.get("last_timbrature_fornitore", ""))
            yesterday = QDate.currentDate().addDays(-1)
            self.params_widget.set_dates(yesterday.toString("dd.MM.yyyy"), yesterday.toString("dd.MM.yyyy"))
        finally:
            self._is_loading = False

    def _save_data(self) -> None:
        """Salva i parametri correnti nella configurazione globale (solo se non in fase di caricamento)."""
        if getattr(self, "_is_loading", False) or not hasattr(self, "params_widget"):
            return
        date_da, date_a = self.params_widget.get_dates()
        config_manager.set_config_value("last_timbrature_fornitore", self.params_widget.get_fornitore())
        config_manager.set_config_value("last_timbrature_date_da", date_da)
        config_manager.set_config_value("last_timbrature_date_a", date_a)

    def validate_ready(self) -> tuple[bool, str]:
        """
        Valida i requisiti per l'avvio: credenziali presenti e fornitore selezionato.

        Returns:
            tuple: (bool pronto, messaggio errore).
        """
        username, password = self.get_credentials()
        if not username or not password:
            return False, "Credenziali ISAB mancanti."
        if not self.params_widget.get_fornitore():
            return False, "Nessun fornitore selezionato."
        return True, ""

    def _on_start(self, params_override: dict[str, Any] | None = None) -> None:
        """Prepara l'ambiente di esecuzione e avvia il thread del bot Timbrature."""
        super()._on_start(params_override)
        if hasattr(self, "params_widget") and not self.params_widget.get_fornitore():
            self._load_saved_data()

        username, password = self.get_credentials()
        fornitore, (data_da, data_a) = self.params_widget.get_fornitore(), self.params_widget.get_dates()

        if params_override:
            fornitore = params_override.get("fornitore", fornitore)
            data_da, data_a = params_override.get("data_da", data_da), params_override.get("data_a", data_a)

        if not all([username, password, fornitore]):
            ToastManager.instance().show("Verifica i parametri (Fornitore mancante).", "warning")
            self._update_status(STATUS_COLORS["error"], "Parametri incompleti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        if not params_override:
            self._save_data()

        from src.bots import create_bot

        config = config_manager.load_config()
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
            ToastManager.instance().show("Errore creazione bot.", "error")
            return

        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None
        bot_data = {"fornitore": fornitore, "data_da": data_da, "data_a": data_a}
        worker = BotWorker(bot, bot_data, telegram_service=tg_service)
        self.worker = worker
        self._setup_worker_connections(worker)
        worker.finished_signal.disconnect(self._on_worker_finished)
        worker.finished_signal.connect(self._on_worker_finished_custom)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append(f"Avvio bot Timbrature ({fornitore})")
        worker.start()
        self.bot_started.emit()

    def _on_worker_finished_custom(self, success: bool) -> None:
        """Gestisce il completamento specifico emettendo il segnale di aggiornamento dati."""
        super()._on_worker_finished(success)
        if success:
            self.data_updated.emit()
