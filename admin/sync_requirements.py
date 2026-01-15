import sys
from pathlib import Path

import tomlkit


def generate_requirements_content():
    lock_file = Path("poetry.lock")
    if not lock_file.exists():
        print("Error: poetry.lock not found.")
        sys.exit(1)

    with open(lock_file, "r", encoding="utf-8") as f:
        lock_data = tomlkit.parse(f.read())

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


def sync(check_only=False):
    content = generate_requirements_content()
    req_file = Path("requirements.txt")

    current_content = ""
    if req_file.exists():
        with open(req_file, "r", encoding="utf-8") as f:
            current_content = f.read()

    # Normalize newlines for comparison
    content = content.replace("\r\n", "\n")
    current_content = current_content.replace("\r\n", "\n")

    if content != current_content:
        if check_only:
            print("FAILURE: requirements.txt is out of sync with poetry.lock")
            sys.exit(1)
        else:
            with open(req_file, "w", encoding="utf-8") as f:
                f.write(content)
            print("SUCCESS: requirements.txt updated from poetry.lock")
    else:
        print("SUCCESS: requirements.txt is already in sync.")


if __name__ == "__main__":
    check_mode = "--check" in sys.argv
    sync(check_only=check_mode)
