from unittest.mock import patch

import pytest
from PyQt6.QtCore import Qt

# Import classes to test
from src.gui.dialogs.account_dialog import AccountDialog
from src.gui.panels.settings.main_panel import SettingsPanel


class TestSettingsPanelCoverage:
    @pytest.fixture
    def mock_config_manager(self, mocker):
        cm = mocker.patch("src.gui.panels.settings.main_panel.config_manager")
        # Setup default config dict
        config_data = {
            "browser_headless": False,
            "browser_timeout": 30,
            "contabilita_file_path": "/path/to/contabilita",
            "giornaliere_path": "",
            "attivita_programmate_path": "",
            "certificati_campione_path": "",
            "dataease_path": "",
            "enable_auto_update_contabilita": True,
            "telegram_token": "",
            "telegram_chat_id": "",
            "fornitori": ["Fornitore 1"],
            "contracts": ["Contratto A"],
            "reparti": [],
            "cantieri": [],
            "accounts": [],
            "safework_accounts": [],
        }
        cm.CONFIG = config_data
        cm.load_config.return_value = config_data
        return cm

    @pytest.fixture
    def mock_keyring(self, mocker):
        # Mock SecretsManager inside settings_panel components
        sm = mocker.patch("src.gui.panels.settings.tabs.telegram_tab.SecretsManager")
        sm.get_gemini_api_key.return_value = "dummy_key"
        sm.get_openai_key.return_value = ""
        sm.get_github_token.return_value = ""
        sm.get_exa_api_key.return_value = ""
        return sm

    @pytest.fixture
    def panel(self, qtbot, mock_config_manager, mock_keyring):
        # Mock ToastManager to avoid popup issues
        with patch("src.gui.panels.settings.main_panel.ToastManager"):
            panel = SettingsPanel()
            qtbot.addWidget(panel)
            return panel

    def test_init_ui(self, panel):
        """Test that UI elements are initialized."""
        assert panel is not None
        assert panel.config_tab.general_page.headless_check is not None
        assert panel.config_tab.paths_page.contabilita_path_edit is not None

    def test_load_config_to_ui(self, panel, mock_config_manager):
        """Test that configuration is correctly loaded into UI widgets."""
        # Verify headless checkbox
        assert panel.config_tab.general_page.headless_check.isChecked() is False

        # Verify text fields
        assert (
            panel.config_tab.paths_page.contabilita_path_edit.text()
            == "/path/to/contabilita"
        )

    def test_autosave_behavior(self, panel, mock_config_manager, mock_keyring):
        """Test that changing widgets triggers auto-save."""
        # Change UI state
        panel.config_tab.general_page.headless_check.setChecked(True)
        # Verify ConfigManager.set_config_value called (via debounce timer in real app, here we check side effects)
        # In refactored version, it might be triggered by settings_changed signal
        panel._save_settings()
        mock_config_manager.set_config_value.assert_any_call("browser_headless", True)

    def test_account_dialog_visibility_toggle(self, qtbot):
        """Test password visibility toggle in AccountDialog."""
        dlg = AccountDialog(None, "user", "pass")
        qtbot.addWidget(dlg)

        # Initial state: Password mode
        assert dlg.password_edit.echoMode() == dlg.password_edit.EchoMode.Password

        # Click toggle
        qtbot.mouseClick(dlg.toggle_pass_btn, Qt.MouseButton.LeftButton)
        assert dlg.password_edit.echoMode() == dlg.password_edit.EchoMode.Normal

        # Click again
        qtbot.mouseClick(dlg.toggle_pass_btn, Qt.MouseButton.LeftButton)
        assert dlg.password_edit.echoMode() == dlg.password_edit.EchoMode.Password

    def test_unsaved_changes_logic(self, panel):
        """Test that unsaved changes logic works."""
        assert panel._has_unsaved_changes is False

        # Change something triggers setting_changed which starts save_timer
        panel.config_tab.general_page.headless_check.setChecked(True)
        assert panel._has_unsaved_changes is True

    def test_add_fornitore(self, panel, mock_config_manager):
        """Test adding a supplier."""
        with patch(
            "PyQt6.QtWidgets.QInputDialog.getText", return_value=("New Supplier", True)
        ):
            lists_page = panel.config_tab.lists_page
            lists_page._add_fornitore()

            # Check list widget
            items = [
                lists_page.fornitori_list.item(i).text()
                for i in range(lists_page.fornitori_list.count())
            ]
            assert "New Supplier" in items
