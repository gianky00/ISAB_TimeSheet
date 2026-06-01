"""Unit tests for AppEventHandler."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtWidgets import QMainWindow

from src.gui.main_window.controllers.app_event_handler import AppEventHandler


@pytest.fixture
def real_main_window(qtbot):
    mw = QMainWindow()
    mw._handle_f5_action = MagicMock()
    mw.tool_bar_component = MagicMock()
    qtbot.addWidget(mw)
    return mw


class TestAppEventHandler:
    """Test suite per AppEventHandler."""

    def test_quit_application(self, real_main_window, mocker):
        handler = AppEventHandler(real_main_window)
        # Mock close to avoid real event
        mock_close = mocker.patch.object(real_main_window, "close")

        handler.quit_application()

        assert handler._force_quit is True
        assert mock_close.called

    def test_handle_close_event_hide(self, real_main_window, mocker):
        handler = AppEventHandler(real_main_window)
        event = MagicMock()

        mocker.patch.object(real_main_window, "isVisible", return_value=True)
        mock_hide = mocker.patch.object(real_main_window, "hide")

        handler.handle_close_event(event)

        assert mock_hide.called
        assert event.ignore.called

    def test_handle_close_event_force_quit(self, real_main_window, mocker):
        handler = AppEventHandler(real_main_window)
        handler._force_quit = True
        event = MagicMock()

        mocker.patch("src.core.app_updater.has_pending_update", return_value=False)
        mocker.patch("src.core.app_updater.run_pending_installer")
        mocker.patch("src.core.config_manager.load_config", return_value={"auto_backup": False})

        handler.handle_close_event(event)

        assert event.accept.called

    def test_handle_f5_delegation(self, real_main_window):
        handler = AppEventHandler(real_main_window)
        handler.handle_f5()
        assert real_main_window._handle_f5_action.called

    def test_handle_ctrl_f_focus(self, real_main_window):
        handler = AppEventHandler(real_main_window)
        mock_search = MagicMock()
        real_main_window.tool_bar_component.global_search = mock_search

        handler.handle_ctrl_f()

        assert mock_search.setFocus.called
        assert mock_search.selectAll.called
