"""
Bot TS Design System - Spacing
"""


class Spacing:
    """Sistema di spaziature consistente."""

    # Base unit: 4px
    BASE = 4

    # Scale
    xxs = BASE  # 4px
    xs = BASE * 2  # 8px
    sm = BASE * 3  # 12px
    md = BASE * 4  # 16px
    lg = BASE * 6  # 24px
    xl = BASE * 8  # 32px
    xxl = BASE * 12  # 48px

    # Specific
    gutter = md  # 16px - spacing between elements
    margin = lg  # 24px - page margins
    padding = md  # 16px - component internal padding


class BorderRadius:
    """Raggi bordi."""

    none = 0
    sm = 4
    md = 8
    lg = 12
    xl = 16
    full = 9999  # Pill shape
