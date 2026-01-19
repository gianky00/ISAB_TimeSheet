import sys
import threading
import unittest
from datetime import datetime
from unittest.mock import MagicMock, PropertyMock, patch

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QGroupBox,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# Import the panels and worker
from src.gui.panels import BaseBotPanel
from src.gui.widgets import (
    EditableDataTable,
    ModernButton,
)


class TestBaseBotPanel(unittest.TestCase):
    def setUp(self):
        # Ensure QApplication exists
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)

        # Mock dependencies for BaseBotPanel and its subclasses
        self.mock_parent = MagicMock(spec=QWidget)
        self.mock_parent.telegram = MagicMock()
        self.mock_parent.telegram.send_message_sync = MagicMock()
        self.mock_parent.telegram.send_document_sync = MagicMock()
        self.mock_parent.show_toast = MagicMock()
        self.mock_parent.show_settings = MagicMock()
        self.mock_parent.show_background_notification = MagicMock()
        self.mock_parent.navigate_to_panel = MagicMock()

        # Patch AuditManager and StatsManager classes in src.gui.panels where they are imported
        self.mock_audit_manager_instance = MagicMock()
        self.patcher_panels_audit_manager = patch(
            "src.gui.panels.AuditManager",
            new=MagicMock(return_value=self.mock_audit_manager_instance),
        )
        self.patcher_panels_audit_manager.start()

        self.mock_stats_manager_instance = MagicMock()
        self.patcher_panels_stats_manager = patch(
            "src.gui.panels.StatsManager",
            new=MagicMock(return_value=self.mock_stats_manager_instance),
        )
        self.patcher_panels_stats_manager.start()

        # Patch StatusCard in src.gui.panels
        self.patcher_status_card = patch("src.gui.panels.StatusCard")
        self.mock_status_card_class = self.patcher_status_card.start()

        self.mock_status_card_instance = MagicMock()
        self.mock_status_card_class.return_value = self.mock_status_card_instance
        type(self.mock_status_card_instance)._status = PropertyMock(
            return_value="idle"
        )  # Mock the _status property
        self.mock_status_card_instance._status_label = MagicMock()
        self.mock_status_card_instance._status_label.text.return_value = "Idle message"
        self.mock_status_card_instance.setStatus = MagicMock()  # Mock setStatus

        # Patch LogWidget in src.gui.panels
        self.patcher_log_widget = patch("src.gui.panels.LogWidget")
        self.mock_log_widget_class = self.patcher_log_widget.start()
        self.mock_log_widget_instance = MagicMock()
        self.mock_log_widget_instance.append = MagicMock()  # Explicitly mock append
        self.mock_log_widget_instance.timeline = MagicMock()
        self.mock_log_widget_instance.timeline.set_mood = MagicMock()  # Mock set_mood
        self.mock_log_widget_class.return_value = self.mock_log_widget_instance

        # Patch ModernButton in src.gui.panels
        self.patcher_modern_button = patch("src.gui.panels.ModernButton")
        self.mock_modern_button_class = self.patcher_modern_button.start()
        # Bind real Enums
        self.mock_modern_button_class.Variant = ModernButton.Variant
        self.mock_modern_button_class.Size = ModernButton.Size

        self.mock_start_btn_instance = MagicMock(spec=QPushButton)
        self.mock_stop_btn_instance = MagicMock(spec=QPushButton)
        self.mock_modern_button_class.side_effect = [
            self.mock_start_btn_instance,
            self.mock_stop_btn_instance,
        ]
        self.mock_start_btn_instance.clicked = MagicMock()  # Mock clicked signal
        self.mock_stop_btn_instance.clicked = MagicMock()  # Mock clicked signal
        self.mock_start_btn_instance.setEnabled = MagicMock()  # Mock setEnabled
        self.mock_stop_btn_instance.setEnabled = MagicMock()  # Mock setEnabled

        # Patch get_asset_path in src.gui.panels because it is imported directly
        self.patcher_get_asset_path = patch("src.gui.panels.get_asset_path")
        self.mock_get_asset_path = self.patcher_get_asset_path.start()
        self.mock_get_asset_path.return_value = "mock/path/to/asset.svg"

        # Patch config_manager in src.gui.panels directly to ensure it catches usage
        self.patcher_config_manager = patch("src.gui.panels.config_manager")
        self.mock_config_manager = self.patcher_config_manager.start()
        self.mock_config_manager.load_config.return_value = {
            "browser_headless": False,
            "browser_timeout": 30,
        }
        self.mock_config_manager.get_download_path.return_value = "/mock/download/path"
        self.mock_config_manager.get_default_account.return_value = {
            "username": "user",
            "password": "password",
        }

        self.patcher_qtimer_singleshot = patch("PyQt6.QtCore.QTimer.singleShot")
        self.mock_qtimer_singleshot = self.patcher_qtimer_singleshot.start()

        self.patcher_qmessagebox = patch("PyQt6.QtWidgets.QMessageBox")
        self.mock_qmessagebox = self.patcher_qmessagebox.start()
        self.mock_qmessagebox.question.return_value = QMessageBox.StandardButton.Yes

        # QInputDialog will be patched in test method
        # self.patcher_qinputdialog = patch('PyQt6.QtWidgets.QInputDialog')
        # self.mock_qinputdialog = self.patcher_qinputdialog.start()
        # self.mock_qinputdialog.getText.return_value = ("mock_input", True)

        self.patcher_create_bot = patch("src.bots.create_bot")
        self.mock_create_bot = self.patcher_create_bot.start()
        self.mock_bot_instance = MagicMock()
        self.mock_create_bot.return_value = self.mock_bot_instance

        self.patcher_bot_worker = patch("src.gui.panels.BotWorker")
        self.mock_bot_worker_class = self.patcher_bot_worker.start()
        self.mock_worker_bot_instance = MagicMock()
        self.mock_worker_bot_instance.downloaded_files = []
        self.mock_bot_worker_instance = MagicMock()
        self.mock_bot_worker_instance.start.return_value = None
        self.mock_bot_worker_instance.bot = self.mock_worker_bot_instance
        self.mock_bot_worker_class.return_value = self.mock_bot_worker_instance

        # Patch PyQt6.QtWidgets Layouts and Widgets in src.gui.panels
        self.patcher_qvboxlayout = patch("src.gui.panels.QVBoxLayout")
        self.mock_qvboxlayout_class = self.patcher_qvboxlayout.start()
        self.mock_qvboxlayout_instance = MagicMock(spec=QVBoxLayout)
        self.mock_qvboxlayout_class.return_value = self.mock_qvboxlayout_instance

        self.patcher_qhboxlayout = patch("src.gui.panels.QHBoxLayout")
        self.mock_qhboxlayout_class = self.patcher_qhboxlayout.start()
        self.mock_qhboxlayout_instance = MagicMock(spec=QHBoxLayout)
        self.mock_qhboxlayout_class.return_value = self.mock_qhboxlayout_instance

        self.patcher_qgroupbox = patch("src.gui.panels.QGroupBox")
        self.mock_qgroupbox_class = self.patcher_qgroupbox.start()
        self.mock_qgroupbox_instance = MagicMock(spec=QGroupBox)
        self.mock_qgroupbox_class.return_value = self.mock_qgroupbox_instance

        # We cannot easily patch src.gui.panels.QWidget because BaseBotPanel inherits from it.
        # If we patch it, we might break the inheritance if the module is reloaded or if we patch before import.
        # But we imported BaseBotPanel at top of file.
        # However, self.content_widget = QWidget() uses the name in the module.
        # Let's try patching it.
        self.patcher_qwidget_for_content = patch("src.gui.panels.QWidget")
        self.mock_qwidget_for_content_class = self.patcher_qwidget_for_content.start()
        self.mock_content_widget_instance = (
            self.mock_qwidget_for_content_class.return_value
        )

        # Patch QGraphicsOpacityEffect in src.gui.widgets.timeline_widget because that's where it is used
        self.patcher_qgraphic_opacity_effect = patch(
            "src.gui.widgets.timeline_widget.QGraphicsOpacityEffect"
        )
        self.mock_qgraphic_opacity_effect_class = (
            self.patcher_qgraphic_opacity_effect.start()
        )
        self.mock_qgraphic_opacity_effect_instance = MagicMock()
        self.mock_qgraphic_opacity_effect_class.return_value = (
            self.mock_qgraphic_opacity_effect_instance
        )

        # Patch MissionReportCard class
        self.patcher_mission_report_card = patch("src.gui.panels.MissionReportCard")
        self.mock_mission_report_card_class = self.patcher_mission_report_card.start()
        self.mock_mission_report_card_instance = MagicMock(
            spec=QWidget
        )  # MissionReportCard is a QWidget
        self.mock_mission_report_card_class.return_value = (
            self.mock_mission_report_card_instance
        )

        # Instantiate BaseBotPanel directly. Its __init__ and _setup_base_ui will run.
        self.panel = BaseBotPanel("bot_id", "Bot Name", "Description", parent=None)

        # Re-patch the signals on the instantiated panel for testing purposes, as pyqtSignals are not mockable directly on mock objects.
        # When BaseBotPanel is instantiated, its signals will be real pyqtSignal objects.
        # We need to replace them with MagicMocks to assert on their calls.
        self.panel.bot_started = MagicMock(spec=pyqtSignal)
        self.panel.bot_started.emit = MagicMock()
        self.panel.bot_stopped = MagicMock(spec=pyqtSignal)
        self.panel.bot_stopped.emit = MagicMock()
        self.panel.bot_finished = MagicMock(spec=pyqtSignal)
        self.panel.bot_finished.emit = MagicMock()
        self.panel.bot_results_ready = MagicMock(spec=pyqtSignal)
        self.panel.bot_results_ready.emit = MagicMock()
        self.panel.status_changed = MagicMock(spec=pyqtSignal)
        self.panel.status_changed.emit = MagicMock()

        # Mock the panel's window() method to return our mock_parent
        self.panel.window = MagicMock(return_value=self.mock_parent)

        # Patch re.sub for _on_log method by patching sys.modules
        self.mock_re_module = MagicMock()
        self.patcher_re_module = patch.dict("sys.modules", {"re": self.mock_re_module})
        self.patcher_re_module.start()
        self.mock_re_module.sub.return_value = "Cleaned message"

    def tearDown(self):
        self.patcher_panels_audit_manager.stop()
        self.patcher_panels_stats_manager.stop()
        self.patcher_status_card.stop()
        self.patcher_log_widget.stop()
        self.patcher_modern_button.stop()
        self.patcher_get_asset_path.stop()
        self.patcher_config_manager.stop()
        self.patcher_qtimer_singleshot.stop()
        self.patcher_qmessagebox.stop()
        # self.patcher_qinputdialog.stop() # Removed
        self.patcher_create_bot.stop()
        self.patcher_bot_worker.stop()
        self.patcher_qvboxlayout.stop()
        self.patcher_qhboxlayout.stop()
        self.patcher_qgroupbox.stop()  # Added
        self.patcher_qwidget_for_content.stop()
        self.patcher_qgraphic_opacity_effect.stop()
        self.patcher_mission_report_card.stop()  # Added
        self.patcher_re_module.stop()

        # Do NOT quit the app here. Keep it alive for the session.
        # if hasattr(self, 'app') and self.app is not None:
        #     self.app.quit()

    def test_base_panel_init(self):
        self.assertEqual(self.panel.bot_id, "bot_id")
        self.assertEqual(self.panel.bot_name, "Bot Name")
        self.assertEqual(self.panel.bot_description, "Description")
        self.assertIsNone(self.panel.worker)
        self.assertIsNone(self.panel.start_time)
        self.mock_status_card_class.assert_called_once_with("Stato Attività")
        self.mock_log_widget_class.assert_called_once()
        self.mock_modern_button_class.assert_any_call(
            "Avvia",
            variant=ModernButton.Variant.SUCCESS,
            size=ModernButton.Size.LARGE,
            icon="mock/path/to/asset.svg",
        )
        self.mock_modern_button_class.assert_any_call(
            "Stop",
            variant=ModernButton.Variant.DANGER,
            size=ModernButton.Size.LARGE,
            icon="mock/path/to/asset.svg",
        )
        self.mock_start_btn_instance.clicked.connect.assert_called_once_with(
            self.panel._on_start
        )
        self.mock_stop_btn_instance.clicked.connect.assert_called_once_with(
            self.panel._on_stop
        )
        self.mock_stop_btn_instance.setEnabled.assert_called_with(False)
        # QTimer.singleShot is not called when BaseBotPanel is instantiated directly, only in subclasses
        # self.mock_qtimer_singleshot.assert_called_once() # Removed as it's not called here

    def test_update_status(self):
        self.panel._update_status("#0d6efd", "Bot is running")
        self.mock_status_card_instance.setStatus.assert_called_once_with(
            "Bot is running", "#0d6efd"
        )
        self.panel.status_changed.emit.assert_called_once_with(
            "#0d6efd", "Bot is running"
        )

    def test_get_current_status(self):
        status, message = self.panel.get_current_status()
        self.assertEqual(status, "idle")  # Corrected assertion to lowercase
        self.assertEqual(message, "Idle message")

    def test_validate_ready_base(self):
        # Default implementation for BaseBotPanel
        ready, msg = self.panel.validate_ready()
        self.assertTrue(ready)
        self.assertEqual(msg, "")

    def test_add_rows_simple(self):
        # BaseBotPanel doesn't have a data_table by default, add one for this test
        self.panel.data_table = MagicMock(spec=EditableDataTable)
        self.panel.data_table.get_data.return_value = [{"col1": "existing"}]
        self.panel._save_data = MagicMock()  # Mock _save_data

        new_rows = [{"col1": "new"}]
        self.panel.add_rows_simple(new_rows)
        self.panel.data_table.set_data.assert_called_once_with(
            [{"col1": "existing"}, {"col1": "new"}]
        )
        self.panel._save_data.assert_called_once()

    def test_clear_rows_simple(self):
        # BaseBotPanel doesn't have a data_table by default, add one for this test
        self.panel.data_table = MagicMock(spec=EditableDataTable)
        self.panel._save_data = MagicMock()  # Mock _save_data

        self.panel.clear_rows_simple()
        self.panel.data_table.set_data.assert_called_once_with([])
        self.panel._save_data.assert_called_once()

    def test_get_rows_count(self):
        # BaseBotPanel doesn't have a data_table by default, add one for this test
        self.panel.data_table = MagicMock(spec=EditableDataTable)
        self.panel.data_table.get_data.return_value = [
            {"col1": "data1"},
            {"col1": "data2"},
        ]
        count = self.panel.get_rows_count()
        self.assertEqual(count, 2)

    @patch("src.gui.panels.datetime")
    def test_on_start(self, mock_datetime):
        # Mock datetime.now() for predictable start_time
        mock_datetime.now.return_value = datetime(2025, 1, 1, 10, 0, 0)

        self.panel._update_status = MagicMock()  # Mock the internal call
        self.panel._on_start()

        self.assertIsNotNone(self.panel.start_time)
        self.mock_log_widget_instance.timeline.set_mood.assert_called_once_with(
            "running"
        )
        self.panel._update_status.assert_called_once_with("#0d6efd")
        self.mock_audit_manager_instance.log_action.assert_called_once_with(
            action="Avvio Automazione",
            category="automazione",
            entity=self.panel.bot_name,
            params={"bot_id": self.panel.bot_id},
        )
        self.mock_stats_manager_instance.increment_usage.assert_called_once_with(
            self.panel.bot_id
        )

    def test_on_stop(self):
        self.panel.worker = self.mock_bot_worker_instance
        self.panel._update_status = MagicMock()  # Mock the internal call

        self.panel._on_stop()

        self.panel.worker.stop.assert_called_once()
        self.mock_log_widget_instance.append.assert_called_once_with(
            "[AVVISO] Stop richiesto..."
        )
        self.panel._update_status.assert_called_once_with(
            "#ffc107", "Arresto richiesto..."
        )

    @patch("src.gui.panels.datetime")
    @patch("src.gui.panels.QApplication")  # Patch QApplication for alert
    def test_on_worker_finished(self, MockQApplication, mock_datetime):
        self.panel.start_time = datetime(2025, 1, 1, 10, 0, 0)
        mock_datetime.now.return_value = datetime(
            2025, 1, 1, 10, 1, 30
        )  # 1m 30s duration

        self.panel.worker = self.mock_bot_worker_instance
        self.panel.worker.bot.downloaded_files = ["file1.pdf", "file2.pdf"]
        self.panel._update_status = MagicMock()

        # Success scenario
        self.panel._on_worker_finished(True)
        self.mock_start_btn_instance.setEnabled.assert_called_with(True)
        self.mock_stop_btn_instance.setEnabled.assert_called_with(False)
        self.mock_mission_report_card_class.assert_called_once_with("1m 30s", True)
        self.mock_audit_manager_instance.log_action.assert_called_with(
            status="success",
            **{
                "action": "Completamento Automazione",
                "category": "automazione",
                "entity": self.panel.bot_name,
                "params": {
                    "durata": "1m 30s",
                    "dettagli": "Esecuzione completata correttamente",
                },
            },
        )
        self.panel.bot_finished.emit.assert_called_once_with(True)
        self.mock_parent.show_background_notification.assert_called_once_with(
            f"{self.panel.bot_name} - Completato",
            "Operazione completata con successo.",
            is_error=False,
        )
        self.mock_bot_worker_instance.wait.assert_called_once()
        self.assertIsNone(self.panel.worker)
        self.panel.bot_results_ready.emit.assert_called_once_with(
            self.panel.bot_id, ["file1.pdf", "file2.pdf"]
        )

        self.mock_audit_manager_instance.log_action.reset_mock()
        self.panel.bot_finished.emit.reset_mock()
        self.mock_parent.show_background_notification.reset_mock()
        self.mock_bot_worker_instance.wait.reset_mock()
        self.panel.worker = (
            self.mock_bot_worker_instance
        )  # Re-assign for next test case

        # Failure scenario
        self.panel._on_worker_finished(False)
        self.mock_audit_manager_instance.log_action.assert_called_with(
            status="error",
            **{
                "action": "Completamento Automazione",
                "category": "automazione",
                "entity": self.panel.bot_name,
                "params": {
                    "durata": "1m 30s",
                    "dettagli": "Esecuzione fallita o interrotta",
                },
            },
        )
        self.panel.bot_finished.emit.assert_called_once_with(False)
        self.mock_parent.show_background_notification.assert_called_once_with(
            f"{self.panel.bot_name} - Errore",
            "Si è verificato un errore durante l'esecuzione.",
            is_error=True,
        )

    def test_on_log(self):
        self.mock_re_module.sub.return_value = "Cleaned message"
        # Mock the window().telegram interaction
        # The window() method is mocked to return self.mock_parent which has telegram attribute
        # self.panel.window().telegram is now self.mock_parent.telegram

        self.panel._on_log("[12:34:56] Test message")

        self.mock_log_widget_instance.append.assert_called_once_with(
            "[12:34:56] Test message"
        )
        self.mock_re_module.sub.assert_called_once()
        self.mock_parent.telegram.send_message_sync.assert_called_once_with(
            "🔹 *Bot Name*\nCleaned message"
        )

    def test_on_status(self):
        self.panel.status_card = self.mock_status_card_instance
        self.panel._on_status("Downloading...")
        self.mock_status_card_instance._update_status_display.assert_called_once_with(
            "Downloading..."
        )
        self.panel.status_changed.emit.assert_called_once_with(
            self.mock_status_card_instance._status, "Downloading..."
        )

    def test_ask_user_input(self):
        result_container = {}
        event = threading.Event()
        with patch(
            "PyQt6.QtWidgets.QInputDialog.getText",
            return_value=("user_input_text", True),
        ) as mock_get_text:
            self.panel._ask_user_input("Enter value:", result_container, event)
            self.assertEqual(result_container["value"], "user_input_text")
            self.assertTrue(event.is_set())
            mock_get_text.assert_called_once_with(
                self.panel, "Richiesta Input", "Enter value:"
            )

        # Test cancel scenario
        result_container = {}
        event = threading.Event()
        with patch(
            "PyQt6.QtWidgets.QInputDialog.getText", return_value=("", False)
        ) as mock_get_text:
            self.panel._ask_user_input("Enter value:", result_container, event)
            self.assertEqual(result_container["value"], "")
            self.assertTrue(event.is_set())
            mock_get_text.assert_called_once_with(
                self.panel, "Richiesta Input", "Enter value:"
            )

    def test_get_credentials(self):
        self.mock_config_manager.get_default_account.return_value = {
            "username": "test_user",
            "password": "test_password",
        }
        username, password = self.panel.get_credentials()
        self.assertEqual(username, "test_user")
        self.assertEqual(password, "test_password")
        self.mock_config_manager.get_default_account.assert_called_once()

        # Test no account
        self.mock_config_manager.get_default_account.return_value = None
        username, password = self.panel.get_credentials()
        self.assertEqual(
            username, "", "Should return empty string for username when no account"
        )
        self.assertEqual(
            password, "", "Should return empty string for password when no account"
        )


if __name__ == "__main__":
    unittest.main()
