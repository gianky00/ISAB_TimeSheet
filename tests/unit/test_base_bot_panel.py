import threading
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

# Import the panels and worker
from src.gui.panels.base import BaseBotPanel
from src.gui.widgets import ModernButton


class TestBaseBotPanel:
    @pytest.fixture(autouse=True)
    def setup_method(self, qapp):
        """Setup method using pytest-qt's qapp fixture."""
        # Mock dependencies
        self.mock_parent = MagicMock(spec=QWidget)
        self.mock_parent.telegram = MagicMock()
        self.mock_parent.show_background_notification = MagicMock()

        # Patch core managers and UI components globally for this test class
        # CRITICAL: We patch layout methods to allow MagicMocks without TypeError
        with patch("src.gui.panels.base.AuditManager"), patch(
            "src.gui.panels.base.StatsManager"
        ), patch("src.gui.panels.base.StatusCard"), patch(
            "src.gui.panels.base.TimelineWidget"
        ), patch("src.gui.panels.base.ModernButton") as mock_btn_class, patch(
            "src.gui.panels.base.get_asset_path", return_value="mock.svg"
        ), patch("src.gui.panels.base.config_manager"), patch.object(
            QVBoxLayout, "addWidget"
        ), patch.object(QHBoxLayout, "addWidget"), patch.object(
            QVBoxLayout, "addLayout"
        ):
            # Setup ModernButton mock
            self.mock_start_btn = MagicMock(spec=QPushButton)
            self.mock_stop_btn = MagicMock(spec=QPushButton)
            mock_btn_class.side_effect = [self.mock_start_btn, self.mock_stop_btn]
            mock_btn_class.Variant = ModernButton.Variant
            mock_btn_class.Size = ModernButton.Size

            self.panel = BaseBotPanel("bot_id", "Bot Name", "Description", parent=None)

            # Replace real signals with mocks to avoid read-only AttributeErrors in tests
            self.panel.status_changed = MagicMock()
            self.panel.bot_started = MagicMock()
            self.panel.bot_stopped = MagicMock()
            self.panel.bot_finished = MagicMock()
            self.panel.bot_results_ready = MagicMock()

            self.panel.window = MagicMock(return_value=self.mock_parent)
            yield

    def test_base_panel_init(self):
        assert self.panel.bot_id == "bot_id"
        assert self.panel.bot_name == "Bot Name"
        # Verify connections
        self.mock_start_btn.clicked.connect.assert_called()
        self.mock_stop_btn.clicked.connect.assert_called()

    def test_update_status(self):
        self.panel.status_card = MagicMock()
        self.panel._update_status("#0d6efd", "Running")
        self.panel.status_card.setStatus.assert_called_with("Running", "#0d6efd")
        self.panel.status_changed.emit.assert_called_with("#0d6efd", "Running")

    def test_add_rows_simple(self):
        # We need to mock data_table and its methods carefully
        self.panel.data_table = MagicMock()
        self.panel.data_table.get_data.return_value = [{"id": 1}]
        self.panel._save_data = MagicMock()

        self.panel.add_rows_simple([{"id": 2}])

        # Verify that set_data was called with the cumulative list
        self.panel.data_table.set_data.assert_called_once()
        args, _ = self.panel.data_table.set_data.call_args
        assert len(args[0]) == 2
        assert args[0][0]["id"] == 1
        assert args[0][1]["id"] == 2

    def test_clear_rows_simple(self):
        self.panel.data_table = MagicMock()
        self.panel._save_data = MagicMock()
        self.panel.clear_rows_simple()
        self.panel.data_table.set_data.assert_called_with([])

    @patch("src.gui.panels.base.datetime")
    def test_on_start(self, mock_dt):
        mock_dt.now.return_value = datetime(2025, 1, 1)
        self.panel.log_widget = MagicMock()
        self.panel._update_status = MagicMock()

        self.panel._on_start()

        assert self.panel.start_time == datetime(2025, 1, 1)
        self.panel.log_widget.timeline.set_mood.assert_called_with("running")

    def test_on_stop(self):
        self.panel.worker = MagicMock()
        self.panel.log_widget = MagicMock()
        self.panel._update_status = MagicMock()

        self.panel._on_stop()

        self.panel.worker.stop.assert_called_once()

    def test_on_log(self):
        self.panel.log_widget = MagicMock()
        self.panel._on_log("[10:00:00] Hello")
        self.panel.log_widget.append.assert_called_with("[10:00:00] Hello")

    def test_ask_user_input(self):
        result = {}
        event = threading.Event()
        with patch(
            "src.gui.panels.base.QInputDialog.getText", return_value=("input", True)
        ):
            self.panel._ask_user_input("Prompt", result, event)
            assert result["value"] == "input"
            assert event.is_set()
