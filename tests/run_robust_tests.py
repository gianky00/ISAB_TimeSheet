"""
SyncroJob Enterprise - Ultra Test Runner V5.2 (The Apex Runner)
================================================================
Sistema ibrido di orchestrazione test, ottimizzato per consumo IA.

Modalita':
- --ai        : Output JSON strutturato per agenti IA (file + stdout).
- -x          : Fail-Fast aggressivo (si ferma al primo errore).
- SNIPER      : ≤5 target → esecuzione live diretta (debug, PDB).
- SHOTGUN     : >5 target o nessuno → parallelo su tutti i core.
- --retry N   : Riesecuzione automatica test falliti (flaky).
- --cov       : Coverage opt-in.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime
import json
import multiprocessing
import os
import re
import subprocess
import sys
import tempfile
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from concurrent.futures.process import BrokenProcessPool
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Final

# --- SYS PATH ---
ROOT_DIR: Final[Path] = Path(__file__).parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# --- CONFIGURAZIONE ---
DEFAULT_TIMEOUT: Final[int] = 120
MAX_WORKERS: Final[int] = max(1, multiprocessing.cpu_count() - 1)
SNIPER_THRESHOLD: Final[int] = 5
AI_REPORT_FILE: Final[Path] = Path(__file__).parent / ".test_results.json"
MAX_OUTPUT_CHARS: Final[int] = 2000  # Limite output per file nel report IA


# ─── Console ──────────────────────────────────────────────────────────────────


class Console:
    """Helper per output ANSI colorato. Silenziabile in AI mode."""

    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CLEAR_LINE = "\033[K"
    MOVE_UP = "\033[F"

    _silent: bool = False

    @classmethod
    def set_silent(cls, silent: bool) -> None:
        """Attiva/disattiva il silenzio (per AI mode)."""
        cls._silent = silent

    @staticmethod
    def print(msg: str, color: str = ENDC, end: str = "\n") -> None:
        """Stampa un messaggio colorato."""
        if Console._silent:
            return
        print(f"{color}{msg}{Console.ENDC}", end=end, flush=True)

    @staticmethod
    def header(msg: str) -> None:
        """Stampa un header con separatore."""
        Console.print(f"\n{Console.BOLD}{msg}{Console.ENDC}", Console.HEADER)

    @staticmethod
    def success(msg: str) -> None:
        """Stampa un messaggio di successo."""
        Console.print(msg, Console.GREEN)

    @staticmethod
    def error(msg: str) -> None:
        """Stampa un messaggio di errore."""
        Console.print(msg, Console.FAIL)

    @staticmethod
    def dim(msg: str) -> None:
        """Stampa un messaggio attenuato."""
        Console.print(msg, Console.DIM)


# ─── Dataclass ────────────────────────────────────────────────────────────────


@dataclass
class FailureDetail:
    """Dettaglio strutturato di un singolo test fallito, ottimizzato per IA."""

    node_id: str
    file: str
    test_name: str
    error_type: str
    error_message: str
    traceback: str
    category: str  # import_error, assertion, timeout, runtime, crash


@dataclass
class TestResult:
    """Risultato di un singolo file/NodeID test."""

    target: str
    success: bool
    duration: float
    passed: int = 0
    failed: int = 0
    error_msg: str | None = None
    full_output: str | None = None
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())


@dataclass
class AIReport:
    """Report strutturato completo per consumo IA."""

    success: bool
    total_passed: int
    total_failed: int
    duration: float
    strategy: str  # SNIPER | SHOTGUN
    total_files: int
    failures: list[dict[str, Any]]
    file_results: list[dict[str, Any]]
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())


# ─── Helpers ──────────────────────────────────────────────────────────────────


def _build_env() -> dict[str, str]:
    """Costruisce l'environment per i subprocess dei test."""
    env = os.environ.copy()
    env["QT_QPA_PLATFORM"] = "offscreen"
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    # Assicura che i test non usino MAI la directory reale dell'utente
    if "SYNCROJOB_CONFIG_DIR" not in env:
        # Usiamo una sottocartella in temp per isolamento globale
        base_temp = Path(tempfile.gettempdir()) / "syncrojob_global_test_env"
        env["SYNCROJOB_CONFIG_DIR"] = str(base_temp)

    return env


def _parse_pytest_summary(output: str) -> tuple[int, int]:
    """Estrae (passed, failed) dalla riga di summary di pytest.

    Gestisce correttamente righe con sia 'failed' che 'error',
    es: '3 failed, 2 error, 10 passed in 5.2s'.
    """
    passed = 0
    failed = 0
    for line in reversed(output.splitlines()):
        if "passed" in line or "failed" in line or "error" in line:
            p_match = re.search(r"(\d+)\s+passed", line)
            # BUG-2 FIX: Usa findall per catturare SIA failed CHE error
            f_matches = re.findall(r"(\d+)\s+(?:failed|error)", line)
            if p_match:
                passed = int(p_match.group(1))
            for fm in f_matches:
                failed += int(fm)
            if p_match or f_matches:
                break
    return passed, failed


def _extract_failures(output: str, target: str) -> list[FailureDetail]:
    """Estrae dettagli strutturati dei fallimenti dall'output pytest.

    Parsing del formato pytest per estrarre: nome test, tipo errore,
    messaggio, traceback, e categoria semantica.
    """
    failures: list[FailureDetail] = []
    lines = output.splitlines()

    # Cerca blocchi FAILED
    i = 0
    while i < len(lines):
        line = lines[i]

        # Pattern: "FAILED tests/unit/test_foo.py::test_bar - ErrorType: msg"  # noqa: ERA001
        failed_match = re.match(r"FAILED\s+([\S]+::\S+)\s*-?\s*(.*)", line)
        if failed_match:
            node_id = failed_match.group(1)
            error_summary = failed_match.group(2).strip()
            file_path = node_id.split("::")[0]
            test_name = node_id.split("::")[-1]
            error_type, error_message, category = _classify_error(error_summary, output, node_id)

            # Estrai il traceback relativo a questo test
            tb = _extract_traceback_block(lines, node_id)

            failures.append(
                FailureDetail(
                    node_id=node_id,
                    file=file_path,
                    test_name=test_name,
                    error_type=error_type,
                    error_message=error_message,
                    traceback=tb,
                    category=category,
                )
            )
            i += 1
            continue

        # Pattern alternativo: "E   ImportError: ..." o "E   AssertionError: ..."
        # BUG-5 FIX: Rimosso 'not failures' — cattura tutti gli errori E-prefix,
        # la deduplica avviene in _finish_ai() per node_id.
        if line.strip().startswith("E ") and re.match(r"E\s+\w+Error|E\s+\w+Exception", line.strip()):
            error_line = line.strip()[2:].strip()
            error_type, error_message, category = _classify_error(error_line, output, target)
            tb = _extract_traceback_block(lines, target)
            failures.append(
                FailureDetail(
                    node_id=target,
                    file=target.split("::")[0],
                    test_name=target.split("::")[-1] if "::" in target else target,
                    error_type=error_type,
                    error_message=error_message,
                    traceback=tb,
                    category=category,
                )
            )
        i += 1

    return failures


def _classify_error(error_text: str, full_output: str, node_id: str) -> tuple[str, str, str]:  # noqa: PLR0911
    """Classifica un errore in tipo, messaggio e categoria semantica."""
    error_text = error_text.strip()

    # ImportError / ModuleNotFoundError
    if "ImportError" in error_text or "ModuleNotFoundError" in error_text:
        return "ImportError", error_text, "import_error"

    # AssertionError
    # BUG-3 FIX: Python usa 'AssertionError', non 'AssertionError'
    if "AssertionError" in error_text or "assert " in error_text.lower():
        return "AssertionError", error_text, "assertion"

    # TypeError / ValueError / AttributeError
    if "TypeError" in error_text:
        return "TypeError", error_text, "runtime"
    if "ValueError" in error_text:
        return "ValueError", error_text, "runtime"
    if "AttributeError" in error_text:
        return "AttributeError", error_text, "runtime"

    # Timeout
    if "TIMEOUT" in error_text or "TimeoutError" in error_text:
        return "TimeoutError", error_text, "timeout"

    # Crash nativo (segfault, access violation)
    if any(x in full_output.lower() for x in ("segfault", "access violation", "fatal")):
        return "NativeCrash", error_text, "crash"

    # Generico
    type_match = re.match(r"(\w+Error|\w+Exception):\s*(.*)", error_text)
    if type_match:
        return type_match.group(1), type_match.group(2), "runtime"

    return "UnknownError", error_text or "No error details captured", "runtime"


def _extract_traceback_block(lines: list[str], node_id: str) -> str:
    """Estrae il blocco di traceback rilevante per un test specifico.

    BUG-6 FIX: Matching piu' preciso — usa i delimitatori pytest
    (riga di '=' o '_') che contengono il nome del test, invece di
    matchare qualsiasi riga con il nome del test + '='.
    """
    in_block = False
    tb_lines: list[str] = []
    test_name = node_id.split("::")[-1] if "::" in node_id else node_id

    for line in lines:
        # Inizio blocco: header pytest delimitato (es. "___ test_foo ___" o "=== FAILURES ===")
        if test_name in line and (
            re.match(r"^[_= ]{5,}", line)  # Riga di delimitazione pytest
            or "FAILED" in line
        ):
            in_block = True
            tb_lines = [line]
            continue
        if in_block:
            tb_lines.append(line)
            # Fine blocco: nuova riga di separazione lunga (almeno 10 '=' o '_')
            if re.match(r"^[=]{10,}", line) and len(tb_lines) > 2:
                break

    return "\n".join(tb_lines[-50:]) if tb_lines else ""


def _collect_tests_inprocess(mark: str | None = None) -> list[str]:
    """Discovery dei test in-process via pytest --collect-only -q."""
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests",
        "--collect-only",
        "-q",
        "-o",
        "addopts=",
        "-p",
        "no:sugar",
        "-p",
        "no:cacheprovider",
    ]
    if mark:
        cmd.extend(["-m", mark])

    env = _build_env()
    try:
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=ROOT_DIR,
            timeout=60,
            env=env,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
        node_ids = []
        for line in res.stdout.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith(("=", "no tests", "ERROR")):
                break
            if "::" in stripped:
                node_ids.append(stripped)
        return node_ids  # noqa: TRY300
    except subprocess.TimeoutExpired:
        Console.error("[!] Timeout nella discovery dei test (60s)")
        return []


# ─── Worker (SHOTGUN) ────────────────────────────────────────────────────────


def _worker_task(
    target: str,
    timeout: int,
    mark: str | None = None,
    with_cov: bool = False,
    ai_mode: bool = False,
) -> TestResult:
    """Funzione stand-alone per il pool di processi (SHOTGUN)."""
    env = _build_env()

    # FIX: Isolamento totale (Config + Coverage) su Windows
    # Usiamo una directory dedicata per worker per evitare conflitti e PermissionError
    worker_id = f"{os.getpid()}_{int(time.time() * 1000)}"
    temp_config_dir = Path(tempfile.gettempdir()) / f"syncrojob_test_{worker_id}"
    temp_config_dir.mkdir(parents=True, exist_ok=True)

    env["SYNCROJOB_CONFIG_DIR"] = str(temp_config_dir)

    if with_cov:
        env["COVERAGE_FILE"] = f".coverage.worker.{worker_id}"

    # In AI mode: --tb=long per traceback completi, altrimenti --tb=short
    tb_style = "long" if ai_mode else "short"
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        target,
        "--no-header",
        "-q",
        f"--tb={tb_style}",
        "-p",
        "no:sugar",
        "-p",
        "no:cacheprovider",
    ]

    # Se la copertura non è richiesta esplicitamente, la disabilitiamo.
    # FIX: Usiamo -o addopts= per evitare conflitti con gli argomenti --cov definiti in pyproject.toml
    if not with_cov:
        cmd.extend(["-p", "no:cov", "-o", "addopts="])
    else:
        cmd.extend(["--cov=src", "--cov-append"])

    start = time.time()
    try:
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=ROOT_DIR,
            timeout=timeout,
            check=False,
            env=env,
            encoding="utf-8",
            errors="replace",
        )
        duration = time.time() - start
        output = res.stdout + res.stderr
        passed, failed = _parse_pytest_summary(output)

        # Un test è fallito se il returncode != 0 o se ci sono errori interni/crash
        success = res.returncode == 0 and "INTERNALERROR" not in output

        error_msg = None
        if not success:
            for line in reversed(output.splitlines()):
                if any(x in line for x in ("E ", "Error:", "FAILED", "ImportError", "INTERNALERROR")):
                    error_msg = line.strip()
                    break
            if not error_msg:
                error_msg = f"Exit code {res.returncode}"

        return TestResult(target, success, duration, passed, failed, error_msg, output)
    except subprocess.TimeoutExpired:
        return TestResult(target, False, time.time() - start, 0, 0, "TIMEOUT", "Execution timed out")
    except Exception as e:
        return TestResult(target, False, 0, 0, 0, str(e), str(e))


# ─── Runner ──────────────────────────────────────────────────────────────────


class UltraRunner:
    """Orchestratore principale dei test con modalita' ibride."""

    def __init__(self) -> None:
        self.failed_list: list[dict[str, str | None]] = []
        self.failure_details: list[FailureDetail] = []
        self.file_results: list[TestResult] = []
        self.total_passed = 0
        self.total_failed = 0
        self.start_time = 0.0
        self.ai_mode = False
        self.strategy = "SHOTGUN"
        self._exit_code = 0  # ARCH-2: Exit code centralizzato

    # ── Dashboard ANSI ──

    def _draw_dashboard(self, completed: int, total: int) -> None:
        """Disegna la progress bar ANSI per SHOTGUN mode."""
        pct = (completed / total * 100) if total > 0 else 0
        elapsed = time.time() - self.start_time
        speed = completed / elapsed if elapsed > 0 else 0
        eta = (total - completed) / speed if speed > 0 else 0

        bar_len = 30
        filled = bar_len * completed // total if total > 0 else 0
        bar = "\u2588" * filled + "\u2591" * (bar_len - filled)

        green = Console.GREEN if self.total_passed > 0 else ""
        red = Console.FAIL if self.total_failed > 0 else ""

        sys.stdout.write(Console.MOVE_UP * 3 if completed > 0 else "")
        sys.stdout.write(f"\r{Console.CLEAR_LINE}{Console.BOLD}SHOTGUN DASHBOARD{Console.ENDC}\n")
        sys.stdout.write(
            f"{Console.CLEAR_LINE}Progresso: [{bar}] {pct:5.1f}% | {completed}/{total} | ETA: {eta:4.0f}s\n"
        )
        sys.stdout.write(
            f"{Console.CLEAR_LINE}Stato:     "
            f"{green}PASS: {self.total_passed}{Console.ENDC} | "
            f"{red}FAIL: {self.total_failed}{Console.ENDC} | "
            f"{Console.CYAN}CPU: {MAX_WORKERS}{Console.ENDC}\n"
        )
        sys.stdout.flush()

    # ── SNIPER ──

    def _run_sniper(self, targets: list[str], args: argparse.Namespace) -> None:  # noqa: C901, PLR0912
        """Esecuzione diretta e live, ottimizzata per il debugging."""
        self.strategy = "SNIPER"
        Console.header(f"SNIPER MODE: Esecuzione mirata di {len(targets)} target")

        env = _build_env()
        tb_style = "long" if self.ai_mode else "short"
        cmd = [sys.executable, "-m", "pytest", *targets, "-v", f"--tb={tb_style}"]
        if args.exitfirst:
            cmd.append("-x")
        if args.mark:
            cmd.extend(["-m", args.mark])
        if args.cov:
            cmd.extend(["--cov=src"])

        self.start_time = time.time()

        if self.ai_mode:
            # In AI mode: cattura output per parsing strutturato
            res = subprocess.run(
                cmd,
                cwd=ROOT_DIR,
                check=False,
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            dur = time.time() - self.start_time
            output = res.stdout + res.stderr
            passed, failed = _parse_pytest_summary(output)
            self.total_passed = passed
            self.total_failed = failed

            self.file_results.append(
                TestResult(
                    target=", ".join(targets),
                    success=res.returncode == 0,
                    duration=dur,
                    passed=passed,
                    failed=failed,
                    error_msg=None if res.returncode == 0 else "Test failures",
                    full_output=output,
                )
            )

            if res.returncode != 0:
                # Estrai dettagli dei fallimenti
                for target in targets:
                    self.failure_details.extend(_extract_failures(output, target))
                # BUG-4 FIX: Retry con --last-failed per rieseguire solo i falliti
                retry_cmd = [*cmd, "--last-failed", "--no-header"]
                for _attempt in range(1, args.retry + 1):
                    res_retry = subprocess.run(
                        retry_cmd,
                        cwd=ROOT_DIR,
                        check=False,
                        env=env,
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                    )
                    if res_retry.returncode == 0:
                        self.failure_details.clear()
                        p, _ = _parse_pytest_summary(res_retry.stdout + res_retry.stderr)
                        self.total_passed = p
                        self.total_failed = 0
                        break

            self._finish_ai(len(targets))
        else:
            # Modalita' umana: stdout live
            res_human = subprocess.run(cmd, cwd=ROOT_DIR, check=False, env=env)
            dur = time.time() - self.start_time

            if res_human.returncode == 0:
                Console.success(f"\nSNIPER SHOT: Successo in {dur:.2f}s")
                self._exit_code = 0
            else:
                # BUG-4 FIX: Retry con --last-failed
                retry_cmd = [*cmd, "--last-failed", "--no-header"]
                if args.retry > 0:
                    Console.header(f"RETRY: Riesecuzione ({args.retry} tentativi rimanenti)")
                    for attempt in range(1, args.retry + 1):
                        Console.print(f"  Tentativo {attempt}/{args.retry}...", Console.WARNING)
                        res_human_retry = subprocess.run(retry_cmd, cwd=ROOT_DIR, check=False, env=env)
                        if res_human_retry.returncode == 0:
                            dur_total = time.time() - self.start_time
                            Console.success(
                                f"\nSNIPER SHOT: Successo al tentativo {attempt + 1} in {dur_total:.2f}s"
                            )
                            self._exit_code = 0
                            return
                Console.error(f"\nSNIPER SHOT: Fallito in {dur:.2f}s")
                self._exit_code = 1

    # ── SHOTGUN ──

    def _run_shotgun(self, args: argparse.Namespace) -> None:  # noqa: C901, PLR0912, PLR0915
        """Esecuzione massiva e parallela, ottimizzata per l'intera suite."""
        self.strategy = "SHOTGUN"
        Console.header("SHOTGUN MODE: Analisi massiva suite")

        # Discovery in-process
        Console.dim("  Collection in corso...")
        collection_start = time.time()
        node_ids = _collect_tests_inprocess(mark=args.mark)
        collection_dur = time.time() - collection_start

        if not node_ids:
            Console.error("x Nessun test trovato!")
            if self.ai_mode:
                self._finish_ai(0)
            return

        Console.dim(f"  Trovati {len(node_ids)} test in {collection_dur:.2f}s")

        # Raggruppa per file
        files_map: dict[str, list[str]] = defaultdict(list)
        for nid in node_ids:
            files_map[nid.split("::")[0]].append(nid)

        queue = sorted(files_map.keys(), key=lambda x: len(files_map[x]), reverse=True)
        total_files = len(queue)

        if args.cov:
            with contextlib.suppress(Exception):
                subprocess.run(
                    [sys.executable, "-m", "coverage", "erase"],
                    check=False,
                    cwd=ROOT_DIR,
                )

        self.start_time = time.time()
        isolation_queue: list[str] = []

        Console.print(
            f"\n  Avvio esecuzione ({MAX_WORKERS} workers, {total_files} file)\n\n\n", Console.GREEN
        )

        completed = 0
        try:
            with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
                futures = {
                    executor.submit(
                        _worker_task,
                        f,
                        args.timeout,
                        args.mark,
                        args.cov,
                        self.ai_mode,
                    ): f
                    for f in queue
                }
                try:
                    for future in as_completed(futures):
                        target = futures[future]
                        try:
                            res = future.result()
                            completed += 1
                            self.file_results.append(res)
                            if not res.success:
                                # BUG-1 FIX: NON contare qui i file che vanno in isolamento.
                                # I conteggi verranno fatti nella fase di isolamento.
                                isolation_queue.append(target)
                                # Estrai dettagli fallimento per IA
                                if self.ai_mode and res.full_output:
                                    self.failure_details.extend(_extract_failures(res.full_output, target))
                            else:
                                # Conta solo i file che hanno avuto successo definitivo
                                self.total_passed += res.passed
                                self.total_failed += res.failed

                            self._draw_dashboard(completed, total_files)

                            # Controllo soglia fallimenti per interruzione anticipata
                            current_fails = self.total_failed + sum(
                                1 for r in self.file_results if not r.success
                            )
                            if args.exitfirst or (args.max_fail > 0 and current_fails >= args.max_fail):
                                with contextlib.suppress(Exception):
                                    executor.shutdown(wait=False, cancel_futures=True)
                                break

                        except Exception as e:
                            completed += 1
                            Console.error(f"\n  Worker error su {target}: {e}")
                            isolation_queue.append(target)
                            self._draw_dashboard(completed, total_files)
                except BrokenProcessPool:
                    Console.error("\n  [!] WORKER CRASH (Segfault/Qt). Recupero task rimanenti...")
                    for future_remaining, target_remaining in futures.items():
                        if not future_remaining.done():
                            isolation_queue.append(target_remaining)
                    Console.error(f"  [!] {len(isolation_queue)} file spostati in isolamento.")
        except Exception as global_e:
            Console.error(f"\n  [FATAL] Errore globale nel pool: {global_e}")

        # Fase Isolamento
        if isolation_queue:
            print("\n")
            Console.header(f"FASE ISOLAMENTO: Riesecuzione sequenziale di {len(isolation_queue)} file")
            for target in isolation_queue:
                if args.exitfirst and self.total_failed > 0:
                    break
                if args.max_fail > 0 and self.total_failed >= args.max_fail:
                    Console.error(
                        f"\n[!] Raggiunta soglia di {args.max_fail} fallimenti. Interruzione anticipata."
                    )
                    break

                Console.print(f"  Analisi: {target}", Console.BOLD)
                for node in files_map.get(target, [target]):
                    if args.exitfirst and self.total_failed > 0:
                        break
                    if args.max_fail > 0 and self.total_failed >= args.max_fail:
                        break

                    short_name = node.split("::")[-1]
                    # In AI mode usiamo stderr per i log di progresso per lasciare stdout pulito per il JSON
                    out_file = sys.stderr if self.ai_mode else sys.stdout
                    print(f"    {short_name} ... ", end="", file=out_file, flush=True)

                    max_attempts = 1 + args.retry
                    final_res: TestResult | None = None
                    for attempt in range(max_attempts):
                        res = _worker_task(
                            node,
                            args.timeout + 30,
                            args.mark,
                            args.cov,
                            self.ai_mode,
                        )
                        if res.success:
                            label = "PASS" if attempt == 0 else f"FIXED (attempt {attempt + 1})"
                            # Console.success/error sono silenti in AI mode, usiamo print diretto su out_file
                            if self.ai_mode:
                                print(f"\033[92m{label}\033[0m", file=out_file, flush=True)
                            else:
                                Console.success(label)

                            # BUG-1 FIX: Conta dal risultato effettivo dell'isolamento
                            self.total_passed += res.passed
                            self.file_results.append(res)
                            final_res = res
                            break
                        final_res = res
                    else:
                        if self.ai_mode:
                            print("\033[91mFAIL\033[0m", file=out_file, flush=True)
                        else:
                            Console.error("FAIL")

                        # BUG-1 FIX: Conta dal risultato effettivo dell'isolamento.
                        # Assicura che se il test fallisce venga contato almeno 1 errore.
                        if final_res is not None:
                            self.total_passed += final_res.passed
                            added_fails = final_res.failed if final_res.failed > 0 else 1
                            self.total_failed += added_fails
                            self.failed_list.append({"id": node, "error": final_res.error_msg})
                            self.file_results.append(final_res)
                            if self.ai_mode and final_res.full_output:
                                self.failure_details.extend(_extract_failures(final_res.full_output, node))
                        else:
                            self.total_failed += 1
                            self.failed_list.append({"id": node, "error": "No result captured"})

        if self.ai_mode:
            self._finish_ai(total_files)
        else:
            self._finish_human(args.cov)

    # ── Report Finale (AI) ──

    def _finish_ai(self, total_files: int) -> None:
        """Output JSON strutturato per agenti IA. Scrive su file + stdout."""
        duration = time.time() - self.start_time

        # Deduplica failure_details per node_id
        seen: set[str] = set()
        unique_failures: list[FailureDetail] = []
        for fd in self.failure_details:
            if fd.node_id not in seen:
                seen.add(fd.node_id)
                unique_failures.append(fd)

        report = AIReport(
            success=self.total_failed == 0 and not unique_failures,
            total_passed=self.total_passed,
            total_failed=self.total_failed,
            duration=duration,
            strategy=self.strategy,
            total_files=total_files,
            failures=[asdict(f) for f in unique_failures],
            # ARCH-4 FIX: Escludi full_output dal report, tronca error_msg
            file_results=[
                {
                    "target": r.target,
                    "success": r.success,
                    "duration": round(r.duration, 3),
                    "passed": r.passed,
                    "failed": r.failed,
                    "error_msg": (r.error_msg[:MAX_OUTPUT_CHARS] if r.error_msg else None),
                }
                for r in sorted(self.file_results, key=lambda x: x.duration, reverse=True)
            ],
        )

        report_dict = asdict(report)

        # Scrivi il report su file persistente (leggibile dall'IA dopo il run)
        AI_REPORT_FILE.write_text(
            json.dumps(report_dict, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        # Output JSON su stdout per consumo diretto
        print(json.dumps(report_dict, indent=2, ensure_ascii=False))

        # ARCH-2 FIX: Salva exit code invece di chiamare sys.exit() direttamente
        self._exit_code = 0 if report.success else 1

        # AGGRESSIVE EXIT: Forza l'uscita se in AI mode per evitare processi orfani appesi
        if self.ai_mode:
            os._exit(self._exit_code)

    # ── Report Finale (Umano) ──

    def _finish_human(self, with_cov: bool) -> None:
        """Report ANSI per umani."""
        duration = time.time() - self.start_time
        Console.header("ESECUZIONE COMPLETATA")

        if self.file_results:
            Console.print(f"\n{'File':<60} {'Status':<8} {'P':>4} {'F':>4} {'Time':>7}", Console.BOLD)
            Console.print("-" * 85, Console.DIM)
            for r in sorted(self.file_results, key=lambda x: x.duration, reverse=True):
                status = (
                    f"{Console.GREEN}PASS{Console.ENDC}" if r.success else f"{Console.FAIL}FAIL{Console.ENDC}"
                )
                name = r.target if len(r.target) <= 58 else "..." + r.target[-55:]
                print(f"  {name:<58} {status:<17} {r.passed:>4} {r.failed:>4} {r.duration:>6.2f}s")

        Console.print(
            f"\n  Totale: {self.total_passed} passed, {self.total_failed} failed in {duration:.2f}s",
            Console.BOLD,
        )

        if with_cov:
            Console.header("REPORT COPERTURA")
            with contextlib.suppress(Exception):
                subprocess.run([sys.executable, "-m", "coverage", "combine"], check=False, cwd=ROOT_DIR)
                subprocess.run([sys.executable, "-m", "coverage", "report", "-m"], check=False, cwd=ROOT_DIR)
                subprocess.run([sys.executable, "-m", "coverage", "html"], check=False, cwd=ROOT_DIR)

        if self.failed_list:
            Console.error(f"\n  Suite fallita con {len(self.failed_list)} errori:")
            for f in self.failed_list:
                Console.error(f"    - {f['id']}: {f['error']}")
            # ARCH-2 FIX: Salva exit code invece di sys.exit()
            self._exit_code = 1
        else:
            Console.success("\n  Suite completata con successo!")
            self._exit_code = 0

    # ── Entry Point ──

    def run(self) -> None:
        """Entry point principale del runner."""
        parser = argparse.ArgumentParser(description="Ultra Test Runner V5.0 (The Apex Runner)")
        parser.add_argument("targets", nargs="*", help="File, cartelle o NodeID da testare.")
        parser.add_argument("--reset", action="store_true", help="Pulisce copertura e cache.")
        parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Timeout per worker (s).")
        parser.add_argument("-m", "--mark", help="Filtra per marker pytest.")
        parser.add_argument("--cov", action="store_true", help="Abilita il calcolo della copertura.")
        parser.add_argument("--retry", type=int, default=0, help="Num. retry per test falliti (flaky).")
        parser.add_argument("--ai", action="store_true", help="Output JSON strutturato per agenti IA.")
        parser.add_argument(
            "-x", "--exitfirst", action="store_true", help="Ferma l'esecuzione al primo fallimento."
        )
        parser.add_argument(
            "--max-fail", type=int, default=0, help="Ferma l'esecuzione dopo N test falliti (0 = illimitato)."
        )
        args = parser.parse_args()

        # AI mode: silenzia Console, output solo JSON
        self.ai_mode = args.ai
        if self.ai_mode:
            Console.set_silent(True)

        # Abilita ANSI su vecchi CMD Windows
        if sys.platform == "win32" and not self.ai_mode:
            import ctypes  # noqa: PLC0415

            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

        # Reset completo se richiesto
        if args.reset:
            with contextlib.suppress(Exception):
                subprocess.run([sys.executable, "-m", "coverage", "erase"], check=False, cwd=ROOT_DIR)

        # Strategia: <= SNIPER_THRESHOLD target specifici -> SNIPER, altrimenti -> SHOTGUN
        if args.targets and len(args.targets) <= SNIPER_THRESHOLD:
            self._run_sniper(args.targets, args)
        else:
            self._run_shotgun(args)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    runner = UltraRunner()
    runner.run()
    # ARCH-2 FIX: Unico punto di exit del processo
    sys.exit(runner._exit_code)
