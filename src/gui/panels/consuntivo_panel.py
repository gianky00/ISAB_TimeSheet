"""
SyncroJob - Consuntivo Panel (Refactored)
Pannello premium per la generazione e manipolazione dei consuntivi automatizzati.
Struttura modulare che integra i widget specializzati per Nuovo, Esistente e Impostazioni.
"""

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from src.core.contabilita.consuntivo.consuntivo_controller import ConsuntivoController
from src.gui.components.animated_tab_widget import AnimatedTabWidget
from src.gui.widgets.contabilita.consuntivo.crea_nuovo_tab import CreaNuovoTab
from src.gui.widgets.contabilita.consuntivo.impostazioni_tab import ImpostazioniTab
from src.gui.widgets.contabilita.consuntivo.modifica_esistente_tab import ModificaEsistenteTab


class ConsuntivoPanel(QWidget):
    """Pannello Root che organizza la suite Premium dei Consuntivi."""

    def __init__(self, controller: ConsuntivoController, parent: QWidget | None = None) -> None:
        """
        Inizializza il pannello consuntivo con iniezione del controller.

        Args:
            controller: Istanza del controller per la logica di business.
            parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self.controller = controller
        self._data_preloaded = False
        self._setup_ui()
        # Avvia il caricamento dei dati immediatamente all'istanza (Eager Loading)
        QTimer.singleShot(100, self._pre_load_data)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # AnimatedTabWidget — stile premium con indicatore glow
        self.tabs = AnimatedTabWidget()
        self.tabs.currentChanged.connect(self._on_tab_changed)

        self._tab_new = CreaNuovoTab(controller=self.controller)
        self._tab_modify = ModificaEsistenteTab()  # TODO: Aggiungere iniezione se serve
        self._tab_settings = ImpostazioniTab()

        self.tabs.addTab(self._tab_new, "Crea Nuovo")
        self.tabs.addTab(self._tab_modify, "Modifica Esistente")
        self.tabs.addTab(self._tab_settings, "Impostazioni")

        layout.addWidget(self.tabs)

    def set_current_tab(self, index: int | None = None) -> None:
        """Cambia il tab visualizzato in base all'indice."""
        if index is not None and 0 <= index < self.tabs.count():
            self.tabs.setCurrentIndex(index)

    def _pre_load_data(self) -> None:
        """Esegue il caricamento pesante dei dati in background all'avvio dell'app."""
        if self._data_preloaded:
            return

        # Carica opzioni tramite controller (CORE)
        opts = self.controller.get_config_options()

        self._tab_new.tcl_combo.blockSignals(True)
        self._tab_new.tcl_combo.clear()
        self._tab_new.tcl_combo.addItems(opts["tcl"])
        self._tab_new.tcl_combo.blockSignals(False)

        self._tab_new.stato_combo.blockSignals(True)
        self._tab_new.stato_combo.clear()
        self._tab_new.stato_combo.addItems(opts["stati"])
        self._tab_new.stato_combo.blockSignals(False)

        self._tab_new.tipo_prev_combo.blockSignals(True)
        self._tab_new.tipo_prev_combo.clear()
        self._tab_new.tipo_prev_combo.addItems(opts["tipologie"])
        self._tab_new.tipo_prev_combo.blockSignals(False)

        self._tab_new.tipo_econ_combo.blockSignals(True)
        self._tab_new.tipo_econ_combo.clear()
        self._tab_new.tipo_econ_combo.addItems(opts["economie"])
        self._tab_new.tipo_econ_combo.blockSignals(False)

        # Carica directory per il tab Modifica Esistente
        self._tab_modify._scan_directory()
        self._data_preloaded = True

    def _on_tab_changed(self, index: int) -> None:
        """Gestisce il refresh leggero dell'interfaccia al cambio scheda.
        I tab ora gestiscono autonomamente il caching pesante."""
        widget = self.tabs.widget(index)

        if isinstance(widget, CreaNuovoTab):
            # Aggiorna solo i percorsi, il progressivo usa la cache interna
            widget._update_dynamic_path()
        elif isinstance(widget, ModificaEsistenteTab):
            # Tenta una scansione silente (usata solo se la cache è scaduta)
            widget._scan_directory()
