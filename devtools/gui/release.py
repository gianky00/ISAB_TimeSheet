"""SyncroJob - Professional Release Tool
Sostituisce i vecchi script .bat con un processo robusto e cross-platform.
"""

import argparse
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent.parent.parent
VENV_PYTHON = (
    ROOT_DIR / ".venv" / "Scripts" / "python.exe"
    if sys.platform == "win32"
    else ROOT_DIR / ".venv" / "bin" / "python"
)
UV_EXE = (
    ROOT_DIR / ".venv" / "Scripts" / "uv.exe"
    if sys.platform == "win32"
    else ROOT_DIR / ".venv" / "bin" / "uv"
)
VENV_BIN = ROOT_DIR / ".venv" / "Scripts" if sys.platform == "win32" else ROOT_DIR / ".venv" / "bin"
os.environ["PATH"] = f"{VENV_BIN}{os.pathsep}{os.environ.get('PATH', '')}"


def find_git_executable() -> str:
    """Tenta di trovare l'eseguibile git in percorsi comuni su Windows."""
    # 1. Prova nel PATH standard
    git_bin = shutil.which("git")
    if git_bin:
        return git_bin

    if sys.platform != "win32":
        return "git"

    # 2. Prova percorsi comuni Windows
    common_paths = [
        Path(os.environ.get("PROGRAMFILES", "C:/Program Files")) / "Git/cmd/git.exe",
        Path(os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)")) / "Git/cmd/git.exe",
        Path(os.environ.get("LOCALAPPDATA", "")) / "GitHubDesktop" / "bin" / "git.exe",
    ]

    # 3. Prova a cercare nelle cartelle app di GitHub Desktop (percorso variabile con versione)
    github_desktop_root = Path(os.environ.get("LOCALAPPDATA", "")) / "GitHubDesktop"
    if github_desktop_root.exists():
        for app_dir in github_desktop_root.glob("app-*"):
            git_path = app_dir / "resources" / "app" / "git" / "cmd" / "git.exe"
            if git_path.exists():
                common_paths.append(git_path)

    for p in common_paths:
        if p.exists():
            return str(p)

    return "git"


def run_command(
    cmd: list[str], description: str, exit_on_fail: bool = True, capture: bool = False
) -> str | bool:
    """Executes a subprocess command with error handling and optional output capture."""
    print(f"\n[STEP] {description}...")
    sys.stdout.flush()

    # Se il primo argomento è 'git', prova a risolverlo
    if cmd[0] == "git":
        cmd[0] = find_git_executable()
    elif not os.path.isabs(cmd[0]):
        resolved = shutil.which(cmd[0])
        if resolved:
            cmd[0] = resolved

    try:
        if capture:
            result = subprocess.run(cmd, cwd=ROOT_DIR, capture_output=True, text=True, check=True)
            return result.stdout.strip()

        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"

        process = subprocess.Popen(
            cmd,
            cwd=ROOT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            env=env,
            bufsize=1,
            universal_newlines=True,
        )

        if process.stdout:
            for line in process.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()

        returncode = process.wait()

        if exit_on_fail and returncode != 0:
            print(f"[ERROR] Comando fallito: {description}")
            print(f"        Exit code: {returncode}")
            sys.stdout.flush()
            sys.exit(1)
        return returncode == 0  # noqa: TRY300
    except Exception as e:
        print(f"[ERROR] Errore durante: {description}")
        print(f"        Dettaglio: {e}")
        sys.stdout.flush()
        if exit_on_fail:
            sys.exit(1)
        return False


def run_command_safe(
    cmd: list[str], description: str, capture: bool = False
) -> tuple[bool, str]:
    """Come run_command ma NON chiama sys.exit: restituisce (successo, output).

    Usato nelle fasi post-bump in modo da poter effettuare rollback prima di uscire.
    """
    print(f"\n[STEP] {description}...")
    sys.stdout.flush()

    if cmd[0] == "git":
        cmd[0] = find_git_executable()

    try:
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"

        process = subprocess.Popen(
            cmd,
            cwd=ROOT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            env=env,
            bufsize=1,
            universal_newlines=True,
        )

        output_lines: list[str] = []
        if process.stdout:
            for line in process.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()
                output_lines.append(line)

        returncode = process.wait()
        return returncode == 0, "".join(output_lines)
    except Exception as e:
        print(f"[ERROR] Errore durante: {description}")
        print(f"        Dettaglio: {e}")
        sys.stdout.flush()
        return False, str(e)


# ---------------------------------------------------------------------------
# File snapshot / rollback
# ---------------------------------------------------------------------------

#: File che vengono modificati dal processo di bump + changelog.
_VERSIONED_FILES: list[Path] = [
    ROOT_DIR / "src" / "application" / "services" / "version.py",
    ROOT_DIR / "pyproject.toml",
    ROOT_DIR / "src" / "application" / "services" / "changelog.json",
    ROOT_DIR / "CHANGELOG.md",
]


def snapshot_versioned_files() -> dict[Path, str | None]:
    """Cattura il contenuto corrente dei file di versione prima del bump.

    Returns:
        Dizionario {path: contenuto} per ciascun file monitorato.
        Il valore è ``None`` se il file non esiste ancora.
    """
    snap: dict[Path, str | None] = {}
    for p in _VERSIONED_FILES:
        snap[p] = p.read_text(encoding="utf-8") if p.exists() else None
    return snap


def rollback_versioned_files(snapshot: dict[Path, str | None]) -> None:
    """Ripristina i file di versione allo stato precedente al bump.

    Args:
        snapshot: Il dizionario restituito da :func:`snapshot_versioned_files`.
    """
    print("\n[ROLLBACK] Ripristino dei file di versione allo stato pre-bump...")
    for path, content in snapshot.items():
        try:
            if content is None:
                # Il file non esisteva prima: lo eliminiamo se è stato creato
                if path.exists():
                    path.unlink()
                    print(f"  ✓ Rimosso (era nuovo): {path.name}")
            else:
                path.write_text(content, encoding="utf-8")
                print(f"  ✓ Ripristinato: {path.name}")
        except Exception as e:
            print(f"  ⚠️  Impossibile ripristinare {path.name}: {e}")
    print("[ROLLBACK] Completato. La versione è tornata a quella precedente.\n")


def get_current_version() -> str:
    """Extracts the current version string from src/application/services/version.py."""
    version_file = ROOT_DIR / "src" / "application" / "services" / "version.py"
    content = version_file.read_text(encoding="utf-8")
    import re

    match = re.search(r'__version__\s*=\s*"(.*?)"', content)
    return match.group(1) if match else "unknown"


def notify_telegram(message: str) -> None:
    """Invia notifica rapida via Telegram (usando i segreti nel progetto)"""
    try:
        config_path = ROOT_DIR / "config.json"
        if not config_path.exists():
            return
        with config_path.open(encoding="utf-8") as f:
            config = json.load(f)

        token = config.get("telegram_token")
        chat_id = config.get("telegram_chat_id")
        if token and chat_id:
            import requests

            url = f"https://api.telegram.org/bot{token}/sendMessage"
            requests.post(
                url,
                json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"},
                timeout=10,
            )
            print("📲 Notifica Telegram inviata.")
    except Exception as e:
        print(f"⚠️ Impossibile inviare notifica: {e}")


def detect_bump_type() -> str | None:
    """Rileva automaticamente il tipo di bump analizzando branch e commit log."""
    try:
        # 1. Controlla il nome del branch corrente
        git_bin = find_git_executable()
        current_branch = (
            subprocess.run(
                [git_bin, "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=ROOT_DIR,
                capture_output=True,
                text=True,
                check=False,
            )
            .stdout.strip()
            .lower()
        )

        # 2. Trova l'ultimo tag
        last_tag = subprocess.run(
            [git_bin, "describe", "--tags", "--abbrev=0"],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()

        # Default se non ci sono tag
        if not last_tag:
            return "patch"

        # 3. Prende i messaggi dei commit dal tag ad oggi
        logs = subprocess.run(
            [git_bin, "log", f"{last_tag}..HEAD", "--oneline"],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.lower()

        # LOGICA DI RILEVAZIONE (Priorità: Major -> Minor -> Patch)

        # Check MAJOR
        if "breaking change" in logs or "!" in logs:
            return "major"

        # Check MINOR (Branch feature o commit feat)
        if (
            current_branch.startswith(("feature/", "feat/"))
            or "feat:" in logs
            or "feat(" in logs
            or "add:" in logs
        ):
            return "minor"

        # Default PATCH (fix, refactor, chore, docs, ecc.)
        return "patch"  # noqa: TRY300
    except Exception:
        return "patch"


def verify_clean_git_status(git_bin: str) -> None:
    """Verifica se il repository Git locale ha modifiche non committate."""
    try:
        status = subprocess.run(
            [git_bin, "status", "--porcelain"],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            check=False,
        ).stdout.strip()
        if status:
            print("\n❌ [ERROR] Ci sono modifiche non committate nel repository Git!")
            print(status)
            print("Pulisci o committa le modifiche prima di procedere con il rilascio.\n")
            sys.exit(1)
    except Exception as e:
        print(f"⚠️ Impossibile verificare lo stato di Git: {e}")


def update_json_changelog(version: str, git_bin: str) -> None:
    """Genera e aggiorna il changelog.json strutturato in src/application/services/changelog.json."""
    changelog_path = ROOT_DIR / "src" / "application" / "services" / "changelog.json"

    # Ottiene l'ultimo tag Git prima del rilascio
    last_tag = None
    with contextlib.suppress(Exception):
        tags_res = subprocess.run(
            [git_bin, "tag", "--sort=-v:refname"],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            check=False,
        )
        tags = [t.strip() for t in tags_res.stdout.splitlines() if t.strip()]
        # Se abbiamo creato un nuovo tag per questa versione, prendiamo il precedente
        if tags:
            last_tag = tags[1] if len(tags) > 1 and tags[0] == f"v{version}" else tags[0]

    # Recupera i messaggi dei commit dall'ultimo tag a HEAD
    notes = []
    if last_tag:
        with contextlib.suppress(Exception):
            logs_res = subprocess.run(
                [git_bin, "log", f"{last_tag}..HEAD", "--pretty=format:%h|%s"],
                cwd=ROOT_DIR,
                capture_output=True,
                text=True,
                check=False,
            )
            logs = logs_res.stdout.splitlines()
            for line in logs:
                if line.strip():
                    if "|" in line:
                        sha, msg = line.split("|", 1)
                        notes.append({"sha": sha.strip(), "message": msg.strip()})
                    else:
                        notes.append({"message": line.strip(), "sha": ""})

    if not notes:
        notes = [{"message": f"Aggiornamenti e ottimizzazioni di stabilità per la versione v{version}", "sha": ""}]

    # Carica il file JSON esistente
    changelog_data = []
    if changelog_path.exists():
        with contextlib.suppress(Exception):
            changelog_data = json.loads(changelog_path.read_text(encoding="utf-8"))

    # Rimuove eventuali duplicati con la stessa versione
    changelog_data = [entry for entry in changelog_data if entry.get("version") != version]

    from datetime import datetime

    new_entry = {
        "version": version,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "notes": notes,
    }
    changelog_data.insert(0, new_entry)

    try:
        changelog_path.write_text(
            json.dumps(changelog_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        print(f"✓ Changelog JSON strutturato aggiornato in: {changelog_path.name}")
    except Exception as e:
        print(f"⚠️ Impossibile salvare il changelog JSON: {e}")


def prompt_interactive_release(args: argparse.Namespace) -> None:
    """Gestisce l'interazione con l'utente per configurare i parametri di rilascio."""
    print("\n" + "=" * 60)
    print("✨ [MODALITÀ INTERATTIVA DI RILASCIO SYNCROJOB]")
    print("=" * 60)

    # 1. Bump type
    print("\nSeleziona il tipo di incremento di versione:")
    print("  1) patch (default) - Bugfix e stabilità")
    print("  2) minor           - Nuove funzionalità retrocompatibili")
    print("  3) major           - Modifiche importanti non retrocompatibili")
    print("  4) auto            - Rilevamento automatico basato sui commit")
    choice = input("Scelta (1-4): ").strip()
    if choice == "2":
        args.type = "minor"
    elif choice == "3":
        args.type = "major"
    elif choice == "4":
        args.type = "auto"
    else:
        args.type = "patch"

    # 2. Skip tests
    skip_ans = input("\nDesideri saltare la suite dei test di qualità pre-flight? (s/N): ").strip().lower()
    args.skip_tests = skip_ans == "s"

    # 3. Nuitka or PyInstaller
    nuitka_ans = input("\nDesideri compilare con Nuitka invece di PyInstaller? (s/N): ").strip().lower()
    args.nuitka = nuitka_ans == "s"

    # 4. Deploy
    deploy_ans = input("\nDesideri eseguire il deploy su Netlify? (s/N): ").strip().lower()
    args.deploy = deploy_ans == "s"

    # 5. Push remote
    push_ans = input("\nDesideri eseguire il push remoto automatico su origin/main? (S/n): ").strip().lower()
    args.push = push_ans != "n"

    print("\n" + "=" * 60 + "\n")


def run_git_operations(
    new_version: str, args: argparse.Namespace, snapshot: dict[Path, str | None]
) -> bool:
    """Esegue il commit e il tagging della nuova versione in Git.

    Se una qualsiasi operazione fallisce, esegue il rollback automatico dei file
    di versione modificati dal bump e restituisce ``False``.

    Args:
        new_version: La nuova stringa di versione (es. ``"1.50.0"``)
        args: I parametri del processo di rilascio.
        snapshot: Lo snapshot pre-bump per il rollback.

    Returns:
        ``True`` se tutte le operazioni Git sono riuscite, ``False`` altrimenti.
    """
    if args.no_git:
        return True

    # Pre-genera lock e .ai-context.json prima dello staging per evitare che il pre-commit
    # modifichi i file durante il commit (pattern noto che causa il fallimento del commit).
    run_command([str(UV_EXE), "lock"], "Updating uv.lock preemptively")

    ai_context_script = ROOT_DIR / "devtools" / "cli" / "generate_ai_context.py"
    if ai_context_script.exists():
        run_command(
            [str(VENV_PYTHON), str(ai_context_script)],
            "Pre-generating .ai-context.json",
        )

    run_command(["git", "add", "."], "Staging changes")

    ok, _ = run_command_safe(
        ["git", "commit", "-m", f"chore: release v{new_version} [auto]"],
        f"Committing v{new_version}",
    )
    if not ok:
        print(f"\n[ERROR] Comando fallito: Committing v{new_version}")
        rollback_versioned_files(snapshot)
        # Annulla anche lo staging già eseguito
        git_bin = find_git_executable()
        subprocess.run([git_bin, "reset", "HEAD"], cwd=ROOT_DIR, check=False)
        return False

    ok, _ = run_command_safe(
        ["git", "tag", "-a", f"v{new_version}", "-m", f"Release v{new_version}"],
        f"Tagging v{new_version}",
    )
    if not ok:
        print(f"\n[ERROR] Comando fallito: Tagging v{new_version}")
        rollback_versioned_files(snapshot)
        return False

    if args.push:
        ok, _ = run_command_safe(["git", "push", "origin", "main", "--tags"], "Pushing to remote")
        if not ok:
            print("\n[ERROR] Comando fallito: Pushing to remote")
            rollback_versioned_files(snapshot)
            # Rollback Git: Rimuove tag appena creato e resetta commit
            git_bin = find_git_executable()
            subprocess.run([git_bin, "tag", "-d", f"v{new_version}"], cwd=ROOT_DIR, check=False)
            subprocess.run([git_bin, "reset", "--soft", "HEAD~1"], cwd=ROOT_DIR, check=False)
            subprocess.run([git_bin, "reset", "HEAD", "."], cwd=ROOT_DIR, check=False)
            print(f"[ROLLBACK] Tag v{new_version} rimosso e commit annullato.")
            return False

    return True


def run_build_operations(new_version: str, args: argparse.Namespace, start_time: float) -> None:
    """Compila il pacchetto di distribuzione e notifica il rilascio su Telegram."""
    build_script = ROOT_DIR / "admin" / "Crea Setup" / "build_dist.py"
    build_cmd = [str(VENV_PYTHON), str(build_script)]
    if not args.deploy:
        build_cmd.append("--no-deploy")
    if args.nuitka:
        build_cmd.append("--use-nuitka")
    run_command(build_cmd, "Building Distribution")

    duration = time.time() - start_time
    success_msg = (
        f"🚀 *SyncroJob v{new_version} Rilasciata!*\n"
        f"Status: Success\n"
        f"Tempo: {duration:.1f}s\n"
        f"Mode: {'Cloud' if args.deploy else 'Local'}"
    )

    print("\n" + "=" * 60)
    print(f"✨ RELEASE v{new_version} COMPLETED in {duration:.1f}s")
    print("=" * 60)

    notify_telegram(success_msg)


def main() -> None:
    """Entry point for the release process, handling arguments and workflow execution."""
    # Fix encoding for Windows console to support emoji
    if sys.platform == "win32":
        with contextlib.suppress(Exception):
            if hasattr(sys.stdout, "buffer"):
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
            if hasattr(sys.stderr, "buffer"):
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="SyncroJob Automated Release Tool")
    parser.add_argument(
        "type",
        choices=["patch", "minor", "major", "auto"],
        default="auto",
        nargs="?",
        help="Bump type",
    )
    parser.add_argument("--deploy", action="store_true", help="Deploy to Netlify")
    parser.add_argument("--nuitka", action="store_true", help="Use Nuitka instead of PyInstaller")
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip test execution during pre-flight",
    )
    parser.add_argument("--force", action="store_true", help="Force release even if checks fail")
    parser.add_argument("--no-git", action="store_true", help="Skip Git operations")
    parser.add_argument("--push", action="store_true", help="Push to remote after release")
    args = parser.parse_args()

    git_bin = find_git_executable()

    # Aggiunge la directory di git al PATH per i subprocessi (es. commitizen)
    if git_bin and git_bin != "git":
        git_dir = Path(git_bin).parent
        if git_dir.exists():
            os.environ["PATH"] = str(git_dir) + os.pathsep + os.environ["PATH"]

    # Rileva se lo script è in esecuzione in un terminale interattivo senza argomenti
    is_interactive = len(sys.argv) == 1 and sys.stdin.isatty()

    if is_interactive:
        prompt_interactive_release(args)

    # Controlla lo stato di Git prima di avviare il processo
    if not args.no_git and not args.force:
        verify_clean_git_status(git_bin)

    start_time = time.time()

    # 0. Sincronizzazione contesti e dipendenze
    ai_context_script = ROOT_DIR / "tools" / "generate_ai_context.py"
    if ai_context_script.exists():
        run_command(
            [str(VENV_PYTHON), str(ai_context_script)],
            "Aggiornamento .ai-context.json",
        )

    # Verifica sincronia lock file (fondamentale per EXE stabile)
    run_command([str(UV_EXE), "lock"], "Verifica integrità uv.lock")

    # 1. Pre-Flight Check Interno
    pre_flight_cmd = [str(VENV_PYTHON), "devtools/gui/pre_flight_check.py"]
    if args.skip_tests:
        pre_flight_cmd.append("--fast")
    if args.force:
        pre_flight_cmd.append("--force")

    run_command(pre_flight_cmd, "Pre-Flight Safety Check")

    # 3. Resolve Bump Type
    bump_type = args.type
    if bump_type == "auto":
        bump_type = detect_bump_type()
        print(f"🔍 Detected bump type: {bump_type}")

    # ── SNAPSHOT pre-bump ────────────────────────────────────────────────────
    # Salviamo il contenuto corrente dei file di versione PRIMA di modificarli.
    # In caso di fallimento delle operazioni Git, potremo ripristinarli esattamente.
    pre_bump_snapshot = snapshot_versioned_files()

    # 4. Version Bump
    run_command([str(VENV_PYTHON), "devtools/gui/bump_version.py", bump_type], f"Bumping {bump_type}")

    # 4.1 Update Changelog
    run_command([str(VENV_PYTHON), "-m", "commitizen", "changelog"], "Updating CHANGELOG.md via Commitizen")

    # 4.2 Ottiene la nuova versione prima di aggiornare il changelog JSON
    new_version = get_current_version()

    # 4.3 Update JSON Changelog strutturato
    update_json_changelog(new_version, git_bin)

    # 5. Operazioni Git (con rollback automatico in caso di fallimento)
    git_ok = run_git_operations(new_version, args, pre_bump_snapshot)
    if not git_ok:
        print("\n[FAILED] Il processo di rilascio è stato annullato a causa di un errore Git.")
        print("         I file di versione sono stati ripristinati allo stato pre-bump.")
        sys.exit(1)

    # 6. Compilazione e notifiche
    run_build_operations(new_version, args, start_time)


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
