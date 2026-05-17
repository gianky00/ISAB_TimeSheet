from unittest.mock import patch

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

    # **CRITICAL**: Mock TimelineWidget to prevent QTimer crashes in CI
    mocker.patch("src.gui.widgets.timeline_widget.TimelineWidget")

    return mocker


def test_base_bot_panel_logic(qtbot, mock_ui_deps):
    """Test BaseBotPanel logic without actually creating complex widgets."""
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
    with patch("PySide6.QtWidgets.QMessageBox.warning"):
        ready, msg = panel.validate_ready()
        assert ready is False
        assert "OdA" in msg

    # Case 2: Success
    panel.data_table.set_data([{"Numero OdA": "123456"}])
    ready, msg = panel.validate_ready()
    assert ready is True


def test_carico_ts_panel_deep(qtbot, mock_ui_deps):
    panel = CaricoTSPanel()
    qtbot.addWidget(panel)

    # Forza il caricamento differito per svuotare la coda dei timer
    panel._safe_load_data()

    # Mock table data con metodo ad alto livello
    panel.add_rows_simple([{"numero_oda": "123456", "cognome": "Rossi"}])

    # get_rows_count() è più robusto perché filtra le righe vuote
    assert panel.get_rows_count() == 1

    # Test reset
    panel.log_widget.clear()
    panel.log_widget.append("Test")
    panel._on_stop()  # Should stop worker if exists


def test_dettagli_oda_panel_deep(qtbot, mock_ui_deps):
    panel = DettagliOdAPanel()
    qtbot.addWidget(panel)

    # Check if correct bot_id
    assert panel.bot_id == "dettagli_oda"

    # Test adding rows (usando nomi tecnici colonne)
    panel.add_rows_simple([{"numero_oda": "999"}])
    assert panel.data_table.get_data()[0]["numero_oda"] == "999"


def test_bot_worker_integration(qtbot, mock_ui_deps):
    """Test che il bot_controller viene invocato correttamente."""
    panel = ScaricaTSPanel()
    qtbot.addWidget(panel)

    # Setup for start
    panel.data_table.set_data([{"Numero OdA": "123"}])

    with patch.object(panel.bot_controller, "start", return_value=True) as mock_start:
        panel._on_start()
        mock_start.assert_called_once()
