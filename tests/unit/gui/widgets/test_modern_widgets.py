from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QApplication

from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.modern_card import ModernCard, ModernContentCard


class TestModernButton:
    def test_button_variants(self, qtbot):
        for variant in [
            ModernButton.Variant.PRIMARY,
            ModernButton.Variant.DANGER,
            ModernButton.Variant.GHOST,
        ]:
            btn = ModernButton("Test", variant=variant)
            qtbot.addWidget(btn)
            assert btn.text() == "Test"
            # _apply_style should have run
            assert btn.styleSheet() != ""

    def test_button_sizes(self, qtbot):
        for size in [ModernButton.Size.SMALL, ModernButton.Size.LARGE]:
            btn = ModernButton("Test", size=size)
            qtbot.addWidget(btn)
            _padding, font = btn._get_size_styles()
            assert font in btn.styleSheet()

    def test_button_click_animation_state(self, qtbot):
        btn = ModernButton("Click Me")
        qtbot.addWidget(btn)

        # Simuliamo pressione
        qtbot.mousePress(btn, Qt.MouseButton.LeftButton)
        assert btn._shadow.blurRadius() == 2

        # Rilascio
        qtbot.mouseRelease(btn, Qt.MouseButton.LeftButton)
        assert btn._shadow.blurRadius() == 8

    def test_button_hover_animation(self, qtbot):
        from PySide6.QtGui import QEnterEvent

        btn = ModernButton("Hover Me")
        qtbot.addWidget(btn)

        # Entrata mouse
        event = QEnterEvent(QPoint(0, 0), QPoint(0, 0), QPoint(0, 0))
        QApplication.sendEvent(btn, event)
        # Aspettiamo che l'animazione inizi/finisca o controlliamo i valori target
        assert btn._anim.endValue() == 0.1

        # Uscita mouse
        from PySide6.QtCore import QEvent

        leave_event = QEvent(QEvent.Type.Leave)
        QApplication.sendEvent(btn, leave_event)
        assert btn._anim.endValue() == 0.0


class TestModernCard:
    def test_card_elevation(self, qtbot):
        card = ModernCard(elevation=20)
        qtbot.addWidget(card)
        assert card.shadow.blurRadius() == 20

    def test_card_hover_effect(self, qtbot):
        from PySide6.QtCore import QEvent
        from PySide6.QtGui import QEnterEvent

        card = ModernCard()
        qtbot.addWidget(card)

        # Enter
        event = QEnterEvent(QPoint(0, 0), QPoint(0, 0), QPoint(0, 0))
        QApplication.sendEvent(card, event)
        assert card.shadow_anim.endValue() == 15 + 15

        # Leave
        leave_event = QEvent(QEvent.Type.Leave)
        QApplication.sendEvent(card, leave_event)
        assert card.shadow_anim.endValue() == 15

    def test_content_card(self, qtbot):
        from PySide6.QtWidgets import QLabel

        card = ModernContentCard()
        qtbot.addWidget(card)

        label = QLabel("Internal")
        card.addWidget(label)

        assert label.parent() is card
        assert card.content_layout.count() == 1
