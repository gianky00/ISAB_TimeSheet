"""
Bot TS - Version Bumper
Incrementa la versione dell'applicazione.
"""
import os
import sys
import re


def bump_version(part='patch'):
    """
    Incrementa la versione in src/core/version.py.
    
    Args:
        part: 'major', 'minor', o 'patch'
    """
    # admin/bump_version.py -> admin -> root
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    version_file = os.path.join(root_dir, "src", "core", "version.py")

    if not os.path.exists(version_file):
        print(f"Errore: File versione non trovato: {version_file}")
        sys.exit(1)

    with open(version_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Estrai versione corrente
    match = re.search(r'__version__\s*=\s*"(\d+)\.(\d+)\.(\d+)"', content)
    if not match:
        print("Errore: Impossibile trovare la stringa di versione.")
        sys.exit(1)

    major, minor, patch = map(int, match.groups())
    old_version = f"{major}.{minor}.{patch}"

    # Incrementa
    if part == 'major':
        major += 1
        minor = 0
        patch = 0
    elif part == 'minor':
        minor += 1
        patch = 0
    else:
        patch += 1

    new_version = f"{major}.{minor}.{patch}"
    
    # Sostituisci nel contenuto
    new_content = re.sub(
        r'__version__\s*=\s*".*"',
        f'__version__ = "{new_version}"',
        content
    )

    with open(version_file, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✓ Versione aggiornata: {old_version} → {new_version}")
    return new_version


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Incrementa la versione dell'applicazione")
    parser.add_argument(
        'part',
        choices=['major', 'minor', 'patch'],
        default='patch',
        nargs='?',
        help='Tipo di incremento (default: patch)'
    )
    
    args = parser.parse_args()
    bump_version(args.part)
