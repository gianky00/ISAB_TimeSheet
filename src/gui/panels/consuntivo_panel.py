"""
SyncroJob - Consuntivo Panel (Refactored)
Pannello premium per la generazione e manipolazione dei consuntivi automatizzati.
Struttura modulare che integra i widget specializzati per Nuovo, Esistente e Impostazioni.
"""

from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from src.core import config_manager
from src.gui.components.animated_tab_widget import AnimatedTabWidget
from src.gui.widgets.contabilita.consuntivo.crea_nuovo_tab import CreaNuovoTab
from src.gui.widgets.contabilita.consuntivo.modifica_esistente_tab import ModificaEsistenteTab
from src.gui.widgets.contabilita.consuntivo.impostazioni_tab import ImpostazioniTab

class ConsuntivoPanel(QWidget):
    """Pannello Root che organizza la suite Premium dei Consuntivi."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # AnimatedTabWidget — stile premium con indicatore glow
        self.tabs = AnimatedTabWidget()
        self.tabs.currentChanged.connect(self._on_tab_changed)

        self._tab_new = CreaNuovoTab()
        self._tab_modify = ModificaEsistenteTab()
        self._tab_settings = ImpostazioniTab()

        self.tabs.addTab(self._tab_new, "Crea Nuovo")
        self.tabs.addTab(self._tab_modify, "Modifica Esistente")
        self.tabs.addTab(self._tab_settings, "Impostazioni")
        
        layout.addWidget(self.tabs)

    def _on_tab_changed(self, index: int) -> None:
        """Gestisce il caricamento dinamico dei dati al cambio scheda."""
        widget = self.tabs.widget(index)
        
        if isinstance(widget, CreaNuovoTab):
            # Forza l'aggiornamento del percorso e ricarica i dati dinamici (TCL, Stati)
            widget._update_dynamic_path()
            
            # Ricarica le combo box dalla configurazione aggiornata
            config = config_manager.load_config()
            
            widget.tcl_combo.blockSignals(True)
            widget.tcl_combo.clear()
            widget.tcl_combo.addItems(config.get("preventivi_tcl", []))
            widget.tcl_combo.blockSignals(False)
            
            widget.stato_combo.blockSignals(True)
            widget.stato_combo.clear()
            widget.stato_combo.addItems(config.get("preventivi_stati", []))
            widget.stato_combo.blockSignals(False)
            
        elif isinstance(widget, ModificaEsistenteTab):
            # Riesegue la scansione della directory per trovare nuovi file
            widget._scan_directory()
