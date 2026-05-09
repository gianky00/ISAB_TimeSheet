"""
SyncroJob - Bots Module
Registry e factory per tutti i bot disponibili.
Supporta motori di automazione multipli (Selenium, Playwright).
"""

import logging
from typing import Any, cast

from src.bots.base import BaseBot, BotStatus

# --- IMPORT BOT SELENIUM (Leggeri, rimangono top-level per compatibilità legacy) ---
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
from src.core.constants import Icons

logger = logging.getLogger(__name__)


def _get_playwright_bot_class(bot_id: str) -> Any:  # noqa: C901, PLR0911
    """Importa dinamicamente la classe bot Playwright solo quando necessaria (Lazy Loading)."""
    try:
        if bot_id == "carico_ts":
            from src.bots.portale_fornitori.carico_ts.playwright_bot import (  # noqa: PLC0415
                PlaywrightCaricoTSBot,
            )

            return PlaywrightCaricoTSBot
        if bot_id == "dettagli_oda":
            from src.bots.portale_fornitori.dettagli_oda.playwright_bot import (  # noqa: PLC0415
                PlaywrightDettagliOdABot,
            )

            return PlaywrightDettagliOdABot
        if bot_id == "prenota_bp":
            from src.bots.portale_fornitori.prenota_bp.playwright_bot import (  # noqa: PLC0415
                PlaywrightPrenotaBPBot,
            )

            return PlaywrightPrenotaBPBot
        if bot_id == "scarico_ts":
            from src.bots.portale_fornitori.scarico_ts.playwright_bot import (  # noqa: PLC0415
                PlaywrightScaricaTSBot,
            )

            return PlaywrightScaricaTSBot
        if bot_id == "timbrature":
            from src.bots.portale_fornitori.timbrature.playwright_bot import (  # noqa: PLC0415
                PlaywrightTimbratureBot,
            )

            return PlaywrightTimbratureBot
        if bot_id == "scarico_pdl":
            from src.bots.safework.pdl.playwright_bot import PlaywrightSafeWorkPDLBot  # noqa: PLC0415

            return PlaywrightSafeWorkPDLBot
        if bot_id == "ricerca_pdl":
            from src.bots.safework.pdl.playwright_search_bot import (  # noqa: PLC0415
                PlaywrightSafeWorkPDLSearchBot,
            )

            return PlaywrightSafeWorkPDLSearchBot
        if bot_id == "programmazione_pdl":
            from src.bots.safework.programmazione.playwright_bot import (  # noqa: PLC0415
                PlaywrightSafeWorkProgrammazioneBot,
            )

            return PlaywrightSafeWorkProgrammazioneBot
        if bot_id == "programmazione_sync":
            from src.bots.safework.programmazione_sync.playwright_bot import (  # noqa: PLC0415
                PlaywrightSafeWorkProgrammazioneSyncBot,
            )

            return PlaywrightSafeWorkProgrammazioneSyncBot
    except ImportError as e:
        logger.debug(f"Playwright bot per '{bot_id}' non disponibile: {e}")
    return None


# Registry dei bot disponibili
BOT_REGISTRY: dict[str, dict[str, Any]] = {
    "scarico_ts": {
        "class": ScaricaTSBot,
        "name": "Scarico TS",
        "description": "Scarica i timesheet dal portale ISAB",
        "icon": Icons.DOWNLOAD,
        "columns": [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"},
        ],
        "config_key": "last_ts_data",
    },
    "carico_ts": {
        "class": CaricoTSBot,
        "name": "Carico TS",
        "description": "Carica i timesheet sul portale ISAB",
        "icon": Icons.UPLOAD,
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
        "name": "Dettagli OdA",
        "description": "Accede ai Dettagli OdA - browser rimane aperto",
        "icon": Icons.LIST,
        "columns": [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"},
        ],
        "config_key": "last_oda_data",
        "warning": "⚠️ Il browser rimarrà aperto dopo l'esecuzione",
    },
    "prenota_bp": {
        "class": PrenotaBPBot,
        "name": "Prenota BP",
        "description": "Prenotazione Badge Provvisori sul portale ISAB",
        "icon": Icons.TICKET,
        "columns": [
            {"name": "Numero BP", "type": "text"},
            {"name": "Note di Ritiro", "type": "text"},
        ],
        "config_key": "last_prenota_bp_data",
    },
    "timbrature": {
        "class": TimbratureBot,
        "name": "Timbrature",
        "description": "Scarica e archivia le timbrature dal portale ISAB",
        "icon": Icons.CLOCK,
        "columns": [],
        "config_key": "last_timbrature_data",
    },
    "scarico_pdl": {
        "class": SafeWorkPDLBot,
        "name": "Scarico PDL",
        "description": "Scarica e stampa Permessi di Lavoro da SafeWork",
        "icon": Icons.PDL,
        "columns": [{"name": "NUMERO PDL", "type": "text"}],
        "config_key": "last_pdl_data",
    },
    "ricerca_pdl": {
        "class": SafeWorkPDLSearchBot,
        "name": "Ricerca PDL",
        "description": "Ricerca massiva e aggiornamento database PDL",
        "icon": Icons.SEARCH,
        "columns": [],
        "config_key": "last_pdl_search_data",
    },
    "programmazione_pdl": {
        "class": SafeWorkProgrammazioneBot,
        "name": "Programmazione PDL",
        "description": "Monitoraggio programmazione settimanale SafeWork",
        "icon": Icons.CALENDAR,
        "columns": [],
        "config_key": "last_pdl_prog_data",
    },
    "programmazione_sync": {
        "class": SafeWorkProgrammazioneSyncBot,
        "name": "Sincronizzazione Programmazione",
        "description": "Download massivo report attività SafeWork",
        "icon": Icons.REFRESH,
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

    if engine == "playwright":
        bot_class_pw = _get_playwright_bot_class(bot_id)
        if bot_class_pw:
            return cast("BaseBot", bot_class_pw(**kwargs))

        msg = f"⚠️ Motore Playwright richiesto ma non disponibile per '{bot_id}'. Eseguo fallback su Selenium."
        logger.warning(msg)
        print(f"[!] {msg}")

    # Default / Fallback: Selenium
    bot_class = bot_info["class"]
    return cast("BaseBot", bot_class(**kwargs))


__all__ = [
    "BOT_REGISTRY",
    "BaseBot",
    "BotStatus",
    "create_bot",
    "get_available_bots",
    "get_bot_info",
]
