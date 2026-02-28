"""
SyncroJob - Account Manager
Gestione degli account nella configurazione.
"""

from contextlib import suppress
from typing import Any

from src.core.secrets_manager import SecretsManager


def add_account_logic(
    config: dict[str, Any], username: str, password: str, is_default: bool = False
) -> dict[str, Any]:
    """Logica per aggiungere o aggiornare un account in una configurazione."""
    accounts = config.get("accounts", [])

    if not accounts:
        is_default = True

    accounts = [a for a in accounts if a.get("username") != username]

    if is_default:
        for acc in accounts:
            acc["default"] = False

    accounts.append({"username": username, "password": password, "default": is_default})
    config["accounts"] = accounts
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


def set_default_account_logic(config: dict[str, Any], username: str) -> bool:
    """Logica per impostare un account come default."""
    accounts = config.get("accounts", [])
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
