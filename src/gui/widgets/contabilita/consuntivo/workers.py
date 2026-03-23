"""
SyncroJob - Consuntivo Workers
Worker per operazioni asincrone nel modulo Consuntivi.
"""

from PyQt6.QtCore import QThread, pyqtSignal

from src.core.contabilita.consuntivo.consuntivo_controller import ConsuntivoController


class ProgWorker(QThread):
    """Worker per il calcolo asincrono del progressivo OdC."""

    finished = pyqtSignal(str)

    def __init__(self, controller: ConsuntivoController, year: str):  # noqa: ANN204
        super().__init__()
        self.controller = controller
        self.year = year

    def run(self):  # noqa: ANN201
        """Esegue il calcolo via controller."""
        prog = self.controller.get_next_progressive(self.year)
        self.finished.emit(prog)
