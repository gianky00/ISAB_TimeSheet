from unittest.mock import MagicMock

from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.notification_item import NotificationItem
from src.gui.widgets.status_indicator import StatusIndicator
from src.utils.secure_logger import get_secure_logger


class TestSmallComponentsBoost:
    def test_secure_logger_flow(self):
        logger = get_secure_logger("TestLogger")
        # Ensure it has the filter
        assert any("SensitiveDataFilter" in str(type(f)) for f in logger.filters)
        # Test masking
        record = MagicMock(msg="password: secret123", args=None)
        # Manually trigger filter for test
        for f in logger.filters:
            f.filter(record)
        assert "MASKED" in record.msg

    def test_status_indicator_states(self, qapp):
        indicator = StatusIndicator()
        indicator.set_status("running", "In esecuzione")
        assert indicator.toolTip() == "In esecuzione"
        indicator.set_status("success", "Fatto")
        assert indicator.toolTip() == "Fatto"
        indicator.set_status("error", "Errore")
        indicator.set_status("idle", "In attesa")

    def test_modern_button_variants(self, qapp):
        btn = ModernButton("Click me", variant=ModernButton.Variant.PRIMARY)
        assert btn.text() == "Click me"
        btn.setEnabled(False)
        assert btn.isEnabled() is False
        btn.setEnabled(True)
        assert btn.isEnabled() is True

    def test_notification_item_display(self, qapp):
        data = {
            "title": "Titolo",
            "message": "Messaggio",
            "timestamp": "2024-01-01 12:00",
            "read": False
        }
        item = NotificationItem(data)
        assert item is not None

