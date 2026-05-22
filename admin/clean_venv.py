"""Script to clean up invalid distributions (directories starting with ~) in site-packages.
These are leftovers from failed pip operations and cause warnings.
"""

import contextlib
import shutil
import sys
from pathlib import Path


def get_site_packages():
    """Retrieves the site-packages directory path from sys.path."""
    # Attempt to find site-packages directory
    for path_str in sys.path:
        path = Path(path_str)
        if "site-packages" in path_str and path.is_dir():
            return path
    return None


def clean_invalid_dists() -> None:
    """Scans and removes invalid distributions (starting with ~) from site-packages."""
    site_pkg = get_site_packages()
    if not site_pkg:
        print("Could not find site-packages directory.")
        return

    print(f"Checking for invalid distributions in: {site_pkg}")

    found = False
    for item in site_pkg.iterdir():
        if item.name.startswith("~"):
            print(f"Found invalid distribution: {item.name}")
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                print(f"  Successfully removed: {item}")
                found = True
            except Exception as e:
                print(f"  Error removing {item.name}: {e}")

    if not found:
        print("No invalid distributions found.")


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        clean_invalid_dists()
