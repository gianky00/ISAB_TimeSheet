from PyQt6.QtWidgets import QApplication
from src.gui.widgets import LogWidget, HorizontalTimelineWidget
import sys

def test_horizontal_magic(qapp):  # Inject the qapp fixture
    """
    Tests the horizontal timeline logic by adding items and verifying the count.
    """
    widget = LogWidget()

    # Verify widget structure
    assert isinstance(widget.timeline, HorizontalTimelineWidget), \
        "FAIL: LogWidget is not using HorizontalTimelineWidget"

    # Add logs
    widget.append("🚀 Avvio sistema")
    widget.append("🔐 Login in corso...")
    widget.append("✅ Accesso effettuato")
    widget.append("📥 Download dati")
    widget.append("❌ Errore critico [IMG:/tmp/screenshot.png]")

    # Check count in container layout
    count = widget.timeline.container.layout.count()
    print(f"Items in horizontal timeline: {count}")

    assert count == 5
    print("Test Finished - Horizontal Logic OK")

