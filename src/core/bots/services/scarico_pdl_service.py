"""Servizio di orchestrazione per il bot Scarico PDL."""

from pathlib import Path
from typing import Any

from src.core import config_manager
from src.core.bots.services.base_service import BaseBotService
from src.core.logging import get_logger

logger = get_logger(__name__)


class ScaricoPDLService(BaseBotService):
    """Implementazione del servizio per lo scarico PDL."""

    def __init__(self) -> None:
        """Inizializza il servizio di scarico PDL."""
        super().__init__("scarico_pdl")

    def load_config(self) -> dict[str, Any]:
        """Carica la configurazione persistente per Scarico PDL."""
        config = config_manager.load_config()
        p_cfg = config.get("last_pdl_params", {})

        dest_path = p_cfg.get("destinazione", "")
        if not dest_path or not Path(dest_path).exists():
            dest_path = str(Path.home() / "Downloads")

        return {
            "stampa": p_cfg.get("stampa", False),
            "stampante": p_cfg.get("stampante", ""),
            "dest_path": dest_path,
            "data": config.get("last_pdl_data", []),
        }

    def save_config(self, params: dict[str, Any], data: list[dict[str, Any]]) -> None:
        """Salva lo stato corrente e i parametri per Scarico PDL."""
        config_manager.set_config_value("last_pdl_data", data)
        config_manager.set_config_value(
            "last_pdl_params",
            {
                "stampa": params.get("stampa", False),
                "stampante": params.get("stampante", ""),
                "destinazione": params.get("dest_path", ""),
            },
        )

    def prepare_payload(
        self,
        credentials: tuple[str, str, str],
        params: dict[str, Any],
        data: list[dict[str, Any]],
        overrides: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Prepara i dati per l'esecuzione del bot Scarico PDL.

        Args:
          credentials: Tupla (username, password, tipo).
          params: Parametri della GUI.
          data: Lista di righe da processare.
          overrides: Eventuali sovrascritture esterne.

        Returns:
          tuple: (bot_params, bot_data).
        """
        username, password, account_type = credentials
        config = config_manager.load_config()

        dest_path = params.get("dest_path") or config_manager.get_download_path()
        stampa = params.get("stampa", False)
        stampante = params.get("stampante", "")

        bot_params = {
            "username": username,
            "password": password,
            "account_type": account_type,
            "headless": config.get("browser_headless", False),
            "timeout": config.get("browser_timeout", 30),
            "download_path": dest_path,
        }

        bot_data = [
            {
                "numero_pdl": it["numero_pdl"],
                "print_enabled": stampa,
                "printer_name": stampante,
                "output_dir": dest_path,
            }
            for it in data
        ]

        return bot_params, bot_data  # type: ignore

    def handle_post_execution(self, success: bool, bot_instance: Any, telegram_service: Any = None) -> None:
        """Esegue l'invio del report a Telegram dopo l'esecuzione."""
        if not success or not telegram_service:
            return

        downloaded_files = getattr(bot_instance, "downloaded_files", [])
        if not downloaded_files:
            return

        try:
            report_path = downloaded_files[0]
            telegram_service.send_document_sync(
                report_path, caption=f"✅ Scarico PDL completato ({len(downloaded_files)} file)"
            )
            logger.info("Report inviato correttamente a Telegram.")
        except Exception:
            logger.exception("Errore invio Telegram")
