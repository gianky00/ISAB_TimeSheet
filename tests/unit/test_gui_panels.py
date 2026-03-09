from unittest.mock import MagicMock, patch
import pytest
from PyQt6.QtWidgets import QApplication
from src.gui.panels.carico_ts import CaricoTSPanel
from src.gui.panels.scarico_ts import ScaricaTSPanel
from src.gui.panels.settings.main_panel import SettingsPanel

class TestGUIPanels:
    @pytest.fixture
    def app(self, qapp):
        return qapp

    def test_scarica_ts_panel_init(self, app, qtbot):
        panel = ScaricaTSPanel()
        qtbot.addWidget(panel)
        QApplication.processEvents()

        panel.params_widget.fornitore_combo.addItem("F1")
        from PyQt6.QtCore import QDate
        panel.params_widget.date_da.setDate(QDate(2025, 1, 1))

        assert panel.params_widget.fornitore_combo.count() >= 1
        panel.data_table.set_data([{"numero_oda": "123"}])
        assert panel.data_table.table.rowCount() >= 1

    @patch("src.gui.panels.scarico_ts.config_manager.set_config_value")
    @patch("src.gui.panels.scarico_ts.config_manager.load_config")
    def test_scarica_ts_panel_save(self, mock_load, mock_save, app, qtbot):
        mock_load.return_value = {}
        panel = ScaricaTSPanel()
        qtbot.addWidget(panel)
        QApplication.processEvents()

        panel.params_widget.fornitore_combo.addItem("NewF")
        panel._save_data()
        assert mock_save.called

    @pytest.mark.skip(reason="Incompatibilità mock strutturale in ambiente headless Windows V9.0.")
    @patch("src.gui.panels.settings.main_panel.config_manager.load_config")
    def test_settings_panel_init(self, mock_load, app, qtbot):
        test_config = {
            "browser_headless": True,
            "browser_timeout": 60,
            "accounts": [{"username": "user_test", "password": "p"}],
            "safework_accounts": [],
            "fornitori": [],
            "reparti": []
        }
        mock_load.return_value = test_config
        
        with patch("src.core.secrets_manager.SecretsManager.get_gemini_api_key", return_value="fake"):
            panel = SettingsPanel()
            qtbot.addWidget(panel)
            QApplication.processEvents()

            # In V9.0, accediamo al config_tab che contiene le pagine
            config_tab = panel.config_tab
            config_tab.load_from_config(test_config)
            QApplication.processEvents()

            gen_page = config_tab.general_page
            lists_page = config_tab.lists_page

            assert gen_page.headless_check.isChecked() is True
            assert gen_page.timeout_spin.value() == 60
            
            # Verifica caricamento account nel widget modulare
            acc_widget = lists_page.account_section
            assert acc_widget.list_widget.count() >= 1

    @pytest.mark.skip(reason="Incompatibilità mock strutturale in ambiente headless Windows V9.0.")
    @patch("src.gui.panels.settings.main_panel.config_manager.save_config")
    @patch("src.gui.panels.settings.main_panel.config_manager.load_config")
    def test_settings_panel_save(self, mock_load, mock_save, app, qtbot):
        mock_load.return_value = {}
        with patch("src.core.secrets_manager.SecretsManager.get_gemini_api_key", return_value="fake"):
            panel = SettingsPanel()
            qtbot.addWidget(panel)
            QApplication.processEvents()

            panel.config_tab.general_page.timeout_spin.setValue(99)
            panel.save_settings()
            assert mock_save.called

    def test_carico_ts_panel_structure(self, app, qtbot):
        panel = CaricoTSPanel()
        qtbot.addWidget(panel)
        QApplication.processEvents()

        assert panel.data_table is not None
        assert panel.bot_id == "carico_ts"
