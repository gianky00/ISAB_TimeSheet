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
        # Nascondiamo la barra dei tab superiore perché la navigazione è ora nella Sidebar
        self.tabBar().hide()
        self.setDocumentMode(True)  # Rimuove i bordi extra del frame
        self.setStyleSheet(
            "QTabWidget::pane { border: none; }"
        )  # Pulizia visuale totale

        # --- TAB 1: Portale Fornitori ---
        self.tab_fornitori = QTabWidget()
        self.tab_fornitori.setProperty("class", "Level2Tabs")  # Clean Style

        # Istanzia TUTTI i pannelli subito
        self.panel_dettagli = DettagliOdAPanel()
        self.panel_prenota = PrenotaBPPanel()
        self.panel_scarico = ScaricaTSPanel()
        self.panel_timbrature = TimbratureBotPanel()
        self.panel_carico = CaricoTSPanel()

        # Aggiungi i tab a Portale Fornitori
        self.tab_fornitori.addTab(
            self.panel_dettagli,
            get_colored_icon(get_asset_path(Icons.LIST), "#546E7A"),
            "Dettagli OdA",
        )
        self.tab_fornitori.addTab(
            self.panel_scarico,
            get_colored_icon(get_asset_path(Icons.DOWNLOAD), "#546E7A"),
            "Scarico TS",
        )
        self.tab_fornitori.addTab(
            self.panel_timbrature,
            get_colored_icon(get_asset_path(Icons.CLOCK), "#546E7A"),
            "Timbrature",
        )
        self.tab_fornitori.addTab(
            self.panel_prenota,
            get_colored_icon(get_asset_path(Icons.TICKET), "#546E7A"),
            "Prenota BP",
        )
        self.tab_fornitori.addTab(
            self.panel_carico,
            get_colored_icon(get_asset_path(Icons.UPLOAD), "#546E7A"),
            "Carico TS",
        )

        # --- TAB 2: SafeWork ---
        self.tab_safework = QTabWidget()
        self.tab_safework.setProperty("class", "Level2Tabs")  # Clean Style

        self.panel_pdl = ScaricoPDLPanel()
        self.panel_pdl_search = RicercaPDLPanel()
        self.tab_safework.addTab(
            self.panel_pdl,
            get_colored_icon(get_asset_path(Icons.SHIELD), "#546E7A"),
            "Scarico PDL",
        )
        self.tab_safework.addTab(
            self.panel_pdl_search,
            get_colored_icon(get_asset_path(Icons.SEARCH), "#546E7A"),
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

    def set_active_tab(self, main_idx: int, sub_idx: int):
        """Imposta programmaticamente il tab attivo con debug."""
        print(f"DEBUG: AutomazioniWidget.set_active_tab({main_idx}, {sub_idx})")

        # 1. Tab Principale
        self.setCurrentIndex(main_idx)

        # 2. Sotto-Tab (con delay per sicurezza UI)
        target_widget = None
        if main_idx == 0:
            target_widget = self.tab_fornitori
        elif main_idx == 1:
            target_widget = self.tab_safework

        if target_widget:
            print(
                f"DEBUG: Switching inner tab {main_idx} to {sub_idx} (Current: {target_widget.currentIndex()})"
            )
            target_widget.setCurrentIndex(sub_idx)
            # Force update
            target_widget.repaint()
