"""
SyncroJob - Telegram Bridge Interfaces
Definizioni per il de-coupling tra CORE e GUI per le funzioni Telegram.
"""

from typing import Protocol


class ScreenshotProvider(Protocol):
    """Interfaccia per la cattura di screenshot, implementata dalla GUI."""

    def capture_app_screenshot(self) -> bytes:
        """Cattura lo screenshot della finestra principale dell'app."""
        ...

    def capture_desktop_screenshot(self) -> bytes:
        """Cattura lo screenshot dell'intero desktop (multi-monitor)."""
        ...


class AppStatusProvider(Protocol):
    """Interfaccia per il recuperòdello stato dell'app."""

    def get_system_status(self) -> tuple[str, str, str]:
        """Restituisce (bot_name, status, detail)."""
        ...

    def restart_application(self) -> None:
        """Comanda il riavvio dell'app."""
        ...
