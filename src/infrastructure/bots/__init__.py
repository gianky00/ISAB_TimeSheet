"""SyncroJob - Bots Module.

Registry e factory per tutti i bot disponibili.
Supporta motori di automazione multipli (Selenium, Playwright).
"""

from typing import Any, cast

from src.application.services.config_manager import load_config
from src.application.services.constants import Icons
from src.application.services.logging import get_logger
from src.infrastructure.bots.base import BaseBot, BotStatus

# --- IMPORT BOT SELENIUM (Leggeri, rimangono top-level per compatibilità legacy) ---
from src.infrastructure.bots.portale_fornitori.carico_ts.bot import CaricoTSBot
from src.infrastructure.bots.portale_fornitori.dettagli_oda.bot import DettagliOdABot
from src.infrastructure.bots.portale_fornitori.prenota_bp import PrenotaBPBot
from src.infrastructure.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot
from src.infrastructure.bots.portale_fornitori.timbrature.bot import TimbratureBot
from src.infrastructure.bots.safework.pdl.bot import SafeWorkPDLBot
from src.infrastructure.bots.safework.pdl.search_bot import SafeWorkPDLSearchBot
from src.infrastructure.bots.safework.programmazione.bot import SafeWorkProgrammazioneBot
from src.infrastructure.bots.safework.programmazione_sync.bot import SafeWorkProgrammazioneSyncBot

logger = get_logger(__name__)

# --- IMPORT BOT PLAYWRIGHT (Top-level con gestione fallback) ---
try:
    from src.infrastructure.bots.portale_fornitori.carico_ts.playwright_bot import PlaywrightCaricoTSBot
except ImportError:
    PlaywrightCaricoTSBot = None  # type: ignore

try:
    from src.infrastructure.bots.portale_fornitori.dettagli_oda.playwright_bot import PlaywrightDettagliOdABot
except ImportError:
    PlaywrightDettagliOdABot = None  # type: ignore

try:
    from src.infrastructure.bots.portale_fornitori.prenota_bp.playwright_bot import PlaywrightPrenotaBPBot
except ImportError:
    PlaywrightPrenotaBPBot = None  # type: ignore

try:
    from src.infrastructure.bots.portale_fornitori.scarico_ts.playwright_bot import PlaywrightScaricaTSBot
except ImportError:
    PlaywrightScaricaTSBot = None  # type: ignore

try:
    from src.infrastructure.bots.portale_fornitori.timbrature.playwright_bot import PlaywrightTimbratureBot
except ImportError:
    PlaywrightTimbratureBot = None  # type: ignore

try:
    from src.infrastructure.bots.safework.pdl.playwright_bot import PlaywrightSafeWorkPDLBot
except ImportError:
    PlaywrightSafeWorkPDLBot = None  # type: ignore

try:
    from src.infrastructure.bots.safework.pdl.playwright_search_bot import PlaywrightSafeWorkPDLSearchBot
except ImportError:
    PlaywrightSafeWorkPDLSearchBot = None  # type: ignore

try:
    from src.infrastructure.bots.safework.programmazione.playwright_bot import (
        PlaywrightSafeWorkProgrammazioneBot,
    )
except ImportError:
    PlaywrightSafeWorkProgrammazioneBot = None  # type: ignore

try:
    from src.infrastructure.bots.safework.programmazione_sync.playwright_bot import (
        PlaywrightSafeWorkProgrammazioneSyncBot,
    )
except ImportError:
    PlaywrightSafeWorkProgrammazioneSyncBot = None  # type: ignore


def _get_playwright_bot_class(bot_id: str) -> Any:
    """Restituisce la classe bot Playwright corrispondente se disponibile."""
    mapping = {
        "carico_ts": PlaywrightCaricoTSBot,
        "dettagli_oda": PlaywrightDettagliOdABot,
        "prenota_bp": PlaywrightPrenotaBPBot,
        "scarico_ts": PlaywrightScaricaTSBot,
        "timbrature": PlaywrightTimbratureBot,
        "scarico_pdl": PlaywrightSafeWorkPDLBot,
        "ricerca_pdl": PlaywrightSafeWorkPDLSearchBot,
        "programmazione_pdl": PlaywrightSafeWorkProgrammazioneBot,
        "programmazione_sync": PlaywrightSafeWorkProgrammazioneSyncBot,
    }
    return mapping.get(bot_id)


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
    """Crea un'istanza di un bot, scegliendo il motore in base alla configurazione.

    Gestisce la conversione dei parametri in SeleniumBotConfig per la nuova architettura.
    """
    bot_info = BOT_REGISTRY.get(bot_id)
    if not bot_info:
        return None

    engine = load_config().get("automation_engine", "selenium").lower()
    logger.info(f"Factory: Creazione bot '{bot_id}' con motore: {engine}")

    # Estrazione parametri per configurazione standardizzata
    from src.application.services.constants import Timeouts
    from src.infrastructure.bots.base.selenium_bot_config import SeleniumBotConfig

    config_raw = load_config()

    config = SeleniumBotConfig(
        username=kwargs.get("username", ""),
        password=kwargs.get("password", ""),
        headless=kwargs.get("headless", config_raw.get("browser_headless", False)),
        timeout=kwargs.get("timeout", config_raw.get("browser_timeout", Timeouts.DEFAULT)),
        download_path=kwargs.get("download_path", ""),
        company=kwargs.get("company", "ISAB"),
    )

    # Rimuoviamo i parametri già inclusi in config da kwargs per evitare duplicati
    bot_kwargs = {
        k: v
        for k, v in kwargs.items()
        if k not in ("username", "password", "headless", "timeout", "download_path", "company")
    }

    if engine == "playwright":
        bot_class_pw = _get_playwright_bot_class(bot_id)
        if bot_class_pw:
            # Assumiamo che anche i bot Playwright vengano aggiornati a BotConfig
            return cast("BaseBot", bot_class_pw(config=config, **bot_kwargs))

        msg = f"⚠️ Motore Playwright richiesto ma non disponibile per '{bot_id}'. Eseguo fallback su Selenium."
        logger.warning(msg)
        print(f"[!] {msg}")

    # Default / Fallback: Selenium
    bot_class = bot_info["class"]
    return cast("BaseBot", bot_class(config=config, **bot_kwargs))


__all__ = [
    "BOT_REGISTRY",
    "BaseBot",
    "BotStatus",
    "create_bot",
    "get_available_bots",
    "get_bot_info",
]
