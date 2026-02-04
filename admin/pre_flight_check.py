#!/usr/bin/env python3
"""
🚀 SyncroJob Master Developer Tool & Pre-Flight Check (Apex Edition)
====================================================================
L'Oracolo del Progetto: Score, Dashboard HTML, Git-Hooks e Intelligence.
"""

import argparse
import datetime
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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
    print("❌ Rich non installato. Esegui 'python -m pip install rich' prima.")
    sys.exit(1)

# Configurazione Base
PROJECT_ROOT = Path(__file__).parent.parent
LOG_DIR = PROJECT_ROOT / "temp" / "logs"
REPORT_DIR = PROJECT_ROOT / "reports" / "preflight"
VENV_BIN = (
    PROJECT_ROOT / ".venv" / "Scripts"
    if sys.platform == "win32"
    else PROJECT_ROOT / ".venv" / "bin"
)

console = Console()

class CheckResult:
    def __init__(self, label: str, success: bool, msg: str, duration: float, name: str):
        self.label = label
        self.success = success
        self.msg = msg
        self.duration = duration
        self.name = name
        self.timestamp = datetime.datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

def get_bin(name):
    """Recupera il percorso dell'eseguibile nel venv o nei path standard di Python."""
    ext = ".exe" if sys.platform == "win32" else ""
    
    # 1. Prova nel VENV
    venv_path = VENV_BIN / f"{name}{ext}"
    if venv_path.exists():
        return str(venv_path)
    
    # 2. Prova in APPDATA (Windows fallback per installazioni --user)
    if sys.platform == "win32":
        appdata_path = Path(os.environ.get("APPDATA", "")) / "Python" / "Python312" / "Scripts" / f"{name}{ext}"
        if appdata_path.exists():
            return str(appdata_path)
            
    return name

def run_tool(name: str, cmd: List[str], label: str, cwd=PROJECT_ROOT) -> Tuple[bool, str, float]:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"{name}.log"
    start_t = time.time()
    try:
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
        duration = time.time() - start_t
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"CMD: {' '.join(cmd)}\nEXIT: {result.returncode}\n{'='*40}\n{result.stdout}\n{'='*40}\n{result.stderr}")
        return (result.returncode == 0), result.stdout if result.returncode != 0 else "", duration
    except Exception as e:
        return False, f"Eccezione: {e}", time.time() - start_t

# --- APEX ENGINE ---

class ApexAudit:
    def __init__(self, fix=False, fast=False, incremental=False, test_only=False):
        self.fix = fix
        self.fast = fast
        self.incremental = incremental
        self.test_only = test_only
        self.results: List[CheckResult] = []
        self.start_time = time.time()
        self.changed_files = self._get_changed_files() if incremental else []

    def _get_changed_files(self) -> List[str]:
        try:
            cmd = ["git", "diff", "HEAD", "--name-only"]
            res = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)
            return [f for f in res.stdout.splitlines() if f.endswith(".py") and Path(f).exists()]
        except Exception: return []

    def _check_environment(self) -> Tuple[bool, str, float]:
        start_t = time.time()
        try:
            if sys.platform == "win32":
                res = subprocess.run(["reg", "query", r"HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon", "/v", "version"], capture_output=True, text=True)
                c_ver = re.search(r"REG_SZ\s+([\d\.]+)", res.stdout).group(1) if "REG_SZ" in res.stdout else "N/A"
            else:
                res = subprocess.run(["google-chrome", "--version"], capture_output=True, text=True)
                c_ver = re.search(r"([\d\.]+)", res.stdout).group(1) if res.returncode == 0 else "N/A"
            d_res = subprocess.run(["chromedriver", "--version"], capture_output=True, text=True)
            d_ver = re.search(r"([\d\.]+)", d_res.stdout).group(1) if d_res.returncode == 0 else "N/A"
            return True, f"Chrome:{c_ver} Driver:{d_ver}", time.time() - start_t
        except Exception: return False, "Env check failed", time.time() - start_t

    def _check_versions(self) -> Tuple[bool, str, float]:
        start_t = time.time()
        try:
            pyproject = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
            v_toml = re.search(r'version\s*=\s*"(.*?)"', pyproject).group(1)
            v_code = re.search(r'__version__\s*=\s*"(.*?)"', (PROJECT_ROOT / "src/core/version.py").read_text(encoding="utf-8")).group(1)
            return (v_toml == v_code), f"v{v_toml}", time.time() - start_t
        except Exception: return False, "Version mismatch", time.time() - start_t

    def _check_db_integrity(self) -> Tuple[bool, str, float]:
        start_t = time.time()
        from platformdirs import user_data_dir
        data_dir = Path(user_data_dir("SyncroJob", appauthor=False)) / "data"
        if not data_dir.exists(): return True, "No DBs", time.time() - start_t
        errors = []
        for db in data_dir.glob("*.db"):
            try:
                with sqlite3.connect(db) as conn:
                    if conn.execute("PRAGMA integrity_check;").fetchone()[0] != "ok": errors.append(db.name)
            except Exception: errors.append(db.name)
        return (not errors), f"Checked {len(list(data_dir.glob('*.db')))} DBs", time.time() - start_t

    def _scan_for_secrets(self) -> Tuple[bool, str, float]:
        start_t = time.time()
        patterns = { "Key": r"(?:api_key|token)[\"']?\s*[:=]\s*[\"']([A-Za-z0-9_\-]{16,})[\"']" }
        found = []
        for path in (PROJECT_ROOT / "src").rglob("*.py"):
            try:
                content = path.read_text(encoding="utf-8")
                if any(re.search(p, content, re.I) for p in patterns.values()): found.append(path.name)
            except Exception: continue
        return (not found), "No secrets found" if not found else f"Secrets in {found[0]}", time.time() - start_t

    def _run_parallel(self, parallel_checks):
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TimeElapsedColumn(), console=console) as prog:
            tasks = {label: prog.add_task(f"Audit {label}...", total=100) for label, _, _ in parallel_checks}
            with ThreadPoolExecutor(max_workers=len(parallel_checks)) as executor:
                futures = {executor.submit(func): (label, name) for label, func, name in parallel_checks}
                for future in futures:
                    label, name = futures[future]
                    success, msg, dur = future.result()
                    self._add_res(label, success, msg, dur, name)
                    prog.update(tasks[label], completed=100, description=f"[green]✅ {label}")

    def run_all(self):
        console.print(Panel.fit("[bold cyan]💎 SYNCROJOB APEX AUDIT ENGINE[/bold cyan]", border_style="cyan"))

        if self.test_only:
            parallel_checks = [("Robust Tests", lambda: run_tool("pytest", [sys.executable, str(PROJECT_ROOT / "tests" / "run_robust_tests.py"), "--reset"], "pytest"), "pytest")]
            self._run_parallel(parallel_checks)
            self.summary()
            return

        # 1. Intelligence
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as prog:
            prog.add_task("Intelligence Scan...", total=None)
            self._add_res("Environment", *self._check_environment(), "env")
            self._add_res("Versions", *self._check_versions(), "ver")
            self._add_res("Secrets", *self._scan_for_secrets(), "sec")
            self._add_res("Database", *self._check_db_integrity(), "db")

        # 2. Parallel Analysis
        targets = self.changed_files if self.incremental and self.changed_files else ["."]
        parallel_checks = [
            ("Lint (Ruff)", lambda: run_tool("ruff", [get_bin("ruff"), "check"] + targets + (["--fix"] if self.fix else []), "ruff"), "ruff"),
            ("Security (Bandit)", lambda: run_tool("bandit", [get_bin("bandit"), "-r", "src/", "-ll", "-q"], "bandit"), "bandit"),
            ("Types (Mypy)", lambda: run_tool("mypy", ["src", "--ignore-missing-imports"], "mypy"), "mypy"),
            ("Complexity (Xenon)", lambda: run_tool("xenon", [get_bin("xenon"), "-a", "B", "src"], "xenon"), "xenon"),
            ("Modernize (Refurb)", lambda: run_tool("refurb", [get_bin("refurb"), "src"], "refurb"), "refurb"),
            ("Typos (Codespell)", lambda: run_tool("codespell", [get_bin("codespell"), "src"], "codespell"), "codespell"),
            ("Docs (Interrogate)", lambda: run_tool("interrogate", [get_bin("interrogate"), "src", "-q"], "interrogate"), "interrogate"),
            ("Deps (Deptry)", lambda: run_tool("deptry", [get_bin("deptry"), "."], "deptry"), "deptry"),
            ("Vulnerabilities", lambda: run_tool("pip_audit", [get_bin("pip-audit"), "--desc", "off"], "pip_audit"), "pip_audit"),
        ]

        if not self.fast:
            parallel_checks.append(("Robust Tests", lambda: run_tool("pytest", [sys.executable, str(PROJECT_ROOT / "tests" / "run_robust_tests.py"), "--reset"], "pytest"), "pytest"))

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn(), TimeElapsedColumn(), console=console) as prog:
            tasks = {label: prog.add_task(f"Audit {label}...", total=100) for label, _, _ in parallel_checks}
            with ThreadPoolExecutor(max_workers=len(parallel_checks)) as executor:
                futures = {executor.submit(func): (label, name) for label, func, name in parallel_checks}
                for future in futures:
                    label, name = futures[future]
                    success, msg, dur = future.result()
                    self._add_res(label, success, msg, dur, name)
                    prog.update(tasks[label], completed=100, description=f"[green]✅ {label}")

        self.summary()

    def _add_res(self, label, success, msg, dur, name):
        res = CheckResult(label, success, msg, dur, name)
        self.results.append(res)
        if not success:
            console.print(f"[bold red]❌ {label} Fail ({dur:.2f}s)[/bold red]")
            if msg: console.print(Panel(msg[:500], border_style="red"))

    def summary(self):
        score = self._get_score()
        table = Table(title="Apex Project Health Summary", border_style="cyan")
        table.add_column("Audit Task", style="cyan"); table.add_column("Status", justify="center")
        for r in self.results: table.add_row(r.label, "[green]PASS[/green]" if r.success else "[bold red]FAIL[/bold red]")
        console.print("\n", table)
        console.print(Panel(f"[bold cyan]🏆 SYNCRO-SCORE: {score}/100[/bold cyan]", border_style="cyan"))
        
        self._export_html(score)
        if score < 80: sys.exit(1)

    def _get_score(self) -> int:
        score = 100
        weights = {"env":10, "ver":5, "sec":10, "db":10, "ruff":10, "bandit":15, "mypy":10, "xenon":5, "pytest":25}
        for r in self.results:
            if not r.success: score -= weights.get(r.name, 5)
        return max(0, score)

    def _export_html(self, score):
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        rows = "".join([f"<tr class='table-{'success' if r.success else 'danger'}'><td>{r.label}</td><td>{'PASS' if r.success else 'FAIL'}</td><td>{r.duration:.2f}s</td></tr>" for r in self.results])
        html = f"<html><head><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'></head><body class='p-5'><div class='container'><div class='card p-4 text-center'><h1>🚀 Apex Audit</h1><div class='display-1'>{score}</div><p>Project Score</p></div><table class='table mt-4'><thead><tr><th>Check</th><th>Status</th><th>Time</th></tr></thead><tbody>{rows}</tbody></table></div></body></html>"
        (REPORT_DIR / "dashboard.html").write_text(html, encoding="utf-8")
        console.print(f"[dim]Dashboard: {REPORT_DIR}/dashboard.html[/dim]")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true")
    parser.add_argument("--fast", action="store_true")
    parser.add_argument("--inc", action="store_true")
    parser.add_argument("--test-only", action="store_true")
    args = parser.parse_args()
    ApexAudit(fix=args.fix, fast=args.fast, incremental=args.inc, test_only=args.test_only).run_all()
