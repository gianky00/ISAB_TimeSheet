from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QStyle, QStyledItemDelegate


class ChildDescriptionDelegate(QStyledItemDelegate):
    """Delegate per gestire lo stile delle righe figlie nel QTreeView degli OdA."""

    def __init__(self, tree_view):
        super().__init__(tree_view)
        self.tree = tree_view

    def paint(self, painter, option, index):
        # Verifica se siamo in una riga figlia (ha un genitore valido)
        if index.parent().isValid():
            col = index.column()

            # --- GESTIONE MERGE COL 0 e COL 1 (Testo Breve) ---
            if col == 0 or col == 1:
                # Disegna il testo SOLO quando siamo sulla Col 1 (disegnando verso sinistra)
                if col == 1:
                    # Recupera dati dalla Col 0 (dove sta il testo vero)
                    sibling0 = index.sibling(index.row(), 0)
                    text = sibling0.data()

                    width_col0 = self.tree.columnWidth(0)

                    try:
                        if option.state & QStyle.StateFlag.State_Selected:
                            painter.setPen(option.palette.highlightedText().color())
                        else:
                            painter.setPen(Qt.GlobalColor.darkBlue)

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
