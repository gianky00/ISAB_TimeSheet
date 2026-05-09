"""
SyncroJob - Screenshot Bridge
Implementazione GUI delle interfacce Telegram per cattura screenshot e stato.
Segue SRP isolando PySide6.
"""

import os
import subprocess
from contextlib import suppress
from typing import Any, cast

from PySide6.QtCore import QBuffer, QIODevice, QRect, Qt
from PySide6.QtGui import QGuiApplication, QPainter, QPixmap
from PySide6.QtWidgets import QApplication

from src.core.telegram.bridge.interfaces import AppStatusProvider, ScreenshotProvider


class TelegramGUIBridge(ScreenshotProvider, AppStatusProvider):
    """Bridge tra la GUI e il sistema Telegram."""

    def __init__(self, main_window: Any) -> None:
        self.mw = main_window

    def capture_app_screenshot(self) -> bytes:
        """Cattura lo screenshot dell'app PyQt."""
        pixmap = self.mw.grab()
        return self._pixmap_to_bytes(pixmap)

    def capture_desktop_screenshot(self) -> bytes:
        """Cattura lo screenshot multi-monitor."""
        screens = QGuiApplication.screens()
        total_rect = QRect()
        for s in screens:
            total_rect = total_rect.united(s.geometry())

        combined = QPixmap(total_rect.size())
        combined.fill(Qt.GlobalColor.black)
        p = QPainter(combined)
        for s in screens:
            p.drawPixmap(s.geometry().topLeft() - total_rect.topLeft(), s.grabWindow(cast("Any", 0)))
        p.end()
        return self._pixmap_to_bytes(combined)

    def _pixmap_to_bytes(self, pixmap: QPixmap) -> bytes:
        buf = QBuffer()
        buf.open(QIODevice.OpenModeFlag.WriteOnly)
        pixmap.save(buf, "PNG")
        return cast("bytes", buf.data().data())

    def get_system_status(self) -> tuple[str, str, str]:
        """Recupera lo stato dal bot controller."""
        panel = self.mw.bot_controller._get_active_bot_panel()
        if panel and hasattr(panel, "get_current_status"):
            status, msg = panel.get_current_status()
            bot_name = getattr(panel, "bot_name", "Sconosciuto")
            return bot_name, status, msg
        return "Idle", "In attesa", ""

    def restart_application(self) -> None:
        """Esegue il restart fisico."""
        with suppress(Exception):
            subprocess.Popen(["cmd.exe", "/c", "start", os.path.abspath("avvio.bat")])
            QApplication.quit()
