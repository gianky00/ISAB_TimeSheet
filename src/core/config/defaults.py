"""
SyncroJob - Config Defaults
Definizioni predefinite per la configurazione dell'applicazione.
"""

from datetime import UTC, datetime
from typing import Any

# Configurazione di default
DEFAULT_CONFIG: dict[str, Any] = {
    "accounts": [],
    "safework_accounts": [],
    "contracts": [],
    "default_contract": "",
    "automation_engine": "selenium",  # Motore di automazione (selenium o playwright)
    "browser_headless": False,
    "browser_timeout": 300,
    "download_path": "",
    "fornitori": [],
    "last_ts_data": [],
    "last_ts_date": f"01.01.{datetime.now(UTC).year}",
    "last_ts_fornitore": "",
    "last_carico_ts_data": [],
    "last_oda_data": [],
    "contabilita_file_path": "",
    "enable_auto_update_contabilita": True,
    "certificati_campione_path": "",
    "master_preventivi_path": "",
    "base_network_path_preventivi": r"\\192.168.11.251\Database_Tecnico_SMI\Contabilità strumentale",
    "preventivi_tcl": [
        "MESSINA I.",
        "AGUSTA D.",
        "CALDARELLA F.",
        "PREZZAVENTO M.",
        "BOSCO F.",
        "RUGGIERI F.",
        "BARBAGALLO G.",
    ],
    "preventivi_stati": [
        "ATTIVITÀ DA COMPLETARE",
        "IN ATTESA TCL",
        "RICHIESTA ODC MIDOLO",
        "CONTABILIZZATA",
    ],
    "reparti": ["STRUMENTALE", "ELETTRICO", "CANTIERE", "ANALISI"],
    "cantieri": [],
    "employee_mappings": {},
    "quick_actions": ["nav_scarico_ts", "cmd_sync", "cmd_open_folder"],
    "roi_weights": {
        "Scarico TS": 5.0,
        "Carico TS": 8.0,
        "Dettagli ODA": 3.0,
        "Prenota BP": 10.0,
        "Scarico PDL": 12.0,
        "Ricerca PDL": 2.0,
        "Sincronizzazione": 1.0,
        "Export Excel": 5.0,
    },
    "certificati_autopilot_enabled": False,
    "certificati_autopilot_time": "08:30",
    "certificati_autopilot_interval_days": 1,
    "certificati_autopilot_last_sent": None,
    "statistics": {},
    "weather_show_details": False,
}
