"""Base service for Bot Automations.

Handles configuration persistence and payload preparation.
"""

from typing import Any

from src.core.logging import get_logger

logger = get_logger(__name__)


class BaseBotService:
    """Classe base per i servizi di orchestrazione dei bot."""

    def __init__(self, bot_id: str) -> None:
        """Inizializza il servizio base del bot.

        Args:
            bot_id: Identificativo unico del bot.
        """
        self.bot_id = bot_id

    def load_config(self) -> dict[str, Any]:
        """Carica la configurazione salvata per questo bot."""
        raise NotImplementedError

    def save_config(self, params: dict[str, Any], data: list[dict[str, Any]]) -> None:
        """Salva la configurazione e i dati correnti."""
        raise NotImplementedError

    def prepare_payload(
        self,
        credentials: tuple[str, str, str],
        params: dict[str, Any],
        data: list[dict[str, Any]],
        overrides: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Prepara bot_params e bot_data per il BotWorker.

        Returns:
            tuple: (bot_params, bot_data).
        """
        raise NotImplementedError

    def handle_post_execution(self, success: bool, bot_instance: Any, telegram_service: Any = None) -> None:
        """Esegue azioni post-completamento (es. invio a Telegram)."""
