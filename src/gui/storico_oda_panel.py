"""
SyncroJob - Storico OdA Panel
Pannello per la visualizzazione del Database Storico OdA con architettura Master-Detail e raggruppamento (QTreeView).
"""

from typing import Any, List, Tuple

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QFont
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSplitter,
    QTreeView,
    QVBoxLayout,
    QWidget,
    QStyledItemDelegate,
    QStyle
)

from src.core.constants import Icons
from src.core.database import db_manager
from src.gui.formatters import format_currency_smart, format_date_it
from src.utils.helpers import get_asset_path, get_colored_icon


class ChildDescriptionDelegate(QStyledItemDelegate):
    """Delegate per estendere il testo della descrizione (Col 1) sulla colonna successiva per i figli."""

    def __init__(self, tree_view):
        super().__init__(tree_view)
        self.tree = tree_view

    def paint(self, painter, option, index):
        if index.column() == 1 and index.parent().isValid():
            # È una riga figlia, colonna Descrizione.
            # Estendi il rettangolo per includere la larghezza della colonna successiva (Pos)
            next_col_width = self.tree.columnWidth(2)
            
            painter.save()
            
            # Setup rect esteso
            full_rect = option.rect.adjusted(0, 0, next_col_width, 0)
            
            # Gestione stato selezione
            if option.state & QStyle.State.State_Selected:
                painter.fillRect(option.rect, option.palette.highlight())
                painter.setPen(option.palette.highlightedText().color())
            else:
                painter.setPen(option.palette.text().color())
                # Disegna sfondo (opzionale, solitamente gestito dalla view)
            
            # Disegna Testo
            text = index.data()
            # Usa TextWordWrap se necessario, o ElideRight
            painter.drawText(full_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)
            
            painter.restore()
        else:
            super().paint(painter, option, index)


class StoricoOdaPanel(QWidget):
    """Pannello per la visualizzazione del Database Storico OdA con Tree View (Grouped)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Colonne della TreeView (Master)
        # Order: OdA, Data OdA, Pos, Valore Netto, Stato
        self.master_headers = [
            "OdA",
            "Data OdA",
            "Pos",
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

        # Use QStandardItemModel for Tree grouping
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(self.master_headers)

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

        # 2. Contenitore Splitter (Tree | Dettaglio)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- TREE VIEW (MASTER) ---
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setAlternatingRowColors(True)
        self.tree.setSortingEnabled(False) # Grouping logic handles sort
        self.tree.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tree.setAnimated(True)

        # Selection
        self.tree.selectionModel().selectionChanged.connect(self._on_selection_changed)

        # Header Styling
        header = self.tree.header()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Custom Delegate per visualizzazione estesa descrizione
        self.tree.setItemDelegate(ChildDescriptionDelegate(self.tree))

        self.splitter.addWidget(self.tree)

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
        """Aggiorna il pannello dettaglio quando si seleziona un item."""
        indexes = self.tree.selectionModel().selectedRows()
        if not indexes:
            return

        index = indexes[0]
        item = self.model.itemFromIndex(index)
        if not item:
            return

        # Retrieve full data stored in UserRole
        full_data = item.data(Qt.ItemDataRole.UserRole)

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
        else:
            # If parent item selected (without specific row data, or aggregate), clear details or show summary?
            # Usually parent has the first row data as representative or aggregate.
            # Let's see how populate_tree attaches data.
            pass

    def refresh_data(self):
        """Aggiorna i dati della tabella."""
        query, params = self._build_query()

        try:
            full_rows = db_manager.execute_query(
                db_manager.DB_STORICO_ODA, query, tuple(params)
            )
            self._raw_full_data = full_rows
            self._populate_tree(full_rows)
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

        # Order by ODA, POS, NUM_RIGA so grouping is easy
        query += " ORDER BY oda DESC, pos_oda ASC, CAST(num_riga AS INTEGER) ASC LIMIT 3000"
        return query, params

    def _populate_tree(self, full_rows: List[Tuple]):
        """Popola il modello ad albero raggruppando per ODA + POS."""
        self.model.removeRows(0, self.model.rowCount())

        groups = {} # (oda, pos) -> ParentItem

        for r in full_rows:
            # Indices based on _build_query / self.full_headers
            # oda=2, data=1, pos=3, valore=10, stato=4
            # num_riga=27, descrizione=6, testo_breve=31, prezzo=30, qta=28, uom=29

            oda = r[2]
            pos = r[3]
            group_key = (oda, pos)

            # Create Parent Group if not exists
            if group_key not in groups:
                # Parent columns: OdA, Data OdA, Pos, Valore Netto, Stato
                item_oda = QStandardItem(str(oda))
                item_data = QStandardItem(format_date_it(str(r[1])))
                item_pos = QStandardItem(str(pos))
                item_val = QStandardItem(format_currency_smart(str(r[10])))
                item_stato = QStandardItem(str(r[4]))
                
                # Make parent bold
                bold_font = QFont()
                bold_font.setBold(True)
                for it in [item_oda, item_data, item_pos, item_val, item_stato]:
                    it.setEditable(False)
                    it.setFont(bold_font)

                # Store full data on the parent too (representative of the position)
                item_oda.setData(r, Qt.ItemDataRole.UserRole)

                self.model.appendRow([item_oda, item_data, item_pos, item_val, item_stato])
                groups[group_key] = item_oda

            parent_item = groups[group_key]

            # Create Child Row (The detailed line)
            # Child layout mapping to columns:
            # Col 0 (OdA) -> "Riga: {num_riga}"
            # Col 1 (Data) -> {Testo Breve} or {Descrizione}
            # Col 2 (Pos) -> ""
            # Col 3 (Valore) -> {Prezzo Lordo}
            # Col 4 (Stato) -> {Quantita} {UOM}

            num_riga = r[27]
            desc = r[31] if r[31] else r[6] # Testo breve pref, else descrizione
            prezzo = r[30]
            qta = r[28]
            uom = r[29]

            c_riga = QStandardItem(f"Riga: {num_riga}")
            c_desc = QStandardItem(str(desc))
            c_empty = QStandardItem("")
            c_prezzo = QStandardItem(format_currency_smart(str(prezzo)))
            c_qta = QStandardItem(f"{qta} {uom}" if qta else "")

            # Child Read-only
            for it in [c_riga, c_desc, c_empty, c_prezzo, c_qta]:
                it.setEditable(False)
                # Visual distinction
                it.setForeground(Qt.GlobalColor.darkGray)

            # Store data on child
            c_riga.setData(r, Qt.ItemDataRole.UserRole)

            parent_item.appendRow([c_riga, c_desc, c_empty, c_prezzo, c_qta])
