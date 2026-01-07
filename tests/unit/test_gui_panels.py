from unittest.mock import patch

import pytest

from src.gui.panels import CaricoTSPanel, ScaricaTSPanel
from src.gui.settings_panel import SettingsPanel


class TestGUIPanels:

    @pytest.fixture
    def app(self, qapp):
        # qapp fixture from pytest-qt handles QApplication instance
        return qapp

    @patch("src.gui.panels.config_manager.load_config")
    def test_scarica_ts_panel_init(self, mock_load, app, qtbot):
        # Mock config
        # Use snake_case for mock data because EditableDataTable normalizes keys
        mock_load.return_value = {
            "fornitori": ["F1", "F2"],
            "last_ts_data": [{"numero_oda": "123"}],  # Changed key to snake_case
            "last_ts_date": "01.01.2025",
        }

        panel = ScaricaTSPanel()
        qtbot.addWidget(panel)

        # Check UI initialization
        assert panel.fornitore_combo.count() == 2
        assert panel.fornitore_combo.itemText(0) == "F1"
        assert panel.date_edit.date().year() == 2025

        # Check table data load
        # EditableDataTable ensures at least 3 rows are present after loading data
        # So we check rowCount is at least 1 (from loaded data) and the content is correct.
        assert panel.data_table.table.rowCount() >= 1

        # Check content of first cell (Numero OdA)
        item = panel.data_table.table.item(0, 0)  # Assuming first data item is row 0
        assert item is not None
        assert item.text() == "123"

    @patch("src.gui.panels.config_manager.set_config_value")
    @patch("src.gui.panels.config_manager.load_config")
    def test_scarica_ts_panel_save(self, mock_load, mock_save, app, qtbot):
        mock_load.return_value = {}
        panel = ScaricaTSPanel()
        qtbot.addWidget(panel)

        # Modify UI
        panel.fornitore_combo.addItem("NewF")
        panel.fornitore_combo.setCurrentText("NewF")
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

        # Just check it doesn't crash and has table
        assert panel.data_table is not None
        assert panel.bot_id == "carico_ts"
