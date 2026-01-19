"""
SyncroJob - Storico OdA Panel
Pannello per la visualizzazione del Database Storico OdA con architettura Master-Detail.
"""

from typing import Any, List, Tuple

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSplitter,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.database import db_manager
from src.gui.formatters import FastTableModel, format_currency_smart, format_date_it
from src.utils.helpers import get_asset_path, get_colored_icon


class StoricoOdaPanel(QWidget):
    """Pannello per la visualizzazione del Database Storico OdA."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Colonne della Tabella (Vista Master)
        self.master_headers = [
            "OdA",
            "Pos",
            "Riga",
            "Fornitore",
            "Data OdA",
            "Descrizione",
            "Qta",
            "Valore Netto",
            "Stato",
        ]

                # Mapping completo per il Dettaglio
                self.full_headers = [
                    "Org. Acq.",
                    "Data OdA",
                    "OdA",
                    "Pos OdA",
                    "Stato",
                    "Cat. Contab.",
                    "Descrizione",
                    "Qta",
                    "UOM",
                    "Data Consegna",
                    "Valore Netto Pos. ODA",
                    "Valore Residuo ODA",
                    "Valore Netto ODA",
                    "Divisione",
                    "Destinatario",
                    "Nome Destinatario",
                    "Codice Fornitore",
                    "Descrizione Fornitore",
                    "Emittente Fattura",
                    "Descrizione Emittente Fattura",
                    "Contract Card",
                    "Contratto",
                    "Posizione Contratto",
                    "Gruppo Acquisti",
                    "Indicatore Rilascio",
                    "Stato Rilascio",
                    "Attività",
                    "Num riga",
                    "Quantità",
                    "Unità di Mis",
                    "Prezzo lordo",
                    "Testo breve",
                ]
        
                self.model = FastTableModel([], self.master_headers)
                
                # Formattatori
                self.model.set_column_formatter(4, format_date_it)  # Data OdA
                self.model.set_column_formatter(7, format_currency_smart)  # Valore Netto
                
                self._raw_full_data = []  # Buffer per i dati completi
        # Timer per ricerca ritardata (Debounce)
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.refresh_data)

        self._setup_ui()
        QTimer.singleShot(50, self.refresh_data)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 1. Filtri (Top)
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Cerca ovunque... (OdA, Fornitore, Descrizione, Contratto...)"
        )
        self.search_input.textChanged.connect(lambda: self.search_timer.start(500))
        filter_layout.addWidget(self.search_input)

        refresh_btn = QPushButton("Aggiorna")
        refresh_btn.setIcon(get_colored_icon(get_asset_path(Icons.REFRESH), "#000000"))
        refresh_btn.clicked.connect(self.refresh_data)
        filter_layout.addWidget(refresh_btn)
        main_layout.addLayout(filter_layout)

        # 2. Contenitore Splitter (Tabella | Dettaglio)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- TABELLA (MASTER) ---
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)

        self.table.selectionModel().selectionChanged.connect(self._on_selection_changed)
        header = self.table.horizontalHeader()
        header.sectionClicked.connect(self._on_header_clicked)

        self.splitter.addWidget(self.table)

        # --- PANNELLO DETTAGLIO (DETAIL) ---
        detail_container = QWidget()
        detail_layout = QVBoxLayout(detail_container)
        detail_layout.setContentsMargins(5, 0, 5, 0)

        detail_title = QLabel("Dettaglio Completo OdA")
        detail_title.setStyleSheet(
            "font-weight: bold; font-size: 14px; color: #2196F3; margin-bottom: 5px;"
        )
        detail_layout.addWidget(detail_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.form_layout = QFormLayout(scroll_content)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self.form_layout.setSpacing(10)

        # Placeholder labels
        self.detail_labels = {}
        for h in self.full_headers:
            val_label = QLabel("-")
            val_label.setWordWrap(True)
            val_label.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )
            self.detail_labels[h] = val_label
            self.form_layout.addRow(f"<b>{h}:</b>", val_label)

        scroll.setWidget(scroll_content)
        detail_layout.addWidget(scroll)

        self.splitter.addWidget(detail_container)
        self.splitter.setStretchFactor(0, 3)  # Tabella più larga
        self.splitter.setStretchFactor(1, 1)  # Dettaglio più stretto

        main_layout.addWidget(self.splitter)

    def _on_selection_changed(self, selected, _deselected):
        """Aggiorna il pannello dettaglio quando si seleziona una riga."""
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return

        row_idx = indexes[0].row()
        # Ensure mapping is correct even after sorting
        # We need to find the raw data index corresponding to the sorted/filtered view
        # FastTableModel sorts the _data in place, so row_idx maps directly to self.model._data
        # But wait, self._raw_full_data is parallel to self.model._data ONLY if we sort both or use proxy.
        # Current FastTableModel implementation: self._data IS the master_rows list.
        # We need to store full data in the model or link them.

        # ISSUE: FastTableModel sorts `self._data`. If I keep `_raw_full_data` separate, they go out of sync on sort.
                # FIX: The `_raw_full_data` should be stored IN the model or accessed via a unique ID.
                # For simplicity, let's look up the full row using the Primary Key (OdA, Pos, Riga).
                
                master_row = self.model._data[row_idx]
                key = (master_row[0], master_row[1], master_row[2]) # oda, pos, riga
                
                # Find in _raw_full_data (inefficient but safe for now, better use a dict)
                # Note: In _raw_full_data, indices are: OdA=2, Pos=3, Riga=27 (based on _build_query)
                full_data = next((r for r in self._raw_full_data if (r[2], r[3], r[27]) == key), None)
                
                if full_data:
                    for i, h in enumerate(self.full_headers):
                        if i < len(full_data):
                            val = str(full_data[i])
                            if val.lower() == "nan" or val == "None":
                                val = ""
                            
                            # Apply specific formatting for detail view
                            if "Data" in h:
                                val = format_date_it(val)
                            elif "Valore" in h or "Prezzo" in h:
                                val = format_currency_smart(val)
                                
                            self.detail_labels[h].setText(val)
        
            def _on_header_clicked(self, logical_index):
                self.model.sort(logical_index, self.table.horizontalHeader().sortIndicatorOrder())
        
            def refresh_data(self):
                """Aggiorna i dati della tabella."""
                query, params = self._build_query()
        
                try:
                    full_rows = db_manager.execute_query(
                        db_manager.DB_STORICO_ODA, query, tuple(params)
                    )
                    self._raw_full_data = full_rows
                    master_rows = self._process_rows(full_rows)
                    self.model.update_data(master_rows)
                    self.table.resizeColumnsToContents()
                except Exception as e:
                    print(f"Errore caricamento Storico OdA: {e}")
        
            def _build_query(self) -> Tuple[str, List[Any]]:
                """Costruisce la query SQL."""
                search_text = self.search_input.text().lower().strip()
                
                # Select columns in the exact order of self.full_headers
                query = """
                    SELECT 
                        org_acq, data_oda, oda, pos_oda, stato, cat_contab, descrizione, 
                        qta, uom, data_consegna, valore_netto_pos, valore_residuo, valore_netto_oda, 
                        divisione, destinatario, nome_destinatario, codice_fornitore, descrizione_fornitore, 
                        emittente_fattura, desc_emittente_fattura, contract_card, contratto, 
                        posizione_contratto, gruppo_acquisti, indicatore_rilascio, stato_rilascio, 
                        attivita, num_riga, quantita, unita_mis, prezzo_lordo, testo_breve
                    FROM storico_oda 
                    WHERE 1=1
                """
                params = []
        
                if search_text:
                    query += """ AND (
                        CAST(oda AS TEXT) LIKE ? OR 
                        descrizione LIKE ? OR 
                        descrizione_fornitore LIKE ? OR 
                        CAST(contratto AS TEXT) LIKE ? OR
                        codice_fornitore LIKE ?
                    )"""
                    p = f"%{search_text}%"
                    params.extend([p, p, p, p, p])
        
                query += " ORDER BY data_oda DESC LIMIT 2000"
                return query, params
        
            def _process_rows(self, full_rows: List[Tuple]) -> List[List[Any]]:
                """Pulisce e formatta le righe per la visualizzazione Master."""
                master_rows = []
                for r in full_rows:
                    # Mapping Full -> Master
                    # OdA=2, Pos=3, Riga=27, Fornitore=17, Data=1, Desc=6, Qta=7, UOM=8, Valore=10, Stato=4
                    
                    # Combine Qta + UOM
                    qta_str = f"{r[7]} {r[8]}" if r[7] else ""
                    
                    row = [
                        r[2], # OdA
                        r[3], # Pos
                        r[27], # Riga (num_riga)
                        r[17], # Fornitore (descrizione_fornitore)
                        r[1], # Data OdA
                        r[6], # Descrizione
                        qta_str, # Qta
                        r[10], # Valore Netto Pos
                        r[4], # Stato
                    ]
                    master_rows.append(
                        [("" if str(val).lower() == "nan" or val is None else val) for val in row]
                    )
                return master_rows
