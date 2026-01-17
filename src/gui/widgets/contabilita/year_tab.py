from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.core.config_manager import CONFIG_DIR
from src.core.contabilita_queries import ContabilitaQueries
from src.gui.formatters import FastTableModel


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
        self._setup_ui()
        # Defer data loading for better responsiveness
        QTimer.singleShot(10, self._load_data)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet(
            """
            QTableView {
                background-color: white;
                border: 1px solid #dee2e6;
                alternate-background-color: #f8f9fa;
            }
            QHeaderView::section {
                background-color: #E1F5FE;
                color: #333333;
                padding: 8px;
                border: none;
                border-right: 1px solid #B3E5FC;
                border-bottom: 2px solid #81D4FA;
                font-weight: bold;
                font-size: 11px;
            }
        """
        )

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
            db_data = ContabilitaQueries.get_data_by_year(db_path, self.year)

            # Formattazione per la visualizzazione
            display_rows = []
            for row in db_data:
                # Trasforma i dati in stringhe leggibili per il modello
                display_row = [
                    str(x) if x is not None else "" for x in row[: len(self.COLUMNS)]
                ]
                display_rows.append(display_row)

            self.model.update_data(display_rows)

        except Exception as e:
            print(f"Error loading data for year {self.year}: {e}")

    def set_search_query(self, query):
        """Placeholder per la ricerca (da implementare nel modello se necessario)."""
        pass
