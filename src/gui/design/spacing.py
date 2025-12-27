"""
Bot TS Design System - Spacing
"""

class Spacing:
    """Sistema di spaziature consistente."""

    # Base unit: 4px
    BASE = 4

    # Scale
    xxs = BASE       # 4px
    xs = BASE * 2    # 8px
    sm = BASE * 3    # 12px
    md = BASE * 4    # 16px
    lg = BASE * 6    # 24px
    xl = BASE * 8    # 32px
    xxl = BASE * 12  # 48px

    # Specific
    gutter = md      # 16px - spacing between elements
    margin = lg      # 24px - page margins
    padding = md     # 16px - component internal padding

class BorderRadius:
    """Raggi bordi."""
    none = 0
    sm = 4
    md = 8
    lg = 12
    xl = 16
    full = 9999  # Pill shape

class Shadow:
    """Ombre (elevation)."""
    none = "none"
    sm = "0 1px 2px rgba(0,0,0,0.05)"
    md = "0 4px 6px rgba(0,0,0,0.1)"
    lg = "0 10px 15px rgba(0,0,0,0.1)"
    xl = "0 20px 25px rgba(0,0,0,0.15)"
