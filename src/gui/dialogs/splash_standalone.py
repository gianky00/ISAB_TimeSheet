"""
SyncroJob - Splash Screen Standalone Process
Esegue lo splash screen in un processo separato per garantire fluidità assoluta (60fps) 
indipendentemente dal carico del processo principale.
Riceve aggiornamenti di stato tramite stdin in formato JSON.
"""

import json
import os
import sys
import logging
import threading
import time
from pathlib import Path

# Setup logging base per il processo standalone
log_path = Path("data/logs/splash_process.log")
log_path.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [SPLASH] - %(levelname)s - %(message)s",
    filename=str(log_path),
    filemode="w"
)
logger = logging.getLogger("StandaloneSplash")

# Aggiungi la root del progetto al path per gli import
project_root = str(Path(__file__).parent.parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PyQt6.QtCore import QObject, pyqtSignal, QTimer, Qt
from PyQt6.QtWidgets import QApplication

from src.gui.dialogs.startup_dialog import StartupDialog

class SplashCommunicator(QObject):
    """Gestore della comunicazione thread-safe tra stdin e UI."""
    update_signal = pyqtSignal(str, int)
    close_signal = pyqtSignal()

class StandaloneSplash(StartupDialog):
    """Estensione dello StartupDialog con logging aggiuntivo e fix visibilità."""
    
    def __init__(self):
        super().__init__()
        # Forza opacità iniziale se l'animazione fallisse
        self.setWindowOpacity(1.0)
        # Assicura che sia in primo piano
        self.raise_()
        self.activateWindow()
    
    def update_status(self, message: str, progress: int):
        logger.info(f"UI UPDATE EXEC: {message} | {progress}%")
        super().update_status(message, progress)

def run_standalone():
    """Main loop dello splash screen standalone."""
    logger.info("Splash standalone process starting...")
    
    # Forza encoding UTF-8 per la comunicazione
    if sys.platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleCP(65001)
        kernel32.SetConsoleOutputCP(65001)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    splash = StandaloneSplash()
    splash.show()
    # Piccola attesa per il rendering iniziale
    QTimer.singleShot(100, lambda: splash.raise_())
    QTimer.singleShot(200, lambda: splash.activateWindow())
    
    logger.info("Splash dialog shown")

    # Setup communicator
    comm = SplashCommunicator()
    comm.update_signal.connect(splash.update_status)
    comm.close_signal.connect(splash.close)

    def read_stdin():
        logger.info("Stdin reader thread active")
        import io
        # Usiamo il buffer binario per evitare problemi di encoding su Windows
        input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', line_buffering=True)
        
        while True:
            try:
                line = input_stream.readline()
                if not line:
                    logger.info("Stdin stream closed")
                    break
                
                line = line.strip()
                if not line:
                    continue
                    
                data = json.loads(line)
                command = data.get("cmd")

                if command == "update":
                    msg = data.get("msg", "")
                    prog = int(data.get("prog", 0))
                    # logger.info(f"Signal emitted: {msg} ({prog}%)") # Troppo rumoroso
                    comm.update_signal.emit(msg, prog)
                elif command == "close":
                    logger.info("Close signal emitted")
                    comm.close_signal.emit()
                    break
            except Exception as e:
                logger.error(f"Error in stdin reader: {e}")
                continue

    input_thread = threading.Thread(target=read_stdin, daemon=True)
    input_thread.start()

    exit_code = app.exec()
    logger.info(f"Splash process exiting (code {exit_code})")
    sys.exit(exit_code)

if __name__ == "__main__":
    try:
        run_standalone()
    except Exception as e:
        logger.critical(f"FATAL: {e}", exc_info=True)
        sys.exit(1)
