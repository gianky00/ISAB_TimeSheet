"""
SyncroJob - Bot Step Manager
Componente dedicato alla gestione della timeline operativa dei bot.
Gestisce gli stati degli step e notifica la GUI tramite segnali.
"""

import logging
from enum import Enum, auto
from typing import Any

from PySide6.QtCore import QObject, Signal

logger = logging.getLogger(__name__)


class StepStatus(Enum):
    """Stati possibili per un singolo step della timeline."""

    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    ERROR = auto()


class BotStepManager(QObject):
    """
    Gestisce la progressione degli step di un bot.
    Isola la logica della macchina a stati della timeline dal bot core.
    """

    step_changed = Signal(int, str, object)  # index, name, status

    def __init__(self, steps_definition: list[tuple[str, str]]) -> None:
        """
        Args:
          steps_definition: Lista di tuple (id, label) definita nella classe del bot.
        """
        super().__init__()
        self.steps = steps_definition
        self._states: list[StepStatus] = [StepStatus.PENDING for _ in self.steps]
        self._current_index = -1

    def reset(self) -> None:
        """Ripristina tutti gli step allo stato iniziale."""
        self._states = [StepStatus.PENDING for _ in self.steps]
        self._current_index = -1

    def update_step(self, step_id: Any, status: StepStatus) -> tuple[int, str]:
        """
        Aggiorna lo stato di uno step.

        Args:
          step_id: Stringa (id) o intero (indice).
          status: Nuovo stato.

        Returns:
          Tuple (indice, nome_step) per logging.
        """
        index = -1
        if isinstance(step_id, str):
            try:
                index = [s[0] for s in self.steps].index(step_id)
            except ValueError:
                logger.warning("Step ID '%s' non trovato nelle definizioni.", step_id)
                return -1, ""
        else:
            index = step_id

        if 0 <= index < len(self._states):
            self._states[index] = status
            self._current_index = index
            name = self.steps[index][1]
            self.step_changed.emit(index, name, status)
            return index, name

        return -1, ""

    @property
    def current_step_name(self) -> str:
        """Restituisce il nome dello step attualmente attivo."""
        if 0 <= self._current_index < len(self.steps):
            return self.steps[self._current_index][1]
        return ""

    @property
    def current_index(self) -> int:
        return self._current_index
