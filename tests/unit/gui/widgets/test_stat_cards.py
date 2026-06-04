from PySide6.QtCore import Qt

from src.application.services.constants import Icons
from src.gui.widgets.dashboard_stat_card import DashboardStatCard
from src.gui.widgets.status_card import StatusCard


class TestStatCards:
    def test_status_card_flow(self, qtbot):
        card = StatusCard("Bot TS", "Pronto")
        qtbot.addWidget(card)
        card.show()

        assert card._title_label.text() == "Bot TS"
        assert card._status_label.text() == "Pronto"

        # Change status
        card.setStatus("Esecuzione...", status_id="#FF0000")
        assert card._status_label.text() == "Esecuzione..."
        assert "#FF0000" in card._icon_bar.styleSheet()

        # Autopilot
        card.setAutopilot(True, "ON")
        qtbot.wait_until(lambda: card._meta_label.isVisible())
        assert card._meta_label.text() == "ON"

        card.setAutopilot(False)
        qtbot.wait_until(lambda: not card._meta_label.isVisible())

    def test_status_card_click(self, qtbot):
        card = StatusCard("Test")
        qtbot.addWidget(card)
        card.show()

        with qtbot.wait_signal(card.clicked):
            qtbot.mouseClick(card, Qt.MouseButton.LeftButton)

    def test_dashboard_stat_card(self, qtbot):
        card = DashboardStatCard("Ore Totali", "150", Icons.CLOCK, color="#00FF00")
        qtbot.addWidget(card)
        card.show()

        assert card.val_lbl.text() == "150"
        assert "ORE TOTALI" in card.title_lbl.text()

        # Update
        card.update_value("200", details="Ultimo mese", meta="+10%")
        qtbot.wait_until(lambda: card.detail_lbl.isVisible())
        qtbot.wait_until(lambda: card.meta_lbl.isVisible())
        assert card.val_lbl.text() == "200"

        card.update_value("200")  # Clear extras
        qtbot.wait_until(lambda: not card.detail_lbl.isVisible())
        qtbot.wait_until(lambda: not card.meta_lbl.isVisible())
