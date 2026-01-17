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
from src.utils.helpers import get_asset_path, get_colored_icon


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
            self.panel_dettagli,
            get_colored_icon(get_asset_path(Icons.LIST), "#000000"),
            "Dettagli OdA",
        )
        self.tab_fornitori.addTab(
            self.panel_scarico,
            get_colored_icon(get_asset_path(Icons.DOWNLOAD), "#000000"),
            "Scarico TS",
        )
        self.tab_fornitori.addTab(
            self.panel_timbrature,
            get_colored_icon(get_asset_path(Icons.CLOCK), "#000000"),
            "Timbrature",
        )
        self.tab_fornitori.addTab(
            self.panel_prenota,
            get_colored_icon(get_asset_path(Icons.TICKET), "#000000"),
            "Prenota BP",
        )
        self.tab_fornitori.addTab(
            self.panel_carico,
            get_colored_icon(get_asset_path(Icons.UPLOAD), "#000000"),
            "Carico TS",
        )

        # --- TAB 2: SafeWork ---
        self.tab_safework = QTabWidget()
        self.panel_pdl = ScaricoPDLPanel()
        self.panel_pdl_search = RicercaPDLPanel()
        self.tab_safework.addTab(
            self.panel_pdl,
            get_colored_icon(get_asset_path(Icons.SHIELD), "#000000"),
            "Scarico PDL",
        )
        self.tab_safework.addTab(
            self.panel_pdl_search,
            get_colored_icon(get_asset_path(Icons.SEARCH), "#000000"),
            "Ricerca PDL",
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
