import pytest
from PyQt6.QtWidgets import QWidget

from src.gui.toast import ToastOverlay


class TestToast:
    @pytest.fixture
    def parent(self, qapp):  # noqa: ANN001
        w = QWidget()
        w.resize(800, 600)
        return w

    def test_toast_show_logic(self, qtbot, parent):  # noqa: ANN001
        """Verifica che il toast mostri il testo e si posizioni correttamente."""
        parent.show()
        toast = ToastOverlay(parent)
        qtbot.addWidget(toast)

        message = "Test Notification"
        toast.show_toast(message, duration=1000)

        # Attendi che l'animazione inizi
        qtbot.waitUntil(lambda: toast.opacity_effect.opacity() > 0, timeout=500)

        assert toast.label.text() == message

        # Verifica posizionamento (deve essere in basso al centro)
        parent_rect = parent.rect()
        expected_x = (parent_rect.width() - toast.width()) // 2
        assert toast.x() == expected_x

    def test_toast_hide_after_duration(self, qtbot, parent):  # noqa: ANN001
        """Verifica che il toast sparisca dopo il timeout."""
        toast = ToastOverlay(parent)
        qtbot.addWidget(toast)

        # Usiamo una durata brevissima per il test
        toast.show_toast("Short", duration=100)

        # Attendiamo che il timer del toast scada (100ms) + animazione (300ms)
        qtbot.wait(600)

        assert not toast.isVisible() or toast.opacity_effect.opacity() == 0
