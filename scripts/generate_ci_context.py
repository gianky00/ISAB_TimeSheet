#!/usr/bin/env python3
"""
SyncroJob - CI Context Generator (Secure Encoding Edition)
Aggrega l'output di Ruff, Mypy e dei Test in un unico file CI_CONTEXT.md
nella root del progetto per facilitare l'analisi da parte dell'IA.
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Forza UTF-8 per stdout/stderr se possibile
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
OUTPUT_FILE = PROJECT_ROOT / "CI_CONTEXT.md"
TEMP_REPORT = PROJECT_ROOT / "tests" / "temp_test_report.md"

def run_command(cmd, label):
    print(f"Running {label}...")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            check=False,
            encoding="utf-8",
            errors="replace"
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", f"Error running {label}: {e}", 1

def main():
    start_time = datetime.now()
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# CI/CD Context Report\n\n")
        f.write(f"**Generated:** {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        try:
            branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], 
                                           text=True, cwd=PROJECT_ROOT, encoding="utf-8").strip()
            f.write(f"**Branch:** {branch}\n\n")
        except Exception:
            f.write("**Branch:** Unknown\n\n")
        
        # 1. RUFF
        f.write("## Ruff Analysis\n")
        stdout, stderr, code = run_command([sys.executable, "-m", "ruff", "check", "."], "Ruff")
        if code == 0 and not stdout:
            f.write("Ruff: No issues found.\n\n")
        else:
            f.write("```text\n")
            if stdout: f.write(stdout)
            if stderr: f.write("\nSTDERR:\n" + stderr)
            if not stdout and not stderr: f.write("No output captured (Exit code: " + str(code) + ")")
            f.write("\n```\n\n")
            
        # 2. MYPY
        f.write("## Mypy Type Checking\n")
        stdout, stderr, code = run_command([sys.executable, "-m", "mypy", "src"], "Mypy")
        if code == 0:
            f.write("Mypy: No type issues found.\n\n")
        else:
            f.write("```text\n")
            if stdout: f.write(stdout)
            if stderr: f.write("\nSTDERR:\n" + stderr)
            if not stdout and not stderr: f.write("No output captured (Exit code: " + str(code) + ")")
            f.write("\n```\n\n")
            
        # 3. ROBUST TESTS
        f.write("## Robust Test Results\n")
        os.environ["TEST_REPORT_PATH"] = str(TEMP_REPORT)
        
        # Eseguiamo il runner robusto
        test_cmd = [sys.executable, "tests/run_robust_tests.py"]
        if len(sys.argv) > 1:
            test_cmd.extend(sys.argv[1:])
            
        print("Running Robust Tests (this may take a while)...")
        subprocess.run(test_cmd, cwd=PROJECT_ROOT, check=False)
        
        if TEMP_REPORT.exists():
            test_content = TEMP_REPORT.read_text(encoding="utf-8", errors="replace")
            # Pulizia titoli
            clean_content = test_content.replace("# Test Execution Report", "").replace("# 📊 Test Execution Report", "")
            f.write(clean_content)
            try:
                TEMP_REPORT.unlink()
            except Exception:
                pass
        else:
            f.write("Error: Test report not generated.\n")

    print("\nCI_CONTEXT.md generated successfully in the project root.")

if __name__ == "__main__":
    main()
