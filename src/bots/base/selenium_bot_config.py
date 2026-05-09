from dataclasses import dataclass
from src.core.constants import Timeouts

@dataclass(frozen=True)
class SeleniumBotConfig:
    username: str
    password: str
    headless: bool = False
    timeout: int = Timeouts.DEFAULT
    download_path: str = ""
    company: str = "ISAB"
