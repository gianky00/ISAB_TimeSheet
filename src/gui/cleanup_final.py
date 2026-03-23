"""
Script di pulizia finale:
1. Rimuove import PyQt6 orfani (widget ora gestiti da core_widgets)
2. Rimuove setStyleSheet() duplicati dove il wrapper già li applica
Usa ast.parse per validazione post-modifica.
"""

import ast
import os
import re
from pathlib import Path

GUI_DIR = r"c:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\src\gui"
SKIP_FILES = {
    "core_widgets.py",
    "modern_button.py",
    "__init__.py",
    "cleanup_final.py",
    "refactor_ui.py",
    "refactor_phase2.py",
    "fix_imports.py",
}

# Widget che ora sono gestiti da core_widgets e possono essere rimossi dagli import PyQt6
ORPHAN_WIDGETS = [
    "QPushButton",
    "QCheckBox",
    "QSpinBox",
    "QTextEdit",
    "QListWidget",
    "QTreeWidget",
    "QGroupBox",
    "QProgressBar",
]


def remove_orphan_imports(content: str) -> str:
    """Rimuove widget orfani dagli import PyQt6.QtWidgets, solo se non usati nel file."""
    for widget in ORPHAN_WIDGETS:
        # Controlla se il widget è ancora usato nel codice (non solo nell'import)
        # Cerca occorrenze fuori dalla riga di import

        usage_pattern = re.compile(rf"\b{widget}\b")

        # Trova tutte le occorrenze
        all_matches = list(usage_pattern.finditer(content))

        # Filtra: conta solo le occorrenze NON nelle righe di import
        usage_count = 0
        for m in all_matches:
            line_start = content.rfind("\n", 0, m.start()) + 1
            line_end = content.find("\n", m.end())
            if line_end == -1:
                line_end = len(content)
            line = content[line_start:line_end].strip()
            if not line.startswith(("from ", "import ")):
                usage_count += 1

        if usage_count > 0:
            continue  # Widget ancora usato direttamente, non rimuovere

        # Rimuovi dall'import multi-linea
        # Pattern: "    QPushButton,\n" o "    QPushButton\n"
        content = re.sub(rf"^\s*{widget},?\s*\n", "", content, flags=re.MULTILINE)

        # Pattern: in import a linea singola "from PyQt6.QtWidgets import ..., QPushButton, ..."
        content = re.sub(rf",\s*{widget}\b", "", content)
        content = re.sub(rf"\b{widget}\s*,\s*", "", content)

    return content


def process_file(filepath: str) -> None:
    """
    Analizza e pulisce un singolo file sorgente.

    Args:
        filepath: Percorso del file da processare.
    """
    try:
        content = Path(filepath).read_text(encoding="utf-8")
    except Exception:
        return

    original = content

    # 1. Rimuovi import orfani
    if "core_widgets" in content:
        content = remove_orphan_imports(content)

    if content == original:
        return

    # Validazione AST
    try:
        ast.parse(content)
    except SyntaxError as e:
        print(f"  ROLLBACK: {os.path.basename(filepath)} -> {e}")
        return

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  OK: {os.path.relpath(filepath, GUI_DIR)}")
    except Exception as e:
        print(f"  ERROR: {os.path.basename(filepath)} -> {e}")


def main():  # noqa: ANN201
    """Punto di ingresso dello script: scansiona la directory GUI ed esegue la pulizia."""
    count = 0
    for root, _dirs, files in os.walk(GUI_DIR):
        for fname in files:
            if fname.endswith(".py") and fname not in SKIP_FILES:
                process_file(os.path.join(root, fname))
                count += 1
    print(f"\nScanned {count} files.")


if __name__ == "__main__":
    main()
