import os
import sys
import time

from PyQt6.QtWidgets import QApplication

# Configura l'ambiente offscreen come nei test
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["PYTHONUTF8"] = "1"

print("--- DEBUG QT INIT START ---")
start = time.time()

try:
    print("Creazione QApplication...")
    app = QApplication(sys.argv)
    print(f"QApplication creata in {time.time() - start:.2f}s")

    print("Importazione MainWindow...")
    # Mockiamo AuditManager per evitare il thread di background
    from unittest.mock import patch

    with patch("src.core.audit_manager.AuditManager.instance"):
        from src.gui.main_window.main import MainWindow

        print("Istanziazione MainWindow...")
        mstart = time.time()
        # Mockiamo tutto ciò che può bloccare
        with (
            patch("src.gui.main_window.main.run_update"),
            patch("src.gui.main_window.main.perform_auto_update"),
            patch("src.gui.main_window.main.config_manager.load_config", return_value={}),
        ):
            window = MainWindow()
            print(f"MainWindow istanziata in {time.time() - mstart:.2f}s")

            print("Chiusura...")
            window.close()
            window.deleteLater()

except Exception as e:
    print(f"ERRORE: {e}")
    import traceback

    traceback.print_exc()

print(f"--- DEBUG QT INIT END (Total: {time.time() - start:.2f}s) ---")
sys.exit(0)
