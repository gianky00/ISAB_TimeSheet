from typing import cast

from PySide6.QtCore import QModelIndex, QPersistentModelIndex, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QStyle, QStyledItemDelegate, QStyleOptionViewItem, QTreeView

from src.gui.styles import COLORS


class ChildDescriptionDelegate(QStyledItemDelegate):
    """Delegate per gestire lo stile delle righe figlie nel QTreeView degli OdA."""

    def __init__(self, tree_view: QTreeView) -> None:
        """Inizializza il delegate associandolo alla vista ad albero degli OdA."""
        super().__init__(tree_view)
        self.tree = tree_view

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex | QPersistentModelIndex
    ) -> None:
        """Personalizza il disegno delle celle, applicando colori di stato e merge testuale per le rilascio."""
        # 1. Applica colorazione per righe parent in base a STATO e Indicatore Rilascio
        if not index.parent().isValid():  # Riga parent
            # Recupera i dati completi dalla colonna 0
            model = self.tree.model()
            if hasattr(model, "item"):
                from PySide6.QtGui import QStandardItemModel

                std_model = cast("QStandardItemModel", model)
                data_item = std_model.item(index.row(), 0)
                if data_item:
                    full_data = data_item.data(Qt.ItemDataRole.UserRole)
                    if full_data:
                        stato = str(full_data[4]) if len(full_data) > 4 else ""
                        ind_rilascio = str(full_data[24]) if len(full_data) > 24 else ""

                        # Logica colorazione
                        if "Cancellato" in stato or "cancellato" in stato:
                            # ❌ ROSSO per stato Cancellato
                            painter.fillRect(option.rect, QColor(COLORS["bg_error_pastel"]))
                        elif "In attesa di Rilascio" in ind_rilascio or "in attesa" in ind_rilascio.lower():
                            # [ARANCIONE] ARANCIONE per In attesa di Rilascio
                            painter.fillRect(option.rect, QColor(COLORS["bg_warning_pastel"]))

        # 2. Verifica se siamo in una riga figlia (ha un genitore valido)
        if index.parent().isValid():
            col = index.column()

            # --- GESTIONE MERGE COL 0 e COL 1 (Testo Breve) ---
            if col in (0, 1):
                # Disegna il testo SOLO quando siamo sulla Col 1 (disegnando verso sinistra)
                if col == 1:
                    # Recupera dati dalla Col 0 (dove sta il testo vero)
                    sibling0 = index.sibling(index.row(), 0)
                    text = str(sibling0.data())

                    width_col0 = self.tree.columnWidth(0)

                    try:
                        if option.state & QStyle.StateFlag.State_Selected:
                            painter.setPen(option.palette.highlightedText().color())
                        else:
                            painter.setPen(QColor(COLORS["primary_dark"]))

                        # Rettangolo Totale: Inizia a sinistra di Col 1 (inizio Col 0) ed estende per W0 + W1
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

                # Ritorna per evitare doppio disegno del testo sulla Col 0 o Col 1
                return

        super().paint(painter, option, index)
