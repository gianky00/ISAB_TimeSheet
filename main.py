#!/usr/bin/env python3
"""
Bot TS - Sistema di Automazione Portale ISAB
Entry point principale dell'applicazione.
"""
import sys
import os

# Ensure src is in path
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    base_path = os.path.dirname(sys.executable)
else:
    # Running as script
    base_path = os.path.dirname(os.path.abspath(__file__))

src_path = os.path.join(base_path, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

def main():
    """Main entry point."""
    # Auto-download license if running from source and license folder is empty
    try:
        from src.core.license_updater import auto_download_license_if_needed
        auto_download_license_if_needed()
    except Exception as e:
        print(f"[AVVISO] Controllo licenza: {e}")
    
    # Import PyQt6 components
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QFont
    
    # Create application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Set application metadata
    app.setApplicationName("Bot TS")
    app.setOrganizationName("Giancarlo Allegretti")
    app.setApplicationVersion("1.0.0")
    
    # Import and show main window
    from src.gui.main_window import MainWindow
    
    window = MainWindow()
    window.showMaximized()
    
    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
