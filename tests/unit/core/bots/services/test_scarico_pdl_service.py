from unittest.mock import MagicMock

from src.core.bots.services.scarico_pdl_service import ScaricoPDLService


class TestScaricoPDLService:
    def test_load_config(self, mocker):
        mocker.patch(
            "src.core.config_manager.load_config",
            return_value={
                "last_pdl_params": {"stampa": True, "destinazione": "/fake"},
                "last_pdl_data": [{"numero_pdl": "123"}],
            },
        )
        mocker.patch("pathlib.Path.exists", return_value=True)

        service = ScaricoPDLService()
        cfg = service.load_config()

        assert cfg["stampa"] is True
        assert cfg["dest_path"] == "/fake"
        assert len(cfg["data"]) == 1

    def test_save_config(self, mocker):
        mock_set = mocker.patch("src.core.config_manager.set_config_value")
        service = ScaricoPDLService()

        params = {"stampa": False, "dest_path": "/new"}
        data = [{"pdl": "1"}]
        service.save_config(params, data)

        assert mock_set.call_count == 2
        mock_set.assert_any_call("last_pdl_data", data)

    def test_prepare_payload(self, mocker):
        mocker.patch("src.core.config_manager.load_config", return_value={"browser_headless": True})
        service = ScaricoPDLService()

        creds = ("user", "pass", "type")
        params = {"stampa": True, "stampante": "HP", "dest_path": "/tmp"}
        data = [{"numero_pdl": "PDL1"}]

        bot_params, bot_data = service.prepare_payload(creds, params, data)

        assert bot_params["username"] == "user"
        assert bot_params["headless"] is True
        assert bot_data[0]["numero_pdl"] == "PDL1"
        assert bot_data[0]["print_enabled"] is True

    def test_handle_post_execution_telegram(self, mocker):
        service = ScaricoPDLService()
        mock_bot = MagicMock()
        mock_bot.downloaded_files = ["/path/to/file.pdf"]
        mock_telegram = MagicMock()

        service.handle_post_execution(True, mock_bot, mock_telegram)

        assert mock_telegram.send_document_sync.called
        args, kwargs = mock_telegram.send_document_sync.call_args
        assert args[0] == "/path/to/file.pdf"
        assert "Scarico PDL" in kwargs["caption"]
