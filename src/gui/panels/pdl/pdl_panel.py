"""
SyncroJob - PDL Database Panel
Pannello per la visualizzazione e gestione del Database PDL SafeWork.
Implementa un'architettura Master-Detail per l'esplorazione dei permessi di lavoro.
"""

import os
from datetime import datetime
from typing import Any

import pandas as pd
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QSplitter,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.bots import create_bot
from src.core import config_manager
from src.core.database import db_manager, pdl_queries
from src.core.sync_tracker import SyncTracker
from src.gui.components.animated_tab_widget import AnimatedTabWidget
from src.gui.formatters import FastTableModel
from src.gui.panels.base import BotWorker
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.toast import ToastManager

from .pdl_delegate import PDLDelegate
from .pdl_detail_view import PDLDetailView
from .pdl_filter_widget import PDLFilterWidget
from .programmazione_tab import ProgrammazioneTab


class PDLDBPanel(QWidget):
    """
    Pannello per la visualizzazione del Database PDL SafeWork con architettura Master-Detail.
    Gestisce il filtraggio avanzato, la ricerca testuale, l'esportazione Excel e
    l'aggiornamento dei dati tramite bot Selenium.
    """

    def __init__(self, parent: QWidget | None = None):
        """
        Inizializza il pannello PDL e carica i dati iniziali.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)

        # Member declarations
        self.filters: PDLFilterWidget
        self.splitter: QSplitter
        self.table: QTableView
        self.detail_view: PDLDetailView
        self.model: FastTableModel

        # Nuove Colonne della Tabella (Vista Master)
        self._raw_full_data: list[tuple[Any, ...]] = []  # Buffer per i dati completi
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
        self._raw_full_data = []
        self._cache: dict[str, list[tuple[Any, ...]]] = {}

        # Stato Ordinamento
        self.current_sort_col: int | None = None
        self.current_sort_order = "DESC"
        self.worker: BotWorker | None = None

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
        """Configura il layout principale con Tab e Splitter."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = AnimatedTabWidget()

        # --- TAB 1: DATABASE PDL ---
        self.db_tab = QWidget()
        db_layout = QVBoxLayout(self.db_tab)
        db_layout.setContentsMargins(10, 10, 10, 10)
        db_layout.setSpacing(5)

        # 1. Filtri
        self.filters = PDLFilterWidget()
        self.filters.filter_changed.connect(self.refresh_data)
        self.filters.site_changed.connect(self._on_site_changed)
        self.filters.area_changed.connect(self._on_area_changed)
        self.filters.update_clicked.connect(self._on_update_bot_clicked)
        self.filters.reset_clicked.connect(self._reset_filters)
        self.filters.export_clicked.connect(self._export_to_excel)
        self.filters.search_input.textChanged.connect(lambda: self.search_timer.start(500))

        db_layout.addWidget(self.filters)

        # 2. Contenitore Splitter (Tabella | Dettaglio)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- TABELLA (MASTER) ---
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(True)
        if v_header := self.table.verticalHeader():
            v_header.setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table.setItemDelegate(PDLDelegate([0], self.table))

        if sel_model := self.table.selectionModel():
            sel_model.selectionChanged.connect(self._on_selection_changed)

        if header := self.table.horizontalHeader():
            header.setSectionsClickable(True)
            header.sectionClicked.connect(self._on_header_clicked)

        self.splitter.addWidget(self.table)

        # --- PANNELLO DETTAGLIO (DETAIL) ---
        self.detail_view = PDLDetailView(self.full_headers)
        self.splitter.addWidget(self.detail_view)

        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 1)

        db_layout.addWidget(self.splitter)

        # --- TAB 2: PROGRAMMAZIONE ---
        self.prog_tab = ProgrammazioneTab()

        # Aggiunta Tab
        self.tabs.addTab(self.db_tab, "Database PDL")
        self.tabs.addTab(self.prog_tab, "Programmazione")

        layout.addWidget(self.tabs)

    def _on_update_bot_clicked(self):
        """Avvia il bot Ricerca PDL per aggiornare i dati dal portale SafeWork."""
        try:
            config = config_manager.load_config()
            safework_accounts = config.get("safework_accounts", [])

            username = ""
            password = ""
            account_type = "Esecutore"

            if safework_accounts:
                default_sw = next(
                    (a for a in safework_accounts if a.get("default")),
                    safework_accounts[0],
                )
                username = default_sw.get("username", "")
                password = default_sw.get("password", "")
                account_type = default_sw.get("type", "Esecutore")

            if not username or not password:
                QMessageBox.warning(self, "Attenzione", "Credenziali SafeWork non configurate.")
                return

            if not self._show_confirmation_dialog(
                "Aggiornamento PDL",
                f"Avviare la ricerca PDL con account <b>{username}</b> ({account_type})?",
            ):
                return

            self.filters.btn_bot_update.setEnabled(False)
            self.filters.lbl_sync_status.setText("⏳ Bot PDL...")
            ToastManager.instance().show(f"Avvio Bot PDL ({username})...", "info")

            bot = create_bot(
                "ricerca_pdl",
                username=username,
                password=password,
                account_type=account_type,
                headless=config.get("browser_headless", False),
                timeout=config.get("browser_timeout", 30),
                download_path=str(config_manager.CONFIG_DIR / "temp"),
            )

            if not bot:
                self.filters.btn_bot_update.setEnabled(True)
                return

            bot_data = [{"site_selection": "Seleziona tutto", "exclude_closed": True}]

            self.worker = BotWorker(bot, bot_data)
            self.worker.finished_signal.connect(self._on_bot_finished)
            self.worker.start()

        except Exception as e:
            self.filters.btn_bot_update.setEnabled(True)
            QMessageBox.critical(self, "Errore", f"Errore avvio bot: {e}")

    def _on_bot_finished(self, success: bool):
        """Gestisce il completamento del bot di ricerca PDL."""
        self.filters.btn_bot_update.setEnabled(True)
        if success:
            ToastManager.instance().show("PDL Aggiornati!", "success")
            self.refresh_data()
            if hasattr(self, "prog_tab"):
                self.prog_tab._load_requesters()
            win = self.window()
            if win:
                scarico_pdl = getattr(win, "scarico_pdl_panel", None)
                if scarico_pdl and hasattr(scarico_pdl, "_on_log"):
                    scarico_pdl._on_log("✅ Bot Ricerca PDL completato.")
        else:
            self.filters.lbl_sync_status.setText("❌ Errore Bot")
            QMessageBox.warning(self, "Errore", "Bot terminato con errori.")

    def _show_confirmation_dialog(self, title: str, message: str) -> bool:
        """Mostra una dialog di conferma con stile coerente."""
        try:
            dlg = QDialog(self)
            dlg.setWindowTitle(title)
            dlg.setMinimumWidth(350)
            dlg.setWindowFlags(dlg.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

            layout = QVBoxLayout(dlg)
            layout.setSpacing(20)
            layout.setContentsMargins(20, 20, 20, 20)

            lbl = QLabel(message)
            lbl.setWordWrap(True)
            lbl.setTextFormat(Qt.TextFormat.RichText)
            layout.addWidget(lbl)

            btn_layout = QHBoxLayout()
            btn_layout.addStretch()

            btn_cancel = ModernButton("Annulla", variant=ModernButton.Variant.GHOST)
            btn_cancel.clicked.connect(dlg.reject)
            btn_confirm = ModernButton("Avvia", variant=ModernButton.Variant.PRIMARY)
            btn_confirm.clicked.connect(dlg.accept)

            btn_layout.addWidget(btn_cancel)
            btn_layout.addWidget(btn_confirm)
            layout.addLayout(btn_layout)

            return dlg.exec() == 1
        except Exception:
            return False

    def _populate_groups(self):
        """Popola la dropdown dei gruppi PDL estratti dai prefissi numerici."""
        try:
            query_grp = "SELECT DISTINCT SUBSTR(n_pdl, INSTR(n_pdl, '/') + 1) as grp FROM pdl WHERE n_pdl LIKE '%/%' ORDER BY grp"
            rows_grp = db_manager.execute_query(db_manager.DB_PDL, query_grp)

            self.filters.group_filter.blockSignals(True)
            self.filters.group_filter.clear()
            self.filters.group_filter.addItem("Tutti")
            for r in rows_grp:
                if r[0]:
                    self.filters.group_filter.addItem(str(r[0]))
            self.filters.group_filter.blockSignals(False)
        except Exception as e:
            print(f"Errore popolamento gruppi: {e}")

    def _update_areas(self):
        """Aggiorna l'elenco delle Aree filtrato per Sito."""
        site = self.filters.site_filter.currentText()
        query = "SELECT DISTINCT area FROM pdl WHERE area IS NOT NULL AND area != ''"
        params = []

        if site != "Tutti i siti":
            query += " AND sito = ?"
            params.append(site)

        query += " ORDER BY area"

        try:
            rows = db_manager.execute_query(db_manager.DB_PDL, query, tuple(params))

            current_area = self.filters.area_filter.currentText()
            self.filters.area_filter.blockSignals(True)
            self.filters.area_filter.clear()
            self.filters.area_filter.addItem("Tutte")

            found = False
            for r in rows:
                if r[0]:
                    self.filters.area_filter.addItem(str(r[0]))
                    if str(r[0]) == current_area:
                        found = True

            if found:
                self.filters.area_filter.setCurrentText(current_area)
            else:
                self.filters.area_filter.setCurrentIndex(0)

            self.filters.area_filter.blockSignals(False)
        except Exception as e:
            print(f"Errore update areas: {e}")

    def _update_units(self):
        """Aggiorna l'elenco delle Unità filtrato per Sito e Area."""
        site = self.filters.site_filter.currentText()
        area = self.filters.area_filter.currentText()

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

            current_unit = self.filters.unit_filter.currentText()
            self.filters.unit_filter.blockSignals(True)
            self.filters.unit_filter.clear()
            self.filters.unit_filter.addItem("Tutte")

            found = False
            for r in rows:
                if r[0]:
                    self.filters.unit_filter.addItem(str(r[0]))
                    if str(r[0]) == current_unit:
                        found = True

            if found:
                self.filters.unit_filter.setCurrentText(current_unit)
            else:
                self.filters.unit_filter.setCurrentIndex(0)

            self.filters.unit_filter.blockSignals(False)
        except Exception as e:
            print(f"Errore update units: {e}")

    def _on_site_changed(self):
        """Triggerato al cambio del sito nei filtri."""
        self._update_areas()
        self._update_units()
        self.refresh_data()

    def _on_area_changed(self):
        """Triggerato al cambio dell'area nei filtri."""
        self._update_units()
        self.refresh_data()

    def _on_selection_changed(self, selected, _deselected):
        """Aggiorna la vista dettaglio caricando i dati della PDL selezionata."""
        sel_model = self.table.selectionModel()
        if not sel_model:
            return

        indexes = sel_model.selectedRows()
        if not indexes:
            self.detail_view.clear()
            return

        row_idx = indexes[0].row()
        if row_idx < len(self._raw_full_data):
            full_data = self._raw_full_data[row_idx]
            n_pdl = str(full_data[1])

            try:
                interventions = pdl_queries.PDLQueries.get_pdl_interventions(n_pdl)
            except Exception as e:
                print(f"Errore recupero interventi PDL {n_pdl}: {e}")
                interventions = []

            self.detail_view.update_details(full_data, interventions)
        else:
            self.detail_view.clear()

    def _on_header_clicked(self, logical_index):
        """Gestisce il toggle dell'ordinamento per colonna."""
        if self.current_sort_col == logical_index:
            self.current_sort_order = "DESC" if self.current_sort_order == "ASC" else "ASC"
        else:
            self.current_sort_col = logical_index
            self.current_sort_order = "ASC"

        self.refresh_data(sort_col=logical_index)

    def refresh_data(self, sort_col=None):
        """
        Ricarica i dati dal database PDL applicando i filtri e l'ordinamento correnti.
        Utilizza un sistema di cache per ottimizzare le prestazioni.
        """
        self.filters.lbl_sync_status.setText(f"Ultimo Sync: {SyncTracker.get_formatted_status('pdl')}")

        query, params = self._build_pdl_query(sort_col)
        cache_key = f"{query}_{params}"

        full_rows: list[tuple[Any, ...]]
        if cache_key in self._cache:
            full_rows = self._cache[cache_key]
        else:
            try:
                full_rows = db_manager.execute_query(db_manager.DB_PDL, query, tuple(params))
                self._cache[cache_key] = full_rows
            except Exception as e:
                print(f"Errore caricamento PDL: {e}")
                return

        self._raw_full_data = full_rows
        master_rows = self._process_pdl_rows(full_rows)
        self.model.update_data(master_rows)
        self._update_pdl_ui(len(master_rows))

    def _build_pdl_query(self, sort_col: int | None) -> tuple[str, list[Any]]:
        """Costruisce dinamicamente la query SQL in base ai filtri attivi."""
        f = self.filters.get_filters()
        search_text = f["search"]
        site_filter = f["site"]
        group_filter = f["group"]
        area_filter = f["area"]
        unit_filter = f["unit"]

        query = "SELECT id, n_pdl, data_creazione, area, unita, ditta, descrizione_lavoro, tipologia, stato, apparecchiatura, richiedente, data_richiesta, emittente, data_emissione, aprente, data_apertura, priorita, contratto, ordine, sito, importato_il FROM pdl WHERE 1=1"
        params = []

        if site_filter != "Tutti i siti":
            query += " AND sito = ?"
            params.append(site_filter)

        if group_filter != "Tutti":
            query += " AND n_pdl LIKE ?"
            params.append(f"%/{group_filter}")

        if area_filter != "Tutte":
            query += " AND area = ?"
            params.append(area_filter)

        if unit_filter != "Tutte":
            query += " AND unita = ?"
            params.append(unit_filter)

        if search_text:
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

        order_map = {
            0: "data_creazione",
            1: "richiedente",
            2: "n_pdl",
            3: "area",
            4: "unita",
            5: "stato",
            6: "descrizione_lavoro",
        }

        if sort_col is not None and sort_col in order_map:
            col_name = order_map[sort_col]
            if col_name == "n_pdl":
                order_clause = f" ORDER BY CAST(n_pdl AS INTEGER) {self.current_sort_order}, n_pdl {self.current_sort_order}"
            elif col_name == "data_creazione":
                order_clause = f" ORDER BY substr(data_creazione, 7, 4) || substr(data_creazione, 4, 2) || substr(data_creazione, 1, 2) || substr(data_creazione, 11) {self.current_sort_order}"
            else:
                order_clause = f" ORDER BY {col_name} {self.current_sort_order}"
        else:
            order_clause = " ORDER BY importato_il DESC"

        query += order_clause
        query += " LIMIT 2000"
        return query, params

    def _process_pdl_rows(self, full_rows: list[tuple[Any, ...]]) -> list[list[Any]]:
        """Formatta le righe per la visualizzazione compatta nella tabella master."""
        master_rows = []
        for r in full_rows:
            row = [r[2], r[10], r[1], r[3], r[4], r[8], r[6]]
            master_rows.append([("" if str(val).lower() in ("nan", "none") else val) for val in row])
        return master_rows

    def _update_pdl_ui(self, count: int):
        """Ottimizza il layout delle colonne della tabella dopo il caricamento."""
        header = self.table.horizontalHeader()
        if not header:
            return

        for i in range(len(self.master_headers)):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)

        self.table.resizeColumnsToContents()
        for i in range(len(self.master_headers)):
            if i != 6 and header.sectionSize(i) > 200:
                header.resizeSection(i, 200)

        QTimer.singleShot(10, lambda: header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch))
        if count < 500:
            QTimer.singleShot(100, self.table.resizeRowsToContents)

    def _reset_filters(self):
        """Ripristina tutti i filtri di ricerca allo stato predefinito."""
        self.filters.group_filter.blockSignals(True)
        self.filters.site_filter.blockSignals(True)
        self.filters.area_filter.blockSignals(True)
        self.filters.unit_filter.blockSignals(True)
        self.filters.search_input.blockSignals(True)

        self.filters.search_input.clear()
        self.filters.group_filter.setCurrentIndex(0)
        self.filters.site_filter.setCurrentIndex(0)
        self.filters.area_filter.clear()
        self.filters.area_filter.addItem("Tutte")
        self.filters.area_filter.setCurrentIndex(0)
        self.filters.unit_filter.clear()
        self.filters.unit_filter.addItem("Tutte")
        self.filters.unit_filter.setCurrentIndex(0)

        self.filters.group_filter.blockSignals(False)
        self.filters.site_filter.blockSignals(False)
        self.filters.area_filter.blockSignals(False)
        self.filters.unit_filter.blockSignals(False)
        self.filters.search_input.blockSignals(False)

        self.refresh_data()
        QTimer.singleShot(100, self._update_areas)
        QTimer.singleShot(150, self._update_units)

    def _export_to_excel(self):
        """Esporta l'attuale vista filtrata del database in un file Excel."""
        try:
            query, params = self._build_pdl_query(self.current_sort_col)
            if " LIMIT " in query:
                query = query.split(" LIMIT ")[0]

            rows = db_manager.execute_query(db_manager.DB_PDL, query, tuple(params))
            if not rows:
                return

            export_data = [
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
                for r in rows
            ]

            df = pd.DataFrame(export_data)
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
                os.startfile(filename)  # noqa: S606

        except Exception as e:
            print(f"Errore Export Excel: {e}")
