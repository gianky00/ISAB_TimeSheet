import pytest

from src.application.services.bots.services.scarico_ts_service import ScaricoTSService


class TestScaricoTSService:
    @pytest.fixture
    def service(self):
        return ScaricoTSService()

    def test_load_config(self, service, mocker):
        mocker.patch(
            "src.application.services.config_manager.load_config",
            return_value={
                "last_scarico_ts_societa": "ISAB_TEST",
                "last_scarico_ts_fornitore": "FOO",
                "path_scarico_ts": "/path/ts",
                "last_scarico_ts_elabora": False,
                "last_scarico_ts_data": [{"ts": "1"}],
            },
        )

        cfg = service.load_config()
        assert cfg["societa"] == "ISAB_TEST"
        assert cfg["fornitore"] == "FOO"
        assert cfg["dest_path"] == "/path/ts"
        assert cfg["elabora_ts"] is False
        assert len(cfg["data"]) == 1

    def test_save_config(self, service, mocker):
        mock_set = mocker.patch("src.application.services.config_manager.set_config_value")
        params = {"societa": "S", "fornitore": "F", "dest_path": "/D", "elabora_ts": True}
        data = []

        service.save_config(params, data)
        assert mock_set.call_count == 5

    def test_prepare_payload(self, service, mocker):
        creds = ("u", "p", "type")
        params = {
            "societa": "S1",
            "fornitore": "F1",
            "data_da": "01.01.2026",
            "dest_path": "/download",
            "elabora_ts": True,
        }
        data = [{"id": 1}]

        mocker.patch("src.application.services.config_manager.load_config", return_value={})

        bot_params, bot_data = service.prepare_payload(creds, params, data)

        assert bot_params["company"] == "S1"
        assert bot_params["download_path"] == "/download"
        assert bot_data["rows"] == data
        assert bot_data["elabora_ts"] is True

    def test_prepare_payload_overrides(self, service, mocker):
        creds = ("u", "p", "t")
        params = {"data_da": "OLD"}
        overrides = {"data_da": "NEW", "single_item": {"id": 2}}

        mocker.patch("src.application.services.config_manager.load_config", return_value={})
        mocker.patch("src.application.services.config_manager.get_download_path", return_value="/tmp")

        _, bot_data = service.prepare_payload(creds, params, [], overrides=overrides)
        assert bot_data["data_da"] == "NEW"
        assert bot_data["rows"] == [{"id": 2}]
