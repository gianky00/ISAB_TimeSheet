"""
SyncroJob - Style Constants and Utilities
Modulo per costanti di stile, colori operativi e timing animazioni.
"""

from src.gui.styles.constants import (
    ANIMATION_TIMINGS,
    COLORS,
    FONT_SIZES,
    MONTHS_IT,
    MONTHS_IT_FULL,
    STATUS_COLORS,
    UI_SIZES,
)
from src.gui.styles.theme_manager import ThemeManager, apply_theme
from src.gui.styles.widget_styles import (
    BUTTON_DANGER,
    BUTTON_ICON_ONLY,
    BUTTON_PRIMARY,
    BUTTON_SECONDARY,
    BUTTON_SUCCESS,
    BUTTON_TRANSPARENT,
    CARD_STYLE_SIMPLE,
    CHECKBOX_STYLE,
    CHECKBOX_TOGGLE,
    COMBOBOX_LIGHT_ON_DARK,
    COMBOBOX_STYLE,
    EMPTY_STATE_LABEL,
    FRAME_HEADER,
    LABEL_MUTED,
    LINEEDIT_STYLE,
    LIVE_DOT,
    SCROLL_AREA_BORDERED,
    SCROLL_AREA_TRANSPARENT,
    SPINBOX_STYLE,
    TIMEEDIT_SMALL,
    TIMEEDIT_STYLE,
    card_style,
    icon_badge,
    label_subtitle,
    label_title,
    status_dot,
)

__all__ = [
    # Theme Management
    "ThemeManager",
    "apply_theme",
    # Constants
    "COLORS",
    "STATUS_COLORS",
    "ANIMATION_TIMINGS",
    "MONTHS_IT",
    "MONTHS_IT_FULL",
    "UI_SIZES",
    "FONT_SIZES",
    # Widget Styles - Buttons
    "BUTTON_PRIMARY",
    "BUTTON_SUCCESS",
    "BUTTON_DANGER",
    "BUTTON_SECONDARY",
    "BUTTON_TRANSPARENT",
    "BUTTON_ICON_ONLY",
    # Widget Styles - Inputs
    "COMBOBOX_STYLE",
    "COMBOBOX_LIGHT_ON_DARK",
    "LINEEDIT_STYLE",
    "TIMEEDIT_STYLE",
    "TIMEEDIT_SMALL",
    "SPINBOX_STYLE",
    "CHECKBOX_STYLE",
    "CHECKBOX_TOGGLE",
    # Widget Styles - Cards & Containers
    "CARD_STYLE_SIMPLE",
    "SCROLL_AREA_TRANSPARENT",
    "SCROLL_AREA_BORDERED",
    "FRAME_HEADER",
    # Widget Styles - Labels
    "LABEL_MUTED",
    "EMPTY_STATE_LABEL",
    "LIVE_DOT",
    # Widget Styles - Functions
    "card_style",
    "label_title",
    "label_subtitle",
    "icon_badge",
    "status_dot",
]
