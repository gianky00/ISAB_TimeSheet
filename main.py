#!/usr/bin/env python3
"""
SyncroJob - Zero-Lag Startup Architecture
Animazioni fluide a 60fps garantite tramite thread separato per il caricamento.
"""

import logging
import logging.handlers
import os
import sys

from src.core.config_manager import CONFIG_DIR


def setup_early_logging():
    """Initialize early file logging before the application starts."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)
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
    """Application entry point with three-phase startup architecture."""
    import warnings

    from PyQt6.QtCore import QObject, QThread, QTimer, pyqtSignal
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
        """Handle incoming connection from another instance to activate window."""
        client_socket = server.nextPendingConnection()
        if client_socket.waitForReadyRead(500):
            msg = client_socket.readAll().data().decode()
            if msg == "ACTIVATE" and main_window_instance:
                main_window_instance.show()
                main_window_instance.raise_()
                main_window_instance.activateWindow()
        client_socket.disconnectFromServer()

    server.newConnection.connect(handle_new_connection)

    # === SETUP STYLE ===
    from src.core.app_initializer import AppInitializer

    AppInitializer.setup_app_style(app)

    # === SPLASH SCREEN ===
    from src.gui.dialogs.startup_dialog import StartupDialog

    splash = StartupDialog()
    splash.show()
    app.processEvents()

    # === WORKER PER FASE 1 (Import pesanti) - Thread separato ===
    class Phase1Worker(QObject):
        """Worker thread for Phase 1 initialization (heavy imports)."""

        progress = pyqtSignal(str, int)
        finished = pyqtSignal(bool)

        def run(self):
            """Execute Phase 1 initialization in background thread."""
            try:
                from src.core.app_initializer import AppInitializer

                # FASE 1 ora usa initialize_core (ritorna bool)
                success = AppInitializer.initialize_core()
                self.finished.emit(success)
            except Exception as e:
                logging.getLogger("Phase1").error(f"Error: {e}")
                self.finished.emit(False)

    # Variabili di stato
    phase1_done = [False]
    phase1_success = [False]

    def on_phase1_progress(msg, prog):
        """Update splash screen with Phase 1 progress."""
        splash.update_status(msg, prog)

    def on_phase1_finished(success):
        """Handle Phase 1 completion and store result."""
        phase1_done[0] = True
        phase1_success[0] = success

    # Avvia thread per fase 1
    thread1 = QThread()
    worker1 = Phase1Worker()
    worker1.moveToThread(thread1)
    thread1.started.connect(worker1.run)
    worker1.progress.connect(on_phase1_progress)
    worker1.finished.connect(on_phase1_finished)
    thread1.start()

    # Attendi completamento fase 1 mantenendo GUI fluida
    while not phase1_done[0]:
        app.processEvents()

    # Cleanup thread 1
    thread1.quit()
    thread1.wait(1000)

    if not phase1_success[0]:
        splash.close()
        QMessageBox.critical(None, "Errore", "Inizializzazione fallita")
        sys.exit(1)

    # === FASE 2: Creazione MainWindow (Thread principale richiesto da Qt) ===
    splash.update_status("Costruzione interfaccia...", 40)
    app.processEvents()

    from src.gui.main_window.main import MainWindow

    main_window_instance = MainWindow()
    app.processEvents()

    # === FASE 3: Preload GUI con Generatore Non-Bloccante ===

    # Inizializza generatore
    gui_init_gen = AppInitializer.init_generator(main_window_instance)

    def finalize_startup():
        """Called when initialization is complete."""
        try:
            logging.getLogger("Startup").info("Finalizing startup sequence...")
            splash.update_status("Avvio completato", 100)

            logging.getLogger("Startup").info("Calling finalize_init...")
            main_window_instance.finalize_init()

            logging.getLogger("Startup").info("Showing main window...")
            # Show main window FIRST (hidden behind splash)
            main_window_instance.show()
            main_window_instance.showMaximized()
            main_window_instance.raise_()
            main_window_instance.activateWindow()

            logging.getLogger("Startup").info("Main window shown, closing splash...")
            # Process events to ensure window is rendered
            app.processEvents()

            # Close splash - main window will automatically come to front
            splash.close()

            logging.getLogger("Startup").info("Startup finalized successfully")
        except Exception as e:
            logging.getLogger("Startup").critical(
                f"Error in finalize_startup: {e}", exc_info=True
            )

    def process_next_step():
        """Execute one initialization step and yield to event loop."""
        try:
            # Esegue UN solo step e ritorna subito
            msg, prog = next(gui_init_gen)
            logging.getLogger("Startup").info(f"Init step: {msg} ({prog}%)")
            splash.update_status(msg, prog)

            # Pianifica il prossimo step al prossimo ciclo di eventi libero (0ms)
            # Questo permette alla GUI di aggiornarsi e alle animazioni di avanzare
            QTimer.singleShot(0, process_next_step)

        except StopIteration:
            # Generatore esaurito = Init completata
            logging.getLogger("Startup").info("Initialization generator completed")
            finalize_startup()
        except Exception as e:
            logging.getLogger("Startup").error(
                f"Error in init loop: {e}", exc_info=True
            )
            finalize_startup()  # Try to proceed anyway

    # Avvia la catena di inizializzazione
    QTimer.singleShot(10, process_next_step)

    try:
        exit_code = app.exec()
        server.close()
        sys.exit(exit_code)
    except Exception as e:
        logging.getLogger("crash").critical("Fatal error", exc_info=True)
        QMessageBox.critical(None, "Errore", f"Errore fatale:\n{e}")
        server.close()
        sys.exit(1)


if __name__ == "__main__":
    main()
