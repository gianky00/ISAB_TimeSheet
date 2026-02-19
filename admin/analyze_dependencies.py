"""
Dependency Analyzer for PyInstaller/PyArmor (NUCLEAR OPTION)
Scansiona il progetto in modo aggressive per trovare TUTTE le dipendenze possibili.
"""

import ast
import sys
from pathlib import Path


def get_all_imports(script_path, src_path):
    print("[ANALYZER] ☢️  Avvio Analisi Totale Dipendenze (AST Optimized)...")
    print(f"[ANALYZER] Script: {script_path}")
    print(f"[ANALYZER] Src: {src_path}")

    found_modules = set()

    # 1. Analisi AST (Abstract Syntax Tree) su tutto il progetto
    # Questo trova importazioni anche in file non direttamente toccati da main.py
    # È molto più robusto di ModuleFinder su Python 3.12+
    print("[ANALYZER] 🔍 Scansione AST ricorsiva su tutto il progetto...")

    # Includiamo anche main.py e altri script in root
    root_dir = Path(script_path).parent
    search_dirs = [root_dir / "src", root_dir]

    for s_dir in search_dirs:
        if not s_dir.exists():
            continue

        for path in s_dir.rglob("*.py"):
            # Saltiamo cartelle di sistema o cache
            if any(part in str(path) for part in [".venv", "node_modules", ".git", "__pycache__"]):
                continue

            try:
                with path.open(encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            found_modules.add(alias.name.split(".")[0])
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        found_modules.add(node.module.split(".")[0])
            except Exception:
                continue

    # 2. Inclusione Forzata di Famiglie Critiche (Deep Expansion)
    critical_families = {
        "cryptography": [
            "cryptography",
            "cryptography.fernet",
            "cryptography.hazmat",
            "cryptography.hazmat.primitives",
            "cryptography.x509",
        ],
        "pandas": ["pandas", "pandas._libs", "pandas.io.formats.style", "pyarrow"],
        "matplotlib": [
            "matplotlib",
            "matplotlib.backends",
            "matplotlib.pyplot",
            "matplotlib.backends.backend_qtagg",
            "matplotlib.backends.backend_qt5agg",
        ],
        "PyQt6": [
            "PyQt6",
            "PyQt6.QtCore",
            "PyQt6.QtGui",
            "PyQt6.QtWidgets",
            "PyQt6.QtPrintSupport",
            "PyQt6.QtSvg",
            "PyQt6.QtNetwork",
        ],
        "selenium": [
            "selenium",
            "selenium.webdriver",
            "selenium.webdriver.chrome",
            "selenium.webdriver.common",
            "selenium.webdriver.support",
        ],
        "telegram": ["telegram", "telegram.ext", "telegram.error"],
        "pandera": ["pandera", "pandera.backends", "pandera.engines"],
        "win32": ["win32api", "win32print", "win32com", "win32con", "win32gui"],
        "openpyxl": ["openpyxl"],
        "requests": ["requests", "urllib3", "idna", "certifi", "charset_normalizer"],
        "PIL": ["PIL", "PIL.Image"],
        "fitz": ["fitz"],
        "keyring": ["keyring", "keyring.backends"],
    }

    print("[ANALYZER] 🛡️  Espansione moduli e pulizia...")

    final_imports = set()

    # Espansione basata sulle famiglie
    for module in list(found_modules):
        if module in critical_families:
            final_imports.update(critical_families[module])
        else:
            final_imports.add(module)

    # Clean up
    cleaned_imports = set()
    excluded_roots = {"src", "tests", "admin", "scripts", "drivers"}

    for imp in final_imports:
        root_mod = imp.split(".")[0]
        if root_mod in excluded_roots:
            continue
        if root_mod in sys.builtin_module_names:
            continue
        if imp.startswith("_"):
            continue
        cleaned_imports.add(imp)

    print(f"[ANALYZER] ✅ Identificati {len(cleaned_imports)} moduli univoci.")
    return sorted(cleaned_imports)


if __name__ == "__main__":
    # Test run
    root = Path(__file__).parent.parent.resolve()
    main_py_file = root / "main.py"
    src_dir_path = root / "src"

    imports_list = get_all_imports(main_py_file, src_dir_path)
    print("\n[ANALYZER] LISTA FINALE Hidden Imports:")
    for i in imports_list:
        print(f"  --hidden-import {i}")
