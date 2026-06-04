from unittest.mock import patch

import pytest

from src.application.services.bots.services.prenota_bp_service import PrenotaBPService


class TestPrenotaBPService:
    @pytest.fixture
    def service(self):
        return PrenotaBPService()

    def test_load_config(self, service):
        with patch("src.application.services.config_manager.load_config") as mock_load:
            mock_load.return_value = {
                "last_prenota_societa": "TEST_SOC",
                "last_prenota_bp_fornitore": "TEST_FORN",
                "last_prenota_date_from": "01.01.2026",
                "last_prenota_date_to": "31.12.2026",
                "last_prenota_bp_data": [{"id": 1}],
            }
            config = service.load_config()
            assert config["societa"] == "TEST_SOC"
            assert config["fornitore"] == "TEST_FORN"
            assert config["data_da"] == "01.01.2026"
            assert config["data_a"] == "31.12.2026"
            assert config["data"] == [{"id": 1}]

    def test_load_config_defaults(self, service):
        with patch("src.application.services.config_manager.load_config") as mock_load:
            mock_load.return_value = {}  # Empty config
            config = service.load_config()
            assert config["societa"] == "ISAB"
            assert config["fornitore"] == ""
            assert "01.01." in config["data_da"]

    def test_save_config(self, service):
        with patch("src.application.services.config_manager.set_config_values") as mock_set:
            params = {"societa": "S1", "fornitore": "F1", "data_da": "D1", "data_a": "D2"}
            data = [{"row": 1}]
            service.save_config(params, data)

            mock_set.assert_called_once()
            updates = mock_set.call_args[0][0]
            assert updates["last_prenota_societa"] == "S1"
            assert updates["last_prenota_bp_data"] == data

    def test_prepare_payload(self, service):
        creds = ("user", "pass", "isab")
        params = {"societa": "S1", "fornitore": "F1", "data_da": "D1", "data_a": "D2"}
        data = [{"id": 100}]

        with patch("src.application.services.config_manager.load_config", return_value={"browser_headless": True}):
            with patch("src.application.services.config_manager.get_download_path", return_value="/tmp"):
                bot_params, bot_data = service.prepare_payload(creds, params, data)

                assert bot_params["username"] == "user"
                assert bot_params["headless"] is True
                assert bot_params["company"] == "S1"
                assert bot_data["rows"] == data

    def test_prepare_payload_overrides(self, service):
        creds = ("u", "p", "sw")
        params = {"societa": "OLD"}
        overrides = {
            "societa": "NEW",
            "fornitore": "FORN_NEW",
            "data_da": "DATE_NEW",
            "single_item": {"id": 999},
        }

        with patch("src.application.services.config_manager.load_config", return_value={}):
            _, bot_data = service.prepare_payload(creds, params, [], overrides=overrides)
            assert bot_data["company"] == "NEW"
            assert bot_data["fornitore"] == "FORN_NEW"
            assert bot_data["data_da"] == "DATE_NEW"
            assert bot_data["rows"] == [{"id": 999}]
