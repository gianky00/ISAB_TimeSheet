from dataclasses import dataclass

from src.bots.base.base_bot import BotConfig
from src.core.constants import Timeouts


@dataclass(frozen=True)
class SeleniumBotConfig(BotConfig):
    username: str = ""
    password: str = ""
    headless: bool = False
    timeout: int = Timeouts.DEFAULT
    download_path: str = ""
    company: str = "ISAB"
