import sys
from pathlib import Path

import tomlkit


def generate_requirements_content() -> str:
    """Estrae le dipendenze principali dal file poetry.lock e le formatta in stile requirements.txt."""
    lock_file = Path("poetry.lock")
    if not lock_file.exists():
        print("Error: poetry.lock not found.")
        sys.exit(1)

    lock_data = tomlkit.parse(lock_file.read_text(encoding="utf-8"))

    packages = []
    for package in lock_data.get("package", []):
        name = package["name"]
        version = package["version"]
        groups = package.get("groups", ["main"])  # Default to main if not specified
        optional = package.get("optional", False)

        if "main" in groups and not optional:
            packages.append(f"{name}=={version}")

    packages.sort(key=str.lower)
    return "\n".join(packages) + "\n"


def sync(check_only: bool = False) -> None:
    """
    Sincronizza il file requirements.txt con lo stato attuale di Poetry.

    Args:
        check_only: Se True, verifica solo la sincronizzazione senza scrivere file.
    """
    content = generate_requirements_content()
    req_file = Path("requirements.txt")

    current_content = ""
    if req_file.exists():
        current_content = req_file.read_text(encoding="utf-8")

    # Normalize newlines for comparison
    content = content.replace("\r\n", "\n")
    current_content = current_content.replace("\r\n", "\n")

    if content != current_content:
        if check_only:
            print("FAILURE: requirements.txt is out of sync with poetry.lock")
            sys.exit(1)
        else:
            req_file.write_text(content, encoding="utf-8")
            print("SUCCESS: requirements.txt updated from poetry.lock")
    else:
        print("SUCCESS: requirements.txt is already in sync.")


if __name__ == "__main__":
    check_mode = "--check" in sys.argv
    sync(check_only=check_mode)
