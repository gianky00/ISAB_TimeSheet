import pytest
from PySide6.QtWidgets import QApplication

from src.gui.widgets.message_bubble import MessageBubble


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_message_bubble_lyra(qapp):
    bubble = MessageBubble(sender="Lyra", text="Hello **World**", is_lyra=True)
    assert bubble.is_lyra is True
    from PySide6.QtWidgets import QFrame

    chat_bubble = bubble.findChild(QFrame, "chatBubble")
    assert "border-top-left-radius: 4px" in chat_bubble.styleSheet()


def test_message_bubble_user(qapp):
    bubble = MessageBubble(sender="User", text="Hi there", is_lyra=False)
    assert bubble.is_lyra is False
    from PySide6.QtWidgets import QFrame

    chat_bubble = bubble.findChild(QFrame, "chatBubble")
    assert "border-top-right-radius: 4px" in chat_bubble.styleSheet()


def test_message_bubble_markdown_table(qapp):
    markdown_table = """
| Col1 | Col2 |
|---|---|
| Val1 | Val2 |
"""
    bubble = MessageBubble(sender="Lyra", text=markdown_table, is_lyra=True)
    from PySide6.QtWidgets import QLabel

    labels = bubble.findChildren(QLabel)
    # The message label is the one that is NOT fixed to 32x32
    text_label = next(
        lbl
        for lbl in labels
        if lbl.maximumSize().width() != 32 and lbl.minimumSize().width() != 32 and "Val1" in lbl.text()
    )
    assert "<table" in text_label.text()
    assert 'border="1"' in text_label.text()
