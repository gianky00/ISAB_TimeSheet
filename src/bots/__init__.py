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


# --- IMPORT BOT PLAYWRIGHT (Caricamento Granulare) ---
def _safe_import_pw(module_path: str, class_name: str) -> Any | None:
    """Tenta di importare una classe Playwright in modo sicuro."""
    try:
        import importlib  # noqa: PLC0415

        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        logger.debug(f"Playwright bot '{class_name}' non disponibile: {e}")
        return None


# Caricamento individuale per massima robustezza
PW_BOTS = {
    "carico_ts": _safe_import_pw(
        "src.bots.portale_fornitori.carico_ts.playwright_bot", "PlaywrightCaricoTSBot"
    ),
    "dettagli_oda": _safe_import_pw(
        "src.bots.portale_fornitori.dettagli_oda.playwright_bot", "PlaywrightDettagliOdABot"
    ),
    "prenota_bp": _safe_import_pw(
        "src.bots.portale_fornitori.prenota_bp.playwright_bot", "PlaywrightPrenotaBPBot"
    ),
    "scarico_ts": _safe_import_pw(
        "src.bots.portale_fornitori.scarico_ts.playwright_bot", "PlaywrightScaricaTSBot"
    ),
    "timbrature": _safe_import_pw(
        "src.bots.portale_fornitori.timbrature.playwright_bot", "PlaywrightTimbratureBot"
    ),
    "scarico_pdl": _safe_import_pw("src.bots.safework.pdl.playwright_bot", "PlaywrightSafeWorkPDLBot"),
    "ricerca_pdl": _safe_import_pw(
        "src.bots.safework.pdl.playwright_search_bot", "PlaywrightSafeWorkPDLSearchBot"
    ),
    "programmazione_pdl": _safe_import_pw(
        "src.bots.safework.programmazione.playwright_bot", "PlaywrightSafeWorkProgrammazioneBot"
    ),
    "programmazione_sync": _safe_import_pw(
        "src.bots.safework.programmazione_sync.playwright_bot", "PlaywrightSafeWorkProgrammazioneSyncBot"
    ),
}

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
        "warning": "⚠️ Il browser rimarrà aperto dopo l'esecuzione",
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
        "icon": "🔍",
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
        "icon": "🔄",
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
        msg = f"⚠️ Motore Playwright richiesto ma non disponibile per '{bot_id}' (class_pw è None). Eseguo fallback su Selenium."
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
