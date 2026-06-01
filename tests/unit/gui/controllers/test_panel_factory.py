from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtWidgets import QMessageBox, QWidget

from src.gui.controllers.panel_factory import PanelFactory
from src.gui.main_window.page_index import PageIndex


class MockNav:
    def __init__(self):
        self.mw = MagicMock()
        self.scarico_ore_controller = MagicMock()
        self.pdl_controller = MagicMock()
        self.oda_controller = MagicMock()
        self.anagrafica_controller = MagicMock()
        self.consuntivo_controller = MagicMock()


def test_panel_factory_init():
    nav = MockNav()
    factory = PanelFactory(nav)
    assert factory.nav == nav
    assert factory.mw == nav.mw


def test_create_panel_reserved_ai(qtbot):
    nav = MockNav()
    factory = PanelFactory(nav)
    panel = factory.create_panel(PageIndex.RESERVED_AI)
    qtbot.addWidget(panel)
    assert isinstance(panel, QWidget)
    assert type(panel) is QWidget  # Should be a base QWidget


@patch("src.gui.panels.dashboard_panel.DashboardPanel")
def test_create_dashboard(mock_dash, qtbot):
    nav = MockNav()
    factory = PanelFactory(nav)
    widget = QWidget()
    qtbot.addWidget(widget)
    mock_dash.return_value = widget
    panel = factory.create_panel(PageIndex.DASHBOARD)
    assert panel is not None
    mock_dash.assert_called_once()


@patch("src.gui.widgets.automazioni_widget.AutomazioniWidget")
def test_create_automazioni(mock_auto, qtbot):
    nav = MockNav()
    factory = PanelFactory(nav)
    widget = QWidget()
    qtbot.addWidget(widget)
    mock_auto.return_value = widget
    panel = factory.create_panel(PageIndex.AUTOMAZIONI)
    assert panel is not None
    mock_auto.assert_called_once_with(main_window=nav.mw)


def test_create_panel_error(qtbot):
    nav = MockNav()
    factory = PanelFactory(nav)

    # Force an error in _instantiate_panel
    with patch.object(factory, "_instantiate_panel", side_effect=Exception("Test error")):
        with patch.object(QMessageBox, "critical") as mock_crit:
            panel = factory.create_panel(PageIndex.DASHBOARD)
            assert panel is None
            mock_crit.assert_called_once()


@pytest.mark.parametrize(
    "index, creator_method",
    [
        (PageIndex.SETTINGS, "_create_settings"),
        (PageIndex.HELP, "_create_help"),
        (PageIndex.NOTIFICATIONS, "_create_notifications"),
        (PageIndex.CHANGELOG, "_create_changelog"),
    ],
)
def test_creators_simple(index, creator_method, qtbot):
    nav = MockNav()
    factory = PanelFactory(nav)

    with patch.object(factory, creator_method) as mock_creator:
        widget = QWidget()
        qtbot.addWidget(widget)
        mock_creator.return_value = widget
        factory.create_panel(index)
        mock_creator.assert_called_once()
