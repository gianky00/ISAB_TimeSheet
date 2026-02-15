#!/usr/bin/env python3
"""
SyncroJob - CI Context Generator
Aggrega l'output di Ruff, Mypy e dei Test in un unico file CI_CONTEXT.md
nella root del progetto per facilitare l'analisi da parte dell'IA.
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

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
            check=False
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", f"Error running {label}: {e}", 1

def main():
    start_time = datetime.now()
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 🤖 CI/CD Context Report

")
        f.write(f"**Generated:** {start_time.strftime('%Y-%m-%d %H:%M:%S')}
")
        f.write(f"**Branch:** {subprocess.getoutput('git rev-parse --abbrev-ref HEAD')}

")
        
        # 1. RUFF
        f.write("## 🧹 Ruff Analysis
")
        stdout, stderr, code = run_command([sys.executable, "-m", "ruff", "check", "."], "Ruff")
        if code == 0 and not stdout:
            f.write("✅ Ruff: No issues found.

")
        else:
            f.write("```text
")
            f.write(stdout or "No output")
            if stderr: f.write("
STDERR:
" + stderr)
            f.write("
```

")
            
        # 2. MYPY
        f.write("## 📝 Mypy Type Checking
")
        stdout, stderr, code = run_command([sys.executable, "-m", "mypy", "src"], "Mypy")
        if code == 0:
            f.write("✅ Mypy: No type issues found.

")
        else:
            f.write("```text
")
            f.write(stdout or "No output")
            if stderr: f.write("
STDERR:
" + stderr)
            f.write("
```

")
            
        # 3. ROBUST TESTS
        f.write("## 🧪 Robust Test Results
")
        os.environ["TEST_REPORT_PATH"] = str(TEMP_REPORT)
        
        # Eseguiamo il runner robusto
        # Nota: usiamo pass-through per gli argomenti (es. -m 'not slow')
        test_cmd = [sys.executable, "tests/run_robust_tests.py"]
        if len(sys.argv) > 1:
            test_cmd.extend(sys.argv[1:])
            
        subprocess.run(test_cmd, cwd=PROJECT_ROOT, check=False)
        
        if TEMP_REPORT.exists():
            test_content = TEMP_REPORT.read_text(encoding="utf-8")
            # Rimuoviamo il titolo duplicato se presente nel report dei test
            f.write(test_content.replace("# 📊 Test Execution Report", ""))
            TEMP_REPORT.unlink()
        else:
            f.write("❌ Error: Test report not generated.
")

    print(f"
✅ CI_CONTEXT.md generato con successo nella root del progetto.")

if __name__ == "__main__":
    main()
