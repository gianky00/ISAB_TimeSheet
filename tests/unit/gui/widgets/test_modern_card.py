"""Unit tests for ModernCard."""

from PySide6.QtCore import QPropertyAnimation

from src.gui.widgets.modern_card import ModernCard, ModernContentCard


class TestModernCard:
    """Test suite per ModernCard."""

    def test_initialization(self, qtbot):
        card = ModernCard(elevation=20)
        qtbot.addWidget(card)

        assert card.elevation == 20
        assert card.shadow.blurRadius() == 20
        assert card.shadow_anim.targetObject() == card.shadow

    def test_hover_effects(self, qtbot):
        card = ModernCard(elevation=10)
        qtbot.addWidget(card)

        # Simuliamo enter
        from PySide6.QtCore import QPointF
        from PySide6.QtGui import QEnterEvent

        enter_event = QEnterEvent(QPointF(0, 0), QPointF(0, 0), QPointF(0, 0))
        card.enterEvent(enter_event)

        assert card.shadow_anim.endValue() == 25  # 10 + 15
        assert card.shadow_anim.state() == QPropertyAnimation.State.Running

        # Simuliamo leave
        from PySide6.QtCore import QEvent

        leave_event = QEvent(QEvent.Type.Leave)
        card.leaveEvent(leave_event)

        assert card.shadow_anim.endValue() == 10
        assert card.shadow_anim.state() == QPropertyAnimation.State.Running

    def test_content_card(self, qtbot):
        card = ModernContentCard()
        qtbot.addWidget(card)

        from PySide6.QtWidgets import QPushButton

        btn = QPushButton("Inside Card")
        card.addWidget(btn)

        assert btn.parent() == card
        assert card.content_layout.count() == 1
