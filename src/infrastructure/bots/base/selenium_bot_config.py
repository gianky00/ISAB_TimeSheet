"""Configurazione specifica per i bot basati su Selenium."""

from dataclasses import dataclass

from src.application.services.constants import Timeouts
from src.infrastructure.bots.base.base_bot import BotConfig


@dataclass(frozen=True)
class SeleniumBotConfig(BotConfig):
    """Configurazione per i bot Selenium."""

    username: str = ""
    password: str = ""
    headless: bool = False
    timeout: int = Timeouts.DEFAULT
    download_path: str = ""
    company: str = "ISAB"
