from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PyQt6.QtCore import QModelIndex, QSortFilterProxyModel, Qt, QTimer
from PyQt6.QtWidgets import (
    QHeaderView,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.core.contabilita_queries import ContabilitaQueries
from src.core.paths import CONFIG_DIR
from src.core.utils.formatters import format_date_it
from src.gui.formatters import (
    FastTableModel,
    format_currency_smart,
    format_number_smart,
)
from src.gui.styles import COLORS

if TYPE_CHECKING:
    from PyQt6.QtCore import QObject


class MultiColumnFilterProxyModel(QSortFilterProxyModel):
    """Proxy model che filtra su tutte le colonne con supporto multi-termine."""

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._filter_text = ""

    def set_filter_text(self, text: str) -> None:
        """Imposta il testo di filtro (supporta termini multipli separati da spazio)."""
        self._filter_text = text.lower().strip()
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, _source_parent: QModelIndex) -> bool:
        """Determina se una riga del modello sorgente deve essere inclusa nel filtro."""
        if not self._filter_text:
            return True

        search_terms = self._filter_text.split()
        model = self.sourceModel()
        if not model:
            return False

        # Concatena tutte le colonne della riga
        row_text = ""
        for col in range(model.columnCount()):
            index = model.index(source_row, col)
            value = model.data(index, Qt.ItemDataRole.DisplayRole)
            if value:
                row_text += str(value).lower() + " "

        # Tutti i termini devono essere presenti
        return all(term in row_text for term in search_terms)


class ContabilitaYearTab(QWidget):
    """Tab per un singolo anno ottimizzato per massima reattività."""

    COLUMNS: ClassVar[list[str]] = [
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

    def __init__(self, year: int, parent: QWidget | None = None) -> None:
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

        # Proxy model per filtraggio
        self.proxy_model = MultiColumnFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.model)

        self._setup_ui()
        # Defer data loading for better responsiveness
        QTimer.singleShot(10, self._load_data)

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)

        self.table = QTableView()
        self.table.setModel(self.proxy_model)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(f"""
            QTableView {{
                gridline-color: {COLORS["bg_alt"]};
                background-color: {COLORS["bg_white"]};
                alternate-background-color: {COLORS["bg_light"]};
                selection-background-color: {COLORS["table_selection_bg"]};
                selection-color: {COLORS["text_dark"]};
                border: none;
            }}
            QHeaderView::section {{
                background-color: {COLORS["bg_light"]};
                color: {COLORS["text_dark"]};
                padding: 8px;
                font-weight: bold;
                border: none;
                border-bottom: 1px solid {COLORS["border_light"]};
            }}
        """)

        # --- Configurazione Selezione (Single row, come richiesto) ---
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

        self.table.setSortingEnabled(True)
        if v_header := self.table.verticalHeader():
            v_header.setVisible(False)
        self.table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        header = self.table.horizontalHeader()
        if header is None:
            raise RuntimeError("Table horizontal header is None - table not properly initialized")  # noqa: TRY003
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        # Inizialmente usa Interactive per tutte le colonne
        # per permettere il ridimensionamento automatico basato sul contenuto
        for i in range(len(self.COLUMNS)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)

        # Imposta larghezze minime ragionevoli
        self.table.setColumnWidth(0, 90)  # DATA PREV.
        self.table.setColumnWidth(1, 70)  # MESE
        self.table.setColumnWidth(2, 80)  # N° PREV.
        self.table.setColumnWidth(3, 100)  # TOTALE PREV.
        self.table.setColumnWidth(4, 300)  # ATTIVITA'
        self.table.setColumnWidth(5, 80)  # TCL
        self.table.setColumnWidth(6, 80)  # ODC
        self.table.setColumnWidth(7, 100)  # STATO ATTIVITA'
        self.table.setColumnWidth(8, 100)  # TIPOLOGIA
        self.table.setColumnWidth(9, 80)  # ORE SP
        self.table.setColumnWidth(10, 80)  # RESA
        self.table.setColumnWidth(11, 250)  # ANNOTAZIONI

        layout.addWidget(self.table)

    def refresh_data(self) -> None:
        """Metodo pubblico per rinfrescare i dati del tab."""
        self._load_data()

    def _load_data(self) -> None:
        """Carica i dati dal DB e aggiorna il modello virtuale."""
        try:
            db_path = CONFIG_DIR / "data" / "contabilita.db"
            # Ottiene dati GREZZI (tupla di valori misti: str, float, None)
            db_data = ContabilitaQueries.get_data_by_year(db_path, self.year)

            # Passa i dati grezzi direttamente al modello.
            # Il modello userà i formatters per la visualizzazione e i valori grezzi per l'ordinamento.
            # FastTableModel si aspetta lista di liste/tuple accessibili per indice.

            # Nota: ContabilitaQueries restituisce tutto. Dobbiamo assicurarci di prendere solo le colonne che servono
            # se la query ritorna più colonne di self.COLUMNS.
            # Slice per sicurezza
            display_rows = [list(row[: len(self.COLUMNS)]) for row in db_data]

            self.model.update_data(display_rows)

            # Ridimensiona le colonne al contenuto dopo il caricamento
            QTimer.singleShot(100, self._adjust_column_widths)

        except Exception as e:
            print(f"Error loading data for year {self.year}: {e}")

    def _adjust_column_widths(self) -> None:
        """Adatta le larghezze delle colonne al contenuto, mantenendo un minimo leggibile."""
        header = self.table.horizontalHeader()
        if header is None:
            raise RuntimeError("Table horizontal header is None - cannot adjust column widths")  # noqa: TRY003

        # Ridimensiona tutte le colonne al contenuto
        self.table.resizeColumnsToContents()

        # Aggiungi un buffer per leggibilità e assicura larghezze minime
        column_min_widths = {
            0: 90,  # DATA PREV.
            1: 70,  # MESE
            2: 80,  # N° PREV.
            3: 100,  # TOTALE PREV.
            4: 200,  # ATTIVITA' (minimo più largo)
            5: 80,  # TCL
            6: 80,  # ODC
            7: 100,  # STATO ATTIVITA'
            8: 100,  # TIPOLOGIA
            9: 80,  # ORE SP
            10: 80,  # RESA
            11: 150,  # ANNOTAZIONI (minimo più largo)
        }

        for col, min_width in column_min_widths.items():
            current_width = self.table.columnWidth(col)
            # Usa il massimo tra contenuto + buffer e il minimo definito
            new_width = max(int(current_width * 1.1) + 10, min_width)
            self.table.setColumnWidth(col, new_width)

        # Imposta Stretch per le colonne con testo lungo (dopo aver impostato le altre)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # ATTIVITA'
        header.setSectionResizeMode(11, QHeaderView.ResizeMode.Stretch)  # ANNOTAZIONI

    def set_search_query(self, query: str) -> None:
        """Applica il filtro di ricerca."""
        self.filter_data(query)

    def filter_data(self, text: str) -> None:
        """Filtra i dati in base al testo di ricerca."""
        self.proxy_model.set_filter_text(text)
