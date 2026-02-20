from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTabWidget, QWidget, QHBoxLayout, QStackedWidget

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
from src.gui.panels.base import BaseBotPanel
from src.utils.helpers import get_asset_path, get_colored_icon


class AutomazioniWidget(QTabWidget):
    """Pannello raggruppato per i Bot con caricamento EAGER (tutto subito)."""

    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window
        # Nascondiamo la barra dei tab superiore perché la navigazione è ora nella Sidebar
        if tab_bar := self.tabBar():
            tab_bar.hide()
        self.setDocumentMode(True)  # Rimuove i bordi extra del frame
        self.setStyleSheet("QTabWidget::pane { border: none; }")  # Pulizia visuale totale

        # --- TAB 1: Portale Fornitori ---
        self.tab_fornitori = QTabWidget()
        self.tab_fornitori.setProperty("class", "Level2Tabs")  # Clean Style
        self.corner_fornitori = QStackedWidget()
        self.tab_fornitori.setCornerWidget(self.corner_fornitori, Qt.Corner.TopRightCorner)
        self.tab_fornitori.currentChanged.connect(self.corner_fornitori.setCurrentIndex)

        # Istanzia TUTTI i pannelli subito
        self.panel_dettagli = DettagliOdAPanel()
        self.panel_scarico = ScaricaTSPanel()
        self.panel_timbrature = TimbratureBotPanel()
        self.panel_prenota = PrenotaBPPanel()
        self.panel_carico = CaricoTSPanel()

        self._add_bot_tab(self.tab_fornitori, self.corner_fornitori, self.panel_dettagli, Icons.LIST, "Dettagli OdA (bot)")
        self._add_bot_tab(self.tab_fornitori, self.corner_fornitori, self.panel_scarico, Icons.DOWNLOAD, "Scarico TS (bot)")
        self._add_bot_tab(self.tab_fornitori, self.corner_fornitori, self.panel_timbrature, Icons.CLOCK, "Timbrature (bot)")
        self._add_bot_tab(self.tab_fornitori, self.corner_fornitori, self.panel_prenota, Icons.TICKET, "Prenota BP (bot)")
        self._add_bot_tab(self.tab_fornitori, self.corner_fornitori, self.panel_carico, Icons.UPLOAD, "Carico TS (bot)")

        # --- TAB 2: SafeWork ---
        self.tab_safework = QTabWidget()
        self.tab_safework.setProperty("class", "Level2Tabs")  # Clean Style
        self.corner_safework = QStackedWidget()
        self.tab_safework.setCornerWidget(self.corner_safework, Qt.Corner.TopRightCorner)
        self.tab_safework.currentChanged.connect(self.corner_safework.setCurrentIndex)

        self.panel_pdl = ScaricoPDLPanel()
        self.panel_pdl_search = RicercaPDLPanel()
        
        self._add_bot_tab(self.tab_safework, self.corner_safework, self.panel_pdl, Icons.SHIELD, "Scarico PDL (bot)")
        self._add_bot_tab(self.tab_safework, self.corner_safework, self.panel_pdl_search, Icons.SEARCH, "Ricerca PDL (bot)")

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

    def _add_bot_tab(self, tab_widget: QTabWidget, corner_stack: QStackedWidget, panel: BaseBotPanel, icon_path: str, title: str):
        """Helper per aggiungere un tab e spostare i suoi controlli nel corner widget."""
        tab_widget.addTab(panel, get_colored_icon(get_asset_path(icon_path), "#546E7A"), title)
        
        # Estraiamo i controlli dal pannello e li mettiamo nello stack del corner
        if hasattr(panel, "controls_widget") and hasattr(panel, "header_layout"):
            # Rimuoviamo dal pannello originale
            panel.header_layout.removeWidget(panel.controls_widget)
            # Nascondiamo l'intero header layout per recuperare spazio
            panel.controls_widget.setParent(None)
            # Aggiungiamo allo stack del corner (il parent diventerà corner_stack)
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 10, 0) # Padding a destra per non toccare il bordo
            layout.addWidget(panel.controls_widget)
            corner_stack.addWidget(container)
            
            # Se il pannello è BaseBotPanel, possiamo anche nascondere l'header_layout del tutto
            # ma lo lasciamo vuoto per ora o lo rimuoviamo dal layout del pannello
            item = panel.main_layout.takeAt(0) # L'header_layout è il primo elemento
            if item:
                if item.layout():
                    # Svuota e distruggi il layout
                    while item.layout().count():
                        w = item.layout().takeAt(0).widget()
                        if w: w.deleteLater()
                # Se è un layout, non ha deleteLater direttamente come widget
                # Ma rimuovendolo dal main_layout abbiamo già guadagnato spazio

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
