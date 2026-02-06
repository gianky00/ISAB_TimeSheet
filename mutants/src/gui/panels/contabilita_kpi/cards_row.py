from PyQt6.QtWidgets import QHBoxLayout, QWidget

from src.gui.widgets.info_widgets import KPIBigCard


class KPICardsRow(QWidget):
    """Widget che raggruppa una riga di KPI cards."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(20)
        self.cards = []

    def add_card(self, title, value, color, subtitle=None):
        card = KPIBigCard(title, value, color, subtitle=subtitle)
        self.layout.addWidget(card)
        self.cards.append(card)
        return card
