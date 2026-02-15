import argparse
import contextlib
import datetime
import io
import json
import signal
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

# --- AGGIUNTA SYS PATH PER ENTERPRISE LOGGING ---
ROOT_DIR = Path(__file__).parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from src.core.logging import get_logger, with_context

    HAS_ENTERPRISE_LOGGING = True
except ImportError:
    HAS_ENTERPRISE_LOGGING = False
# ------------------------------------------------

# Fix encoding for Windows console to support emoji
if sys.platform == "win32":
    with contextlib.suppress(Exception):
        if hasattr(sys.stdout, "buffer"):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        if hasattr(sys.stderr, "buffer"):
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# --- CONFIGURAZIONE ---
STATE_FILE = Path(__file__).parent / ".test_session_state.json"
REPORT_FILE = Path(__file__).parent / "test_report.md"
DEFAULT_TIMEOUT = 60  # Secondi per file prima di considerare timeout
# ----------------------


class Console:
    """Helper per output colorato senza dipendenze esterne."""

    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @staticmethod
    def print(msg, color=ENDC, end="\n"):
        print(f"{color}{msg}{Console.ENDC}", end=end, flush=True)

    @staticmethod
    def info(msg):
        Console.print(f"i  {msg}", Console.CYAN)

    @staticmethod
    def success(msg):
        Console.print(f"v {msg}", Console.GREEN)

    @staticmethod
    def warning(msg):
        Console.print(f"!  {msg}", Console.WARNING)

    @staticmethod
    def error(msg):
        Console.print(f"x {msg}", Console.FAIL)

    @staticmethod
    def header(msg):
        Console.print(f"\n{Console.BOLD}{msg}{Console.ENDC}", Console.HEADER)


class TestRunner:
    def __init__(self):
        self.total_tests = 0
        self.files_map = defaultdict(list)
        self.failed_tests = []
        self.passed_tests = 0
        self.skipped_tests = 0
        self.start_time = 0
        self.queue_files = []
        self.interrupted = False

        # Inizializzazione Logger Enterprise
        if HAS_ENTERPRISE_LOGGING:
            self.logger = get_logger("test_runner")
        else:
            self.logger = None

        # Gestione Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        if not self.interrupted:
            self.interrupted = True
            Console.warning("\n\n! Interrupt ricevuto! Salvataggio stato e chiusura in corso...")
            self.save_state()
            sys.exit(130)

    def load_state(self):
        if STATE_FILE.exists():
            try:
                return json.loads(STATE_FILE.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                return None
        return None

    def save_state(self):
        state = {
            "queue": self.queue_files,
            "failed": self.failed_tests,
            "passed": self.passed_tests,
            "skipped": self.skipped_tests,
            "total_files_map": dict(self.files_map),
            "timestamp": time.time(),
        }
        with contextlib.suppress(Exception):
            STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")

    def discover_tests(self, targets=None):
        Console.info("🔍 Rilevamento test in corso (pytest --collect-only)...")

        if targets is None:
            targets = ["tests"]

        cmd = [sys.executable, "-m", "pytest", "--collect-only", "-qq"]
        if targets:
            if isinstance(targets, list):
                cmd.extend(targets)
            else:
                cmd.append(targets)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=ROOT_DIR,
                check=False,
            )
        except Exception as e:
            Console.error(f"Errore critico discovery: {e}")
            sys.exit(1)

        files_map = defaultdict(list)

        for line in result.stdout.splitlines():
            line = line.strip()
            # Un NodeID valido di pytest contiene '::'
            if "::" in line:
                # Se la riga contiene spazi (es. descrizioni), prendiamo solo il NodeID
                node_id = line.split()[0] if " " in line else line
                if "::" in node_id:
                    # Rimuoviamo eventuali tag tipo <Module, <Class se presenti nel NodeID
                    node_id = (
                        node_id.replace("<Module ", "")
                        .replace("<Class ", "")
                        .replace("<Function ", "")
                        .replace(">", "")
                        .strip()
                    )
                    file_path = node_id.split("::")[0]
                    files_map[file_path].append(node_id)

        if not files_map:
            if result.stderr:
                print(result.stderr)
            Console.error("Nessun test trovato!")
            sys.exit(1)

        return files_map

    def run_process(self, target, isolate=False, timeout=None):
        # Aggiungiamo --cov=src --cov-append per accumulare la copertura
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            target,
            "--no-header",
            "--quiet",
            "--tb=short",
            "--cov=src",
            "--cov-append",
        ]

        start = time.time()
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=ROOT_DIR,
                timeout=timeout,
                check=False,
            )
            duration = time.time() - start
            return result, duration, False  # False = No Timeout
        except subprocess.TimeoutExpired:
            duration = time.time() - start
            return None, duration, True  # True = Timeout

    def generate_report(self):
        """Genera un report Markdown dettagliato."""
        total_duration = time.time() - self.start_time

        try:
            with REPORT_FILE.open("w", encoding="utf-8") as f:
                f.write("# 📊 Test Execution Report\n\n")
                f.write(f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Duration:** {total_duration:.2f}s\n\n")

                f.write("## Summary\n")
                f.write("| Metric | Count |\n")
                f.write("|---|---|\n")
                f.write(f"| 🧪 Total | {self.total_tests} |\n")
                f.write(f"| ✅ Passed | {self.passed_tests} |\n")
                f.write(f"| ❌ Failed | {len(self.failed_tests)} |\n")
                f.write(f"| ⏩ Skipped | {self.skipped_tests} |\n\n")

                if self.failed_tests:
                    f.write("## ❌ Failures Details\n")
                    for item in self.failed_tests:
                        if isinstance(item, dict):
                            f.write(f"### `{item.get('id', 'Unknown')}`\n")
                            f.write(f"**Error:** `{item.get('error', 'Unknown')}`\n\n")
                            f.write(f"**Timestamp:** `{item.get('timestamp', 'N/A')}`\n\n")
                            f.write("<details><summary>Full Output</summary>\n\n")
                            f.write("```text\n")
                            f.write(item.get("full_output", "No output captured"))
                            f.write("\n```\n")
                            f.write("</details>\n\n")
                        else:
                            f.write(f"### `{item}`\n")
                            f.write("**Error:** `Dettagli non disponibili (ripreso da stato precedente)`\n\n")
                        f.write("---\n")
                else:
                    f.write("## ✅ All Tests Passed!\n")
                    f.write("Great job! No issues found.\n")

            Console.info(f"📄 Report salvato in: {REPORT_FILE}")
        except Exception as e:
            Console.error(f"Errore generazione report: {e}")

    def show_coverage(self):
        """Mostra il report di copertura totale in modo rapido."""
        Console.header("📊 REPORT COPERTURA")

        # 1. Tenta di mostrare dati esistenti
        with contextlib.suppress(Exception):
            res = subprocess.run(
                [sys.executable, "-m", "coverage", "report", "-m"], cwd=ROOT_DIR, check=False
            )
            if res.returncode == 0:
                return

        # 2. Se non ci sono dati, calcola
        Console.info("Dati non trovati. Calcolo in corso (attendere)...")
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            "--cov=src",
            "--cov-report=term-missing",
            "-q",
            "--no-summary",
        ]
        with contextlib.suppress(Exception):
            subprocess.run(cmd, cwd=ROOT_DIR, check=False)

    def run(self):
        parser = argparse.ArgumentParser(description="🛡️ Robust Test Runner")
        parser.add_argument("targets", nargs="*", help="File o directory di test specifici da eseguire.")
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Ricomincia da zero ignorando lo stato precedente.",
        )
        parser.add_argument(
            "--filter",
            type=str,
            help="Esegui solo test in questo path (es. tests/unit).",
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=DEFAULT_TIMEOUT,
            help="Timeout in secondi per file.",
        )
        parser.add_argument(
            "--retry",
            type=int,
            default=0,
            help="Numero di retry per test falliti (per flaky tests).",
        )
        parser.add_argument(
            "--coverage-only",
            action="store_true",
            help="Calcola e mostra solo la copertura totale.",
        )
        parser.add_argument(
            "-x",
            "--exitfirst",
            action="store_true",
            help="Ferma l'esecuzione al primo fallimento.",
        )
        args = parser.parse_args()
        self.exitfirst = args.exitfirst

        if args.coverage_only:
            self.show_coverage()
            return

        Console.header("🛡️  ROBUST TEST RUNNER AVVIATO")

        if self.logger:
            self.logger.info("Robust test runner session started")

        # 1. Caricamento Stato o Inizio
        state = self.load_state()

        # Determina i target: preferenza ad argomenti posizionali, poi --filter
        targets = args.targets if args.targets else args.filter

        should_reset = args.reset or state is None or targets

        if should_reset:
            # Pulizia dati copertura precedenti su reset
            with contextlib.suppress(Exception):
                subprocess.run([sys.executable, "-m", "coverage", "erase"], cwd=ROOT_DIR, check=False)

            self.files_map = self.discover_tests(targets)
            self.total_tests = sum(len(ids) for ids in self.files_map.values())
            self.queue_files = sorted(self.files_map.keys())
            Console.info(f"Nuova sessione: {self.total_tests} test in {len(self.files_map)} file.")
            if STATE_FILE.exists():
                STATE_FILE.unlink()
        else:
            # Mostra copertura precedente se esiste
            with contextlib.suppress(Exception):
                Console.info("📊 Copertura precedente:")
                subprocess.run(
                    [sys.executable, "-m", "coverage", "report", "--format=text"], cwd=ROOT_DIR, check=False
                )

            self.files_map = defaultdict(list, state.get("total_files_map", {}))
            self.queue_files = state.get("queue", [])
            self.failed_tests = state.get("failed", [])
            self.passed_tests = state.get("passed", 0)
            self.skipped_tests = state.get("skipped", 0)

            # Ricalcola totale se la mappa esiste, altrimenti rifà discovery
            if not self.files_map:
                self.files_map = self.discover_tests()

            self.total_tests = sum(len(ids) for ids in self.files_map.values())
            Console.warning(f"Ripresa sessione: {len(self.queue_files)} file rimanenti.")

        self.start_time = time.time()

        # 2. Execution Loop
        while self.queue_files:
            current_file = self.queue_files[0]
            node_ids = self.files_map.get(current_file, [])

            if not node_ids:
                self.queue_files.pop(0)
                continue

            test_count = len(node_ids)
            progress_pct = (
                ((self.passed_tests + len(self.failed_tests)) / self.total_tests) * 100
                if self.total_tests > 0
                else 0
            )

            print(f"\n📂 File: {Console.BOLD}{current_file}{Console.ENDC} ({test_count} tests)")
            print(
                f"   📊 Progress: {progress_pct:.1f}% | Passed: {self.passed_tests} | Failed: {len(self.failed_tests)}"
            )

            # Tentativo esecuzione veloce (Intero File)
            res, dur, is_timeout = self.run_process(current_file, timeout=args.timeout)

            if not is_timeout and res.returncode == 0:
                Console.success(f"PASS ({dur:.2f}s)")
                self.passed_tests += test_count
                self.queue_files.pop(0)
                self.save_state()
            else:
                reason = "TIMEOUT" if is_timeout else "FAIL"
                Console.warning(f"{reason} ({dur:.2f}s) -> Attivazione ISOLATION MODE")

                # Fallback: Esecuzione Isolata
                self.run_isolated_tests(node_ids, retry_count=args.retry)
                self.queue_files.pop(0)
                self.save_state()

        self.finish()

    def run_isolated_tests(self, node_ids, retry_count=0):
        """Esegue i test uno alla volta per isolare i fallimenti."""
        for nid in node_ids:
            if self.interrupted:
                break

            print(f"    👉 {nid.split('::')[-1]} ... ", end="", flush=True)
            success, res = self._execute_test_with_retries(nid, retry_count)

            if success:
                Console.print("PASS", Console.GREEN)
                self.passed_tests += 1
            else:
                self._handle_isolated_failure(nid, res)

    def _execute_test_with_retries(self, nid, retry_count):
        """Tenta l'esecuzione di un test singolo con logica di retry."""
        success = False
        res = None
        for attempt in range(retry_count + 1):
            res, _dur, is_timeout = self.run_process(nid, isolate=True, timeout=60)
            if not is_timeout and res.returncode == 0:
                success = True
                break
            if attempt < retry_count:
                print(f"{Console.WARNING}RETRY{Console.ENDC} ... ", end="", flush=True)
        return success, res

    def _handle_isolated_failure(self, nid, res):
        """Gestisce il fallimento finale di un test isolato."""
        Console.print("FAIL", Console.FAIL)
        error_msg = "Timeout"
        full_log = "Execution Timed Out"

        if res:
            full_log = res.stdout + res.stderr
            error_msg = self._extract_error_message(res.stdout.splitlines())

        # Logging Enterprise con contesto
        if self.logger:
            with with_context(test_id=nid, phase="execution"):
                self.logger.error(
                    "Test failed during robust execution",
                    error=error_msg,
                    file=nid.split("::")[0],
                )

        self.failed_tests.append(
            {
                "id": nid,
                "error": error_msg,
                "log": full_log,
                "full_output": full_log,
                "timestamp": datetime.datetime.now().isoformat(),
            }
        )

        # Salvataggio immediato e generazione report ad ogni fail
        self.save_state()
        self.generate_report()

        # Interruzione immediata ad ogni fallimento come richiesto
        Console.error(f"\n🛑 Test Fallito: {nid}")
        Console.error(
            "Interruzione automatica per permettere la correzione. Il prossimo avvio riprenderà da questo file."
        )
        sys.exit(1)

    def _extract_error_message(self, lines):
        """Estrae un messaggio di errore significativo dalle ultime righe del log."""
        for line in lines[-15:]:
            if any(x in line for x in ["E ", "Error:", "FAILED"]):
                return line.strip()
        return "Unknown Error"

    def finish(self):
        total_time = time.time() - self.start_time
        Console.header("🏁 ESECUZIONE COMPLETATA")

        # Tabella di riepilogo ANSI
        print("\n┌──────────────────────────────────────┬────────────┐")
        print(
            f"│ {Console.BOLD}Metric{Console.ENDC}                               │ {Console.BOLD}Value{Console.ENDC}      │"
        )
        print("├──────────────────────────────────────┼────────────┤")
        print(f"│ 🧪 Total Tests                       │ {self.total_tests:<10} │")
        print(
            f"│ ✅ Passed                            │ {Console.GREEN}{self.passed_tests:<10}{Console.ENDC} │"
        )
        print(
            f"│ ❌ Failed                            │ {Console.FAIL}{len(self.failed_tests):<10}{Console.ENDC} │"
        )
        print(
            f"│ ⏩ Skipped                           │ {Console.WARNING}{self.skipped_tests:<10}{Console.ENDC} │"
        )
        print(f"│ ⏱️  Total Duration                    │ {f'{total_time:.2f}s':<10} │")
        print("└──────────────────────────────────────┴────────────┘\n")

        # Mostra Report Copertura Finale
        Console.header("📊 COPERTURA FINALE")
        with contextlib.suppress(Exception):
            subprocess.run([sys.executable, "-m", "coverage", "report", "-m"], cwd=ROOT_DIR, check=False)
            subprocess.run(
                [sys.executable, "-m", "coverage", "xml"], cwd=ROOT_DIR, check=False
            )  # Genera XML per CI
            subprocess.run(
                [sys.executable, "-m", "coverage", "html"], cwd=ROOT_DIR, check=False
            )  # Genera anche HTML
            Console.info("Report HTML generato in htmlcov/index.html")

        if self.failed_tests:
            print(f"❌ Falliti: {len(self.failed_tests)}")
            Console.warning(f"! Vedi {REPORT_FILE} per i dettagli completi.")
            self.generate_report()
            if self.logger:
                self.logger.warning("Test session finished with failures", count=len(self.failed_tests))
            sys.exit(1)
        else:
            Console.success("Tutti i test passati!")
            self.generate_report()
            if self.logger:
                self.logger.info("Test session finished successfully")
            if STATE_FILE.exists():
                STATE_FILE.unlink()
            sys.exit(0)


if __name__ == "__main__":
    runner = TestRunner()
    runner.run()
