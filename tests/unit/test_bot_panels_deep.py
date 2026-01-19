from unittest.mock import MagicMock, patch

import pytest

from src.gui.panels import BaseBotPanel, CaricoTSPanel, DettagliOdAPanel, ScaricaTSPanel


@pytest.fixture
def mock_ui_deps(mocker):
    # Mocking external managers used in panels
    mocker.patch("src.core.config_manager.load_config", return_value={})
    mocker.patch("src.core.config_manager.set_config_value")
    mocker.patch("src.core.audit_manager.AuditManager")
    mocker.patch("src.core.stats_manager.StatsManager")
    mocker.patch("src.utils.helpers.get_asset_path", return_value="")
    return mocker


def test_base_bot_panel_logic(qtbot, mock_ui_deps):
    panel = BaseBotPanel("test_bot", "Test Bot", "Description")
    qtbot.addWidget(panel)

    panel._update_status("in_corso", "Esecuzione...")
    status, msg = panel.get_current_status()
    assert status == "in_corso"
    assert "Esecuzione" in msg

    # Test finished logic
    panel.start_btn.setEnabled(False)
    panel.stop_btn.setEnabled(True)
    panel._on_bot_finished(True)
    assert panel.start_btn.isEnabled() is True
    assert panel.stop_btn.isEnabled() is False


def test_scarica_ts_panel_deep(qtbot, mock_ui_deps):
    panel = ScaricaTSPanel()
    qtbot.addWidget(panel)

    # Test validation
    # Case 1: Empty OdA
    with patch("src.gui.panels.QMessageBox.warning"):
        ready, msg = panel.validate_ready()
        assert ready is False
        assert "OdA" in msg

    # Case 2: Success
    panel.data_table.set_data([{"numero_oda": "123456"}])
    ready, msg = panel.validate_ready()
    assert ready is True


def test_carico_ts_panel_deep(qtbot, mock_ui_deps):
    panel = CaricoTSPanel()
    qtbot.addWidget(panel)

    # Mock table data
    panel.data_table.set_data([{"id": "1", "stato": "da_caricare"}])
    assert panel.data_table.table.rowCount() == 1

    # Test reset
    panel.log_widget.clear()
    panel.log_widget.append("Test")
    panel._on_stop()  # Should stop worker if exists


def test_dettagli_oda_panel_deep(qtbot, mock_ui_deps):
    panel = DettagliOdAPanel()
    qtbot.addWidget(panel)

    # Check if correct bot_id
    assert panel.bot_id == "dettagli_oda"

    # Test adding rows
    panel.add_rows_simple([{"numero_oda": "999"}])
    assert panel.data_table.get_data()[0]["numero_oda"] == "999"


@patch("src.gui.panels.BotWorker")
def test_bot_worker_integration(mock_worker_cls, qtbot, mock_ui_deps):
    panel = ScaricaTSPanel()
    qtbot.addWidget(panel)

    # Setup for start
    panel.data_table.set_data([{"numero_oda": "123"}])

    with patch.object(panel, "get_bot_instance", return_value=MagicMock()):
        panel._on_start()
        assert panel.worker is not None
        mock_worker_cls.assert_called_once()
