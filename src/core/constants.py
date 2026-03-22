"""
SyncroJob - Global Constants
Centralized configuration for the application.
"""

from typing import Final

from src.core import version


class URLs:
    """Application URLs."""

    ISAB_PORTAL = "https://portalefornitori.isab.com/Ui/"
    SAFEWORK_URL = "https://safework.isab.com/"
    UPDATE_URL = version.UPDATE_URL
    OLLAMA_DEFAULT = "http://localhost:11434"
    NET_TIME_CHECK = "https://www.google.com"


class Paths:
    """Standard filesystem paths."""

    LOGS_DIR = "logs"
    DATA_DIR = "data"
    CONFIG_DIR = "config"
    TEMP_DIR = "temp"
    BACKUP_DIR = "backups"


class Business:
    """Business logic constants."""

    # Password standard per i file Excel protetti (ISAB)
    DEFAULT_EXCEL_PASSWORD = "isab"  # noqa: S105

    # Soglia giorni per considerare una password in scadenza (Portale ISAB)
    PWD_EXPIRY_THRESHOLD_DAYS = 5

    # Giorni di validità massima per i certificati di campione
    CERT_VALIDITY_DAYS = 365


class Icons:
    """SVG Icons paths."""

    DIPENDENTI = "assets/icons/users.svg"
    CONTABILITA = "assets/icons/bar-chart.svg"
    DASHBOARD = "assets/icons/layout.svg"
    HELP = "assets/icons/help-circle.svg"
    SETTINGS = "assets/icons/settings.svg"
    REFRESH = "assets/icons/refresh-cw.svg"
    SEARCH = "assets/icons/search.svg"
    FILTER = "assets/icons/filter.svg"
    ALERT = "assets/icons/alert-triangle.svg"
    SUCCESS = "assets/icons/check-circle.svg"
    ERROR = "assets/icons/x-circle.svg"
    INFO = "assets/icons/info.svg"
    CALENDAR = "assets/icons/calendar.svg"
    CLOCK = "assets/icons/clock.svg"
    DOWNLOAD = "assets/icons/download.svg"
    UPLOAD = "assets/icons/upload.svg"
    LOCK = "assets/icons/lock.svg"
    UNLOCK = "assets/icons/unlock.svg"
    USER = "assets/icons/user.svg"
    EDIT = "assets/icons/edit.svg"
    DELETE = "assets/icons/trash-2.svg"
    ADD = "assets/icons/plus.svg"
    SAVE = "assets/icons/save.svg"
    CANCEL = "assets/icons/x.svg"
    CLOSE = "assets/icons/x.svg"
    MENU = "assets/icons/menu.svg"
    CHEVRON_RIGHT = "assets/icons/chevron-right.svg"
    CHEVRON_LEFT = "assets/icons/chevron-left.svg"
    CHEVRON_DOWN = "assets/icons/chevron-down.svg"
    CHEVRON_UP = "assets/icons/chevron-up.svg"
    EYE = "assets/icons/eye.svg"
    EYE_OFF = "assets/icons/eye-off.svg"
    COPY = "assets/icons/copy.svg"
    EXTERNAL_LINK = "assets/icons/external-link.svg"
    MAIL = "assets/icons/mail.svg"
    PHONE = "assets/icons/phone.svg"
    MAP_PIN = "assets/icons/map-pin.svg"
    BUILDING = "assets/icons/building.svg"
    BRIEFCASE = "assets/icons/briefcase.svg"
    ACTIVITY = "assets/icons/activity.svg"
    BELL = "assets/icons/bell.svg"
    BELL_OFF = "assets/icons/bell-off.svg"
    TAG = "assets/icons/tag.svg"
    FLAG = "assets/icons/flag.svg"
    SHIELD = "assets/icons/shield.svg"
    DATABASE = "assets/icons/database.svg"
    TERMINAL = "assets/icons/terminal.svg"
    CODE = "assets/icons/code.svg"
    PLAY = "assets/icons/play.svg"
    STOP = "assets/icons/square.svg"
    PAUSE = "assets/icons/pause.svg"
    SKIP_BACK = "assets/icons/skip-back.svg"
    SKIP_FORWARD = "assets/icons/skip-forward.svg"
    REWIND = "assets/icons/rewind.svg"
    FAST_FORWARD = "assets/icons/fast-forward.svg"
    TRASH = "assets/icons/trash.svg"
    SHARE = "assets/icons/share-2.svg"
    LOG_OUT = "assets/icons/log-out.svg"
    LOG_IN = "assets/icons/log-in.svg"
    USER_PLUS = "assets/icons/user-plus.svg"
    USER_MINUS = "assets/icons/user-minus.svg"
    USER_CHECK = "assets/icons/user-check.svg"
    USER_X = "assets/icons/user-x.svg"
    USERS = "assets/icons/users.svg"
    PRINTER = "assets/icons/printer.svg"
    FILE_TEXT = "assets/icons/file-text.svg"
    FILE_PLUS = "assets/icons/file-plus.svg"
    FILE_MINUS = "assets/icons/file-minus.svg"
    FILE = "assets/icons/file.svg"
    FOLDER = "assets/icons/folder.svg"
    FOLDER_PLUS = "assets/icons/folder-plus.svg"
    FOLDER_MINUS = "assets/icons/folder-minus.svg"
    ARCHIVE = "assets/icons/archive.svg"
    HARD_DRIVE = "assets/icons/hard-drive.svg"
    CPU = "assets/icons/cpu.svg"
    MONITOR = "assets/icons/monitor.svg"
    SMARTPHONE = "assets/icons/smartphone.svg"
    TABLET = "assets/icons/tablet.svg"
    WIFI = "assets/icons/wifi.svg"
    WIFI_OFF = "assets/icons/wifi-off.svg"
    BLUETOOTH = "assets/icons/bluetooth.svg"
    BATTERY = "assets/icons/battery.svg"
    BATTERY_CHARGING = "assets/icons/battery-charging.svg"
    SUN = "assets/icons/sun.svg"
    MOON = "assets/icons/moon.svg"
    CLOUD = "assets/icons/cloud.svg"
    CLOUD_RAIN = "assets/icons/cloud-rain.svg"
    CLOUD_SNOW = "assets/icons/cloud-snow.svg"
    CLOUD_LIGHTNING = "assets/icons/cloud-lightning.svg"
    CLOUD_OFF = "assets/icons/cloud-off.svg"
    WIND = "assets/icons/wind.svg"
    DROPLET = "assets/icons/droplet.svg"
    UMBRELLA = "assets/icons/umbrella.svg"
    THERMOMETER = "assets/icons/thermometer.svg"
    HEART = "assets/icons/heart.svg"
    STAR = "assets/icons/star.svg"
    THUMBS_UP = "assets/icons/thumbs-up.svg"
    THUMBS_DOWN = "assets/icons/thumbs-down.svg"
    MESSAGE_SQUARE = "assets/icons/message-square.svg"
    MESSAGE_CIRCLE = "assets/icons/message-circle.svg"
    SEND = "assets/icons/send.svg"
    LINK = "assets/icons/link.svg"
    LINK_2 = "assets/icons/link-2.svg"
    ATTACHMENT = "assets/icons/paperclip.svg"
    IMAGE = "assets/icons/image.svg"
    MUSIC = "assets/icons/music.svg"
    VIDEO = "assets/icons/video.svg"
    MIC = "assets/icons/mic.svg"
    MIC_OFF = "assets/icons/mic-off.svg"
    HEADPHONES = "assets/icons/headphones.svg"
    VOLUME_2 = "assets/icons/volume-2.svg"
    VOLUME_X = "assets/icons/volume-x.svg"
    MAP = "assets/icons/map.svg"
    NAVIGATION = "assets/icons/navigation.svg"
    COMPASS = "assets/icons/compass.svg"
    GLOBE = "assets/icons/globe.svg"
    PIE_CHART = "assets/icons/pie-chart.svg"
    BAR_CHART_2 = "assets/icons/bar-chart-2.svg"
    LINE_CHART = "assets/icons/line-chart.svg"
    SHOPPING_CART = "assets/icons/shopping-cart.svg"
    SHOPPING_BAG = "assets/icons/shopping-bag.svg"
    CREDIT_CARD = "assets/icons/credit-card.svg"
    DOLLAR_SIGN = "assets/icons/dollar-sign.svg"
    EURO_SIGN = "assets/icons/euro.svg"
    TOOLTIP = "assets/icons/help-circle.svg"
    SYNC = "assets/icons/refresh-cw.svg"
    UPDATE = "assets/icons/arrow-up-circle.svg"
    HISTORY = "assets/icons/history.svg"
    LOGS = "assets/icons/file-text.svg"
    STATS = "assets/icons/trending-up.svg"
    ANALYTICS = "assets/icons/activity.svg"
    TELEGRAM = "assets/icons/send.svg"
    BOT = "assets/icons/cpu.svg"
    AUTOMATION = "assets/icons/zap.svg"
    ROCKET = "assets/icons/rocket.svg"
    SHOE = "assets/icons/footprints.svg"
    STETHOSCOPE = "assets/icons/stethoscope.svg"
    MEDKIT = "assets/icons/briefcase.svg"
    CLIPBOARD = "assets/icons/clipboard.svg"
    TOOL = "assets/icons/tool.svg"
    WRENCH = "assets/icons/tool.svg"
    HAMMER = "assets/icons/tool.svg"
    KEY = "assets/icons/key.svg"
    GIFT = "assets/icons/gift.svg"
    COFFEE = "assets/icons/coffee.svg"
    PIZZA = "assets/icons/coffee.svg"
    PACKAGE = "assets/icons/package.svg"
    TRUCK = "assets/icons/truck.svg"
    BOOK = "assets/icons/book.svg"
    BOOK_OPEN = "assets/icons/book-open.svg"
    LAYERS = "assets/icons/layers.svg"
    GRID = "assets/icons/grid.svg"
    LIST = "assets/icons/list.svg"
    COLUMNS = "assets/icons/columns.svg"
    ROWS = "assets/icons/rows.svg"
    CHECK_SQUARE = "assets/icons/check-square.svg"
    SQUARE = "assets/icons/square.svg"
    CIRCLE = "assets/icons/circle.svg"
    CHECK = "assets/icons/check.svg"
    X = "assets/icons/x.svg"
    ALERT_CIRCLE = "assets/icons/alert-circle.svg"
    ALERT_TRIANGLE = "assets/icons/alert-triangle.svg"
    HELP_CIRCLE = "assets/icons/help-circle.svg"
    INFO_CIRCLE = "assets/icons/info.svg"
    MINUS_CIRCLE = "assets/icons/minus-circle.svg"
    PLUS_CIRCLE = "assets/icons/plus-circle.svg"
    X_CIRCLE = "assets/icons/x-circle.svg"
    CHECK_CIRCLE = "assets/icons/check-circle.svg"
    ARROW_RIGHT = "assets/icons/arrow-right.svg"
    ARROW_LEFT = "assets/icons/arrow-left.svg"
    ARROW_UP = "assets/icons/arrow-up.svg"
    ARROW_DOWN = "assets/icons/arrow-down.svg"
    EXTERNAL = "assets/icons/external-link.svg"
    EYE_SHOW = "assets/icons/eye.svg"
    EYE_HIDE = "assets/icons/eye-off.svg"
    LOGOUT = "assets/icons/log-out.svg"
    LOGIN = "assets/icons/log-in.svg"
    MORE_VERTICAL = "assets/icons/more-vertical.svg"
    MORE_HORIZONTAL = "assets/icons/more-horizontal.svg"
    FILTER_LIST = "assets/icons/filter.svg"
    SORT_ASC = "assets/icons/bar-chart.svg"
    SORT_DESC = "assets/icons/bar-chart.svg"
    DOWNLOAD_CLOUD = "assets/icons/download-cloud.svg"
    UPLOAD_CLOUD = "assets/icons/upload-cloud.svg"
    CLOUD_OFF_CONN = "assets/icons/cloud-off.svg"
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
}
