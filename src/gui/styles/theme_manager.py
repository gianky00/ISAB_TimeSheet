"""
SyncroJob - Theme and Style Manager
Gestisce l'applicazione di temi, palette e fogli di stile (QSS).
"""

import logging
from pathlib import Path
from typing import Any, Optional

from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication

from src.gui.design.colors import LIGHT, ColorPalette
from src.utils.helpers import get_asset_path

logger = logging.getLogger(__name__)


class ThemeManager:
    """Manager centralizzato per l'aspetto visivo dell'applicazione."""

    _instance: Optional["ThemeManager"] = None

    def __new__(cls) -> "ThemeManager":
        """Pattern Singleton per il gestore dello stile."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.current_theme = "light"
        return cls._instance

    @property
    def palette(self) -> ColorPalette:
        """Restituisce la palette del tema corrente (FORZATA A LIGHT)."""
        return LIGHT

    def apply_theme(self, app: QApplication, theme_name: str = "light") -> None:
        """
        Applica il tema completo all'applicazione (FORZATO A LIGHT).
        Configura la QPalette e carica i file QSS necessari.
        """
        # Forza sempre il tema light per standard aziendale
        theme_name = "light"
        self.current_theme = "light"
        logger.info("Applicazione tema Enterprise Light Mode (Forced)")

        # 0. Force Fusion Style (Crucial for consistent palette)
        app.setStyle("Fusion")

        # 1. Applica QPalette (Livello System-Native)
        self._apply_palette(app)

        # 2. Applica QSS Principale (Livello Branding)
        self._apply_stylesheet(app, theme_name)

    def _apply_palette(self, app: QApplication) -> None:
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
            palette.setColor(group, QPalette.ColorRole.AlternateBase, q(p.surface_variant))
            palette.setColor(group, QPalette.ColorRole.ToolTipBase, q(p.surface))
            palette.setColor(group, QPalette.ColorRole.Button, q(p.surface))

            # Text / Foreground
            txt_col = q(p.disabled) if group == QPalette.ColorGroup.Disabled else q(p.on_background)

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

    def _apply_stylesheet(self, app: QApplication, theme_name: str) -> None:
        """Carica, processa e applica il file QSS principale e gli overrides."""
        # 1. Carica QSS del tema specifico
        qss_path = Path(get_asset_path(f"assets/styles/{theme_name}.qss"))
        qss_content = ""
        if qss_path.exists():
            try:
                qss_content = qss_path.read_text(encoding="utf-8")
                qss_content = self._process_qss(qss_content)
            except Exception as e:
                logger.error(f"Errore lettura QSS {qss_path}: {e}")

        if not qss_content:
            qss_content = f"QMainWindow {{ background-color: {self.palette.background}; }}"

        # 2. Carica QSS degli Overrides globali
        overrides_path = Path(get_asset_path("assets/styles/overrides.qss"))
        overrides_content = ""
        if overrides_path.exists():
            try:
                overrides_content = overrides_path.read_text(encoding="utf-8")
                overrides_content = self._process_qss(overrides_content)
            except Exception as e:
                logger.error(f"Errore lettura Overrides QSS: {e}")

        # 3. Applica la combinazione degli stili
        app.setStyleSheet(qss_content + overrides_content)

    def _process_qss(self, content: str) -> str:
        """Sostituisce i segnaposto {{key}} con i valori della palette e delle costanti."""
        p = self.palette
        from src.gui.styles.constants import COLORS, FONT_SIZES, UI_SIZES

        # Mapping di base dalla ColorPalette
        mapping: dict[str, Any] = {
            "primary": p.primary,
            "primary_variant": p.primary_variant,
            "on_primary": p.on_primary,
            "secondary": p.secondary,
            "secondary_variant": p.secondary_variant,
            "on_secondary": p.on_secondary,
            "background": p.background,
            "surface": p.surface,
            "surface_variant": p.surface_variant,
            "on_background": p.on_background,
            "on_surface": p.on_surface,
            "success": p.success,
            "warning": p.warning,
            "error": p.error,
            "info": p.info,
            "border": p.border,
            "divider": p.divider,
            "disabled": p.disabled,
            "hover": p.hover,
            "focus": p.focus,
        }

        # Estende con tutte le costanti COLORS
        for k, v in COLORS.items():
            if k not in mapping:
                mapping[k] = v

        # Aggiunge dimensioni UI
        for size_k, size_v in UI_SIZES.items():
            mapping[size_k] = f"{size_v}px"

        # Aggiunge font sizes
        for font_k, font_v in FONT_SIZES.items():
            mapping[f"font_{font_k}"] = f"{font_v}px"

        processed = content
        for key, value in mapping.items():
            processed = processed.replace(f"{{{{{key}}}}}", str(value))

        return processed


def apply_theme(app: QApplication, theme_name: str = "light") -> None:
    """Wrapper per compatibilità con il codice esistente."""
    ThemeManager().apply_theme(app, theme_name)
