"""
SyncroJob - Theme and Style Manager
Gestisce l'applicazione di temi, palette e fogli di stile (QSS).
"""

import logging
from pathlib import Path

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication

from src.gui.design.colors import LIGHT, ColorPalette
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
        """Restituisce la palette del tema corrente (FORZATA A LIGHT)."""
        return LIGHT

    def apply_theme(self, app: QApplication, theme_name: str = "light"):
        """
        Applica il tema completo all'applicazione.
        Configura la QPalette e carica i file QSS necessari.
        """
        self.current_theme = theme_name
        logger.info(f"Applicazione tema: {theme_name}")

        # 0. Force Fusion Style (Crucial for consistent palette)
        app.setStyle("Fusion")

        # 1. Applica QPalette (Livello System-Native)
        self._apply_palette(app)

        # 2. Applica QSS Principale (Livello Branding)
        self._apply_stylesheet(app, theme_name)

    def _apply_palette(self, app: QApplication):
        """Traduce la ColorPalette in una QPalette Qt (STRICT MODE)."""
        p = self.palette
        palette = QPalette()

        # Helper per convertire HEX in QColor
        def q(hex_color: str) -> QColor:
            return QColor(hex_color)

        # Apply to ALL groups to prevent system text bleeding in Inactive/Disabled states
        groups = [
            QPalette.ColorGroup.Active,
            QPalette.ColorGroup.Inactive,
            QPalette.ColorGroup.Disabled,
        ]

        for group in groups:
            # Backgrounds
            palette.setColor(group, QPalette.ColorRole.Window, q(p.background))
            palette.setColor(group, QPalette.ColorRole.Base, q(p.surface))
            palette.setColor(
                group, QPalette.ColorRole.AlternateBase, q(p.surface_variant)
            )
            palette.setColor(group, QPalette.ColorRole.ToolTipBase, q(p.surface))
            palette.setColor(group, QPalette.ColorRole.Button, q(p.surface))

            # Text / Foreground
            if group == QPalette.ColorGroup.Disabled:
                # Dimmed text for disabled
                txt_col = q(p.disabled)
            else:
                txt_col = q(p.on_background)

            palette.setColor(group, QPalette.ColorRole.WindowText, txt_col)
            palette.setColor(group, QPalette.ColorRole.Text, txt_col)
            palette.setColor(group, QPalette.ColorRole.ButtonText, txt_col)
            palette.setColor(group, QPalette.ColorRole.ToolTipText, q(p.on_surface))
            palette.setColor(group, QPalette.ColorRole.PlaceholderText, q(p.disabled))

            # Accents
            palette.setColor(group, QPalette.ColorRole.Link, q(p.primary))
            palette.setColor(group, QPalette.ColorRole.Highlight, q(p.primary))
            palette.setColor(group, QPalette.ColorRole.HighlightedText, q(p.on_primary))
            palette.setColor(group, QPalette.ColorRole.BrightText, q(p.error))

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

        # Global Light Theme Enforcement for Popups & Windows
        global_overrides = """
            /* FORCE LIGHT THEME ON ALL DIALOGS AND MENUS */
            QDialog, QMainWindow {
                background-color: #ffffff;
                color: #000000;
            }
            /* Force all widgets INSIDE a Dialog to be light */
            QDialog QWidget {
                background-color: #ffffff;
                color: #000000;
            }
            /* But allow specific widgets to have their own backgrounds (like buttons) */
            QDialog QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QDialog QPushButton:hover {
                background-color: #e9ecef;
            }
            QDialog QLabel, QDialog QCheckBox {
                background-color: transparent; /* inherit white from parent */
                color: #000000;
            }

            QMenu {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #ced4da;
            }
            QMenu::item {
                background-color: transparent;
                color: #000000;
                padding: 6px 20px;
            }
            QMenu::item:selected {
                background-color: #e9ecef;
                color: #000000;
            }
            QMenuBar {
                background-color: #ffffff;
                color: #000000;
            }
            QMenuBar::item {
                background-color: transparent;
                color: #000000;
            }
            QMenuBar::item:selected {
                background-color: #e9ecef;
            }

            /* Tree View Force Light */
            QTreeWidget, QTreeView {
                background-color: #ffffff;
                color: #000000;
                alternate-background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                selection-background-color: #e9ecef;
                selection-color: #000000;
            }
            QTreeWidget::item, QTreeView::item {
                color: #000000;
            }
            QTreeWidget::item:hover {
                 background-color: #f1f3f5;
                 color: #000000;
            }
            QTreeWidget::item:selected {
                background-color: #e9ecef;
                color: #000000;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: #000000;
                border: none;
                border-bottom: 2px solid #dee2e6;
                padding: 4px;
                font-weight: bold;
            }

            /* Scrollbars */
            QScrollBar:vertical {
                border: none;
                background: #f1f3f5;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #ced4da;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }

            /* Tooltips */
            QToolTip {
                background-color: #ffffff;
                color: #424242;
                border: 1px solid #bdbdbd;
                border-radius: 4px;
                padding: 5px;
            }
        """
        app.setStyleSheet(qss_content + global_overrides)


def apply_theme(app: QApplication, theme_name: str = "light"):
    """Wrapper per compatibilità con il codice esistente."""
    ThemeManager().apply_theme(app, theme_name)
