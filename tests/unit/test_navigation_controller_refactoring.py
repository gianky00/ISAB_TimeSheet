"""
Tests for NavigationController.get_panel refactoring.
Ensures functional parity before refactoring.
"""

from unittest.mock import MagicMock, patch

import pytest


# Define a dummy QObject to avoid PyQt6 dependency and Mock errors
class DummyQObject:
    def __init__(self, parent=None):
        self._parent = parent


# Patch QObject before importing NavigationController
with patch("PyQt6.QtCore.QObject", DummyQObject):
    from src.gui.controllers.navigation_controller import NavigationController


@pytest.fixture
def mock_mw():
    mw = MagicMock()
    mw.page_stack = MagicMock()
    # Mock return values for widgets in stack
    mw.page_stack.widget.return_value = MagicMock()
    return mw


@pytest.fixture
def controller(mock_mw):
    return NavigationController(mock_mw)


def test_get_panel_already_initialized(controller, mock_mw):
    """Test getting a panel that is already initialized."""
    index = 0
    setattr(mock_mw, f"_panel_initialized_{index}", True)
    existing_widget = MagicMock()
    mock_mw.page_stack.widget.return_value = existing_widget

    panel = controller.get_panel(index)

    assert panel == existing_widget
    mock_mw.page_stack.insertWidget.assert_not_called()


@patch("src.gui.panels.DashboardPanel")
def test_get_panel_lazy_load_dashboard(mock_dashboard, controller, mock_mw):
    """Test lazy loading of DashboardPanel (index 0)."""
    index = 0
    setattr(mock_mw, f"_panel_initialized_{index}", False)
    mock_mw.footer_left = MagicMock()

    new_widget = MagicMock()
    mock_dashboard.return_value = new_widget

    panel = controller.get_panel(index)

    assert panel == new_widget
    assert getattr(mock_mw, f"_panel_initialized_{index}") is True
    mock_mw.page_stack.insertWidget.assert_called_with(index, new_widget)


@patch("src.gui.panels.SettingsPanel")
def test_get_panel_lazy_load_settings(mock_settings, controller, mock_mw):
    """Test lazy loading of SettingsPanel (index 7) with signal connection."""
    # SETTINGS è ora indice 7
    index = 7
    setattr(mock_mw, f"_panel_initialized_{index}", False)

    new_widget = MagicMock()
    mock_settings.return_value = new_widget

    panel = controller.get_panel(index)

    assert panel == new_widget
    # Verify signal connections
    new_widget.settings_saved.connect.assert_called_with(mock_mw._on_settings_saved)
    new_widget.request_help_section.connect.assert_called_with(
        mock_mw._on_help_requested
    )


def test_get_panel_exception_handling(controller, mock_mw):
    """Test error handling during panel creation."""
    index = 0
    setattr(mock_mw, f"_panel_initialized_{index}", False)

    with patch(
        "src.gui.panels.DashboardPanel", side_effect=Exception("Load Fail")
    ):
        # Mock QMessageBox.critical
        with patch("PyQt6.QtWidgets.QMessageBox.critical") as mock_msg:
            placeholder = MagicMock()
            mock_mw.page_stack.widget.return_value = placeholder

            panel = controller.get_panel(index)

            assert panel == placeholder
            mock_msg.assert_called_once()

