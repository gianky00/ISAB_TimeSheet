"""
SyncroJob - Config Security
Gestione della protezione delle credenziali.
"""

from contextlib import suppress
from typing import Any

from src.core.secrets_manager import SecretsManager


def decrypt_all_credentials(config: dict[str, Any]) -> None:
    """Decripta le credenziali per tutti i tipiùdi account configurati."""
    _decrypt_account_list(config.get("accounts", []), "isab_portal")
    _decrypt_account_list(config.get("safework_accounts", []), "safework_portal")


def _decrypt_account_list(accounts: list[dict[str, Any]], service_name: str) -> None:
    """Decripta una lista di account usando keyring o fallback locale."""
    if not accounts:
        return

    from src.utils.security import password_manager  # noqa: PLC0415

    for acc in accounts:
        username = acc.get("username")
        if not username:
            continue

        # Ottimizzazione: Se abbiamo già una password in chiaro (es. appena inserita o già decriptata), non andare su Keyring
        current_pw = acc.get("password", "")
        if current_pw and not current_pw.startswith("ENC:v2:"):
            continue

        # Tenta recuperòda Keyring
        pw_keyring = SecretsManager.get_credential(service_name, username)
        if pw_keyring:
            acc["password"] = pw_keyring
            continue

        if current_pw and current_pw.startswith("ENC:v2:"):
            with suppress(Exception):
                acc["password"] = password_manager.decrypt(current_pw)


def encrypt_all_credentials(config: dict[str, Any]) -> None:
    """Gestisce la protezione delle credenziali prima del salvataggio."""
    _encrypt_account_list(config.get("accounts", []), "isab_portal")
    _encrypt_account_list(config.get("safework_accounts", []), "safework_portal")


def _encrypt_account_list(accounts: list[dict[str, Any]], service_name: str) -> None:
    """Sposta in keyring o cripta localmente le password di una lista di account."""
    if not accounts:
        return

    from src.utils.security import password_manager  # noqa: PLC0415

    for acc in accounts:
        password = acc.get("password")
        username = acc.get("username")

        # Se non c'è password (perché già in keyring e rimosso dalla coda), salta
        if not password:
            continue

        if not username:
            continue

        with suppress(Exception):
            if SecretsManager.is_available():
                SecretsManager.store_credential(service_name, username, password)
                # Una volta in keyring, la rimuoviamo dal dizionario per il salvataggio JSON
                acc.pop("password", None)
                continue

        # Se keyring non disponibile, cripta localmente
        acc["password"] = password_manager.encrypt(password)
