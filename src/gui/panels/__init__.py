"""
SyncroJob - GUI Panels Module
Modulo contenitore per i pannelli dell'interfaccia utente.
Gli import sono stati rimossi per favorire il lazy loading ed evitare il caricamento di massa all'avvio.
"""

from src.gui.panels.base import BaseBotPanel, BotWorker

__all__ = [
    "BaseBotPanel",
    "BotWorker",
]
