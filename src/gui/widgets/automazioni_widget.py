from PyQt6.QtWidgets import QTabWidget

from src.gui.panels import (
    CaricoTSPanel,
    DettagliOdAPanel,
    PrenotaBPPanel,
    ScaricaTSPanel,
    ScaricoPDLPanel,
    TimbratureBotPanel,
)


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
        self.tab_fornitori.addTab(self.panel_dettagli, "📋 Dettagli OdA")
        self.tab_fornitori.addTab(self.panel_scarico, "📥 Scarico TS")
        self.tab_fornitori.addTab(self.panel_timbrature, "⏱️ Timbrature")
        self.tab_fornitori.addTab(self.panel_prenota, "🎫 Prenota BP")
        self.tab_fornitori.addTab(self.panel_carico, "📤 Carico TS")

        # --- TAB 2: SafeWork ---
        self.tab_safework = QTabWidget()
        self.panel_pdl = ScaricoPDLPanel()
        self.tab_safework.addTab(self.panel_pdl, "🛡️ Scarico PDL")

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
                ]
            )
