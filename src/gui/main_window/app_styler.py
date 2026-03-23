"""
SyncroJob - App Styler
Configura l'aspetto visivo e i metadati dell'applicazione.
Estratto da AppInitializer per seguire l'SRP.
"""

import ctypes
import os

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from src.core.version import __version__
from src.gui.styles import apply_theme


class AppStyler:
    """Gestisce la configurazione dello stile globale di PyQt."""

    @staticmethod
    def setup_app_style(app: QApplication) -> None:
        """
        Configura il tema, il font e i metadati per Windows.
        """
        if os.name == "nt":
            try:
                myappid = f"Coemi.SyncroJob.Enterprise.{__version__}"
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            except Exception:  # noqa: S110
                pass

        app.setStyle("Fusion")
        apply_theme(app, "light")
        app.setFont(QFont("Segoe UI", 10))
        app.setApplicationName("SyncroJob")
        app.setApplicationVersion(__version__)
        app.setDesktopFileName(f"Coemi.SyncroJob.Enterprise.{__version__}")
