"""SyncroJob - Consuntivo Workers.

Worker per operazioni asincrone nel modulo Consuntivi.
"""

from PySide6.QtCore import QThread, Signal

from src.core.contabilita.consuntivo.consuntivo_controller import ConsuntivoController


class ProgWorker(QThread):
    """Worker per il calcolo asincrono del progressivo OdC."""

    finished = Signal(str)

    def __init__(self, controller: ConsuntivoController, year: str) -> None:
        """Inizializza la classe."""
        super().__init__()
        self.controller = controller
        self.year = year

    def run(self) -> None:
        """Esegue il calcolo via controller."""
        prog = self.controller.get_next_progressive(self.year)
        self.finished.emit(prog)
