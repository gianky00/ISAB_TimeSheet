from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QHeaderView,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.core.config_manager import CONFIG_DIR
from src.core.contabilita_queries import ContabilitaQueries
from src.gui.formatters import (
    FastTableModel,
    format_currency_smart,
    format_date_it,
    format_number_smart,
)


class ContabilitaYearTab(QWidget):
    """Tab per un singolo anno ottimizzato per massima reattività."""

    COLUMNS = [
        "DATA\nPREV.",
        "MESE",
        "N°\nPREV.",
        "TOTALE\nPREV.",
        "ATTIVITA'",
        "TCL",
        "ODC",
        "STATO\nATTIVITA'",
        "TIPOLOGIA",
        "ORE\nSP",
        "RESA",
        "ANNOTAZIONI",
    ]

    def __init__(self, year: int, parent=None):
        super().__init__(parent)
        self.year = year
        self.model = FastTableModel([], self.COLUMNS)

        # --- Configurazione Formattatori ---
        # Col 0: Data -> DD/MM/YYYY
        self.model.set_column_formatter(0, format_date_it)
        # Col 3: Totale Prev -> Euro Smart (1.200 o 1.200,50)
        self.model.set_column_formatter(3, format_currency_smart)
        # Col 9: ORE SP -> Smart Number
        self.model.set_column_formatter(9, format_number_smart)
        # Col 10: RESA -> Smart Number
        self.model.set_column_formatter(10, format_number_smart)

        self._setup_ui()
        # Defer data loading for better responsiveness
        QTimer.singleShot(10, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)

        # --- Configurazione Selezione (Identica a DataEase) ---
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        self.table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        # Imposta larghezze iniziali ragionevoli
        self.table.setColumnWidth(0, 90)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(4, 300)

        header.setStretchLastSection(True)

        layout.addWidget(self.table)

    def refresh_data(self):
        """Metodo pubblico per rinfrescare i dati del tab."""
        self._load_data()

    def _load_data(self):
        """Carica i dati dal DB e aggiorna il modello virtuale."""
        try:
            db_path = CONFIG_DIR / "data" / "contabilita.db"
            # Ottiene dati GREZZI (tupla di valori misti: str, float, None)
            db_data = ContabilitaQueries.get_data_by_year(db_path, self.year)

            # Passa i dati grezzi direttamente al modello.
            # Il modello userà i formatters per la visualizzazione e i valori grezzi per l'ordinamento.
            # Convertiamo solo in lista per mutabilità se necessario, ma db_data è lista di tuple
            # FastTableModel si aspetta lista di liste/tuple accessibili per indice.

            # Nota: ContabilitaQueries restituisce tutto. Dobbiamo assicurarci di prendere solo le colonne che servono
            # se la query ritorna più colonne di self.COLUMNS.
            # Slice per sicurezza
            display_rows = [row[: len(self.COLUMNS)] for row in db_data]

            self.model.update_data(display_rows)

        except Exception as e:
            print(f"Error loading data for year {self.year}: {e}")

    def set_search_query(self, query):
        """Placeholder per la ricerca (da implementare nel modello se necessario)."""
        pass
