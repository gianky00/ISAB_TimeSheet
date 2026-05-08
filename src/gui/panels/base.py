# mypy: disable-error-code="no-untyped-def, no-untyped-call, arg-type, attr-defined, misc, no-redef"
"""
SyncroJob - Base Panel Components
Classi base per i pannelli dei bot.
Refactored V9.5: SRP Compliance via Composition.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from src.bots import BOT_REGISTRY
from src.core import config_manager
from src.core.audit_manager import AuditManager
from src.core.logging import get_logger
from src.core.stats_manager import StatsManager
from src.core.sync_tracker import SyncTracker
from src.gui.design.spacing import Spacing
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.dialogs.standard_input_dialog import StandardInputDialog
from src.gui.panels.bot_components import BotControlComponent, BotLogComponent, BotTimelineComponent
from src.gui.styles import STATUS_COLORS
from src.gui.widgets.status_card import StatusCard

if TYPE_CHECKING:
    import threading

    from src.bots.base.base_bot import BaseBot
    from src.gui.controllers.bot_worker import BotWorker


class BaseBotPanel(QWidget):
    """
    Classe base orchestratrice per i pannelli dei bot.
    Gestisce il ciclo di vita del bot delegando logica e UI a componenti specializzati.
    """

    bot_started = pyqtSignal()
    bot_stopped = pyqtSignal()
    bot_finished = pyqtSignal(bool)
    data_updated = pyqtSignal()
    bot_results_ready = pyqtSignal(str, list)  # bot_id, list of results
    status_changed = pyqtSignal(str, str)  # status, message
    autopilot_changed = pyqtSignal()

    def __init__(
        self, bot_id: str, bot_name: str, bot_description: str, parent: QWidget | None = None
    ) -> None:
        """Inizializza il pannello base e i suoi componenti."""
        super().__init__(parent)
        self.bot_id = bot_id
        self.bot_name = bot_name
        self.bot_description = bot_description
        self._logger = get_logger(f"gui.panel.{bot_id}")
        self.sync_module_id: str | None = None

        self.worker: BotWorker | None = None
        self.start_time: datetime | None = None

        # Componenti Core (Composition)
        self.controls = BotControlComponent()
        self.activity_timeline = BotTimelineComponent()
        self.log_widget = BotLogComponent()
        self.status_card = StatusCard("Stato Attività")

        # Alias di compatibilità per sottoclassi legacy
        self.start_btn = self.controls.start_btn
        self.stop_btn = self.controls.stop_btn

        self._setup_ui()
        self._connect_internal_signals()

    def get_bot_class(self) -> type[BaseBot] | None:
        """Restituisce la classe del bot associata al pannello."""
        return None

    def _init_ghost_timeline(self) -> None:
        """Inizializza gli step della timeline dai metadati del bot."""
        try:
            bot_class = self.get_bot_class()
            if not bot_class:
                bot_info = BOT_REGISTRY.get(self.bot_id)
                if bot_info:
                    config = config_manager.load_config()
                    engine = config.get("automation_engine", "selenium").lower()
                    bot_class = bot_info.get("class_pw") if engine == "playwright" else bot_info.get("class")

            if bot_class and hasattr(bot_class, "STEPS") and bot_class.STEPS:
                self.activity_timeline.set_steps(bot_class.STEPS)
        except Exception as e:
            self._logger.warning("Impossibile inizializzare timeline ghost", bot_id=self.bot_id, error=str(e))

    def showEvent(self, event: Any) -> None:
        """Triggera inizializzazioni differite."""
        super().showEvent(event)
        QTimer.singleShot(100, self._init_ghost_timeline)

    def _setup_ui(self) -> None:
        """Costruisce il layout basato sui componenti."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(Spacing.md, Spacing.xs, Spacing.md, Spacing.md)
        self.main_layout.setSpacing(Spacing.md)

        self.header_layout = QHBoxLayout()
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.controls)
        self.main_layout.addLayout(self.header_layout)

        top_h_layout = QHBoxLayout()
        top_h_layout.setSpacing(Spacing.md)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        top_h_layout.addWidget(self.content_widget, stretch=4)
        top_h_layout.addWidget(self.activity_timeline, stretch=1)

        self.main_layout.addLayout(top_h_layout)
        self.main_layout.addWidget(self.log_widget, stretch=2)

    def _connect_internal_signals(self) -> None:
        """Connette gli eventi dei componenti alle azioni del pannello."""
        self.controls.start_clicked.connect(self._on_start)
        self.controls.stop_clicked.connect(self._on_stop)

    def _update_status(self, color: str, message: str = "") -> None:
        """Aggiorna la visualizzazione dello stato."""
        if not message:
            mapping = {
                STATUS_COLORS["running"]: "In esecuzione...",
                STATUS_COLORS["completed"]: "Completato",
                STATUS_COLORS["pending"]: "In attesa",
                STATUS_COLORS["error"]: "Errore",
            }
            message = mapping.get(color, "In attesa")

        self.status_card.setStatus(message, color)
        self.status_changed.emit(color, message)

    def _on_start(self, params_override: dict[str, Any] | None = None) -> None:
        """Avvia la missione del bot."""
        self.start_time = datetime.now(UTC)
        self._update_status(STATUS_COLORS["running"])
        self.controls.set_running(True)

        if self.sync_module_id:
            SyncTracker.mark_start(self.sync_module_id)

        if hasattr(self, "data_table") and hasattr(self.data_table, "clear_status_columns"):
            QTimer.singleShot(0, self.data_table.clear_status_columns)

        self.log_widget.set_mood("running")

        # Inizializza timeline attività se il bot ha gli steps
        bot_class = self.get_bot_class()
        if bot_class and hasattr(bot_class, "STEPS") and bot_class.STEPS:
            self.activity_timeline.set_steps(bot_class.STEPS)

        QTimer.singleShot(0, self._log_startup_telemetry)

    def _log_startup_telemetry(self) -> None:
        try:
            AuditManager.instance().log_action(
                action="Avvio Automazione",
                category="automazione",
                entity=self.bot_name,
                params={"bot_id": self.bot_id},
            )
            StatsManager().increment_usage(self.bot_id)
        except Exception as e:
            self._logger.warning("Telemetry error", error=str(e))

    def _on_stop(self) -> None:
        """Richiede l'arresto del worker."""
        if self.worker:
            self.worker.stop()
            self.log_widget.log_warning("[AVVISO] Stop richiesto...")
            self._update_status(STATUS_COLORS["pending"], "Arresto richiesto...")

    def _on_worker_finished(self, success: bool) -> None:
        """Finalizza l'esecuzione del worker."""
        self.controls.set_running(False)
        self.log_widget.set_mood("idle")

        duration = self._calculate_duration_str()
        self._log_mission_report(duration, success)

        final_color = STATUS_COLORS["completed"] if success else STATUS_COLORS["error"]
        self._update_status(final_color, "Completato" if success else "Errore")

        self._handle_completion_logic(success)
        self._notify_system(success)

        if self.worker:
            self.worker.wait()
            self.worker = None

    def _on_bot_finished(self, success: bool) -> None:
        """Alias per _on_worker_finished (compatibilità test)."""
        self._on_worker_finished(success)

    def _handle_completion_logic(self, success: bool) -> None:
        """Invia i segnali di completamento e gestisce i risultati."""
        if self.worker and self.worker.bot:
            files = getattr(self.worker.bot, "downloaded_files", [])
            if files:
                self.bot_results_ready.emit(self.bot_id, files)

        if not success and self.sync_module_id:
            SyncTracker.mark_failure(self.sync_module_id)

        self.bot_finished.emit(success)
        self.autopilot_changed.emit()

    def _calculate_duration_str(self) -> str:
        if not self.start_time:
            return "N/D"
        delta = datetime.now(UTC) - self.start_time
        m, s = divmod(int(delta.total_seconds()), 60)
        return f"{m}m {s}s"

    def _log_mission_report(self, duration: str, success: bool) -> None:
        status_text = "SUCCESS" if success else "ERROR"
        self.log_widget.append(f"MISSION REPORT: Duration {duration} | Status: {status_text}", status_text)

        QTimer.singleShot(
            0,
            lambda: AuditManager.instance().log_action(
                action="Completamento Automazione",
                category="automazione",
                entity=self.bot_name,
                params={"durata": duration, "success": success},
                status="success" if success else "error",
            ),
        )

    def _notify_system(self, success: bool) -> None:
        win = self.window()
        if win and hasattr(win, "show_background_notification"):
            msg = "Operazione completata." if success else "Errore esecuzione."
            win.show_background_notification(self.bot_name, msg, is_error=not success)
        else:
            QApplication.alert(self, 0)

    def _setup_worker_connections(self, worker: BotWorker) -> None:
        """Cablaggio segnali worker -> UI."""
        worker.log_signal.connect(self._on_log)
        worker.finished_signal.connect(self._on_worker_finished)
        worker.step_changed_signal.connect(self.activity_timeline.on_step_changed)
        worker.critical_error_signal.connect(lambda t, m: ConfirmationDialog.show_error(self, t, m))
        worker.request_input_signal.connect(self._ask_user_input)

        if hasattr(self, "on_step_completed"):
            worker.row_status_signal.connect(self.on_step_completed)

        worker.finished_signal.connect(lambda s: self.data_updated.emit() if s else None)

    def _ask_user_input(self, prompt: str, result: dict[str, Any], event: threading.Event) -> None:
        text, ok = StandardInputDialog.get_input(self, "Richiesta Input", prompt)
        result["value"] = text if ok else ""
        event.set()

    # --- Compatibility Methods for Subclasses and Tests ---

    def _on_log(self, message: str) -> None:
        """Bridge per il widget log."""
        self.log_widget.append(message)

    def validate_ready(self) -> tuple[bool, str]:
        """Metodo legacy richiesto da alcuni bot."""
        return True, ""

    def get_current_status(self) -> tuple[str, str]:
        """Restituisce lo stato attuale (id, messaggio)."""
        return self.status_card._status, self.status_card._status_label.text()

    def get_rows_count(self) -> int:
        """Ritorna il numero di righe nella tabella (se presente)."""
        if hasattr(self, "data_table"):
            return len(self.data_table.get_data())
        return 0

    def get_bot_instance(self) -> BaseBot | None:
        """Restituisce l'istanza del bot dal worker."""
        return self.worker.bot if self.worker else None

    def run_externally(self, params: dict[str, Any] | None = None) -> None:
        """Avvia il bot da trigger esterni passando eventuali parametri override."""
        self._on_start(params_override=params)

    def get_credentials(self) -> tuple[str, str]:
        """Recupera le credenziali account ISAB di default dalla configurazione."""
        acc = config_manager.get_default_account("isab")
        return (acc.get("username", ""), acc.get("password", "")) if acc else ("", "")

    def add_rows_simple(self, rows: list[Any]) -> None:
        """Aggiunge righe alla tabella dati e persiste lo stato se supportato."""
        if hasattr(self, "data_table"):
            data = self.data_table.get_data()
            data.extend(rows)
            self.data_table.set_data(data)
            if hasattr(self, "_save_data"):
                self._save_data()

    def clear_rows_simple(self) -> None:
        """Svuota rapidamente la tabella dati e salva il nuovo stato."""
        if hasattr(self, "data_table"):
            self.data_table.set_data([])
            if hasattr(self, "_save_data"):
                self._save_data()
