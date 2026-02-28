from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout
)
from src.gui.widgets.contabilita.preventivi.main_view import PreventiviMainView

class GeneratorePreventiviTab(QWidget):
    """Entry point rifattorizzato per il Generatore di Preventivi/Consuntivi."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Carica il nuovo widget rifattorizzato che contiene i Tab
        self.main_view = PreventiviMainView()
        layout.addWidget(self.main_view)
