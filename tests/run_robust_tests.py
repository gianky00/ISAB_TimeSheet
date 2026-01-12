import argparse
import datetime
import json
import os
import signal
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

# --- CONFIGURAZIONE ---
ROOT_DIR = Path(__file__).parent.parent
STATE_FILE = Path(__file__).parent / ".test_session_state.json"
REPORT_FILE = Path(__file__).parent / "test_report.md"
DEFAULT_TIMEOUT = 60  # Secondi per file prima di considerare timeout
# ----------------------

class Console:
    """Helper per output colorato senza dipendenze esterne."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def print(msg, color=ENDC, end="\n"):
        print(f"{color}{msg}{Console.ENDC}", end=end, flush=True)

    @staticmethod
    def info(msg): Console.print(f"ℹ️  {msg}", Console.CYAN)

    @staticmethod
    def success(msg): Console.print(f"✅ {msg}", Console.GREEN)

    @staticmethod
    def warning(msg): Console.print(f"⚠️  {msg}", Console.WARNING)

    @staticmethod
    def error(msg): Console.print(f"❌ {msg}", Console.FAIL)

    @staticmethod
    def header(msg): Console.print(f"\n{Console.BOLD}{msg}{Console.ENDC}", Console.HEADER)

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

        # Gestione Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        if not self.interrupted:
            self.interrupted = True
            Console.warning("\n\n🛑 Interrupt ricevuto! Salvataggio stato e chiusura in corso...")
            self.save_state()
            sys.exit(130)

    def load_state(self):
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return None
        return None

    def save_state(self):
        state = {
            "queue": self.queue_files,
            "failed": self.failed_tests,
            "passed": self.passed_tests,
            "skipped": self.skipped_tests,
            "total_files_map": dict(self.files_map),
            "timestamp": time.time()
        }
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)

    def discover_tests(self, targets=None):
        Console.info("🔍 Rilevamento test in corso (pytest --collect-only)...")

        cmd = [sys.executable, "-m", "pytest", "--collect-only", "-q"]
        if targets:
            if isinstance(targets, list):
                cmd.extend(targets)
            else:
                cmd.append(targets)

        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=ROOT_DIR
            )
        except Exception as e:
            Console.error(f"Errore critico discovery: {e}")
            sys.exit(1)

        files_map = defaultdict(list)
        for line in result.stdout.splitlines():
            line = line.strip()
            if "::" in line and "error" not in line.lower():
                file_path = line.split("::")[0]
                files_map[file_path].append(line)

        if not files_map:
            if result.stderr:
                print(result.stderr)
            Console.error("Nessun test trovato!")
            sys.exit(1)

        return files_map

    def run_process(self, target, isolate=False, timeout=None):
        # Aggiungiamo --cov=src --cov-append per accumulare la copertura
        cmd = [sys.executable, "-m", "pytest", target, "--no-header", "--quiet", "--tb=short", "--cov=src", "--cov-append"]

        start = time.time()
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=ROOT_DIR,
                timeout=timeout
            )
            duration = time.time() - start
            return result, duration, False # False = No Timeout
        except subprocess.TimeoutExpired:
            duration = time.time() - start
            return None, duration, True # True = Timeout

    def generate_report(self):
        """Genera un report Markdown dettagliato."""
        total_duration = time.time() - self.start_time

        with open(REPORT_FILE, "w", encoding="utf-8") as f:
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
                    f.write(f"### `{item['id']}`\n")
                    f.write(f"**Error:** `{item.get('error', 'Unknown')}`\n\n")
                    f.write("<details><summary>Full Output</summary>\n\n")
                    f.write("```text\n")
                    f.write(item.get("full_output", "No output captured"))
                    f.write("\n```\n")
                    f.write("</details>\n\n")
                    f.write("---\n")
            else:
                f.write("## ✅ All Tests Passed!\n")
                f.write("Great job! No issues found.\n")

        Console.info(f"📄 Report salvato in: {REPORT_FILE}")

    def show_coverage(self):
        """Mostra il report di copertura totale in modo rapido."""
        Console.header("📊 REPORT COPERTURA")

        # 1. Tenta di mostrare dati esistenti
        try:
            res = subprocess.run([sys.executable, "-m", "coverage", "report", "-m"],
                                 cwd=ROOT_DIR)
            if res.returncode == 0:
                return
        except Exception:
            pass

        # 2. Se non ci sono dati, calcola
        Console.info("Dati non trovati. Calcolo in corso (attendere)...")
        cmd = [sys.executable, "-m", "pytest", "--cov=src", "--cov-report=term-missing", "-q", "--no-summary"]
        try:
            subprocess.run(cmd, cwd=ROOT_DIR)
        except Exception as e:
            Console.error(f"Errore calcolo copertura: {e}")

    def run(self):
        parser = argparse.ArgumentParser(description="🛡️ Robust Test Runner")
        parser.add_argument("targets", nargs="*", help="File o directory di test specifici da eseguire.")
        parser.add_argument("--reset", action="store_true", help="Ricomincia da zero ignorando lo stato precedente.")
        parser.add_argument("--filter", type=str, help="Esegui solo test in questo path (es. tests/unit).")
        parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Timeout in secondi per file.")
        parser.add_argument("--retry", type=int, default=0, help="Numero di retry per test falliti (per flaky tests).")
        parser.add_argument("--coverage-only", action="store_true", help="Calcola e mostra solo la copertura totale.")
        parser.add_argument("-x", "--exitfirst", action="store_true", help="Ferma l'esecuzione al primo fallimento.")
        args = parser.parse_args()
        self.exitfirst = args.exitfirst

        if args.coverage_only:
            self.show_coverage()
            return

        Console.header("🛡️  ROBUST TEST RUNNER AVVIATO")

        # 1. Caricamento Stato o Inizio
        state = self.load_state()

        # Determina i target: preferenza ad argomenti posizionali, poi --filter
        targets = args.targets if args.targets else args.filter

        should_reset = args.reset or state is None or targets

        if should_reset:
            # Pulizia dati copertura precedenti su reset
            try:
                subprocess.run([sys.executable, "-m", "coverage", "erase"], cwd=ROOT_DIR)
            except Exception:
                pass

            self.files_map = self.discover_tests(targets)
            self.total_tests = sum(len(ids) for ids in self.files_map.values())
            self.queue_files = sorted(list(self.files_map.keys()))
            Console.info(f"Nuova sessione: {self.total_tests} test in {len(self.files_map)} file.")
            if STATE_FILE.exists():
                os.remove(STATE_FILE)
        else:
            # Mostra copertura precedente se esiste
            try:
                Console.info("📊 Copertura precedente:")
                subprocess.run([sys.executable, "-m", "coverage", "report", "--format=text"], cwd=ROOT_DIR)
            except Exception:
                pass

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
        processed_files = 0
        total_files_count = len(self.queue_files) # Aprossimativo se ripreso

        while self.queue_files:
            current_file = self.queue_files[0]
            node_ids = self.files_map.get(current_file, [])

            if not node_ids:
                self.queue_files.pop(0)
                continue

            test_count = len(node_ids)
            progress_pct = ((self.passed_tests + len(self.failed_tests)) / self.total_tests) * 100

            print(f"\n📂 File: {Console.BOLD}{current_file}{Console.ENDC} ({test_count} tests)")
            print(f"   📊 Progress: {progress_pct:.1f}% | Passed: {self.passed_tests} | Failed: {len(self.failed_tests)}")

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
        for nid in node_ids:
            if self.interrupted: break

            print(f"    👉 {nid.split('::')[-1]} ... ", end="", flush=True)

            success = False
            # Tentativi (Retry Logic)
            for attempt in range(retry_count + 1):
                res, dur, is_timeout = self.run_process(nid, isolate=True, timeout=30)

                if not is_timeout and res.returncode == 0:
                    success = True
                    break
                else:
                     if attempt < retry_count:
                         print(f"{Console.WARNING}RETRY{Console.ENDC} ... ", end="", flush=True)

            if success:
                Console.print("PASS", Console.GREEN)
                self.passed_tests += 1
            else:
                Console.print("FAIL", Console.FAIL)

                error_msg = "Timeout"
                full_log = "Execution Timed Out"

                if res:
                    lines = res.stdout.splitlines()
                    full_log = res.stdout + res.stderr
                    # Euristiche parsing errore
                    for line in lines[-15:]:
                        if any(x in line for x in ["E ", "Error:", "FAILED"]):
                            error_msg = line.strip()
                            break

                self.failed_tests.append({
                    "id": nid,
                    "error": error_msg,
                    "full_output": full_log
                })

                if getattr(self, "exitfirst", False):
                    Console.error("\n⛔ EXITFIRST: Test fallito. Interruzione immediata.")
                    self.save_state()
                    self.generate_report()
                    sys.exit(1)

    def finish(self):
        total_time = time.time() - self.start_time
        Console.header("🏁 ESECUZIONE COMPLETATA")
        print(f"⏱️  Tempo Totale: {total_time:.2f}s")
        print(f"✅ Passati: {self.passed_tests}")

        # Mostra Report Copertura Finale
        Console.header("📊 COPERTURA FINALE")
        try:
            subprocess.run([sys.executable, "-m", "coverage", "report", "-m"], cwd=ROOT_DIR)
            subprocess.run([sys.executable, "-m", "coverage", "html"], cwd=ROOT_DIR) # Genera anche HTML
            Console.info("Report HTML generato in htmlcov/index.html")
        except Exception as e:
            Console.error(f"Impossibile generare report copertura: {e}")

        if self.failed_tests:
            print(f"❌ Falliti: {len(self.failed_tests)}")
            Console.warning(f"⚠️  Vedi {REPORT_FILE} per i dettagli completi.")
            self.generate_report()
            # Non cancelliamo lo stato se ci sono fallimenti, per permettere re-run o debug
            sys.exit(1)
        else:
            Console.success("Tutti i test passati!")
            self.generate_report()
            if STATE_FILE.exists():
                os.remove(STATE_FILE)
            sys.exit(0)

if __name__ == "__main__":
    runner = TestRunner()
    runner.run()
