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
    "ANIMATION_TIMINGS",
    "BUTTON_DANGER",
    "BUTTON_ICON_ONLY",
    # Widget Styles - Buttons
    "BUTTON_PRIMARY",
    "BUTTON_SECONDARY",
    "BUTTON_SUCCESS",
    "BUTTON_TRANSPARENT",
    # Widget Styles - Cards & Containers
    "CARD_STYLE_SIMPLE",
    "CHECKBOX_STYLE",
    "CHECKBOX_TOGGLE",
    # Constants
    "COLORS",
    "COMBOBOX_LIGHT_ON_DARK",
    # Widget Styles - Inputs
    "COMBOBOX_STYLE",
    "EMPTY_STATE_LABEL",
    "FONT_SIZES",
    "FRAME_HEADER",
    # Widget Styles - Labels
    "LABEL_MUTED",
    "LINEEDIT_STYLE",
    "LIVE_DOT",
    "MONTHS_IT",
    "MONTHS_IT_FULL",
    "SCROLL_AREA_BORDERED",
    "SCROLL_AREA_TRANSPARENT",
    "SPINBOX_STYLE",
    "STATUS_COLORS",
    "TIMEEDIT_SMALL",
    "TIMEEDIT_STYLE",
    "UI_SIZES",
    # Theme Management
    "ThemeManager",
    "apply_theme",
    # Widget Styles - Functions
    "card_style",
    "icon_badge",
    "label_subtitle",
    "label_title",
    "status_dot",
]
