import pytest
from PyQt6.QtCore import Qt

from src.gui.dialogs.account_dialog import AccountDialog
from src.gui.panels.settings.main_panel import SettingsPanel


class TestSettingsPanelCoverage:
    @pytest.fixture
    def mock_config(self, mocker):
        # Patch config_manager in all relevant modules
        config_data = {
            "browser_headless": False,
            "browser_timeout": 30,
            "contabilita_file_path": "/path/to/contabilita",
            "giornaliere_path": "",
            "attivita_programmate_path": "",
            "certificati_campione_path": "",
            "dataease_path": "",
            "dataease_db_path": "",
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

        # Patch the base core module
        cm = mocker.patch("src.core.config_manager")
        cm.load_config.return_value = config_data

        # ALSO patch specifically in the module that actually imports it
        mocker.patch("src.gui.panels.settings.main_panel.config_manager", cm)

        return cm

    @pytest.fixture
    def mock_secrets(self, mocker):
        sm = mocker.patch("src.core.secrets_manager.SecretsManager")
        sm.get_gemini_api_key.return_value = "dummy_key"
        return sm

    @pytest.fixture
    def panel(self, qapp, qtbot, mock_config, mock_secrets):
        # Create panel with mocked dependencies
        p = SettingsPanel()
        qtbot.addWidget(p)
        return p

    def test_init_ui(self, panel):
        """Test that UI elements are initialized."""
        assert panel is not None
        assert panel.config_tab.general_page.headless_check is not None
        assert panel.config_tab.paths_page.contabilita_path_edit is not None

    def test_load_config_to_ui(self, panel):
        """Test that configuration is correctly loaded into UI widgets."""
        assert panel.config_tab.general_page.headless_check.isChecked() is False
        assert panel.config_tab.paths_page.contabilita_path_edit.text() == "/path/to/contabilita"

    def test_autosave_behavior(self, panel, mock_config):
        """Test that changing widgets triggers auto-save."""
        panel.config_tab.general_page.headless_check.setChecked(True)
        # Force immediate save (original uses timer)
        panel._save_settings()
        # Verify that save_to_config was called on the tab, which should call config_manager
        assert mock_config.set_config_value.called

    def test_account_dialog_visibility_toggle(self, qtbot):
        """Test password visibility toggle in AccountDialog."""
        dlg = AccountDialog(None, "user", "pass")
        qtbot.addWidget(dlg)
        assert dlg.password_edit.echoMode() == dlg.password_edit.EchoMode.Password
        qtbot.mouseClick(dlg.toggle_pass_btn, Qt.MouseButton.LeftButton)
        assert dlg.password_edit.echoMode() == dlg.password_edit.EchoMode.Normal

    def test_unsaved_changes_logic(self, panel):
        """Test that unsaved changes logic works."""
        assert panel.has_unsaved_changes() is False
        panel.config_tab.general_page.headless_check.setChecked(True)
        assert panel.has_unsaved_changes() is True

    def test_add_fornitore(self, panel, mocker):
        """Test adding a supplier."""
        mocker.patch("PyQt6.QtWidgets.QInputDialog.getText", return_value=("New Supplier", True))
        lists_page = panel.config_tab.lists_page
        lists_page._add_fornitore()
        items = [lists_page.fornitori_list.item(i).text() for i in range(lists_page.fornitori_list.count())]
        assert "New Supplier" in items
