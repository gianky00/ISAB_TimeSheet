"""
SyncroJob - Account Manager
Gestione degli account nella configurazione.
"""

from contextlib import suppress
from typing import Any

from src.core.secrets_manager import SecretsManager


def add_account_logic(
    config: dict[str, Any], username: str, password: str, is_default: bool = False, account_type: str = ""
) -> dict[str, Any]:
    """Logica per aggiungere o aggiornare un account in una configurazione."""
    key = "accounts" if not account_type else "safework_accounts"
    accounts = config.get(key, [])

    if not accounts:
        is_default = True

    # Trova account esistente per preservare altri campi
    existing: dict[str, Any] = next((a for a in accounts if a.get("username") == username), {})

    accounts = [a for a in accounts if a.get("username") != username]

    if is_default:
        for acc in accounts:
            acc["default"] = False

    new_acc = existing.copy()
    new_acc.update({"username": username, "password": password, "default": is_default})
    if account_type:
        new_acc["type"] = account_type

    accounts.append(new_acc)
    config[key] = accounts
    return config


def remove_account_logic(config: dict[str, Any], username: str) -> dict[str, Any]:
    """Logica per rimuovere un account da una configurazione."""
    accounts = config.get("accounts", [])
    config["accounts"] = [a for a in accounts if a.get("username") != username]

    with suppress(Exception):
        if SecretsManager.is_available():
            SecretsManager.delete_credential("isab_portal", username)

    if config["accounts"] and not any(a.get("default") for a in config["accounts"]):
        config["accounts"][0]["default"] = True

    return config


def set_default_account_logic(config: dict[str, Any], username: str, bot_type: str = "isab") -> bool:
    """Logica per impostare un account come default per il tipo specificato."""
    key = "accounts" if bot_type == "isab" else "safework_accounts"
    accounts = config.get(key, [])

    found = False
    for acc in accounts:
        acc["default"] = acc.get("username") == username
        if acc["default"]:
            found = True
    return found


def switch_default_account_logic(
    config: dict[str, Any], service_type: str = "isab"
) -> tuple[bool, str | None]:
    """Logica circular switch degli account di default."""
    key = "accounts" if service_type == "isab" else "safework_accounts"
    accounts = config.get(key, [])

    if len(accounts) < 2:
        return False, None

    current_idx = -1
    for i, acc in enumerate(accounts):
        if acc.get("default"):
            current_idx = i
            break

    if current_idx == -1:
        current_idx = 0

    next_idx = (current_idx + 1) % len(accounts)

    for i, acc in enumerate(accounts):
        acc["default"] = i == next_idx

    return True, accounts[next_idx].get("username")
