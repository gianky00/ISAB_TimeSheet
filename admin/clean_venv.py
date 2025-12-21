"""
Script to clean up invalid distributions (directories starting with ~) in site-packages.
These are leftovers from failed pip operations and cause warnings.
"""
import os
import shutil
import sys
import site

def get_site_packages():
    # Attempt to find site-packages directory
    for path in sys.path:
        if 'site-packages' in path and os.path.isdir(path):
            return path
    return None

def clean_invalid_dists():
    site_pkg = get_site_packages()
    if not site_pkg:
        print("Could not find site-packages directory.")
        return

    print(f"Checking for invalid distributions in: {site_pkg}")

    found = False
    for name in os.listdir(site_pkg):
        if name.startswith('~'):
            full_path = os.path.join(site_pkg, name)
            print(f"Found invalid distribution: {name}")
            try:
                if os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                else:
                    os.remove(full_path)
                print(f"  Successfully removed: {full_path}")
                found = True
            except Exception as e:
                print(f"  Error removing {name}: {e}")

    if not found:
        print("No invalid distributions found.")

if __name__ == "__main__":
    clean_invalid_dists()
