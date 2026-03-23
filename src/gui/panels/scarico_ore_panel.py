"""
SyncroJob - Scarico Ore Panel
Interfaccia ad alte prestazioni per la consultazione e la gestione dello Scarico Ore Cantiere.
Refactored V9.5: Modular architecture with Controller and specialized Widgets.
"""

from contextlib import suppress

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.constants import Icons
from src.core.contabilita.scarico_ore.controller import ScaricoOreController
from src.core.contabilita_manager import ContabilitaManager
from src.gui.components.animated_tab_widget import AnimatedTabWidget
from src.gui.components.scarico_ore import ScaricoOreTableModel
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.scarico_ore.widgets.filter_bar import ScaricoOreFilterBar
from src.gui.panels.scarico_ore.widgets.table_view import ScaricoOreTableView
from src.gui.styles import COLORS
from src.gui.widgets import ShimmerSkeleton
from src.utils.helpers import get_asset_path, get_colored_icon


class ScaricoOrePanel(QWidget):
    """
    Orchestratore dello Scarico Ore coordinato dal ScaricoOreController.
    Gestisce il caricamento asincrono, il filtraggio avanzato e la visualizzazione delle ore.
    """

    def __init__(self, controller: ScaricoOreController, parent: QWidget | None = None) -> None:
        """
        Inizializza il pannello dello scarico ore con iniezione del controller.

        Args:
            controller: Istanza del controller per la logica di business.
            parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self.controller = controller
        self._current_col_filters: dict[int, set[str]] = {}
        self._last_update_status: str | None = None

        self._setup_ui()

        # Connessioni Controller
        self.controller.status_changed.connect(self.filters.status_label.setText)
        self.controller.update_finished.connect(self._on_update_finished)

        # Inizializzazione dati differita
        self.filters.search_input.setPlaceholderText("Inizializzazione dati... attendere")
        self.filters.search_input.setEnabled(False)
        QTimer.singleShot(50, self._load_data)

    def _setup_ui(self) -> None:
        """Configura il layout, la toolbar dei filtri e la tabella dati con effetto shimmer."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # 1. Filter & Stats Bar
        self.filters = ScaricoOreFilterBar()
        self.filters.search_requested.connect(self._perform_search)
        self.filters.update_requested.connect(self._start_update)
        layout.addWidget(self.filters)

        # 2. Tabs & Table
        self.tabs = AnimatedTabWidget()
        self.scarico_tab = QWidget()
        scarico_layout = QVBoxLayout(self.scarico_tab)

        self.table_view = ScaricoOreTableView()
        self.source_model = ScaricoOreTableModel([])
        self.source_model.cache_loaded.connect(self._on_cache_loaded)
        self.source_model.loading_progress.connect(self._on_loading_progress)
        self.table_view.set_source_model(self.source_model)

        self.table_view.selection_totals_changed.connect(self._update_selection_totals)
        self.table_view.filter_changed.connect(self._on_header_filter_changed)

        scarico_layout.addWidget(self.table_view)

        # Shimmer Loading
        self.shimmer = ShimmerSkeleton(rows=10)
        self.shimmer.setParent(self.table_view)
        self.shimmer.hide()

        self.tabs.addTab(
            self.scarico_tab,
            get_colored_icon(get_asset_path(Icons.DOWNLOAD), COLORS["text_muted"]),
            "Dati Scaricati",
        )
        layout.addWidget(self.tabs)

    def _perform_search(self, text: str) -> None:
        """
        Applica i filtri testuali e per colonna al modello dati.

        Args:
            text: Testo di ricerca globale.
        """
        self.source_model.set_filter(text, self._current_col_filters)
        self._update_totals()

    def _start_update(self) -> None:
        """Avvia la procedura di sincronizzazione/importazione dei dati via controller."""
        path = config_manager.load_config().get("dataease_path", "")
        if not path:
            ConfirmationDialog.show_warning(
                self,
                "Configurazione Mancante",
                "Configura il percorso 'File Scarico Ore' nelle Impostazioni.",
            )
            return

        self.filters.status_label.setText("Calcolo stima tempi...")
        self.filters.update_btn.setEnabled(False)
        self.table_view.setEnabled(False)
        self.controller.start_import(path)

    def _on_update_finished(self, success: bool, status_msg: str) -> None:
        """
        Gestisce la finalizzazione del processo di aggiornamento.

        Args:
            success: True se l'operazione è andata a buon fine.
            status_msg: Messaggio di stato restituito dal bot.
        """
        self.filters.update_btn.setEnabled(True)
        self.table_view.setEnabled(True)

        if success:
            # Colorazione HTML per lo stato (Success)
            formatted_msg = f"<font color='{COLORS['success_dark']}'>{status_msg}</font>"
            self.filters.status_label.setText(formatted_msg)
            self._last_update_status = formatted_msg

            # Invalida cache
            with suppress(Exception):
                if ScaricoOreTableModel.CACHE_PATH.exists():
                    ScaricoOreTableModel.CACHE_PATH.unlink()
            ScaricoOreTableModel._global_cache["loaded"] = False
            self._load_data()
        else:
            self.filters.status_label.setText("Errore")
            ConfirmationDialog.show_error(self, "Errore Aggiornamento", status_msg)

    def _load_data(self) -> None:
        """Avvia il caricamento asincrono dei dati dal database o dalla cache locale."""
        if not ContabilitaManager.DB_PATH.exists():
            self.filters.status_label.setText("Database non trovato.")
            return

        self._set_ui_loading(True)
        if ScaricoOreTableModel.CACHE_PATH.exists():
            self.source_model.load_data_async(None)
        else:
            try:
                self.source_model.load_data_async(ContabilitaManager.get_scarico_ore_data())
            except Exception as e:
                self.filters.status_label.setText(f"Errore: {e}")
                self._set_ui_loading(False)

    def _on_cache_loaded(self) -> None:
        """Esegue le operazioni finali di UI una volta che i dati sono pronti in memoria."""
        self.filters.status_label.setText(self._last_update_status or "Pronto")
        self._set_ui_loading(False)
        self.table_view.resize_columns()
        self.table_view.sortByColumn(0, Qt.SortOrder.DescendingOrder)
        self._update_totals()

    def _update_totals(self) -> None:
        """Ricalcola e aggiorna le statistiche globali (righe totali e ore)."""
        row_count = self.source_model.rowCount()
        total_hours = self.source_model.get_float_total_for_visible() if row_count > 0 else 0.0

        self.filters.set_stats(
            visible_rows=row_count,
            selection_total=self.filters.lbl_selection.text(),
            total_hours=f"Totale Ore: {self.controller.format_number(total_hours)}",
        )

    def _update_selection_totals(self, total: float) -> None:
        """
        Aggiorna l'indicatore delle ore totali per le righe selezionate.

        Args:
            total: Somma delle ore selezionate.
        """
        self.filters.lbl_selection.setText(f"Totale selezionato: {self.controller.format_number(total)}")

    def _on_header_filter_changed(self, col: int, values: list[str]) -> None:
        """
        Gestisce l'attivazione di filtri specifici per singola colonna.

        Args:
            col: Indice della colonna interessata.
            values: Elenco di valori da filtrare.
        """
        if not values:
            self._current_col_filters.pop(col, None)
        else:
            self._current_col_filters[col] = {v.lower() for v in values}
        self._perform_search(self.filters.search_input.text())

    def _set_ui_loading(self, loading: bool) -> None:
        """
        Mostra o nasconde l'interfaccia di caricamento (shimmer).

        Args:
            loading: True per mostrare l'effetto shimmer, False per la tabella.
        """
        self.filters.search_input.setEnabled(not loading)
        self.filters.update_btn.setEnabled(not loading)
        self.filters.search_input.setPlaceholderText(
            "Caricamento..." if loading else "Filtra dati (Premi Invio)..."
        )

        if loading:
            self.table_view.hide()
            self.shimmer.show()
            self.shimmer.resize(self.table_view.size())
        else:
            self.shimmer.hide()
            self.table_view.show()

        self.table_view.setDisabled(loading)

    def _on_loading_progress(self, msg: str) -> None:
        """Aggiorna la label di stato durante le fasi del caricamento asincrono."""
        self.filters.status_label.setText(msg)

    def resizeEvent(self, event: QResizeEvent | None) -> None:
        """
        Aggiorna le dimensioni degli overlay (shimmer) al ridimensionamento del pannello.

        Args:
            event: Evento di ridimensionamento Qt.
        """
        super().resizeEvent(event)
        if hasattr(self, "shimmer") and self.shimmer.isVisible():
            self.shimmer.resize(self.table_view.size())

    def set_search_query(self, text: str) -> None:
        """
        API pubblica per impostare una ricerca dall'esterno (es. NavigationController).

        Args:
            text: Testo da cercare.
        """
        self.filters.search_input.setText(text)
        self.filters.search_input.setFocus()
        self.filters.search_input.selectAll()
        self._perform_search(text)
