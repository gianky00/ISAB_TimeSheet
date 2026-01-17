from unittest.mock import patch

import pytest
from PyQt6.QtCore import Qt

# Import classes to test
from src.gui.settings_panel import AccountDialog, SettingsPanel


class TestSettingsPanelCoverage:
    @pytest.fixture
    def mock_config_manager(self, mocker):
        cm = mocker.patch("src.gui.settings_panel.config_manager")
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
        # Mock SecretsManager inside settings_panel
        sm = mocker.patch("src.gui.settings_panel.SecretsManager")
        sm.get_gemini_api_key.return_value = "dummy_key"
        sm.get_openai_key.return_value = ""
        sm.get_github_token.return_value = ""
        sm.get_exa_api_key.return_value = ""
        return sm

    @pytest.fixture
    def panel(self, qtbot, mock_config_manager, mock_keyring):
        # Mock ToastManager to avoid popup issues
        with patch("src.gui.settings_panel.ToastManager"):
            panel = SettingsPanel()
            qtbot.addWidget(panel)
            return panel

    def test_init_ui(self, panel):
        """Test that UI elements are initialized."""
        assert panel is not None
        assert panel.headless_check is not None
        assert panel.contabilita_path_edit is not None

    def test_load_config_to_ui(self, panel, mock_config_manager):
        """Test that configuration is correctly loaded into UI widgets."""
        # _load_settings is called in __init__, so we just verify

        # Verify headless checkbox
        assert panel.headless_check.isChecked() is False

        # Verify text fields
        assert panel.contabilita_path_edit.text() == "/path/to/contabilita"

    def test_autosave_behavior(self, panel, mock_config_manager, mock_keyring):
        """Test that changing widgets triggers auto-save."""
        # Mock _save_settings to verify it's called or check config update
        # Since _save_settings calls config_manager.set_config_value, we check that.

        # Change UI state
        panel.headless_check.setChecked(True)
        # Verify ConfigManager.set_config_value called immediately
        mock_config_manager.set_config_value.assert_any_call("browser_headless", True)

        panel.timeout_spin.setValue(60)
        mock_config_manager.set_config_value.assert_any_call("browser_timeout", 60)

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

    def test_unsaved_changes_always_false(self, panel):
        """Test that unsaved changes logic is disabled (auto-save enabled)."""
        assert panel.has_unsaved_changes() is False

        # Change something
        panel.headless_check.setChecked(True)

        # Should still be False
        assert panel.has_unsaved_changes() is False

    def test_reset_config(self, panel, mock_config_manager):
        """Test resetting configuration."""
        # Force has_unsaved_changes to True to test the prompt logic if it were used,
        # but _reset_settings checks _has_unsaved_changes which is set to False in _load_settings.
        # But wait, _reset_settings implementation:
        # if self._has_unsaved_changes: prompt else load.
        # Since autosave is on, _has_unsaved_changes is False.
        # So _reset_settings just reloads.

        panel._reset_settings()
        mock_config_manager.load_config.assert_called()

    def test_add_fornitore(self, panel, mock_config_manager):
        """Test adding a supplier."""
        with patch(
            "PyQt6.QtWidgets.QInputDialog.getText", return_value=("New Supplier", True)
        ):
            panel._add_fornitore()

            # Check list widget
            items = [
                panel.fornitori_list.item(i).text()
                for i in range(panel.fornitori_list.count())
            ]
            assert "New Supplier" in items

            # Check save called
            mock_config_manager.set_config_value.assert_called()
