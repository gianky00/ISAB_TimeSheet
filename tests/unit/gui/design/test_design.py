from src.gui.design.colors import LIGHT, ColorPalette, get_palette
from src.gui.design.spacing import BorderRadius, Spacing


class TestDesignSystem:
    def test_color_palette(self):
        palette = get_palette("light")
        assert palette == LIGHT
        assert palette.primary == "#009688"
        assert isinstance(palette, ColorPalette)

    def test_spacing_values(self):
        assert Spacing.BASE == 4
        assert Spacing.md == 16
        assert Spacing.gutter == 16
        assert Spacing.margin == 24

    def test_border_radius(self):
        assert BorderRadius.sm == 4
        assert BorderRadius.full == 9999
