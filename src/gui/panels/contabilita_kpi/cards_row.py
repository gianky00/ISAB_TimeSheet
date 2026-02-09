from PyQt6.QtWidgets import QHBoxLayout, QWidget

from src.gui.widgets.info_widgets import KPIBigCard


class KPICardsRow(QWidget):
    """Widget che raggruppa una riga di KPI cards."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)
        self.cards: list[KPIBigCard] = []

    def add_card(self, title: str, value: str, color: str, subtitle: str | None = None) -> KPIBigCard:
        card = KPIBigCard(title, value, color, subtitle=subtitle)
        self.main_layout.addWidget(card)
        self.cards.append(card)
        return card
