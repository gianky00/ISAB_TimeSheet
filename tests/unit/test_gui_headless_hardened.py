from unittest.mock import patch

import pytest
from PySide6.QtWidgets import QWidget

from src.gui.panels import SettingsPanel
from src.gui.widgets.toast import Toast, ToastParams


class TestGUIHeadlessHardened:
    """Test di resilienza per componenti GUI in ambiente headless."""

    @pytest.fixture(autouse=True)
    def mock_sync_save_worker(self, mocker):
        """Forza il worker di salvataggio config ad essere sincrono."""

        def mock_start(instance):
            instance.run()

        mocker.patch("src.gui.panels.settings.main_panel.ConfigSaveWorker.start", mock_start)

    def test_settings_auto_save_trigger(self, qapp, mocker, qtbot):
        mock_save = mocker.patch("src.core.config_manager.save_config")
        mocker.patch("src.core.config_manager.load_config", return_value={})

        panel = SettingsPanel()
        # V9.4: Widget is inside general_page
        panel.config_tab.general_page.headless_check.setChecked(True)

        # Debounce timer is 500ms. Force execution.
        panel._execute_async_save()

        assert mock_save.called

    def test_toast_animation_lifecycle(self, qapp, mocker):
        """Verifica che il toast si mostri e avvii l'animazione."""
        parent = QWidget()
        params = ToastParams(message="Test Message", parent=parent)
        toast = Toast(params)

        toast.show_at(100, 100)
        assert toast.isVisible()
        # Access animation from Toast internal
        assert toast._fade_in.state() == toast._fade_in.State.Running
        toast.close()

    def test_settings_account_addition_flow(self, qapp, mocker, qtbot):
        mocker.patch("src.core.config_manager.add_account", return_value=True)
        mocker.patch("src.core.config_manager.load_config", return_value={})
        mock_save = mocker.patch("src.core.config_manager.save_config")

        panel = SettingsPanel()

        # Aggressive mock for AccountDialog to avoid Qt execution in headless
        with patch("src.gui.panels.settings.widgets.account_list_widget.AccountDialog") as mock_dlg_class:
            mock_dlg = mock_dlg_class.return_value
            mock_dlg.exec.return_value = 1
            mock_dlg.get_data.return_value = ("u", "p", "")

            panel.config_tab.lists_page.account_section.add_account()

            # Force save execution (since it might be debounced via SettingsPanel signals)
            panel._execute_async_save()

            assert mock_save.called

    def test_settings_tab_change_logic(self, qapp):
        panel = SettingsPanel()
        panel.tabs.setCurrentIndex(1)
        assert panel.tabs.currentIndex() == 1
