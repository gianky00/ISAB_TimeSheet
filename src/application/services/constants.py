"""SyncroJob - Global Constants.

Centralized configuration for the application.
"""

from enum import Enum
from typing import Final

from src.application.services import version


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
    DB_CERTIFICATI = "certificati_campione.db"
    DB_SCARICO_ORE = "scarico_ore.db"
    DB_GIORNALIERE = "giornaliere.db"
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

    DEFAULT = 300
    SHORT = 5
    MEDIUM = 15
    LONG = 60
    EXTREME = 600
    OVERLAY = 90
    DOWNLOAD = 25
    PAGE_LOAD = 15
    ELEMENT_WAIT = 20
    DOWNLOAD_WAIT = 120
    UI_DELAY = 0.5
    SHORT_WAIT = 2


class Business:
    """Business logic constants."""

    HOURLY_COST_STD = 28.50
    DEFAULT_SUPPLIER = "SYNCROJOB"
    DEFAULT_SITE = "ISAB"
    DEFAULT_EXCEL_PASSWORD = "isab"  # nosec B105 # noqa: S105


class Emails:
    """Default email recipients and configurations."""

    # Report Accessi Dipendenti
    ACCESSI_TO = "resp.accessi@example.com"
    ACCESSI_CC = "ufficio.personale@example.com"

    # Programmazione PDL
    PROG_CC = "resp.programmazione@example.com"

    # Supporto tecnico
    SUPPORT = "supporto@syncrojob.it"


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


class UbicazioneStrumenti(Enum):
    """Costanti per le ubicazioni degli strumenti campione."""

    ASSENTE = "ASSENTE"
    UFFICIO_STRU = "UFFICIO STRU"
    UFFICIO_CC = "UFFICIO CAPO CANTIERE"
    OFFICINA = "OFFICINA STRU"
    SEDE = "SEDE"
    TECNICO = "ASSEGNATO AL TECNICO"


class StatoCertificatoLabel:
    """Etichette testuali definitive per gli stati dei certificati."""

    SCADUTO = "Scaduto"
    IN_SCADENZA = "In scadenza"
    ATTIVO = "Attivo"
    SENZA_SCADENZA = "N/D (Senza Scadenza)"
    GUASTO = "STRUMENTO GUASTO"
    CONTROLLO = "IN VALUTAZIONE TECNICA"
    DISMESSO = "DISMESSO"


class TipoAnomalia(Enum):
    """Tipologie di anomalie per strumenti campione."""

    MECCANICO = "Guasto meccanico"
    ELETTRONICO = "Guasto elettronico"
    NON_ACCENDE = "Non si accende"
    FUORI_TOLLERANZA = "Fuori tolleranza"
    DISPLAY_ILLEGGIBILE = "Display illeggibile"
    DANNO_FISICO = "Danno fisico"
    PERDITA_FLUIDO = "Perdita fluido"
    CALIBRAZIONE_IMPOSSIBILE = "Calibrazione impossibile"
    ALTRO = "Altro"


class BrowserConfig:
    """Browser configuration constants."""

    WINDOW_SIZE = "1920,1080"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    CACHE_DIR_NAME = "chrome_profile"


class Icons:
    """Relative paths for application icons."""

    # Navigation
    HOME = "assets/ui/icons/home.svg"
    SETTINGS = "assets/ui/icons/settings.svg"
    SETTINGS_DARK = "assets/ui/icons/settings_dark.svg"
    HELP = "assets/ui/icons/help-circle.svg"

    # Actions
    PLAY = "assets/ui/icons/play.svg"
    STOP = "assets/ui/icons/stop.svg"
    REFRESH = "assets/ui/icons/refresh.svg"
    RESET = "assets/ui/icons/reset.svg"
    TRASH = "assets/ui/icons/trash.svg"
    EDIT = "assets/ui/icons/edit.svg"
    FOLDER = "assets/ui/icons/folder.svg"
    FOLDER_OPEN = "assets/ui/icons/folder-open.svg"
    MAXIMIZE = "assets/ui/icons/maximize.svg"
    MINIMIZE = "assets/ui/icons/minimize.svg"
    CLOUD = "assets/ui/icons/cloud.svg"
    CLOUD_UPLOAD = "assets/ui/icons/cloud-upload.svg"
    UNDO = "assets/ui/icons/undo.svg"
    PLUS = "assets/ui/icons/plus.svg"
    SEARCH = "assets/ui/icons/search.svg"
    DOWNLOAD = "assets/ui/icons/download.svg"
    UPLOAD = "assets/ui/icons/upload.svg"
    CHEVRON_RIGHT = "assets/ui/icons/chevron-right.svg"
    CHEVRON_DOWN = "assets/ui/icons/chevron-down.svg"
    SEND = "assets/ui/icons/send.svg"

    # Status
    CHECK = "assets/ui/icons/check.svg"
    CHECK_CIRCLE = "assets/ui/icons/check-circle.svg"
    X_CIRCLE = "assets/ui/icons/x-circle.svg"
    ALERT = "assets/ui/icons/alert-triangle.svg"
    LOCK = "assets/ui/icons/lock.svg"
    EYE = "assets/ui/icons/eye.svg"
    EYE_OFF = "assets/ui/icons/eye-off.svg"

    BELL = "assets/ui/icons/bell.svg"
    STAR = "assets/ui/icons/star.svg"
    SHIELD = "assets/ui/icons/shield.svg"
    INFO = "assets/ui/icons/info.svg"

    # Domain Specific
    DATABASE = "assets/ui/icons/database.svg"
    CLOCK = "assets/ui/icons/clock.svg"
    LIST = "assets/ui/icons/list.svg"
    TICKET = "assets/ui/icons/ticket.svg"
    ROCKET = "assets/ui/icons/rocket.svg"
    CPU = "assets/ui/icons/cpu.svg"
    SPARKLES = "assets/ui/icons/sparkles.svg"
    CALENDAR = "assets/ui/icons/calendar.svg"
    USER = "assets/ui/icons/user.svg"
    USERS = "assets/ui/icons/users.svg"
    DIPENDENTI = "assets/ui/icons/users.svg"
    PDL = "assets/ui/icons/building.svg"
    FILE_TEXT = "assets/ui/icons/file-text.svg"
    COPY = "assets/ui/icons/file-text.svg"
    EXCEL = "assets/ui/icons/excel.svg"
    BAR_CHART = "assets/ui/icons/bar-chart.svg"
    ACTIVITY = "assets/ui/icons/activity.svg"
    HEART = "assets/ui/icons/activity.svg"  # Alias per Health (usa activity come fallback)
    GLOBE = "assets/ui/icons/globe.svg"
    MESSAGE_SQUARE = "assets/ui/icons/message-square.svg"
    ALERT_CIRCLE = "assets/ui/icons/alert-circle.svg"
    ALERT_TRIANGLE = "assets/ui/icons/alert-triangle.svg"
    SMART_TOY = "assets/ui/icons/sparkles.svg"  # Fallback/Alias for AI
    TERMINAL = "assets/ui/icons/terminal.svg"
    COMMAND_PALETTE = "assets/ui/icons/command-palette.svg"

    ARCHIVE = "assets/ui/icons/archive.svg"
    LOG_OUT = "assets/ui/icons/log-out.svg"

    # Status Dots
    STATUS_DOT_RED = "assets/ui/icons/status_dot_red.svg"
    STATUS_DOT_ORANGE = "assets/ui/icons/status_dot_orange.svg"
    STATUS_DOT_YELLOW = "assets/ui/icons/status_dot_yellow.svg"
    STATUS_DOT_GREEN = "assets/ui/icons/status_dot_green.svg"
    STATUS_DOT_GRAY = "assets/ui/icons/status_dot_gray.svg"
    STATUS_DOT_PURPLE = "assets/ui/icons/status_dot_purple.svg"

    # UI Elements
    FLAG_TCL_ON = "assets/ui/icons/flag_tcl_on.svg"
    FLAG_TCL_OFF = "assets/ui/icons/flag_tcl_off.svg"
    SPLIT_WINDOW = "assets/ui/icons/split-window.svg"
    FLAG_TGO_ON = "assets/ui/icons/flag_tgo_on.svg"
    FLAG_TGO_OFF = "assets/ui/icons/flag_tgo_off.svg"


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
