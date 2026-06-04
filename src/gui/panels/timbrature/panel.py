"""Modulo Panel."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QSplitter,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.application.services import config_manager
from src.application.services.audit_manager import AuditManager
from src.application.services.constants import Icons
from src.application.services.utils.formatters import format_date_it
from src.gui.components.animated_tab_widget import AnimatedTabWidget
from src.gui.formatters import FastTableModel
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import (
    FilterComboBox,
    SearchInput,
)
from src.gui.widgets.toast import ToastManager
from src.gui.workers.timbrature_worker import TimbratureDataWorker
from src.infrastructure.bots.portale_fornitori.timbrature.storage import TimbratureStorage
from src.infrastructure.utils.helpers import get_asset_path, get_colored_icon

from .components.detail_view import TimbratureDetailView
from .components.settings_tab import TimbratureSettingsTab

if TYPE_CHECKING:
    from PySide6.QtCore import QItemSelection


class TimbratureDBPanel(QWidget):
    """Pannello per la visualizzazione del Database Timbrature Isab con architettura Master-Detail.

    Refactored: usa componenti modulari.

    Inizializza la classe.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        # Member declarations
        self.main_layout: QVBoxLayout
        self.tabs: AnimatedTabWidget
        self.toolbar_container: QWidget
        self.search_input: QLineEdit
        self.anno_filter: QComboBox
        self.reparto_filter: QComboBox
        self.cantiere_filter: QComboBox
        self.tab_database: QWidget
        self.model: FastTableModel
        self.db_table: QTableView
        self.detail_view: TimbratureDetailView
        self.settings_tab: TimbratureSettingsTab

        self.db_path = config_manager.CONFIG_DIR / "data" / "timbrature_Isab.db"
        self.storage = TimbratureStorage(self.db_path)

        # Local cache for filters (Inizializzato a vuoto, caricato asincronamente)
        self.reparti: list[str] = []
        self.cantieri: list[str] = []

        self._data_worker: TimbratureDataWorker | None = None
        self._filter_worker: TimbratureDataWorker | None = None
        self._import_worker: TimbratureDataWorker | None = None

        self._setup_ui()

        # Caricamento differito per massimizzare la fluidit  dello splash screen
        QTimer.singleShot(150, self._deferred_init)

    def _deferred_init(self) -> None:
        """Carica le liste e i dati iniziali dopo la creazione del widget."""
        try:
            self._update_filter_combos()
            self.refresh_data()
        except Exception as e:
            from src.application.services.logging import get_logger

            get_logger(__name__).error(f"Error in deferred init: {e}")

    def _setup_ui(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # Toolbar (Aggiunta prima dei tab per evitare il setCornerWidget)
        self._setup_toolbar()
        self.main_layout.addWidget(self.toolbar_container)

        # Tabs
        self.tabs = AnimatedTabWidget()

        # Tab 1: Database
        self.tab_database = QWidget()
        self._setup_database_tab(self.tab_database)
        self.tabs.addTab(
            self.tab_database,
            get_colored_icon(get_asset_path(Icons.DATABASE), COLORS["text_muted"]),
            "Database",
        )

        # Tab 2: Settings
        self.settings_tab = TimbratureSettingsTab(self.storage)
        self.tabs.addTab(
            self.settings_tab,
            get_colored_icon(get_asset_path(Icons.SETTINGS_DARK), COLORS["text_muted"]),
            "Impostazioni",
        )

        self.tabs.currentChanged.connect(self._on_tab_changed)
        self.main_layout.addWidget(self.tabs)

        # Signals from Settings Tab
        self.settings_tab.settings_changed.connect(self._on_settings_changed)

    def _setup_toolbar(self) -> None:
        """Configura la barra degli strumenti superiore con filtri e ricerca."""
        self.toolbar_container = QFrame()
        self.toolbar_container.setObjectName("filterBar")
        self.toolbar_container.setStyleSheet(
            f"QFrame#filterBar {{ background-color: {COLORS['bg_white']}; border: 1px solid {COLORS['border_light']}; border-radius: 12px; }}"
        )

        toolbar_layout = QHBoxLayout(self.toolbar_container)
        toolbar_layout.setContentsMargins(15, 10, 15, 10)
        toolbar_layout.setSpacing(15)

        self._setup_search_section(toolbar_layout)
        self._add_toolbar_divider(toolbar_layout)
        self._setup_filters_section(toolbar_layout)

        toolbar_layout.addStretch()
        self._setup_action_buttons(toolbar_layout)

    def _setup_search_section(self, layout: QHBoxLayout) -> None:
        """Configura la sezione di ricerca libera."""
        from src.gui.styles import LABEL_MUTED, LINEEDIT_STYLE

        search_v = QVBoxLayout()
        search_v.setSpacing(4)

        lbl_search = QLabel("CERCA PERSONALE")
        lbl_search.setStyleSheet(LABEL_MUTED)
        self.search_input = SearchInput()
        self.search_input.setPlaceholderText("Cognome, Nome...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setMinimumWidth(200)
        self.search_input.setStyleSheet(LINEEDIT_STYLE)
        self.search_input.textChanged.connect(self.refresh_data)

        search_v.addWidget(lbl_search)
        search_v.addWidget(self.search_input)
        layout.addLayout(search_v)

    def _add_toolbar_divider(self, layout: QHBoxLayout) -> None:
        """Aggiunge un divisore verticale nella toolbar."""
        v_line = QFrame()
        v_line.setFrameShape(QFrame.Shape.VLine)
        v_line.setFrameShadow(QFrame.Shadow.Plain)
        v_line.setStyleSheet(f"color: {COLORS['border_light']};")
        layout.addWidget(v_line)

    def _setup_filters_section(self, layout: QHBoxLayout) -> None:
        """Configura i selettori di anno, reparto e cantiere."""
        from src.gui.styles import COMBOBOX_STYLE, LABEL_MUTED

        filters_h = QHBoxLayout()
        filters_h.setSpacing(12)

        # Anno
        anno_v = QVBoxLayout()
        anno_v.setSpacing(4)
        lbl_anno = QLabel("ANNO")
        lbl_anno.setStyleSheet(LABEL_MUTED)
        self.anno_filter = FilterComboBox()
        self.anno_filter.setMinimumWidth(100)
        self.anno_filter.setStyleSheet(COMBOBOX_STYLE)
        self.anno_filter.currentIndexChanged.connect(self.refresh_data)
        anno_v.addWidget(lbl_anno)
        anno_v.addWidget(self.anno_filter)
        filters_h.addLayout(anno_v)

        # Reparto
        rep_v = QVBoxLayout()
        rep_v.setSpacing(4)
        lbl_rep = QLabel("REPARTO")
        lbl_rep.setStyleSheet(LABEL_MUTED)
        self.reparto_filter = FilterComboBox()
        self.reparto_filter.setMinimumWidth(150)
        self.reparto_filter.setStyleSheet(COMBOBOX_STYLE)
        self.reparto_filter.currentIndexChanged.connect(self.refresh_data)
        rep_v.addWidget(lbl_rep)
        rep_v.addWidget(self.reparto_filter)
        filters_h.addLayout(rep_v)

        # Cantiere
        cant_v = QVBoxLayout()
        cant_v.setSpacing(4)
        lbl_cant = QLabel("CANTIERE")
        lbl_cant.setStyleSheet(LABEL_MUTED)
        self.cantiere_filter = FilterComboBox()
        self.cantiere_filter.setMinimumWidth(150)
        self.cantiere_filter.setStyleSheet(COMBOBOX_STYLE)
        self.cantiere_filter.currentIndexChanged.connect(self.refresh_data)
        cant_v.addWidget(lbl_cant)
        cant_v.addWidget(self.cantiere_filter)
        filters_h.addLayout(cant_v)

        layout.addLayout(filters_h)
        self._update_filter_combos()

    def _setup_action_buttons(self, layout: QHBoxLayout) -> None:
        """Aggiunge i pulsanti di azione (es. Importa)."""
        from src.gui.widgets.modern_button import ModernButton

        import_btn = ModernButton(
            "IMPORTA EXCEL",
            variant=ModernButton.Variant.PRIMARY,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.PLUS),
        )
        import_btn.clicked.connect(self._import_excel_manually)
        layout.addWidget(import_btn, alignment=Qt.AlignmentFlag.AlignBottom)

    def _setup_database_tab(self, parent: QWidget) -> None:
        layout = QVBoxLayout(parent)
        layout.setContentsMargins(0, 5, 0, 0)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Master Table
        self.model = FastTableModel(
            [], ["Data", "Cognome", "Nome", "Ingresso", "Uscita", "Reparto", "Cantiere"]
        )
        self.model.set_column_formatter(0, format_date_it)

        self.db_table = QTableView()
        self.db_table.setModel(self.model)
        if v_header := self.db_table.verticalHeader():
            v_header.setVisible(False)
        self.db_table.setAlternatingRowColors(True)
        self.db_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.db_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.db_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.db_table.setSortingEnabled(True)

        header = self.db_table.horizontalHeader()
        if header is None:
            raise RuntimeError("Table horizontal header is None")
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)

        # Connessione protetta del selectionModel
        selection_model = self.db_table.selectionModel()
        if selection_model:
            selection_model.selectionChanged.connect(self._on_selection_changed)

        splitter.addWidget(self.db_table)

        # Detail View
        self.detail_view = TimbratureDetailView()
        splitter.addWidget(self.detail_view)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)
        layout.addWidget(splitter)

    def _update_filter_combos(self) -> None:
        """Richiede il caricamento delle liste filtri in background (Asincrono)."""
        self._filter_worker = TimbratureDataWorker(self.storage, "fetch_filters")
        self._filter_worker.filters_ready.connect(self._on_filters_ready)
        self._filter_worker.start()

    def _on_filters_ready(self, lists: dict[str, list[Any]]) -> None:
        """Popola i menu a tendina con i dati caricati dal worker."""
        self.reparti = lists.get("reparti", [])
        self.cantieri = lists.get("cantieri", [])
        years = lists.get("years", [])

        # Update Anno
        self.anno_filter.blockSignals(True)
        self.anno_filter.clear()
        self.anno_filter.addItem("Tutti gli anni", "Tutti")
        for yr in years:
            self.anno_filter.addItem(str(yr), str(yr))
        self.anno_filter.blockSignals(False)

        # Update Reparto
        self.reparto_filter.blockSignals(True)
        self.reparto_filter.clear()
        self.reparto_filter.addItem("Tutti i reparti", "Tutti")
        for rep in self.reparti:
            self.reparto_filter.addItem(rep, rep)
        self.reparto_filter.blockSignals(False)

        # Update Cantiere
        self.cantiere_filter.blockSignals(True)
        self.cantiere_filter.clear()
        self.cantiere_filter.addItem("Tutti i cantieri", "Tutti")
        for cant in self.cantieri:
            self.cantiere_filter.addItem(cant, cant)
        self.cantiere_filter.blockSignals(False)

    def refresh_data(self) -> None:
        """Carica i dati dal DB in background (Asincrono)."""
        text = self.search_input.text()
        anno = self.anno_filter.currentData()
        reparto = self.reparto_filter.currentData()
        cantiere = self.cantiere_filter.currentData()

        if self._data_worker and self._data_worker.isRunning():
            self._data_worker.terminate()
            self._data_worker.wait()

        self._data_worker = TimbratureDataWorker(
            self.storage,
            "fetch_data",
            filter_text=text,
            filter_reparto=reparto,
            filter_cantiere=cantiere,
            filter_year=anno,
        )
        self._data_worker.data_ready.connect(self._on_data_ready)
        self._data_worker.start()

    def _on_data_ready(self, rows: list[tuple[Any, ...]]) -> None:
        """Aggiorna il modello virtuale con i dati caricati in background."""
        # Headers: Data(0), Cognome(4), Nome(3), Ingresso(1), Uscita(2), Reparto(16), Cantiere(17)
        master_rows = []
        for row in rows:
            iso_date = str(row[0]).split(" ")[0] if row[0] else ""
            m_row = [
                iso_date,
                row[4] or "",
                row[3] or "",
                row[1] or "",
                row[2] or "",
                row[16] or "",
                row[17] or "",
            ]
            master_rows.append(m_row)

        self.model.update_data(master_rows, new_metadata=rows)
        # Resize ottimizzato (già deferito via QTimer internamente se usassimo smart_resize,
        # ma qui manteniamo la compatibilità esistente con QTimer.singleShot)
        QTimer.singleShot(
            0,
            lambda: self.db_table.resizeColumnsToContents() if self.db_table else None,
        )
        self.detail_view.clear_fields()

    def _on_selection_changed(self, selected: QItemSelection, _deselected: QItemSelection) -> None:
        # Protezione contro selectionModel None
        selection_model = self.db_table.selectionModel()
        if not selection_model:
            return

        indexes = selection_model.selectedRows()
        if not indexes:
            return

        # Get raw full row from metadata
        try:
            row_data = indexes[0].data(Qt.ItemDataRole.UserRole)
            if row_data:
                self.detail_view.display_data(row_data)
            else:
                self.detail_view.clear_fields()
        except (IndexError, RuntimeError, AttributeError) as e:
            # Gestione errori durante l'accesso ai dati
            print(f"Errore in _on_selection_changed: {e}")
            self.detail_view.clear_fields()

    def _on_tab_changed(self, index: int) -> None:
        if index == 0:  # Database
            if hasattr(self, "toolbar_container"):
                self.toolbar_container.show()
            self.refresh_data()
        else:  # Settings
            if hasattr(self, "toolbar_container"):
                self.toolbar_container.hide()
            self.settings_tab.load_data()

    def _on_settings_changed(self) -> None:
        """Reagisce al cambio di impostazioni aggiornando i filtri di reparto e cantiere."""
        self._update_filter_combos()

    def _import_excel_manually(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona File Excel Timbrature",
            str(Path.home() / "Downloads"),
            "Excel Files (*.xlsx *.xls)",
        )
        if not file_path:
            return

        ToastManager.instance().show("Importazione in corso...", "info")

        self._import_worker = TimbratureDataWorker(self.storage, "import_excel", file_path)
        self._import_worker.import_finished.connect(self._on_import_finished)
        self._import_worker.start()

    def _on_import_finished(self, success: bool, message: str) -> None:
        """Gestisce il completamento dell'importazione asincrona."""
        if success:
            AuditManager.instance().log_action(
                "Importazione Manuale",
                "database",
                params={"status": "success"},
            )
            self.refresh_data()
            ToastManager.instance().show("Dati importati correttamente.", "success")
            self.settings_tab.load_data()
        else:
            ToastManager.instance().show(message, "error")

    # Exposed for external calls (compatibility)
    def refresh_fornitori(self) -> None:
        """Aggiorna le liste dei fornitori nei menu a tendina dei filtri."""
        self._update_filter_combos()
