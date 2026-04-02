# mypy: disable-error-code="no-any-unimported, unused-ignore"
"""
SyncroJob - Base Bot
Classe base astratta e orchestratore del ciclo di vita per tutti i bot di automazione.
Implementa una robusta State Machine per la gestione degli stati (IDLE, RUNNING, ERROR, etc.),
un sistema di tracciamento progressivo tramite 'Steps' per la timeline della GUI,
e logica enterprise di logging con trace_id.
"""

import re
from abc import ABC, abstractmethod
from collections.abc import Callable
from contextlib import suppress
from enum import Enum, auto
from typing import Any, ClassVar

from PyQt6.QtCore import QObject, pyqtSignal

from src.core.constants import BotStatus, Timeouts, URLs
from src.core.license_updater import run_update
from src.core.license_validator import verify_license
from src.core.logging import generate_trace_id, get_logger, measure_time, with_context

logger = get_logger(__name__)


class StepStatus(Enum):
    """Enumerazione degli stati possibili per un singolo step della timeline operativa."""

    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    ERROR = auto()


class BotSignals(QObject):
    """
    Segnali PyQt6 per la comunicazione asincrona tra il thread del bot e l'interfaccia utente.
    """

    step_changed = pyqtSignal(int, str, object)
    status_changed = pyqtSignal(object)
    log_emitted = pyqtSignal(str, str)
    critical_error = pyqtSignal(str, str)


class BaseBot(ABC):
    """
    Architettura base agnostica dal driver per i bot ISAB/SafeWork.
    """

    ISAB_URL = URLs.ISAB_PORTAL

    def __init__(
        self,
        username: str,
        password: str,
        headless: bool = False,
        timeout: int = Timeouts.DEFAULT,
        download_path: str = "",
    ) -> None:
        self.username = username
        self.password = password
        self.headless = headless
        self.timeout = timeout
        self.download_path = download_path
        self._status = BotStatus.IDLE
        self._stop_requested = False
        self._log_callback: Callable[[str], None] | None = None
        self._input_callback: Callable[[str], str] | None = None
        self._progress_callback: Callable[[int, bool, str], None] | None = None
        self._telegram_service: Any = None
        self.signals = BotSignals()
        self._current_step_index = -1
        self._steps_state: list[StepStatus] = []
        self._trace_id = generate_trace_id()
        self._logger = get_logger(f"bot.{self.__class__.__name__}")

    @property
    @abstractmethod
    def name(self) -> str:
        """Restituisce il nome visualizzato del bot."""

    STEPS: ClassVar[list[tuple[str, str]]] = []

    def _initialize_steps(self) -> None:
        self._steps_state = [StepStatus.PENDING for _ in self.STEPS]

    def update_step(self, step_id: str | int, status: StepStatus, message: str | None = None) -> None:
        if isinstance(step_id, str):
            try:
                index = [s[0] for s in self.STEPS].index(step_id)
            except ValueError:
                return
        else:
            index = step_id

        if not hasattr(self, "_steps_state") or not self._steps_state:
            self._initialize_steps()

        if 0 <= index < len(self._steps_state):
            self._steps_state[index] = status
            self._current_step_index = index
            step_name = self.STEPS[index][1]
            self.signals.step_changed.emit(index, step_name, status)

            if message:
                self.log(f"[{step_name}] {message}", current_step=step_name, step_index=index)
            elif status == StepStatus.RUNNING:
                self.log(f"⏳ Avvio: {step_name}", current_step=step_name, step_index=index)
            elif status == StepStatus.ERROR:
                self.log(f"❌ ERRORE: {step_name}", "ERROR", current_step=step_name, step_index=index)

    @property
    @abstractmethod
    def description(self) -> str:
        """Restituisce la descrizione estesa."""

    @staticmethod
    @abstractmethod
    def get_columns() -> list[dict[str, Any]]:
        """Restituisce lo schema delle colonne."""

    @property
    def status(self) -> BotStatus:
        return self._status

    @status.setter
    def status(self, value: BotStatus) -> None:
        if self._status != value:
            self._status = value
            self.signals.status_changed.emit(value)
            if value in (BotStatus.ERROR, BotStatus.COMPLETED, BotStatus.STOPPED):
                self.log(f"🏁 Stato finale: {value.name}")

    def validate_data(self, data: list[dict[str, Any]] | dict[str, Any]) -> tuple[bool, str]:
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
        self.signals.log_emitted.emit(message, level)
        if self._log_callback:
            self._log_callback(message)

        if (
            current_step is None
            and hasattr(self, "_current_step_index")
            and 0 <= self._current_step_index < len(self.STEPS)
        ):
            current_step = self.STEPS[self._current_step_index][1]

        logger_obj = getattr(self, "_logger", logger)
        trace_id = getattr(self, "_trace_id", "no-trace")
        status_name = self._status.name
        step_idx = step_index if step_index is not None else getattr(self, "_current_step_index", -1)

        getattr(logger_obj, level.lower(), logger_obj.info)(
            message,
            trace_id=trace_id,
            bot_type=self.name.lower().replace(" ", "_"),
            bot_status=status_name,
            current_step=current_step or "",
            step_index=step_idx,
        )

        if self._telegram_service:
            with suppress(Exception):
                clean = re.sub(r"^\[\d{2}:\d{2}:\d{2}\]\s*", "", message.strip())
                self._telegram_service.send_message_sync(f"🔹 *{self.name}*\n{clean}")

    def set_log_callback(self, callback: Callable[[str], None]) -> None:
        self._log_callback = callback

    def set_telegram_service(self, service: Any) -> None:
        self._telegram_service = service

    def set_input_callback(self, callback: Callable[[str], str]) -> None:
        self._input_callback = callback

    def set_progress_callback(self, callback: Callable[[int, bool, str], None]) -> None:
        self._progress_callback = callback

    def request_stop(self) -> None:
        self._stop_requested = True
        self.log("⚠️ Interruzione richiesta...")

    def _check_stop(self) -> None:
        if self._stop_requested:
            raise InterruptedError("Bot interrotto dall'utente")

    @abstractmethod
    def _init_driver(self) -> None:
        """Inizializza il driver del browser specifico."""

    @abstractmethod
    def cleanup(self) -> None:
        """Rilascia le risorse del driver."""

    @abstractmethod
    def _save_error_state(self, error_msg: str) -> None:
        """Salva screenshot e HTML di errore."""

    @abstractmethod
    def _login(self) -> bool:
        """Esegue il login al portale."""

    def _safe_login_with_retry(self, max_retries: int = 2) -> bool:
        """Tenta il login con retry."""
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

    @measure_time(threshold_ms=5000)
    def execute(self, data: list[dict[str, Any]]) -> bool:
        self._stop_requested = False

        try:
            run_update()
        except Exception as le:
            if "REVOCATA" in str(le):
                self.log(f"❌ ACCESSO NEGATO: {le}", "ERROR")
                self.signals.critical_error.emit("Licenza Revocata", str(le))
                self.status = BotStatus.ERROR
                return False

        valid, msg = verify_license()
        if not valid:
            self.log(f"❌ AVVIO NEGATO: {msg}", "ERROR")
            self.status = BotStatus.ERROR
            return False

        self._initialize_steps()
        with with_context(
            trace_id=self._trace_id,
            bot_type=self.name.lower().replace(" ", "_"),
            username=self.username[:3] + "***",
        ):
            self.log(f"⚙️ Avvio {self.name} | Headless: {self.headless} | Timeout: {self.timeout}s")

            valid_res, valid_msg = self.validate_data(data)
            if not valid_res:
                self.log(f"❌ Validazione fallita: {valid_msg}", "ERROR")
                self.status = BotStatus.ERROR
                return False

            result = False
            try:
                if self.STEPS:
                    self.update_step(0, StepStatus.RUNNING)
                if not self._safe_login_with_retry():
                    self.status = BotStatus.ERROR
                    if self.STEPS:
                        self.update_step(0, StepStatus.ERROR)
                    return False
                self.status = BotStatus.RUNNING
                result = self.run(data)
                self.status = BotStatus.COMPLETED if result else BotStatus.ERROR
            except InterruptedError:
                self.log("Bot interrotto", "WARNING")
                self.status = BotStatus.STOPPED
                return False
            except Exception as e:
                self.log(f"✗ Errore fatale: {e}", "ERROR")
                self._save_error_state(str(e))
                self.status = BotStatus.ERROR
                if 0 <= self._current_step_index < len(self.STEPS):
                    self.update_step(self._current_step_index, StepStatus.ERROR)
                return False
            finally:
                self.cleanup()

            return result

    @abstractmethod
    def run(self, data: list[dict[str, Any]]) -> bool:
        """Punto di ingresso della logica bot specifica."""
