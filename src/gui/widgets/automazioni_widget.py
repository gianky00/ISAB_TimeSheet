from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QTabWidget

from src.core.constants import Icons
from src.gui.panels import (
    CaricoTSPanel,
    DettagliOdAPanel,
    PrenotaBPPanel,
    RicercaPDLPanel,
    ScaricaTSPanel,
    ScaricoPDLPanel,
    TimbratureBotPanel,
)
from src.utils.helpers import get_asset_path


class AutomazioniWidget(QTabWidget):
    """Pannello raggruppato per i Bot con caricamento EAGER (tutto subito)."""

    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window
        self.setTabPosition(QTabWidget.TabPosition.North)

        # --- TAB 1: Portale Fornitori ---
        self.tab_fornitori = QTabWidget()

        # Istanzia TUTTI i pannelli subito
        self.panel_dettagli = DettagliOdAPanel()
        self.panel_prenota = PrenotaBPPanel()
        self.panel_scarico = ScaricaTSPanel()
        self.panel_timbrature = TimbratureBotPanel()
        self.panel_carico = CaricoTSPanel()

        # Aggiungi i tab a Portale Fornitori
        self.tab_fornitori.addTab(
            self.panel_dettagli, QIcon(get_asset_path(Icons.LIST)), "Dettagli OdA"
        )
        self.tab_fornitori.addTab(
            self.panel_scarico, QIcon(get_asset_path(Icons.DOWNLOAD)), "Scarico TS"
        )
        self.tab_fornitori.addTab(
            self.panel_timbrature, QIcon(get_asset_path(Icons.CLOCK)), "Timbrature"
        )
        self.tab_fornitori.addTab(
            self.panel_prenota, QIcon(get_asset_path(Icons.TICKET)), "Prenota BP"
        )
        self.tab_fornitori.addTab(
            self.panel_carico, QIcon(get_asset_path(Icons.UPLOAD)), "Carico TS"
        )

        # --- TAB 2: SafeWork ---
        self.tab_safework = QTabWidget()
        self.panel_pdl = ScaricoPDLPanel()
        self.panel_pdl_search = RicercaPDLPanel()
        self.tab_safework.addTab(
            self.panel_pdl, QIcon(get_asset_path(Icons.SHIELD)), "Scarico PDL"
        )
        self.tab_safework.addTab(
            self.panel_pdl_search, QIcon(get_asset_path(Icons.SEARCH)), "Ricerca PDL"
        )

        # Aggiunta tab principali
        self.addTab(self.tab_fornitori, "Portale Fornitori")
        self.addTab(self.tab_safework, "SafeWork")

        # Registra riferimenti nella Main Window (per compatibilità)
        self.mw.dettagli_panel = self.panel_dettagli
        self.mw.prenota_panel = self.panel_prenota
        self.mw.scarico_panel = self.panel_scarico
        self.mw.timbrature_bot_panel = self.panel_timbrature
        self.mw.carico_panel = self.panel_carico
        self.mw.pdl_panel = self.panel_pdl
        self.mw.pdl_search_panel = self.panel_pdl_search
        self.mw.tab_fornitori = self.tab_fornitori
        self.mw.tab_safework = self.tab_safework

        # Registrazione Controller (se presente)
        if hasattr(self.mw, "bot_controller"):
            self.mw.bot_controller.register_panels(
                [
                    self.panel_dettagli,
                    self.panel_prenota,
                    self.panel_scarico,
                    self.panel_timbrature,
                    self.panel_carico,
                    self.panel_pdl,
                    self.panel_pdl_search,
                ]
            )
