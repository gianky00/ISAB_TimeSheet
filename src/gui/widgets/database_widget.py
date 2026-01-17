from PyQt6.QtWidgets import QTabWidget

from src.gui.contabilita_panel import ContabilitaPanel
from src.gui.panels import PDLDBPanel, TimbratureDBPanel
from src.gui.scarico_ore_panel import ScaricoOrePanel


class DatabaseWidget(QTabWidget):
    """Pannello raggruppato per i Database con caricamento EAGER (tutto subito)."""

    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window

        # Istanzia TUTTI i pannelli subito
        self.panel_timbrature = TimbratureDBPanel()
        self.panel_contabilita = ContabilitaPanel()
        self.panel_dataease = ScaricoOrePanel()
        self.panel_pdl = PDLDBPanel()

        # Registra riferimenti nella Main Window
        self.mw.timbrature_db_panel = self.panel_timbrature
        self.mw.contabilita_panel = self.panel_contabilita
        self.mw.scarico_ore_panel = self.panel_dataease
        self.mw.pdl_db_panel = self.panel_pdl

        # Aggiungi i tab
        self.addTab(self.panel_timbrature, "Timbrature Isab")
        self.addTab(self.panel_contabilita, "Strumentale")
        self.addTab(self.panel_dataease, "DataEase")
        self.addTab(self.panel_pdl, "Database PDL")
