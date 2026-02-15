"""
SyncroJob - Costanti di Stile Centralizzate
Colori operativi, timing animazioni e costanti UI usate in tutta l'applicazione.

Nota: Questi colori estendono la palette Material in src/gui/design/colors.py
con colori "operativi" Bootstrap-like usati nei widget.
"""

from typing import Final

# =============================================================================
# COLORI OPERATIVI (Bootstrap-like, usati nei widget)
# =============================================================================

COLORS: Final[dict[str, str]] = {
    # Primary
    "primary_blue": "#3498db",
    "primary_dark": "#0d6efd",
    # Success
    "success_green": "#2ecc71",
    "success_dark": "#198754",
    "success_material": "#2E7D32",
    # Warning
    "warning_orange": "#f39c12",
    "warning_light": "#fd7e14",
    "warning_yellow": "#ffc107",
    # Error/Danger
    "error_red": "#dc3545",
    "error_material": "#C62828",
    # Text
    "text_dark": "#212529",
    "text_muted": "#6c757d",
    "text_secondary": "#868e96",
    "text_light": "#adb5bd",
    # Backgrounds
    "bg_white": "#ffffff",
    "bg_light": "#f8f9fa",
    "bg_hover": "#e9ecef",
    "bg_alt": "#f1f3f5",
    # Borders
    "border_light": "#dee2e6",
    "border_medium": "#ced4da",
    "border_dark": "#adb5bd",
}


# =============================================================================
# COLORI STATUS (per indicatori di stato nei widget)
# =============================================================================

STATUS_COLORS: Final[dict[str, str]] = {
    # Bot/Task status
    "running": "#0d6efd",
    "completed": "#2E7D32",
    "pending": "#ffc107",
    "error": "#C62828",
    "stopped": "#6c757d",
    # Employee/Access status
    "ok": "#198754",
    "warning": "#fd7e14",
    "expired": "#dc3545",
    "excluded": "#6c757d",
    # Audit levels
    "high": "#dc3545",
    "medium": "#fd7e14",
    "low": "#198754",
    "info": "#3498db",
}


# =============================================================================
# TIMING ANIMAZIONI
# =============================================================================

ANIMATION_TIMINGS: Final[dict[str, int]] = {
    # Frame rates
    "fps_60": 16,  # ~60 FPS (1000ms / 60)
    "fps_30": 33,  # ~30 FPS
    "fade_fast": 150,
    "fade_normal": 300,
    "fade_slow": 500,
    "pulse_duration": 800,
    "pulse_slow": 2000,
    # Intervals
    "countdown_update": 60000,  # 1 minuto
    "dot_cycle": 350,
    "status_refresh": 5000,
    "telemetry_refresh": 2000,
}


# =============================================================================
# MESI ITALIANI (usato in grafici e report)
# =============================================================================

MONTHS_IT: Final[list[str]] = [
    "Gen",
    "Feb",
    "Mar",
    "Apr",
    "Mag",
    "Giu",
    "Lug",
    "Ago",
    "Set",
    "Ott",
    "Nov",
    "Dic",
]

MONTHS_IT_FULL: Final[list[str]] = [
    "Gennaio",
    "Febbraio",
    "Marzo",
    "Aprile",
    "Maggio",
    "Giugno",
    "Luglio",
    "Agosto",
    "Settembre",
    "Ottobre",
    "Novembre",
    "Dicembre",
]


# =============================================================================
# DIMENSIONI UI COMUNI
# =============================================================================

UI_SIZES: Final[dict[str, int]] = {
    # Border radius
    "radius_small": 4,
    "radius_medium": 8,
    "radius_large": 12,
    "radius_card": 16,
    # Icon sizes
    "icon_small": 16,
    "icon_medium": 20,
    "icon_large": 24,
    "icon_xlarge": 32,
    # Spacing
    "spacing_xs": 4,
    "spacing_sm": 8,
    "spacing_md": 12,
    "spacing_lg": 16,
    "spacing_xl": 24,
}


# =============================================================================
# FONT SIZES
# =============================================================================

FONT_SIZES: Final[dict[str, int]] = {
    "xs": 10,
    "sm": 12,
    "md": 14,
    "lg": 16,
    "xl": 18,
    "xxl": 24,
    "title": 28,
}
