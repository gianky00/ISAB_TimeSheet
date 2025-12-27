"""
Bot TS - Styles and Themes
Defines the visual styles for the application.
Currently enforces Light Theme via QSS file.
"""
import os
from pathlib import Path

def apply_theme(app, theme_name="light"):
    """
    Applica il tema all'applicazione.
    Carica il file QSS corrispondente da assets/styles.
    """
    # Force light theme as per current requirement
    theme_name = "light"

    # Path resolution
    base_dir = Path(__file__).parent.parent.parent
    qss_path = base_dir / "assets" / "styles" / f"{theme_name}.qss"

    if qss_path.exists():
        with open(qss_path, "r", encoding="utf-8") as f:
            qss_content = f.read()
            # Here we could inject variables if needed, but QSS handles most
            app.setStyleSheet(qss_content)
    else:
        # Fallback to inline style if file missing (dev mode)
        print(f"Warning: Stylesheet {qss_path} not found. Using default.")
        from .design.colors import LIGHT
        app.setStyleSheet(f"QMainWindow {{ background-color: {LIGHT.background}; }}")
