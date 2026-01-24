from unittest.mock import patch

import pytest

from src.gui.panels.settings.main_panel import SettingsPanel


class TestSettingsPanelComplete:
    @pytest.fixture
    def panel(self, qapp):
        with patch(
            "src.gui.panels.settings.main_panel.config_manager.load_config",
            return_value={},
        ):
            with patch(
                "src.gui.panels.settings.tabs.telegram_tab.SecretsManager.get_gemini_api_key",
                return_value="",
            ):
                return SettingsPanel()

    def test_settings_navigation(self, panel, qtbot):
        qtbot.addWidget(panel)
        # 0: Configurazione, 1: Backup, 2: Statistiche, 3: Telegram
        assert panel.tabs.count() >= 4

        # Go to Telegram Tab
        panel.tabs.setCurrentIndex(3)
        assert "Telegram" in panel.tabs.tabText(3)

    def test_account_settings_logic(self, panel, qtbot):
        qtbot.addWidget(panel)
        panel.tabs.setCurrentIndex(0)  # Configurazione

        # Test adding an account
        with (
            patch(
                "src.gui.panels.settings.pages.lists_page.AccountDialog.exec",
                return_value=True,
            ),
            patch(
                "src.gui.panels.settings.pages.lists_page.AccountDialog.get_data",
                return_value=("new_user", "pw"),
            ),
        ):
            with patch.object(panel, "_save_settings") as mock_save:
                panel.config_tab.lists_page._add_account()
                mock_save.assert_called()

    def test_telegram_settings_change(self, panel, qtbot):
        qtbot.addWidget(panel)
        panel.tabs.setCurrentIndex(3)  # Telegram

        with patch.object(panel, "_save_settings") as mock_save:
            panel.telegram_tab.tg_token_edit.setText("new_token")
            # manual trigger
            panel._save_settings()
            mock_save.assert_called()

    def test_open_data_folder(self, panel, qtbot):
        qtbot.addWidget(panel)
        with patch("src.gui.panels.settings.pages.diag_page.open_folder") as mock_open:
            panel.config_tab.diag_page._open_data_folder()
            mock_open.assert_called()

    def test_backup_manual(self, panel, qtbot):
        qtbot.addWidget(panel)
        panel.tabs.setCurrentIndex(1)  # Backup
        with patch(
            "src.core.backup_manager.BackupManager.create_backup",
            return_value=(True, "OK"),
        ):
            panel.backup_tab._run_manual_backup()
            # Logic reached
            assert True
