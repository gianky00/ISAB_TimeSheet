from src.gui.widgets import HorizontalTimelineWidget, LogWidget

# The 'qapp' fixture is automatically provided by pytest-qt and ensures a
# QApplication instance exists before any tests that use GUI components are run.


def test_horizontal_timeline_functionality(qapp):
    """
    Tests the basic functionality of the LogWidget and its HorizontalTimelineWidget.
    """
    widget = LogWidget()

    # Verify that the LogWidget correctly contains a HorizontalTimelineWidget
    assert isinstance(
        widget.timeline, HorizontalTimelineWidget
    ), "LogWidget should be using HorizontalTimelineWidget"

    # Add a series of logs to the widget
    logs_to_add = [
        "🚀 Avvio sistema",
        "🔐 Login in corso...",
        "✅ Accesso effettuato",
        "📥 Download dati",
        "❌ Errore critico [IMG:/tmp/screenshot.png]",
    ]

    for log_message in logs_to_add:
        widget.append(log_message)

    # Check if the number of items in the timeline's container layout matches the number of logs added
    item_count = widget.timeline.container.layout().count()

    assert item_count == len(
        logs_to_add
    ), f"Expected {len(logs_to_add)} items in timeline, but found {item_count}"
