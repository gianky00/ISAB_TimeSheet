"""Bot TS - Version Bumper
Incrementa la versione dell'applicazione.
"""

import contextlib
import io
import re
import sys
from pathlib import Path

# Fix encoding for Windows console to support emoji
if sys.platform == "win32":
    with contextlib.suppress(Exception):
        if hasattr(sys.stdout, "buffer"):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "buffer"):
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def bump_version(part="patch"):
    """Incrementa la versione in src/application/services/version.py.

    Args:
        part: 'major', 'minor', o 'patch'
    """
    # devtools/gui/bump_version.py -> admin -> root
    root_dir = Path(__file__).parent.parent.resolve()
    version_file = root_dir / "src" / "core" / "version.py"

    if not version_file.exists():
        print(f"Errore: File versione non trovato: {version_file}")
        sys.exit(1)

    content = version_file.read_text(encoding="utf-8")

    # Estrai versione corrente
    match = re.search(r'__version__\s*=\s*"(\d+)\.(\d+)\.(\d+)"', content)
    if not match:
        print("Errore: Impossibile trovare la stringa di versione.")
        sys.exit(1)

    major, minor, patch = map(int, match.groups())
    old_version = f"{major}.{minor}.{patch}"

    # Incrementa
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1

    new_version = f"{major}.{minor}.{patch}"

    # Sostituisci nel contenuto di version.py
    new_content = re.sub(r'__version__\s*=\s*".*"', f'__version__ = "{new_version}"', content)

    version_file.write_text(new_content, encoding="utf-8")

    # Aggiorna pyproject.toml
    pyproject_file = root_dir / "pyproject.toml"
    if pyproject_file.exists():
        pp_content = pyproject_file.read_text(encoding="utf-8")

        # Sostituisci solo la prima occorrenza di version = "..." (quella del pacchetto)
        pp_new_content = re.sub(
            r'^version\s*=\s*".*"',
            f'version = "{new_version}"',
            pp_content,
            flags=re.MULTILINE,
        )

        pyproject_file.write_text(pp_new_content, encoding="utf-8")
        print(f"✓ pyproject.toml aggiornato alla versione {new_version}")

    print(f"✓ Versione aggiornata: {old_version} → {new_version}")
    return new_version


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Incrementa la versione dell'applicazione")
    parser.add_argument(
        "part",
        choices=["major", "minor", "patch"],
        default="patch",
        nargs="?",
        help="Tipo di incremento (default: patch)",
    )

    args = parser.parse_args()
    bump_version(args.part)
