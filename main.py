#!/usr/bin/env python3
from __future__ import annotations

"""
SyncroJob - Zero-Lag Startup Architecture
Animazioni fluide a 60fps garantite tramite thread separato per il caricamento.
"""

import contextlib
import ctypes
import json
import os
import subprocess
import sys
import traceback
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, NoReturn, cast

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtWidgets import QApplication

    from src.gui.main_window.main import MainWindow

# Setup path FIRST (before any other imports)
ROOT_DIR = Path(__file__).parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def _print_exception_and_exit(
    exc_type: type[BaseException], exc_value: BaseException, exc_tb: Any
) -> NoReturn:
    """Gestore globale delle eccezioni non catturate."""
    print("FATAL UNCAUGHT EXCEPTION:")
    traceback.print_exception(exc_type, exc_value, exc_tb)
    import contextlib

    with contextlib.suppress(Exception):
        from src.core.config_manager import CONFIG_DIR

        crash_file = CONFIG_DIR / "crash.txt"
        with crash_file.open("a", encoding="utf-8") as f:
            f.write(
                f"\n[{datetime.now(UTC).astimezone().strftime('%Y-%m-%d %H:%M:%S')}] NATIVE FATAL UNCAUGHT EXCEPTION:\n"
            )
            traceback.print_exception(exc_type, exc_value, exc_tb, file=f)
    sys.exit(1)


sys.excepthook = _print_exception_and_exit

from src.core.config_manager import CONFIG_DIR
from src.core.logging import (
    configure_logging,
    get_logger,
)
from src.utils.resource_manager import ResourceManager

# Setup path (ResourceManager handles frozen vs dev)
ROOT_DIR = ResourceManager.PROJECT_ROOT
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def setup_enterprise_logging() -> Any:
    """Initialize enterprise logging system."""
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir(parents=True)

    crash_file = CONFIG_DIR / "crash.txt"
    import contextlib

    with contextlib.suppress(Exception):
        crash_file.write_text(
            "=== SYNCROJOB CRASH LOG ===\nNessun crash rilevato in questa sessione.\n", encoding="utf-8"
        )
        import faulthandler

        crash_native_file = crash_file.open("a", encoding="utf-8")
        crash_native_file.write("\n[DEBUG] Native C++ faulthandler engine enabled.\n")
        crash_native_file.flush()
        faulthandler.enable(file=crash_native_file)

    configure_logging()
    logger = get_logger("startup")
    logger.info("Enterprise logging system initialized")
    return logger


if "--splash-mode" in sys.argv:
    from src.gui.dialogs.splash_standalone import run_standalone

    run_standalone()
    sys.exit(0)

startup_logger_global = setup_enterprise_logging()


def _setup_windows_taskbar(app: QApplication) -> None:
    """Configura l'icona della taskbar e l'AppUserModelID su Windows."""
    from PySide6.QtGui import QIcon

    from src.core.version import __version__

    if os.name == "nt":
        try:
            myappid = f"SyncroJob.Manager.{__version__}"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            startup_logger_global.warning(f"Failed to set AppUserModelID: {e}")

    try:
        app_icon_path = ResourceManager.get_asset_path("app.ico")
        if Path(app_icon_path).exists():
            app.setWindowIcon(QIcon(app_icon_path))
    except Exception as e:
        startup_logger_global.warning(f"Failed to set global window icon: {e}")


def _check_single_instance() -> None:
    """Verifica se l'applicazione è già in esecuzione."""
    from PySide6.QtNetwork import QLocalSocket

    socket = QLocalSocket()
    socket.connectToServer("SyncroJob_Instance_Connector")
    if socket.waitForConnected(500):
        startup_logger_global.info("Another instance found, activating it and exiting.")
        socket.write(b"ACTIVATE")
        socket.waitForBytesWritten(500)
        socket.disconnectFromServer()
        sys.exit(0)


def _run_phase1(
    app: QApplication,
    update_splash: Callable[[str, int], None],
    close_splash: Callable[[], None],
    logger: Any,
) -> None:
    """Esegue la fase 1 di inizializzazione (import pesanti) in un thread separato."""
    from PySide6.QtCore import QObject, QThread, Signal

    class Phase1Worker(QObject):
        progress = Signal(str, int)
        finished = Signal(bool, str)

        def run(self) -> None:
            try:
                from src.core.app_initializer import AppInitializer

                logger.info("Starting Phase 1 initialization")
                success = AppInitializer.initialize_core(progress_callback=self.progress.emit)
                logger.info("Phase 1 completed", success=success)
                self.finished.emit(success, "" if success else "Inizializzazione fallita")
            except Exception as e:
                logger.exception("Phase 1 initialization failed", exc=e)
                self.finished.emit(False, str(e))

    phase1_done = [False]
    phase1_res = [False, ""]

    def on_finished(s: bool, m: str) -> None:
        phase1_done[0] = True
        phase1_res[0] = s
        phase1_res[1] = m

    thread = QThread()
    worker = Phase1Worker()
    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.progress.connect(update_splash)
    worker.finished.connect(on_finished)
    thread.start()

    while not phase1_done[0]:
        app.processEvents()
    thread.quit()
    thread.wait(1000)

    if not phase1_res[0]:
        close_splash()
        from src.gui.dialogs.confirmation_dialog import ConfirmationDialog

        ConfirmationDialog.show_error(None, "Errore Avvio", cast("str", phase1_res[1]))
        sys.exit(1)


def _run_phase3(
    app: QApplication, mw: MainWindow, update: Callable[[str, int], None], close: Callable[[], None], log: Any
) -> None:
    """Esegue la fase 3 di precaricamento GUI."""
    from PySide6.QtCore import QTimer

    from src.core.app_initializer import AppInitializer

    gen = AppInitializer.init_generator(mw)

    def finalize() -> None:
        log.info("Finalizing startup...")
        update("Avvio completato", 100)
        mw.show()
        mw.showMaximized()
        mw.raise_()
        mw.activateWindow()
        app.processEvents()
        close()
        QTimer.singleShot(100, mw.finalize_init)

    def next_step() -> None:
        try:
            m, p = next(gen)
            update(m, p)
            QTimer.singleShot(0, next_step)
        except StopIteration:
            finalize()
        except Exception as e:
            log.exception("Error in phase 3", exc=e)
            finalize()

    QTimer.singleShot(10, next_step)


def _start_instance_server() -> Any:
    """Avvia il server per la gestione della singola istanza."""
    from PySide6.QtNetwork import QLocalServer

    server = QLocalServer()
    server.listen("SyncroJob_Instance_Connector")
    return server


class SplashPipeWriter:
    """Gestisce la comunicazione sicura e binaria verso lo splash screen standalone."""

    def __init__(self, sp: subprocess.Popen[bytes]) -> None:
        self.sp = sp

    def _write(self, data_dict: dict[str, Any]) -> None:
        if self.sp.poll() is None and self.sp.stdin:
            data = json.dumps(data_dict) + "\n"
            with contextlib.suppress(OSError):
                self.sp.stdin.write(data.encode("utf-8"))
                self.sp.stdin.flush()

    def update(self, msg: str, prog: int) -> None:
        """Invia un comando di aggiornamento avanzamento allo splash screen."""
        self._write({"cmd": "update", "msg": msg.replace("\n", " "), "prog": prog})

    def send_license(self, cliente: str, hw_id: str, scadenza: str) -> None:
        """Invia i dati di licenza decifrati allo splash screen."""
        self._write({"cmd": "license_info", "cliente": cliente, "hw_id": hw_id, "scadenza": scadenza})

    def close(self) -> None:
        """Invia il segnale di chiusura e attende la terminazione del processo splash."""
        if self.sp.poll() is None and self.sp.stdin:
            self._write({"cmd": "close"})
            with contextlib.suppress(OSError):
                self.sp.stdin.close()
            try:
                self.sp.wait(0.1)
            except subprocess.TimeoutExpired:
                self.sp.kill()


def _init_splash() -> tuple[Callable[[str, int], None], Callable[[], None], Callable[[str, str, str], None]]:
    """Inizializza il processo splash e restituisce le funzioni di controllo."""
    cmd = (
        [sys.executable, "--splash-mode"]
        if getattr(sys, "frozen", False)
        else [sys.executable, str(ROOT_DIR / "src" / "gui" / "dialogs" / "splash_standalone.py")]
    )
    sp = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        bufsize=0,  # Unbuffered per trasmissione istantanea
        env=os.environ | {"PYTHONUNBUFFERED": "1", "PYTHONPATH": str(ROOT_DIR)},
    )
    writer = SplashPipeWriter(sp)
    return writer.update, writer.close, writer.send_license


def _send_license_to_splash(send_lic_fn: Callable[[str, str, str], None]) -> None:
    """Invia in modo sicuro i dati di licenza (in cache o reali) allo splash screen."""
    try:
        from src.core.license_validator import get_hardware_id, get_license_client, get_license_expiry

        cliente = get_license_client()
        hw_id = get_hardware_id()
        scadenza = get_license_expiry()
        get_logger("startup").info(f"Invio dati licenza allo splash: {cliente} | {hw_id} | {scadenza}")
        send_lic_fn(cliente, hw_id, scadenza)
    except Exception as e:
        get_logger("startup").warning(f"Impossibile inviare dati licenza allo splash: {e}")


def main() -> None:
    """Application entry point with three-phase startup architecture."""
    if getattr(sys, "frozen", False) and getattr(sys, "stderr", None) is None:
        sys.stdout = open(os.devnull, "w")  # noqa: SIM115
        sys.stderr = open(os.devnull, "w")  # noqa: SIM115

    from PySide6.QtWidgets import QApplication

    from src.gui.main_window.main import MainWindow

    app = QApplication(sys.argv)
    _setup_windows_taskbar(app)
    _check_single_instance()

    server: Any = _start_instance_server()
    mw_inst: MainWindow | None = None

    def handle_conn() -> None:
        """Gestisce le connessioni in entrata per l'attivazione della singola istanza."""
        c = server.nextPendingConnection()
        if c and c.waitForReadyRead(500) and bytes(c.read(1024)).decode() == "ACTIVATE" and mw_inst:
            mw_inst.show()
            mw_inst.raise_()
            mw_inst.activateWindow()
        if c:
            c.disconnectFromServer()

    server.newConnection.connect(handle_conn)
    upd, cls, send_lic = _init_splash()

    from src.core.audit.signals import AuditSignals
    from src.core.notification_manager import NotificationManager

    # Pre-inizializzazione sicura dei Singleton QObject sul Main Thread
    # Previene l'errore "access violation" quando emettono segnali dopo la morte del Phase1Worker
    AuditSignals.instance()
    NotificationManager.instance()

    # Invia immediatamente i dati di licenza reali (o memorizzati) allo splash screen
    _send_license_to_splash(send_lic)

    upd("Inizializzazione Nucleo...", 5)
    _run_phase1(app, upd, cls, get_logger("phase1"))

    # Invia nuovamente i dati di licenza aggiornati dopo la Fase 1
    _send_license_to_splash(send_lic)

    from src.core.app_initializer import AppInitializer
    from src.gui.dialogs.confirmation_dialog import ConfirmationDialog

    for s, m in AppInitializer.get_alerts():
        if s in ("CRITICAL", "ERROR"):
            ConfirmationDialog.show_error(None, "Licenza", m, is_rich_text=True)
        elif s == "WARNING":
            ConfirmationDialog.show_warning(None, "Licenza", m, is_rich_text=True)
        else:
            ConfirmationDialog.show_info(None, "Licenza", m, is_rich_text=True)

    upd("Costruzione interfaccia...", 40)
    app.processEvents()
    mw_inst = MainWindow()
    _run_phase3(app, mw_inst, upd, cls, get_logger("startup"))

    try:
        sys.exit(app.exec())
    except Exception as e:
        get_logger("crash").exception("Fatal crash", exc=e)
        sys.exit(1)


if __name__ == "__main__":
    main()
