"""
SyncroJob - Bots Module
Registry e factory per tutti i bot disponibili.
Supporta motori di automazione multipli (Selenium, Playwright).
"""

import logging
from typing import Any, cast

from src.bots.base import BaseBot, BotStatus

# --- IMPORT BOT SELENIUM (Sempre disponibili come fallback) ---
from src.bots.portale_fornitori.carico_ts.bot import CaricoTSBot
from src.bots.portale_fornitori.dettagli_oda.bot import DettagliOdABot
from src.bots.portale_fornitori.prenota_bp import PrenotaBPBot
from src.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot
from src.bots.portale_fornitori.timbrature.bot import TimbratureBot
from src.bots.safework.pdl.bot import SafeWorkPDLBot
from src.bots.safework.pdl.search_bot import SafeWorkPDLSearchBot
from src.bots.safework.programmazione.bot import SafeWorkProgrammazioneBot
from src.bots.safework.programmazione_sync.bot import SafeWorkProgrammazioneSyncBot
from src.core.config_manager import load_config

logger = logging.getLogger(__name__)


# --- IMPORT BOT PLAYWRIGHT (Gestione nativa per PyInstaller) ---
PW_BOTS: dict[str, Any] = {
    "carico_ts": None,
    "dettagli_oda": None,
    "prenota_bp": None,
    "scarico_ts": None,
    "timbrature": None,
    "scarico_pdl": None,
    "ricerca_pdl": None,
    "programmazione_pdl": None,
    "programmazione_sync": None,
}

try:
    from src.bots.portale_fornitori.carico_ts.playwright_bot import PlaywrightCaricoTSBot

    PW_BOTS["carico_ts"] = PlaywrightCaricoTSBot
except ImportError as e:
    logger.debug(f"Playwright bot 'PlaywrightCaricoTSBot' non disponibile: {e}")

try:
    from src.bots.portale_fornitori.dettagli_oda.playwright_bot import PlaywrightDettagliOdABot

    PW_BOTS["dettagli_oda"] = PlaywrightDettagliOdABot
except ImportError as e:
    logger.debug(f"Playwright bot 'PlaywrightDettagliOdABot' non disponibile: {e}")

try:
    from src.bots.portale_fornitori.prenota_bp.playwright_bot import PlaywrightPrenotaBPBot

    PW_BOTS["prenota_bp"] = PlaywrightPrenotaBPBot
except ImportError as e:
    logger.debug(f"Playwright bot 'PlaywrightPrenotaBPBot' non disponibile: {e}")

try:
    from src.bots.portale_fornitori.scarico_ts.playwright_bot import PlaywrightScaricaTSBot

    PW_BOTS["scarico_ts"] = PlaywrightScaricaTSBot
except ImportError as e:
    logger.debug(f"Playwright bot 'PlaywrightScaricaTSBot' non disponibile: {e}")

try:
    from src.bots.portale_fornitori.timbrature.playwright_bot import PlaywrightTimbratureBot

    PW_BOTS["timbrature"] = PlaywrightTimbratureBot
except ImportError as e:
    logger.debug(f"Playwright bot 'PlaywrightTimbratureBot' non disponibile: {e}")

try:
    from src.bots.safework.pdl.playwright_bot import PlaywrightSafeWorkPDLBot

    PW_BOTS["scarico_pdl"] = PlaywrightSafeWorkPDLBot
except ImportError as e:
    logger.debug(f"Playwright bot 'PlaywrightSafeWorkPDLBot' non disponibile: {e}")

try:
    from src.bots.safework.pdl.playwright_search_bot import PlaywrightSafeWorkPDLSearchBot

    PW_BOTS["ricerca_pdl"] = PlaywrightSafeWorkPDLSearchBot
except ImportError as e:
    logger.debug(f"Playwright bot 'PlaywrightSafeWorkPDLSearchBot' non disponibile: {e}")

try:
    from src.bots.safework.programmazione.playwright_bot import PlaywrightSafeWorkProgrammazioneBot

    PW_BOTS["programmazione_pdl"] = PlaywrightSafeWorkProgrammazioneBot
except ImportError as e:
    logger.debug(f"Playwright bot 'PlaywrightSafeWorkProgrammazioneBot' non disponibile: {e}")

try:
    from src.bots.safework.programmazione_sync.playwright_bot import PlaywrightSafeWorkProgrammazioneSyncBot

    PW_BOTS["programmazione_sync"] = PlaywrightSafeWorkProgrammazioneSyncBot
except ImportError as e:
    logger.debug(f"Playwright bot 'PlaywrightSafeWorkProgrammazioneSyncBot' non disponibile: {e}")

# Registry dei bot disponibili
BOT_REGISTRY: dict[str, dict[str, Any]] = {
    "scarico_ts": {
        "class": ScaricaTSBot,
        "class_pw": PW_BOTS["scarico_ts"],
        "name": "Scarico TS",
        "description": "Scarica i timesheet dal portale ISAB",
        "icon": "📥",
        "columns": [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"},
        ],
        "config_key": "last_ts_data",
    },
    "carico_ts": {
        "class": CaricoTSBot,
        "class_pw": PW_BOTS["carico_ts"],
        "name": "Carico TS",
        "description": "Carica i timesheet sul portale ISAB",
        "icon": "📤",
        "columns": [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"},
            {"name": "Codice Fiscale", "type": "text"},
            {"name": "Ingresso", "type": "text"},
            {"name": "Uscita", "type": "text"},
            {"name": "Tipo Prestazione", "type": "text"},
            {"name": "C", "type": "text"},
            {"name": "M", "type": "text"},
            {"name": "Str D", "type": "text"},
            {"name": "Str N", "type": "text"},
            {"name": "Str F D", "type": "text"},
            {"name": "Str F N", "type": "text"},
            {"name": "Sq", "type": "text"},
            {"name": "Nota D", "type": "text"},
            {"name": "Nota S", "type": "text"},
            {"name": "F S", "type": "text"},
            {"name": "G T", "type": "text"},
        ],
        "config_key": "last_carico_ts_data",
    },
    "dettagli_oda": {
        "class": DettagliOdABot,
        "class_pw": PW_BOTS["dettagli_oda"],
        "name": "Dettagli OdA",
        "description": "Accede ai Dettagli OdA - browser rimane aperto",
        "icon": "📋",
        "columns": [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"},
        ],
        "config_key": "last_oda_data",
        "warning": "[ATTENZIONE] Il browser rimarrà aperto dopo l'esecuzione",
    },
    "prenota_bp": {
        "class": PrenotaBPBot,
        "class_pw": PW_BOTS["prenota_bp"],
        "name": "Prenota BP",
        "description": "Prenotazione Badge Provvisori sul portale ISAB",
        "icon": "🎫",
        "columns": [
            {"name": "Numero BP", "type": "text"},
            {"name": "Note di Ritiro", "type": "text"},
        ],
        "config_key": "last_prenota_bp_data",
    },
    "timbrature": {
        "class": TimbratureBot,
        "class_pw": PW_BOTS["timbrature"],
        "name": "Timbrature",
        "description": "Scarica e archivia le timbrature dal portale ISAB",
        "icon": "⏱️",
        "columns": [],
        "config_key": "last_timbrature_data",
    },
    "scarico_pdl": {
        "class": SafeWorkPDLBot,
        "class_pw": PW_BOTS["scarico_pdl"],
        "name": "Scarico PDL",
        "description": "Scarica e stampa Permessi di Lavoro da SafeWork",
        "icon": "🛡️",
        "columns": [{"name": "NUMERO PDL", "type": "text"}],
        "config_key": "last_pdl_data",
    },
    "ricerca_pdl": {
        "class": SafeWorkPDLSearchBot,
        "class_pw": PW_BOTS["ricerca_pdl"],
        "name": "Ricerca PDL",
        "description": "Ricerca massiva e aggiornamento database PDL",
        "icon": "[CERCA]",
        "columns": [],
        "config_key": "last_pdl_search_data",
    },
    "programmazione_pdl": {
        "class": SafeWorkProgrammazioneBot,
        "class_pw": PW_BOTS["programmazione_pdl"],
        "name": "Programmazione PDL",
        "description": "Monitoraggio programmazione settimanale SafeWork",
        "icon": "📅",
        "columns": [],
        "config_key": "last_pdl_prog_data",
    },
    "programmazione_sync": {
        "class": SafeWorkProgrammazioneSyncBot,
        "class_pw": PW_BOTS["programmazione_sync"],
        "name": "Sincronizzazione Programmazione",
        "description": "Download massivo report attività SafeWork",
        "icon": "[SYNC]",
        "columns": [],
        "config_key": "last_prog_sync_data",
    },
}


def get_available_bots() -> dict[str, dict[str, Any]]:
    """Restituisce tutti i bot disponibili."""
    return BOT_REGISTRY


def get_bot_info(bot_id: str) -> dict[str, Any] | None:
    """Restituisce le informazioni di un bot specifico."""
    return BOT_REGISTRY.get(bot_id)


def create_bot(bot_id: str, **kwargs: Any) -> BaseBot | None:
    """
    Crea un'istanza di un bot, scegliendo il motore in base alla configurazione.
    """
    bot_info = BOT_REGISTRY.get(bot_id)
    if not bot_info:
        return None

    engine = load_config().get("automation_engine", "selenium").lower()

    logger.info(f"Factory: Creazione bot '{bot_id}' con motore: {engine}")

    bot_class = bot_info["class"]
    if engine == "playwright" and bot_info.get("class_pw"):
        bot_class = bot_info["class_pw"]
    elif engine == "playwright":
        msg = f"[ATTENZIONE] Motore Playwright richiesto ma non disponibile per '{bot_id}' (class_pw è None). Eseguo fallback su Selenium."
        logger.warning(msg)
        print(f"[!] {msg}")  # Output visibile se eseguito da console

    return cast("BaseBot", bot_class(**kwargs))


__all__ = [
    "BOT_REGISTRY",
    "BaseBot",
    "BotStatus",
    "create_bot",
    "get_available_bots",
    "get_bot_info",
]
