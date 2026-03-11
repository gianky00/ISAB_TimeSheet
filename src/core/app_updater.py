"""
SyncroJob - App Updater (Wrapper)
Provides high-level update management by delegating to engine and gui modules.
This file is part of the refactoring to keep modules under 400 lines.
"""

from .updater.engine import (
    get_local_setup_path,
    has_pending_update,
    run_pending_installer,
)
from .updater.gui import (
    check_for_updates,
    perform_auto_update,
    show_install_prompt,
)

# Export for compatibility
__all__ = [
    "check_for_updates",
    "get_local_setup_path",
    "has_pending_update",
    "perform_auto_update",
    "run_pending_installer",
    "show_install_prompt",
]

if __name__ == "__main__":
    import sys

    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    check_for_updates(silent=False)
    sys.exit(app.exec())
