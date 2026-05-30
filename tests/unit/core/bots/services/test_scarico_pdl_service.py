from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.core.bots.services.scarico_pdl_service import ScaricoPDLService


class TestScaricoPDLService:
    @pytest.fixture
    def service(self):
        return ScaricoPDLService()

    def test_load_config(self, service, mocker):
        mocker.patch(
            "src.core.config_manager.load_config",
            return_value={
                "last_pdl_params": {"stampa": True, "stampante": "HP-Laser", "destinazione": "/tmp/pdl"},
                "last_pdl_data": [{"numero_pdl": "123"}],
            },
        )
        # Mock Path.exists for the destination
        mocker.patch("src.core.bots.services.scarico_pdl_service.Path.exists", return_value=True)

        cfg = service.load_config()
        assert cfg["stampa"] is True
        assert cfg["stampante"] == "HP-Laser"
        assert cfg["dest_path"] == "/tmp/pdl"
        assert len(cfg["data"]) == 1

    def test_load_config_fallback_path(self, service, mocker):
        mocker.patch("src.core.config_manager.load_config", return_value={})
        mocker.patch("src.core.bots.services.scarico_pdl_service.Path.home", return_value=Path("/home/user"))

        cfg = service.load_config()
        assert "Downloads" in cfg["dest_path"]

    def test_save_config(self, service, mocker):
        mock_set = mocker.patch("src.core.config_manager.set_config_value")
        params = {"stampa": False, "stampante": "None", "dest_path": "/out"}
        data = [{"id": 1}]

        service.save_config(params, data)

        assert mock_set.call_count == 2
        # Check params structure
        args = mock_set.call_args_list[1][0]
        assert args[0] == "last_pdl_params"
        assert args[1]["destinazione"] == "/out"

    def test_prepare_payload(self, service, mocker):
        creds = ("u", "p", "safework")
        params = {"dest_path": "/custom", "stampa": True, "stampante": "PRN"}
        data = [{"numero_pdl": "PDL-001"}]

        mocker.patch("src.core.config_manager.load_config", return_value={"browser_headless": False})

        bot_params, bot_data = service.prepare_payload(creds, params, data)

        assert bot_params["username"] == "u"
        assert bot_params["download_path"] == "/custom"
        assert len(bot_data) == 1
        assert bot_data[0]["numero_pdl"] == "PDL-001"
        assert bot_data[0]["print_enabled"] is True

    def test_handle_post_execution_telegram(self, service, mocker):
        mock_tg = MagicMock()
        mock_bot = MagicMock()
        mock_bot.downloaded_files = ["/tmp/report.pdf"]

        service.handle_post_execution(True, mock_bot, mock_tg)

        mock_tg.send_document_sync.assert_called_once_with(
            "/tmp/report.pdf", caption="✅ Scarico PDL completato (1 file)"
        )

    def test_handle_post_execution_no_files(self, service):
        mock_tg = MagicMock()
        mock_bot = MagicMock()
        mock_bot.downloaded_files = []

        service.handle_post_execution(True, mock_bot, mock_tg)
        mock_tg.send_document_sync.assert_not_called()
