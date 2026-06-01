"""Unit tests for MessageBubble."""

from PySide6.QtWidgets import QLabel

from src.gui.widgets.message_bubble import MessageBubble


class TestMessageBubble:
    """Test suite per MessageBubble."""

    def test_lyra_bubble(self, qtbot):
        """Verifica allineamento a sinistra per AI."""
        text = "Hello, I am Lyra. **Bold**"
        bubble = MessageBubble(sender="Lyra", text=text, is_lyra=True)
        qtbot.addWidget(bubble)

        assert bubble.is_lyra is True
        # Verifica rendering markdown (strong invece di b per markdown standard)
        msg_label = bubble.findChildren(QLabel)[1]
        assert "<strong>Bold</strong>" in msg_label.text()
        assert "L" in bubble.findChildren(QLabel)[0].text()

    def test_user_bubble(self, qtbot):
        """Verifica allineamento a destra per Utente."""
        bubble = MessageBubble(sender="User", text="Test", is_lyra=False)
        qtbot.addWidget(bubble)

        assert bubble.is_lyra is False
        assert "U" in bubble.findChildren(QLabel)[1].text()

    def test_markdown_tables(self, qtbot):
        """Verifica il rendering delle tabelle."""
        table_md = "| H1 | H2 |\n|---|---|\n| V1 | V2 |"
        bubble = MessageBubble(sender="L", text=table_md, is_lyra=True)
        qtbot.addWidget(bubble)

        msg_label = next(lbl for lbl in bubble.findChildren(QLabel) if "<table" in lbl.text())
        assert "<table" in msg_label.text()
        assert "V1" in msg_label.text()
