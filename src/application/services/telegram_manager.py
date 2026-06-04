"""Facade for backward compatibility.

Delegates to the new modular package src.application.services.telegram.
"""

from src.api.telegram import TelegramService

__all__ = ["TelegramService"]
