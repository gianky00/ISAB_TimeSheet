"""
SyncroJob - Scarico Ore Panel
Interfaccia ad alte prestazioni per la consultazione e la gestione dello Scarico Ore Cantiere (DataEase).
Utilizza una QTableView con modello virtuale per gestire fluidamente oltre 130.000 righe di dati.
Include filtri avanzati per colonna (Excel-style), ricerca full-text e calcolo dinamico delle somme ore.
"""

import operator
import time
from contextlib import suppress
from datetime import datetime

from PyQt6.QtCore import QItemSelection, Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.constants import Icons
from src.core.contabilita_manager import ContabilitaManager
from src.gui.components.animated_tab_widget import AnimatedTabWidget
from src.gui.components.scarico_ore import FilterHeaderView, ScaricoOreTableModel
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.styles import COLORS
from src.gui.widgets import ModernButton, ShimmerSkeleton
from src.gui.widgets.modern_card import ModernCard
from src.utils.helpers import get_asset_path, get_colored_icon


class ScaricoOreWorker(QThread):
    """
    Thread dedicato all'importazione asincrona dei dati di scarico ore.
    Esegue il parsing dei file sorgente, la sincronizzazione con il database SQLite locale
    e comunica i progressi calcolando l'ETA stimato.
    """

    finished_signal = pyqtSignal(bool, str, int, int, float)
    """Segnale emesso al termine dell'operazione (successo, msg, aggiunti, rimossi, durata)."""

    progress_signal = pyqtSignal(str)
    """Segnale emesso per aggiornare la UI sullo stato di avanzamento testuale."""

    def __init__(self, file_path: str) -> None:
        """
        Inizializza il worker per l'importazione.

        Args:
            file_path: Percorso assoluto del file sorgente da importare.
        """
        super().__init__()
        self.file_path = file_path
        self.start_time: float = 0.0

    def run(self) -> None:
        """Logica di esecuzione del thread: inizializza il DB, calcola il totale righe e avvia l'importazione."""
        ContabilitaManager.init_db()
        self.start_time = time.time()
        try:
            total_rows = ContabilitaManager.scan_scarico_ore_rows(self.file_path)
        except Exception:
            total_rows = 1000

        def progress_cb(current, total):
            """Callback per l'aggiornamento del progresso con calcolo ETA."""
            real_total = max(total if total > 0 else total_rows, current)
            elapsed = time.time() - self.start_time
            if current > 0 and elapsed > 0:
                rate = current / elapsed
                remaining = real_total - current
                eta_sec = remaining / rate if rate > 0 else 0
                m, s = divmod(int(eta_sec), 60)
                percent = min(int((current / real_total) * 100), 99)
                self.progress_signal.emit(
                    f"Importazione: {percent}% completato ({current}/{real_total}) • ETA: {m}m {s}s"
                )

        success, msg, added, removed = ContabilitaManager.import_scarico_ore(
            self.file_path, progress_callback=progress_cb
        )
        self.finished_signal.emit(success, msg, added, removed, time.time() - self.start_time)

    def stop(self) -> None:
        """Richiede l'interruzione sicura del thread e attende la chiusura."""
        self.requestInterruption()
        self.quit()
        self.wait()


class ScaricoOrePanel(QWidget):
    """
    Widget principale per la visualizzazione dello scarico ore.
    Coordina la visualizzazione tabellare, l'applicazione dei filtri persistenti e la conservazione
    della selezione durante il riordino delle colonne.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """Costruisce la UI e avvia il caricamento differito della cache per non bloccare lo startup."""
        super().__init__(parent)
        self.worker: ScaricoOreWorker | None = None
        self._current_col_filters: dict[int, set[str]] = {}
        self._last_update_status: str | None = None
        self._saved_selection_real_ids: set[int] = set()
        self._setup_ui()
        self.search_input.setPlaceholderText("Inizializzazione dati... attendere")
        self.search_input.setEnabled(False)
        QTimer.singleShot(50, self._load_data)

    def _setup_ui(self) -> None:
        """Configura la toolbar superiore con statistiche e ricerca, e la vista tabellare virtuale."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # --- TOOLBAR (Design Modern Card) ---
        self.toolbar_card = ModernCard(elevation=10)
        self.toolbar_card.setObjectName("filterBar")
        
        toolbar_layout = QHBoxLayout(self.toolbar_card)
        toolbar_layout.setContentsMargins(15, 10, 15, 10)
        toolbar_layout.setSpacing(15)

        from src.gui.styles import LABEL_MUTED, LINEEDIT_STYLE

        # Sezione Statistiche
        stats_h = QHBoxLayout()
        stats_h.setSpacing(20)

        count_v = QVBoxLayout()
        count_v.setSpacing(4)
        lbl_count_title = QLabel("RIGHE VISIBILI")
        lbl_count_title.setStyleSheet(LABEL_MUTED)
        self.lbl_count = QLabel("0")
        self.lbl_count.setStyleSheet(f"color: {COLORS['text_dark']}; font-weight: 700; font-size: 14px;")
        count_v.addWidget(lbl_count_title)
        count_v.addWidget(self.lbl_count)
        stats_h.addLayout(count_v)

        sel_v = QVBoxLayout()
        sel_v.setSpacing(4)
        lbl_sel_title = QLabel("SELEZIONATO")
        lbl_sel_title.setStyleSheet(LABEL_MUTED)
        self.lbl_selection_total = QLabel("0")
        self.lbl_selection_total.setStyleSheet(f"color: {COLORS['primary_blue']}; font-weight: 700; font-size: 14px;")
        sel_v.addWidget(lbl_sel_title)
        sel_v.addWidget(self.lbl_selection_total)
        stats_h.addLayout(sel_v)

        hours_v = QVBoxLayout()
        hours_v.setSpacing(4)
        lbl_hours_title = QLabel("TOTALE ORE")
        lbl_hours_title.setStyleSheet(LABEL_MUTED)
        self.lbl_total_hours = QLabel("0")
        self.lbl_total_hours.setStyleSheet(f"color: {COLORS['teal_accent']}; font-weight: 800; font-size: 14px;")
        hours_v.addWidget(lbl_hours_title)
        hours_v.addWidget(self.lbl_total_hours)
        stats_h.addLayout(hours_v)

        toolbar_layout.addLayout(stats_h)

        # Divisore
        v_line = QFrame()
        v_line.setFrameShape(QFrame.Shape.VLine)
        v_line.setFrameShadow(QFrame.Shadow.Plain)
        v_line.setStyleSheet(f"color: {COLORS['border_light']};")
        toolbar_layout.addWidget(v_line)

        # Sezione Ricerca
        search_v = QVBoxLayout()
        search_v.setSpacing(4)
        lbl_search = QLabel("CERCA PERSONALE / ODA")
        lbl_search.setStyleSheet(LABEL_MUTED)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filtra dati (Premi Invio)...")
        self.search_input.setMinimumWidth(300)
        self.search_input.setStyleSheet(LINEEDIT_STYLE)
        self.search_input.returnPressed.connect(self._perform_search)
        search_v.addWidget(lbl_search)
        search_v.addWidget(self.search_input)
        toolbar_layout.addLayout(search_v)

        toolbar_layout.addStretch()

        # Info & Actions
        info_v = QVBoxLayout()
        info_v.setSpacing(4)
        info_v.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.status_label = QLabel("Inizializzazione...")
        self.status_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
        self.status_label.setTextFormat(Qt.TextFormat.RichText)

        self.update_btn = ModernButton(
            "SINCRONIZZA",
            variant=ModernButton.Variant.PRIMARY,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.REFRESH),
        )
        self.update_btn.clicked.connect(self._start_update)

        info_v.addWidget(self.status_label)
        info_v.addWidget(self.update_btn)
        toolbar_layout.addLayout(info_v)

        layout.addWidget(self.toolbar_card)

        self.tabs = AnimatedTabWidget()
        self.scarico_tab = QWidget()
        scarico_layout = QVBoxLayout(self.scarico_tab)
        self.table_view = QTableView()
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setSortingEnabled(True)
        self.source_model = ScaricoOreTableModel([])
        self.source_model.cache_loaded.connect(self._on_cache_loaded)
        self.source_model.loading_progress.connect(self._on_loading_progress)
        self.table_view.setModel(self.source_model)

        header = FilterHeaderView(Qt.Orientation.Horizontal, self.table_view)
        self.table_view.setHorizontalHeader(header)
        header.filterChanged.connect(self._on_header_filter_changed)

        scarico_layout.addWidget(self.table_view)

        # --- SHIMMER LOADING ---
        self.shimmer = ShimmerSkeleton(rows=10)
        self.shimmer.setParent(self.table_view)
        self.shimmer.hide()

        self.tabs.addTab(
            self.scarico_tab, get_colored_icon(get_asset_path(Icons.DOWNLOAD), COLORS["text_muted"]), "Dati Scaricati"
        )
        layout.addWidget(self.tabs)

        if selection_model := self.table_view.selectionModel():
            selection_model.selectionChanged.connect(self._update_selection_totals)

        self.source_model.layoutAboutToBeChanged.connect(self._preserve_selection)
        self.source_model.layoutChanged.connect(self._restore_selection)

    def _preserve_selection(self) -> None:
        """Mappa gli indici visuali selezionati sugli ID riga reali prima di un cambiamento del layout (sort/filter)."""
        self._saved_selection_real_ids.clear()
        if (sel := self.table_view.selectionModel()) and sel.hasSelection():
            for idx in sel.selectedRows():
                if idx.isValid() and idx.row() < len(self.source_model._visible_indices):
                    self._saved_selection_real_ids.add(self.source_model._visible_indices[idx.row()])

    def _restore_selection(self) -> None:
        """Ripristina la selezione riga per riga cercandone la nuova posizione visuale tramite gli ID preservati."""
        if not self._saved_selection_real_ids:
            return
        real_to_vis = {real_id: vis_row for vis_row, real_id in enumerate(self.source_model._visible_indices)}
        new_sel = QItemSelection()
        for rid in self._saved_selection_real_ids:
            if rid in real_to_vis:
                vrow = real_to_vis[rid]
                new_sel.select(
                    self.source_model.index(vrow, 0),
                    self.source_model.index(vrow, self.source_model.columnCount() - 1),
                )
        if not new_sel.isEmpty() and (sel := self.table_view.selectionModel()):
            sel.select(new_sel, sel.SelectionFlag.ClearAndSelect | sel.SelectionFlag.Rows)
            self._update_selection_totals()

    def _format_number(self, value: float) -> str:
        """Converte un float in stringa: intero se possibile, altrimenti con 2 decimali."""
        return str(int(value)) if value % 1 == 0 else f"{value:.2f}"

    def _update_totals(self) -> None:
        """Calcola la somma delle ore per tutte le righe attualmente filtrate e visibili."""
        row_count = self.source_model.rowCount()
        self.lbl_count.setText(f"Righe visibili: {row_count}")
        total = self.source_model.get_float_total_for_visible() if row_count > 0 else 0.0
        self.lbl_total_hours.setText(f"Totale Ore: {self._format_number(total)}")

    def _update_selection_totals(self) -> None:
        """Somma i valori della colonna 'TOTALE ORE' per le sole celle selezionate dall'utente."""
        try:
            if not (sel := self.table_view.selectionModel()) or not (idxs := sel.selectedIndexes()):
                self.lbl_selection_total.setText("Totale selezionato: 0")
                return
            total = 0.0
            for idx in idxs:
                if idx.column() == 7:  # TOTALE ORE
                    with suppress(ValueError):
                        val = str(idx.data(Qt.ItemDataRole.DisplayRole)).replace(",", ".")
                        if val:
                            total += float(val)
            self.lbl_selection_total.setText(f"Totale selezionato: {self._format_number(total)}")
        except Exception as e:
            print(f"Errore selezione: {e}")

    def set_search_query(self, text: str) -> None:
        """Imposta il testo di ricerca globale ed esegue il filtro."""
        self.search_input.setText(text)
        self.search_input.setFocus()
        self.search_input.selectAll()
        self._perform_search()

    def _start_update(self) -> None:
        """Avvia la procedura di sincronizzazione dal file DataEase esterno."""
        path = config_manager.load_config().get("dataease_path", "")
        if not path:
            ConfirmationDialog.show_warning(
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
        self, success: bool, msg: str, added: int = 0, removed: int = 0, duration: float = 0.0
    ) -> None:
        """Gestisce il post-aggiornamento: invalida la cache e ricarica i dati in memoria."""
        self.update_btn.setEnabled(True)
        self.table_view.setEnabled(True)
        if success:
            ts = datetime.now().strftime("%d/%m/%Y %H:%M")
            time_str = (
                f"{duration:.1f}s" if duration < 60 else f"{int(duration // 60)}m {int(duration % 60)}s"
            )
            status = f"{ts} <font color='{COLORS['success_dark']}'><b>+{added}</b></font> <font color='{COLORS['error_red']}'><b>-{removed}</b></font> ({time_str})"
            self.status_label.setText(status)
            self._last_update_status = status
            with suppress(Exception):
                if ScaricoOreTableModel.CACHE_PATH.exists():
                    ScaricoOreTableModel.CACHE_PATH.unlink()
            ScaricoOreTableModel._global_cache["loaded"] = False
            self._load_data()
        else:
            self.status_label.setText("Errore")
            ConfirmationDialog.show_error(self, "Errore Aggiornamento", msg)

    def _perform_search(self) -> None:
        """Applica il filtro testuale globale al modello e ricalcola i totali."""
        self.source_model.set_filter(self.search_input.text(), self._current_col_filters)
        self._update_totals()

    def _on_header_filter_changed(self, col: int, values: list[str]) -> None:
        """Aggiorna i set di filtri per colonna e riapplica il filtraggio completo."""
        if not values:
            self._current_col_filters.pop(col, None)
        else:
            self._current_col_filters[col] = {v.lower() for v in values}
        self._perform_search()

    def _set_ui_loading(self, loading: bool) -> None:
        """Inibisce l'interazione durante le fasi di caricamento dati pesanti."""
        self.search_input.setEnabled(not loading)
        self.update_btn.setEnabled(not loading)
        self.search_input.setPlaceholderText("Caricamento..." if loading else "Filtra dati (Premi Invio)...")
        
        if loading:
            self.table_view.hide()
            self.shimmer.show()
            self.shimmer.resize(self.table_view.size())
        else:
            self.shimmer.hide()
            self.table_view.show()

        self.table_view.setDisabled(loading)
        QApplication.processEvents()

    def resizeEvent(self, event) -> None:
        """Sincronizza shimmer e altri overlay."""
        super().resizeEvent(event)
        if hasattr(self, "shimmer") and self.shimmer.isVisible():
            self.shimmer.resize(self.table_view.size())

    def _on_loading_progress(self, msg: str) -> None:
        """Inoltra i messaggi di progresso dal worker alla label di stato."""
        self.status_label.setText(msg)
        QApplication.processEvents()

    def _on_cache_loaded(self) -> None:
        """Finalizza l'interfaccia una volta che i dati sono popolati: ordina e ridimensiona le colonne."""
        self.status_label.setText(self._last_update_status or "Pronto")
        self._set_ui_loading(False)
        self._resize_columns()
        self.table_view.sortByColumn(0, Qt.SortOrder.DescendingOrder)
        self._update_totals()

    def _load_data(self) -> None:
        """Carica i dati in modalità asincrona, privilegiando la cache binaria se disponibile."""
        if not ContabilitaManager.DB_PATH.exists():
            self.status_label.setText("Database non trovato.")
            return
        self._set_ui_loading(True)
        if ScaricoOreTableModel.CACHE_PATH.exists():
            self.source_model.load_data_async(None)
        else:
            try:
                self.source_model.load_data_async(ContabilitaManager.get_scarico_ore_data())
            except Exception as e:
                self.status_label.setText(f"Errore: {e}")
                self._set_ui_loading(False)

    def _resize_columns(self) -> None:
        """Applica larghezze fisse alle colonne note e stretch alla descrizione per una UX ottimale."""
        h = self.table_view.horizontalHeader()
        if not h:
            return
        h.setMinimumHeight(80)
        h.setStretchLastSection(False)
        for i in range(11):
            h.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)
        widths = [120, 150, 150, 100, 60, 75, 75, 90]
        for i, w in enumerate(widths):
            self.table_view.setColumnWidth(i, w)
        h.setSectionResizeMode(8, QHeaderView.ResizeMode.Stretch)
        self.table_view.setColumnWidth(9, 80)
        self.table_view.setColumnWidth(10, 130)

    def keyPressEvent(self, event) -> None:
        """Intercetta tasti rapidi, come Ctrl+C per la copia dei dati in formato TSV."""
        if event.matches(QKeySequence.StandardKey.Copy):
            self._copy_selection()
        else:
            super().keyPressEvent(event)

    def _copy_selection(self) -> None:
        """Esporta il contenuto delle celle selezionate negli appunti in formato tab-separated."""
        if not (sel := self.table_view.selectionModel()) or not (idxs := sel.selectedIndexes()):
            return
        idxs.sort(key=lambda x: (x.row(), x.column()))
        rows: dict[int, list[tuple[int, str]]] = {}
        for idx in idxs:
            rows.setdefault(idx.row(), []).append((idx.column(), str(idx.data(Qt.ItemDataRole.DisplayRole))))
        lines = [
            "\t".join([x[1] for x in sorted(rows[r], key=operator.itemgetter(0))])
            for r in sorted(rows.keys())
        ]
        if cb := QApplication.clipboard():
            cb.setText("\n".join(lines))
