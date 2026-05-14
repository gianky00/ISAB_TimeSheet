from typing import Any

from src.core import config_manager
from src.core.bots.services.base_service import BaseBotService


class ScaricoTSService(BaseBotService):
    def __init__(self) -> None:
        super().__init__("scarico_ts")

    def load_config(self) -> dict[str, Any]:
        config = config_manager.load_config()
        return {
            "societa": config.get("last_scarico_ts_societa", "ISAB"),
            "fornitore": config.get("last_scarico_ts_fornitore", ""),
            "dest_path": config.get("path_scarico_ts", ""),
            "elabora_ts": config.get("last_scarico_ts_elabora", True),
            "data": config.get("last_scarico_ts_data", []),
        }

    def save_config(self, params: dict[str, Any], data: list[dict[str, Any]]) -> None:
        config_manager.set_config_value("last_scarico_ts_data", data)
        config_manager.set_config_value("last_scarico_ts_societa", params.get("societa", ""))
        config_manager.set_config_value("last_scarico_ts_fornitore", params.get("fornitore", ""))
        config_manager.set_config_value("path_scarico_ts", params.get("dest_path", ""))
        config_manager.set_config_value("last_scarico_ts_elabora", params.get("elabora_ts", True))

    def prepare_payload(
        self,
        credentials: tuple[str, str, str],
        params: dict[str, Any],
        data: list[dict[str, Any]],
        overrides: dict[str, Any] | None = None
    ) -> tuple[dict[str, Any], dict[str, Any]]:

        username, password, _ = credentials
        config = config_manager.load_config()

        societa = params.get("societa", "ISAB")
        fornitore = params.get("fornitore", "")
        data_da = params.get("data_da", "")
        download_path = params.get("dest_path") or config_manager.get_download_path()
        elabora_ts = params.get("elabora_ts", True)

        if overrides:
            if "data_da" in overrides:
                data_da = overrides["data_da"]
            if overrides.get("single_item"):
                data = [overrides["single_item"]]

        bot_params = {
            "username": username,
            "password": password,
            "headless": config.get("browser_headless", False),
            "timeout": config.get("browser_timeout", 30),
            "download_path": download_path,
            "data_da": data_da,
            "fornitore": fornitore,
            "company": societa,
            "elabora_ts": elabora_ts,
        }

        bot_data = {
            "rows": data,
            "data_da": data_da,
            "fornitore": fornitore,
            "company": societa,
            "elabora_ts": elabora_ts,
        }

        return bot_params, bot_data
