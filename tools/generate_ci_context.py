#!/usr/bin/env python3
"""SyncroJob - CI Context Generator (Final Secure Edition).

Aggrega l'output di Ruff, Mypy e dei Test in un unico file CI_CONTEXT.md
nella root del progetto per facilitare l'analisi da parte dell'IA.
"""

import contextlib
import os
import subprocess
import sys
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path

# Forza UTF-8 per stdout/stderr se possibile per evitare UnicodeEncodeError su Windows
if sys.stdout.encoding != "utf-8":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
OUTPUT_FILE = PROJECT_ROOT / "CI_CONTEXT.md"
TEMP_REPORT = PROJECT_ROOT / "tests" / "temp_test_report.md"


def run_command(cmd: Sequence[str], label: str) -> tuple[str, str, int]:
    """Esegue un comando e cattura l'output in modo sicuro."""
    print(f"Running {label}...")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            check=False,
            encoding="utf-8",
            errors="replace",
        )
        return result.stdout, result.stderr, result.returncode  # noqa: TRY300
    except Exception as e:
        return "", f"Error running {label}: {e}", 1


def main() -> None:  # noqa: C901, PLR0912, PLR0915
    """Aggregatore principale del contesto CI."""
    start_time = datetime.now()

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        f.write("# CI/CD Context Report\n\n")
        f.write(f"**Generated:** {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        try:
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                text=True,
                cwd=PROJECT_ROOT,
                encoding="utf-8",
            ).strip()
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
            if stdout:
                f.write(stdout)
            if stderr:
                f.write("\nSTDERR:\n")
                f.write(stderr)
            if not stdout and not stderr:
                f.write(f"No output captured (Exit code: {code})")
            f.write("\n```\n\n")

        # 2. MYPY
        f.write("## Mypy Type Checking\n")
        stdout, stderr, code = run_command([sys.executable, "-m", "mypy", "src"], "Mypy")
        if code == 0:
            f.write("Mypy: No type issues found.\n\n")
        else:
            f.write("```text\n")
            if stdout:
                f.write(stdout)
            if stderr:
                f.write("\nSTDERR:\n")
                f.write(stderr)
            if not stdout and not stderr:
                f.write(f"No output captured (Exit code: {code})")
            f.write("\n```\n\n")

        # 3. ROBUST TESTS
        f.write("## Robust Test Results\n")
        os.environ["TEST_REPORT_PATH"] = str(TEMP_REPORT)

        # Eseguiamo il runner robusto con --reset forzato
        test_cmd = [sys.executable, "-m", "tests.run_robust_test", "--reset"]
        if len(sys.argv) > 1:
            test_cmd.extend(sys.argv[1:])

        print("Running Robust Tests (this may take a while)...")
        subprocess.run(test_cmd, cwd=PROJECT_ROOT, check=False)

        if TEMP_REPORT.exists():
            test_content = TEMP_REPORT.read_text(encoding="utf-8", errors="replace")
            # Pulizia titoli duplicati
            clean_content = test_content.replace("# Test Execution Report", "").replace(
                "# \ud83d\udcca Test Execution Report", ""
            )
            f.write(clean_content)
            with contextlib.suppress(Exception):
                TEMP_REPORT.unlink()
        else:
            f.write("Error: Test report not generated.\n")

    print("\nCI_CONTEXT.md generated successfully in the project root.")


if __name__ == "__main__":
    main()
