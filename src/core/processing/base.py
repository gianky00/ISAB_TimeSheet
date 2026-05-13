from abc import ABC, abstractmethod
from typing import Any


class ProcessingStep(ABC):
    """Interfaccia base per un passaggio nel processo di elaborazione."""

    @abstractmethod
    def execute(self, context: dict[str, Any]) -> None:
        """Esegue la logica specifica del passaggio."""


class Pipeline:
    """Gestisce l'esecuzione sequenziale di vari passaggi di elaborazione."""

    def __init__(self) -> None:
        self.steps: list[ProcessingStep] = []

    def add_step(self, step: ProcessingStep) -> "Pipeline":
        """Aggiunge un passaggio alla pipeline."""
        self.steps.append(step)
        return self

    def run(self, initial_context: dict[str, Any]) -> dict[str, Any]:
        """Esegue tutti i passaggi registrati."""
        context = initial_context
        for step in self.steps:
            step.execute(context)
        return context
