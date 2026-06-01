from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QObject

from src.core.telegram.bridge.data_processor import TelegramDataProcessor
from src.core.telegram.bridge.intent_handler import TelegramIntentHandler


class TestTelegramBridgeLogic:
    @pytest.fixture
    def mw(self):
        m = QObject()
        m.pdl_panel = MagicMock()
        m.scarico_panel = MagicMock()
        m.navigation_controller = MagicMock()
        m.bot_controller = MagicMock()
        m.show_toast = MagicMock()
        return m

    @pytest.fixture
    def service(self):
        m = MagicMock()
        m.loop = MagicMock()
        m.pending_data = {}
        # Supporto per send_message asincrono se mockato
        m.app.bot.send_message = MagicMock()
        return m

    def test_intent_handler_handle_status(self, mw, service):
        sys_h = MagicMock()
        handler = TelegramIntentHandler(mw, service, sys_h)
        handler.handle_intent(123, {"action": "status"})
        assert sys_h.handle_status.called

    def test_intent_handler_process_pdl_data(self, mw, service):
        handler = TelegramIntentHandler(mw, service)
        intent = {"object": "pdl", "items": ["100000", "200000"]}
        handler.handle_intent(123, intent)
        assert mw.pdl_panel.add_rows_simple.called
        assert mw.show_toast.called

    def test_data_processor_pdl_flow(self, mw, service):
        processor = TelegramDataProcessor(mw, service)
        mw.pdl_panel.data_table.get_data.return_value = []

        processor.process_pdl_items(["123456", "invalid"])

        assert mw.pdl_panel.add_rows_simple.called
        assert "Aggiunti" in service.send_message_sync.call_args[0][0]
        assert "Errori" in service.send_message_sync.call_args[0][0]

    def test_data_processor_oda_flow(self, mw, service):
        processor = TelegramDataProcessor(mw, service)
        mw.scarico_panel.data_table.get_data.return_value = []

        processor.process_oda_items(["ODA123"])

        assert mw.scarico_panel.add_rows_simple.called
        assert mw.navigation_controller.navigate_to_panel.called
        assert "Aggiunti/Impostati 1" in service.send_message_sync.call_args[0][0]

    def test_data_processor_pdl_duplicates(self, mw, service):
        processor = TelegramDataProcessor(mw, service)
        mw.pdl_panel.data_table.get_data.return_value = [{"numero_pdl": "100000/S"}]

        processor.process_pdl_items(["100000"])
        assert not mw.pdl_panel.add_rows_simple.called
        assert "1 duplicati" in service.send_message_sync.call_args[0][0]

    def test_data_processor_bp_items(self, mw, service):
        processor = TelegramDataProcessor(mw, service)
        mock_panel = MagicMock()
        mock_panel.bot_id = "prenota_bp"
        mw.bot_controller._get_active_bot_panel.return_value = mock_panel

        processor.process_bp_items(["12345 Note", "  ", "67890"])

        assert mock_panel.data_table.set_data.called
        data = mock_panel.data_table.set_data.call_args[0][0]
        assert len(data) == 2
        assert data[0]["NUMERO BP"] == "12345"
        assert data[0]["NOTE DI RITIRO"] == "Note"

    def test_data_processor_bp_no_panel(self, mw, service):
        processor = TelegramDataProcessor(mw, service)
        mw.bot_controller._get_active_bot_panel.return_value = None

        processor.process_bp_items(["123"])
        assert not service.send_message_sync.called  # Fallisce prima di inviare feedback se non c'è panel

    def test_data_processor_empty_items(self, mw, service):
        processor = TelegramDataProcessor(mw, service)
        processor.process_pdl_items([])
        assert "Nessun dato valido" in service.send_message_sync.call_args[0][0]
