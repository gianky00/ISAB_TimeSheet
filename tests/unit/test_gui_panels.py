from unittest.mock import patch

import pytest

from src.gui.panels import CaricoTSPanel, ScaricaTSPanel
from src.gui.settings_panel import SettingsPanel


class TestGUIPanels:
    @pytest.fixture
    def app(self, qapp):
        # qapp fixture from pytest-qt handles QApplication instance
        return qapp

    def test_scarica_ts_panel_init(self, app, qtbot):
        panel = ScaricaTSPanel()
        qtbot.addWidget(panel)
        qtbot.wait(100)  # Wait for lazy loading

        # Manually set data
        panel.params_widget.fornitore_combo.addItem("F1")
        panel.params_widget.fornitore_combo.addItem("F2")
        from PyQt6.QtCore import QDate

        panel.params_widget.date_da.setDate(QDate(2025, 1, 1))

        # Check UI initialization
        assert panel.params_widget.fornitore_combo.count() == 2
        assert panel.params_widget.fornitore_combo.itemText(0) == "F1"
        assert panel.params_widget.date_da.date().year() == 2025

        # Check table data load
        panel.data_table.set_data([{"numero_oda": "123"}])
        assert panel.data_table.table.rowCount() >= 1

    @patch("src.core.config_manager.set_config_value")
    @patch("src.core.config_manager.load_config")
    def test_scarica_ts_panel_save(self, mock_load, mock_save, app, qtbot):
        mock_load.return_value = {}
        panel = ScaricaTSPanel()
        qtbot.addWidget(panel)
        qtbot.wait(100)

        # Modify UI
        panel.params_widget.fornitore_combo.addItem("NewF")
        panel.params_widget.fornitore_combo.setCurrentText("NewF")
        panel.elabora_ts_check.setChecked(True)

        # Trigger save (usually manual or signal based)
        panel._save_data()

        # Verify save called (actual checks of args would be more complex)
        assert mock_save.called

    @patch("src.gui.settings_panel.config_manager.load_config")
    def test_settings_panel_init(self, mock_load, app, qtbot):
        mock_load.return_value = {
            "browser_headless": True,
            "browser_timeout": 60,
            "accounts": [{"username": "u", "password": "p"}],
        }

        panel = SettingsPanel()
        qtbot.addWidget(panel)

        assert panel.headless_check.isChecked() is True
        assert panel.timeout_spin.value() == 60
        assert panel.account_list.count() == 1

    @patch("src.gui.settings_panel.config_manager.set_config_value")
    @patch("src.gui.settings_panel.config_manager.load_config")
    def test_settings_panel_save(self, mock_load, mock_save, app, qtbot):
        mock_load.return_value = {}
        panel = SettingsPanel()
        qtbot.addWidget(panel)

        # Change something
        panel.timeout_spin.setValue(99)

        # Click save
        with patch("src.gui.settings_panel.QMessageBox.information"):  # Suppress popup
            panel.save_btn.click()

        # Verify save called
        assert mock_save.called

    def test_carico_ts_panel_structure(self, app, qtbot):
        panel = CaricoTSPanel()
        qtbot.addWidget(panel)
        qtbot.wait(100)

        # Just check it doesn't crash and has table
        assert panel.data_table is not None
        assert panel.bot_id == "carico_ts"
