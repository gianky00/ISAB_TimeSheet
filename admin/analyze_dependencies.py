"""
Dependency Analyzer for PyInstaller/PyArmor (NUCLEAR OPTION)
Scansiona il progetto in modo aggressive per trovare TUTTE le dipendenze possibili.
"""

import ast
import contextlib
import sys
from modulefinder import ModuleFinder
from pathlib import Path


def get_all_imports(script_path, src_path):
    print("[ANALYZER] ☢️  Avvio Analisi Totale Dipendenze...")
    print(f"[ANALYZER] Script: {script_path}")
    print(f"[ANALYZER] Src: {src_path}")

    # 1. Analisi Statica (ModuleFinder)
    # Aggiungi src al path
    sys.path.insert(0, str(src_path))

    finder = ModuleFinder(path=sys.path)
    finder.run_script(str(script_path))

    found_modules = set()

    # 2. Analisi AST (Abstract Syntax Tree) su tutto il progetto
    # Questo trova importazioni anche in file non direttamente toccati da main.py
    print("[ANALYZER] 🔍 Scansione AST ricorsiva su 'src'...")
    src_dir = Path(src_path)
    for path in src_dir.rglob("*.py"):
        with contextlib.suppress(Exception):
            with path.open(encoding="utf-8") as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        found_modules.add(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom) and node.module:
                    found_modules.add(node.module.split(".")[0])

    # 3. Inclusione Forzata di Famiglie Critiche
    critical_families = {
        "cryptography": [
            "cryptography",
            "cryptography.fernet",
            "cryptography.hazmat",
            "cryptography.hazmat.backends",
            "cryptography.hazmat.backends.openssl",
            "cryptography.hazmat.bindings",
            "cryptography.hazmat.primitives",
            "cryptography.hazmat.primitives.kdf",
            "cryptography.hazmat.primitives.kdf.pbkdf2",
            "cryptography.hazmat.primitives.kdf.scrypt",
            "cryptography.hazmat.primitives.ciphers",
            "cryptography.hazmat.primitives.ciphers.algorithms",
            "cryptography.hazmat.primitives.ciphers.modes",
            "cryptography.x509",
        ],
        "pandas": ["pandas", "pandas._libs", "pandas.io.formats.style"],
        "matplotlib": [
            "matplotlib",
            "matplotlib.backends",
            "matplotlib.pyplot",
            "matplotlib.backends.backend_qtagg",
        ],
        "PyQt6": [
            "PyQt6",
            "PyQt6.QtCore",
            "PyQt6.QtGui",
            "PyQt6.QtWidgets",
            "PyQt6.QtPrintSupport",
            "PyQt6.QtSvg",
            "PyQt6.QtNetwork",
            "PyQt6.QtWebEngineCore",
            "PyQt6.QtWebEngineWidgets",
        ],
        "selenium": [
            "selenium",
            "selenium.webdriver",
            "selenium.webdriver.common",
            "selenium.webdriver.support",
        ],
        "telegram": [
            "telegram",
            "telegram.ext",
            "telegram.error",
            "telegram.constants",
        ],
        "pandera": ["pandera", "pandera.backends", "pandera.api", "pandera.engines"],
        "win32": [
            "win32api",
            "win32print",
            "win32com",
            "win32con",
            "win32gui",
            "win32process",
        ],
        "openpyxl": ["openpyxl"],
        "requests": ["requests", "urllib3", "idna", "certifi", "charset_normalizer"],
        "PIL": ["PIL", "PIL.Image", "PIL.ImageTk"],
        "fitz": ["fitz"],  # PyMuPDF
        "keyring": ["keyring", "keyring.backends", "keyring.util"],
    }

    print("[ANALYZER] 🛡️  Applicazione regole famiglie critiche...")

    # Merge dei risultati AST con quelli del ModuleFinder
    for name in finder.modules:
        root_mod = name.split(".")[0]
        if root_mod not in sys.builtin_module_names:
            found_modules.add(root_mod)

    final_imports = set()

    # Espansione basata sulle famiglie
    for module in list(found_modules):
        if module in critical_families:
            print(f"  -> Espansione famiglia critica: {module}")
            final_imports.update(critical_families[module])
        else:
            final_imports.add(module)

    # Clean up
    cleaned_imports = set()
    for imp in final_imports:
        if imp.startswith("src"):
            continue
        if imp in sys.builtin_module_names:
            continue
        if imp.startswith("_"):
            continue  # Skip internal modules usually
        cleaned_imports.add(imp)

    print(f"[ANALYZER] ✅ Identificati {len(cleaned_imports)} moduli univoci da includere.")
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
