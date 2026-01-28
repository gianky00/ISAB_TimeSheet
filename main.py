#!/usr/bin/env python3
"""
# SyncroJob - Sistema di Automazione Portale ISAB
Entry point principale dell'applicazione con Smart Startup.
"""

import logging
import logging.handlers
import os
import shutil
import sys
import threading
import traceback
from pathlib import Path

from src.core.config_manager import CONFIG_DIR

# --- CRASH LOGGING SETUP ---
logger = logging.getLogger("crash_logger")


def handle_exception(exc_type, exc_value, exc_traceback):
    """Gestore globale per eccezioni non gestite (Thread Principale)."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logger.critical(f"UNHANDLED EXCEPTION (MainThread):\n{error_msg}")

    for handler in logger.handlers:
        handler.flush()

    try:
        log_file = CONFIG_DIR / "logs" / "crash.log"
        if log_file.exists():
            shutil.copy2(log_file, Path(__file__).parent / "crash.log")
    except Exception:
        pass


def handle_thread_exception(args):
    """Gestore globale per eccezioni nei thread secondari."""
    error_msg = "".join(
        traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback)
    )
    logger.critical(f"UNHANDLED EXCEPTION (Thread: {args.thread.name}):\n{error_msg}")

    for handler in logger.handlers:
        handler.flush()


def setup_logging():
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)
    log_dir = CONFIG_DIR / "logs"
    log_dir.mkdir(exist_ok=True)

    app_log_file = log_dir / "syncrojob.log"
    app_handler = logging.handlers.RotatingFileHandler(
        app_log_file, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    app_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    if not root_logger.handlers:
        root_logger.addHandler(app_handler)

    crash_handler = logging.FileHandler(
        log_dir / "crash.log", mode="w", encoding="utf-8"
    )
    crash_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )

    clogger = logging.getLogger("crash_logger")
    if not clogger.handlers:
        clogger.addHandler(crash_handler)
    clogger.setLevel(logging.INFO)
    clogger.propagate = False

    sys.excepthook = handle_exception
    threading.excepthook = handle_thread_exception


setup_logging()

# Ensure src is in path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)


def main():
    import warnings
    from PyQt6.QtCore import QCoreApplication
    from PyQt6.QtNetwork import QLocalServer, QLocalSocket
    from PyQt6.QtWidgets import QApplication, QMessageBox

    try:
        from icecream import ic
        ic.configureOutput(prefix="DEBUG| ", includeContext=True)
        import builtins
        builtins.ic = ic  # type: ignore
    except ImportError:
        pass

    warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

    app = QApplication(sys.argv)
    
    # === SINGLE INSTANCE & ACTIVATION LOGIC ===
    server_name = "SyncroJob_Instance_Connector"
    socket = QLocalSocket()
    socket.connectToServer(server_name)
    
    if socket.waitForConnected(500):
        socket.write(b"ACTIVATE")
        socket.waitForBytesWritten(500)
        socket.disconnectFromServer()
        sys.exit(0)
    
    server = QLocalServer()
    server.listen(server_name)
    main_window_instance = None

    def handle_new_connection():
        client_socket = server.nextPendingConnection()
        if client_socket.waitForReadyRead(500):
            msg = client_socket.readAll().data().decode()
            if msg == "ACTIVATE" and main_window_instance:
                main_window_instance.show()
                main_window_instance.raise_()
                main_window_instance.activateWindow()
        client_socket.disconnectFromServer()

    server.newConnection.connect(handle_new_connection)

    # Configurazione path e ambiente
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(sys.executable)
        plugin_path = os.path.join(exe_dir, "_internal", "PyQt6", "Qt6", "plugins")
        if os.path.exists(plugin_path):
            QCoreApplication.addLibraryPath(plugin_path)
        os.environ["QT_SVG_ICON_DIR"] = os.path.join(exe_dir, "_internal", "assets", "icons")

    from src.core.app_initializer import AppInitializer
    from src.gui.main_window import MainWindow
    from src.gui.dialogs.startup_dialog import StartupDialog

    AppInitializer.setup_app_style(app)

    # === STARTUP LOADING WINDOW ===
    startup_dialog = StartupDialog()
    startup_dialog.show()
    
    # Funzione per aggiornare la UI durante l'inizializzazione
    def update_startup_ui(msg, prog):
        startup_dialog.update_status(msg, prog)

    # Esegui inizializzazione con feedback visivo
    if not AppInitializer.initialize(status_callback=update_startup_ui):
        startup_dialog.close()
        sys.exit(1)

    # Chiudi finestra di caricamento e apri la principale
    startup_dialog.close()

    try:
        main_window_instance = MainWindow()
        main_window_instance.showMaximized()
        exit_code = app.exec()
        server.close()
        sys.exit(exit_code)
    except Exception as e:
        logger.critical("Errore fatale GUI", exc_info=True)
        QMessageBox.critical(None, "Errore GUI", f"Errore fatale durante l'avvio:\n{e}")
        server.close()
        sys.exit(1)


if __name__ == "__main__":
    main()
