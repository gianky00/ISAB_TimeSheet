from PyQt6.QtWidgets import QApplication
from src.gui.widgets import LogWidget, HorizontalTimelineWidget
import sys

def test_horizontal_magic():
    app = QApplication(sys.argv)
    widget = LogWidget()

    # Verify widget structure
    if not isinstance(widget.timeline, HorizontalTimelineWidget):
        print("FAIL: LogWidget is not using HorizontalTimelineWidget")
        return

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

if __name__ == "__main__":
    test_horizontal_magic()
