#!/usr/bin/env python3
"""
# SyncroJob - Zero-Lag Startup Architecture
Tutto il caricamento (anche quello della GUI) avviene nello Splash Screen.
Le animazioni rimangono fluide grazie al refresh timer.
"""

import logging
import logging.handlers
import os
import sys
import threading
from pathlib import Path

from src.core.config_manager import CONFIG_DIR

def setup_early_logging():
    if not CONFIG_DIR.exists(): CONFIG_DIR.mkdir(parents=True)
    log_dir = CONFIG_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_dir / "startup.log", mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    root_logger.addHandler(handler)

setup_early_logging()
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

def main():
    import warnings
    from PyQt6.QtCore import QCoreApplication, QTimer
    from PyQt6.QtNetwork import QLocalServer, QLocalSocket
    from PyQt6.QtWidgets import QApplication, QMessageBox

    warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
    app = QApplication(sys.argv)

    # === SINGLE INSTANCE ===
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

    # Import veloci per lo splash
    from src.gui.dialogs.startup_dialog import StartupDialog
    from src.core.app_initializer import AppInitializer

    AppInitializer.setup_app_style(app)

    # 1. MOSTRA SPLASH SCREEN IMMEDIATAMENTE
    startup_dialog = StartupDialog()
    startup_dialog.show()

    # === ANIMATION REFRESH TIMER ===
    # Forza il refresh delle animazioni ogni 16ms (~60fps) anche durante il caricamento
    animation_timer = QTimer()
    animation_timer.setInterval(16)
    animation_timer.timeout.connect(lambda: app.processEvents())
    animation_timer.start()

    def update_startup_ui(msg, prog):
        startup_dialog.update_status(msg, prog)
        # processEvents viene già chiamato dal timer, ma lo chiamiamo anche qui per sicurezza
        app.processEvents()

    # 2. CARICA I MODULI CORE
    # (Inizializzazione database, licenza, import pandas/selenium)
    # Nota: NON passiamo ancora la mw_instance qui perché dobbiamo ancora importare MainWindow
    if not AppInitializer.initialize(status_callback=update_startup_ui):
        animation_timer.stop()
        startup_dialog.close()
        sys.exit(1)

    # 3. IMPORTA E CREA MAINWINDOW (SILENZIOSAMENTE)
    update_startup_ui("Preparazione interfaccia grafica...", 85)
    from src.gui.main_window.main import MainWindow
    main_window_instance = MainWindow()

    # 4. ESEGUI DEEP PRELOAD (Caricamento pannelli GUI)
    # Ora passiamo l'istanza appena creata per caricare i moduli interni
    AppInitializer.initialize(status_callback=update_startup_ui, mw_instance=main_window_instance)

    # 5. FINALIZZAZIONE
    update_startup_ui("Configurazione finale in corso...", 100)
    main_window_instance.finalize_init()

    # Ferma il timer delle animazioni forzate
    animation_timer.stop()

    # Piccola pausa per mostrare il 100%
    QTimer.singleShot(500, lambda: startup_dialog.close())
    QTimer.singleShot(600, lambda: main_window_instance.showMaximized())

    try:
        exit_code = app.exec()
        server.close()
        sys.exit(exit_code)
    except Exception as e:
        logging.getLogger("crash_logger").critical("Errore fatale GUI", exc_info=True)
        QMessageBox.critical(None, "Errore GUI", f"Errore fatale durante l'avvio:\n{e}")
        server.close()
        sys.exit(1)

if __name__ == "__main__":
    main()
