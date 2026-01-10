"""
SyncroJob - Professional Release Tool
Sostituisce i vecchi script .bat con un processo robusto e cross-platform.
"""

import argparse
import subprocess
import sys
import os
import time
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent.parent
VENV_PYTHON = ROOT_DIR / ".venv" / "Scripts" / "python.exe" if sys.platform == "win32" else ROOT_DIR / ".venv" / "bin" / "python"

def run_command(cmd, description, exit_on_fail=True):
    print(f"\n[STEP] {description}...")
    print(f"Executing: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, cwd=ROOT_DIR, capture_output=False, text=True)
        if result.returncode != 0:
            print(f"❌ Error during: {description}")
            if exit_on_fail:
                sys.exit(result.returncode)
            return False
        print(f"✅ {description} completed successfully.")
        return True
    except Exception as e:
        print(f"❌ Exception during {description}: {e}")
        if exit_on_fail:
            sys.exit(1)
        return False

def main():
    parser = argparse.ArgumentParser(description="SyncroJob Release Tool")
    parser.add_argument("type", choices=["patch", "minor", "major"], default="patch", nargs="?", help="Tipo di bump versione")
        parser.add_argument("--skip-tests", action="store_true", help="Salta l'esecuzione dei test")
        parser.add_argument("--no-build", action="store_true", help="Non creare l'eseguibile")
        parser.add_argument("--deploy", action="store_true", help="Esegui il deploy su Netlify")
        args = parser.parse_args()
    
        start_time = time.time()
        print("=" * 60)
        print("🚀 SYNCROJOB - MODERN RELEASE PROCESS")
        if args.deploy:
            print("🌍 MODE: CLOUD DEPLOYMENT")
        else:
            print("🏠 MODE: LOCAL BUILD ONLY")
        print("=" * 60)
    
        # 1. Tests
        if not args.skip_tests:
            # Core Tests
            run_command(
                [str(VENV_PYTHON), "-m", "pytest", "tests/",
                 "--ignore=tests/unit/test_gui_contabilita_extra.py",
                 "--ignore=tests/unit/test_gui_contabilita_logic.py",
                 "--ignore=tests/unit/test_gui_panels_new.py",
                 "--ignore=tests/unit/test_gui_panels.py",
                 "--ignore=tests/unit/test_gui_settings.py",
                 "--ignore=tests/unit/test_main_window.py",
                 "--ignore=tests/unit/test_ux_settings_menus.py",
                 "--ignore=tests/unit/test_gui_snapshots.py",
                 "--ignore=tests/unit/test_horizontal_timeline.py",
                 "-v", "--tb=short"],
                "Running Core Tests"
            )
            
            # GUI Tests
            run_command(
                [str(VENV_PYTHON), "-m", "pytest",
                 "tests/unit/test_gui_contabilita_extra.py",
                 "tests/unit/test_gui_contabilita_logic.py",
                 "tests/unit/test_gui_panels_new.py",
                 "tests/unit/test_gui_panels.py",
                 "tests/unit/test_gui_settings.py",
                 "tests/unit/test_main_window.py",
                 "tests/unit/test_ux_settings_menus.py",
                 "tests/unit/test_gui_snapshots.py",
                 "tests/unit/test_horizontal_timeline.py",
                 "-v", "--tb=short"],
                "Running GUI Tests"
            )
    
        # 2. Version Bump
        run_command(
            [str(VENV_PYTHON), "admin/bump_version.py", args.type],
            f"Incrementing version ({args.type})"
        )
    
        # 3. Icons
        run_command(
            [str(VENV_PYTHON), "admin/Crea Setup/generate_icons.py"],
            "Generating Icons"
        )
    
        # 4. Build
        if not args.no_build:
            build_cmd = [str(VENV_PYTHON), "admin/Crea Setup/build_dist.py"]
            if not args.deploy:
                build_cmd.append("--no-deploy")
                
            run_command(
                build_cmd,
                "Building Distribution"
            )
    duration = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"✨ RELEASE COMPLETED in {duration:.1f}s")
    print("=" * 60)

if __name__ == "__main__":
    main()
