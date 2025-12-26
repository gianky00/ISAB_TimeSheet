import os
import re
import sys
from pathlib import Path
from stdlib_list import stdlib_list

def get_std_libs():
    """Returns a set of standard Python libraries for a known compatible version."""
    # Use a known compatible version as a fallback
    compatible_version = "3.11"
    return set(stdlib_list(compatible_version))

def find_imports(file_path, std_libs):
    """Finds all non-standard, non-local imports in a Python file."""
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # Match 'import X' or 'from X import Y'
                match = re.match(r'^\s*(?:import|from)\s+([a-zA-Z0-9_]+)', line)
                if match:
                    module = match.group(1)
                    # Exclude standard libraries and local project imports
                    if module not in std_libs and not is_local_import(module, file_path):
                        imports.add(module)
    except Exception as e:
        print(f"Could not read {file_path}: {e}", file=sys.stderr)
    return imports

def is_local_import(module, file_path):
    """
    Checks if an import is likely a local module.
    A simple check: if a directory with the module's name exists in src/, it's local.
    """
    return os.path.isdir(os.path.join('src', module))

# --- Main Execution ---
if __name__ == "__main__":
    all_imports = set()
    std_libs = get_std_libs()

    # Find all Python files in the repository, excluding venv
    for root, _, files in os.walk("."):
        if "venv" in root or ".git" in root:
            continue
        for name in files:
            if name.endswith(".py"):
                file_path = os.path.join(root, name)
                all_imports.update(find_imports(file_path, std_libs))

    # Print sorted list of unique imports
    for imp in sorted(list(all_imports)):
        print(imp)
