from unittest.mock import patch

import pytest

from src.gui.panels.settings.main_panel import SettingsPanel


class TestSettingsGUI:
    @pytest.mark.skip(reason="Incompatibilità mock strutturale in ambiente headless Windows V9.0.")
    @patch("src.gui.panels.settings.main_panel.config_manager.load_config")
    def test_settings_panel_init(self, mock_load, qapp, qtbot):
        test_config = {
            "browser_headless": True,
            "browser_timeout": 45,
            "ai_provider": "gemini",
            "accounts": [],
            "safework_accounts": [],
        }
        mock_load.return_value = test_config

        with patch("src.core.secrets_manager.SecretsManager.get_gemini_api_key", return_value="fake"):
            panel = SettingsPanel()
            qtbot.addWidget(panel)

            # Forza caricamento tab configurazione
            panel.config_tab.load_from_config(test_config)

            gen_page = panel.config_tab.general_page
            assert gen_page.headless_check.isChecked() is True
            assert gen_page.timeout_spin.value() == 45

    @pytest.mark.skip(reason="Incompatibilità mock strutturale in ambiente headless Windows V9.0.")
    @patch("src.gui.panels.settings.main_panel.config_manager.save_config")
    @patch("src.gui.panels.settings.main_panel.config_manager.load_config")
    def test_settings_save_flow(self, mock_load, mock_save, qapp, qtbot):
        mock_load.return_value = {"browser_timeout": 30}
        with patch("src.core.secrets_manager.SecretsManager.get_gemini_api_key", return_value="fake"):
            panel = SettingsPanel()
            qtbot.addWidget(panel)

            panel.config_tab.general_page.timeout_spin.setValue(120)
            panel.save_settings()

            assert mock_save.called
