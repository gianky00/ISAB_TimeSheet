"""Unit tests for AutomazioniWidget."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtWidgets import QWidget

from src.gui.widgets.automazioni_widget import AutomazioniWidget


@pytest.fixture
def mock_main_window():
    """Mock per MainWindow."""
    mw = MagicMock()
    mw.bot_controller = MagicMock()
    return mw


class TestAutomazioniWidget:
    """Test suite per AutomazioniWidget."""

    @pytest.fixture(autouse=True)
    def mock_panels(self, mocker):
        """Mock di tutti i pannelli per evitare inizializzazioni pesanti."""
        mocker.patch("src.gui.widgets.automazioni_widget.CaricoTSPanel", return_value=QWidget())
        mocker.patch("src.gui.widgets.automazioni_widget.DettagliOdAPanel", return_value=QWidget())
        mocker.patch("src.gui.widgets.automazioni_widget.PrenotaBPPanel", return_value=QWidget())
        mocker.patch("src.gui.widgets.automazioni_widget.RicercaPDLPanel", return_value=QWidget())
        mocker.patch("src.gui.widgets.automazioni_widget.ScaricaTSPanel", return_value=QWidget())
        mocker.patch("src.gui.widgets.automazioni_widget.ScaricoPDLPanel", return_value=QWidget())
        mocker.patch("src.gui.widgets.automazioni_widget.TimbratureBotPanel", return_value=QWidget())

    def test_initialization(self, qtbot, mock_main_window):
        """Verifica lbl'inizializzazione del widget."""
        widget = AutomazioniWidget(mock_main_window)
        qtbot.addWidget(widget)

        assert widget.main_tabs.count() == 2
        assert widget.tab_fornitori.count() == 5

        assert mock_main_window.carico_panel is not None
        assert mock_main_window.bot_controller.register_panels.called

    def test_set_current_tab(self, qtbot, mock_main_window):
        """Verifica la navigazione tra tab interni."""
        widget = AutomazioniWidget(mock_main_window)
        qtbot.addWidget(widget)

        widget.set_current_tab(sub_index=1, bot_index=1)
        assert widget.main_tabs.currentIndex() == 1
        assert widget.tab_safework.currentIndex() == 1

    def test_get_bot_panel(self, qtbot, mock_main_window):
        """Verifica il recupero di un pannello specifico."""
        widget = AutomazioniWidget(mock_main_window)
        qtbot.addWidget(widget)

        panel = widget.get_bot_panel(0, 2)
        assert panel == widget.panel_timbrature
