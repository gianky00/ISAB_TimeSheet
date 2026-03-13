"""
SyncroJob - Automazioni Widget (Refactored)
Pannello raggruppato per i Bot con animazioni integrate e controlli locali.
Gestisce l'orchestrazione dei bot Selenium per Portale Fornitori e SafeWork.
"""

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.components.animated_tab_widget import AnimatedTabWidget
from src.gui.styles import COLORS
from src.utils.helpers import get_asset_path, get_colored_icon


class AutomazioniWidget(QWidget):
    """
    Pannello raggruppato per i Bot con animazioni Snapshot-Fade.
    Centralizza l'accesso a tutti i processi di automazione web.
    """

    def __init__(self, main_window) -> None:
        """
        Inizializza il widget delle automazioni.

        Args:
            main_window: Riferimento alla finestra principale per la registrazione dei pannelli.
        """
        super().__init__()
        self.mw = main_window
        self._panels_initialized = False

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Tab principale (Fornitori | SafeWork)
        self.main_tabs = AnimatedTabWidget()
        main_layout.addWidget(self.main_tabs)

        # Creiamo i contenitori dei tab (vuoti)
        self.tab_fornitori = AnimatedTabWidget()
        self.tab_fornitori.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_safework = AnimatedTabWidget()
        self.tab_safework.setTabPosition(QTabWidget.TabPosition.North)

        # Aggiunta tab principali
        self.main_tabs.addTab(self.tab_fornitori, "Portale Fornitori")
        self.main_tabs.addTab(self.tab_safework, "SafeWork")

        # Registriamo i tab nella mw per compatibilità immediata (ma saranno popolati dopo)
        self.mw.tab_fornitori = self.tab_fornitori
        self.mw.tab_safework = self.tab_safework

        # Inizializzazione posticipata e granulare dei pannelli interni
        self._init_queue = []
        QTimer.singleShot(100, self._start_granular_init)

    def _start_granular_init(self) -> None:
        """Prepara la coda di inizializzazione per i pannelli bot."""
        from src.gui.panels.carico_ts import CaricoTSPanel
        from src.gui.panels.dettagli_oda import DettagliOdAPanel
        from src.gui.panels.prenota_bp import PrenotaBPPanel
        from src.gui.panels.ricerca_pdl import RicercaPDLPanel
        from src.gui.panels.scarico_pdl import ScaricoPDLPanel
        from src.gui.panels.scarico_ts import ScaricaTSPanel
        from src.gui.panels.timbrature_bot import TimbratureBotPanel

        # Definiamo i task: (classe, icona, label, tab_parent, attr_name)
        self._init_queue = [
            (DettagliOdAPanel, Icons.LIST, "Dettagli OdA (bot)", self.tab_fornitori, "panel_dettagli"),
            (ScaricaTSPanel, Icons.DOWNLOAD, "Scarico TS (bot)", self.tab_fornitori, "panel_scarico"),
            (TimbratureBotPanel, Icons.CLOCK, "Timbrature (bot)", self.tab_fornitori, "panel_timbrature"),
            (PrenotaBPPanel, Icons.TICKET, "Prenota BP (bot)", self.tab_fornitori, "panel_prenota"),
            (CaricoTSPanel, Icons.UPLOAD, "Carico TS (bot)", self.tab_fornitori, "panel_carico"),
            (ScaricoPDLPanel, Icons.SHIELD, "Scarico PDL (bot)", self.tab_safework, "panel_pdl"),
            (RicercaPDLPanel, Icons.SEARCH, "Ricerca PDL (bot)", self.tab_safework, "panel_pdl_search"),
        ]
        self._process_init_queue()

    def _process_init_queue(self) -> None:
        """Crea un singolo pannello bot e programma il prossimo, mantenendo la UI fluida."""
        if not self._init_queue:
            self._finalize_init()
            return

        cls, icon, label, tab_parent, attr_name = self._init_queue.pop(0)
        
        try:
            panel = cls()
            setattr(self, attr_name, panel)
            tab_parent.addTab(
                panel,
                get_colored_icon(get_asset_path(icon), COLORS["text_muted"]),
                label,
            )
            # Collega alla mw per compatibilità
            setattr(self.mw, attr_name, panel)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Errore inizializzazione bot {label}: {e}")

        # Cede il controllo e passa al prossimo al prossimo giro dell'event loop
        QTimer.singleShot(0, self._process_init_queue)

    def _finalize_init(self) -> None:
        """Registra i controller una volta che tutti i pannelli sono pronti."""
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
        self._panels_initialized = True


    def set_active_tab(self, main_idx: int, sub_idx: int) -> None:
        """
        Imposta programmaticamente il tab e il sottomenu attivi.

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
        """
        Cambia il portale attivo.

        Args:
            index: Nuovo indice.
        """
        self.main_tabs.setCurrentIndex(index)

    def get_bot_panel(self, main_idx: int, sub_idx: int) -> QWidget | None:
        """
        Restituisce l'istanza del pannello bot all'indice specificato.

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
