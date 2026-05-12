import os
import sys
from unittest.mock import MagicMock, patch

from PySide6.QtWidgets import QApplication, QMessageBox

# Aggiungi root al path
sys.path.insert(0, os.getcwd())

from src.core import version
from src.core.app_updater import check_for_updates


def debug_test():
    # Evita errori se QApplication esiste già
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    print("QApplication initialized")

    # Mocking version
    version.__version__ = "1.0.0"

    with patch("src.core.updater.gui.get_web_update_info") as mock_web:
        with patch("src.core.updater.gui.get_network_update_info") as mock_net:
            with patch("src.core.updater.gui.QMessageBox") as mock_msg:
                mock_web.return_value = {"version": "1.1.0", "url": "http://download.url"}
                mock_net.return_value = None
                mock_msg.question.return_value = QMessageBox.StandardButton.Yes
                mock_msg.StandardButton = QMessageBox.StandardButton

                # Mock HEAD request
                with patch("src.core.updater.gui.requests.head") as mock_head:
                    mock_resp = MagicMock()
                    mock_resp.headers = {"content-length": "1000000"}
                    mock_head.return_value = mock_resp

                    print("Starting check_for_updates...")
                    try:
                        check_for_updates(silent=False)
                        print("check_for_updates finished successfully")
                    except Exception as e:
                        print(f"Caught exception: {e}")
                        import traceback

                        traceback.print_exc()


if __name__ == "__main__":
    debug_test()
