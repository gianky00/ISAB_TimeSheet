from unittest.mock import MagicMock, patch

import pytest

from src.gui.panels.scarico_ts import ScaricaTSPanel


class TestScaricaTSPanel:
    @pytest.fixture
    def panel(self, qtbot):
        # Consolida i patch nel fixture per coerenza
        with (
            patch("src.gui.controllers.bot_execution_controller.BotExecutionController") as mock_ctrl_class,
            patch("src.core.bots.services.ScaricoTSService") as mock_service_class,
            patch("src.gui.styles.ui_effects.UIEffectsManager.apply_shadow"),
            patch("src.gui.styles.ui_effects.UIEffectsManager.animate_fade"),
        ):
            # Setup mock service per _load_saved_data
            mock_service = mock_service_class.return_value
            mock_service.load_config.return_value = {
                "societa": "ISAB",
                "fornitore": "COEMI",
                "dest_path": "/tmp",
                "elabora_ts": True,
                "data": [],
            }

            p = ScaricaTSPanel()
            p.bot_controller = mock_ctrl_class.return_value  # Ensure instance is correct
            qtbot.addWidget(p)
            p.show()
            return p

    def test_initialization(self, panel):
        assert panel.bot_id == "scarico_ts"
        assert panel.bot_controller is not None
        assert panel.status_list is not None

    def test_validate_ready(self, panel):
        with patch.object(panel.data_table, "get_data", return_value=[]):
            ready, _msg = panel.validate_ready()
            assert not ready
        with patch.object(panel.data_table, "get_data", return_value=[{"oda": "1"}]):
            ready, _msg = panel.validate_ready()
            assert ready

    def test_on_step_completed(self, panel):
        panel.status_list.update_status = MagicMock()
        panel.data_table.columns = [{"name": "esito"}]
        panel.data_table.update_cell = MagicMock()
        panel.on_step_completed(0, True, "OK")
        assert panel.status_list.update_status.called

    def test_on_start_flow(self, panel):
        # Reuse patched class from fixture via internal instance or new instance
        with patch("src.core.bots.services.ScaricoTSService") as mock_service_class:
            mock_service = mock_service_class.return_value
            mock_service.prepare_payload.return_value = ({"p": 1}, [{"d": 1}])

            panel.params_widget.get_dates = MagicMock(return_value=("01.01.2024", ""))
            panel.get_credentials = MagicMock(return_value=("u", "p"))
            panel.bot_controller.start.return_value = True

            panel._on_start()

            assert panel.bot_controller.start.called
            assert mock_service.prepare_payload.called

    def test_on_stop(self, panel):
        panel._on_stop()
        assert panel.bot_controller.stop.called

    def test_clear_table(self, panel):
        with patch("src.gui.panels.scarico_ts.ConfirmationDialog.confirm", return_value=True):
            panel.data_table.clear = MagicMock()
            panel._save_data = MagicMock()
            panel._clear_table()
            assert panel.data_table.clear.called
