#!/usr/bin/env python3
"""
🚀 SyncroJob Master Developer Tool & Pre-Flight Check (Rich Edition)
====================================================================
Suite di controllo qualità, sicurezza e integrità potenziata con Rich.
Tool: Ruff, Bandit, Interrogate, Pytest, Mypy, Xenon, Vulture, Codespell, Deptry, Pip-Audit.
"""

import argparse
import io
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import List, Tuple

# Rich Imports
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
except ImportError:
    print("❌ Rich non installato. Esegui 'poetry install' prima.")
    sys.exit(1)

# Configurazione Base
PROJECT_ROOT = Path(__file__).parent.parent
LOG_DIR = PROJECT_ROOT / "temp" / "logs"
VENV_BIN = (
    PROJECT_ROOT / ".venv" / "Scripts"
    if sys.platform == "win32"
    else PROJECT_ROOT / ".venv" / "bin"
)

console = Console()


def get_bin(name):
    """Recupera il percorso dell'eseguibile nel venv."""
    ext = ".exe" if sys.platform == "win32" else ""
    venv_path = VENV_BIN / f"{name}{ext}"
    return str(venv_path) if venv_path.exists() else name


def run_tool(
    name: str, cmd: List[str], label: str, cwd=PROJECT_ROOT
) -> Tuple[bool, str, float]:
    """Esegue un tool e restituisce (successo, output, durata)."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"{name}.log"
    start_t = time.time()

    try:
        # Esecuzione subprocess
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )
        duration = time.time() - start_t

        # Scrittura Log
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(f"CMD: {' '.join(cmd)}\n")
            f.write(f"EXIT: {result.returncode}\n")
            f.write("=" * 40 + "\n")
            f.write(result.stdout)
            f.write("\n" + "=" * 40 + "\n")
            f.write(result.stderr)

        if result.returncode == 0:
            return True, "", duration

        # Preparazione Sommario Errore
        output = result.stdout if result.stdout.strip() else result.stderr
        lines = output.splitlines()
        summary = "\n".join(lines[:15])
        if len(lines) > 15:
            summary += f"\n... (vedi {log_file.name} per altri {len(lines) - 15} righe)"

        return False, summary, duration

    except Exception as e:
        return False, f"Eccezione critica: {e}", time.time() - start_t


def check_versions() -> Tuple[bool, str, float]:
    """Verifica sincronizzazione versioni."""
    start_t = time.time()
    try:
        v_toml = re.search(
            r'version\s*=\s*"(.*?)"',
            (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"),
        ).group(1)
        v_code = re.search(
            r'__version__\s*=\s*"(.*?)"',
            (PROJECT_ROOT / "src/core/version.py").read_text(encoding="utf-8"),
        ).group(1)

        duration = time.time() - start_t
        if v_toml == v_code:
            return True, f"v{v_toml}", duration
        return False, f"Discrepanza! TOML: {v_toml} != CODE: {v_code}", duration
    except Exception as e:
        return False, str(e), time.time() - start_t


def sync_requirements() -> Tuple[bool, str, float]:
    """Sincronizza requirements.txt."""
    script = PROJECT_ROOT / "admin" / "sync_requirements.py"
    return run_tool("sync_req", [sys.executable, str(script)], "Requirements")


# --- WRAPPER TOOL ---


def run_ruff(fix=False):
    cmd = [get_bin("ruff"), "check", ".", "--fix" if fix else ""]
    cmd = [c for c in cmd if c]
    success, out, dur = run_tool("ruff_check", cmd, "Ruff Lint")
    if not success:
        return False, out, dur

    fmt_cmd = [get_bin("ruff"), "format", ".", "--check" if not fix else ""]
    fmt_cmd = [c for c in fmt_cmd if c]
    s2, o2, d2 = run_tool("ruff_format", fmt_cmd, "Ruff Format")
    return s2, o2, dur + d2


def run_mypy():
    cmd = [get_bin("mypy"), "src", "--ignore-missing-imports", "--no-error-summary"]
    return run_tool("mypy", cmd, "Mypy Types")


def run_bandit():
    cmd = [get_bin("bandit"), "-r", "src/", "-ll", "-q"]
    return run_tool("bandit", cmd, "Bandit Security")


def run_xenon():
    cmd = [
        get_bin("xenon"),
        "--max-absolute",
        "C",
        "--max-modules",
        "B",
        "--max-average",
        "A",
        "src",
    ]
    return run_tool("xenon", cmd, "Xenon Complexity")


def run_vulture():
    cmd = [get_bin("vulture"), "src", "--min-confidence", "80"]
    return run_tool("vulture", cmd, "Vulture Dead Code")


def run_codespell():
    cmd = [get_bin("codespell")]
    return run_tool("codespell", cmd, "Codespell Typos")


def run_interrogate():
    cmd = [get_bin("interrogate"), ".", "-q"]
    return run_tool("interrogate", cmd, "Interrogate Docs")


def run_deptry():
    """Verifica dipendenze inutilizzate o mancanti."""
    cmd = [get_bin("deptry"), "."]
    return run_tool("deptry", cmd, "Deptry Dependencies")


def run_pip_audit():
    """Verifica vulnerabilità nelle dipendenze installate."""
    # --desc stampa la descrizione della vuln, --progress-spinner=off pulisce l'output
    cmd = [get_bin("pip-audit"), "--desc", "--progress-spinner", "off"]
    return run_tool("pip_audit", cmd, "Pip-Audit Vulnerabilities")


def run_tests():
    runner = PROJECT_ROOT / "tests" / "run_robust_tests.py"
    cmd = [sys.executable, str(runner), "--reset", "--exitfirst"]
    return run_tool("pytest", cmd, "Pytest Suite")


# --- MAIN EXECUTION ---


def main():
    # Fix encoding windows
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    parser = argparse.ArgumentParser(description="SyncroJob Developer Toolbox")
    parser.add_argument("--fix", action="store_true", help="Applica fix automatici")
    parser.add_argument("--fast", action="store_true", help="Salta i test lenti")
    parser.add_argument("--test-only", action="store_true", help="Solo test")
    parser.add_argument(
        "--super-audit", action="store_true", help="Audit completo + bump"
    )
    parser.add_argument("--force", action="store_true", help="Ignora errori")
    args = parser.parse_args()

    # Header
    console.print(
        Panel.fit(
            "[bold yellow]🚀 SYNCROJOB ENTERPRISE PRE-FLIGHT CHECK[/bold yellow]\n"
            "[italic]Quality, Security, Integrity & Documentation[/italic]",
            border_style="blue",
        )
    )

    # Definizione Controlli
    checks = []

    if args.test_only:
        checks.append(("🧪 Testing", run_tests))
    else:
        # Fase 1: Integrità
        checks.append(("📦 Versions", lambda: check_versions()))
        checks.append(("🔄 Requirements", lambda: sync_requirements()))
        checks.append(("📦 Dependencies (Deptry)", lambda: run_deptry()))

        # Fase 2: Qualità Codice
        checks.append(("✨ Lint & Format (Ruff)", lambda: run_ruff(args.fix)))
        checks.append(("🔤 Typos (Codespell)", lambda: run_codespell()))
        checks.append(("📐 Types (Mypy)", lambda: run_mypy()))
        checks.append(("🧠 Complexity (Xenon)", lambda: run_xenon()))
        checks.append(("💀 Dead Code (Vulture)", lambda: run_vulture()))
        checks.append(("📝 Documentation (Interrogate)", lambda: run_interrogate()))

        # Fase 3: Sicurezza
        checks.append(("🛡️ SAST Security (Bandit)", lambda: run_bandit()))
        checks.append(("🦠 Dependency Vulns (Pip-Audit)", lambda: run_pip_audit()))

        # Fase 4: Test (se non fast)
        if not args.fast:
            checks.append(("🧪 Unit Tests", lambda: run_tests()))

    # Esecuzione
    results = []
    overall_success = True

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for label, func in checks:
            task_id = progress.add_task(f"Esecuzione {label}...", total=None)
            success, msg, duration = func()
            progress.remove_task(task_id)

            status_icon = "✅" if success else "❌"
            status_style = "green" if success else "bold red"

            results.append(
                {"label": label, "success": success, "msg": msg, "duration": duration}
            )

            if not success:
                overall_success = False
                console.print(
                    f"[{status_style}]{status_icon} {label} fallito in {duration:.2f}s[/{status_style}]"
                )
                console.print(Panel(msg, title=f"Errore: {label}", border_style="red"))
                if not args.force:
                    break
            else:
                console.print(f"[green]✅ {label} completato ({duration:.2f}s)[/green]")

    # Riepilogo Finale
    console.print("\n")
    table = Table(title="Riepilogo Pre-Flight Check", border_style="blue")
    table.add_column("Controllo", style="cyan")
    table.add_column("Stato", justify="center")
    table.add_column("Tempo", justify="right")

    for r in results:
        status = "[green]PASS[/green]" if r["success"] else "[bold red]FAIL[/bold red]"
        table.add_row(r["label"], status, f"{r['duration']:.2f}s")

    console.print(table)

    if overall_success or args.force:
        console.print(
            Panel(
                "[bold green]✨ SISTEMA PRONTO AL DECOLLO![/bold green]",
                border_style="green",
            )
        )
        sys.exit(0)
    else:
        console.print(
            Panel(
                "[bold red]⛔ CONTROLLI FALLITI - REVISIONE NECESSARIA[/bold red]",
                border_style="red",
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
