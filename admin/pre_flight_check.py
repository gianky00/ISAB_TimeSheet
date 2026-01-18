#!/usr/bin/env python3
"""
🚀 SyncroJob Master Developer Tool & Pre-Flight Check
===================================================
Gestione avanzata della qualità con output sintetico per AI.
Tool: Ruff, Bandit, Interrogate, Pytest, Mypy, Xenon, Vulture, Codespell.
"""

import argparse
import io
import re
import subprocess
import sys
import time
from pathlib import Path

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

PROJECT_ROOT = Path(__file__).parent.parent
LOG_DIR = PROJECT_ROOT / "temp" / "logs"
VENV_BIN = (
    PROJECT_ROOT / ".venv" / "Scripts"
    if sys.platform == "win32"
    else PROJECT_ROOT / ".venv" / "bin"
)


def print_step(msg):
    print(f"\n{BOLD}{CYAN}🔹 {msg}{RESET}")


def print_ok(msg):
    print(f"{GREEN}✅ {msg}{RESET}")


def print_fail(msg):
    print(f"{RED}❌ {msg}{RESET}")


def get_bin(name):
    ext = ".exe" if sys.platform == "win32" else ""
    venv_path = VENV_BIN / f"{name}{ext}"
    return str(venv_path) if venv_path.exists() else name


def run_tool(name, cmd, cwd=PROJECT_ROOT):
    """Esegue un tool, cattura l'output e mostra solo un sommario in caso di errore."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / f"{name}.log"

    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
        )

        with open(log_file, "w", encoding="utf-8") as f:
            f.write(result.stdout)
            f.write("\n" + "=" * 40 + "\n")
            f.write(result.stderr)

        if result.returncode == 0:
            return True, ""

        output = result.stdout if result.stdout.strip() else result.stderr
        lines = output.splitlines()
        summary = "\n".join(lines[:12])
        if len(lines) > 12:
            summary += f"\n... (altre {len(lines) - 12} righe nel log: {log_file.name})"

        return False, summary
    except Exception as e:
        return False, f"Eccezione durante l'esecuzione: {e}"


def check_versions():
    print_step("VERSIONI: Verifica allineamento pyproject.toml vs code...")
    try:
        v_toml = re.search(
            r'version\s*=\s*"(.*?)"',
            (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8"),
        ).group(1)
        v_code = re.search(
            r'__version__\s*=\s*"(.*?)"',
            (PROJECT_ROOT / "src/core/version.py").read_text(encoding="utf-8"),
        ).group(1)
        if v_toml == v_code:
            print_ok(f"Sincronizzate: {v_toml}")
            return True
        print_fail(f"Discrepanza! TOML: {v_toml}, CODE: {v_code}")
        return False
    except Exception as e:
        print_fail(f"Errore lettura versioni: {e}")
        return False


def run_ruff(fix=False):
    print_step("RUFF: Controllo Qualità e Formattazione...")
    cmd = [get_bin("ruff"), "check", ".", "--fix" if fix else ""]
    cmd = [c for c in cmd if c]
    success, output = run_tool("ruff_check", cmd)
    if not success:
        print_fail("Problemi Ruff (Linter):")
        print(output)
        return False

    fmt_cmd = [get_bin("ruff"), "format", ".", "--check" if not fix else ""]
    fmt_cmd = [c for c in fmt_cmd if c]
    success, output = run_tool("ruff_format", fmt_cmd)
    if not success:
        print_fail("Problemi Ruff (Formatter):")
        print(output)
        return False

    print_ok("Codice pulito e formattato.")
    return True


def run_mypy():
    print_step("MYPY: Controllo Statico dei Tipi...")
    cmd = [get_bin("mypy"), "src", "--ignore-missing-imports", "--no-error-summary"]
    success, output = run_tool("mypy", cmd)
    if success:
        print_ok("Nessun errore di tipizzazione trovato.")
        return True
    print_fail("Rilevati errori di tipo:")
    print(output)
    return False


def run_bandit():
    print_step("BANDIT: Analisi Sicurezza...")
    cmd = [get_bin("bandit"), "-r", "src/", "-ll", "-q"]
    success, output = run_tool("bandit", cmd)
    if success:
        print_ok("Sicurezza verificata.")
        return True
    print_fail("Potenziali falle di sicurezza:")
    print(output)
    return False


def run_xenon():
    print_step("XENON: Analisi Complessità...")
    # Ripristiniamo il rigore: Grado B come limite massimo per tutto
    cmd = [
        get_bin("xenon"),
        "--max-absolute",
        "B",
        "--max-modules",
        "B",
        "--max-average",
        "A",
        "src",
    ]
    success, output = run_tool("xenon", cmd)
    if success:
        print_ok("Codice manutenibile.")
        return True
    print_fail("Codice troppo complesso:")
    print(output)
    return False


def run_vulture():
    print_step("VULTURE: Ricerca Codice Morto...")
    cmd = [get_bin("vulture"), "src", "--min-confidence", "80"]
    success, output = run_tool("vulture", cmd)
    if success:
        print_ok("Nessun codice morto rilevato.")
        return True
    print_fail("Trovato potenziale codice inutilizzato:")
    print(output)
    return False


def run_codespell():
    print_step("CODESPELL: Controllo battitura...")
    cmd = [get_bin("codespell")]
    success, output = run_tool("codespell", cmd)
    if success:
        print_ok("Battitura corretta.")
        return True
    print_fail("Errori di battitura rilevati:")
    print(output)
    return False


def run_interrogate():
    print_step("INTERROGATE: Copertura Docstring...")
    cmd = [get_bin("interrogate"), ".", "-q"]
    success, output = run_tool("interrogate", cmd)
    if success:
        print_ok("Documentazione presente.")
        return True
    print_fail("Mancano docstring:")
    print(output)
    return False


def run_tests():
    print_step("PYTEST: Esecuzione Test Suite...")
    runner = PROJECT_ROOT / "tests" / "run_robust_tests.py"
    # Per i test lasciamo l'output visibile perché è già filtrato dal nostro runner robusto
    ret = subprocess.call(
        [sys.executable, str(runner), "--reset", "--exitfirst"], cwd=PROJECT_ROOT
    )
    return ret == 0


def sync_requirements():
    print_step("REQUIREMENTS: Sincronizzazione...")
    script = PROJECT_ROOT / "admin" / "sync_requirements.py"
    success, _ = run_tool("sync_req", [sys.executable, str(script)])
    return success


def run_super_audit():
    """Automatizza il ciclo di vita completo di un audit di qualita."""

    print_step("SUPER AUDIT: Inizio processo automatizzato...")

    timestamp = time.strftime("%Y%m%d_%H%M%S")

    branch_name = f"audit/quality_{timestamp}"

    # 1. Crea branch

    print(f"🔹 Creazione branch: {branch_name}")

    subprocess.call(["git", "checkout", "-b", branch_name], cwd=PROJECT_ROOT)

    # 2. Esegue controlli

    print("🔹 Esecuzione controlli qualità...")

    # Qui chiamiamo la logica main internamente

    # (Per semplicita' usiamo subprocess per isolare l'esecuzione)

    ret = subprocess.call([sys.executable, __file__, "--fast"], cwd=PROJECT_ROOT)

    if ret != 0:
        print_fail("Audit fallito. Risolvi i problemi sul branch corrente.")

        return False

    # 3. Aggiornamento Versione (Auto-patch)

    print("🔹 Incremento versione (patch)...")

    subprocess.call(
        [sys.executable, "admin/bump_version.py", "patch"], cwd=PROJECT_ROOT
    )

    # 4. Git operations

    print("🔹 Finalizzazione release e merge su main...")

    subprocess.call(["git", "add", "."], cwd=PROJECT_ROOT)

    subprocess.call(
        [
            "git",
            "commit",
            "-m",
            f"CHORE: automated quality audit and version bump {timestamp}",
        ],
        cwd=PROJECT_ROOT,
    )

    subprocess.call(["git", "checkout", "main"], cwd=PROJECT_ROOT)

    subprocess.call(["git", "merge", branch_name], cwd=PROJECT_ROOT)

    subprocess.call(["git", "branch", "-D", branch_name], cwd=PROJECT_ROOT)

    print_ok("SUPER AUDIT COMPLETATO CON SUCCESSO!")

    return True


def main():
    # Fix encoding for Windows console to support emoji
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

    parser = argparse.ArgumentParser(description="SyncroJob Developer Toolbox")

    parser.add_argument(
        "--fix", action="store_true", help="Applica correzioni automatiche"
    )

    parser.add_argument("--fast", action="store_true", help="Salta i test")

    parser.add_argument("--test-only", action="store_true", help="Esegue solo i test")

    parser.add_argument(
        "--super-audit",
        action="store_true",
        help="Esegue il ciclo completo di audit e upgrade",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Forza il successo anche in caso di errori (per deploy urgenti)",
    )

    args = parser.parse_args()

    if args.super_audit:
        if run_super_audit():
            sys.exit(0)

        sys.exit(1)

    start_time = time.time()

    print(f"\n{BOLD}{YELLOW}🚀 SYNCROJOB MASTER CHECK (Versione AI-Safe){RESET}")
    print(f"{'=' * 60}")

    if args.test_only:
        success = run_tests()
    else:
        checks = [
            (check_versions, []),
            (sync_requirements, []),
            (run_ruff, [args.fix]),
            (run_codespell, []),
            (run_mypy, []),
            (run_bandit, []),
            (run_xenon, []),
            (run_vulture, []),
            (run_interrogate, []),
        ]
        if not args.fast:
            checks.append((run_tests, []))

        success = True
        for func, f_args in checks:
            if not func(*f_args):
                success = False
                print(f"\n{RED}🛑 Bloccato al passaggio: {func.__name__}{RESET}")
                if not args.force:
                    break
                else:
                    print(f"{YELLOW}⚠️ FORCE ACTIVE: Ignoro errore e continuo...{RESET}")

    duration = time.time() - start_time
    print(f"\n{'=' * 50}")
    if success or args.force:
        print(f"{GREEN}{BOLD}✨ TUTTI I CONTROLLI SUPERATI! ({duration:.1f}s){RESET}")
        if not success and args.force:
            print(f"{YELLOW}⚠️ ATTENZIONE: Check passati con --force.{RESET}")
        sys.exit(0)
    else:
        print(f"{RED}{BOLD}❌ QUALITÀ NON SUFFICIENTE.{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
