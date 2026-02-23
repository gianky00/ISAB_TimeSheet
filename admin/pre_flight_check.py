#!/usr/bin/env python3
"""
SyncroJob Master Developer Tool & Pre-Flight Check (Apex Edition)
====================================================================
L'Oracolo del Progetto: Score, Dashboard HTML, Git-Hooks e Intelligence.
"""

import argparse
import contextlib
import datetime
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
LOG_DIR = PROJECT_ROOT / "temp" / "logs"
REPORT_DIR = PROJECT_ROOT / "reports" / "preflight"
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

    def __init__(self, label: str, success: bool, msg: str, duration: float, name: str):
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
    """
    Recupera il percorso dell'eseguibile nel venv o nei path standard di Python.

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
    """
    Esegue uno strumento esterno registrando l'output in un file di log dedicato.

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
        )
        duration = time.time() - start_t
        log_file.write_text(
            f"CMD: {' '.join(cmd)}\nEXIT: {result.returncode}\n{'=' * 40}\n{result.stdout}\n{'=' * 40}\n{result.stderr}",
            encoding="utf-8",
        )
        return (
            (result.returncode == 0),
            result.stdout if result.returncode != 0 else "",
            duration,
        )
    except Exception as e:
        return False, f"Eccezione: {e}", time.time() - start_t


# --- APEX ENGINE ---


class ApexAudit:
    """Motore di audit principale che esegue una suite completa di test e controlli statici."""

    def __init__(
        self,
        fix=False,
        fast=False,
        incremental=False,
        test_only=False,
        target: str | None = None,
        force=False,
    ):
        """Inizializza l'audit configurando le modalità di esecuzione."""
        self.fix = fix
        self.fast = fast
        self.incremental = incremental
        self.test_only = test_only
        self.target = target.lower() if target else None
        self.force = force
        self.results: list[CheckResult] = []
        self.start_time = time.time()
        self.changed_files = self._get_changed_files() if incremental else []

    def _get_changed_files(self) -> list[str]:
        try:
            cmd = ["git", "diff", "HEAD", "--name-only"]
            res = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT, check=False)
            return [f for f in res.stdout.splitlines() if f.endswith(".py") and Path(f).exists()]
        except Exception:
            return []

    def _check_environment(self) -> tuple[bool, str, float]:
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
                (PROJECT_ROOT / "src/core/version.py").read_text(encoding="utf-8"),
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

    def _run_parallel(self, parallel_checks):
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

    def run_all(self):
        console.print(
            Panel.fit(
                "[bold cyan]SYNCROJOB APEX AUDIT ENGINE[/bold cyan]",
                border_style="cyan",
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
                cmd("bandit", [get_bin("bandit"), "-r", "src/", "-ll", "-q"]),
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
                        "--ignore-vuln",
                        "CVE-2025-69872",  # diskcache: no fix version yet
                        "--ignore-vuln",
                        "PYSEC-2022-42969",  # py: legacy dev dependency
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
                cmd(
                    "pytest",
                    [
                        sys.executable,
                        str(PROJECT_ROOT / "tests" / "run_robust_tests.py"),
                        "--reset",
                    ],
                ),
                "pytest",
                False,
            ),
        ]

        # Intelligence Checks
        if not self.target or self.target in ["all", "intelligence"]:
            # Usa spinner ASCII-only se TERM=dumb (eseguito da GUI)
            spinner_type = "dots"

            with Progress(
                SpinnerColumn(spinner_name=spinner_type),
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
            selected_checks = [c for c in all_checks if c[2] == "pytest"]
        else:  # Default (Full Audit)
            excluded = ["radon_mi", "radon_cc", "pygount", "vulture"]
            if self.fast:
                excluded.append("pytest")

            selected_checks = [c for c in all_checks if c[2] not in excluded]

        if not selected_checks and self.target:
            console.print(f"[bold red][X] Nessun check trovato per target: {self.target}[/bold red]")
            return

        self._run_parallel(selected_checks)

        if not self.target:  # Only show summary score if running full/default audit
            self.summary()

    def _add_res(self, label, success, msg, dur, name, always_show):
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
        if score < 80 and not self.force:
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
            "pytest": 25,
        }
        for r in self.results:
            if not r.success:
                score -= weights.get(r.name, 5)
        return max(0, score)

    def _export_html(self, score):
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
