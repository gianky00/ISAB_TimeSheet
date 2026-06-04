from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.api.telegram.bridge.system_handler import TelegramSystemHandler


class TestTelegramSystemHandler:
    @pytest.fixture
    def mock_service(self):
        return MagicMock()

    @pytest.fixture
    def mock_screenshot(self):
        m = MagicMock()
        m.capture_app_screenshot.return_value = b"APP_SC"
        m.capture_desktop_screenshot.return_value = b"DSK_SC"
        return m

    @pytest.fixture
    def mock_status(self):
        m = MagicMock()
        m.get_system_status.return_value = ("Bot1", "Running", "Step 5")
        return m

    @pytest.fixture
    def handler(self, mock_service, mock_screenshot, mock_status):
        return TelegramSystemHandler(mock_service, mock_screenshot, mock_status)

    def test_handle_status(self, handler, mock_service):
        handler.handle_status()
        assert mock_service.send_message_sync.called
        msg = mock_service.send_message_sync.call_args[0][0]
        assert "Bot1" in msg

    def test_handle_status_idle(self, handler, mock_service, mock_status):
        mock_status.get_system_status.return_value = ("Idle", "", "")
        handler.handle_status()
        assert "in attesa" in mock_service.send_message_sync.call_args[0][0]

    def test_handle_screenshot_app(self, handler, mock_service):
        handler.handle_screenshot(mode="app")
        # Match esatto con grassetto e spazi
        mock_service.send_photo_sync.assert_called_with(b"APP_SC", caption="   **Screenshot: Solo App**")

    def test_handle_screenshot_desktop(self, handler, mock_service):
        handler.handle_screenshot(mode="desktop")
        mock_service.send_photo_sync.assert_called_with(b"DSK_SC", caption="   **Screenshot: Desktop**")

    @patch("src.api.telegram.bridge.system_handler.ContabilitaManager.search_extended")
    @patch("src.api.telegram.bridge.system_handler.generate_pdf_from_html")
    @patch("src.api.telegram.bridge.system_handler.config_manager.CONFIG_DIR", Path("/config"))
    def test_handle_search_db_pdf_strumentale(self, mock_gen, mock_search, handler, mock_service, fs):
        fs.create_dir("/config/temp")
        mock_search.return_value = {
            "GIORNALIERE": [{"data": "01/01", "personale": "P1", "descrizione": "D1"}]
        }

        # Side effect per creare il file PDF quando viene chiamato il generatore
        def side_effect_gen(html, path):
            fs.create_file(path)
            return True

        mock_gen.side_effect = side_effect_gen

        handler.handle_search_db_pdf({"db": "strumentale", "query": "test"})

        print(f"DEBUG MOCK SERVICE: {mock_service.send_message_sync.call_args_list}")

        assert mock_search.called
        assert mock_gen.called
        assert mock_service.send_document_sync.called
        assert "Report strumentale" in mock_service.send_document_sync.call_args[1]["caption"]

    def test_handle_restart_app(self, handler, mock_status):
        handler.handle_restart_app()
        assert mock_status.restart_application.called
