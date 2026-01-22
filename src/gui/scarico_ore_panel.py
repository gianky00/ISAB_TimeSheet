"""
Bot TS - Scarico Ore Panel
Pannello dedicato per lo Scarico Ore Cantiere.
Aggiornato per usare Virtual Table (130k+ righe) e Filtri Avanzati.
"""

import time
from contextlib import suppress
from datetime import datetime

from PyQt6.QtCore import Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableView,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.constants import Icons
from src.core.contabilita_manager import ContabilitaManager
from src.gui.scarico_ore_components import FilterHeaderView, ScaricoOreTableModel
from src.utils.helpers import get_asset_path, get_colored_icon


class ScaricoOreWorker(QThread):
    """Worker per l'importazione in background dei dati di Scarico Ore Cantiere."""

    finished_signal = pyqtSignal(
        bool, str, int, int, float
    )  # Successo, Messaggio, Aggiunti, Rimossi, Durata
    progress_signal = pyqtSignal(str)

    def __init__(self, file_path: str):
        """Inizializza il worker con il percorso del file sorgente."""
        super().__init__()
        self.file_path = file_path
        self.start_time = 0

    def run(self):
        """Esegue l'importazione dei dati, calcolando progressi ed ETA."""
        # Inizializza DB se necessario (sicurezza)
        ContabilitaManager.init_db()
        self.start_time = time.time()

        # Pre-scan for total rows to enable accurate progress/ETA
        try:
            total_rows = ContabilitaManager.scan_scarico_ore_rows(self.file_path)
        except Exception:
            total_rows = 1000  # Fallback

        def progress_cb(current, total):
            # Use the more accurate total from scan if available
            real_total = total if total > 0 else total_rows
            if current > real_total:
                real_total = current  # Dynamic update to prevent > 100%

            elapsed = time.time() - self.start_time
            if current > 0 and elapsed > 0:
                rate = current / elapsed
                remaining = real_total - current
                eta_seconds = remaining / rate if rate > 0 else 0

                m, s = divmod(int(eta_seconds), 60)
                percent = int((current / real_total) * 100) if real_total > 0 else 0
                if percent > 99:
                    percent = 99  # Cap until actually finished

                self.progress_signal.emit(
                    f"Importazione: {percent}% completato ({current}/{real_total}) • Tempo stimato: {m}m {s}s"
                )

        success, msg, added, removed = ContabilitaManager.import_scarico_ore(
            self.file_path, progress_callback=progress_cb
        )
        total_duration = time.time() - self.start_time
        self.finished_signal.emit(success, msg, added, removed, total_duration)


class ScaricoOrePanel(QWidget):
    """
    Pannello per la visualizzazione e gestione dello Scarico Ore Cantiere.
    Implementa una tabella virtuale per gestire dataset di oltre 130.000 righe.
    """

    def __init__(self, parent=None):
        """Inizializza l'interfaccia e avvia il caricamento asincrono della cache."""
        super().__init__(parent)
        self.worker = None
        self._last_update_status = (
            None  # Store the status string to persist after reload
        )
        self._setup_ui()
        # Delay load to allow UI to show up first (optimization)
        self.search_input.setPlaceholderText("Inizializzazione dati... attendere")
        self.search_input.setEnabled(False)
        QTimer.singleShot(50, self._load_data)

    def _setup_ui(self):
        """Configura i widget del pannello (toolbar, tabella virtuale, footer)."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # 1. Create Tabs (DataEase Wrapper)
        self.tabs = QTabWidget()
        self.tabs.setProperty("class", "Level2Tabs")  # Standard Style

        # --- UNIFIED TOOLBAR (Corner Widget) ---
        self.toolbar_container = QWidget()
        toolbar_layout = QHBoxLayout(self.toolbar_container)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(15)

        # Totals Labels
        self.lbl_count = QLabel("Righe: 0")
        self.lbl_count.setStyleSheet(
            "color: #607D8B; font-weight: 600; font-size: 12px;"
        )

        self.lbl_selection_total = QLabel("Selezionato: 0")
        self.lbl_selection_total.setStyleSheet(
            "color: #009688; font-weight: 600; font-size: 12px;"
        )

        self.lbl_total_hours = QLabel("Totale Ore: 0")
        self.lbl_total_hours.setStyleSheet(
            "color: #455A64; font-weight: 700; font-size: 12px;"
        )

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cerca nei dati...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setFixedWidth(250)
        self.search_input.returnPressed.connect(
            self._perform_search
        )  # Manteniamo returnPressed per performance su grandi dati

        # Status Label
        self.status_label = QLabel("Inizializzazione...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 12px;")
        self.status_label.setTextFormat(Qt.TextFormat.RichText)

        # Update Button
        self.update_btn = QPushButton("Aggiorna")
        self.update_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.REFRESH), "#FFFFFF")
        )
        self.update_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_btn.setFixedSize(110, 34)
        self.update_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
                font-size: 13px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
            QPushButton:disabled {
                background-color: #94a3b8;
            }
        """
        )
        self.update_btn.clicked.connect(self._start_update)

        # Add widgets to toolbar
        toolbar_layout.addWidget(self.lbl_count)
        toolbar_layout.addWidget(self.lbl_selection_total)
        toolbar_layout.addWidget(self.lbl_total_hours)
        toolbar_layout.addSpacing(10)
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(self.status_label)
        toolbar_layout.addWidget(self.update_btn)

        self.tabs.setCornerWidget(self.toolbar_container, Qt.Corner.TopRightCorner)
        main_layout.addWidget(self.tabs)

        # 2. "Scarico Ore" Tab Content (Only Table)
        self.scarico_tab = QWidget()
        scarico_layout = QVBoxLayout(self.scarico_tab)
        scarico_layout.setContentsMargins(
            0, 10, 0, 0
        )  # Top margin for spacing from tabs

        # --- Virtual Table View ---
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

        # Style Fix
        self.table_view.setAlternatingRowColors(True)
        self.table_view.verticalHeader().setVisible(False)

        # Models
        self.source_model = ScaricoOreTableModel([])
        self.source_model.cache_loaded.connect(self._on_cache_loaded)
        self.source_model.loading_progress.connect(self._on_loading_progress)

        self.table_view.setModel(self.source_model)

        # Custom Header
        header = FilterHeaderView(Qt.Orientation.Horizontal, self.table_view)
        self.table_view.setHorizontalHeader(header)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap
        )

        # Connect Header Filters
        header.filterChanged.connect(self._on_header_filter_changed)

        scarico_layout.addWidget(self.table_view)

        # Add Tab
        self.tabs.addTab(
            self.scarico_tab,
            get_colored_icon(get_asset_path(Icons.DOWNLOAD), "#546E7A"),
            "Dati Scaricati",
        )

        # Connect selection changes
        self.table_view.selectionModel().selectionChanged.connect(
            self._update_selection_totals
        )

    def _format_number(self, value: float) -> str:
        """Formatta un numero: intero se non ha decimali, altrimenti 2 decimali."""
        if value % 1 == 0:
            return f"{int(value)}"
        return f"{value:.2f}"

    def _update_totals(self):
        """Ricalcola i totali basandosi esclusivamente sulle righe visibili."""
        row_count = self.source_model.rowCount()
        self.lbl_count.setText(f"Righe visibili: {row_count}")

        if row_count > 0:
            total = self.source_model.get_float_total_for_visible()
            formatted = self._format_number(total)
            self.lbl_total_hours.setText(f"Totale Ore: {formatted}")
        else:
            self.lbl_total_hours.setText("Totale Ore: 0")

    def _update_selection_totals(self):
        """Calcola la somma dei valori 'TOTALE ORE' nelle celle selezionate."""
        try:
            indexes = self.table_view.selectionModel().selectedIndexes()
            if not indexes:
                self.lbl_selection_total.setText("Totale selezionato: 0")
                return

            total_selected = 0.0
            # Column 7 is 'TOTALE ORE'
            target_col = 7

            for idx in indexes:
                if idx.column() == target_col:
                    with suppress(ValueError):
                        val_str = str(idx.data(Qt.ItemDataRole.DisplayRole))
                        if val_str:
                            val_str = val_str.replace(",", ".")
                            total_selected += float(val_str)

            formatted = self._format_number(total_selected)
            self.lbl_selection_total.setText(f"Totale selezionato: {formatted}")
        except Exception as e:
            print(f"Errore selezione: {e}")

    def set_search_query(self, text):
        """Imposta il testo della ricerca globale e sposta il focus."""
        self.search_input.setText(text)
        self.search_input.setFocus()
        self.search_input.selectAll()

    def _start_update(self):
        """Avvia il thread worker per aggiornare i dati dal file DataEase."""
        config = config_manager.load_config()
        path = config.get("dataease_path", "")

        if not path:
            QMessageBox.warning(
                self,
                "Configurazione Mancante",
                "Configura il percorso 'File Scarico Ore' nelle Impostazioni.",
            )
            return

        self.status_label.setText("Calcolo stima tempi...")
        self.update_btn.setEnabled(False)
        self.table_view.setEnabled(False)

        self.worker = ScaricoOreWorker(path)
        self.worker.finished_signal.connect(self._on_update_finished)
        self.worker.progress_signal.connect(self.status_label.setText)
        self.worker.start()

    def _on_update_finished(
        self,
        success: bool,
        msg: str,
        added: int = 0,
        removed: int = 0,
        duration: float = 0.0,
    ):
        """Callback eseguito al termine dell'aggiornamento dati."""
        self.update_btn.setEnabled(True)
        self.table_view.setEnabled(True)

        if success:
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            added_str = f"<font color='green'><b>+{added}</b></font>"
            removed_str = f"<font color='red'><b>-{removed}</b></font>"

            if duration < 60:
                time_str = f"{duration:.1f}s"
            else:
                m, s = divmod(int(duration), 60)
                time_str = f"{m}m {s}s"

            final_status = f"{timestamp} {added_str} {removed_str} (Tempo: {time_str})"
            self.status_label.setText(final_status)
            self._last_update_status = final_status

            # Invalidate cache
            try:
                if ScaricoOreTableModel.CACHE_PATH.exists():
                    ScaricoOreTableModel.CACHE_PATH.unlink()
            except Exception:
                pass

            ScaricoOreTableModel._global_cache["loaded"] = False
            self._load_data()
        else:
            self.status_label.setText("Errore")
            QMessageBox.critical(self, "Errore Aggiornamento", msg)

    def _perform_search(self):
        """Esegue il filtraggio testuale globale basato sull'input utente."""
        text = self.search_input.text()
        if not hasattr(self, "_current_col_filters"):
            self._current_col_filters = {}

        self.source_model.set_filter(text, self._current_col_filters)
        self._update_totals()

    def _on_header_filter_changed(self, col, values):
        """Gestisce il cambiamento dei filtri per colonna provenienti dall'header."""
        if not hasattr(self, "_current_col_filters"):
            self._current_col_filters = {}

        if not values:
            if col in self._current_col_filters:
                del self._current_col_filters[col]
        else:
            self._current_col_filters[col] = {str(v).lower() for v in values}

        # Re-apply filters
        text = self.search_input.text()
        self.source_model.set_filter(text, self._current_col_filters)
        self._update_totals()

    def _set_ui_loading(self, loading: bool):
        """Abilita o disabilita l'interfaccia durante operazioni pesanti."""
        self.search_input.setEnabled(not loading)
        self.update_btn.setEnabled(not loading)

        if loading:
            self.search_input.setPlaceholderText("Caricamento in corso... attendere")
            self.table_view.setDisabled(True)
            QApplication.processEvents()
        else:
            self.search_input.setPlaceholderText(
                "Filtra dati (es. scavullo 4041)... (Premi Invio)"
            )
            self.table_view.setDisabled(False)

    def _on_loading_progress(self, msg):
        """Aggiorna la label di stato con i messaggi di progresso del worker."""
        self.status_label.setText(f"{msg}")
        QApplication.processEvents()

    def _on_cache_loaded(self):
        """Callback invocato quando la cache dei dati è pronta per la visualizzazione."""
        if self._last_update_status:
            self.status_label.setText(self._last_update_status)
        else:
            self.status_label.setText("Pronto")

        self._set_ui_loading(False)
        self._resize_columns()
        self._update_totals()

    def _load_data(self):
        """Avvia il caricamento dei dati dal database o dalla cache."""
        if not ContabilitaManager.DB_PATH.exists():
            self.status_label.setText("Database non trovato.")
            return

        self._set_ui_loading(True)

        if ScaricoOreTableModel.CACHE_PATH.exists():
            self.source_model.load_data_async(raw_data=None)
        else:
            try:
                rows = ContabilitaManager.get_scarico_ore_data()
                self.source_model.load_data_async(raw_data=rows)
            except Exception as e:
                self.status_label.setText(f"Errore caricamento: {e}")
                self._set_ui_loading(False)

    def _resize_columns(self):
        """Imposta le larghezze ottimali per le colonne della tabella virtuale."""
        header = self.table_view.horizontalHeader()
        header.setMinimumHeight(80)
        header.setStretchLastSection(False)

        for i in range(11):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)

        self.table_view.setColumnWidth(0, 100)  # Data
        self.table_view.setColumnWidth(1, 150)  # Pers1
        self.table_view.setColumnWidth(2, 150)  # Pers2
        self.table_view.setColumnWidth(3, 100)  # ODC
        self.table_view.setColumnWidth(4, 60)  # POS
        self.table_view.setColumnWidth(5, 75)  # Dalle
        self.table_view.setColumnWidth(6, 75)  # Alle
        self.table_view.setColumnWidth(7, 90)  # Totale Ore

        header.setSectionResizeMode(8, QHeaderView.ResizeMode.Stretch)  # Descrizione

        self.table_view.setColumnWidth(9, 80)  # Finito
        self.table_view.setColumnWidth(10, 100)  # Commessa

    def keyPressEvent(self, event):
        """Gestisce gli eventi da tastiera, incluso Ctrl+C per la copia dei dati."""
        if event.matches(QKeySequence.StandardKey.Copy):
            self._copy_selection()
        else:
            super().keyPressEvent(event)

    def _copy_selection(self):
        """Copia le celle selezionate negli appunti in formato TSV."""
        selection = self.table_view.selectionModel()
        indexes = selection.selectedIndexes()
        if not indexes:
            return

        indexes.sort(key=lambda x: (x.row(), x.column()))

        rows_text = {}
        for idx in indexes:
            r = idx.row()
            c = idx.column()
            data = self.table_view.model().data(idx)
            if r not in rows_text:
                rows_text[r] = []
            rows_text[r].append((c, str(data)))

        tsv_lines = []
        for r in sorted(rows_text.keys()):
            line = "\t".join([x[1] for x in sorted(rows_text[r], key=lambda y: y[0])])
            tsv_lines.append(line)

        QApplication.clipboard().setText("\n".join(tsv_lines))
