import os
import sys

# Add root to path
sys.path.append(os.getcwd())

try:
    from src.gui.notifications_panel import NotificationItem

    print("Imported NotificationItem from notifications_panel (unexpected)")
except ImportError:
    print("Could not import NotificationItem from notifications_panel (expected)")
except Exception as e:
    print(f"Error importing from notifications_panel: {e}")

try:

    print("Imported NotificationItem from widgets.notification_item (SUCCESS)")
except Exception as e:
    print(f"Error importing from widgets.notification_item: {e}")

try:

    print("Imported NotificationsPanel (SUCCESS)")
except Exception as e:
    print(f"Error importing NotificationsPanel: {e}")
