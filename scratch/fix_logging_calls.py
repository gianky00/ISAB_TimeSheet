"""Script di utilità per correggere le chiamate di logging obsolete nel codice sorgente."""

import os
import re
from pathlib import Path

# Lista dei file trovati con grep
files_to_fix = [
    r"src\gui\workers\pdl_io_worker.py",
    r"src\gui\workers\oda_io_worker.py",
    r"src\gui\widgets\pdl\status_bar_widget.py",
    r"src\gui\widgets\pdl\table_widget.py",
    r"src\gui\widgets\dashboard\roi_widget.py",
    r"src\gui\widgets\dashboard\pdl_stats_widget.py",
    r"src\gui\panels\dipendenti\utils\report_generator.py",
    r"src\gui\panels\dipendenti\shared.py",
    r"src\gui\styles\theme_manager.py",
    r"src\gui\dialogs\splash_standalone.py",
    r"src\gui\main_window\controllers\monitoring_controller.py",
    r"src\core\backup_manager.py",
    r"src\core\license_validator.py",
    r"src\core\preventivi_manager.py",
    r"src\core\pdl\pdl_controller.py",
    r"src\core\search\search_service.py",
    r"src\core\license_updater.py",
    r"src\core\logging\decorators.py",
    r"src\core\employees.py",
    r"src\core\importers\contabilita.py",
    r"src\core\importers\pdl_sync_manager.py",
    r"src\core\contabilita_search.py",
    r"src\core\contabilita_manager.py",
    r"src\bots\portale_fornitori\timbrature\storage.py",
    r"src\core\contabilita\consuntivo\consuntivo_controller.py",
    r"src\bots\safework\pdl\bot.py",
    r"src\core\audit\manager.py",
    r"src\core\app_initializer.py",
]

pattern = re.compile(r"(logger\.exception\(.*),\s*exc=e\)")

for rel_path in files_to_fix:
    abs_path = Path(os.getcwd()) / rel_path
    if not abs_path.exists():
        print(f"File not found: {rel_path}")
        continue

    with open(abs_path, encoding="utf-8") as f:
        content = f.read()

    new_content = pattern.sub(r"\1)", content)

    if new_content != content:
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed: {rel_path}")
    else:
        print(f"No changes needed for: {rel_path}")
