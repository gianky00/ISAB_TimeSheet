from __future__ import annotations

import re
from abc import ABC, abstractmethod
from contextlib import suppress
from typing import TYPE_CHECKING, Any, ClassVar

from PySide6.QtCore import QObject, Signal

from src.bots.base.execution_guard import ExecutionGuard
from src.bots.base.step_manager import BotStepManager, StepStatus
from src.core.constants import BotStatus, Timeouts, URLs
from src.core.logging import generate_trace_id, get_logger, measure_time, with_context

logger = get_logger(__name__)

if TYPE_CHECKING:
    from collections.abc import Callable


class BotSignals(QObject):
    """
    Segnali PySide6 per la comunicazione asincrona tra il thread del bot e l'interfaccia utente.
    """

    step_changed = Signal(int, str, object)
    status_changed = Signal(object)
    log_emitted = Signal(str, str)
    critical_error = Signal(str, str)


class BaseBot(ABC):
    """
    Architettura base agnostica dal driver per i bot ISAB/SafeWork.
    Refactored V9.0: SRP Compliance via BotStepManager and ExecutionGuard.
    """

    ISAB_URL = URLs.ISAB_PORTAL
    """URL base del portale fornitori ISAB."""

    STEPS: ClassVar[list[tuple[str, str]]] = []
    """Definizione degli step sequenziali visualizzati nella GUI."""

    def __init__(  # noqa: PLR0913
        self,
        username: str,
        password: str,
        headless: bool = False,
        timeout: int = Timeouts.DEFAULT,
        download_path: str = "",
        company: str = "ISAB",
    ) -> None:
        """
        Inizializza le propriet  fondamentali del bot.
        """
        self.username = username
        self.password = password
        self.headless = headless
        self.timeout = timeout
        self.download_path = download_path
        self.company = company
        self._status = BotStatus.IDLE
        self._stop_requested = False
        self._log_callback: Callable[[str], None] | None = None
        self._input_callback: Callable[[str], str] | None = None
        self._progress_callback: Callable[[int, bool, str], None] | None = None
        self._telegram_service: Any = None

        # 1. Segnali UI
        self.signals = BotSignals()

        # 2. Gestore Step (SRP)
        self.step_manager = BotStepManager(self.STEPS)
        self.step_manager.step_changed.connect(self.signals.step_changed.emit)

        # 3. Telemetria e Tracciamento
        self._trace_id = generate_trace_id()
        self._logger = get_logger(f"bot.{self.__class__.__name__}")

    @property
    @abstractmethod
    def name(self) -> str:
        """Restituisce il nome visualizzato del bot."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Restituisce la descrizione estesa delle finalit  del bot."""

    @staticmethod
    @abstractmethod
    def get_columns() -> list[dict[str, Any]]:
        """Restituisce lo schema delle colonne per la visualizzazione tabellare."""

    #    Gestione Step (Delegata)

    def update_step(self, step_id: str | int, status: StepStatus, message: str | None = None) -> None:
        """
        Aggiorna lo stato di uno step tramite il gestore dedicato.
        """
        idx, name = self.step_manager.update_step(step_id, status)

        if idx != -1:
            if message:
                self.log(f"[{name}] {message}", current_step=name, step_index=idx)
            elif status == StepStatus.RUNNING:
                self.log(f"[ATTESA] Avvio: {name}", current_step=name, step_index=idx)
            elif status == StepStatus.ERROR:
                self.log(f"❌ ERRORE: {name}", "ERROR", current_step=name, step_index=idx)

    #    Propriet  di Stato

    @property
    def status(self) -> BotStatus:
        """Restituisce lo stato attuale della State Machine del bot."""
        return self._status

    @status.setter
    def status(self, value: BotStatus) -> None:
        """Imposta il nuovo stato ed emette i segnali di notifica relativi."""
        if self._status != value:
            self._status = value
            self.signals.status_changed.emit(value)
            if value in (BotStatus.ERROR, BotStatus.COMPLETED, BotStatus.STOPPED):
                self.log(f"   Stato finale: {value.name}")

    #    Validazione e Logging

    def validate_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> tuple[bool, str]:
        """Verifica la validità formale dei dati di input."""
        if not data:
            return False, "Nessun dato da elaborare."
        if not self.username or not self.password:
            return False, "Credenziali mancanti."
        return True, ""

    def log(
        self,
        message: str,
        level: str = "INFO",
        current_step: str | None = None,
        step_index: int | None = None,
    ) -> None:
        """Emette un log intercettato dalla GUI e registrato nel sistema enterprise."""
        # 1. Notifica UI
        self.signals.log_emitted.emit(message, level)
        if self._log_callback:
            self._log_callback(message)

        # 2. Risoluzione contesto step se omesso
        if current_step is None:
            current_step = self.step_manager.current_step_name
        if step_index is None:
            step_index = self.step_manager.current_index

        # 3. Log di Sistema con Contesto
        logger_obj = getattr(self, "_logger", logger)
        getattr(logger_obj, level.lower(), logger_obj.info)(
            message,
            trace_id=self._trace_id,
            bot_type=self.name.lower().replace(" ", "_"),
            bot_status=self._status.name,
            current_step=current_step or "",
            step_index=step_index,
        )

        # 4. Notifica Telegram (opzionale)
        if self._telegram_service:
            with suppress(Exception):
                clean = re.sub(r"^\[\d{2}:\d{2}:\d{2}\]\s*", "", message.strip())
                self._telegram_service.send_message_sync(f"   *{self.name}*\n{clean}")

    #    Callbacks

    def set_log_callback(self, callback: Callable[[str], None]) -> None:
        """Registra il callback UI usato per ricevere i log del bot."""
        self._log_callback = callback

    def set_telegram_service(self, service: Any) -> None:
        """Imposta il servizio Telegram opzionale per notifiche runtime."""
        self._telegram_service = service

    def set_input_callback(self, callback: Callable[[str], str]) -> None:
        """Registra il callback per richieste input bloccanti all'utente."""
        self._input_callback = callback

    def set_progress_callback(self, callback: Callable[[int, bool, str], None]) -> None:
        """Registra il callback di avanzamento per risultati per-riga."""
        self._progress_callback = callback

    #    Controllo Flusso

    def request_stop(self) -> None:
        """Richiede l'interruzione immediata del bot."""
        self._stop_requested = True
        self.log("⚠️ Interruzione richiesta...")

    def _check_stop(self) -> None:
        """Verifica se  stata richiesta un'interruzione."""
        if self._stop_requested:
            raise InterruptedError("Interrotto")

    #    Ciclo di Vita Driver (Abstract)

    @abstractmethod
    def _init_driver(self) -> None:
        """Inizializza il driver specifico."""

    @abstractmethod
    def cleanup(self) -> None:
        """Rilascia le risorse."""

    @abstractmethod
    def _save_error_state(self, error_msg: str) -> None:
        """Salva screenshot/sorgente in caso di errore."""

    @abstractmethod
    def _login(self) -> bool:
        """Esegue il login al portale."""

    def _safe_login_with_retry(self, max_retries: int = 2) -> bool:
        """Tenta il login con gestione automatica errori."""
        for _ in range(max_retries):
            self._check_stop()
            try:
                self._init_driver()
                if self._login():
                    return True
                self.cleanup()
            except Exception as e:
                self.log(f"⚠️ Errore tentativo: {e}")
                self.cleanup()
        return False

    #    Orchestrazione Esecuzione

    @measure_time(threshold_ms=5000)
    def execute(self, data: list[dict[str, Any]]) -> bool:
        """
        Orchestratore principale dell'esecuzione.
        Delegata la sicurezza a ExecutionGuard e il progresso a BotStepManager.
        """
        self._stop_requested = False

        # 1. Controlli Ambiente (Licenza/Aggiornamenti) - SRP: Delegato a ExecutionGuard
        env_ok, env_msg = ExecutionGuard.check_environment()
        if not env_ok:
            self.log(f"❌ AVVIO NEGATO: {env_msg}", "ERROR")
            if "ACCESSO NEGATO" in env_msg:
                self.signals.critical_error.emit("Licenza", env_msg)
            self.status = BotStatus.ERROR
            return False

        # 2. Preparazione
        self.step_manager.reset()

        with with_context(
            trace_id=self._trace_id,
            bot_type=self.name.lower().replace(" ", "_"),
            username=self.username[:3] + "***",
        ):
            self.log(f"    Avvio {self.name} | Headless: {self.headless} | Timeout: {self.timeout}s")

            # 3. Validazione Dati
            valid_res, valid_msg = self.validate_data(data)
            if not valid_res:
                self.log(f"❌ Validazione fallita: {valid_msg}", "ERROR")
                self.status = BotStatus.ERROR
                return False

            result = False
            try:
                if self.STEPS:
                    self.update_step(0, StepStatus.RUNNING)

                # 4. Workflow Login -> Run
                if self._safe_login_with_retry():
                    self.status = BotStatus.RUNNING
                    result = self.run(data)
                    self.status = BotStatus.COMPLETED if result else BotStatus.ERROR
                else:
                    self.status = BotStatus.ERROR
                    if self.STEPS:
                        self.update_step(0, StepStatus.ERROR)

            except InterruptedError:
                self.log("Bot interrotto", "WARNING")
                self.status = BotStatus.STOPPED
            except Exception as e:
                self.log(f"  Errore fatale: {e}", "ERROR")
                self._save_error_state(str(e))
                self.status = BotStatus.ERROR
                if self.step_manager.current_index != -1:
                    self.update_step(self.step_manager.current_index, StepStatus.ERROR)
            finally:
                self.cleanup()

            return result

    @abstractmethod
    def run(self, data: list[dict[str, Any]]) -> bool:
        """Logica operativa specifica del bot."""
