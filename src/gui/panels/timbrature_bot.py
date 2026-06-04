"""SyncroJob - Timbrature Bot Panel.

Interfaccia operativa dedicata all'automazione del download e della gestione delle timbrature del personale.
Permette di selezionare il fornitore, definire il periodo temporale e monitorare l'avanzamento dello scarico dati dal portale.
Integra segnali per l'aggiornamento dinamico delle statistiche e della dashboard.
"""

import traceback
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QDate, QTimer, Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from src.application.services import config_manager
from src.gui.controllers.bot_worker import BotWorker
from src.gui.panels.base import BaseBotPanel
from src.gui.styles import STATUS_COLORS
from src.gui.widgets import BotParametersWidget
from src.gui.widgets.toast import ToastManager

if TYPE_CHECKING:
    from src.infrastructure.bots.base.base_bot import BaseBot


class TimbratureBotPanel(BaseBotPanel):
    """Pannello operativo per il bot Timbrature.

    Gestisce la configurazione dei parametri di ricerca (fornitore e date) e il ciclo di vita del worker Selenium.
    Emette segnali per notificare il completamento delle operazioni e i cambi di stato dell'Autopilot.

    Inizializza il pannello e prepara il caricamento dei dati salvati.

    Args:
      parent: Widget genitore.

    Attributes:
        data_updated: Segnale o attributo della classe.
        status_changed: Segnale o attributo della classe.
    """

    data_updated = Signal()
    """Segnale emesso quando i dati delle timbrature sono stati aggiornati con successo."""

    status_changed = Signal(str, str)
    """Segnale emesso quando cambia lo stato del bot (stato, messaggio)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(
            bot_id="timbrature",
            bot_name="Timbrature",
            bot_description="Scarica e gestisci le timbrature del personale",
            parent=parent,
        )
        self.sync_module_id = "timbrature"
        self._is_loading = False
        self._setup_content()
        self._data_loaded = False
        # Il caricamento dati viene differito a showEvent

    def showEvent(self, event: Any) -> None:
        """Esegue il primo caricamento dati solo quando il pannello diventa visibile."""
        super().showEvent(event)
        if not self._data_loaded:
            self._data_loaded = True
            QTimer.singleShot(10, self._safe_load_data)

    def get_bot_class(self) -> type["BaseBot"]:
        """Restituisce la classe bot specifica per la gestione delle timbrature."""
        from src.infrastructure.bots.portale_fornitori.timbrature.bot import TimbratureBot

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
        from src.gui.styles.ui_effects import UIEffectsManager
        from src.gui.styles.widget_styles import CARD_SHADOW_BLUR, CARD_SHADOW_COLOR, CARD_STYLE

        # Sezione Parametri
        params_container = QWidget()
        params_container.setStyleSheet(CARD_STYLE)
        UIEffectsManager.apply_shadow(params_container, blur=CARD_SHADOW_BLUR, color=CARD_SHADOW_COLOR)
        UIEffectsManager.animate_fade(params_container, duration=400)

        params_layout = QVBoxLayout(params_container)
        params_layout.setContentsMargins(15, 15, 15, 15)

        self.params_widget = BotParametersWidget(show_date_range=True, show_dest_path=False)
        self.params_widget.settings_requested.connect(self._open_settings)
        self.params_widget.changed.connect(self._save_data)
        params_layout.addWidget(self.params_widget)

        # Inserimento Pulsante "Crea Database"
        from src.gui.widgets.modern_button import ModernButton

        self.create_db_btn = ModernButton(
            "CREA DATABASE", variant=ModernButton.Variant.SECONDARY, size=ModernButton.Size.SMALL
        )
        self.create_db_btn.setToolTip(
            "Analizza e scarica le timbrature mancanti per un intero anno (trimestre per trimestre)"
        )
        self.create_db_btn.clicked.connect(self._on_create_database_clicked)

        # Lo aggiungiamo al widget parametri accanto a DATA FINE
        self.params_widget.add_widget_to_row(self.create_db_btn)

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
            self.params_widget.set_societa(config.get("last_timbrature_societa", "ISAB"))
            self.params_widget.set_fornitore(config.get("last_timbrature_fornitore", ""))
            yesterday = QDate.currentDate().addDays(-1)
            self.params_widget.set_dates(yesterday.toString("dd.MM.yyyy"), yesterday.toString("dd.MM.yyyy"))
        finally:
            self._is_loading = False

    def _save_data(self) -> None:
        """Salva i parametri correnti nella configurazione globale (solo se non in fase di caricamento)."""
        from PySide6.QtWidgets import QApplication

        if QApplication.closingDown():
            return
        if getattr(self, "_is_loading", False) or not hasattr(self, "params_widget"):
            return
        date_da, date_a = self.params_widget.get_dates()
        config_manager.set_config_value("last_timbrature_societa", self.params_widget.get_societa())
        config_manager.set_config_value("last_timbrature_fornitore", self.params_widget.get_fornitore())
        config_manager.set_config_value("last_timbrature_date_da", date_da)
        config_manager.set_config_value("last_timbrature_date_a", date_a)

    def validate_ready(self) -> tuple[bool, str]:
        """Valida i requisiti per l'avvio: credenziali presenti e fornitore selezionato.

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
        societa = self.params_widget.get_societa()
        fornitore, (data_da, data_a) = self.params_widget.get_fornitore(), self.params_widget.get_dates()

        if params_override:
            fornitore = params_override.get("fornitore", fornitore)
            data_da, data_a = params_override.get("data_da", data_da), params_override.get("data_a", data_a)
            societa = params_override.get("societa", societa)

        if not all([username, password, fornitore]):
            ToastManager.instance().show("Verifica i parametri (Fornitore mancante).", "warning")
            self._update_status(STATUS_COLORS["error"], "Parametri incompleti")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            return

        if not params_override:
            self._save_data()

        from src.application.services.config_manager import load_config

        config = load_config()

        main_win = self.window()
        tg_service = getattr(main_win, "telegram", None) if main_win else None

        # Configura i parametri per il BotWorker (verranno passati a create_bot nel thread secondario)
        bot_params = {
            "username": username,
            "password": password,
            "headless": config.get("browser_headless", False),
            "timeout": config.get("browser_timeout", 30),
            "download_path": config_manager.get_download_path(),
            "data_da": data_da,
            "data_a": data_a,
            "fornitore": fornitore,
            "societa": societa,
        }

        # Dati da elaborare
        bot_data = {
            "fornitore": fornitore,
            "societa": societa,
            "data_da": data_da,
            "data_a": data_a,
        }

        # Integrazione modalità Multi-Range (Crea Database)
        if params_override and "ranges" in params_override:
            bot_data["ranges"] = params_override["ranges"]
            # Quando ci sono i ranges, i log devono riflettere lo storico
            log_msg = f"Avvio ricostruzione Database Timbrature ({fornitore})"
        else:
            log_msg = f"Avvio bot Timbrature ({fornitore})"

        # Inizializza il worker (nessuna importazione pesante Selenium qui)
        self.worker = BotWorker(
            bot_id="timbrature",
            bot_params=bot_params,
            data=bot_data,
            telegram_service=tg_service,
        )

        self._setup_worker_connections(self.worker)

        # Override del finished_signal per logica custom
        self.worker.finished_signal.disconnect(self._on_worker_finished)
        self.worker.finished_signal.connect(self._on_worker_finished_custom)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_widget.clear()
        self.log_widget.append(log_msg)
        self.worker.start()
        self.bot_started.emit()

    def _on_worker_finished_custom(self, success: bool) -> None:
        """Gestisce il completamento specifico emettendo il segnale di aggiornamento dati."""
        super()._on_worker_finished(success)
        if success:
            self.data_updated.emit()

    def _on_create_database_clicked(self) -> None:
        """Avvia la procedura di creazione massiva del database storico."""
        from datetime import UTC, datetime

        from PySide6.QtWidgets import QInputDialog

        current_year = datetime.now(UTC).year
        start_year, ok = QInputDialog.getInt(
            self,
            "Crea Database Storico",
            "Anno di inizio ricostruzione:",
            current_year - 1,
            2000,
            current_year,
        )

        if not ok:
            return

        # Generazione Slot Trimestrali dal start_year ad oggi
        ranges = self._generate_quarterly_ranges(start_year)
        if not ranges:
            ToastManager.instance().show("Nessun periodo valido da elaborare.", "info")
            return

        # Avvio Bot in modalità Multi-Range
        fornitore = self.params_widget.get_fornitore()
        if not fornitore:
            ToastManager.instance().show("Seleziona prima un fornitore.", "warning")
            return

        params_override = {
            "ranges": ranges,
            "fornitore": fornitore,
            "societa": self.params_widget.get_societa(),
        }

        self.log_widget.append(
            f"🚀 Ricostruzione DATABASE dal {start_year} ad oggi ({len(ranges)} trimestri)"
        )
        self._on_start(params_override=params_override)

    def _generate_quarterly_ranges(self, start_year: int) -> list[dict[str, str]]:
        """Calcola i trimestri solari dal start_year indicato fino alla data odierna."""
        from datetime import UTC, date, datetime

        today = datetime.now(UTC).date()
        quarters_template = [
            ("01.01", "31.03"),
            ("01.04", "30.06"),
            ("01.07", "30.09"),
            ("01.10", "31.12"),
        ]

        valid_ranges = []
        for year in range(start_year, today.year + 1):
            for start_str, end_str in quarters_template:
                start_d, start_m = map(int, start_str.split("."))
                end_d, end_m = map(int, end_str.split("."))

                q_start = date(year, start_m, start_d)
                q_end = date(year, end_m, end_d)

                # Se il trimestre inizia nel futuro, interrompiamo la generazione
                if q_start > today:
                    break

                # Se il trimestre finisce nel futuro, lo limitiamo ad oggi
                q_end = min(q_end, today)

                valid_ranges.append(
                    {"data_da": q_start.strftime("%d.%m.%Y"), "data_a": q_end.strftime("%d.%m.%Y")}
                )

        return valid_ranges
