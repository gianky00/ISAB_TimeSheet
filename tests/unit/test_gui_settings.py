import pytest
from PyQt6.QtWidgets import QApplication
from src.gui.settings_panel import SettingsPanel
from unittest.mock import patch, MagicMock

class TestSettingsGUI:

    @pytest.fixture
    def app(self, qapp):
        return qapp

    @patch('src.gui.settings_panel.config_manager.load_config')
    def test_settings_panel_init(self, mock_load, app, qtbot):
        mock_load.return_value = {
            "browser_headless": True,
            "browser_timeout": 45,
            "accounts": []
        }
        
        panel = SettingsPanel()
        qtbot.addWidget(panel)
        
        assert panel.headless_check.isChecked() is True
        assert panel.timeout_spin.value() == 45

    @patch('src.gui.settings_panel.config_manager.set_config_value')
    @patch('src.gui.settings_panel.config_manager.load_config')
    def test_settings_save(self, mock_load, mock_set, app, qtbot):
        mock_load.return_value = {}
        panel = SettingsPanel()
        qtbot.addWidget(panel)
        
        panel.timeout_spin.setValue(99)
        
        # Suppress message box
        with patch('src.gui.settings_panel.QMessageBox.information'):
            panel._save_settings()
            
        # Verify call to config_manager
        mock_set.assert_any_call("browser_timeout", 99)
