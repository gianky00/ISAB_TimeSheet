"""
SyncroJob - Costanti di Stile Centralizzate
Colori operativi, timing animazioni e costanti UI usate in tutta l'applicazione.

Nota: Questi colori estendono la palette Material in src/gui/design/colors.py
con colori "operativi" Bootstrap-like usati nei widget.
"""

from typing import Final

from src.utils.date_utils import MONTHS_IT, MONTHS_IT_FULL

# Re-export per retrocompatibilità

__all__ = [
    "ANIMATION_TIMINGS",
    "COLORS",
    "FONT_SIZES",
    "MONTHS_IT",
    "MONTHS_IT_FULL",
    "STATUS_COLORS",
    "THRESHOLD_DAYS",
    "UI_SIZES",
]

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
    # Info & Semantic
    "info_blue": "#0d6efd",
    "purple": "#6f42c1",
    "purple_deep": "#6610f2",
    "magenta_pink": "#d63384",
    "teal_accent": "#009688",
    "teal_light": "#20c997",
    "cyan_info": "#0dcaf0",
    # Sidebar Glass Effect
    "glass_dark": "#1a2639",
    "glass_deep": "#0d1421",
    "glass_border": "rgba(255, 255, 255, 0.08)",
    # Table Status Backgrounds (Pastels)
    "table_success_bg": "#C8E6C9",
    "table_error_bg": "#FFCDD2",
    "table_warning_bg": "#FFF9C4",
    "table_info_bg": "#E3F2FD",
    "table_selection_bg": "#E0F7FA",
    # Pastel Backgrounds for Cards/Sections
    "bg_success_pastel": "#f0fdf4",
    "bg_error_pastel": "#fef2f2",
    "bg_warning_pastel": "#fff7ed",
    "bg_attention_pastel": "#fefce8",
    "bg_info_pastel": "#eff6ff",
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
# SOGLIE OPERATIVE (Business Logic)
# =============================================================================

THRESHOLD_DAYS: Final[dict[str, int]] = {
    "warning": 20,
    "expired": 30,
    "critical": 60,
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
    "idle": "#6c757d",
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
    # Toast Durations
    "countdown_update": 60000,  # 1 minuto
    "dot_cycle": 350,
    "status_refresh": 5000,
    "telemetry_refresh": 2000,
    "auth_check": 4 * 3600 * 1000,  # 4 ore
    "init_delay": 2000,
}


# =============================================================================
# MESI ITALIANI (re-export per retrocompatibilit )
# =============================================================================

# Le costanti sono importate al top del file da src.utils.date_utils


# =============================================================================
# DIMENSIONI UI COMUNI
# =============================================================================

UI_SIZES: Final[dict[str, int]] = {
    # Border radius
    "radius_small": 4,
    "radius_medium": 8,
    "radius_large": 12,
    "radius_card": 16,
    "grid_step": 25,
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

# =============================================================================
# TYPOGRAPHY SYSTEM
# =============================================================================

FONT_WEIGHTS: Final[dict[str, int]] = {
    "regular": 400,
    "medium": 500,
    "semibold": 600,
    "bold": 700,
}
