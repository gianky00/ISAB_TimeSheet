import os
import sys

# Add root to path
sys.path.append(os.getcwd())

def test_imports_gui():
    """Verify that main GUI components can be imported without errors."""
    try:
        from src.gui.notifications_panel import NotificationsPanel
        from src.gui.widgets.notification_item import NotificationItem
        print("Import SUCCESS")
        assert True
    except Exception as e:
        pytest.fail(f"Import failed: {e}")

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])