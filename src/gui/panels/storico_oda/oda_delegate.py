"""Modulo Oda Delegate.

Delegate personalizzato per il QTreeView degli Ordini di Acquisto.
Gestisce la colorazione per stato, il merge testuale delle righe figlie,
e l'overlay shimmer animato sui parent al momento dell'espansione.
"""

import math
import operator
from typing import cast

from PySide6.QtCore import QModelIndex, QPersistentModelIndex, Qt
from PySide6.QtGui import QBrush, QColor, QLinearGradient, QPainter
from PySide6.QtWidgets import QStyle, QStyledItemDelegate, QStyleOptionViewItem, QTreeView

from src.gui.styles import COLORS

# ── Parametri shimmer ────────────────────────────────────────────────────────
# Blu saturo su sfondo chiaro: visibile e non aggressivo
_SH_R: int = 41
_SH_G: int = 182
_SH_B: int = 246  # Material Light Blue 400 (#29B6F6)
_SH_PEAK_ALPHA: int = 140  # alpha al picco: 140/255 ≈ 55%, ben visibile
_SH_SPREAD: float = 0.40  # ampiezza onda come frazione della larghezza riga


class ChildDescriptionDelegate(QStyledItemDelegate):
    """Delegate per gestire lo stile delle righe nel QTreeView degli OdA.

    Inizializza il delegate associandolo alla vista ad albero degli OdA.
    """

    def __init__(self, tree_view: QTreeView) -> None:
        """Inizializza il delegate con riferimento al tree view.

        Args:
            tree_view: La vista ad albero a cui il delegate è associato.
        """
        super().__init__(tree_view)
        self.tree = tree_view

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex
    ) -> None:
        """Personalizza il disegno delle celle applicando colori di stato e shimmer.

        Args:
            painter: Il painter Qt corrente.
            option: Le opzioni di stile per la cella.
            index: L'indice del modello per la cella da disegnare.
        """
        if not index.parent().isValid():
            # 1. Sfondo stato (errore/warning)
            self._paint_parent_bg(painter, option, index)
            # 2. Contenuto standard (testo, icone, selezione)
            super().paint(painter, option, index)
            # 3. Overlay shimmer SOPRA il testo con SourceOver semi-trasparente
            self._paint_shimmer(painter, option, index)
            return

        # Righe figlie: merge colonne 0+1
        if index.parent().isValid() and self._paint_child_row(painter, option, index):
            return

        super().paint(painter, option, index)

    # ── Parent row ────────────────────────────────────────────────────────────

    def _paint_parent_bg(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex
    ) -> None:
        """Applica la colorazione di sfondo per le righe principali in base allo stato OdA.

        Args:
            painter: Il painter Qt corrente.
            option: Le opzioni di stile per la cella.
            index: L'indice del modello per la riga parent.
        """
        model = self.tree.model()
        if not hasattr(model, "item"):
            return

        from PySide6.QtGui import QStandardItemModel

        std_model = cast("QStandardItemModel", model)
        data_item = std_model.item(index.row(), 0)
        if not data_item:
            return

        full_data = data_item.data(Qt.ItemDataRole.UserRole)
        if not full_data:
            return

        stato = str(full_data[4]) if len(full_data) > 4 else ""
        ind_rilascio = str(full_data[24]) if len(full_data) > 24 else ""

        if "Cancellato" in stato.lower():
            painter.fillRect(option.rect, QColor(COLORS["bg_error_pastel"]))
        elif "in attesa" in ind_rilascio.lower():
            painter.fillRect(option.rect, QColor(COLORS["bg_warning_pastel"]))

    # ── Shimmer overlay ───────────────────────────────────────────────────────

    def _paint_shimmer(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex
    ) -> None:
        """Sovrappone l'onda shimmer animata sulla riga padre appena espansa.

        Confronta per riga (row + parent), non per cella, così l'onda copre
        tutte le colonne della riga. Alpha modulata da ``sin(π·t)`` per un
        effetto ingresso/uscita morbido. Usa ``SourceOver`` con alpha ~140
        ben visibile su sfondi chiari.

        Args:
            painter: Il painter Qt corrente.
            option: Le opzioni di stile per la cella.
            index: L'indice del modello per la cella parent da decorare.
        """
        anim_idx: QPersistentModelIndex | None = getattr(self.tree, "_anim_index", None)
        progress: float = getattr(self.tree, "_anim_progress", 0.0)

        if anim_idx is None or not anim_idx.isValid():
            return

        # Confronto per RIGA (non per cella): l'onda deve coprire tutte le colonne
        if anim_idx.row() != index.row() or anim_idx.parent() != index.parent():
            return

        # Curva alpha: sin(π·t) → sale a 0→peak→0 nel tempo 0→1
        alpha = int(math.sin(math.pi * progress) * _SH_PEAK_ALPHA)
        if alpha <= 0:
            return

        # Centro dell'onda che scorre da sinistra a destra:
        # parte da -_SH_SPREAD (invisibile a sx) e arriva a 1+_SH_SPREAD (invisibile a dx)
        wave_center = -_SH_SPREAD + progress * (1.0 + _SH_SPREAD * 2.0)

        rect = option.rect
        gradient = QLinearGradient(float(rect.left()), 0.0, float(rect.right()), 0.0)

        transparent = QColor(_SH_R, _SH_G, _SH_B, 0)
        peak_color = QColor(_SH_R, _SH_G, _SH_B, alpha)

        # 5 fermate: bordi trasparenti + onda con sfumatura
        raw_stops: list[tuple[float, QColor]] = [
            (0.0, transparent),
            (max(0.0, min(1.0, wave_center - _SH_SPREAD)), transparent),
            (max(0.0, min(1.0, wave_center)), peak_color),
            (max(0.0, min(1.0, wave_center + _SH_SPREAD)), transparent),
            (1.0, transparent),
        ]

        # Deduplicazione posizioni (Qt richiede valori strettamente in [0,1])
        seen: set[int] = set()
        for pos, color in sorted(raw_stops, key=operator.itemgetter(0)):
            key = int(pos * 100_000)
            if key not in seen:
                gradient.setColorAt(pos, color)
                seen.add(key)

        painter.save()
        # SourceOver: compositing standard, l'onda si sovrappone con il suo alpha
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
        painter.setClipRect(option.rect)
        painter.fillRect(option.rect, QBrush(gradient))
        painter.restore()

    # ── Child row ─────────────────────────────────────────────────────────────

    def _paint_child_row(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex
    ) -> bool:
        """Gestisce il disegno delle righe figlie con merge delle prime due colonne.

        Args:
            painter: Il painter Qt corrente.
            option: Le opzioni di stile per la cella.
            index: L'indice del modello per la cella figlia.

        Returns:
            ``True`` se la cella è stata gestita dal delegate, ``False`` altrimenti.
        """
        col = index.column()
        if col not in (0, 1):
            return False

        if col == 1:
            sibling0 = index.sibling(index.row(), 0)
            text = str(sibling0.data())
            width_col0 = self.tree.columnWidth(0)

            try:
                if option.state & QStyle.StateFlag.State_Selected:
                    painter.setPen(option.palette.highlightedText().color())
                else:
                    painter.setPen(QColor(COLORS["primary_dark"]))

                draw_rect = option.rect.adjusted(-width_col0, 0, 0, 0)
                painter.setClipRect(draw_rect)
                padded_rect = draw_rect.adjusted(5, 0, 0, 0)

                painter.drawText(
                    padded_rect,
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                    text,
                )
            finally:
                painter.setClipping(False)

        return True
