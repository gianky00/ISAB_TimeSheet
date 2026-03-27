#!/usr/bin/env python3
from __future__ import annotations

"""
SyncroJob - Zero-Lag Startup Architecture
Animazioni fluide a 60fps garantite tramite thread separato per il caricamento.
"""

import os
import sys
import traceback
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.gui.main_window.main import MainWindow

# Setup path FIRST (before any other imports)
ROOT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(ROOT_DIR / "src"))


def _print_exception_and_exit(exc_type, exc_value, exc_tb):  # noqa: ANN001, ANN202
    print("FATAL UNCAUGHT EXCEPTION:")
    traceback.print_exception(exc_type, exc_value, exc_tb)
    # Salvataggio del crash di basso livello nativo
    import contextlib  # noqa: PLC0415

    with contextlib.suppress(Exception):
        from src.core.config_manager import CONFIG_DIR  # noqa: PLC0415

        crash_file = CONFIG_DIR / "crash.txt"
        with crash_file.open("a", encoding="utf-8") as f:
            f.write(
                f"\n[{datetime.now(UTC).astimezone().strftime('%Y-%m-%d %H:%M:%S')}] NATIVE FATAL UNCAUGHT EXCEPTION:\n"
            )
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


def setup_enterprise_logging():  # noqa: ANN201
    """Initialize enterprise logging system."""
    # Ensure config directory exists
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)

    # Assicurati che il file crash esista e puliscilo per la nuova sessione
    crash_file = CONFIG_DIR / "crash.txt"
    import contextlib  # noqa: PLC0415

    with contextlib.suppress(Exception):
        crash_file.write_text(
            "=== SYNCROJOB CRASH LOG ===\nNessun crash rilevato in questa sessione.\n", encoding="utf-8"
        )

        # Abilita traceback a livello C/C++ (Segmentation Fault, Access Violation)
        import faulthandler  # noqa: PLC0415

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


def main():  # noqa: ANN201, PLR0915
    """Application entry point with three-phase startup architecture."""
    # CRITICAL: Redirect stdout/stderr to devnull in frozen/noconsole mode
    # This prevents crashes when libraries try to print to a non-existent console
    if getattr(sys, "frozen", False) and getattr(sys, "stderr", None) is None:
        sys.stdout = open(os.devnull, "w")  # noqa: SIM115
        sys.stderr = open(os.devnull, "w")  # noqa: SIM115

    # === SPLASH SCREEN (Standalone Process for Zero-Stutter) ===
    # Lancia lo splash immediatamente prima di ogni altro import Qt/Pesante
    import json  # noqa: PLC0415
    import subprocess  # noqa: PLC0415

    splash_script = str(ROOT_DIR / "src" / "gui" / "dialogs" / "splash_standalone.py")
    startup_logger_global.info(f"Launching standalone splash process: {splash_script}")

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["PYTHONPATH"] = str(ROOT_DIR)

    splash_process = subprocess.Popen(
        [sys.executable, splash_script],
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1,
        encoding="utf-8",
        env=env,
    )

    def update_splash(msg: str, prog: int):  # noqa: ANN202
        if splash_process.poll() is None and splash_process.stdin:
            try:
                clean_msg = msg.replace("\n", " ").replace("\r", "").strip()
                data = json.dumps({"cmd": "update", "msg": clean_msg, "prog": prog}, ensure_ascii=False)
                splash_process.stdin.write(data + "\n")
                splash_process.stdin.flush()
            except Exception as e:
                startup_logger_global.warning(f"Failed to update splash process: {e}")

    def close_splash():  # noqa: ANN202
        if splash_process.poll() is None and splash_process.stdin:
            try:
                data = json.dumps({"cmd": "close"})
                splash_process.stdin.write(data + "\n")
                splash_process.stdin.flush()
                splash_process.stdin.close()
                try:
                    splash_process.wait(timeout=1.5)
                except subprocess.TimeoutExpired:
                    splash_process.kill()
            except Exception:
                splash_process.kill()

    update_splash("Inizializzazione Nucleo...", 5)

    import warnings  # noqa: PLC0415

    from PyQt6.QtCore import QObject, QThread, QTimer, pyqtSignal  # noqa: PLC0415
    from PyQt6.QtNetwork import QLocalServer, QLocalSocket  # noqa: PLC0415
    from PyQt6.QtWidgets import QApplication  # noqa: PLC0415

    # Get loggers
    logger = get_logger("main")
    phase1_logger = get_logger("phase1")
    startup_logger = get_logger("startup")
    crash_logger = get_logger("crash")

    app_trace_id = generate_trace_id()
    logger.info("Application starting", app_trace_id=app_trace_id)

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

    def handle_new_connection():  # noqa: ANN202
        client_socket = server.nextPendingConnection()
        if client_socket and client_socket.waitForReadyRead(500):
            data = client_socket.read(1024)
            msg = data.decode("utf-8", errors="ignore")
            if msg == "ACTIVATE" and main_window_instance:
                main_window_instance.show()
                main_window_instance.raise_()
                main_window_instance.activateWindow()
        if client_socket:
            client_socket.disconnectFromServer()

    server.newConnection.connect(handle_new_connection)

    # === SETUP STYLE ===
    from src.gui.main_window.app_styler import AppStyler  # noqa: PLC0415
    AppStyler.setup_app_style(app)
    app.processEvents()

    # === WORKER PER FASE 1 (Import pesanti) - Thread separato ===
    class Phase1Worker(QObject):
        """Worker thread for Phase 1 initialization (heavy imports)."""

        progress = pyqtSignal(str, int)
        finished = pyqtSignal(bool, str)

        def run(self):  # noqa: ANN202
            """Execute Phase 1 initialization in background thread."""
            try:
                from src.core.app_initializer import AppInitializer  # noqa: PLC0415

                phase1_logger.info("Starting Phase 1 initialization")

                # FASE 1 ora usa initialize_core con callback di progresso
                success = AppInitializer.initialize_core(progress_callback=self.progress.emit)

                phase1_logger.info("Phase 1 completed", success=success)
                if not success:
                    self.finished.emit(False, "Errore generico di inizializzazione")
                else:
                    self.finished.emit(True, "")
            except Exception as e:
                phase1_logger.exception("Phase 1 initialization failed", exc=e)
                self.finished.emit(False, str(e))

    # Variabili di stato
    phase1_done = [False]
    phase1_success = [False]
    phase1_error_msg = [""]

    def on_phase1_progress(msg, prog):  # noqa: ANN001, ANN202
        """Update splash screen with Phase 1 progress."""
        update_splash(msg, prog)

    def on_phase1_finished(success, error_msg):  # noqa: ANN001, ANN202
        """Handle Phase 1 completion and store result."""
        phase1_done[0] = True
        phase1_success[0] = success
        phase1_error_msg[0] = error_msg

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

    from src.gui.dialogs.confirmation_dialog import ConfirmationDialog  # noqa: PLC0415

    if not phase1_success[0]:
        close_splash()
        err_text = phase1_error_msg[0] or "Inizializzazione fallita"
        ConfirmationDialog.show_error(None, "Errore Avvio", err_text)
        sys.exit(1)

    # Visualizzazione Avvisi Accumulati (Non-Bloccanti ma importanti per l'utente)
    from src.core.app_initializer import AppInitializer  # noqa: PLC0415

    for severity, message in AppInitializer.get_alerts():
        if severity in ("CRITICAL", "ERROR"):
            ConfirmationDialog.show_error(None, "Allerta Licenza", message, is_rich_text=True)
        elif severity == "WARNING":
            ConfirmationDialog.show_warning(None, "Avviso Licenza", message, is_rich_text=True)
        else:
            ConfirmationDialog.show_info(None, "Sincronizzazione", message, is_rich_text=True)

    # === FASE 2: Creazione MainWindow (Thread principale richiesto da Qt) ===
    update_splash("Costruzione interfaccia...", 40)
    app.processEvents()

    from src.gui.main_window.main import MainWindow  # noqa: PLC0415

    main_window_instance = MainWindow()
    app.processEvents()

    # === FASE 3: Preload GUI con Generatore Non-Bloccante ===

    # Inizializza generatore
    gui_init_gen = AppInitializer.init_generator(main_window_instance)

    def finalize_startup():  # noqa: ANN202
        """Called when initialization is complete."""
        try:
            startup_logger.info("Finalizing startup sequence...")
            update_splash("Avvio completato", 100)

            # Show main window sequences (from main branch)
            main_window_instance.show()
            main_window_instance.showMaximized()
            main_window_instance.raise_()
            main_window_instance.activateWindow()

            startup_logger.info("Main window shown, closing splash...")
            # Process events to ensure window is rendered
            app.processEvents()

            # Close splash process
            close_splash()

            startup_logger.info("Calling finalize_init...")
            # Ritardiamo leggermente finalize_init per dare priorità al rendering dell'UI
            QTimer.singleShot(100, main_window_instance.finalize_init)

            startup_logger.info("Startup finalized successfully")
        except Exception as e:
            startup_logger.exception("Error in finalize_startup", exc=e)

    def process_next_step():  # noqa: ANN202
        """Execute one initialization step and yield to event loop."""
        try:
            # Esegue UN solo step e ritorna subito
            msg, prog = next(gui_init_gen)
            startup_logger.debug("Init step", step_message=msg, progress=prog)
            update_splash(msg, prog)

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
            crash_file = log_dir / f"crash_{datetime.now(UTC).astimezone().strftime('%Y%m%d_%H%M%S')}.txt"
            report: list[str] = []
            report.extend(("=== TRACEBACK ===\n", traceback.format_exc()))

            crash_content = (
                f"=== CRASH REPORT ===\n"
                f"Timestamp: {datetime.now(UTC).astimezone().strftime('%d/%m/%Y %H:%M:%S')}\n"
                f"Trace ID: {app_trace_id}\n"
                f"Error: {e!s}\n\n" + "".join(report)
            )

            crash_file.write_text(crash_content, encoding="utf-8")

            # Scrivi anche nel file globale pulito all'avvio
            with global_crash_file.open("w", encoding="utf-8") as f:
                f.write(crash_content)

        except Exception as io_error:
            print(f"Failed to write crash.txt: {io_error}")

        from src.gui.dialogs.confirmation_dialog import ConfirmationDialog  # noqa: PLC0415

        ConfirmationDialog.show_error(
            None,
            "Errore Fatale",
            f"Errore improvviso:\n{e}\n\nDettagli salvati in: {crash_file or 'logs'}",
        )
        server.close()
        sys.exit(1)


if __name__ == "__main__":
    main()
