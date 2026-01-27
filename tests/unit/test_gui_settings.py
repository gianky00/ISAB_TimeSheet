from unittest.mock import patch

import pytest

from src.gui.panels.settings.main_panel import SettingsPanel


class TestSettingsGUI:
    @pytest.fixture
    def app(self, qapp):
        return qapp

    @patch("src.gui.panels.settings.main_panel.config_manager.load_config")
    def test_settings_panel_init(self, mock_load, app, qtbot):
        mock_load.return_value = {
            "browser_headless": True,
            "browser_timeout": 45,
            "accounts": [],
        }

        panel = SettingsPanel()
        qtbot.addWidget(panel)

        # Accessing nested widgets in modular structure
        general_page = panel.config_tab.general_page
        assert general_page.headless_check.isChecked() is True
        assert general_page.timeout_spin.value() == 45

    @patch("src.gui.panels.settings.main_panel.config_manager.set_config_value")
    @patch("src.gui.panels.settings.main_panel.config_manager.load_config")
    def test_settings_save(self, mock_load, mock_set, app, qtbot):
        mock_load.return_value = {}
        panel = SettingsPanel()
        qtbot.addWidget(panel)

        general_page = panel.config_tab.general_page
        general_page.timeout_spin.setValue(99)

        # Trigger save
        panel._save_settings()

        # Verify call to config_manager
        mock_set.assert_any_call("browser_timeout", 99)

