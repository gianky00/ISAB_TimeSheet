#!/usr/bin/env python3
from __future__ import annotations

"""
SyncroJob - Zero-Lag Startup Architecture
Animazioni fluide a 60fps garantite tramite thread separato per il caricamento.
"""

import os
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.gui.main_window.main import MainWindow

# Setup path FIRST (before any other imports)
ROOT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(ROOT_DIR / "src"))


def _print_exception_and_exit(exc_type, exc_value, exc_tb):
    print("FATAL UNCAUGHT EXCEPTION:")
    traceback.print_exception(exc_type, exc_value, exc_tb)
    # Salvataggio del crash di basso livello nativo
    import contextlib

    with contextlib.suppress(Exception):
        from src.core.config_manager import CONFIG_DIR

        crash_file = CONFIG_DIR / "crash.txt"
        with crash_file.open("a", encoding="utf-8") as f:
            f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] NATIVE FATAL UNCAUGHT EXCEPTION:\n")
            traceback.print_exception(exc_type, exc_value, exc_tb, file=f)
    sys.exit(1)


sys.excepthook = _print_exception_and_exit

from src.core.config_manager import CONFIG_DIR

# Now we can import our logging system
from src.core.logging import (
    configure_logging,
    generate_trace_id,
    get_logger,
)


def setup_enterprise_logging():
    """Initialize enterprise logging system."""
    # Ensure config directory exists
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)

    # Assicurati che il file crash esista e puliscilo per la nuova sessione
    crash_file = CONFIG_DIR / "crash.txt"
    import contextlib

    with contextlib.suppress(Exception):
        crash_file.write_text(
            "=== SYNCROJOB CRASH LOG ===\nNessun crash rilevato in questa sessione.\n", encoding="utf-8"
        )

        # Abilita traceback a livello C/C++ (Segmentation Fault, Access Violation)
        import faulthandler

        # Mantiene il file aperto per faulthandler in modo safely append
        crash_native_file = crash_file.open("a", encoding="utf-8")
        crash_native_file.write("\n[DEBUG] Native C++ faulthandler engine enabled.\n")
        crash_native_file.flush()
        faulthandler.enable(file=crash_native_file)

    # Configure logging system
    configure_logging()

    # Get startup logger
    logger = get_logger("startup")
    logger.info("Enterprise logging system initialized")

    return logger


# Initialize enterprise logging
startup_logger_global = setup_enterprise_logging()


def main():
    """Application entry point with three-phase startup architecture."""
    import warnings

    from PyQt6.QtCore import QObject, QThread, QTimer, pyqtSignal
    from PyQt6.QtNetwork import QLocalServer, QLocalSocket
    from PyQt6.QtWidgets import QApplication, QMessageBox

    # Get loggers
    logger = get_logger("main")
    phase1_logger = get_logger("phase1")
    startup_logger = get_logger("startup")
    crash_logger = get_logger("crash")

    # Application trace ID per questa sessione
    app_trace_id = generate_trace_id()
    logger.info("Application starting", app_trace_id=app_trace_id)

    # CRITICAL: Redirect stdout/stderr to devnull in frozen/noconsole mode
    # This prevents crashes when libraries try to print to a non-existent console
    if getattr(sys, "frozen", False) and getattr(sys, "stderr", None) is None:
        sys.stdout = open(os.devnull, "w")  # noqa: SIM115
        sys.stderr = open(os.devnull, "w")  # noqa: SIM115

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
    main_window_instance: MainWindow | None = None

    def handle_new_connection():
        """Handle incoming connection from another instance to activate window."""
        client_socket = server.nextPendingConnection()
        if client_socket and client_socket.waitForReadyRead(500):
            msg = client_socket.readAll().data().decode()
            if msg == "ACTIVATE" and main_window_instance:
                main_window_instance.show()
                main_window_instance.raise_()
                main_window_instance.activateWindow()
        if client_socket:
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

                phase1_logger.info("Starting Phase 1 initialization")
                # FASE 1 ora usa initialize_core (ritorna bool)
                success = AppInitializer.initialize_core()
                phase1_logger.info("Phase 1 completed", success=success)
                self.finished.emit(success)
            except Exception as e:
                phase1_logger.exception("Phase 1 initialization failed", exc=e)
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
            startup_logger.info("Finalizing startup sequence...")
            splash.update_status("Avvio completato", 100)

            startup_logger.info("Showing main window...")
            # Show main window FIRST (hidden behind splash)
            main_window_instance.show()
            main_window_instance.showMaximized()
            main_window_instance.raise_()
            main_window_instance.activateWindow()

            startup_logger.info("Main window shown, closing splash...")
            # Process events to ensure window is rendered
            app.processEvents()

            # Close splash - main window will automatically come to front
            splash.close()

            startup_logger.info("Calling finalize_init...")
            # Ritardiamo leggermente finalize_init per dare priorità al rendering dell'UI
            QTimer.singleShot(100, main_window_instance.finalize_init)

            startup_logger.info("Startup finalized successfully")
        except Exception as e:
            startup_logger.exception("Error in finalize_startup", exc=e)

    def process_next_step():
        """Execute one initialization step and yield to event loop."""
        try:
            # Esegue UN solo step e ritorna subito
            msg, prog = next(gui_init_gen)
            startup_logger.debug("Init step", step_message=msg, progress=prog)
            splash.update_status(msg, prog)

            # Pianifica il prossimo step al prossimo ciclo di eventi libero (0ms)
            # Questo permette alla GUI di aggiornarsi e alle animazioni di avanzare
            QTimer.singleShot(0, process_next_step)

        except StopIteration:
            # Generatore esaurito = Init completata
            startup_logger.info("Initialization generator completed")
            finalize_startup()
        except Exception as e:
            startup_logger.exception("Error in init loop", exc=e)
            finalize_startup()  # Try to proceed anyway

    # Avvia la catena di inizializzazione
    QTimer.singleShot(10, process_next_step)

    try:
        logger.info("Application started successfully")
        exit_code = app.exec()
        logger.info("Application exiting", exit_code=exit_code)
        server.close()
        sys.exit(exit_code)
    except Exception as e:
        crash_logger.exception("Fatal application crash", exc=e, app_trace_id=app_trace_id)

        # Write explicitly to crash.txt for user visibility
        crash_file = None
        global_crash_file = CONFIG_DIR / "crash.txt"
        try:
            log_dir = CONFIG_DIR / "logs" / "errors"
            log_dir.mkdir(exist_ok=True, parents=True)
            crash_file = log_dir / f"crash_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            report: list[str] = []
            report.extend(("=== TRACEBACK ===\n", traceback.format_exc()))

            crash_content = (
                f"=== CRASH REPORT ===\n"
                f"Timestamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                f"Trace ID: {app_trace_id}\n"
                f"Error: {e!s}\n\n" + "".join(report)
            )

            crash_file.write_text(crash_content, encoding="utf-8")

            # Scrivi anche nel file globale pulito all'avvio
            with global_crash_file.open("w", encoding="utf-8") as f:
                f.write(crash_content)

        except Exception as io_error:
            print(f"Failed to write crash.txt: {io_error}")

        QMessageBox.critical(
            None,
            "Errore",
            f"Errore fatale:\n{e}\n\nDettagli salvati in: {crash_file or 'logs'}",
        )
        server.close()
        sys.exit(1)


if __name__ == "__main__":
    main()
