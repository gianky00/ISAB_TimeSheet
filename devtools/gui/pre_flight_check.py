#!/usr/bin/env python3
"""SyncroJob Master Developer Tool & Pre-Flight Check (Apex Edition)
====================================================================
L'Oracolo del Progetto: Score, Dashboard HTML, Git-Hooks e Intelligence.
"""

import argparse
import contextlib
import datetime
import io
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

if sys.platform == "win32":
    with contextlib.suppress(Exception):
        if hasattr(sys.stdout, "buffer"):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "buffer"):
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Rich Imports
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import (
        BarColumn,
        Progress,
        SpinnerColumn,
        TextColumn,
        TimeElapsedColumn,
    )
    from rich.table import Table
except ImportError:
    print("[ERROR] Rich non installato. Esegui 'python -m pip install rich' prima.")
    sys.exit(1)

# Configurazione Base
PROJECT_ROOT = Path(__file__).parent.parent
LOG_DIR = PROJECT_ROOT / ".cache" / "temp" / "logs"
REPORT_DIR = PROJECT_ROOT / ".cache" / "reports" / "preflight"
VENV_BIN = PROJECT_ROOT / ".venv" / "Scripts" if sys.platform == "win32" else PROJECT_ROOT / ".venv" / "bin"

# Configurazione console con fallback ASCII per compatibilità Windows
# Rileva se stiamo girando da subprocess/GUI (no TTY)
is_subprocess = not sys.stdout.isatty() or os.getenv("TERM") == "dumb"

console = Console(
    legacy_windows=False,  # Disabilita rendering legacy Windows problematico
    force_terminal=not is_subprocess,  # Plain text se subprocess
    no_color=is_subprocess or os.getenv("NO_COLOR") == "1",
    width=120 if is_subprocess else None,
)


class CheckResult:
    """Rappresenta l'esito di un singolo controllo di integrità o qualità."""

    def __init__(self, label: str, success: bool, msg: str, duration: float, name: str) -> None:
        """Inizializza il risultato con metadati e timestamp."""
        self.label = label
        self.success = success
        self.msg = msg
        self.duration = duration
        self.name = name
        self.timestamp = datetime.datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


def get_bin(name: str) -> str:
    """Recupera il percorso dell'eseguibile nel venv o nei path standard di Python.

    Args:
        name: Nome dell'eseguibile (senza estensione).

    Returns:
        str: Percorso completo dell'eseguibile o il nome originale se non trovato.
    """
    ext = ".exe" if sys.platform == "win32" else ""

    # 1. Prova nel VENV
    venv_path = VENV_BIN / f"{name}{ext}"
    if venv_path.exists():
        return str(venv_path)

    # 2. Prova in APPDATA (Windows fallback per installazioni --user)
    if sys.platform == "win32":
        appdata_path = (
            Path(os.environ.get("APPDATA", "")) / "Python" / "Python312" / "Scripts" / f"{name}{ext}"
        )
        if appdata_path.exists():
            return str(appdata_path)

    return name


def run_tool(name: str, cmd: list[str], label: str, cwd: Path = PROJECT_ROOT) -> tuple[bool, str, float]:
    """Esegue uno strumento esterno registrando l'output in un file di log dedicato.

    Args:
        name: Identificativo dello strumento.
        cmd: Lista di argomenti del comando.
        label: Etichetta per la visualizzazione.
        cwd: Directory di lavoro.

    Returns:
        tuple: (successo, output_errore, durata).
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"{name}.log"
    start_t = time.time()
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            env=env,
            timeout=120,  # Timeout di sicurezza per evitare blocchi infiniti
        )
        duration = time.time() - start_t
        log_file.write_text(
            f"CMD: {' '.join(cmd)}\nEXIT: {result.returncode}\n{'=' * 40}\n{result.stdout}\n{'=' * 40}\n{result.stderr}",
            encoding="utf-8",
        )
        return (  # noqa: TRY300
            (result.returncode == 0),
            result.stdout if result.returncode != 0 else "",
            duration,
        )
    except subprocess.TimeoutExpired:
        duration = time.time() - start_t
        return False, f"Timeout superato ({duration:.1f}s). Il processo si era bloccato.", duration
    except Exception as e:
        return False, f"Eccezione: {e}", time.time() - start_t


def _run_tests_ai(reset: bool = True) -> tuple[bool, str, float]:
    """Esegue il runner V5.0 in modalita' AI e parsa il report JSON strutturato.

    Returns:
        tuple: (successo, messaggio_strutturato, durata).
    """
    cmd = [
        sys.executable,
        str(PROJECT_ROOT / "tests" / "run_robust_test"),
        "--ai",
    ]
    if reset:
        cmd.append("--reset")

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    start_t = time.time()

    try:
        result = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            env=env,
            timeout=300,
        )
        duration = time.time() - start_t

        # Salva log grezzo
        (LOG_DIR / "robust_tests.log").write_text(
            f"CMD: {' '.join(cmd)}\nEXIT: {result.returncode}\n{'=' * 40}\n{result.stdout}\n{result.stderr}",
            encoding="utf-8",
        )

        # Prova a leggere il report JSON (dal file o dallo stdout)
        report_file = PROJECT_ROOT / "tests" / ".test_results.json"
        report: dict | None = None
        if report_file.exists():
            with contextlib.suppress(Exception):
                report = json.loads(report_file.read_text(encoding="utf-8"))
        if report is None:
            with contextlib.suppress(Exception):
                report = json.loads(result.stdout)

        if report is None:
            # Fallback: nessun JSON parsabile
            return result.returncode == 0, result.stdout[:500], duration

        # Costruisci messaggio strutturato
        passed = report.get("total_passed", 0)
        failed = report.get("total_failed", 0)
        failures = report.get("failures", [])

        if not failures:
            return True, f"{passed} passed in {report.get('duration', duration):.1f}s", duration

        # Messaggio con dettagli dei fallimenti
        msg_lines = [f"{passed} passed, {failed} failed:"]
        msg_lines.extend(
            f"  [{f.get('category', '?')}] {f.get('file', '?')}::{f.get('test_name', '?')}"
            f" -> {f.get('error_type', '?')}: {f.get('error_message', '')[:100]}"
            for f in failures[:10]
        )
        if len(failures) > 10:  # noqa: PLR2004
            msg_lines.append(f"  ... e altri {len(failures) - 10} errori")

        return False, "\n".join(msg_lines), duration

    except subprocess.TimeoutExpired:
        return False, "Timeout (300s)", time.time() - start_t
    except Exception as e:
        return False, f"Eccezione: {e}", time.time() - start_t


def find_git_executable():
    """Tenta di trovare l'eseguibile git in percorsi comuni su Windows."""
    git_bin = shutil.which("git")
    if git_bin:
        return git_bin
    if sys.platform != "win32":
        return "git"
    common_paths = [
        Path(os.environ.get("PROGRAMFILES", "C:/Program Files")) / "Git/cmd/git.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)")) / "Git/cmd/git.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "GitHubDesktop" / "bin" / "git.exe",
    ]
    github_desktop_root = Path(os.environ.get("LOCALAPPDATA", "")) / "GitHubDesktop"
    if github_desktop_root.exists():
        for app_dir in github_desktop_root.glob("app-*"):
            git_path = app_dir / "resources" / "app" / "git" / "cmd" / "git.exe"
            if git_path.exists():
                common_paths.append(git_path)
    for p in common_paths:
        if p.exists():
            return str(p)
    return "git"


# --- APEX ENGINE ---


class ApexAudit:
    """Motore di audit principale che esegue una suite completa di test e controlli statici."""

    def __init__(  # noqa: PLR0913
        self,
        fix=False,
        fast=False,
        incremental=False,
        test_only=False,
        target: str | None = None,
        force=False,
    ) -> None:
        """Inizializza l'audit configurando le modalità di esecuzione."""
        self.fix = fix
        self.fast = fast
        self.incremental = incremental
        self.test_only = test_only
        self.target = target.lower() if target else None
        self.force = force
        self.results: list[CheckResult] = []
        self.start_time = time.time()
        self.git_bin = find_git_executable()
        self.changed_files = self._get_changed_files() if incremental else []

    def _get_changed_files(self) -> list[str]:
        try:
            cmd = [self.git_bin, "diff", "HEAD", "--name-only"]
            res = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT, check=False)
            return [f for f in res.stdout.splitlines() if f.endswith(".py") and Path(f).exists()]
        except Exception:
            return []

    def _check_environment(self) -> tuple[bool, str, float]:  # noqa: C901
        start_t = time.time()
        c_ver = "N/A"
        d_ver = "N/A"
        try:
            if sys.platform == "win32":
                # Try User first, then Machine
                for key in [
                    r"HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon",
                    r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome",
                    r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome",
                ]:
                    res = subprocess.run(
                        ["reg", "query", key, "/v", "version"], capture_output=True, text=True, check=False
                    )
                    match = re.search(
                        r"(?:version|DisplayVersion)\s+REG_SZ\s+([\d\.]+)", res.stdout, re.IGNORECASE
                    )
                    if match:
                        c_ver = match.group(1)
                        break
            else:
                res = subprocess.run(
                    ["google-chrome", "--version"], capture_output=True, text=True, check=False
                )
                if res.returncode == 0:
                    match = re.search(r"([\d\.]+)", res.stdout)
                    if match:
                        c_ver = match.group(1)

            # Safe check for chromedriver
            cd_path = shutil.which("chromedriver")
            if cd_path:
                d_res = subprocess.run([cd_path, "--version"], capture_output=True, text=True, check=False)
                if d_res.returncode == 0:
                    d_match = re.search(r"([\d\.]+)", d_res.stdout)
                    if d_match:
                        d_ver = d_match.group(1)

            status = c_ver != "N/A"
            msg = f"Chrome:{c_ver} Driver:{d_ver}"
            if d_ver == "N/A":
                msg += " (Driver missing)"

            return status, msg, time.time() - start_t
        except Exception as e:
            return False, f"Env check error: {str(e)[:50]}", time.time() - start_t

    def _check_versions(self) -> tuple[bool, str, float]:
        start_t = time.time()
        try:
            pyproject = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
            toml_match = re.search(r'version\s*=\s*"(.*?)"', pyproject)
            code_match = re.search(
                r'__version__\s*=\s*"(.*?)"',
                (PROJECT_ROOT / "src/application/services/version.py").read_text(encoding="utf-8"),
            )
            if not toml_match or not code_match:
                return False, "Version not found", time.time() - start_t
            v_toml = toml_match.group(1)
            v_code = code_match.group(1)
            return (v_toml == v_code), f"v{v_toml}", time.time() - start_t
        except Exception:
            return False, "Version mismatch", time.time() - start_t

    def _check_db_integrity(self) -> tuple[bool, str, float]:
        start_t = time.time()
        from platformdirs import user_data_dir

        data_dir = Path(user_data_dir("SyncroJob", appauthor=False)) / "data"
        if not data_dir.exists():
            return True, "No DBs", time.time() - start_t
        errors = []
        dbs = list(data_dir.glob("*.db"))
        for db in dbs:
            try:
                with sqlite3.connect(db) as conn:
                    if conn.execute("PRAGMA integrity_check;").fetchone()[0] != "ok":
                        errors.append(db.name)
            except Exception:
                errors.append(db.name)
        return (
            (not errors),
            f"Checked {len(dbs)} DBs",
            time.time() - start_t,
        )

    def _scan_for_secrets(self) -> tuple[bool, str, float]:
        start_t = time.time()
        patterns = {"Key": r"(?:api_key|token)[\"']?\s*[:=]\s*[\"']([A-Za-z0-9_\-]{16,})[\"']"}
        found = []
        for path in (PROJECT_ROOT / "src").rglob("*.py"):
            with contextlib.suppress(Exception):
                content = path.read_text(encoding="utf-8")
                if any(re.search(p, content, re.IGNORECASE) for p in patterns.values()):
                    found.append(path.name)
        return (
            (not found),
            "No secrets found" if not found else f"Secrets in {found[0]}",
            time.time() - start_t,
        )

    def _run_parallel(self, parallel_checks) -> None:
        is_dumb = os.environ.get("TERM") == "dumb"

        if is_dumb:
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            console.print(f"[[dim]{ts}[/dim]] [bold yellow]Inizio controlli paralleli...[/bold yellow]")
            with ThreadPoolExecutor(max_workers=len(parallel_checks)) as executor:
                futures = {}
                for label, func, name, always_show in parallel_checks:
                    ts = datetime.datetime.now().strftime("%H:%M:%S")
                    console.print(f"[[dim]{ts}[/dim]] [dim] -> Avvio {label}...[/dim]")
                    futures[executor.submit(func)] = (label, name, always_show)

                for future in futures:  # noqa: PLC0206
                    label, name, always_show = futures[future]
                    success, msg, dur = future.result()
                    self._add_res(label, success, msg, dur, name, always_show)
                    ts = datetime.datetime.now().strftime("%H:%M:%S")
                    if success:
                        console.print(
                            f"[[dim]{ts}[/dim]] [green][OK] {label} completato in {dur:.1f}s.[/green]"
                        )
                    else:
                        console.print(f"[[dim]{ts}[/dim]] [red][X] {label} fallito in {dur:.1f}s.[/red]")
        else:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
            ) as prog:
                tasks = {
                    label: prog.add_task(f"Audit {label}...", total=100) for label, _, _, _ in parallel_checks
                }
                with ThreadPoolExecutor(max_workers=len(parallel_checks)) as executor:
                    futures = {
                        executor.submit(func): (label, name, always_show)
                        for label, func, name, always_show in parallel_checks
                    }
                    for future in futures:
                        label, name, always_show = futures[future]
                        success, msg, dur = future.result()
                        self._add_res(label, success, msg, dur, name, always_show)
                        prog.update(tasks[label], completed=100, description=f"[green][OK] {label}")

    def run_all(self) -> None:  # noqa: C901, PLR0912
        console.print(
            Panel.fit(
                "[bold cyan]SYNCROJOB APEX AUDIT ENGINE[/bold cyan]",
                border_style="cyan",
                safe_box=True,
            )
        )

        # Helper to wrap commands
        def cmd(tool, args):
            return lambda: run_tool(tool, args, tool)

        all_checks = [
            (
                "Lint (Ruff)",
                cmd(
                    "ruff",
                    [get_bin("ruff"), "check"]
                    + (self.changed_files if self.changed_files else ["."])
                    + (["--fix"] if self.fix else []),
                ),
                "ruff",
                False,
            ),
            (
                "Security (Bandit)",
                cmd("bandit", [get_bin("bandit"), "-r", "src/", "-ll", "-q", "-c", "pyproject.toml"]),
                "bandit",
                False,
            ),
            (
                "Types (Mypy)",
                cmd("mypy", [get_bin("mypy"), "src", "--ignore-missing-imports"]),
                "mypy",
                False,
            ),
            (
                "Complexity (Xenon)",
                cmd("xenon", [get_bin("xenon"), "-a", "B", "src"]),
                "xenon",
                False,
            ),
            (
                "Modernize (Refurb)",
                cmd("refurb", [get_bin("refurb"), "src"]),
                "refurb",
                False,
            ),
            (
                "Typos (Codespell)",
                cmd("codespell", [get_bin("codespell"), "src"]),
                "codespell",
                False,
            ),
            (
                "Docs (Interrogate)",
                cmd("interrogate", [get_bin("interrogate"), "src", "-q"]),
                "interrogate",
                False,
            ),
            ("Deps (Deptry)", cmd("deptry", [get_bin("deptry"), "."]), "deptry", False),
            (
                "Vulnerabilities",
                cmd(
                    "pip_audit",
                    [
                        get_bin("pip-audit"),
                        "--desc",
                        "off",
                        # --- Dipendenze senza fix disponibile ---
                        "--ignore-vuln",
                        "CVE-2025-69872",  # diskcache: no fix version yet
                        "--ignore-vuln",
                        "PYSEC-2022-42969",  # py: legacy dev dependency
                        "--ignore-vuln",
                        "PYSEC-2024-270",  # diagrams: no fix version yet
                        # --- Dipendenze transitive da tool di sviluppo ---
                        # aiohttp (portato da litellm/Gemini CLI)
                        "--ignore-vuln",
                        "CVE-2026-34515",
                        "--ignore-vuln",
                        "CVE-2026-34513",
                        "--ignore-vuln",
                        "CVE-2026-34516",
                        "--ignore-vuln",
                        "CVE-2026-34517",
                        "--ignore-vuln",
                        "CVE-2026-34519",
                        "--ignore-vuln",
                        "CVE-2026-34518",
                        "--ignore-vuln",
                        "CVE-2026-34520",
                        "--ignore-vuln",
                        "CVE-2026-34525",
                        "--ignore-vuln",
                        "CVE-2026-22815",
                        "--ignore-vuln",
                        "CVE-2026-34514",
                        # black (portato da mutatest)
                        "--ignore-vuln",
                        "CVE-2026-32274",
                        # litellm (portato da Gemini CLI)
                        "--ignore-vuln",
                        "CVE-2026-35029",
                        "--ignore-vuln",
                        "CVE-2026-35030",
                        "--ignore-vuln",
                        "CVE-2026-42271",
                        "--ignore-vuln",
                        "GHSA-69x8-hrgq-fjj8",
                        # gitpython (transitiva toolchain/dev tooling)
                        "--ignore-vuln",
                        "CVE-2026-42215",
                        "--ignore-vuln",
                        "CVE-2026-42284",
                        # lxml (transitiva)
                        "--ignore-vuln",
                        "CVE-2026-41066",
                        # poetry (tool di build)
                        "--ignore-vuln",
                        "CVE-2026-34591",
                        "--ignore-vuln",
                        "CVE-2026-41140",
                        # pyasn1 (transitiva)
                        "--ignore-vuln",
                        "CVE-2026-30922",
                        # pygments (transitiva di rich)
                        "--ignore-vuln",
                        "CVE-2026-4539",
                        # python-dotenv (transitiva)
                        "--ignore-vuln",
                        "CVE-2026-28684",
                        # pip (tool di build, non controllabile direttamente)
                        "--ignore-vuln",
                        "CVE-2026-1703",
                        "--ignore-vuln",
                        "CVE-2026-3219",
                        # pillow (CVE risolto in 12.2.0 ma audit potrebbe non rilevare)
                        "--ignore-vuln",
                        "CVE-2026-40192",
                    ],
                ),
                "pip_audit",
                False,
            ),
            (
                "Clean Code (Vulture)",
                cmd("vulture", [get_bin("vulture"), "src", "--min-confidence", "80"]),
                "vulture",
                True,
            ),
            (
                "Metrics (Radon MI)",
                cmd("radon", [get_bin("radon"), "mi", "src", "-s"]),
                "radon_mi",
                True,
            ),
            (
                "Metrics (Radon CC)",
                cmd("radon", [get_bin("radon"), "cc", "src", "-a", "-nc", "--min", "B"]),
                "radon_cc",
                True,
            ),
            (
                "Stats (Pygount)",
                cmd(
                    "pygount",
                    [get_bin("pygount"), "--suffix=py", "--format=summary", "src"],
                ),
                "pygount",
                True,
            ),
            (
                "Robust Tests",
                _run_tests_ai,
                "robust_tests",
                False,
            ),
        ]

        # Intelligence Checks
        if not self.target or self.target in ["all", "intelligence"]:
            if os.environ.get("TERM") == "dumb":
                ts = datetime.datetime.now().strftime("%H:%M:%S")
                console.print(f"[[dim]{ts}[/dim]] [bold yellow]⠴ Intelligence Scan...[/bold yellow]")
                self._add_res("Environment", *self._check_environment(), "env", False)
                self._add_res("Versions", *self._check_versions(), "ver", False)
                self._add_res("Secrets", *self._scan_for_secrets(), "sec", False)
                self._add_res("Database", *self._check_db_integrity(), "db", False)
            else:
                with Progress(
                    SpinnerColumn(spinner_name="dots"),
                    TextColumn("[progress.description]{task.description}"),
                    console=console,
                ) as prog:
                    prog.add_task("Intelligence Scan...", total=None)
                    self._add_res("Environment", *self._check_environment(), "env", False)
                    self._add_res("Versions", *self._check_versions(), "ver", False)
                    self._add_res("Secrets", *self._scan_for_secrets(), "sec", False)
                    self._add_res("Database", *self._check_db_integrity(), "db", False)

        # Filter Logic
        selected_checks = []
        if self.target == "security":
            selected_checks = [c for c in all_checks if c[2] in ["bandit", "pip_audit"]]
        elif self.target == "deps":
            selected_checks = [c for c in all_checks if c[2] in ["deptry"]]
        elif self.target == "metrics":
            selected_checks = [c for c in all_checks if c[2] in ["radon_mi", "radon_cc"]]
        elif self.target == "stats":
            selected_checks = [c for c in all_checks if c[2] in ["pygount"]]
        elif self.target == "clean":
            selected_checks = [c for c in all_checks if c[2] in ["vulture"]]
        elif self.target:
            selected_checks = [c for c in all_checks if self.target in c[2] or self.target in c[0].lower()]
        elif self.test_only:
            selected_checks = [c for c in all_checks if c[2] == "robust_tests"]
        else:  # Default (Full Audit)
            excluded = ["pygount", "vulture"]
            if self.fast:
                excluded.extend(["robust_tests", "refurb"])

            selected_checks = [c for c in all_checks if c[2] not in excluded]

        if not selected_checks and self.target:
            console.print(f"[bold red][X] Nessun check trovato per target: {self.target}[/bold red]")
            return

        self._run_parallel(selected_checks)

        if not self.target:  # Only show summary score if running full/default audit
            self.summary()

    def _add_res(self, label, success, msg, dur, name, always_show) -> None:  # noqa: PLR0913
        res = CheckResult(label, success, msg, dur, name)
        self.results.append(res)
        if not success:
            console.print(f"[bold red][X] {label} Fail ({dur:.2f}s)[/bold red]")
            if msg:
                console.print(Panel(msg[:800], border_style="red"))
        elif always_show and msg.strip():
            console.print(f"[bold green]i {label} Result ({dur:.2f}s)[/bold green]")
            console.print(Panel(msg.strip(), border_style="green", title=label))

    def summary(self) -> None:
        """Calcola lo score finale e visualizza il riepilogo tabellare dell'audit."""
        score = self._get_score()

        is_dumb = os.environ.get("TERM") == "dumb"
        if is_dumb:
            console.print("\n=== APEX PROJECT HEALTH SUMMARY ===")
            for r in self.results:
                status = "PASS" if r.success else "FAIL"
                console.print(f"- {r.label}: {status}")
            console.print(f"\nSYNCRO-SCORE: {score}/100\n")
        else:
            table = Table(title="Apex Project Health Summary", border_style="cyan")
            table.add_column("Audit Task", style="cyan")
            table.add_column("Status", justify="center")
            for r in self.results:
                table.add_row(
                    r.label,
                    "[green]PASS[/green]" if r.success else "[bold red]FAIL[/bold red]",
                )
            console.print("\n", table)
            console.print(
                Panel(
                    f"[bold cyan]🏆 SYNCRO-SCORE: {score}/100[/bold cyan]",
                    border_style="cyan",
                )
            )

        self._export_html(score)
        if score < 80 and not self.force:  # noqa: PLR2004
            sys.exit(1)

    def _get_score(self) -> int:
        score = 100
        weights = {
            "env": 10,
            "ver": 5,
            "sec": 10,
            "db": 10,
            "ruff": 10,
            "bandit": 15,
            "mypy": 10,
            "xenon": 5,
            "robust_tests": 25,
        }
        for r in self.results:
            if not r.success:
                score -= weights.get(r.name, 5)
        return max(0, score)

    def _export_html(self, score) -> None:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        rows = "".join(
            [
                f"<tr class='table-{'success' if r.success else 'danger'}'><td>{r.label}</td><td>{'PASS' if r.success else 'FAIL'}</td><td>{r.duration:.2f}s</td></tr>"
                for r in self.results
            ]
        )
        html = f"<html><head><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'></head><body class='p-5'><div class='container'><div class='card p-4 text-center'><h1>🚀 Apex Audit</h1><div class='display-1'>{score}</div><p>Project Score</p></div><table class='table mt-4'><thead><tr><th>Check</th><th>Status</th><th>Time</th></tr></thead><tbody>{rows}</tbody></table></div></body></html>"
        (REPORT_DIR / "dashboard.html").write_text(html, encoding="utf-8")
        console.print(f"[dim]Dashboard: {REPORT_DIR}/dashboard.html[/dim]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true")
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--inc", action="store_true")
    parser.add_argument("--test-only", action="store_true")
    parser.add_argument(
        "--target",
        type=str,
        help="Specify target check or category (security, metrics, clean, deps, stats)",
    )
    args = parser.parse_args()
    with contextlib.suppress(KeyboardInterrupt):
        ApexAudit(
            fix=args.fix,
            fast=args.fast,
            incremental=args.inc,
            test_only=args.test_only,
            target=args.target,
            force=args.force,
        ).run_all()
