"""SyncroJob - ODA Tree Widget.

Widget specializzato per la visualizzazione gerarchica degli Ordini di Acquisto.
Supporta animazione shimmer sui parent al momento dell'espansione.
"""

import time

from PySide6.QtCore import QAbstractItemModel, QModelIndex, QPersistentModelIndex, Qt, QTimer, Signal
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTreeView, QWidget

from src.gui.panels.storico_oda.oda_delegate import ChildDescriptionDelegate
from src.gui.styles import COLORS

# Costanti animazione
_ANIM_INTERVAL_MS: int = 15  # ~66 fps
_ANIM_DURATION_MS: float = 600.0  # durata totale shimmer in ms


class ODATreeView(QTreeView):
    """Vista gerarchica per Storico OdA con supporto Master-Detail e shimmer animato.

    Espone ``_anim_index`` (normalizzato a col 0) e ``_anim_progress`` letti
    dal delegate per il rendering dello shimmer.

    La larghezza delle colonne è gestita tramite l'override di
    ``sizeHintForColumn`` che considera solo le righe padre: in questo modo
    ``ResizeToContents`` funziona perfettamente senza mai ridimensionare
    durante l'espansione dei figli (i figli non influenzano l'hint).
    """

    selection_changed_custom = Signal()
    row_double_clicked = Signal()
    context_menu_requested = Signal(object)  # pos

    def __init__(self, model: QAbstractItemModel, parent: QWidget | None = None) -> None:
        """Inizializza il tree view con modello dati e sistema di animazione shimmer.

        Args:
            model: Il modello dati da visualizzare.
            parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self.setModel(model)

        # ── Stato animazione shimmer (letti dal delegate) ────────────────────
        self._anim_index: QPersistentModelIndex | None = None
        self._anim_progress: float = 0.0  # 0.0 = inizio, 1.0 = fine
        self._anim_start_ms: float = 0.0

        self._anim_timer: QTimer = QTimer(self)
        self._anim_timer.setInterval(_ANIM_INTERVAL_MS)
        self._anim_timer.timeout.connect(self._on_anim_tick)

        self._setup_ui()

    # ── Sizing ────────────────────────────────────────────────────────────────

    def sizeHintForColumn(self, column: int) -> int:
        """Calcola la larghezza ottimale considerando SOLO le righe padre (root).

        Override di ``QTreeView.sizeHintForColumn`` che di default itera tutte
        le righe visibili, incluse quelle figlie. Quando una riga padre viene
        espansa, Qt richiama questo metodo: poiché le righe figlie sono ignorate,
        il valore restituito non cambia → nessun resize → nessun jump visivo.
        Al tempo stesso le colonne si autodimensionano al contenuto dei parent
        grazie a ``ResizeToContents``.

        Args:
            column: Indice della colonna di cui calcolare la larghezza.

        Returns:
            Larghezza in pixel sufficiente a contenere tutti i valori delle righe root.
        """
        model = self.model()
        h = self.header()
        if not model or not h:
            return super().sizeHintForColumn(column)

        fm = self.fontMetrics()

        # Gestione padding dinamico:
        # Più respiro alle prime colonne (0, 1, 2)
        if column in (0, 1, 2):
            pad = 55
        elif column == 3:
            pad = 35
        else:
            pad = 28

        # Parte dalla larghezza minima di sezione
        min_section = max(h.minimumSectionSize(), 40)

        # Considera anche il testo dell'header
        hdr = model.headerData(column, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
        max_w = (fm.horizontalAdvance(str(hdr)) + pad) if hdr is not None else min_section
        max_w = max(max_w, min_section)

        # Itera solo le righe root — i figli non vengono mai considerati
        for row in range(model.rowCount()):
            idx = model.index(row, column)
            val = model.data(idx, Qt.ItemDataRole.DisplayRole)
            if val is not None:
                max_w = max(max_w, fm.horizontalAdvance(str(val)) + pad)

        return max_w

    # ── Setup ─────────────────────────────────────────────────────────────────

    def _setup_ui(self) -> None:
        """Configura le opzioni visive e i segnali del tree view."""
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setUniformRowHeights(True)
        self.setIndentation(25)
        self.setAnimated(True)
        self.setExpandsOnDoubleClick(False)

        self.setItemDelegate(ChildDescriptionDelegate(self))

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu_requested.emit)

        self.doubleClicked.connect(self._on_double_clicked)

        # Il segnale 'expanded' è emesso da Qt per QUALSIASI tipo di espansione
        self.expanded.connect(self._on_expanded)

        if sel_model := self.selectionModel():
            sel_model.selectionChanged.connect(lambda _1, _2: self.selection_changed_custom.emit())

        self._apply_stylesheet()

    def configure_headers(self) -> None:
        """Configura le modalità di ridimensionamento degli header.

        Usa ``ResizeToContents`` per le colonne a contenuto variabile: Qt
        chiamerà ``sizeHintForColumn`` (override root-only) per calcolare
        la larghezza — stabile all'espansione dei figli, sempre corretta
        al caricamento dei dati. Zero jumps, zero troncamenti.
        """
        h = self.header()
        if not h:
            return

        # ResizeToContents + sizeHintForColumn override (root-only):
        # le colonne si adattano automaticamente ma non cambiano mai
        # durante l'espansione dei figli → fluido e senza troncamenti.
        h.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Data OdA
        h.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # OdA
        h.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Pos
        h.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # CREATO DA
        h.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Descrizione
        h.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Valore Netto
        h.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Stato
        h.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)  # Ind. Rilascio

    # ── Animazione shimmer ────────────────────────────────────────────────────

    def _on_expanded(self, index: QModelIndex) -> None:
        """Avvia lo shimmer e lo scroll minimale al momento dell'espansione.

        Args:
            index: Indice del modello della riga espansa.
        """
        self.scrollTo(index, QAbstractItemView.ScrollHint.EnsureVisible)
        self._start_shimmer(index)

    def _start_shimmer(self, index: QModelIndex) -> None:
        """Avvia (o riavvia) il ciclo di animazione shimmer per la riga indicata.

        Normalizza l'indice alla colonna 0 così il delegate può confrontarlo
        per riga indipendentemente dalla colonna selezionata.

        Args:
            index: Indice del modello (qualsiasi colonna) della riga da animare.
        """
        col0 = index.sibling(index.row(), 0)
        self._anim_index = QPersistentModelIndex(col0)
        self._anim_progress = 0.0
        self._anim_start_ms = time.monotonic() * 1000.0
        if not self._anim_timer.isActive():
            self._anim_timer.start()

    def _on_anim_tick(self) -> None:
        """Aggiorna il progresso dell'animazione a ogni tick del timer e forza il repaint."""
        elapsed = time.monotonic() * 1000.0 - self._anim_start_ms
        t = min(1.0, elapsed / _ANIM_DURATION_MS)
        self._anim_progress = t

        if t >= 1.0:
            self._anim_timer.stop()
            self._anim_index = None
            self._anim_progress = 0.0

        if vp := self.viewport():
            vp.update()

    # ── Gestione eventi ───────────────────────────────────────────────────────

    def _on_double_clicked(self, index: QModelIndex) -> None:
        """Espande o comprime la riga al doppio click su qualsiasi colonna."""
        if not index.isValid():
            return
        if not index.parent().isValid():
            if self.isExpanded(index):
                self.collapse(index)
            else:
                self.expand(index)
        self.row_double_clicked.emit()

    # ── Stile ─────────────────────────────────────────────────────────────────

    def _apply_stylesheet(self) -> None:
        """Applica lo stylesheet del tree con selection-color scuro per leggibilità."""
        self.setStyleSheet(f"""
      QTreeView {{
        gridline-color: {COLORS["bg_alt"]};
        selection-background-color: {COLORS["table_selection_bg"]};
        selection-color: {COLORS["text_dark"]};
        border: 1px solid {COLORS["border_light"]};
        border-radius: 8px;
        background-color: {COLORS["bg_white"]};
      }}
      QHeaderView::section {{
        background-color: {COLORS["bg_light"]};
        color: {COLORS["text_dark"]};
        padding: 10px;
        font-weight: bold;
        border: none;
        border-bottom: 1px solid {COLORS["border_light"]};
      }}
    """)
