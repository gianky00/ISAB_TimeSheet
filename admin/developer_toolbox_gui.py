#!/usr/bin/env python3
"""
SyncroJob Developer Toolbox - GUI Edition
==========================================
Interfaccia grafica per tutti gli strumenti di sviluppo del progetto.
"""

import os
import subprocess
import sys
import webbrowser
from collections.abc import Callable
from pathlib import Path

from PyQt6.QtCore import QProcess, QProcessEnvironment, Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QTextCursor
from PyQt6.QtWidgets import (
    QApplication,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# Configurazione
PROJECT_ROOT = Path(__file__).parent.parent
if sys.platform == "win32":
    VENV_PYTHON = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
    VENV_BIN = PROJECT_ROOT / ".venv" / "Scripts"
else:
    VENV_PYTHON = PROJECT_ROOT / ".venv" / "bin" / "python"
    VENV_BIN = PROJECT_ROOT / ".venv" / "bin"


class CommandRunner(QThread):
    """Thread per eseguire comandi senza bloccare la UI"""

    output_received = pyqtSignal(str)
    finished_signal = pyqtSignal(int)

    def __init__(self, command: list[str], shell: bool = False):
        super().__init__()
        self.command = command
        self.shell = shell
        self.process: QProcess | subprocess.Popen[str] | None = None

    def run(self):
        """Esegue il comando e emette l'output in tempo reale"""
        try:
            # Variabili d'ambiente per forzare ASCII e UTF-8
            env_vars = os.environ.copy()
            env_vars["PYTHONIOENCODING"] = "utf-8"
            env_vars["PYTHONUTF8"] = "1"
            env_vars["TERM"] = "dumb"  # Disabilita caratteri speciali Rich
            env_vars["NO_COLOR"] = "1"  # Disabilita colori se problematici
            env_vars["PYTHONUNBUFFERED"] = "1"  # Forza unbuffered output

            if self.shell:
                # Per comandi shell (mkdocs serve, ecc.)
                self.process = QProcess()
                self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)

                # Imposta variabili d'ambiente
                q_env = QProcessEnvironment.systemEnvironment()
                for k, v in env_vars.items():
                    q_env.insert(k, v)
                self.process.setProcessEnvironment(q_env)

                # self.process.readyRead.connect(self._read_output)  # Preferiamo lettura manuale in loop
                # self.process.finished.connect(lambda code, status: self._on_finished(code))

                program = self.command[0]
                args = self.command[1:] if len(self.command) > 1 else []
                self.process.start(program, args)

                # Loop per leggere output in tempo reale con QProcess in un QThread (senza event loop)
                while self.process.state() == QProcess.ProcessState.Running:
                    if self.process.waitForReadyRead(100):
                        self._read_output()

                self.process.waitForFinished(-1)
                self._read_output()  # Un'ultima lettura per sicurezza
                self.finished_signal.emit(self.process.exitCode())
            else:
                # Esecuzione con streaming output in tempo reale (merged stdout/stderr)
                process = subprocess.Popen(
                    self.command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=str(PROJECT_ROOT),
                    encoding="utf-8",
                    errors="replace",
                    env=env_vars,
                    bufsize=1,  # Line buffered
                    universal_newlines=True,
                )
                self.process = process

                # Leggi output in tempo reale senza read-ahead buffer
                if process.stdout:
                    for line in iter(process.stdout.readline, ""):
                        self.output_received.emit(line)

                # Aspetta che il processo finisca
                returncode = process.wait()
                self.finished_signal.emit(returncode)

        except Exception as e:
            self.output_received.emit(f"\n[ERROR] {e!s}\n")
            self.finished_signal.emit(1)

    def _read_output(self):
        """Legge output dal processo QProcess"""
        if isinstance(self.process, QProcess):
            data = self.process.readAll().data().decode("utf-8", errors="replace")
            self.output_received.emit(data)

    def _on_finished(self, exit_code: int):
        """Chiamato quando il processo finisce"""
        self.finished_signal.emit(exit_code)

    def stop(self):
        """Termina il processo in esecuzione"""
        if self.process:
            if isinstance(self.process, QProcess):
                if self.process.state() == QProcess.ProcessState.Running:
                    self.process.kill()
            elif isinstance(self.process, subprocess.Popen):
                self.process.kill()
                self.process.wait()


class DeveloperToolboxGUI(QMainWindow):
    """Finestra principale del Developer Toolbox"""

    def __init__(self):
        super().__init__()
        self.current_runner: CommandRunner | None = None
        self.init_ui()

    def init_ui(self):
        """Inizializza l'interfaccia utente"""
        self.setWindowTitle("SyncroJob - Developer Toolbox (Apex Edition)")
        self.setGeometry(100, 100, 1400, 900)

        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principale
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Pannello sinistro: comandi con scroll
        commands_scroll = QScrollArea()
        commands_scroll.setWidgetResizable(True)
        commands_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        commands_widget = QWidget()
        commands_layout = QVBoxLayout()
        commands_widget.setLayout(commands_layout)
        commands_scroll.setWidget(commands_widget)
        main_layout.addWidget(commands_scroll, stretch=1)

        # Pannello destro: output
        output_layout = QVBoxLayout()
        main_layout.addLayout(output_layout, stretch=2)

        # === SEZIONI COMANDI ===

        # 0. SYSTEM BOOTSTRAP
        bootstrap_group = self._create_group(
            "SYSTEM BOOTSTRAP AND SETUP",
            [
                (
                    "Init System",
                    self._init_system,
                    "Installa/Aggiorna librerie (Poetry)",
                ),
            ],
        )
        commands_layout.addWidget(bootstrap_group)

        # A. QUALITY AND SECURITY ENGINE
        quality_group = self._create_group(
            "QUALITY AND SECURITY ENGINE",
            [
                (
                    "Full Audit",
                    self._full_audit,
                    "Analisi totale: Sicurezza, Tipi, Stile e Test",
                ),
                ("Fast Audit", self._fast_audit, "Check completo saltando i test"),
                (
                    "Smart Check",
                    self._smart_check,
                    "Analisi incrementale (solo file modificati)",
                ),
                ("Only Tests", self._only_tests, "Esegue solo la suite unitaria"),
                (
                    "Auto-Fix",
                    self._auto_fix,
                    "Sistema automaticamente errori di stile Ruff",
                ),
                ("Dashboard", self._dashboard, "Apre il report HTML dell'ultimo Audit"),
            ],
        )
        commands_layout.addWidget(quality_group)

        # B. SECURITY AND ARCHITECTURE
        security_group = self._create_group(
            "SECURITY AND ARCHITECTURE",
            [
                (
                    "Security Scan",
                    self._security_scan,
                    "Pip-audit: Verifica vulnerabilità CVE",
                ),
                (
                    "Coverage",
                    self._coverage,
                    "Genera report HTML di copertura del codice",
                ),
                (
                    "Architecture",
                    self._architecture,
                    "Genera diagramma delle classi (PNG)",
                ),
            ],
        )
        commands_layout.addWidget(security_group)

        # C. DOCUMENTATION
        docs_group = self._create_group(
            "DOCUMENTATION AND KNOWLEDGE",
            [
                ("Build Docs", self._build_docs, "Compila documentazione MkDocs"),
                ("Serve Docs", self._serve_docs, "Avvia server live per i manuali"),
            ],
        )
        commands_layout.addWidget(docs_group)

        # D. CI/CD, RELEASE AND DEPLOY
        cicd_group = self._create_group(
            "CI/CD, RELEASE AND DEPLOY",
            [
                (
                    "Commit Wizard",
                    self._commit_wizard,
                    "Guida al commit (Conventional Commits)",
                ),
                (
                    "Version Bump",
                    self._version_bump,
                    "Incrementa versione e genera Changelog",
                ),
                ("Full Release", self._full_release, "Build EXE totale (con test)"),
                ("Fast Release", self._fast_release, "Build EXE rapida (salta test)"),
                ("Full Deploy", self._full_deploy, "Release + Caricamento su server"),
            ],
        )
        commands_layout.addWidget(cicd_group)

        # E. ENTERPRISE POWER TOOLS
        power_group = self._create_group(
            "ENTERPRISE POWER TOOLS",
            [
                (
                    "Secrets Mgmt",
                    self._secrets_mgmt,
                    "Gestore grafico chiavi e credenziali",
                ),
                ("Performance", self._performance, "Profiling profondo (cProfile)"),
                (
                    "DB Maintain",
                    self._db_maintain,
                    "Ottimizzazione e Integrity Check SQLite",
                ),
                (
                    "Raw Metrics",
                    self._raw_metrics,
                    "Complessità ciclomatica e indici tecnici",
                ),
                (
                    "Clean Code",
                    self._clean_code,
                    "Rimuove codice commentato e dead code",
                ),
                ("Depty Check", self._depty_check, "Verifica dipendenze inutilizzate"),
                ("Project Stats", self._project_stats, "Statistiche linee di codice"),
                (
                    "Dep Audit",
                    self._dep_audit,
                    "Verifica isomorfismo dipendenze Sorgente/EXE",
                ),
            ],
        )
        commands_layout.addWidget(power_group)

        # F. SYSTEM AND RUN
        system_group = self._create_group(
            "SYSTEM AND RUN",
            [
                ("Run App (Dev)", self._run_app, "Avvia l'app in modalità Sviluppo"),
                (
                    "Clean Cache",
                    self._clean_cache,
                    "Pulisce .pyc, __pycache__ e temp files",
                ),
                ("Inspector", self._inspector, "Ispezione universale del sistema/log"),
            ],
        )
        commands_layout.addWidget(system_group)

        commands_layout.addStretch()

        # === OUTPUT CONSOLE ===
        output_label = QPushButton("Console Output")
        output_label.setEnabled(False)
        output_label.setStyleSheet(
            "QPushButton:disabled { background-color: #2c3e50; color: white; font-weight: bold; }"
        )
        output_layout.addWidget(output_label)

        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)
        self.output_console.setFont(QFont("Consolas", 9))
        self.output_console.setStyleSheet(
            """
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3e3e3e;
                padding: 10px;
            }
        """
        )
        output_layout.addWidget(self.output_console)

        # Pulsanti controllo console
        console_controls = QHBoxLayout()
        clear_btn = QPushButton("Clear Console")
        clear_btn.clicked.connect(self.output_console.clear)
        stop_btn = QPushButton("Stop Process")
        stop_btn.clicked.connect(self._stop_current_process)
        stop_btn.setStyleSheet("QPushButton { background-color: #c0392b; color: white; }")
        console_controls.addWidget(clear_btn)
        console_controls.addWidget(stop_btn)
        console_controls.addStretch()
        output_layout.addLayout(console_controls)

        # Messaggio iniziale
        self._log_output("=== SyncroJob Developer Toolbox ===\n")
        self._log_output("Seleziona un'operazione dal pannello sinistro.\n\n")

        # Gestione CLI args
        QTimer.singleShot(500, self._handle_cli_args)

    def _handle_cli_args(self):
        """Gestisce eventuali argomenti passati da riga di comando"""
        if len(sys.argv) < 2:
            return

        arg = " ".join(sys.argv[1:]).lower().replace("-", " ")
        if "fast release" in arg:
            self._fast_release()
        elif "full release" in arg:
            self._full_release()
        elif "fast audit" in arg:
            self._fast_audit()
        elif "full audit" in arg:
            self._full_audit()
        elif "smart check" in arg:
            self._smart_check()
        elif "deploy" in arg:
            self._full_deploy()

    def _create_group(self, title: str, buttons: list[tuple[str, Callable[[], None], str]]) -> QGroupBox:
        """Crea un gruppo di pulsanti con descrizioni"""
        group = QGroupBox(title)
        group.setStyleSheet(
            """
            QGroupBox {
                font-weight: bold;
                font-size: 11pt;
                border: 2px solid #34495e;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 10px;
                background-color: #34495e;
                color: white;
                border-radius: 3px;
            }
        """
        )
        layout = QVBoxLayout()
        layout.setSpacing(8)  # Più spazio tra i pulsanti

        for btn_text, callback, tooltip in buttons:
            # Container per pulsante + descrizione
            btn_container = QWidget()
            btn_layout = QVBoxLayout()
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.setSpacing(2)

            # Pulsante
            btn = QPushButton(f"▶ {btn_text}")
            btn.setToolTip(f"<b>{btn_text}</b><br>{tooltip}")
            btn.setMinimumHeight(40)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(callback)
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 10px 15px;
                    text-align: left;
                    font-weight: bold;
                    font-size: 10pt;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                    border: 1px solid #1abc9c;
                }
                QPushButton:pressed {
                    background-color: #21618c;
                }
            """
            )

            # Etichetta descrittiva sotto il pulsante
            desc_label = QLabel(f"   {tooltip}")
            desc_label.setStyleSheet(
                """
                QLabel {
                    color: #7f8c8d;
                    font-size: 8pt;
                    font-style: italic;
                    padding-left: 5px;
                }
            """
            )
            desc_label.setWordWrap(True)

            btn_layout.addWidget(btn)
            btn_layout.addWidget(desc_label)
            btn_container.setLayout(btn_layout)

            layout.addWidget(btn_container)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def _run_command(self, command: list[str], label: str, shell: bool = False):
        """Esegue un comando in un thread separato"""
        self._log_output(f"\n{'=' * 60}\n")
        self._log_output(f"[INFO] Avvio: {label}\n")
        self._log_output(f"[CMD] {' '.join(command)}\n")
        self._log_output(f"{'=' * 60}\n\n")

        self.current_runner = CommandRunner(command, shell=shell)
        self.current_runner.output_received.connect(self._log_output)
        self.current_runner.finished_signal.connect(self._on_command_finished)
        self.current_runner.start()

    def _log_output(self, text: str):
        """Aggiunge testo alla console di output"""
        self.output_console.moveCursor(QTextCursor.MoveOperation.End)
        self.output_console.insertPlainText(text)
        self.output_console.moveCursor(QTextCursor.MoveOperation.End)

    def _on_command_finished(self, exit_code: int):
        """Chiamato quando un comando finisce"""
        status = "SUCCESS" if exit_code == 0 else f"FAILED (exit code: {exit_code})"
        self._log_output(f"\n[{status}] Operazione completata.\n")
        self.current_runner = None

    def _stop_current_process(self):
        """Termina il processo corrente"""
        if self.current_runner:
            self._log_output("\n[WARNING] Interruzione processo...\n")
            self.current_runner.stop()
            self.current_runner = None

    # === COMANDI ===

    def _init_system(self):
        """Opzione 0: Init System"""
        self._run_command(["poetry", "install"], "Init System (Poetry Install)")

    def _full_audit(self):
        """Opzione 1: Full Audit"""
        self._run_command([str(VENV_PYTHON), "admin/pre_flight_check.py"], "Full Audit")

    def _fast_audit(self):
        """Opzione 2: Fast Audit"""
        self._run_command([str(VENV_PYTHON), "admin/pre_flight_check.py", "--fast"], "Fast Audit")

    def _smart_check(self):
        """Opzione 3: Smart Check"""
        self._run_command(
            [str(VENV_PYTHON), "admin/pre_flight_check.py", "--fast", "--inc"],
            "Smart Check (Incremental)",
        )

    def _only_tests(self):
        """Opzione 4: Only Tests"""
        self._run_command([str(VENV_PYTHON), "admin/pre_flight_check.py", "--test-only"], "Only Tests")

    def _auto_fix(self):
        """Opzione 5: Auto-Fix"""
        self._run_command(
            [str(VENV_PYTHON), "admin/pre_flight_check.py", "--fix", "--fast"],
            "Auto-Fix (Ruff)",
        )

    def _dashboard(self):
        """Opzione 6: Dashboard"""
        dashboard_path = PROJECT_ROOT / "reports" / "preflight" / "dashboard.html"
        if dashboard_path.exists():
            self._log_output(f"\n[INFO] Apertura dashboard: {dashboard_path}\n")
            webbrowser.open(str(dashboard_path))
        else:
            self._log_output(f"\n[ERROR] Dashboard non trovata: {dashboard_path}\n")

    def _security_scan(self):
        """Opzione 7: Security Scan"""
        self._run_command(
            [str(VENV_PYTHON), "admin/pre_flight_check.py", "--target", "security"],
            "Security Scan",
        )

    def _coverage(self):
        """Opzione 8: Coverage"""
        self._run_command(
            [str(VENV_BIN / "pytest"), "--cov=src", "--cov-report=html"],
            "Code Coverage",
        )

    def _architecture(self):
        """Opzione 9: Architecture"""
        self._run_command(
            [str(VENV_PYTHON), "docs/generate_architecture.py"],
            "Generate Architecture Diagram",
        )

    def _build_docs(self):
        """Opzione 10: Build Docs"""
        self._run_command([str(VENV_BIN / "mkdocs"), "build"], "Build MkDocs")

    def _serve_docs(self):
        """Opzione 11: Serve Docs"""
        self._log_output("\n[INFO] Avvio server MkDocs...\n")
        self._log_output("[INFO] Premi 'Stop Process' per terminare il server.\n\n")
        self._run_command([str(VENV_BIN / "mkdocs"), "serve"], "Serve MkDocs")

    def _commit_wizard(self):
        """Opzione 12: Commit Wizard"""
        self._run_command([str(VENV_BIN / "cz"), "commit"], "Commit Wizard")

    def _version_bump(self):
        """Opzione 13: Version Bump"""
        self._run_command([str(VENV_BIN / "cz"), "bump", "--changelog"], "Version Bump")

    def _full_release(self):
        """Opzione 14: Full Release"""
        self._run_command([str(VENV_PYTHON), "admin/release.py", "auto"], "Full Release")

    def _fast_release(self):
        """Opzione 15: Fast Release"""
        self._run_command(
            [str(VENV_PYTHON), "admin/release.py", "auto", "--skip-tests"],
            "Fast Release",
        )

    def _full_deploy(self):
        """Opzione 16: Full Deploy"""
        self._run_command([str(VENV_PYTHON), "admin/release.py", "auto", "--deploy"], "Full Deploy")

    def _secrets_mgmt(self):
        """Opzione 17: Secrets Management"""
        self._run_command([str(VENV_PYTHON), "admin/manage_secrets_gui.py"], "Secrets Management GUI")

    def _performance(self):
        """Opzione 18: Performance Profiling"""
        self._run_command(
            [
                str(VENV_PYTHON),
                "-m",
                "cProfile",
                "-o",
                "profiling_report.prof",
                "main.py",
            ],
            "Performance Profiling (cProfile)",
        )

    def _db_maintain(self):
        """Opzione 19: DB Maintenance"""
        self._run_command([str(VENV_PYTHON), "admin/db_maintenance.py"], "Database Maintenance")

    def _raw_metrics(self):
        """Opzione 20: Raw Metrics"""
        self._run_command(
            [str(VENV_PYTHON), "admin/pre_flight_check.py", "--target", "metrics"],
            "Raw Metrics",
        )

    def _clean_code(self):
        """Opzione 21: Clean Code"""
        self._run_command(
            [str(VENV_PYTHON), "admin/pre_flight_check.py", "--target", "clean"],
            "Clean Code",
        )

    def _depty_check(self):
        """Opzione 22: Dependency Check"""
        self._run_command(
            [str(VENV_PYTHON), "admin/pre_flight_check.py", "--target", "deps"],
            "Dependency Check",
        )

    def _project_stats(self):
        """Opzione 23: Project Stats"""
        self._run_command(
            [str(VENV_PYTHON), "admin/pre_flight_check.py", "--target", "stats"],
            "Project Stats",
        )

    def _run_app(self):
        """Opzione 24: Run App (Dev)"""
        self._run_command([str(VENV_PYTHON), "main.py"], "Run App (Development Mode)")

    def _clean_cache(self):
        """Opzione 25: Clean Cache"""
        self._run_command([str(VENV_PYTHON), "admin/clean_venv.py"], "Clean Cache")

    def _inspector(self):
        """Opzione 26: Inspector"""
        self._run_command([str(VENV_PYTHON), "admin/universal_inspector.py"], "Universal Inspector")

    def _dep_audit(self):
        """Opzione 27: Dependency Audit"""
        self._run_command([str(VENV_PYTHON), "admin/analyze_dependencies.py"], "Dependency Audit")


def main():
    """Entry point"""
    app = QApplication(sys.argv)

    # Stile applicazione
    app.setStyle("Fusion")

    window = DeveloperToolboxGUI()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
