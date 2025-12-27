import sys
import os
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.gui.main_window import MainWindow

def capture_screenshot():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Navigate to settings panel
    window.sidebar.setCurrentItem(window.sidebar.findItems("Impostazioni", Qt.MatchFlag.MatchExactly)[0])

    # Wait for UI to render
    QTimer.singleShot(2000, lambda: take_screenshot_and_exit(app, window))

    app.exec()

def take_screenshot_and_exit(app, window):
    # Use xwd to capture the window content
    os.system(f"xwd -root -out verification/screenshot.xwd")
    os.system(f"convert verification/screenshot.xwd verification/verification.png")
    app.quit()

if __name__ == "__main__":
    if not os.path.exists("verification"):
        os.makedirs("verification")
    capture_screenshot()
