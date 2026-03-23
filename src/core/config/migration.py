"""
SyncroJob - Config Migration
Logica di migrazione per vecchie configurazioni.
"""

import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

from platformdirs import user_data_dir

from src.core.constants import FileNames

APP_NAME = "SyncroJob"
CONFIG_DIR = Path(user_data_dir(APP_NAME, appauthor=False))


def deep_update_paths(data: Any, old_path: str, new_path: str) -> Any:  # noqa: ANN401
    """Sostituisce ricorsivamente i puntamenti ai vecchi percorsi nelle stringhe."""
    if isinstance(data, str):
        updated = data.replace(old_path.replace("/", ""), new_path.replace("/", ""))
        return updated.replace(old_path.replace("", "/"), new_path.replace("", "/"))
    if isinstance(data, dict):
        return {k: deep_update_paths(v, old_path, new_path) for k, v in data.items()}
    if isinstance(data, list):
        return [deep_update_paths(i, old_path, new_path) for i in data]
    return data


def check_and_migrate_local_config(base_dir: Path, load_base_func: Any, atomic_write_func: Any) -> bool:  # noqa: ANN401
    """Cerca file config.json fuori dalla cartella standard e lo migra."""
    app_dir = Path(sys.executable).parent if getattr(sys, "frozen", False) else base_dir
    legacy_app_names = ["SyncroJob"]
    potential_dirs = [
        app_dir,
        Path(user_data_dir(APP_NAME, appauthor=False, roaming=True)),
    ]

    local_appdata = Path(os.environ.get("LOCALAPPDATA", ""))
    if local_appdata:
        for old_name in legacy_app_names:
            if old_name != APP_NAME:
                potential_dirs.extend(
                    (local_appdata / old_name, local_appdata / "GiancarloAllegretti" / old_name)
                )

    roaming_appdata = Path(os.environ.get("APPDATA", ""))
    if roaming_appdata:
        potential_dirs.extend(roaming_appdata / old_name for old_name in legacy_app_names)

    migrated = False
    for legacy_dir in potential_dirs:
        legacy_config_file = legacy_dir / FileNames.CONFIG
        if legacy_config_file.exists() and legacy_dir.resolve() != CONFIG_DIR.resolve():
            try:
                CONFIG_DIR.mkdir(parents=True, exist_ok=True)
                with legacy_config_file.open("r", encoding="utf-8") as f:
                    old_config = json.load(f)

                old_path_str = str(legacy_dir)
                new_path_str = str(CONFIG_DIR)
                migrated_config = deep_update_paths(old_config, old_path_str, new_path_str)

                current_config = load_base_func()
                for key, value in migrated_config.items():
                    if key not in current_config or not current_config[key]:
                        current_config[key] = value

                atomic_write_func(current_config, CONFIG_DIR / FileNames.CONFIG)
                print(f"[MIGRATION] Config merged and paths updated from {legacy_dir}")

                legacy_data = legacy_dir / "data"
                target_data = CONFIG_DIR / "data"
                if legacy_data.exists():
                    shutil.copytree(legacy_data, target_data, dirs_exist_ok=True)
                    print(f"[MIGRATION] Data folder merged from {legacy_dir}")

                migrated = True
                break
            except Exception as e:
                print(f"[MIGRATION] Error during migration from {legacy_dir}: {e}")

    return migrated


def migrate_legacy_keys(config: dict[str, Any]) -> bool:
    """Migra le vecchie chiavi nel nuovo formato accounts."""
    if "isab_username" not in config or not config.get("isab_username"):
        return False

    old_user = config["isab_username"]
    if not any(a.get("username") == old_user for a in config.get("accounts", [])):
        if "accounts" not in config:
            config["accounts"] = []
        config["accounts"].append(
            {
                "username": old_user,
                "password": config.get("isab_password", ""),
                "default": True,
            }
        )

    del config["isab_username"]
    config.pop("isab_password", None)
    return True
