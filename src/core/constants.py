"""
SyncroJob - Global Constants
Centralized configuration for the application.
"""

from enum import Enum


class URLs:
    """Application URLs."""

    ISAB_PORTAL = "https://portalefornitori.isab.com/Ui/"
    UPDATE_URL = "https://raw.githubusercontent.com/Isab-Bot/SyncroJob-Update/main/"


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


class Icons:
    """Relative paths for application icons."""

    # Navigation
    MENU = "assets/icons/menu.svg"
    HOME = "assets/icons/home.svg"
    SETTINGS = "assets/icons/settings.svg"
    SETTINGS_DARK = "assets/icons/settings_dark.svg"
    HELP = "assets/icons/help-circle.svg"

    # Actions
    PLAY = "assets/icons/play.svg"
    STOP = "assets/icons/stop.svg"
    REFRESH = "assets/icons/refresh.svg"
    TRASH = "assets/icons/trash.svg"
    EDIT = "assets/icons/edit.svg"
    SAVE = "assets/icons/save.svg"
    FOLDER = "assets/icons/folder.svg"
    FOLDER_OPEN = "assets/icons/folder-open.svg"
    CLOUD = "assets/icons/cloud.svg"
    CLOUD_UPLOAD = "assets/icons/cloud-upload.svg"
    UNDO = "assets/icons/undo.svg"
    PLUS = "assets/icons/plus.svg"
    SEARCH = "assets/icons/search.svg"
    DOWNLOAD = "assets/icons/download.svg"
    UPLOAD = "assets/icons/upload.svg"
    SEND = "assets/icons/send.svg"

    # Status
    CHECK_CIRCLE = "assets/icons/check-circle.svg"
    X_CIRCLE = "assets/icons/x-circle.svg"
    ALERT = "assets/icons/alert-triangle.svg"
    LOCK = "assets/icons/lock.svg"
    EYE = "assets/icons/eye.svg"
    EYE_OFF = "assets/icons/eye-off.svg"
    BELL = "assets/icons/bell.svg"
    STAR = "assets/icons/star.svg"
    KEY = "assets/icons/key.svg"
    SHIELD = "assets/icons/shield.svg"

    # Domain Specific
    DATABASE = "assets/icons/database.svg"
    CLOCK = "assets/icons/clock.svg"
    LIST = "assets/icons/list.svg"
    TICKET = "assets/icons/ticket.svg"
    ROCKET = "assets/icons/rocket.svg"
    CPU = "assets/icons/cpu.svg"
    SPARKLES = "assets/icons/sparkles.svg"
    CALENDAR = "assets/icons/calendar.svg"
    USER = "assets/icons/user.svg"
    USERS = "assets/icons/users.svg"
    FILE_TEXT = "assets/icons/file-text.svg"
    BAR_CHART = "assets/icons/bar-chart.svg"
    BUILDING = "assets/icons/building.svg"
    GLOBE = "assets/icons/globe.svg"
