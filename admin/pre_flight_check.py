#!/usr/bin/env python3
"""
🚀 SyncroJob Developer Toolbox & Pre-Flight Check
================================================
Un unico entry point per tutti i controlli di qualità, sicurezza e integrità.
Tool integrati: Ruff, Bandit, Interrogate, Pytest, Pre-commit.
"""

import argparse
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
    """Restituisce il percorso dell'eseguibile nel venv o nel sistema."""
    ext = ".exe" if sys.platform == "win32" else ""
    venv_path = VENV_BIN / f"{name}{ext}"
    return str(venv_path) if venv_path.exists() else name


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
    ret = subprocess.call(cmd, cwd=PROJECT_ROOT)

    # Formattazione
    subprocess.call(
        [get_bin("ruff"), "format", ".", "--check" if not fix else ""], cwd=PROJECT_ROOT
    )

    if ret == 0:
        print_ok("Codice pulito.")
        return True
    return False


def run_bandit():
    print_step("BANDIT: Analisi Sicurezza...")
    cmd = [get_bin("bandit"), "-r", "src/", "-ll", "-q"]
    ret = subprocess.call(cmd, cwd=PROJECT_ROOT)
    if ret == 0:
        print_ok("Nessuna vulnerabilità critica rilevata.")
        return True
    print_fail("Rilevati potenziali problemi di sicurezza.")
    return False


def run_interrogate():
    print_step("INTERROGATE: Copertura Documentazione...")
    cmd = [get_bin("interrogate"), ".", "-q"]
    ret = subprocess.call(cmd, cwd=PROJECT_ROOT)
    if ret == 0:
        print_ok("Documentazione adeguata.")
        return True
    print_fail("Mancano docstring in alcune parti del codice.")
    return False


def run_tests():
    print_step("PYTEST: Esecuzione Test Suite (Robust Mode)...")
    runner = PROJECT_ROOT / "tests" / "run_robust_tests.py"
    cmd = [sys.executable, str(runner), "--reset", "--exitfirst"]
    ret = subprocess.call(cmd, cwd=PROJECT_ROOT)
    return ret == 0


def run_pre_commit():
    print_step("PRE-COMMIT: Validazione finale hook...")
    cmd = [get_bin("pre-commit"), "run", "--all-files"]
    ret = subprocess.call(cmd, cwd=PROJECT_ROOT)
    return ret == 0


def sync_requirements():
    print_step("REQUIREMENTS: Sincronizzazione requirements.txt...")
    script = PROJECT_ROOT / "admin" / "sync_requirements.py"
    ret = subprocess.call([sys.executable, str(script)], cwd=PROJECT_ROOT)
    return ret == 0


def main():
    parser = argparse.ArgumentParser(description="SyncroJob Master Developer Tool")
    parser.add_argument(
        "--fix", action="store_true", help="Applica correzioni automatiche (Ruff)"
    )
    parser.add_argument("--fast", action="store_true", help="Salta i test pesanti")
    parser.add_argument("--test-only", action="store_true", help="Esegue solo i test")
    args = parser.parse_args()

    start_time = time.time()
    print(f"\n{BOLD}{YELLOW}🚀 SYNCROJOB MASTER CHECK AVVIATO{RESET}")
    print(f"{ '='*50}")

    if args.test_only:
        success = run_tests()
    else:
        # Pipeline completa
        checks = [
            (check_versions, []),
            (sync_requirements, []),
            (run_ruff, [args.fix]),
            (run_bandit, []),
            (run_interrogate, []),
        ]

        if not args.fast:
            checks.append((run_tests, []))
            checks.append((run_pre_commit, []))

        success = True
        for func, f_args in checks:
            if not func(*f_args):
                success = False
                print(f"\n{RED}🛑 Bloccato al passaggio: {func.__name__}{RESET}")
                break

    duration = time.time() - start_time
    print(f"\n{'='*50}")
    if success:
        print(
            f"{GREEN}{BOLD}✨ TUTTI I CONTROLLI PASSATI! (Tempo: {duration:.1f}s){RESET}"
        )
        sys.exit(0)
    else:
        print(f"{RED}{BOLD}❌ CONTROLLI FALLITI. Correggi gli errori sopra.{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
