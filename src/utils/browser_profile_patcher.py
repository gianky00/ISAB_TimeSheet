"""
SyncroJob - Browser Profile Patcher
Utility per forzare le impostazioni di sicurezza e privacy nel profilo Chromium.
Risolve il problema dei popup nativi "Password Compromessa" e "Leak Detection".
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger("ProfilePatcher")


def patch_browser_profile(user_data_dir: Path | str) -> bool:
    """
    Applica patch aggressive al file Preferences del profilo Chromium per disabilitare
    il gestore password, il rilevamento dei leak e altre notifiche bloccanti.
    """
    user_data_path = Path(user_data_dir)

    # In launch_persistent_context di Playwright, il file Preferences è solitamente
    # in 'Default/Preferences' o direttamente nella root se il profilo è minimale.
    # Proviamo a patchare entrambi, o a creare 'Default/Preferences' se nessuno esiste.
    preferred_path = user_data_path / "Default" / "Preferences"
    preferences_paths = [
        preferred_path,
        user_data_path / "Preferences",
        user_data_path / "Local State",  # Alcune impostazioni sono globali
    ]

    # Se nessuno dei due file di preferenze esiste, forziamo la creazione di quello standard
    if not any(
        (user_data_path / "Default" / "Preferences").exists() or (user_data_path / "Preferences").exists()
        for p in preferences_paths
    ):
        _patch_file(preferred_path)

    success = False
    for pref_path in preferences_paths:
        if _patch_file(pref_path):
            success = True

    return success


def _patch_file(path: Path) -> bool:
    """Legge, modifica e sovrascrive il file JSON delle preferenze. Crea il file se non esiste."""
    try:
        data: dict[str, Any] = {}
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)

        # Mappa delle preferenze critiche da forzare a False
        overrides = {
            # Gestione Password (Root e Profile)
            "password_manager.enabled": False,
            "password_manager.google_password_manager_enabled": False,
            "password_manager.leak_detection_check_enabled": False,
            "password_manager.password_leak_detection_enabled": False,
            "password_manager.password_check_enabled": False,
            "password_manager.compromised_credentials_check_enabled": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "profile.password_manager_leak_detection_check_enabled": False,
            "credentials_enable_service": False,
            "credentials_enable_autosignin": False,
            # Autofill e Privacy
            "autofill.profile_enabled": False,
            "autofill.credit_card_enabled": False,
            "autofill.enabled": False,
            "safebrowsing.enabled": False,
            "safebrowsing.enhanced": False,
            "signin.allowed": False,
            "sync.managed": True,  # Blocca la sincronizzazione
            "profile.nickname": "SyncroJob-Bot",
            "plugins.always_open_pdf_externally": True,
        }

        modified = False
        for key, value in overrides.items():
            if _set_nested_value(data, key, value):
                modified = True

        if modified or not path.exists():
            with path.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"[OK] Patch applicata con successo a: {path}")
            return True
    except Exception:
        logger.exception(f"[ERRORE] Errore durante il patching di {path}")
        return False
    return False


def _set_nested_value(dic: dict[str, Any], keys: str, value: Any) -> bool:
    """
    Imposta un valore in un dizionario annidato usando la dot notation (es. 'a.b.c').
    Ritorna True se il valore è stato cambiato o aggiunto.
    """
    parts = keys.split(".")
    current = dic

    for part in parts[:-1]:
        if part not in current or not isinstance(current[part], dict):
            current[part] = {}
        current = current[part]

    last_key = parts[-1]
    if last_key not in current or current[last_key] != value:
        current[last_key] = value
        return True

    return False
