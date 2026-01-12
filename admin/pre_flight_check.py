#!/usr/bin/env python3
"""
🚀 SyncroJob Pre-Flight Check
=============================
Questo script verifica che il sistema sia pronto per il rilascio.
Controlla:
1. Coerenza versioni (pyproject.toml vs code)
2. Stato Git (Clean working tree)
3. Integrità Test Suite
"""

import re
import subprocess
import sys
from pathlib import Path

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

PROJECT_ROOT = Path(__file__).parent.parent

def print_step(msg):
    print(f"\n{BOLD}🔍 {msg}{RESET}")

def print_ok(msg):
    print(f"{GREEN}✅ {msg}{RESET}")

def print_fail(msg):
    print(f"{RED}❌ {msg}{RESET}")

def get_pyproject_version():
    content = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'version\s*=\s*"(.*?)"', content)
    return match.group(1) if match else None

def get_code_version():
    content = (PROJECT_ROOT / "src/core/version.py").read_text(encoding="utf-8")
    match = re.search(r'__version__\s*=\s*"(.*?)"', content)
    return match.group(1) if match else None

def check_versions():
    print_step("Verifica allineamento versioni...")
    v_toml = get_pyproject_version()
    v_code = get_code_version()

    if v_toml == v_code:
        print_ok(f"Versioni allineate: {v_toml}")
        return True
    else:
        print_fail(f"Discrepanza versioni!\n   pyproject.toml: {v_toml}\n   version.py:     {v_code}")
        return False

def check_git_status():
    print_step("Verifica stato Git...")
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if not result.stdout.strip():
        print_ok("Working tree pulito.")
        return True
    else:
        print(f"{YELLOW}⚠️  Attenzione: Ci sono modifiche non committate.{RESET}")
        print(f"{YELLOW}   Verranno incluse automaticamente nel commit di release.{RESET}")
        return True # Non blocca più la release

def check_requirements_sync():
    print_step("Sincronizzazione requirements.txt...")
    script_path = PROJECT_ROOT / "admin" / "sync_requirements.py"
    # Esegue la sincronizzazione (senza --check) per assicurare l'allineamento
    ret = subprocess.call([sys.executable, str(script_path)], cwd=PROJECT_ROOT)
    if ret == 0:
        print_ok("requirements.txt sincronizzato correttamente.")
        return True
    else:
        print_fail("Errore durante la sincronizzazione di requirements.txt!")
        return False

def run_tests():
    print_step("Esecuzione Test Suite (Robust Mode)...")
    # Utilizza il runner robusto che gestisce isolamento, report e retry
    runner_script = PROJECT_ROOT / "tests" / "run_robust_tests.py"
    cmd = [sys.executable, str(runner_script), "--reset"]

    try:
        # Eseguiamo subprocess lasciando l'output visibile
        ret = subprocess.call(cmd, cwd=PROJECT_ROOT)
        if ret == 0:
            print_ok("Tutti i test passati.")
            return True
        else:
            print_fail("Test falliti. Controlla il report o l'output sopra. Build annullata.")
            return False
    except Exception as e:
        print_fail(f"Errore esecuzione test: {e}")
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="SyncroJob Pre-Flight Check")
    parser.add_argument("--skip-tests", action="store_true", help="Salta l'esecuzione dei test")
    args = parser.parse_args()

    print(f"{BOLD}✈️  AVVIO PRE-FLIGHT CHECK...{RESET}")

    checks = [
        check_versions,
        check_requirements_sync,
        check_git_status
    ]

    if not args.skip_tests:
        checks.append(run_tests)
    else:
        print(f"{YELLOW}⚠️  SKIP: Esecuzione test saltata su richiesta utente.{RESET}")

    for check in checks:
        if not check():
            print(f"\n{RED}⛔ ABORT: Controllo fallito. Correggi gli errori e riprova.{RESET}")
            sys.exit(1)

    print(f"\n{GREEN}{BOLD}🚀 READY FOR TAKEOFF! Tutte le verifiche superate.{RESET}")
    sys.exit(0)

if __name__ == "__main__":
    main()
