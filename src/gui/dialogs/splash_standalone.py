# mypy: disable-error-code="unused-ignore, arg-type"
"""
SyncroJob - Splash Screen Standalone Process
Esegue lo splash screen in un processo separato per garantire fluidità assoluta (60fps)
indipendentemente dal carico del processo principale.
Riceve aggiornamenti di stato tramite stdin in formato JSON.
"""

import json
import logging
import sys
import threading
from pathlib import Path

# Setup logging base per il processo standalone
log_path = Path("data/logs/splash_process.log")
log_path.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [SPLASH] - %(levelname)s - %(message)s",
    filename=str(log_path),
    filemode="w",
)
logger = logging.getLogger("StandaloneSplash")

# Aggiungi la root del progetto al path per gli import tramite ResourceManager
from src.utils.resource_manager import ResourceManager  # noqa: E402

project_root = str(ResourceManager.PROJECT_ROOT)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Assicura che src sia nel path
src_path = str(ResourceManager.PROJECT_ROOT / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from PyQt6.QtCore import QObject, QTimer, pyqtSignal  # noqa: E402
from PyQt6.QtWidgets import QApplication  # noqa: E402

from src.gui.dialogs.startup_dialog import StartupDialog  # noqa: E402


class SplashCommunicator(QObject):
    """Gestore della comunicazione thread-safe tra stdin e UI."""

    update_signal = pyqtSignal(str, int)
    close_signal = pyqtSignal()


class StandaloneSplash(StartupDialog):
    """Estensione dello StartupDialog con logging aggiuntivo e fix visibilità."""

    def __init__(self) -> None:
        super().__init__()
        # Forza opacità iniziale se l'animazione fallisse
        self.setWindowOpacity(1.0)
        # Assicura che sia in primo piano
        self.raise_()
        self.activateWindow()

    def update_status(self, message: str, progress: int) -> None:
        logger.info(f"UI UPDATE EXEC: {message} | {progress}%")
        super().update_status(message, progress)


def run_standalone() -> None:
    """Main loop dello splash screen standalone."""
    logger.info("Splash standalone process starting...")

    # Forza encoding UTF-8 per la comunicazione
    if sys.platform == "win32":
        import ctypes  # noqa: PLC0415

        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleCP(65001)
        kernel32.SetConsoleOutputCP(65001)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    splash = StandaloneSplash()
    splash.show()
    # Piccola attesa per il rendering iniziale
    QTimer.singleShot(100, splash.raise_)
    QTimer.singleShot(200, splash.activateWindow)

    logger.info("Splash dialog shown")

    # Setup communicator
    comm = SplashCommunicator()
    comm.update_signal.connect(splash.update_status)
    comm.close_signal.connect(splash.close)

    def read_stdin() -> None:
        logger.info("Stdin reader thread active")
        import io  # noqa: PLC0415

        # Usiamo il buffer binario per evitare problemi di encoding su Windows
        input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8", line_buffering=True)

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
                    # logger.info(f"Signal emitted: {msg} ({prog}%)") # Troppo rumoroso  # noqa: ERA001
                    comm.update_signal.emit(msg, prog)
                elif command == "close":
                    logger.info("Close signal emitted")
                    comm.close_signal.emit()
                    break
            except Exception as e:
                logger.error(f"Error in stdin reader: {e}")  # noqa: TRY400
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
