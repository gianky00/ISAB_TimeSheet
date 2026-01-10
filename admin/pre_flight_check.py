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

import sys
import re
import subprocess
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
        print_fail("Ci sono modifiche non committate:")
        print(result.stdout)
        print(f"{YELLOW}⚠️  Consiglio: Committa le modifiche prima del rilascio.{RESET}")
        return False # Cambia a True se vuoi permettere build dirty (sconsigliato)

def run_tests():
    print_step("Esecuzione Test Suite (Fast Mode)...")
    # Usa il comando 'test' definito in pyproject.toml che include già le esclusioni
    cmd = ["poetry", "run", "test"]
    
    try:
        # Eseguiamo subprocess lasciando l'output visibile così l'utente vede i progressi
        ret = subprocess.call(cmd, cwd=PROJECT_ROOT, shell=True)
        if ret == 0:
            print_ok("Tutti i test passati.")
            return True
        else:
            print_fail("Test falliti. Build annullata.")
            return False
    except Exception as e:
        print_fail(f"Errore esecuzione test: {e}")
        return False

def main():
    print(f"{BOLD}✈️  AVVIO PRE-FLIGHT CHECK...{RESET}")
    
    checks = [
        check_versions,
        check_git_status,
        run_tests
    ]
    
    for check in checks:
        if not check():
            print(f"\n{RED}⛔ ABORT: Controllo fallito. Correggi gli errori e riprova.{RESET}")
            sys.exit(1)
            
    print(f"\n{GREEN}{BOLD}🚀 READY FOR TAKEOFF! Tutte le verifiche superate.{RESET}")
    sys.exit(0)

if __name__ == "__main__":
    main()
