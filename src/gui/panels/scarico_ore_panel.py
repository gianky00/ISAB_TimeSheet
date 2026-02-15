"""
Bot TS - Scarico Ore Panel
Pannello dedicato per lo Scarico Ore Cantiere.
Aggiornato per usare Virtual Table (130k+ righe) e Filtri Avanzati.
"""

import operator
import time
from contextlib import suppress
from datetime import datetime

from PyQt6.QtCore import QItemSelection, Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QTableView,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.constants import Icons
from src.core.contabilita_manager import ContabilitaManager
from src.gui.components.scarico_ore import FilterHeaderView, ScaricoOreTableModel
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path, get_colored_icon


class ScaricoOreWorker(QThread):
    """Worker per l'importazione in background dei dati di Scarico Ore Cantiere."""

    finished_signal = pyqtSignal(bool, str, int, int, float)  # Successo, Messaggio, Aggiunti, Rimossi, Durata
    progress_signal = pyqtSignal(str)

    def __init__(self, file_path: str):
        """Inizializza il worker con il percorso del file sorgente."""
        super().__init__()
        self.file_path = file_path
        self.start_time: float = 0.0

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

    def stop(self) -> None:
        """Ferma il worker."""
        self.requestInterruption()
        self.quit()
        self.wait()


class ScaricoOrePanel(QWidget):
    """
    Pannello per la visualizzazione e gestione dello Scarico Ore Cantiere.
    Implementa una tabella virtuale per gestire dataset di oltre 130.000 righe.
    """

    def __init__(self, parent=None):
        """Inizializza l'interfaccia e avvia il caricamento asincrono della cache."""
        super().__init__(parent)

        # Widget members (Strict Typing - Option D)
        self.tabs: QTabWidget
        self.toolbar_container: QWidget
        self.lbl_count: QLabel
        self.lbl_selection_total: QLabel
        self.lbl_total_hours: QLabel
        self.search_input: QLineEdit
        self.status_label: QLabel
        self.update_btn: ModernButton
        self.scarico_tab: QWidget
        self.table_view: QTableView
        self.source_model: ScaricoOreTableModel

        self.worker: ScaricoOreWorker | None = None
        self._current_col_filters: dict[int, set[str]] = {}
        self._last_update_status: str | None = None  # Store the status string to persist after reload
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
        self.lbl_count.setStyleSheet("color: #607D8B; font-weight: 600; font-size: 12px;")

        self.lbl_selection_total = QLabel("Selezionato: 0")
        self.lbl_selection_total.setStyleSheet("color: #009688; font-weight: 600; font-size: 12px;")

        self.lbl_total_hours = QLabel("Totale Ore: 0")
        self.lbl_total_hours.setStyleSheet("color: #455A64; font-weight: 700; font-size: 12px;")

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
        self.update_btn = ModernButton(
            "Aggiorna",
            variant=ModernButton.Variant.PRIMARY,
            icon=get_asset_path(Icons.REFRESH),
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
        scarico_layout.setContentsMargins(0, 10, 0, 0)  # Top margin for spacing from tabs

        # --- Virtual Table View ---
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        self.table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

        # Style Fix
        self.table_view.setAlternatingRowColors(True)
        v_header = self.table_view.verticalHeader()
        if v_header:
            v_header.setVisible(False)

        # Models
        self.source_model = ScaricoOreTableModel([])
        self.source_model.cache_loaded.connect(self._on_cache_loaded)
        self.source_model.loading_progress.connect(self._on_loading_progress)

        self.table_view.setModel(self.source_model)

        # Custom Header
        header = FilterHeaderView(Qt.Orientation.Horizontal, self.table_view)
        self.table_view.setHorizontalHeader(header)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap)

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
        selection_model = self.table_view.selectionModel()
        if selection_model is None:
            raise RuntimeError("SelectionModel should exist after setModel")
        selection_model.selectionChanged.connect(self._update_selection_totals)

        # Enable Sorting
        self.table_view.setSortingEnabled(True)

        # Selection Preservation Hooks
        self.source_model.layoutAboutToBeChanged.connect(self._preserve_selection)
        self.source_model.layoutChanged.connect(self._restore_selection)

        self._saved_selection_real_ids = set()

    def _preserve_selection(self):
        """Salva gli ID reali (indici sorgente) delle righe selezionate prima di un cambio layout (sort/filter)."""
        self._saved_selection_real_ids.clear()
        selection = self.table_view.selectionModel()
        if selection is None or not selection.hasSelection():
            return

        # Get selected visual rows
        selected_rows = selection.selectedRows()
        model = self.source_model

        # Map Visual Row -> Real Row ID (index in _display_data)
        for idx in selected_rows:
            if idx.isValid():
                visual_row = idx.row()
                if visual_row < len(model._visible_indices):
                    real_id = model._visible_indices[visual_row]
                    self._saved_selection_real_ids.add(real_id)

    def _restore_selection(self):
        """Ripristina la selezione basandosi sugli ID reali salvati."""
        if not self._saved_selection_real_ids:
            return

        model = self.source_model
        # Build map: Real ID -> New Visual Row
        # Optimization: Only build for visible rows
        real_to_visual = {real_id: vis_row for vis_row, real_id in enumerate(model._visible_indices)}

        new_selection = self.table_view.selectionModel()
        if new_selection is None:
            raise RuntimeError("SelectionModel should exist for restoration")

        selection_batch = QItemSelection()
        col_count = model.columnCount() - 1

        for real_id in self._saved_selection_real_ids:
            if real_id in real_to_visual:
                vis_row = real_to_visual[real_id]
                # Select entire row
                top_left = model.index(vis_row, 0)
                bottom_right = model.index(vis_row, col_count)
                selection_batch.select(top_left, bottom_right)

        if not selection_batch.isEmpty():
            new_selection.select(
                selection_batch,
                new_selection.SelectionFlag.ClearAndSelect | new_selection.SelectionFlag.Rows,
            )
            # Update totals
            self._update_selection_totals()

    def _format_number(self, value: float) -> str:
        """Formatta un numero: intero se non ha decimali, altrimenti 2 decimali."""
        if value % 1 == 0:
            return str(int(value))
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
            selection_model = self.table_view.selectionModel()
            if selection_model is None:
                raise RuntimeError("Table view selection model is None")
            indexes = selection_model.selectedIndexes()
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

    def set_search_query(self, text: str):
        """Imposta il testo della ricerca globale e sposta il focus."""
        self.search_input.setText(text)
        self.search_input.setFocus()
        self.search_input.selectAll()

    def _start_update(self):
        """Avvia il thread worker per aggiornare i dati dal file DataEase."""
        path = config_manager.load_config().get("dataease_path", "")

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

        worker = ScaricoOreWorker(path)
        self.worker = worker
        worker.finished_signal.connect(self._on_update_finished)
        worker.progress_signal.connect(self.status_label.setText)
        worker.start()

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
            with suppress(Exception):
                if ScaricoOreTableModel.CACHE_PATH.exists():
                    ScaricoOreTableModel.CACHE_PATH.unlink()

            ScaricoOreTableModel._global_cache["loaded"] = False
            self._load_data()
        else:
            self.status_label.setText("Errore")
            QMessageBox.critical(self, "Errore Aggiornamento", msg)

    def _on_stop(self):
        """Gestisce lo stop del bot."""
        if self.worker:
            self.worker.stop()
            self.status_label.setText("Arresto richiesto...")

    def _perform_search(self):
        """Esegue il filtraggio testuale globale basato sull'input utente."""
        text = self.search_input.text()
        self.source_model.set_filter(text, self._current_col_filters)
        self._update_totals()

    def _on_header_filter_changed(self, col: int, values: list[str]):
        """Gestisce il cambiamento dei filtri per colonna provenienti dall'header."""

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
            self.search_input.setPlaceholderText("Filtra dati (es. scavullo 4041)... (Premi Invio)")
            self.table_view.setDisabled(False)

    def _on_loading_progress(self, msg: str):
        """Aggiorna la label di stato con i messaggi di progresso del worker."""
        self.status_label.setText(str(msg))
        QApplication.processEvents()

    def _on_cache_loaded(self):
        """Callback invocato quando la cache dei dati è pronta per la visualizzazione."""
        if self._last_update_status:
            self.status_label.setText(self._last_update_status)
        else:
            self.status_label.setText("Pronto")

        self._set_ui_loading(False)
        self._resize_columns()
        self.table_view.sortByColumn(0, Qt.SortOrder.DescendingOrder)
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
        if header is None:
            raise RuntimeError("Table horizontal header is None")
        header.setMinimumHeight(80)
        header.setStretchLastSection(False)

        for i in range(11):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)

        self.table_view.setColumnWidth(0, 120)  # Data (aumentato da 100 a 120)
        self.table_view.setColumnWidth(1, 150)  # Pers1
        self.table_view.setColumnWidth(2, 150)  # Pers2
        self.table_view.setColumnWidth(3, 100)  # ODC
        self.table_view.setColumnWidth(4, 60)  # POS
        self.table_view.setColumnWidth(5, 75)  # Dalle
        self.table_view.setColumnWidth(6, 75)  # Alle
        self.table_view.setColumnWidth(7, 90)  # Totale Ore

        header.setSectionResizeMode(8, QHeaderView.ResizeMode.Stretch)  # Descrizione

        self.table_view.setColumnWidth(9, 80)  # Finito
        self.table_view.setColumnWidth(10, 130)  # Commessa (aumentato da 100 a 130)

    def keyPressEvent(self, event):
        """Gestisce gli eventi da tastiera, incluso Ctrl+C per la copia dei dati."""
        if event.matches(QKeySequence.StandardKey.Copy):
            self._copy_selection()
        else:
            super().keyPressEvent(event)

    def _copy_selection(self):
        """Copia le celle selezionate negli appunti in formato TSV."""
        selection_model = self.table_view.selectionModel()
        if selection_model is None:
            raise RuntimeError("Table view selection model is None")
        if not (indexes := selection_model.selectedIndexes()):
            return

        indexes.sort(key=lambda x: (x.row(), x.column()))
        rows_text: dict[int, list[tuple[int, str]]] = {}
        for idx in indexes:
            r = idx.row()
            c = idx.column()
            model = self.table_view.model()
            if model is None:
                raise RuntimeError("Table view model is None")
            data = model.data(idx, Qt.ItemDataRole.DisplayRole)
            if r not in rows_text:
                rows_text[r] = []
            rows_text[r].append((c, str(data)))

        tsv_lines = []
        for r in sorted(rows_text.keys()):
            line = "\t".join([x[1] for x in sorted(rows_text[r], key=operator.itemgetter(0))])
            tsv_lines.append(line)

        clipboard = QApplication.clipboard()
        if clipboard is None:
            raise RuntimeError("System clipboard is None")
        clipboard.setText("\n".join(tsv_lines))
