"""
SyncroJob - Global Constants
Centralized configuration for the application.
"""

from enum import Enum
from typing import Final

from src.core import version


class URLs:
    """Application URLs."""

    ISAB_PORTAL = "https://portalefornitori.isab.com/Ui/"
    SAFEWORK_URL = "https://safework.isab.com/"
    UPDATE_URL = version.UPDATE_URL
    OLLAMA_DEFAULT = "http://localhost:11434"
    NET_TIME_CHECK = "https://www.google.com"


class FileNames:
    """Standard file and database names."""

    # Databases
    DB_CONTABILITA = "contabilita.db"
    DB_TIMBRATURE = "timbrature_Isab.db"
    DB_PDL = "pdl.db"
    DB_STORICO_ODA = "storico_oda.db"
    DB_DIPENDENTI = "anagrafica_dipendenti.db"
    DB_AUDIT_LOG = "audit_log.db"

    # Configuration & State
    CONFIG = "config.json"
    SYNC_STATE = "sync_state.json"
    REPORT_HISTORY = "report_history.json"
    NOTIFICATIONS = "notifications.json"
    STATISTICS = "statistics.json"
    LICENSE_MANIFEST = "manifest.json"

    # Logs
    LOG_JSON = "app.json"
    LOG_HUMAN = "app.log"
    LOG_ERRORS = "errors.json"


class Timeouts:
    """Global timeout settings (in seconds)."""

    DEFAULT = 30
    SHORT = 5
    MEDIUM = 15
    LONG = 60
    EXTREME = 600
    OVERLAY = 45
    DOWNLOAD = 25
    PAGE_LOAD = 15
    ELEMENT_WAIT = 20
    DOWNLOAD_WAIT = 120


class Business:
    """Business logic constants."""

    HOURLY_COST_STD = 28.50
    DEFAULT_SUPPLIER = "COEMI"
    DEFAULT_SITE = "ISAB"
    DEFAULT_EXCEL_PASSWORD = "isab"  # noqa: S105


class Emails:
    """Default email recipients and configurations."""

    # Report Accessi Dipendenti
    ACCESSI_TO = "luca.riccio@coemi.it"
    ACCESSI_CC = "isabsud@coemi.it"

    # Programmazione PDL
    PROG_CC = "francesco.millo@coemi.it; ciro.scaravelli@coemi.it"

    # Supporto tecnico
    SUPPORT = "gianky.allegretti@gmail.com"


class BotStatus(Enum):
    """Possible states of a bot."""

    IDLE = "idle"
    INITIALIZING = "initializing"
    LOGGING_IN = "logging_in"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    STOPPED = "stopped"
    CANCELLED = "cancelled"
    PAUSED = "paused"


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
    SPLIT_WINDOW = "assets/icons/split-window.svg"
    FLAG_TGO_ON = "assets/icons/flag_tgo_on.svg"
    FLAG_TGO_OFF = "assets/icons/flag_tgo_off.svg"


# =============================================================================
# SOGLIE OPERATIVE (Business Logic)
# =============================================================================


THRESHOLD_DAYS: Final[dict[str, int]] = {
    "warning": 20,
    "expired": 30,
    "critical": 60,
}

# Colori base usati dai servizi di reportistica (HTML export)
REPORT_COLORS: Final[dict[str, str]] = {
    "primary_dark": "#0d6efd",
    "success_dark": "#198754",
    "warning_orange": "#f39c12",
    "error_red": "#dc3545",
    "bg_light": "#f8f9fa",
    "border_gray": "#dee2e6",
    "text_muted": "#6c757d",
}
