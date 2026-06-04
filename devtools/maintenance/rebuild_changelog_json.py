"""
SyncroJob - Rebuild Changelog JSON Utility
Utility script to parse CHANGELOG.md and rebuild the complete core/changelog.json history.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

MAX_SCOPE_LEN = 15


def _get_current_version() -> str:
    """Legge la versione corrente del software da src/application/services/version.py."""
    version_file = Path(__file__).resolve().parent.parent / "src" / "core" / "version.py"
    if version_file.exists():
        content = version_file.read_text(encoding="utf-8")
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    return "1.47.0"


def _clean_and_format_note(
    note_text: str, current_category: str, raw_cat: str, cat_map: dict[str, str]
) -> str:
    """Pulisce il testo del commit e aggiunge il prefisso di categoria opportuno."""
    prefix = f"{current_category}:"
    clean_note = note_text

    if note_text.lower().startswith(prefix.lower()):
        clean_note = note_text[len(prefix) :].strip()
    elif ":" in note_text:
        parts = note_text.split(":", 1)
        scope = parts[0].strip()
        msg = parts[1].strip()
        if len(scope) < MAX_SCOPE_LEN and (
            scope.lower().startswith(raw_cat) or scope.lower() in cat_map
        ):
            clean_note = msg

    return f"{current_category}: {clean_note}"


def _detect_version_and_date(line: str, version_pattern: re.Pattern[str]) -> tuple[str, str] | None:
    """Rileva se la riga rappresenta un'intestazione di versione, restituendo (versione, data) o None."""
    if line.lower().startswith("## unreleased") or line.lower().startswith("## [unreleased]"):
        version = _get_current_version()
        date = datetime.now().strftime("%Y-%m-%d")
        return version, date

    version_match = version_pattern.match(line)
    if version_match:
        version = version_match.group(1)
        date = version_match.group(2) or "N/D"
        return version, date

    return None


def _parse_changelog_content(content: str) -> list[dict[str, Any]]:
    """Analizza il contenuto testuale del changelog e restituisce le release strutturate."""
    lines = [line.strip() for line in content.splitlines() if line.strip()]

    releases: list[dict[str, Any]] = []
    current_release: dict[str, Any] = {}
    current_category: str = ""
    raw_cat: str = ""

    # Regex per catturare intestazioni di versione, es. "## v1.46.0 (2026-05-12)"
    version_pattern = re.compile(r"^##\s+v?(\d+\.\d+\.\d+)(?:\s+\((\d{4}-\d{2}-\d{2})\))?")
    # Regex per catturare categorie di note, es. "### Feat"
    category_pattern = re.compile(r"^###\s+(\w+)")

    cat_map = {
        "feat": "Feat",
        "fix": "Fix",
        "refactor": "Refactor",
        "perf": "Perf",
        "docs": "Docs",
        "chore": "Chore",
        "style": "Style",
        "test": "Test",
    }

    for line in lines:
        # 1. Rilevamento Intestazione Versione (standard o Unreleased)
        version_info = _detect_version_and_date(line, version_pattern)
        if version_info:
            version, date = version_info

            if current_release and current_release.get("notes"):
                releases.append(current_release)

            current_release = {"version": version, "date": date, "notes": []}
            current_category = ""
            raw_cat = ""
            continue

        if not current_release:
            continue

        # 2. Rilevamento Categoria
        category_match = category_pattern.match(line)
        if category_match:
            raw_cat = category_match.group(1).lower()
            current_category = cat_map.get(raw_cat, raw_cat.capitalize())
            continue

        # 3. Rilevamento Nota (Bullet Point)
        if line.startswith(("- ", "* ")) and current_category:
            note_text = line[2:].strip()
            if note_text:
                formatted_note = _clean_and_format_note(
                    note_text, current_category, raw_cat, cat_map
                )
                current_release["notes"].append(formatted_note)

    if current_release and current_release.get("notes"):
        releases.append(current_release)

    return releases


def rebuild_changelog() -> None:
    """Parses CHANGELOG.md and generates a comprehensive src/application/services/changelog.json."""
    root_dir = Path(__file__).resolve().parent.parent
    changelog_md_path = root_dir / "CHANGELOG.md"
    changelog_json_path = root_dir / "src" / "core" / "changelog.json"

    if not changelog_md_path.exists():
        print(f"Errore: {changelog_md_path} non esiste.")
        return

    content = changelog_md_path.read_text(encoding="utf-8")
    releases = _parse_changelog_content(content)

    # Scrittura su changelog.json
    changelog_json_path.parent.mkdir(parents=True, exist_ok=True)
    changelog_json_path.write_text(
        json.dumps(releases, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        f"Successo: Ricreato lo storico changelog. json generato in {changelog_json_path} con {len(releases)} release indicizzate."
    )


if __name__ == "__main__":
    rebuild_changelog()
