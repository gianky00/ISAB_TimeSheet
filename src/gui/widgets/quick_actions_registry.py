from typing import Any

from src.core.constants import Icons
from src.gui.styles import COLORS

# Registry of all available actions with 3-level hierarchy
# Path format: [Level1, Level2] - excludes the action text itself
# Level 1 & 2 are non-selectable groups, Level 3 items are selectable
AVAILABLE_ACTIONS: dict[str, dict[str, Any]] = {
    # ============================================================
    # PRIMO LIVELLO: Automazioni > SECONDO LIVELLO: Portale Fornitori
    # ============================================================
    "nav_dettagli_oda": {
        "text": "Dettagli OdA (bot)",
        "icon": Icons.LIST,
        "color": COLORS["purple"],
        "path": ["Automazioni", "Portale Fornitori"],
    },
    "nav_scarico_ts": {
        "text": "Scarico TS (bot)",
        "icon": Icons.DOWNLOAD,
        "color": COLORS["primary_dark"],
        "path": ["Automazioni", "Portale Fornitori"],
    },
    "nav_carico_ts": {
        "text": "Carico TS (bot)",
        "icon": Icons.UPLOAD,
        "color": COLORS["teal_light"],
        "path": ["Automazioni", "Portale Fornitori"],
    },
    "pf_timbrature": {
        "text": "Timbrature (bot)",
        "icon": Icons.CLOCK,
        "color": COLORS["warning_orange"],
        "path": ["Automazioni", "Portale Fornitori"],
    },
    "pf_prenota_bp": {
        "text": "Prenota BP (bot)",
        "icon": Icons.CALENDAR,
        "color": COLORS["success_dark"],
        "path": ["Automazioni", "Portale Fornitori"],
    },
    # ============================================================
    # PRIMO LIVELLO: Automazioni > SECONDO LIVELLO: SafeWork
    # ============================================================
    "nav_scarico_pdl": {
        "text": "Scarico PDL (bot)",
        "icon": Icons.SHIELD,
        "color": COLORS["success_dark"],
        "path": ["Automazioni", "SafeWork"],
    },
    "nav_ricerca_pdl": {
        "text": "Ricerca PDL (bot)",
        "icon": Icons.SEARCH,
        "color": COLORS["success_dark"],
        "path": ["Automazioni", "SafeWork"],
    },
    # ============================================================
    # PRIMO LIVELLO: DataBase > SECONDO LIVELLO: Strumentale
    # ============================================================
    "nav_sub_strumentale_0": {
        "text": "Preventivi",
        "icon": Icons.FOLDER,
        "color": COLORS["warning_orange"],
        "path": ["Strumentale"],
    },
    "nav_sub_strumentale_1": {
        "text": "Giornaliere",
        "icon": Icons.CLOCK,
        "color": COLORS["warning_orange"],
        "path": ["Strumentale"],
    },
    "nav_sub_strumentale_2": {
        "text": "Attività Programmate",
        "icon": Icons.CALENDAR,
        "color": COLORS["warning_orange"],
        "path": ["Strumentale"],
    },
    "nav_sub_strumentale_3": {
        "text": "Certificati Campione",
        "icon": Icons.FILE_TEXT,
        "color": COLORS["warning_orange"],
        "path": ["Strumentale"],
    },
    "nav_sub_strumentale_4": {
        "text": "Analisi KPI",
        "icon": Icons.BAR_CHART,
        "color": COLORS["warning_orange"],
        "path": ["Strumentale"],
    },
    # ============================================================
    # PRIMO LIVELLO: DataBase > SECONDO LIVELLO: DataEase
    # ============================================================
    "nav_page_5": {
        "text": "DataEase",
        "icon": Icons.DOWNLOAD,
        "color": COLORS["warning_orange"],
        "path": ["DataBase"],
    },
    # ============================================================
    # PRIMO LIVELLO: DataBase > SECONDO LIVELLO: PDL
    # ============================================================
    "nav_page_6": {
        "text": "PDL",
        "icon": Icons.PDL,
        "color": COLORS["warning_orange"],
        "path": ["DataBase"],
    },
    "nav_page_11": {
        "text": "Dipendenti",
        "icon": Icons.DIPENDENTI,
        "color": COLORS["warning_orange"],
        "path": ["DataBase"],
    },
    "nav_storico_oda": {
        "text": "Storico OdA",
        "icon": Icons.FILE_TEXT,
        "color": COLORS["warning_orange"],
        "path": ["DataBase"],
    },
    # ============================================================
    # PRIMO LIVELLO: Notifiche > SECONDO LIVELLO: Audit
    # ============================================================
    "nav_sub_notifiche_1": {
        "text": "Audit",
        "icon": Icons.SHIELD,
        "color": COLORS["warning_yellow"],
        "path": ["Notifiche"],
    },
    # ============================================================
    # PRIMO LIVELLO: Impostazioni > SECONDO LIVELLO: Items
    # ============================================================
    "settings_configurazione": {
        "text": "Configurazione",
        "icon": Icons.SETTINGS,
        "color": COLORS["text_muted"],
        "path": ["Impostazioni"],
    },
    "settings_backup_cloud": {
        "text": "Backup Cloud",
        "icon": Icons.CLOUD,
        "color": COLORS["text_muted"],
        "path": ["Impostazioni"],
    },
    "settings_statistiche": {
        "text": "Statistiche",
        "icon": Icons.BAR_CHART,
        "color": COLORS["text_muted"],
        "path": ["Impostazioni"],
    },
    "settings_telegram": {
        "text": "Telegram",
        "icon": Icons.MESSAGE_SQUARE,
        "color": COLORS["text_muted"],
        "path": ["Impostazioni"],
    },
    # ============================================================
    # PRIMO LIVELLO: Guida (selectable root)
    # ============================================================
    "nav_page_8": {
        "text": "Guida",
        "icon": Icons.HELP,
        "color": COLORS["cyan_info"],
        "path": [],
    },
}
