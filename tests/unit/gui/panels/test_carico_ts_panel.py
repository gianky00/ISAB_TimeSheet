from unittest.mock import MagicMock, patch

import pytest

from src.gui.panels.carico_ts import CaricoTSPanel


class TestCaricoTSPanel:
    @pytest.fixture
    def panel(self, qtbot):
        with (
            patch("src.gui.panels.carico_ts.config_manager.load_config", return_value={}),
            patch("src.gui.panels.carico_ts.config_manager.set_config_value"),
            patch("src.gui.styles.ui_effects.UIEffectsManager.apply_shadow"),
            patch("src.gui.styles.ui_effects.UIEffectsManager.animate_fade"),
        ):
            p = CaricoTSPanel()
            qtbot.addWidget(p)
            return p

    def test_initialization(self, panel):
        assert panel.bot_id == "carico_ts"
        assert panel.data_table is not None
        assert panel.clear_btn is not None

    def test_validate_ready_fail(self, panel):
        # Empty data
        panel.get_credentials = MagicMock(return_value=("u", "p"))
        with patch.object(panel.data_table, "get_data", return_value=[]):
            ready, msg = panel.validate_ready()
            assert not ready
            assert "Nessun dato" in msg

        # Empty credentials
        panel.get_credentials = MagicMock(return_value=("", ""))
        ready, msg = panel.validate_ready()
        assert not ready
        assert "credenziali" in msg.lower()

    def test_validate_ready_success(self, panel):
        panel.get_credentials = MagicMock(return_value=("user", "pass"))
        with patch.object(panel.data_table, "get_data", return_value=[{"oda": "1"}]):
            ready, _msg = panel.validate_ready()
            assert ready

    def test_clear_table(self, panel):
        with patch("src.gui.panels.carico_ts.ConfirmationDialog.confirm", return_value=True):
            panel.data_table.clear = MagicMock()
            panel._clear_table()
            assert panel.data_table.clear.called

    @patch("src.gui.panels.carico_ts.BotWorker")
    @patch("src.core.config_manager.load_config")
    def test_on_start_flow(self, mock_load, mock_worker, panel):
        mock_load.return_value = {"browser_headless": True}
        panel.get_credentials = MagicMock(return_value=("u", "p"))
        panel.data_table.get_data = MagicMock(return_value=[{"k": "v"}])

        panel._on_start()

        assert mock_worker.called
        _args, kwargs = mock_worker.call_args
        assert kwargs["bot_id"] == "carico_ts"
        assert kwargs["bot_params"]["username"] == "u"
        assert kwargs["bot_params"]["headless"] is True
        assert panel.worker.start.called

    def test_save_data_logic(self, panel):
        with patch("src.gui.panels.carico_ts.config_manager.set_config_value") as mock_set:
            panel.data_table.get_data = MagicMock(return_value=[{"test": 1}])
            panel._save_data()
            mock_set.assert_called_with("last_carico_ts_data", [{"test": 1}])
