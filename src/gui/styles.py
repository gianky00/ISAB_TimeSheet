"""
SyncroJob - Theme and Style Manager
Gestisce l'applicazione di temi, palette e fogli di stile (QSS).
"""

import logging
from pathlib import Path

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication

from src.gui.design.colors import DARK, LIGHT, ColorPalette
from src.utils.helpers import get_asset_path

logger = logging.getLogger(__name__)


class ThemeManager:
    """Manager centralizzato per l'aspetto visivo dell'applicazione."""

    _instance = None

    def __new__(cls):
        """Pattern Singleton per il gestore dello stile."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.current_theme = "light"
        return cls._instance

    @property
    def palette(self) -> ColorPalette:
        """Restituisce la palette del tema corrente."""
        return DARK if self.current_theme == "dark" else LIGHT

    def apply_theme(self, app: QApplication, theme_name: str = "light"):
        """
        Applica il tema completo all'applicazione.
        Configura la QPalette e carica i file QSS necessari.
        """
        self.current_theme = theme_name
        logger.info(f"Applicazione tema: {theme_name}")

        # 1. Applica QPalette (Livello System-Native)
        self._apply_palette(app)

        # 2. Applica QSS Principale (Livello Branding)
        self._apply_stylesheet(app, theme_name)

    def _apply_palette(self, app: QApplication):
        """Traduce la ColorPalette in una QPalette Qt."""
        p = self.palette
        palette = QPalette()

        # Helper per convertire HEX in QColor
        def q(hex_color: str) -> QColor:
            return QColor(hex_color)

        # Mappatura ruoli standard
        palette.setColor(QPalette.ColorRole.Window, q(p.background))
        palette.setColor(QPalette.ColorRole.WindowText, q(p.on_background))
        palette.setColor(QPalette.ColorRole.Base, q(p.surface))
        palette.setColor(QPalette.ColorRole.AlternateBase, q(p.surface_variant))
        palette.setColor(QPalette.ColorRole.ToolTipBase, q(p.surface))
        palette.setColor(QPalette.ColorRole.ToolTipText, q(p.on_surface))
        palette.setColor(QPalette.ColorRole.Text, q(p.on_surface))
        palette.setColor(QPalette.ColorRole.Button, q(p.surface))
        palette.setColor(QPalette.ColorRole.ButtonText, q(p.on_surface))
        palette.setColor(QPalette.ColorRole.BrightText, q(p.on_primary))
        palette.setColor(QPalette.ColorRole.Link, q(p.primary))
        palette.setColor(QPalette.ColorRole.Highlight, q(p.primary))
        palette.setColor(QPalette.ColorRole.HighlightedText, q(p.on_primary))

        # Stati disabilitati
        palette.setColor(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, q(p.disabled)
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, q(p.disabled)
        )
        palette.setColor(
            QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, q(p.disabled)
        )

        app.setPalette(palette)

    def _apply_stylesheet(self, app: QApplication, theme_name: str):
        """Carica e applica il file QSS principale."""
        qss_path = Path(get_asset_path(f"assets/styles/{theme_name}.qss"))

        qss_content = ""
        if qss_path.exists():
            try:
                with open(qss_path, "r", encoding="utf-8") as f:
                    qss_content = f.read()
            except Exception as e:
                logger.error(f"Errore lettura QSS {qss_path}: {e}")

        # Se il file manca o è vuoto, applica uno stile minimo basato sulla palette
        if not qss_content:
            qss_content = (
                f"QMainWindow {{ background-color: {self.palette.background}; }}"
            )

        app.setStyleSheet(qss_content)


# Wrapper per compatibilità con il codice esistente
def apply_theme(app: QApplication, theme_name: str = "light"):
    ThemeManager().apply_theme(app, theme_name)
