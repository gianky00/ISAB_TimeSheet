"""
SyncroJob - Config Defaults
Definizioni predefinite per la configurazione dell'applicazione.
"""

from datetime import UTC, datetime
from typing import Any

from src.core.constants import URLs

# Configurazione di default
DEFAULT_CONFIG: dict[str, Any] = {
    "accounts": [],
    "safework_accounts": [],
    "contracts": [],
    "default_contract": "",
    "browser_headless": False,
    "browser_timeout": 30,
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
    "base_network_path_preventivi": r"\192.168.11.251\Database_Tecnico_SMI\Contabilita' strumentale",
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
        "ATTIVITA' DA COMPLETARE",
        "IN ATTESA TCL",
        "RICHIESTA ODC MIDOLO",
        "CONTABILIZZATA",
    ],
    "reparti": ["STRUMENTALE", "ELETTRICO", "CANTIERE", "ANALISI"],
    "cantieri": [],
    "employee_mappings": {},
    "ai_provider": "gemini",
    "ai_model": "gemini-1.5-pro",
    "ollama_url": URLs.OLLAMA_DEFAULT,
    "quick_actions": ["nav_scarico_ts", "nav_lyra", "cmd_sync", "cmd_open_folder"],
    "statistics": {},
}
