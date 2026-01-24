"""
Facade for backward compatibility.
Delegates to the new modular package src.core.telegram.
"""

from src.core.telegram import TelegramService

__all__ = ["TelegramService"]