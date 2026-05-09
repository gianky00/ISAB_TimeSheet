"""
SyncroJob - App Updater (Wrapper)
Provides high-level update management by delegating to engine and gui modules.
This file is part of the refactoring to keep modules under 400 lines.
"""

from src.gui.dialogs.updater_dialog import (
    check_for_updates,
    perform_auto_update,
    show_install_prompt,
)

from .updater.engine import (
    get_local_setup_path,
    get_pending_installer_path,
    has_pending_update,
    run_pending_installer,
)

# Export for compatibility
__all__ = [
    "check_for_updates",
    "get_local_setup_path",
    "get_pending_installer_path",
    "has_pending_update",
    "perform_auto_update",
    "run_pending_installer",
    "show_install_prompt",
]

if __name__ == "__main__":
    import sys

    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    check_for_updates(silent=False)
    sys.exit(app.exec())
