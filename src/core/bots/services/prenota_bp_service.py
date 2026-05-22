"""Servizio di orchestrazione per il bot Prenota BP."""

from datetime import UTC, datetime
from typing import Any

from src.core import config_manager
from src.core.bots.services.base_service import BaseBotService


class PrenotaBPService(BaseBotService):
    """Implementazione del servizio per la prenotazione BP.

    Inizializza il servizio di prenotazione BP.
    """

    def __init__(self) -> None:
        super().__init__("prenota_bp")

    def load_config(self) -> dict[str, Any]:
        """Carica la configurazione persistente per Prenota BP."""
        config = config_manager.load_config()
        current_year = datetime.now(UTC).year

        return {
            "societa": config.get("last_prenota_societa", "ISAB"),
            "fornitore": config.get("last_prenota_bp_fornitore", ""),
            "data_da": config.get("last_prenota_date_from", f"01.01.{current_year}"),
            "data_a": config.get("last_prenota_date_to", f"31.12.{current_year}"),
            "data": config.get("last_prenota_bp_data", []),
        }

    def save_config(self, params: dict[str, Any], data: list[dict[str, Any]]) -> None:
        """Salva lo stato corrente e i parametri per Prenota BP."""
        updates = {
            "last_prenota_bp_data": data,
            "last_prenota_societa": params.get("societa", "ISAB"),
            "last_prenota_bp_fornitore": params.get("fornitore", ""),
            "last_prenota_date_from": params.get("data_da", ""),
            "last_prenota_date_to": params.get("data_a", ""),
        }
        config_manager.set_config_values(updates)

    def prepare_payload(
        self,
        credentials: tuple[str, str, str],
        params: dict[str, Any],
        data: list[dict[str, Any]],
        overrides: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Prepara i dati per l'esecuzione del bot Prenota BP.

        Args:
          credentials: Tupla (username, password, tipo).
          params: Parametri della GUI.
          data: Lista di righe da processare.
          overrides: Eventuali sovrascritture esterne.

        Returns:
          tuple: (bot_params, bot_data).
        """
        username, password, _ = credentials
        config = config_manager.load_config()

        societa = params.get("societa", "ISAB")
        fornitore = params.get("fornitore", "")
        data_da = params.get("data_da", "")
        data_a = params.get("data_a", "")

        if overrides:
            if "fornitore" in overrides:
                fornitore = overrides["fornitore"]
            if "societa" in overrides:
                societa = overrides["societa"]
            if "data_da" in overrides:
                data_da = overrides["data_da"]
            if overrides.get("single_item"):
                data = [overrides["single_item"]]

        bot_params = {
            "username": username,
            "password": password,
            "headless": config.get("browser_headless", False),
            "timeout": config.get("browser_timeout", 30),
            "download_path": config_manager.get_download_path(),
            "fornitore": fornitore,
            "company": societa,
            "data_da": data_da,
            "data_a": data_a,
        }

        bot_data = {
            "rows": data,
            "fornitore": fornitore,
            "company": societa,
            "data_da": data_da,
            "data_a": data_a,
        }

        return bot_params, bot_data
