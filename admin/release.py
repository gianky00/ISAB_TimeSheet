"""
SyncroJob - Professional Release Tool
Sostituisce i vecchi script .bat con un processo robusto e cross-platform.
"""

import argparse
import io
import json
import subprocess
import sys
import time
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent.parent
VENV_PYTHON = (
    ROOT_DIR / ".venv" / "Scripts" / "python.exe"
    if sys.platform == "win32"
    else ROOT_DIR / ".venv" / "bin" / "python"
)


def run_command(cmd, description, exit_on_fail=True, capture=False):
    """Executes a subprocess command with error handling and optional output capture."""
    print(f"\n[STEP] {description}...")
    sys.stdout.flush()
    try:
        if capture:
            result = subprocess.run(
                cmd, cwd=ROOT_DIR, capture_output=True, text=True, check=True
            )
            return result.stdout.strip()

        result = subprocess.run(cmd, cwd=ROOT_DIR, check=exit_on_fail)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Comando fallito: {description}")
        print(f"        Exit code: {e.returncode}")
        sys.stdout.flush()
        if exit_on_fail:
            sys.exit(1)
        return False
    except Exception as e:
        print(f"[ERROR] Errore durante: {description}")
        print(f"        Dettaglio: {e}")
        sys.stdout.flush()
        if exit_on_fail:
            sys.exit(1)
        return False


def get_current_version():
    """Extracts the current version string from src/core/version.py."""
    version_file = ROOT_DIR / "src" / "core" / "version.py"
    content = version_file.read_text()
    import re

    match = re.search(r'__version__\s*=\s*"(.*?)"', content)
    return match.group(1) if match else "unknown"


def notify_telegram(message):
    """Invia notifica rapida via Telegram (usando i segreti nel progetto)"""
    try:
        config_path = ROOT_DIR / "config.json"
        if not config_path.exists():
            return
        with open(config_path, "r") as f:
            config = json.load(f)

        token = config.get("telegram_token")
        chat_id = config.get("telegram_chat_id")
        if token and chat_id:
            import requests

            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(
                url,
                json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"},
            )
            print("📲 Notifica Telegram inviata.")
    except Exception as e:
        print(f"⚠️ Impossibile inviare notifica: {e}")


def detect_bump_type():
    """Rileva automaticamente il tipo di bump analizzando branch e commit log."""
    try:
        # 1. Controlla il nome del branch corrente
        current_branch = (
            subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=ROOT_DIR,
                capture_output=True,
                text=True,
            )
            .stdout.strip()
            .lower()
        )

        # 2. Trova l'ultimo tag
        last_tag = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
        ).stdout.strip()

        # Default se non ci sono tag
        if not last_tag:
            return "patch"

        # 3. Prende i messaggi dei commit dal tag ad oggi
        logs = subprocess.run(
            ["git", "log", f"{last_tag}..HEAD", "--oneline"],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
        ).stdout.lower()

        # LOGICA DI RILEVAZIONE (Priorità: Major -> Minor -> Patch)

        # Check MAJOR
        if "breaking change" in logs or "!" in logs:
            return "major"

        # Check MINOR (Branch feature o commit feat)
        if (
            current_branch.startswith("feature/")
            or current_branch.startswith("feat/")
            or "feat:" in logs
            or "feat(" in logs
            or "add:" in logs
        ):
            return "minor"

        # Default PATCH (fix, refactor, chore, docs, ecc.)
        return "patch"
    except Exception:
        return "patch"


def main():
    """Entry point for the release process, handling arguments and workflow execution."""
    # Fix encoding for Windows console to support emoji
    if sys.platform == "win32":
        try:
            if hasattr(sys.stdout, "buffer"):
                sys.stdout = io.TextIOWrapper(
                    sys.stdout.buffer, encoding="utf-8", errors="replace"
                )
            if hasattr(sys.stderr, "buffer"):
                sys.stderr = io.TextIOWrapper(
                    sys.stderr.buffer, encoding="utf-8", errors="replace"
                )
        except Exception:
            pass  # Fallback silenzioso se il wrapping fallisce

    parser = argparse.ArgumentParser(description="SyncroJob Automated Release Tool")
    parser.add_argument(
        "type",
        choices=["patch", "minor", "major", "auto"],
        default="auto",
        nargs="?",
        help="Bump type",
    )
    parser.add_argument("--deploy", action="store_true", help="Deploy to Netlify")
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip test execution during pre-flight",
    )
    parser.add_argument(
        "--force", action="store_true", help="Force release even if checks fail"
    )
    parser.add_argument("--no-git", action="store_true", help="Skip Git operations")
    parser.add_argument(
        "--push", action="store_true", help="Push to remote after release"
    )
    args = parser.parse_args()

    start_time = time.time()

    # 1. Pre-Flight Check Interno
    pre_flight_cmd = [str(VENV_PYTHON), "admin/pre_flight_check.py"]
    if args.skip_tests:
        pre_flight_cmd.append("--fast")
    if args.force:
        pre_flight_cmd.append("--force")

    run_command(pre_flight_cmd, "Pre-Flight Safety Check")

    # 2. Sync Requirements
    run_command(
        [str(VENV_PYTHON), "admin/sync_requirements.py"], "Syncing Requirements"
    )

    # 3. Resolve Bump Type
    bump_type = args.type
    if bump_type == "auto":
        bump_type = detect_bump_type()
        print(f"🔍 Detected bump type: {bump_type}")

    # 4. Version Bump
    run_command(
        [str(VENV_PYTHON), "admin/bump_version.py", bump_type], f"Bumping {bump_type}"
    )
    new_version = get_current_version()

    # 5. Git Operations
    if not args.no_git:
        run_command(["git", "add", "."], "Staging changes")
        run_command(
            ["git", "commit", "-m", f"chore: release v{new_version} [auto]"],
            f"Committing v{new_version}",
        )
        run_command(
            ["git", "tag", "-a", f"v{new_version}", "-m", f"Release v{new_version}"],
            f"Tagging v{new_version}",
        )
        if args.push:
            run_command(
                ["git", "push", "origin", "main", "--tags"], "Pushing to remote"
            )

    # 5. Build
    build_script = ROOT_DIR / "admin" / "Crea Setup" / "build_dist.py"
    build_cmd = [str(VENV_PYTHON), str(build_script)]
    if not args.deploy:
        build_cmd.append("--no-deploy")
    run_command(build_cmd, "Building Distribution")

    duration = time.time() - start_time
    success_msg = f"🚀 *SyncroJob v{new_version} Rilasciata!*\nStatus: Success\nTempo: {duration:.1f}s\nMode: {'Cloud' if args.deploy else 'Local'}"

    print("\n" + "=" * 60)
    print(f"✨ RELEASE v{new_version} COMPLETED in {duration:.1f}s")
    print("=" * 60)

    notify_telegram(success_msg)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] Operazione annullata dall'utente.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[FATAL ERROR] Errore non gestito: {e}")
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        sys.exit(1)
