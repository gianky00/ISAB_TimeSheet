"""Script di pulizia finale.

1. Rimuove import PySide6 orfani (widget ora gestiti da core_widgets)
2. Rimuove setStyleSheet() duplicati dove il wrapper già li applica
Usa ast.parse per validazione post-modifica.
"""

import ast
import os
import re
from pathlib import Path

GUI_DIR = str(Path(__file__).parent)
SKIP_FILES = {
    "core_widgets.py",
    "modern_button.py",
    "__init__.py",
    "cleanup_final.py",
    "refactor_ui.py",
    "refactor_phase2.py",
    "fix_imports.py",
}

# Widget che ora sono gestiti da core_widgets e possono essere rimossi dagli import PySide6
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
    """Rimuove widget orfani dagli import PySide6.QtWidgets, solo se non usati nel file.

    Usa AST per una rilevazione robusta degli utilizzi reale.
    """
    try:
        tree = ast.parse(content)
        # Raccogliamo tutti i nomi utilizzati nel codice (caricamenti, store, attributi, annotazioni)
        used_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                used_names.add(node.id)
            elif isinstance(node, ast.Attribute):
                used_names.add(node.attr)
    except Exception:
        # In caso di errore di parsing (es. codice incompleto), restituiamo l'originale per sicurezza
        return content

    for widget in ORPHAN_WIDGETS:
        # Se il widget è effettivamente utilizzato nel codice, lo manteniamo
        if widget in used_names:
            continue

        # Altrimenti, procediamo con la rimozione testuale
        # 1. Rimozione dall'import multi-linea (es. all'interno di parentesi)
        # Pattern: "    QPushButton,\n" o "    QPushButton\n"
        # Usiamo [ \t]* invece di \s* per evitare di consumare accidentalmente i newline successivi
        content = re.sub(rf"^[ \t]*{widget},?[ \t]*\r?\n", "", content, flags=re.MULTILINE)

        # 2. Rimozione da import a linea singola "from ... import ..., QPushButton, ..."
        content = re.sub(rf",\s*{widget}\b", "", content)
        content = re.sub(rf"\b{widget}\s*,\s*", "", content)

    return content


def process_file(filepath: str) -> None:
    """Analizza e pulisce un singolo file sorgente.

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

    # Validazione AST post-modifica
    try:
        ast.parse(content)
    except SyntaxError as e:
        print(f" ROLLBACK: {os.path.basename(filepath)} -> {e}")
        return

    try:
        Path(filepath).write_text(content, encoding="utf-8")
        print(f" OK: {os.path.relpath(filepath, GUI_DIR)}")
    except Exception as e:
        print(f" ERROR: {os.path.basename(filepath)} -> {e}")


def main() -> None:
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
