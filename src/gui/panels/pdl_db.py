"""
SyncroJob - PDL Database Panel
Pannello per la visualizzazione del Database PDL SafeWork.
"""

import os
from datetime import datetime
from typing import Any, List, Optional, Tuple

import pandas as pd
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QScrollArea,
    QSplitter,
    QStyledItemDelegate,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.database import db_manager
from src.gui.formatters import FastTableModel
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path, get_colored_icon


class PDLDelegate(QStyledItemDelegate):
    """Delegate per gestire il wrap selettivo e l'allineamento nelle celle PDL."""

    def __init__(self, date_columns, parent=None):
        super().__init__(parent)
        self.date_columns = date_columns

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        # Abilita il wrap per tutte le colonne tranne quelle date
        if index.column() not in self.date_columns:
            option.features |= option.ViewItemFeature.HasDisplay
            option.displayAlignment = (
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
            )
            option.textElideMode = Qt.TextElideMode.ElideNone
        else:
            # Date: riga singola
            option.textElideMode = Qt.TextElideMode.ElideRight


class PDLDBPanel(QWidget):
    """Pannello per la visualizzazione del Database PDL SafeWork con architettura Master-Detail."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Nuove Colonne della Tabella (Vista Master)
        self.master_headers = [
            "Data Creazione",
            "Richiedente",
            "N° PDL",
            "Area",
            "Unità",
            "Stato",
            "Descrizione",
        ]

        # Mapping completo per il Dettaglio (Tutte le 21 colonne)
        self.full_headers = [
            "ID",
            "N° PDL",
            "Data Creazione",
            "Area",
            "Unità",
            "Ditta",
            "Descrizione",
            "Tipologia",
            "Stato",
            "Apparecchiatura",
            "Richiedente",
            "Data Richiesta",
            "Emittente",
            "Data Emissione",
            "Aprente",
            "Data Apertura",
            "Priorità",
            "Contratto",
            "Ordine",
            "Sito",
            "Importato il",
        ]

        self.model = FastTableModel([], self.master_headers)
        self._raw_full_data = []  # Buffer per i dati completi
        self._cache = {}  # Cache per le query

        # Stato Ordinamento
        self.current_sort_col = None
        self.current_sort_order = "DESC"

        # Timer per ricerca ritardata (Debounce)
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.refresh_data)

        self._setup_ui()
        QTimer.singleShot(50, self.refresh_data)
        QTimer.singleShot(100, self._populate_groups)
        QTimer.singleShot(150, self._update_areas)
        QTimer.singleShot(200, self._update_units)

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 1. Filtri (Top)
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca ovunque...")
        self.search_input.setMaximumWidth(250)  # Restringi barra ricerca
        self.search_input.textChanged.connect(lambda: self.search_timer.start(500))
        filter_layout.addWidget(self.search_input)

        filter_layout.addWidget(QLabel("Gruppo:"))
        self.group_filter = QComboBox()
        self.group_filter.addItem("Tutti")
        self.group_filter.setMinimumWidth(80)
        filter_layout.addWidget(self.group_filter)

        filter_layout.addWidget(QLabel("Sito:"))
        self.site_filter = QComboBox()
        self.site_filter.addItems(["Tutti i siti", "IGCC", "ISAB Nord", "ISAB Sud"])
        filter_layout.addWidget(self.site_filter)

        filter_layout.addWidget(QLabel("Area:"))
        self.area_filter = QComboBox()
        self.area_filter.addItem("Tutte")
        self.area_filter.setMinimumWidth(100)
        filter_layout.addWidget(self.area_filter)

        filter_layout.addWidget(QLabel("Unità:"))
        self.unit_filter = QComboBox()
        self.unit_filter.addItem("Tutte")
        self.unit_filter.setMinimumWidth(80)
        filter_layout.addWidget(self.unit_filter)

        # Connessioni segnali (DOPO inizializzazione widget per evitare crash)
        self.group_filter.currentTextChanged.connect(self.refresh_data)
        self.site_filter.currentTextChanged.connect(self._on_site_changed)
        self.area_filter.currentTextChanged.connect(self._on_area_changed)
        self.unit_filter.currentTextChanged.connect(self.refresh_data)

        filter_layout.addStretch()

        # Clear Filters
        self.clear_btn = ModernButton(
            "RESETTA FILTRI",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.SMALL,
        )
        self.clear_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.RESET), "#FFFFFF")
        )
        self.clear_btn.setToolTip("Resetta Filtri")
        self.clear_btn.clicked.connect(self._reset_filters)
        filter_layout.addWidget(self.clear_btn)

        # Export Excel
        self.export_btn = ModernButton(
            "ESPORTA", variant=ModernButton.Variant.SUCCESS, size=ModernButton.Size.SMALL
        )
        self.export_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.EXCEL), "#FFFFFF")
        )
        self.export_btn.setToolTip("Esporta Excel")
        self.export_btn.clicked.connect(self._export_to_excel)
        filter_layout.addWidget(self.export_btn)

        main_layout.addLayout(filter_layout)

        # 2. Contenitore Splitter (Tabella | Dettaglio)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- TABELLA (MASTER) ---
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setItemDelegate(
            PDLDelegate([0], self.table)
        )  # Data Creazione è indice 0

        self.table.selectionModel().selectionChanged.connect(self._on_selection_changed)
        header = self.table.horizontalHeader()
        header.setSectionsClickable(True)
        header.sectionClicked.connect(self._on_header_clicked)

        self.splitter.addWidget(self.table)

        # --- PANNELLO DETTAGLIO (DETAIL) ---
        detail_container = QWidget()
        detail_layout = QVBoxLayout(detail_container)
        detail_layout.setContentsMargins(5, 0, 5, 0)

        detail_title = QLabel("Dettaglio Completo PDL")
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
        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 1)

        main_layout.addWidget(self.splitter)

    def _populate_groups(self):
        """Popola la dropdown dei gruppi (indipendente)."""
        try:
            query_grp = "SELECT DISTINCT SUBSTR(n_pdl, INSTR(n_pdl, '/') + 1) as grp FROM pdl WHERE n_pdl LIKE '%/%' ORDER BY grp"
            rows_grp = db_manager.execute_query(db_manager.DB_PDL, query_grp)

            self.group_filter.blockSignals(True)
            self.group_filter.clear()
            self.group_filter.addItem("Tutti")
            for r in rows_grp:
                if r[0]:
                    self.group_filter.addItem(str(r[0]))
            self.group_filter.blockSignals(False)
        except Exception as e:
            print(f"Errore popolamento gruppi: {e}")

    def _update_areas(self):
        """Aggiorna le aree in base al sito selezionato."""
        site = self.site_filter.currentText()
        query = "SELECT DISTINCT area FROM pdl WHERE area IS NOT NULL AND area != ''"
        params = []

        if site != "Tutti i siti":
            query += " AND sito = ?"
            params.append(site)

        query += " ORDER BY area"

        try:
            rows = db_manager.execute_query(db_manager.DB_PDL, query, tuple(params))

            current_area = self.area_filter.currentText()
            self.area_filter.blockSignals(True)
            self.area_filter.clear()
            self.area_filter.addItem("Tutte")

            found = False
            for r in rows:
                if r[0]:
                    self.area_filter.addItem(str(r[0]))
                    if str(r[0]) == current_area:
                        found = True

            # Ripristina selezione se possibile, altrimenti Tutte
            if found:
                self.area_filter.setCurrentText(current_area)
            else:
                self.area_filter.setCurrentIndex(0)

            self.area_filter.blockSignals(False)
        except Exception as e:
            print(f"Errore update areas: {e}")

    def _update_units(self):
        """Aggiorna le unità in base a sito e area selezionati."""
        site = self.site_filter.currentText()
        area = self.area_filter.currentText()

        query = "SELECT DISTINCT unita FROM pdl WHERE unita IS NOT NULL AND unita != ''"
        params = []

        if site != "Tutti i siti":
            query += " AND sito = ?"
            params.append(site)

        if area != "Tutte":
            query += " AND area = ?"
            params.append(area)

        query += " ORDER BY unita"

        try:
            rows = db_manager.execute_query(db_manager.DB_PDL, query, tuple(params))

            current_unit = self.unit_filter.currentText()
            self.unit_filter.blockSignals(True)
            self.unit_filter.clear()
            self.unit_filter.addItem("Tutte")

            found = False
            for r in rows:
                if r[0]:
                    self.unit_filter.addItem(str(r[0]))
                    if str(r[0]) == current_unit:
                        found = True

            if found:
                self.unit_filter.setCurrentText(current_unit)
            else:
                self.unit_filter.setCurrentIndex(0)

            self.unit_filter.blockSignals(False)
        except Exception as e:
            print(f"Errore update units: {e}")

    def _on_site_changed(self):
        """Gestisce il cambio sito: aggiorna aree (che aggiorneranno unità) e tabella."""
        self._update_areas()
        self._update_units()  # Forzato per sicurezza
        self.refresh_data()

    def _on_area_changed(self):
        """Gestisce il cambio area: aggiorna unità e tabella."""
        self._update_units()
        self.refresh_data()

    def _on_selection_changed(self, selected, _deselected):
        """Aggiorna il pannello dettaglio quando si seleziona una riga."""
        indexes = self.table.selectionModel().selectedRows()
        if not indexes:
            return

        row_idx = indexes[0].row()
        if row_idx < len(self._raw_full_data):
            data = self._raw_full_data[row_idx]
            for i, h in enumerate(self.full_headers):
                val = str(data[i])
                if val.lower() == "nan" or val == "None":
                    val = ""

                # Formattazione "Importato il"
                if h == "Importato il" and val:
                    try:
                        dt = datetime.strptime(val, "%Y-%m-%d %H:%M:%S")
                        val = dt.strftime("%d/%m/%Y %H:%M:%S")
                    except Exception:
                        pass

                self.detail_labels[h].setText(val)

    def _on_header_clicked(self, logical_index):
        """Gestisce il toggle dell'ordinamento."""
        if self.current_sort_col == logical_index:
            self.current_sort_order = (
                "DESC" if self.current_sort_order == "ASC" else "ASC"
            )
        else:
            self.current_sort_col = logical_index
            self.current_sort_order = "ASC"

        self.refresh_data(sort_col=logical_index)

    def refresh_data(self, sort_col=None):
        """Aggiorna i dati della tabella PDL con sistema di cache."""
        query, params = self._build_pdl_query(sort_col)
        cache_key = f"{query}_{params}"

        if cache_key in self._cache:
            full_rows = self._cache[cache_key]
        else:
            try:
                full_rows = db_manager.execute_query(
                    db_manager.DB_PDL, query, tuple(params)
                )
                self._cache[cache_key] = full_rows
            except Exception as e:
                print(f"Errore caricamento PDL: {e}")
                return

        self._raw_full_data = full_rows
        master_rows = self._process_pdl_rows(full_rows)
        self.model.update_data(master_rows)
        self._update_pdl_ui(len(master_rows))

    def _build_pdl_query(self, sort_col: Optional[int]) -> Tuple[str, List[Any]]:
        """Costruisce la query SQL per i PDL."""
        search_text = self.search_input.text().lower()
        site_filter = self.site_filter.currentText()
        group_filter = self.group_filter.currentText()

        query = "SELECT id, n_pdl, data_creazione, area, unita, ditta, descrizione_lavoro, tipologia, stato, apparecchiatura, richiedente, data_richiesta, emittente, data_emissione, aprente, data_apertura, priorita, contratto, ordine, sito, importato_il FROM pdl WHERE 1=1"
        params = []

        if site_filter != "Tutti i siti":
            query += " AND sito = ?"
            params.append(site_filter)

        if group_filter != "Tutti":
            query += " AND n_pdl LIKE ?"
            params.append(f"%/{group_filter}")

        if self.area_filter.currentText() != "Tutte":
            query += " AND area = ?"
            params.append(self.area_filter.currentText())

        if self.unit_filter.currentText() != "Tutte":
            query += " AND unita = ?"
            params.append(self.unit_filter.currentText())

        if search_text:
            # Ricerca estesa su TUTTI i campi rilevanti
            # Colonne: n_pdl, area, unita, ditta, descrizione_lavoro, tipologia, stato,
            # apparecchiatura, richiedente, emittente, aprente, priorita, contratto, ordine, sito

            search_cols = [
                "n_pdl",
                "area",
                "unita",
                "ditta",
                "descrizione_lavoro",
                "tipologia",
                "stato",
                "apparecchiatura",
                "richiedente",
                "emittente",
                "aprente",
                "priorita",
                "contratto",
                "ordine",
                "sito",
            ]

            OR_clause = " OR ".join([f"{col} LIKE ?" for col in search_cols])
            query += f" AND ({OR_clause})"

            p = f"%{search_text}%"
            params.extend([p] * len(search_cols))

        # Ordinamento
        order_map = {
            0: "data_creazione",
            1: "richiedente",
            2: "n_pdl",
            3: "area",
            4: "unita",
            5: "stato",
            6: "descrizione_lavoro",
        }

        order_clause = ""
        if sort_col is not None and sort_col in order_map:
            col_name = order_map[sort_col]
            # Ordinamento numerico speciale per N° PDL
            if col_name == "n_pdl":
                order_clause = f" ORDER BY CAST(n_pdl AS INTEGER) {self.current_sort_order}, n_pdl {self.current_sort_order}"

            # Ordinamento per Data (DD/MM/YYYY HH:MM:SS -> YYYYMMDD...)
            elif col_name == "data_creazione":
                # substr(date, 7, 4) = YYYY
                # substr(date, 4, 2) = MM
                # substr(date, 1, 2) = DD
                # substr(date, 11) = HH:MM:SS
                order_clause = f" ORDER BY substr(data_creazione, 7, 4) || substr(data_creazione, 4, 2) || substr(data_creazione, 1, 2) || substr(data_creazione, 11) {self.current_sort_order}"

            else:
                order_clause = f" ORDER BY {col_name} {self.current_sort_order}"
        else:
            order_clause = " ORDER BY importato_il DESC"

        query += order_clause
        query += " LIMIT 2000"
        return query, params

    def _process_pdl_rows(self, full_rows: List[Tuple]) -> List[List[Any]]:
        """Pulisce e formatta le righe per la visualizzazione Master."""
        # Nuova mappatura Master: DATA CREAZIONE, RICHIEDENTE, N° PDL, AREA, UNITA, STATO, DESCRIZIONE
        # Indici full: 2, 10, 1, 3, 4, 8, 6
        master_rows = []
        for r in full_rows:
            row = [r[2], r[10], r[1], r[3], r[4], r[8], r[6]]
            master_rows.append(
                [("" if str(val).lower() in ["nan", "none"] else val) for val in row]
            )
        return master_rows

    def _update_pdl_ui(self, count: int):
        """Ottimizza il layout della tabella."""
        header = self.table.horizontalHeader()
        for i in range(len(self.master_headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)

        self.table.resizeColumnsToContents()
        # Limita larghezza colonne tranne descrizione
        for i in range(len(self.master_headers)):
            if i != 6 and header.sectionSize(i) > 200:
                header.resizeSection(i, 200)

        QTimer.singleShot(
            10, lambda: header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        )
        if count < 500:
            QTimer.singleShot(100, self.table.resizeRowsToContents)

    def _reset_filters(self):
        """Resetta tutti i filtri allo stato iniziale."""
        # Blocca segnali per evitare reload multipli
        self.group_filter.blockSignals(True)
        self.site_filter.blockSignals(True)
        self.area_filter.blockSignals(True)
        self.unit_filter.blockSignals(True)
        self.search_input.blockSignals(True)

        self.search_input.clear()
        self.group_filter.setCurrentIndex(0)  # Tutti
        self.site_filter.setCurrentIndex(0)  # Tutti i siti

        # Reset dinamico Area/Unità
        self.area_filter.clear()
        self.area_filter.addItem("Tutte")
        self.area_filter.setCurrentIndex(0)

        self.unit_filter.clear()
        self.unit_filter.addItem("Tutte")
        self.unit_filter.setCurrentIndex(0)

        # Sblocca segnali
        self.group_filter.blockSignals(False)
        self.site_filter.blockSignals(False)
        self.area_filter.blockSignals(False)
        self.unit_filter.blockSignals(False)
        self.search_input.blockSignals(False)

        # Trigger update singolo
        self.refresh_data()
        # Ripopola per sicurezza (es. se aree erano filtrate)
        QTimer.singleShot(100, self._update_areas)
        QTimer.singleShot(150, self._update_units)

    def _export_to_excel(self):
        """Esporta i dati correnti in Excel secondo colonne specifiche."""
        try:
            # 1. Costruisce query senza limiti
            query, params = self._build_pdl_query(self.current_sort_col)
            # Rimuove LIMIT se presente (dalla logica attuale di _build_query che appende " LIMIT 2000")
            if " LIMIT " in query:
                query = query.split(" LIMIT ")[0]

            # Esegue query
            rows = db_manager.execute_query(db_manager.DB_PDL, query, tuple(params))

            if not rows:
                print("Nessun dato da esportare.")
                return

            # Colonne richieste (Ordine Specifico)
            # Query originale: id, n_pdl, data_creazione, area, unita, ditta, descrizione_lavoro, tipologia, stato,
            # apparecchiatura, richiedente, data_richiesta, emittente, data_emissione, aprente, data_apertura,
            # priorita, contratto, ordine, sito, importato_il

            # Map Indici Query -> Colonne Excel
            # N° PDL [1], Data Creazione [2], Area [3], Unità [4], Descrizione [6], Stato [8],
            # Apparecchiatura [9], Richiedente [10], Contratto [17], Ordine [18], Sito [19]

            export_data = []
            for r in rows:
                export_data.append(
                    {
                        "N° PDL": r[1],
                        "Data Creazione": r[2],
                        "Area": r[3],
                        "Unità": r[4],
                        "Descrizione": r[6],
                        "Stato": r[8],
                        "Apparecchiatura": r[9],
                        "Richiedente": r[10],
                        "Contratto": r[17],
                        "Ordine": r[18],
                        "Sito": r[19],
                    }
                )

            df = pd.DataFrame(export_data)

            # Dialog Salva
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Esporta Excel",
                f"Export_PDL_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                "Excel Files (*.xlsx)",
            )

            if filename:
                if not filename.endswith(".xlsx"):
                    filename += ".xlsx"

                df.to_excel(filename, index=False, engine="openpyxl")
                os.startfile(filename)  # Apre il file automaticamente

        except Exception as e:
            print(f"Errore Export Excel: {e}")
