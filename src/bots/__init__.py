"""
Bot TS - Bots Module
Registry e factory per tutti i bot disponibili.
"""
from typing import Dict, Any, Optional
from src.bots.base import BaseBot, BotStatus
from src.bots.scarico_ts import ScaricaTSBot
from src.bots.carico_ts import CaricoTSBot
from src.bots.dettagli_oda import DettagliOdABot
from src.bots.timbrature import TimbratureBot
from src.bots.hello_bot.bot import HelloBot


# Registry dei bot disponibili
BOT_REGISTRY: Dict[str, Dict[str, Any]] = {
    "scarico_ts": {
        "class": ScaricaTSBot,
        "name": "Scarico TS",
        "description": "Scarica i timesheet dal portale ISAB",
        "icon": "📥",
        "columns": [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"}
        ],
        "config_key": "last_ts_data"
    },
    "carico_ts": {
        "class": CaricoTSBot,
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
            {"name": "G T", "type": "text"}
        ],
        "config_key": "last_carico_ts_data"
    },
    "dettagli_oda": {
        "class": DettagliOdABot,
        "name": "Dettagli OdA",
        "description": "Accede ai Dettagli OdA - browser rimane aperto",
        "icon": "📋",
        "columns": [
            {"name": "Numero OdA", "type": "text"},
            {"name": "Posizione OdA", "type": "text"}
        ],
        "config_key": "last_oda_data",
        "warning": "⚠️ Il browser rimarrà aperto dopo l'esecuzione"
    },
    "timbrature": {
        "class": TimbratureBot,
        "name": "Timbrature",
        "description": "Scarica e archivia le timbrature dal portale ISAB",
        "icon": "⏱️",
        "columns": [],
        "config_key": "last_timbrature_data"
    },
    "hello_bot": {
        "class": HelloBot,
        "name": "Ciao Bot",
        "description": "Un semplice bot che saluta.",
        "icon": "👋",
        "columns": [],
        "config_key": "last_hello_data"
    }
}


def get_available_bots() -> Dict[str, Dict[str, Any]]:
    """Restituisce tutti i bot disponibili."""
    return BOT_REGISTRY


def get_bot_info(bot_id: str) -> Optional[Dict[str, Any]]:
    """
    Restituisce le informazioni di un bot specifico.
    
    Args:
        bot_id: ID del bot
        
    Returns:
        Dict con le informazioni del bot o None
    """
    return BOT_REGISTRY.get(bot_id)


def create_bot(bot_id: str, **kwargs) -> Optional[BaseBot]:
    """
    Crea un'istanza di un bot.
    
    Args:
        bot_id: ID del bot da creare
        **kwargs: Parametri per il costruttore del bot
        
    Returns:
        Istanza del bot o None se non trovato
    """
    bot_info = BOT_REGISTRY.get(bot_id)
    if bot_info:
        bot_class = bot_info["class"]
        return bot_class(**kwargs)
    return None


__all__ = [
    'BaseBot',
    'BotStatus',
    'ScaricaTSBot',
    'CaricoTSBot',
    'DettagliOdABot',
    'TimbratureBot',
    'HelloBot',
    'BOT_REGISTRY',
    'get_available_bots',
    'get_bot_info',
    'create_bot'
]
