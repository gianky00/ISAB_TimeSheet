"""Unit tests for Info Widgets."""

from unittest.mock import MagicMock

from PySide6.QtCore import Qt

from src.gui.widgets.info_widgets import DetailedInfoDialog, InfoLabel, KPIBigCard


class TestDetailedInfoDialog:
    """Test suite per DetailedInfoDialog."""

    def test_initialization(self, qtbot):
        dialog = DetailedInfoDialog("Test Title", "Test Content")
        qtbot.addWidget(dialog)

        # Cerchiamo le label nel layout
        from PySide6.QtWidgets import QLabel

        labels = dialog.findChildren(QLabel)
        assert any("Test Title" in lbl.text() for lbl in labels)
        assert any("Test Content" in lbl.text() for lbl in labels)

    def test_mouse_click_closes(self, qtbot):
        dialog = DetailedInfoDialog("Title", "Content")
        qtbot.addWidget(dialog)

        # Simuliamo click
        with qtbot.waitSignal(dialog.accepted):
            qtbot.mouseClick(dialog, Qt.MouseButton.LeftButton)


class TestInfoLabel:
    """Test suite per InfoLabel."""

    def test_initialization(self, qtbot):
        btn = InfoLabel("Test help", "Test text")
        qtbot.addWidget(btn)
        assert btn.title == "Test help"

    def test_show_info_dialog(self, qtbot, mocker):
        # Mocking DetailedInfoDialog.exec per evitare blocco UI
        mock_exec = mocker.patch("src.gui.widgets.info_widgets.DetailedInfoDialog.exec")

        btn = InfoLabel("Help", "Content")
        qtbot.addWidget(btn)

        qtbot.mouseClick(btn, Qt.MouseButton.LeftButton)
        assert mock_exec.called


class TestKPIBigCard:
    """Test suite per KPIBigCard."""

    def test_initialization(self, qtbot):
        card = KPIBigCard("My KPI", "123.45", color="#ff0000", subtitle="Unit")
        qtbot.addWidget(card)

        assert card.lbl_value.text() == "123.45"
        # Verifica titolo cercandolo nelle label
        from PySide6.QtWidgets import QLabel

        labels = card.findChildren(QLabel)
        assert any("My KPI" in lbl.text() for lbl in labels)
        assert any("Unit" in lbl.text() for lbl in labels)

    def test_info_callback(self, qtbot, mocker):
        card = KPIBigCard("Title", "1")
        qtbot.addWidget(card)

        mock_cb = MagicMock(return_value="Dynamic Info")
        card.set_info_callback(mock_cb)

        # Trigger help click
        mock_exec = mocker.patch("src.gui.widgets.info_widgets.DetailedInfoDialog.exec")
        qtbot.mouseClick(card.info_icon, Qt.MouseButton.LeftButton)

        assert mock_cb.called
        assert mock_exec.called
