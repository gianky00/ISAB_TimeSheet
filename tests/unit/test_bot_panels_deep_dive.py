from unittest.mock import MagicMock, patch

import pytest

from src.gui.panels import (
    BaseBotPanel,
    BotWorker,
    CaricoTSPanel,
    DettagliOdAPanel,
    ScaricaTSPanel,
    ScaricoPDLPanel,
    TimbratureBotPanel,
    TimbratureDBPanel,
)


class TestBotWorker:
    def test_worker_execution_success(self, qtbot):
        mock_bot = MagicMock()
        mock_bot.execute.return_value = True

        worker = BotWorker(mock_bot, {"test": "data"})

        # Connect signals
        finished_mock = MagicMock()
        worker.finished_signal.connect(finished_mock)

        worker.start()
        qtbot.waitUntil(lambda: finished_mock.called, timeout=2000)

        assert finished_mock.call_args[0][0] is True
        mock_bot.execute.assert_called_once_with({"test": "data"})
        mock_bot.set_log_callback.assert_called_once()

    def test_worker_execution_error(self, qtbot):
        mock_bot = MagicMock()
        mock_bot.execute.side_effect = Exception("Crash")

        worker = BotWorker(mock_bot, {})

        log_mock = MagicMock()
        finished_mock = MagicMock()
        worker.log_signal.connect(log_mock)
        worker.finished_signal.connect(finished_mock)

        worker.start()
        qtbot.waitUntil(lambda: finished_mock.called, timeout=2000)

        assert finished_mock.call_args[0][0] is False
        assert any("Crash" in call[0][0] for call in log_mock.call_args_list)

    def test_worker_request_input(self, qtbot):
        mock_bot = MagicMock()
        # Simulate bot needing input
        def bot_side_effect(data):
            val = worker._request_input_wrapper("Enter code:")
            return val == "1234"

        mock_bot.execute.side_effect = bot_side_effect
        worker = BotWorker(mock_bot, {})

        def handle_input_request(prompt, container, event):
            container["value"] = "1234"
            event.set()

        worker.request_input_signal.connect(handle_input_request)

        finished_mock = MagicMock()
        worker.finished_signal.connect(finished_mock)

        worker.start()
        qtbot.waitUntil(lambda: finished_mock.called, timeout=2000)

        assert finished_mock.call_args[0][0] is True

@pytest.fixture
def mock_gui_deps():
    with patch("src.gui.panels.AuditManager") as mock_audit, \
         patch("src.gui.panels.StatsManager") as mock_stats, \
         patch("src.gui.panels.config_manager") as mock_config, \
         patch("src.gui.panels.get_asset_path", return_value="mock/path.svg"), \
         patch("src.gui.panels.ToastManager") as mock_toast:

        # Setup mock config behavior
        mock_config.load_config.return_value = {"fornitori": ["F1", "F2"]}
        mock_config.get_default_account.return_value = {"username": "user", "password": "pwd"}

        yield {
            "audit": mock_audit,
            "stats": mock_stats,
            "config": mock_config,
            "toast": mock_toast
        }

class TestBaseBotPanel:
    def test_initialization(self, qapp, qtbot, mock_gui_deps):
        panel = BaseBotPanel("test_bot", "Test Bot", "Description")
        qtbot.addWidget(panel)

        assert panel.bot_id == "test_bot"
        assert panel.bot_name == "Test Bot"
        assert panel.start_btn.text() == "Avvia"
        assert panel.stop_btn.isEnabled() is False

    def test_on_start_audit(self, qapp, qtbot, mock_gui_deps):
        panel = BaseBotPanel("test_bot", "Test Bot", "Description")
        qtbot.addWidget(panel)

        panel._on_start()

        mock_gui_deps["audit"].return_value.log_action.assert_called()
        mock_gui_deps["stats"].return_value.increment_usage.assert_called_with("test_bot")

    def test_on_log_forward_to_telegram(self, qapp, qtbot, mock_gui_deps):
        panel = BaseBotPanel("bot", "Bot", "Desc")
        mock_win = MagicMock()
        mock_win.telegram = MagicMock()
        panel.window = MagicMock(return_value=mock_win)
        qtbot.addWidget(panel)

        panel._on_log("[12:00:00] Message")
        mock_win.telegram.send_message_sync.assert_called()
        assert "Message" in mock_win.telegram.send_message_sync.call_args[0][0]

    def test_ask_user_input(self, qapp, qtbot, mock_gui_deps):
        panel = BaseBotPanel("bot", "Bot", "Desc")
        qtbot.addWidget(panel)

        container = {}
        event = MagicMock()

        with patch("PyQt6.QtWidgets.QInputDialog.getText", return_value=("secret", True)):
            panel._ask_user_input("Prompt", container, event)
            assert container["value"] == "secret"
            event.set.assert_called_once()

class TestScaricaTSPanel:
    def test_validate_ready_success(self, qapp, qtbot, mock_gui_deps):
        panel = ScaricaTSPanel()
        qtbot.addWidget(panel)

        panel.data_table.set_data([{"numero_oda": "123"}])
        panel.params_widget.get_fornitore = MagicMock(return_value="Fornitore A")

        with patch.object(panel, "get_credentials", return_value=("user", "pass")):
            ready, msg = panel.validate_ready()
            assert ready is True

    def test_validate_ready_fail_no_data(self, qapp, qtbot, mock_gui_deps):
        panel = ScaricaTSPanel()
        qtbot.addWidget(panel)

        panel.data_table.set_data([])
        panel.params_widget.get_fornitore = MagicMock(return_value="Fornitore A")

        with patch.object(panel, "get_credentials", return_value=("user", "pass")):
            ready, msg = panel.validate_ready()
            assert ready is False
            assert "Nessun dato" in msg

    @patch("src.bots.create_bot")
    def test_on_start_workflow(self, mock_create_bot, qapp, qtbot, mock_gui_deps):
        mock_bot = MagicMock()
        mock_create_bot.return_value = mock_bot

        panel = ScaricaTSPanel()
        mock_win = MagicMock()
        mock_win.telegram = MagicMock()
        panel.window = MagicMock(return_value=mock_win)
        qtbot.addWidget(panel)

        panel.data_table.set_data([{"numero_oda": "123"}])
        panel.params_widget.get_fornitore = MagicMock(return_value="F")
        panel.params_widget.get_dates = MagicMock(return_value=("01.01.2025", "01.01.2025"))
        panel.params_widget.get_dest_path = MagicMock(return_value="/tmp")

        with patch.object(panel, "get_credentials", return_value=("user", "pass")):
            panel._on_start()

        assert panel.worker is not None
        panel.worker.stop()
        panel.worker.wait()

class TestCaricoTSPanel:
    def test_validate_ready(self, qapp, qtbot, mock_gui_deps):
        panel = CaricoTSPanel()
        qtbot.addWidget(panel)
        with patch.object(panel, "get_credentials", return_value=("u", "p")):
            panel.data_table.set_data([{"numero_oda": "1"}])
            ready, _ = panel.validate_ready()
            assert ready is True

    @patch("src.bots.create_bot")
    def test_on_start_workflow(self, mock_create_bot, qapp, qtbot, mock_gui_deps):
        panel = CaricoTSPanel()
        mock_win = MagicMock()
        mock_win.telegram = MagicMock()
        panel.window = MagicMock(return_value=mock_win)
        qtbot.addWidget(panel)

        panel.data_table.set_data([{"numero_oda": "1"}])
        with patch.object(panel, "get_credentials", return_value=("u", "p")):
            panel._on_start()

        assert panel.worker is not None
        panel.worker.stop()
        panel.worker.wait()

class TestTimbratureBotPanel:
    def test_load_save_data(self, qapp, qtbot, mock_gui_deps):
        panel = TimbratureBotPanel()
        qtbot.addWidget(panel)

        panel.autopilot_check.setChecked(True)
        panel._save_data()
        mock_gui_deps["config"].set_config_value.assert_any_call("timbrature_autopilot_enabled", True)

    @patch("src.bots.create_bot")
    def test_on_start(self, mock_create_bot, qapp, qtbot, mock_gui_deps):
        panel = TimbratureBotPanel()
        mock_win = MagicMock()
        mock_win.telegram = MagicMock()
        panel.window = MagicMock(return_value=mock_win)
        qtbot.addWidget(panel)

        panel.params_widget.get_fornitore = MagicMock(return_value="F")
        with patch.object(panel, "get_credentials", return_value=("u", "p")):
            panel._on_start()

        assert panel.worker is not None
        panel.worker.stop()
        panel.worker.wait()

class TestScaricoPDLPanel:
    @patch("src.bots.create_bot")
    def test_telegram_send_after_finish(self, mock_create_bot, qapp, qtbot, mock_gui_deps):
        mock_bot = MagicMock()
        mock_bot.downloaded_files = ["/tmp/test.pdf"]
        mock_create_bot.return_value = mock_bot

        panel = ScaricoPDLPanel()
        mock_win = MagicMock()
        mock_win.telegram = MagicMock()
        panel.window = MagicMock(return_value=mock_win)
        qtbot.addWidget(panel)

        panel.data_table.set_data([{"numero_pdl": "999"}])
        panel.merge_and_send_from_telegram = True

        with patch.object(panel, "get_credentials", return_value=("u", "p")), \
             patch("os.path.exists", return_value=True):
            panel._on_start()
            panel._on_worker_finished(True)

            mock_win.telegram.send_document_sync.assert_called()

class TestTimbratureDBPanel:
    def test_refresh_data(self, qapp, qtbot, mock_gui_deps):
        with patch("src.gui.panels.TimbratureStorage") as mock_storage:
            mock_storage.return_value.get_timbrature_with_reparto.return_value = [
                ("2024-01-01", "08:00", "17:00", "A", "B", "S", "I", "R", "C")
            ]
            panel = TimbratureDBPanel()
            qtbot.addWidget(panel)
            panel.refresh_data()
            assert panel.model.rowCount() == 1

class TestDettagliOdAPanel:
    def test_validate_ready(self, qapp, qtbot, mock_gui_deps):
        panel = DettagliOdAPanel()
        qtbot.addWidget(panel)
        panel.params_widget.get_fornitore = MagicMock(return_value="F")
        panel.data_table.set_data([{"numero_oda": "123"}])
        with patch.object(panel, "get_credentials", return_value=("u", "p")):
            ready, _ = panel.validate_ready()
            assert ready is True
