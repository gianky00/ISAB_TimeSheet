"""
SyncroJob - Global Constants
Centralized configuration for the application.
"""

from enum import Enum


class URLs:
    """Application URLs."""

    ISAB_PORTAL = "https://portalefornitori.isab.com/Ui/"
    UPDATE_URL = "https://projectjob-bot.netlify.app/"


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
    HOME = "assets/icons/home.svg"
    SETTINGS = "assets/icons/settings.svg"
    SETTINGS_DARK = "assets/icons/settings_dark.svg"
    HELP = "assets/icons/help-circle.svg"

    # Actions
    PLAY = "assets/icons/play.svg"
    STOP = "assets/icons/stop.svg"
    REFRESH = "assets/icons/refresh.svg"
    RESET = "assets/icons/reset.svg"
    TRASH = "assets/icons/trash.svg"
    EDIT = "assets/icons/edit.svg"
    FOLDER = "assets/icons/folder.svg"
    FOLDER_OPEN = "assets/icons/folder-open.svg"
    CLOUD = "assets/icons/cloud.svg"
    CLOUD_UPLOAD = "assets/icons/cloud-upload.svg"
    UNDO = "assets/icons/undo.svg"
    PLUS = "assets/icons/plus.svg"
    SEARCH = "assets/icons/search.svg"
    DOWNLOAD = "assets/icons/download.svg"
    UPLOAD = "assets/icons/upload.svg"
    CHEVRON_RIGHT = "assets/icons/chevron-right.svg"
    CHEVRON_DOWN = "assets/icons/chevron-down.svg"
    SEND = "assets/icons/send.svg"

    # Status
    CHECK = "assets/icons/check.svg"
    CHECK_CIRCLE = "assets/icons/check-circle.svg"
    X_CIRCLE = "assets/icons/x-circle.svg"
    ALERT = "assets/icons/alert-triangle.svg"
    LOCK = "assets/icons/lock.svg"
    EYE = "assets/icons/eye.svg"
    EYE_OFF = "assets/icons/eye-off.svg"

    BELL = "assets/icons/bell.svg"
    STAR = "assets/icons/star.svg"
    SHIELD = "assets/icons/shield.svg"
    INFO = "assets/icons/info.svg"

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
    DIPENDENTI = "assets/icons/users.svg"
    PDL = "assets/icons/building.svg"
    FILE_TEXT = "assets/icons/file-text.svg"
    EXCEL = "assets/icons/excel.svg"
    BAR_CHART = "assets/icons/bar-chart.svg"
    ACTIVITY = "assets/icons/activity.svg"
    HEART = "assets/icons/activity.svg"  # Alias per Health (usa activity come fallback)
    GLOBE = "assets/icons/globe.svg"
    MESSAGE_SQUARE = "assets/icons/message-square.svg"
    ALERT_CIRCLE = "assets/icons/alert-circle.svg"
    ALERT_TRIANGLE = "assets/icons/alert-triangle.svg"
    SMART_TOY = "assets/icons/sparkles.svg"  # Fallback/Alias for AI
    TERMINAL = "assets/icons/terminal.svg"
    COMMAND_PALETTE = "assets/icons/command-palette.svg"

    ARCHIVE = "assets/icons/archive.svg"
    LOG_OUT = "assets/icons/log-out.svg"

    # Status Dots
    STATUS_DOT_RED = "assets/icons/status_dot_red.svg"
    STATUS_DOT_ORANGE = "assets/icons/status_dot_orange.svg"
    STATUS_DOT_YELLOW = "assets/icons/status_dot_yellow.svg"
    STATUS_DOT_GREEN = "assets/icons/status_dot_green.svg"
    STATUS_DOT_GRAY = "assets/icons/status_dot_gray.svg"

    # UI Elements
    FLAG_TCL_ON = "assets/icons/flag_tcl_on.svg"
    FLAG_TCL_OFF = "assets/icons/flag_tcl_off.svg"
    FLAG_TGO_ON = "assets/icons/flag_tgo_on.svg"
    FLAG_TGO_OFF = "assets/icons/flag_tgo_off.svg"
