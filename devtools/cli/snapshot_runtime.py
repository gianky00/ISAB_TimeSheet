#!/usr/bin/env python
"""Crea uno snapshot di %LOCALAPPDATA%/SyncroJob nel repo (cartella runtime/).

Copia database, config, licenza e chiavi di cifratura. Esclude log, driver,
profilo Chrome e cache. Le password del keyring vengono salvate in config.json
come ENC:v2 (mai in chiaro).
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.application.services.secrets_manager import SecretsManager  # noqa: E402
from src.infrastructure.utils.security import password_manager  # noqa: E402

SKIP_DIR_NAMES = frozenset({"logs", "drivers", "temp", "chrome_profile", "backups"})
SKIP_FILE_SUFFIXES = frozenset({".log", ".db-shm", ".db-wal"})
SKIP_FILE_NAMES = frozenset({"crash.txt"})


def _appdata_root() -> Path:
    local = Path.home() / "AppData" / "Local" / "SyncroJob"
    roaming = Path.home() / "AppData" / "Roaming" / "SyncroJob"
    if local.exists():
        return local
    if roaming.exists():
        return roaming
    raise FileNotFoundError("Cartella SyncroJob non trovata in LocalAppData/AppData.")


def _should_skip(path: Path, source_root: Path) -> bool:
    relative_parts = path.relative_to(source_root).parts
    if any(part in SKIP_DIR_NAMES for part in relative_parts):
        return True
    return path.is_file() and (path.name in SKIP_FILE_NAMES or path.suffix in SKIP_FILE_SUFFIXES)


def _copy_tree(source_root: Path, dest_root: Path) -> int:
    copied = 0
    dest_root.mkdir(parents=True, exist_ok=True)
    for item in source_root.rglob("*"):
        if _should_skip(item, source_root):
            continue
        relative = item.relative_to(source_root)
        target = dest_root / relative
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        copied += 1
    return copied


def _embed_encrypted_passwords(config_path: Path) -> int:
    if not config_path.exists():
        return 0

    with config_path.open(encoding="utf-8") as handle:
        config = json.load(handle)

    embedded = 0
    account_groups = (
        ("accounts", "isab_portal"),
        ("safework_accounts", "safework_portal"),
    )
    for key, service in account_groups:
        for account in config.get(key, []):
            username = account.get("username")
            if not username:
                continue
            password = SecretsManager.get_credential(service, username)
            if not password:
                continue
            account["password"] = password_manager.encrypt(password)
            embedded += 1

    with config_path.open("w", encoding="utf-8") as handle:
        json.dump(config, handle, indent=4, ensure_ascii=False)
        handle.write("\n")
    return embedded


def main() -> int:
    """Esegue lo snapshot runtime nel repository."""
    source = _appdata_root()
    dest = PROJECT_ROOT / "runtime"
    restore_script = dest / "restore_to_appdata.ps1"
    restore_backup = restore_script.read_text(encoding="utf-8") if restore_script.exists() else None

    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)

    copied = _copy_tree(source, dest)
    embedded = _embed_encrypted_passwords(dest / "config.json")
    if restore_backup:
        restore_script.write_text(restore_backup, encoding="utf-8")

    print(f"Snapshot creato in {dest}")
    print(f"File copiati: {copied}")
    print(f"Password cifrate incorporate: {embedded}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
