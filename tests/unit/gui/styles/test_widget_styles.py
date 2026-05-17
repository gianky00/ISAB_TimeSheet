from src.gui.styles.widget_styles import card_style, icon_badge, label_subtitle, label_title, status_dot


class TestWidgetStyles:
    def test_card_style(self):
        style = card_style("#FF0000")
        assert "border-left: 4px solid #FF0000" in style
        assert "QFrame" in style

    def test_label_styles(self):
        title = label_title(20, "#111111")
        assert "font-size: 20px" in title
        assert "color: #111111" in title

        subtitle = label_subtitle(14)
        assert "font-size: 14px" in subtitle

    def test_icon_badge(self):
        badge = icon_badge("#00FF00", 40)
        assert "background-color: #00FF00" in badge
        assert "border-radius: 20px" in badge  # 40 // 2

    def test_status_dot(self):
        dot = status_dot("#0000FF", 12)
        assert "min-width: 12px" in dot
        assert "border-radius: 6px" in dot
