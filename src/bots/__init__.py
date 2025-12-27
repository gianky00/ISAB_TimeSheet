"""
Bot TS - Bots Module
Registry e factory per tutti i bot disponibili.
"""
from typing import Dict, Any, Optional, Type
from src.bots.base import BaseBot, BotStatus

# Registry dei bot disponibili
BOT_REGISTRY: Dict[str, Dict[str, Any]] = {}

def register_bot(bot_id: str):
    """
    Decorator per registrare un bot nel registry globale.

    Args:
        bot_id: Identificatore univoco del bot
    """
    def decorator(cls: Type[BaseBot]):
        # Cerca metadati nella classe o usa default
        meta = getattr(cls, 'METADATA', {})

        entry = {
            "class": cls,
            "name": meta.get("name", bot_id),
            "description": meta.get("description", ""),
            "icon": meta.get("icon", "🤖"),
            "columns": meta.get("columns", []),
            "config_key": meta.get("config_key", ""),
            "warning": meta.get("warning", "")
        }

        BOT_REGISTRY[bot_id] = entry
        return cls
    return decorator

# --- Imports for Auto-Discovery ---
# Questi import attivano i decoratori @register_bot
from src.bots.scarico_ts import ScaricaTSBot
from src.bots.carico_ts import CaricoTSBot
from src.bots.dettagli_oda import DettagliOdABot
from src.bots.timbrature import TimbratureBot

# --- Legacy Helper Functions ---

def get_available_bots() -> Dict[str, Dict[str, Any]]:
    """Restituisce tutti i bot disponibili."""
    return BOT_REGISTRY

def get_bot_info(bot_id: str) -> Optional[Dict[str, Any]]:
    return BOT_REGISTRY.get(bot_id)

def create_bot(bot_id: str, **kwargs) -> Optional[BaseBot]:
    """
    Crea un'istanza di un bot.
    """
    bot_info = BOT_REGISTRY.get(bot_id)
    if bot_info:
        bot_class = bot_info["class"]
        return bot_class(**kwargs)
    return None

__all__ = [
    'BaseBot',
    'BotStatus',
    'register_bot',
    'BOT_REGISTRY',
    'get_available_bots',
    'get_bot_info',
    'create_bot'
]
