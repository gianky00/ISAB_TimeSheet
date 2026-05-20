from src.gui.styles.constants import COLORS
from src.gui.styles.palette_helpers import get_glass_gradient, get_status_color, hex_to_rgba


class TestPaletteHelpers:
    def test_hex_to_rgba(self):
        # #FFFFFF -> rgba(255, 255, 255, 1.0)
        assert hex_to_rgba("#FFFFFF") == "rgba(255, 255, 255, 1.0)"
        assert hex_to_rgba("#000000", 0.5) == "rgba(0, 0, 0, 0.5)"

    def test_get_glass_gradient(self):
        grad_v = get_glass_gradient(vertical=True)
        assert "y2:1" in grad_v
        assert COLORS["glass_dark"] in grad_v

        grad_h = get_glass_gradient(vertical=False)
        assert "x2:1" in grad_h
        assert "y2:0" in grad_h

    def test_get_status_color(self):
        assert get_status_color("success") == COLORS["success_dark"]
        assert get_status_color("error") == COLORS["error_red"]
        assert get_status_color("UNKNOWN") == COLORS["text_muted"]
        assert get_status_color("RUNNING") == COLORS["primary_dark"]
