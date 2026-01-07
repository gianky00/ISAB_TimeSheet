"""
Bot TS - Styles and Themes
Defines the visual styles for the application.
Currently enforces Light Theme via QSS file AND QPalette.
"""

from pathlib import Path

from PyQt6.QtGui import QColor, QPalette

from src.utils.helpers import get_asset_path


def apply_theme(app, theme_name="light"):
    """
    Applica il tema all'applicazione.
    Carica il file QSS corrispondente da assets/styles E forza la QPalette chiara.
    """
    # Force light theme as per current requirement
    theme_name = "light"

    # --- 1. FORCE LIGHT PALETTE (Overrides System Dark Mode) ---
    palette = QPalette()

    # Define Light Colors
    white = QColor(255, 255, 255)
    off_white = QColor(250, 250, 250)  # Very light gray for window background
    light_gray = QColor(240, 240, 240)  # For buttons
    text_color = QColor(33, 33, 33)  # Dark gray for text, softer than pure black
    disabled_text = QColor(127, 127, 127)
    primary_color = QColor(0, 150, 136)  # Teal (matches QSS)

    # Set Palette Roles
    palette.setColor(QPalette.ColorRole.Window, off_white)
    palette.setColor(QPalette.ColorRole.WindowText, text_color)
    palette.setColor(QPalette.ColorRole.Base, white)
    palette.setColor(QPalette.ColorRole.AlternateBase, light_gray)
    palette.setColor(QPalette.ColorRole.ToolTipBase, white)
    palette.setColor(QPalette.ColorRole.ToolTipText, text_color)
    palette.setColor(QPalette.ColorRole.Text, text_color)
    palette.setColor(QPalette.ColorRole.Button, white)  # Fusion buttons are usually white/light
    palette.setColor(QPalette.ColorRole.ButtonText, text_color)
    palette.setColor(QPalette.ColorRole.BrightText, white)
    palette.setColor(QPalette.ColorRole.Link, primary_color)
    palette.setColor(QPalette.ColorRole.Highlight, primary_color)
    palette.setColor(QPalette.ColorRole.HighlightedText, white)

    # Disabled state adjustments
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, disabled_text)
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, disabled_text)
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, disabled_text)

    app.setPalette(palette)

    # --- 2. LOAD STYLESHEET (QSS) ---
    # Use helper to resolve path correctly in both dev and frozen modes
    qss_path = Path(get_asset_path(f"assets/styles/{theme_name}.qss"))

    if qss_path.exists():
        with open(qss_path, "r", encoding="utf-8") as f:
            qss_content = f.read()
            app.setStyleSheet(qss_content)
    else:
        # Fallback to inline style if file missing (dev mode)
        print(f"Warning: Stylesheet {qss_path} not found. Using default.")
        # Try to import colors, handle failure gracefully
        try:
            from .design.colors import LIGHT

            app.setStyleSheet(f"QMainWindow {{ background-color: {LIGHT.background}; }}")
        except ImportError:
            pass
