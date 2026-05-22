"""SyncroJob - Automazioni Widget (Refactored).

Pannello raggruppato per i Bot con animazioni integrate e controlli locali.
Gestisce l'orchestrazione dei bot Selenium per Portale Fornitori e SafeWork.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.components.animated_tab_widget import AnimatedTabWidget
from src.gui.panels import (
    CaricoTSPanel,
    DettagliOdAPanel,
    PrenotaBPPanel,
    RicercaPDLPanel,
    ScaricaTSPanel,
    ScaricoPDLPanel,
    TimbratureBotPanel,
)
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon

if TYPE_CHECKING:
    from src.gui.main_window.main import MainWindow


class AutomazioniWidget(QWidget):
    """Pannello raggruppato per i Bot con animazioni Snapshot-Fade.

    Centralizza l'accesso a tutti i processi di automazione web.
    """

    def __init__(self, main_window: MainWindow) -> None:
        """Inizializza il widget delle automazioni.

        Args:
          main_window: Riferimento alla finestra principale per la registrazione dei pannelli.
        """
        super().__init__()
        self.mw = main_window

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Tab principale (Fornitori | SafeWork)
        self.main_tabs = AnimatedTabWidget()
        main_layout.addWidget(self.main_tabs)

        # --- TAB 1: Portale Fornitori ---
        self.tab_fornitori = AnimatedTabWidget()
        self.tab_fornitori.setTabPosition(QTabWidget.TabPosition.North)

        # Istanzia i pannelli (I pulsanti ora rimangono DENTRO i pannelli)
        self.panel_dettagli = DettagliOdAPanel()
        self.panel_scarico = ScaricaTSPanel()
        self.panel_timbrature = TimbratureBotPanel()
        self.panel_prenota = PrenotaBPPanel()
        self.panel_carico = CaricoTSPanel()

        self.tab_fornitori.addTab(
            self.panel_dettagli,
            get_colored_icon(get_asset_path(Icons.LIST), COLORS["text_muted"]),
            "Dettagli OdA (bot)",
        )
        self.tab_fornitori.addTab(
            self.panel_scarico,
            get_colored_icon(get_asset_path(Icons.DOWNLOAD), COLORS["text_muted"]),
            "Scarico TS (bot)",
        )
        self.tab_fornitori.addTab(
            self.panel_timbrature,
            get_colored_icon(get_asset_path(Icons.CLOCK), COLORS["text_muted"]),
            "Timbrature (bot)",
        )
        self.tab_fornitori.addTab(
            self.panel_prenota,
            get_colored_icon(get_asset_path(Icons.TICKET), COLORS["text_muted"]),
            "Prenota BP (bot)",
        )
        self.tab_fornitori.addTab(
            self.panel_carico,
            get_colored_icon(get_asset_path(Icons.UPLOAD), COLORS["text_muted"]),
            "Carico TS (bot)",
        )

        # --- TAB 2: SafeWork ---
        self.tab_safework = AnimatedTabWidget()
        self.tab_safework.setTabPosition(QTabWidget.TabPosition.North)

        self.panel_pdl = ScaricoPDLPanel()
        self.panel_pdl_search = RicercaPDLPanel()

        self.tab_safework.addTab(
            self.panel_pdl,
            get_colored_icon(get_asset_path(Icons.SHIELD), COLORS["text_muted"]),
            "Scarico PDL (bot)",
        )
        self.tab_safework.addTab(
            self.panel_pdl_search,
            get_colored_icon(get_asset_path(Icons.SEARCH), COLORS["text_muted"]),
            "Ricerca PDL (bot)",
        )

        # Aggiunta tab principali
        self.main_tabs.addTab(self.tab_fornitori, "Portale Fornitori")
        self.main_tabs.addTab(self.tab_safework, "SafeWork")

        # Registra riferimenti nella Main Window (per compatibilit )
        self.mw.dettagli_panel = self.panel_dettagli
        self.mw.prenota_panel = self.panel_prenota
        self.mw.scarico_panel = self.panel_scarico
        self.mw.timbrature_bot_panel = self.panel_timbrature
        self.mw.carico_panel = self.panel_carico
        self.mw.pdl_panel = self.panel_pdl
        self.mw.pdl_search_panel = self.panel_pdl_search
        self.mw.tab_fornitori = self.tab_fornitori
        self.mw.tab_safework = self.tab_safework

        # Registrazione Controller
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

    def set_current_tab(self, sub_index: int | None = None, bot_index: int | None = None) -> None:
        """Metodo standard per il NavigationController per impostare i tab interni."""
        if sub_index is not None:
            self.main_tabs.setCurrentIndex(sub_index)
            if bot_index is not None and bot_index != -1:
                target = self.tab_fornitori if sub_index == 0 else self.tab_safework
                target.setCurrentIndex(bot_index)

    def set_active_tab(self, main_idx: int, sub_idx: int) -> None:
        """Imposta programmaticamente il tab e il sottomenu attivi.

        Args:
          main_idx: Indice del portale (0: Fornitori, 1: SafeWork).
          sub_idx: Indice del bot all'interno del portale.
        """
        self.main_tabs.setCurrentIndex(main_idx)
        target = self.tab_fornitori if main_idx == 0 else self.tab_safework
        target.setCurrentIndex(sub_idx)

    def currentIndex(self) -> int:
        """Restituisce l'indice del portale attivo."""
        return self.main_tabs.currentIndex()

    def setCurrentIndex(self, index: int) -> None:
        """Cambia il portale attivo.

        Args:
          index: Nuovo indice.
        """
        self.main_tabs.setCurrentIndex(index)

    def get_bot_panel(self, main_idx: int, sub_idx: int) -> QWidget | None:
        """Restituisce l'istanza del pannello bot all'indice specificato.

        Args:
          main_idx: Indice del portale (0: Fornitori, 1: SafeWork).
          sub_idx: Indice del bot nel tab secondario.

        Returns:
          Optional[QWidget]: L'istanza del pannello o None se non trovato.
        """
        target_tab = self.tab_fornitori if main_idx == 0 else self.tab_safework
        if sub_idx < target_tab.count():
            return target_tab.widget(sub_idx)
        return None
