from src.gui.widgets.timeline_widget import HorizontalTimelineWidget, TimelineWidget

# The 'qapp' fixture is automatically provided by pytest-qt and ensures a
# QApplication instance exists before any tests that use GUI components are run.


def test_horizontal_timeline_functionality(qtbot):
    """
    Tests the basic functionality of the TimelineWidget and its HorizontalTimelineWidget.
    """
    widget = TimelineWidget()
    qtbot.addWidget(widget)

    # Verify that the TimelineWidget correctly contains a HorizontalTimelineWidget
    assert isinstance(widget.timeline, HorizontalTimelineWidget), (
        "TimelineWidget should be using HorizontalTimelineWidget"
    )

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
    # We count only the widgets, as the layout also contains a stretch (spacer)
    layout = widget.timeline.container.main_layout
    item_count = sum(1 for i in range(layout.count()) if layout.itemAt(i).widget())

    assert item_count == len(logs_to_add), (
        f"Expected {len(logs_to_add)} items in timeline, but found {item_count}"
    )
