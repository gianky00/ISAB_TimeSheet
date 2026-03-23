"""
SyncroJob - Base Panel Components
Classi base e worker per i pannelli dei bot.
"""

from __future__ import annotations

import threading
import traceback
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from PyQt6.QtCore import QThread, QTimer, pyqtSignal

if TYPE_CHECKING:
    from src.bots.base.base_bot import BaseBot
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.audit_manager import AuditManager
from src.core.constants import Icons
from src.core.logging import get_logger
from src.core.stats_manager import StatsManager
from src.gui.components.activity_timeline import ActivityTimelineWidget
from src.gui.design.spacing import Spacing
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.dialogs.standard_input_dialog import StandardInputDialog
from src.gui.styles import STATUS_COLORS
from src.gui.widgets import TimelineWidget
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.status_card import StatusCard
from src.utils.helpers import get_asset_path


class BotWorker(QThread):
    """
    Thread worker per eseguire i bot in background.
    Gestisce l'inizializzazione del bot (pesante) e l'esecuzione.
    """

    log_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool)
    request_input_signal = pyqtSignal(str, dict, threading.Event)
    row_status_signal = pyqtSignal(int, bool, str)  # index, success, message
    step_changed_signal = pyqtSignal(int, str, object)  # Bridge for timeline
    critical_error_signal = pyqtSignal(str, str)  # Bridge for license/fatal errors

    def __init__(  # noqa: ANN204
        self,
        bot_id: str | BaseBot,
        bot_params: dict[str, Any] | None = None,
        data: Any = None,  # noqa: ANN401
        telegram_service: Any = None,  # noqa: ANN401
    ):
        """
        Inizializza il worker del bot.

        Args:
            bot_id: ID del bot da creare o istanza già creata.
            bot_params: Parametri per create_bot (se bot_id è str).
            data: I dati di input per il bot.
            telegram_service: Servizio opzionale per notifiche Telegram.
        """
        super().__init__()
        self.bot_id = bot_id
        self.bot_params = bot_params or {}
        self.data = data
        self._is_running = True
        self.telegram_service = telegram_service
        self.bot: BaseBot | None = None

    def run(self):  # noqa: ANN201
        """Avvia l'esecuzione del bot nel thread dedicato."""
        try:
            # 1. Inizializzazione Differita (Background)
            from src.bots import create_bot  # noqa: PLC0415

            if isinstance(self.bot_id, str):
                self.log_signal.emit("🔧 Preparazione ambiente bot...")
                self.bot = create_bot(self.bot_id, **self.bot_params)
            else:
                self.bot = self.bot_id

            if not self.bot:
                self.log_signal.emit("❌ Errore critico: Impossibile creare l'istanza del bot.")
                self.finished_signal.emit(False)
                return

            # 2. Configurazione Bot
            if self.telegram_service:
                self.bot.set_telegram_service(self.telegram_service)

            self.bot.set_log_callback(self.log_signal.emit)
            self.bot.signals.step_changed.connect(self.step_changed_signal.emit)
            self.bot.signals.critical_error.connect(self.critical_error_signal.emit)

            if hasattr(self.bot, "set_input_callback"):
                self.bot.set_input_callback(self._request_input_wrapper)

            if hasattr(self.bot, "set_progress_callback"):
                self.bot.set_progress_callback(self.row_status_signal.emit)

            # 3. Esecuzione
            result = self.bot.execute(self.data)
            self.finished_signal.emit(result)
        except Exception as e:
            error_trace = traceback.format_exc()
            self.log_signal.emit(f"[ERRORE CRITICO] {e}\n{error_trace}")
            self.finished_signal.emit(False)
        finally:
            if self.bot:
                self.bot.cleanup()

    def _request_input_wrapper(self, prompt: str) -> str:
        """
        Wrapper thread-safe per richiedere input all'utente tramite la GUI.
        Blocca l'esecuzione del bot finché l'utente non risponde.

        Args:
            prompt: Messaggio da mostrare all'utente.
        Returns:
            str: Il valore inserito dall'utente.
        """
        result_container: dict[str, str] = {}
        event = threading.Event()
        self.request_input_signal.emit(prompt, result_container, event)
        event.wait()
        return result_container.get("value", "")

    def stop(self):  # noqa: ANN201
        """Interrompe l'esecuzione del bot segnalando la richiesta di stop."""
        self._is_running = False
        if self.bot and hasattr(self.bot, "request_stop"):
            self.bot.request_stop()


class BaseBotPanel(QWidget):
    """
    Classe base per i pannelli di controllo dei bot.
    Gestisce l'interfaccia comune: tabella dati, log, controlli di avvio/stop e report.
    """

    bot_started = pyqtSignal()
    bot_stopped = pyqtSignal()
    bot_finished = pyqtSignal(bool)
    data_updated = pyqtSignal()
    bot_results_ready = pyqtSignal(str, list)  # bot_id, list of results (e.g. file paths)
    status_changed = pyqtSignal(str, str)  # status, message
    autopilot_changed = pyqtSignal()  # Segnale per aggiornamento UI Autopilot

    def __init__(self, bot_id: str, bot_name: str, bot_description: str, parent=None):  # noqa: ANN001, ANN204
        """
        Inizializza il pannello base.

        Args:
            bot_id: Identificativo unico del bot.
            bot_name: Nome visualizzato del bot.
            bot_description: Descrizione delle funzionalità del bot.
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.bot_id = bot_id
        self.bot_name = bot_name
        self.bot_description = bot_description
        self._logger = get_logger(f"gui.panel.{bot_id}")
        self.sync_module_id: str | None = None  # Mapping per SyncTracker (es. 'pdl', 'oda')

        self.worker: BotWorker | None = None
        self.start_time: datetime | None = None
        self._setup_ui()
        self._connect_signals()

        # Inizializza timeline attività in modo differito (Ghost Mode)
        # Usiamo un timer per assicurarci che la sottoclasse abbia completato l'init
        QTimer.singleShot(50, self._init_ghost_timeline)

    def get_bot_class(self) -> type[BaseBot] | None:
        """Restituisce la classe del bot associata al pannello. Da implementare nelle sottoclassi."""
        return None

    def _init_ghost_timeline(self):  # noqa: ANN202
        """Inizializza gli step della timeline utilizzando i metadati della classe del bot."""
        try:
            # 1. Tenta di ottenere la classe direttamente dal pannello (Più robusto)
            bot_class = self.get_bot_class()

            # 2. Fallback al registro se la classe non è fornita
            if not bot_class:
                from src.bots import BOT_REGISTRY  # noqa: PLC0415

                bot_info = BOT_REGISTRY.get(self.bot_id)
                if bot_info:
                    bot_class = bot_info["class"]

            if bot_class and hasattr(bot_class, "STEPS") and bot_class.STEPS:
                self.activity_timeline.set_steps(bot_class.STEPS)
            else:
                self._logger.debug(f"Nessun set di STEPS trovato per il bot_id: {self.bot_id}")
        except Exception as e:
            self._logger.warning(f"Impossibile inizializzare timeline ghost per {self.bot_id}: {e}")

    def showEvent(self, event):  # noqa: ANN001, ANN201
        """Forza l'inizializzazione della timeline all'apertura del pannello."""
        super().showEvent(event)
        QTimer.singleShot(100, self._init_ghost_timeline)

    def _setup_base_ui(self):  # noqa: ANN202
        """Inizializza l'interfaccia utente di base comune a tutti i pannelli bot."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(Spacing.md, Spacing.xs, Spacing.md, Spacing.md)
        self.main_layout.setSpacing(Spacing.md)

        # Widget per le azioni (esposto per permettere ad AutomazioniWidget di spostarlo nel cornerWidget)
        self.controls_widget = QWidget()
        self.controls_layout = QHBoxLayout(self.controls_widget)
        self.controls_layout.setContentsMargins(0, 0, 0, 0)
        self.controls_layout.setSpacing(Spacing.sm)

        self.start_btn = ModernButton(
            "Avvia",
            variant=ModernButton.Variant.SUCCESS,
            size=ModernButton.Size.MEDIUM,
            icon=get_asset_path(Icons.PLAY),
        )
        self.start_btn.setMinimumWidth(110)
        self.start_btn.clicked.connect(self._on_start)
        self.controls_layout.addWidget(self.start_btn)

        self.stop_btn = ModernButton(
            "Stop",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.MEDIUM,
            icon=get_asset_path(Icons.STOP),
        )
        self.stop_btn.setMinimumWidth(90)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self._on_stop)
        self.controls_layout.addWidget(self.stop_btn)

        # Header layout interno al pannello per i controlli
        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(Spacing.xs, 0, Spacing.xs, 0)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.controls_widget)
        self.main_layout.addLayout(self.header_layout)

        # Status Card (Model only, not in layout by default)
        self.status_card = StatusCard("Stato Attività")

        # Top Area: Content + Activity Rail
        top_h_layout = QHBoxLayout()
        top_h_layout.setSpacing(Spacing.md)

        # Content area (da sovrascrivere nelle sottoclassi)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(Spacing.md)
        top_h_layout.addWidget(self.content_widget, stretch=4)

        # Activity Timeline (Cyber-Stepper Rail)
        self.activity_timeline = ActivityTimelineWidget()
        self.activity_timeline.setContentsMargins(10, 10, 10, 10)
        top_h_layout.addWidget(self.activity_timeline, stretch=1)

        self.main_layout.addLayout(top_h_layout)

        # Bottom Area: Activity Log (Cyber Console)
        self.log_widget = TimelineWidget()
        self.main_layout.addWidget(self.log_widget, stretch=2)

    def _setup_ui(self):  # noqa: ANN202
        """
        Inizializza l'interfaccia utente.
        Deve essere sovrascritto nelle sottoclassi se necessario.
        """
        self._setup_base_ui()

    def _update_status(self, color: str, message: str = ""):  # noqa: ANN202
        """Aggiorna la card di stato con colore e messaggio."""
        if not message:
            # Map standard colors to messages
            mapping = {
                STATUS_COLORS["running"]: "In esecuzione...",
                STATUS_COLORS["completed"]: "Completato",
                STATUS_COLORS["pending"]: "In attesa",
                STATUS_COLORS["error"]: "Errore",
            }
            message = mapping.get(color, "In attesa")

        self.status_card.setStatus(message, color)
        self.status_changed.emit(color, message)

    def _connect_signals(self):  # noqa: ANN202
        """Connette i segnali comuni ai callback del pannello."""

    def get_bot_instance(self):  # noqa: ANN201
        """Restituisce un'istanza del bot. Da implementare nelle sottoclassi."""

    def get_current_status(self) -> tuple[str, str]:
        """Restituisce lo stato attuale della card (id, messaggio)."""
        return self.status_card._status, self.status_card._status_label.text()

    def validate_ready(self) -> tuple[bool, str]:
        """
        Verifica se il bot è pronto per l'avvio (credenziali, dati, ecc.).
        Ritorna (Successo, Messaggio Errore).
        Da implementare nelle sottoclassi.
        """
        return True, ""

    def run_externally(self, params: dict[str, Any] | None = None):  # noqa: ANN201
        """
        Avvia il bot programmaticamente con parametri opzionali che sovrascrivono quelli UI.

        Args:
            params: Dizionario di parametri da sovrascrivere (es. {'data_da': '01.01.2025'}).
        """
        self._on_start(params_override=params)

    def add_rows_simple(self, new_rows: list[Any]):  # noqa: ANN201
        """Aggiunge righe alla tabella dati esistente (se presente)."""
        if hasattr(self, "data_table"):
            current_data = self.data_table.get_data()
            current_data.extend(new_rows)
            self.data_table.set_data(current_data)
            if hasattr(self, "_save_data"):
                self._save_data()

    def clear_rows_simple(self):  # noqa: ANN201
        """Svuota la tabella dati."""
        if hasattr(self, "data_table"):
            self.data_table.set_data([])
            if hasattr(self, "_save_data"):
                self._save_data()

    def get_rows_count(self) -> int:
        """Ritorna il numero di righe nella tabella."""
        if hasattr(self, "data_table"):
            return len(self.data_table.get_data())
        return 0

    def _on_start(self, params_override: dict[str, Any] | None = None):  # noqa: ANN202
        """Gestisce l'avvio del bot. Da implementare nelle sottoclassi."""
        self.start_time = datetime.now(UTC)
        self._update_status(STATUS_COLORS["running"])

        # Segnala inizio sync a SyncTracker
        if self.sync_module_id:
            from src.core.sync_tracker import SyncTracker  # noqa: PLC0415

            SyncTracker.mark_start(self.sync_module_id)

        # Pulizia della tabella dagli esiti della sessione precedente (Asincrona per evitare blocchi UI)
        if hasattr(self, "data_table") and hasattr(self.data_table, "clear_status_columns"):
            QTimer.singleShot(0, self.data_table.clear_status_columns)

        # Attiva Cyber-Mood per il log
        if hasattr(self.log_widget, "set_mood"):
            self.log_widget.set_mood("running")

        # Inizializza timeline attività se il bot ha gli steps (doppio controllo)
        bot_class = self.get_bot_class()
        if bot_class and hasattr(bot_class, "STEPS") and bot_class.STEPS:
            self.activity_timeline.set_steps(bot_class.STEPS)

        # Audit & Stats (Defer to next event loop to avoid UI blocking on DB contention)
        QTimer.singleShot(0, self._log_startup_telemetry)

    def _log_startup_telemetry(self):  # noqa: ANN202
        """Esegue il logging di avvio in modo asincrono rispetto all'evento click UI."""
        try:
            AuditManager.instance().log_action(
                action="Avvio Automazione",
                category="automazione",
                entity=self.bot_name,
                params={"bot_id": self.bot_id},
            )
            StatsManager().increment_usage(self.bot_id)
        except Exception as e:
            self._logger.warning(f"Errore durante il logging della telemetria: {e}")

    def _on_stop(self):  # noqa: ANN202
        """Gestisce lo stop del bot."""
        if self.worker:
            self.worker.stop()
            self.log_widget.append("[AVVISO] Stop richiesto...")
            self._update_status(STATUS_COLORS["pending"], "Arresto richiesto...")

    def _on_worker_finished(self, success: bool):  # noqa: ANN202
        """Gestisce il completamento del worker."""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        # Ripristina Cyber-Mood
        if hasattr(self.log_widget, "set_mood"):
            self.log_widget.set_mood("idle")

        duration = self._calculate_duration_str()
        self._log_mission_report(duration, success)

        # Update Status Card
        final_status = STATUS_COLORS["completed"] if success else STATUS_COLORS["error"]
        self._update_status(final_status, "Completato" if success else "Errore")

        # Notify & Signals
        self._handle_worker_completion_signals(success)
        self._notify_completion(success)

        if self.worker:
            self.worker.wait()
            self.worker = None

    def _calculate_duration_str(self) -> str:
        """Helper per calcolare la durata dell'operazione."""
        if not self.start_time:
            return "N/D"
        delta = datetime.now(UTC) - self.start_time
        m, s = divmod(int(delta.total_seconds()), 60)
        return f"{m}m {s}s"

    def _log_mission_report(self, duration: str, success: bool):  # noqa: ANN202
        """Gestisce la UI del report e l'audit."""
        status_text = "SUCCESS" if success else "ERROR"
        self.log_widget.append(f"MISSION REPORT: Duration {duration} | Status: {status_text}", status_text)

        dettagli = "Esecuzione completata correttamente" if success else "Esecuzione fallita o interrotta"

        # Audit (Defer to next event loop cycle)
        QTimer.singleShot(
            0,
            lambda: AuditManager.instance().log_action(
                action="Completamento Automazione",
                category="automazione",
                entity=self.bot_name,
                params={"durata": duration, "dettagli": dettagli},
                status="success" if success else "error",
            ),
        )

    def _handle_worker_completion_signals(self, success: bool):  # noqa: ANN202
        """Invia segnali e gestisce risultati per Telegram."""
        if self.worker and self.worker.bot and hasattr(self.worker.bot, "downloaded_files"):
            files = getattr(self.worker.bot, "downloaded_files", [])
            if files:
                self.bot_results_ready.emit(self.bot_id, files)

        # Tracciamento fallimento tentativi sync
        if not success and self.sync_module_id:
            from src.core.sync_tracker import SyncTracker  # noqa: PLC0415

            SyncTracker.mark_failure(self.sync_module_id)

        self.bot_finished.emit(success)
        self.autopilot_changed.emit()

    def _notify_completion(self, success: bool):  # noqa: ANN202
        """Gestisce le notifiche di sistema e background."""
        win = self.window()
        if win and hasattr(win, "show_background_notification"):
            msg = (
                "Operazione completata con successo."
                if success
                else "Si è verificato un errore durante l'esecuzione."
            )
            title = f"{self.bot_name} - {'Completato' if success else 'Errore'}"

            cast_win: Any = win
            cast_win.show_background_notification(title, msg, is_error=not success)
        else:
            QApplication.alert(self, 0)

    def _on_bot_finished(self, success: bool):  # noqa: ANN202
        """Alias per _on_worker_finished (compatibilità test)."""
        self._on_worker_finished(success)

    def _on_log(self, message: str):  # noqa: ANN202
        """Aggiunge un messaggio al log."""
        if hasattr(self, "log_widget") and self.log_widget:
            self.log_widget.append(message)

    def _on_status(self, status: str):  # noqa: ANN202
        """Aggiorna lo stato (messaggio custom)."""
        # Map string status to StatusCard if possible, or just update message
        # Often bots send generic strings like "Downloading..."
        # We keep the icon based on general state (RUNNING) but update text
        self.status_card._update_status_display(status)
        # We also need to emit the change for the global card
        # Using current status enum, but updating message
        self.status_changed.emit(self.status_card._status, status)

    def _ask_user_input(self, prompt: str, result_container: dict[str, Any], event: threading.Event):  # noqa: ANN202
        """Callback per input utente dal worker (thread-safe via signal)."""
        text, ok = StandardInputDialog.get_input(self, "Richiesta Input", prompt)
        if ok:
            result_container["value"] = text
        else:
            result_container["value"] = ""
        event.set()

    def _setup_worker_connections(self, worker: BotWorker):  # noqa: ANN202
        """Connette tutti i segnali standard del worker ai callback del pannello."""
        worker.log_signal.connect(self._on_log)
        worker.status_signal.connect(self._on_status)
        worker.finished_signal.connect(self._on_worker_finished)

        # Segnale per errori critici (es. licenza revocata) - Bridge via Worker
        worker.critical_error_signal.connect(
            lambda title, msg: ConfirmationDialog.show_error(self, title, msg)
        )

        # Segnale di aggiornamento dati (per sincronizzare altri pannelli)
        if hasattr(self, "data_updated"):
            worker.finished_signal.connect(lambda success: self.data_updated.emit() if success else None)

        # Connessione automatica timeline
        if hasattr(self, "activity_timeline"):
            worker.step_changed_signal.connect(self.activity_timeline.on_step_changed)

        # Connessione input interattivo
        if hasattr(self, "_ask_user_input"):
            worker.request_input_signal.connect(self._ask_user_input)

        # Connessione segnale specifico per riga (Feedback Tabella)
        if hasattr(self, "on_step_completed"):
            worker.row_status_signal.connect(self.on_step_completed)

    def get_credentials(self) -> tuple[str, str]:
        """Ottiene le credenziali dall'account di default."""
        account = config_manager.get_default_account()
        if account:
            return account.get("username", ""), account.get("password", "")
        return "", ""
