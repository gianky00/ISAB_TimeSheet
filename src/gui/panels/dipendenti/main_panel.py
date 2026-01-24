import logging

from PyQt6.QtWidgets import QVBoxLayout, QWidget

from src.gui.panels.dipendenti.pages.anagrafica_page import AnagraficaPage

logger = logging.getLogger(__name__)


class DipendentiPanel(QWidget):
    """
    Pannello principale Dipendenti.
    Facade che orchestra i sotto-pannelli (Tabs).
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Per ora usiamo direttamente la pagina Anagrafica
        # In futuro, qui metteremo un QTabWidget:
        # self.tabs = QTabWidget()
        # self.tabs.addTab(AnagraficaPage(), "Anagrafica")
        # self.tabs.addTab(CertificatiPage(), "Certificati")
        # main_layout.addWidget(self.tabs)

        self.anagrafica_page = AnagraficaPage()
        main_layout.addWidget(self.anagrafica_page)

    def refresh_data(self):
        """Metodo pubblico chiamato dal controller per aggiornare i dati."""
        if hasattr(self.anagrafica_page, "refresh_data"):
            self.anagrafica_page.refresh_data()
