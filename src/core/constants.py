"""
Bot TS - Global Constants
Centralized configuration for the application.
"""

from enum import Enum

class URLs:
    """Application URLs."""
    ISAB_PORTAL = "https://portalefornitori.isab.com/Ui/"
    UPDATE_URL = "https://raw.githubusercontent.com/Isab-Bot/Bot-TS-Update/main/"

class Timeouts:
    """Global timeout settings (in seconds)."""
    DEFAULT = 30
    SHORT = 5
    LONG = 60
    OVERLAY = 45
    DOWNLOAD = 25
    PAGE_LOAD = 15

class BotStatus(Enum):
    """Possible states of a bot."""
    IDLE = "idle"
    INITIALIZING = "initializing"
    LOGGING_IN = "logging_in"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    STOPPED = "stopped"

class BrowserConfig:
    """Browser configuration constants."""
    WINDOW_SIZE = "1920,1080"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    CACHE_DIR_NAME = "chrome_profile"
