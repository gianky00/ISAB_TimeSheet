from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QPushButton,
    QSplitter,
    QTableView,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.bots.portale_fornitori.timbrature.storage import TimbratureStorage
from src.core import config_manager
from src.core.audit_manager import AuditManager
from src.core.constants import Icons
from src.gui.formatters import FastTableModel, format_date_it
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path, get_colored_icon

from .components.detail_view import TimbratureDetailView
from .components.settings_tab import TimbratureSettingsTab


class TimbratureDBPanel(QWidget):
    """
    Pannello per la visualizzazione del Database Timbrature Isab con architettura Master-Detail.
    Refactored: usa componenti modulari.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_path = config_manager.CONFIG_DIR / "data" / "timbrature_Isab.db"
        self.storage = TimbratureStorage(self.db_path)

        # Local cache for filters
        self.lists = self.storage.get_lists()
        self.reparti = self.lists.get("reparti", [])
        self.cantieri = self.lists.get("cantieri", [])

        self._setup_ui()
        QTimer.singleShot(50, self.refresh_data)

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setProperty("class", "Level2Tabs")

        # Toolbar
        self._setup_toolbar()

        # Tab 1: Database
        self.tab_database = QWidget()
        self._setup_database_tab(self.tab_database)
        self.tabs.addTab(
            self.tab_database,
            get_colored_icon(get_asset_path(Icons.DATABASE), "#546E7A"),
            "Database",
        )

        # Tab 2: Settings
        self.settings_tab = TimbratureSettingsTab(self.storage)
        self.tabs.addTab(
            self.settings_tab,
            get_colored_icon(get_asset_path(Icons.SETTINGS_DARK), "#546E7A"),
            "Impostazioni",
        )

        self.tabs.currentChanged.connect(self._on_tab_changed)
        self.main_layout.addWidget(self.tabs)

        # Signals from Settings Tab
        self.settings_tab.settings_changed.connect(self._on_settings_changed)

    def _setup_toolbar(self):
        self.toolbar_container = QWidget()
        toolbar_layout = QHBoxLayout(self.toolbar_container)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setFixedWidth(200)
        self.search_input.textChanged.connect(lambda: self.refresh_data())

        self.reparto_filter = QComboBox()
        self.reparto_filter.setMinimumWidth(130)
        self.reparto_filter.currentIndexChanged.connect(lambda: self.refresh_data())

        self.cantiere_filter = QComboBox()
        self.cantiere_filter.setMinimumWidth(130)
        self.cantiere_filter.currentIndexChanged.connect(lambda: self.refresh_data())

        self._update_filter_combos()

        import_btn = QPushButton("Importa")
        import_btn.setIcon(get_colored_icon(get_asset_path(Icons.PLUS), "#FFFFFF"))
        import_btn.setFixedSize(90, 32)
        import_btn.clicked.connect(self._import_excel_manually)

        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(self.reparto_filter)
        toolbar_layout.addWidget(self.cantiere_filter)
        toolbar_layout.addWidget(import_btn)

        self.tabs.setCornerWidget(self.toolbar_container, Qt.Corner.TopRightCorner)

    def _setup_database_tab(self, parent):
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
        self.db_table.verticalHeader().setVisible(False)
        self.db_table.setAlternatingRowColors(True)
        self.db_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.db_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.db_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.db_table.setSortingEnabled(True)

        header = self.db_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)

        # Connessione protetta del selectionModel
        if self.db_table.selectionModel():
            self.db_table.selectionModel().selectionChanged.connect(
                self._on_selection_changed
            )

        splitter.addWidget(self.db_table)

        # Detail View
        self.detail_view = TimbratureDetailView()
        splitter.addWidget(self.detail_view)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)
        layout.addWidget(splitter)

    def _update_filter_combos(self):
        # Cache reload
        self.lists = self.storage.get_lists()
        self.reparti = self.lists.get("reparti", [])
        self.cantieri = self.lists.get("cantieri", [])

        self.reparto_filter.blockSignals(True)
        self.reparto_filter.clear()
        self.reparto_filter.addItem("Tutti i reparti", "Tutti")
        for rep in self.reparti:
            self.reparto_filter.addItem(rep, rep)
        self.reparto_filter.blockSignals(False)

        self.cantiere_filter.blockSignals(True)
        self.cantiere_filter.clear()
        self.cantiere_filter.addItem("Tutti i cantieri", "Tutti")
        for cant in self.cantieri:
            self.cantiere_filter.addItem(cant, cant)
        self.cantiere_filter.blockSignals(False)

    def refresh_data(self):
        """Carica i dati dal DB e aggiorna il modello virtuale."""
        text = self.search_input.text()
        reparto = self.reparto_filter.currentData()
        cantiere = self.cantiere_filter.currentData()

        # Get rows
        rows = self.storage.get_timbrature_with_reparto(
            limit=2000,
            filter_text=text,
            filter_reparto=reparto,
            filter_cantiere=cantiere,
        )

        # Prepare for FastTableModel
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
        # Resize con protezione
        QTimer.singleShot(
            0,
            lambda: self.db_table.resizeColumnsToContents() if self.db_table else None,
        )
        # Reset detail
        self.detail_view.clear_fields()

    def _on_selection_changed(self, selected, _deselected):
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

    def _on_tab_changed(self, index):
        if index == 0:  # Database
            if hasattr(self, "toolbar_container"):
                self.toolbar_container.show()
            self.refresh_data()
        else:  # Settings
            if hasattr(self, "toolbar_container"):
                self.toolbar_container.hide()
            self.settings_tab.load_data()

    def _on_settings_changed(self):
        # Settings updated (data storage updated), we might need to refresh options
        self._update_filter_combos()

    def _import_excel_manually(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleziona File Excel Timbrature",
            str(Path.home() / "Downloads"),
            "Excel Files (*.xlsx *.xls)",
        )
        if not file_path:
            return

        try:
            success = self.storage.import_excel(file_path, lambda msg: print(msg))
            if success:
                AuditManager.instance().log_action(
                    "Importazione Manuale",
                    "database",
                    params={"file": Path(file_path).name},
                )
                self.refresh_data()
                ToastManager.instance().show("Dati importati correttamente.", "success")
                self.settings_tab.load_data()
            else:
                ToastManager.instance().show("Impossibile importare il file.", "error")
        except Exception as e:
            ToastManager.instance().show(f"Errore importazione: {e}", "error")

    # Exposed for external calls (compatibility)
    def refresh_fornitori(self):
        self._update_filter_combos()
