"""SyncroJob - Bot Execution Controller.

Gestore universale per il coordinamento tra GUI e BotWorker.
Aderisce al principio SRP separando la gestione dello stato dalla visualizzazione.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtCore import QObject, Signal

from src.gui.controllers.bot_worker import BotWorker

if TYPE_CHECKING:
    from src.infrastructure.bots.base.base_bot import BaseBot


class BotExecutionController(QObject):
    """Controller universale per la gestione dell'esecuzione dei bot.

    Centralizza la logica di avvio, stop e gestione dei segnali.

    Inizializza il controller.

    Args:
        bot_id: Identificativo del bot da gestire.
        parent: Oggetto genitore.

    Attributes:
        critical_error: Segnale o attributo della classe.
        execution_finished: Segnale o attributo della classe.
        input_requested: Segnale o attributo della classe.
        log_received: Segnale o attributo della classe.
        row_status_updated: Segnale o attributo della classe.
        status_updated: Segnale o attributo della classe.
        step_changed: Segnale o attributo della classe.
    """

    log_received = Signal(str)
    status_updated = Signal(str)
    execution_finished = Signal(bool)
    row_status_updated = Signal(int, bool, str)
    step_changed = Signal(int, str, object)
    critical_error = Signal(str, str)
    input_requested = Signal(str, dict, object)  # prompt, result_container, event

    def __init__(self, bot_id: str, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.bot_id = bot_id
        self.worker: BotWorker | None = None
        self._is_running = False

    def is_running(self) -> bool:
        """Restituisce True se il bot è in esecuzione."""
        return self._is_running

    def start(
        self,
        bot_params: dict[str, Any],
        data: list[dict[str, Any]] | dict[str, Any],
        telegram_service: Any | None = None,
    ) -> bool:
        """Avvia l'esecuzione asincrona del bot.

        Args:
            bot_params: Parametri di configurazione del bot.
            data: Dati da processare (deve essere una lista di dizionari).
            telegram_service: Servizio per notifiche Telegram.

        Returns:
            bool: True se l'avvio è riuscito.
        """
        if self._is_running:
            return False

        self.worker = BotWorker(
            bot_id=self.bot_id,
            bot_params=bot_params,
            data=data,
            telegram_service=telegram_service,
        )

        # Connessione segnali Worker -> Controller
        self.worker.log_signal.connect(self.log_received.emit)
        self.worker.status_signal.connect(self.status_updated.emit)
        self.worker.finished_signal.connect(self._on_finished)
        self.worker.row_status_signal.connect(self.row_status_updated.emit)
        self.worker.step_changed_signal.connect(self.step_changed.emit)
        self.worker.critical_error_signal.connect(self.critical_error.emit)
        self.worker.request_input_signal.connect(self.input_requested.emit)

        # Pulizia automatica del worker al termine
        self.worker.finished.connect(self.worker.deleteLater)

        self._is_running = True
        self.worker.start()
        return True

    def stop(self) -> None:
        """Richiede l'interruzione controllata del bot."""
        if self.worker and self.worker.isRunning():
            self.worker.stop()

    def _on_finished(self, success: bool) -> None:
        """Gestisce il termine dell'esecuzione del worker."""
        self._is_running = False
        self.execution_finished.emit(success)

    def get_bot_instance(self) -> BaseBot | None:
        """Restituisce l'istanza del bot dal worker."""
        return self.worker.bot if self.worker else None
