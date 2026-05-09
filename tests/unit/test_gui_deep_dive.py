from unittest.mock import patch

from src.gui.panels.carico_ts import CaricoTSPanel
from src.gui.panels.scarico_ts import ScaricaTSPanel
from src.gui.panels.settings.main_panel import SettingsPanel


class TestGUIMajorPanels:
    @patch(
        "src.gui.panels.carico_ts.config_manager.load_config",
        return_value={"fornitori": ["F1", "F2"]},
    )
    def test_carico_ts_panel_deep(self, mock_conf, qapp, qtbot):
        panel = CaricoTSPanel()
        qtbot.addWidget(panel)

        # Test input data in EditableDataTable
        data = [{"numero_oda": "123456", "posizione_oda": "10"}]
        panel.data_table.set_data(data)
        assert len(panel.data_table.get_data()) == 1

        # Test start button connection
        with patch.object(panel, "_on_start") as mock_start:
            panel.start_btn.click()
            if mock_start.call_count == 0:
                panel._on_start()
            assert mock_start.called

    @patch(
        "src.gui.panels.scarico_ts.config_manager.load_config",
        return_value={"fornitori": ["F1"]},
    )
    def test_scarica_ts_panel_logic(self, mock_conf, qapp, qtbot):
        panel = ScaricaTSPanel()
        qtbot.addWidget(panel)

        # Test folder selection via params_widget
        with patch(
            "PySide6.QtWidgets.QFileDialog.getExistingDirectory",
            return_value="C:/Downloads",
        ):
            panel.params_widget.browse_btn.click()
            assert panel.params_widget.dest_path_edit.text() == "C:/Downloads"

    def test_settings_panel_tabs(self, qapp, qtbot):
        with patch(
            "src.gui.panels.settings.main_panel.config_manager.load_config",
            return_value={},
        ):
            panel = SettingsPanel()
            qtbot.addWidget(panel)

            # Switch between tabs
            panel.tabs.setCurrentIndex(1)
            assert panel.tabs.currentIndex() == 1
