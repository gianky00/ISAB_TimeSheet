"""
SyncroJob - License Updater
Modulo dedicato all'aggiornamento e alla sincronizzazione dei file di licenza dal repository GitHub.
Gestisce i periodi di grazia offline tramite token cifrati e garantisce la validità temporale del software.
"""

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import requests
from cryptography.fernet import Fernet

from src.core.logging import get_logger
from src.core.secrets_manager import SecretsManager

from . import config_manager, license_validator, time_manager

logger = get_logger(__name__)


def get_github_token() -> str:
    """
    Recupera il token GitHub tramite il gestore dei segreti.

    Returns:
        str: Il token di autenticazione GitHub.
    """
    return SecretsManager.get_github_token()


def get_license_dir() -> Path:
    """
    Restituisce il percorso assoluto della cartella Licenza all'interno dei dati utente.

    Returns:
        Path: Oggetto Path della directory licenza.
    """
    base_dir = Path(config_manager.get_data_path())
    return base_dir / "Licenza"


def _get_validity_token_path() -> Path:
    """Restituisce il percorso del file validity.token."""
    return get_license_dir() / "validity.token"


def _get_emergency_grace_token_path() -> Path:
    """Restituisce il percorso del file emergency_grace.token."""
    return get_license_dir() / "emergency_grace.token"


def update_grace_timestamp() -> None:
    """
    Cifra e salva il timestamp corrente dell'ultimo avvio online riuscito.
    Questo permette il funzionamento dell'applicazione offline per un periodo limitato.
    """
    try:
        token_path = _get_validity_token_path()
        current_time, _ = time_manager.get_trusted_time()

        cipher = Fernet(SecretsManager.get_grace_period_key())
        encrypted_time = cipher.encrypt(current_time.isoformat().encode("utf-8"))

        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_bytes(encrypted_time)

        emergency_token = _get_emergency_grace_token_path()
        if emergency_token.exists():
            emergency_token.unlink()
    except Exception as e:
        logger.warning(f"Errore aggiornamento timestamp: {e}")


def check_grace_period() -> bool:
    """
    Verifica se l'applicazione può funzionare offline controllando il token di validità.
    Il periodo di grazia massimo è di 3 giorni dall'ultima sincronizzazione online.

    Returns:
        bool: True se il periodo di grazia è valido.

    Raises:
        Exception: Se il token non esiste, è scaduto o è stata rilevata manipolazione oraria.
    """
    token_path = _get_validity_token_path()
    if not token_path.exists():
        raise Exception(
            "Nessuna validazione online precedente.\nConnessione internet richiesta per il primo avvio."
        )

    try:
        encrypted_data = token_path.read_bytes()
        cipher = Fernet(SecretsManager.get_grace_period_key())
        decrypted_data = cipher.decrypt(encrypted_data).decode("utf-8")
        last_online = datetime.fromisoformat(decrypted_data)

        now, _ = time_manager.get_trusted_time()
        now_utc = now.astimezone(UTC)
        last_online_utc = last_online.astimezone(UTC)

        if now_utc < last_online_utc - timedelta(minutes=5):
            raise Exception("Rilevata incoerenza orologio di sistema.")

        days_offline = (now_utc - last_online_utc).days
        if days_offline >= 3:
            raise Exception("Periodo di grazia offline (3 giorni) SCADUTO.\nConnettiti a internet.")

        return True
    except Exception as e:
        if any(x in str(e) for x in ("SCADUTO", "incoerenza", "Nessuna validazione")):
            raise
        raise Exception(f"Errore verifica periodo di grazia: {e}") from e


def check_emergency_grace_period() -> tuple[bool, str, int]:
    """
    Gestisce un periodo di grazia di emergenza (3 giorni) per licenze mancanti.
    Usato per consentire l'utilizzo immediato del software prima della sincronizzazione definitiva.

    Returns:
        tuple: (bool attivo, str messaggio, int giorni_rimanenti).
    """
    token_path = _get_emergency_grace_token_path()
    current_time, _ = time_manager.get_trusted_time()

    if not token_path.exists():
        try:
            cipher = Fernet(SecretsManager.get_grace_period_key())
            encrypted_start = cipher.encrypt(current_time.isoformat().encode("utf-8"))
            token_path.parent.mkdir(parents=True, exist_ok=True)
            token_path.write_bytes(encrypted_start)
            return True, "Periodo di grazia attivato (3 giorni)", 3
        except Exception as e:
            return False, f"Errore attivazione periodo di grazia: {e}", 0

    try:
        encrypted_data = token_path.read_bytes()
        cipher = Fernet(SecretsManager.get_grace_period_key())
        decrypted_data = cipher.decrypt(encrypted_data).decode("utf-8")
        start_time = datetime.fromisoformat(decrypted_data)

        now_utc = current_time.astimezone(UTC)
        start_utc = start_time.astimezone(UTC)

        if now_utc < start_utc - timedelta(minutes=60):
            return False, "Rilevata manipolazione orologio di sistema", 0

        elapsed = now_utc - start_utc
        if elapsed.days >= 3:
            return False, "Periodo di grazia di 3 giorni SCADUTO.", 0

        remaining_days = 3 - elapsed.days
        return True, f"Periodo di grazia attivo ({remaining_days} giorni rimanenti)", remaining_days
    except Exception as e:
        return False, f"Errore lettura periodo di grazia: {e}", 0


def is_running_from_source() -> bool:
    """Verifica se l'applicazione è in esecuzione dall'interprete Python (sorgenti)."""
    import sys

    return not getattr(sys, "frozen", False)


def is_license_folder_empty() -> bool:
    """Verifica la presenza dei file vitali di licenza (config.dat e manifest.json)."""
    license_dir = get_license_dir()
    if not license_dir.exists():
        return True
    config_dat = license_dir / "config.dat"
    manifest_json = license_dir / "manifest.json"
    return not (config_dat.exists() and manifest_json.exists())


def run_update() -> bool:
    """
    Esegue la procedura completa di aggiornamento licenza.
    Recupera l'Hardware ID, interroga le API di GitHub e scarica i file necessari se presenti o modificati.
    Gestisce proattivamente la revoca della licenza con validazione preventiva.
    """
    logger.info("Verifica stato licenza cloud...")
    hw_id = license_validator.get_hardware_id().strip().rstrip(".")
    license_dir = get_license_dir()

    if not _ensure_license_dir(license_dir):
        return False

    base_url = f"https://api.github.com/repos/gianky00/intelleo-licenses/contents/licenses/{hw_id}"
    token = get_github_token()
    headers_api = {"Authorization": f"token {token}"}
    headers_raw = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3.raw"}

    try:
        # 1. Verifica se la cartella hw_id esiste sul server (Revoca)
        dir_res = requests.get(base_url, headers=headers_api, timeout=10)

        if dir_res.status_code == 404:
            # Licenza rimossa dal server -> REVOCATA
            config_dat = license_dir / "config.dat"
            manifest_json = license_dir / "manifest.json"
            if config_dat.exists():
                config_dat.unlink()
            if manifest_json.exists():
                manifest_json.unlink()

            from src.core.app_initializer import AppInitializer

            logger.critical("Licenza REVOCATA dal server!")
            AppInitializer.add_alert("CRITICAL", "LICENZA REVOCATA DAL SERVER. Contattare l'amministratore.")
            raise Exception("LICENZA REVOCATA DAL SERVER. Contattare l'amministratore.")

        if dir_res.status_code != 200:
            logger.warning(f"Impossibile verificare la licenza cloud (HTTP {dir_res.status_code})")
            return False

        # 2. Scarica il manifest.json per controllare l'aggiornamento
        man_res = requests.get(f"{base_url}/manifest.json", headers=headers_raw, timeout=10)
        if man_res.status_code != 200:
            logger.warning("File manifest.json non trovato sul server.")
            return False

        remote_manifest_bytes = man_res.content
        remote_manifest = json.loads(remote_manifest_bytes.decode("utf-8"))
        remote_hash = remote_manifest.get("config.dat")

        local_config = license_dir / "config.dat"
        local_hash = ""
        local_status, _ = license_validator.get_detailed_license_status()

        if local_config.exists():
            from src.core.license_validator import _calculate_sha256

            local_hash = _calculate_sha256(local_config)

        # 3. Scarica config.dat solo se l'hash è diverso O se quella locale non è valida
        if local_hash != remote_hash or local_status != license_validator.LicenseStatus.VALID:
            logger.info("Rilevato aggiornamento o licenza locale non valida, download in corso...")
            conf_res = requests.get(f"{base_url}/config.dat", headers=headers_raw, timeout=10)
            if conf_res.status_code == 200:
                new_config_bytes = conf_res.content

                # --- SICUREZZA: Verifica la validità dei nuovi dati prima di sovrascrivere ---
                try:
                    from src.core.secrets_manager import SecretsManager

                    key_raw = SecretsManager.get_license_key()
                    if key_raw:
                        cipher = Fernet(key_raw)
                        # Tenta la decifratura in memoria
                        decrypted = cipher.decrypt(new_config_bytes).decode("utf-8")
                        payload = json.loads(decrypted)

                        # Verifica HWID matching
                        cur_hw = license_validator.get_hardware_id().strip().rstrip(".")
                        lic_hw = payload.get("Hardware ID", "").strip().rstrip(".")

                        if cur_hw != lic_hw and "UNKNOWN" not in cur_hw:
                            logger.error(
                                "La licenza sul cloud non corrisponde a questo Hardware ID. Update annullato."
                            )
                            return False
                    else:
                        logger.error("Impossibile recuperare la chiave di decifratura per la validazione.")
                        return False
                except Exception as ve:
                    logger.error(
                        f"La nuova licenza sul cloud è corrotta o non valida ({ve}). Update annullato."
                    )
                    return False
                # ----------------------------------------------------------------------------

                files = {"manifest.json": remote_manifest_bytes, "config.dat": new_config_bytes}
                saved = _save_license_files(license_dir, files)
                if saved:
                    from src.core.app_initializer import AppInitializer

                    AppInitializer.add_alert("INFO", "Licenza aggiornata con successo dal cloud.")
                return saved

            logger.error("Errore durante il download di config.dat")
            return False

        logger.info("✓ Licenza locale già aggiornata.")
        update_grace_timestamp()
        return True

    except requests.RequestException as e:
        logger.warning(f"Offline o errore di rete - Impossibile aggiornare: {e}")
        return False
    except Exception as e:
        # Se è l'eccezione di revoca la facciamo passare
        if "REVOCATA" in str(e):
            raise
        logger.error(f"Errore inatteso durante update licenza: {e}")
        return False


def _ensure_license_dir(path: str | Path) -> bool:
    """Garantisce la creazione della cartella di destinazione licenze."""
    path_obj = Path(path)
    if not path_obj.exists():
        try:
            path_obj.mkdir(parents=True)
            logger.info("Cartella licenza creata")
        except OSError as e:
            logger.error(f"Errore creazione cartella licenza: {e}")
            return False
    return True


def _save_license_files(license_dir: str | Path, files: dict[str, bytes]) -> bool:
    """Scrive i file di licenza su disco e aggiorna il timestamp di grazia."""
    try:
        dir_path = Path(license_dir)
        for name, content in files.items():
            (dir_path / name).write_bytes(content)
        logger.info("✓ Aggiornamento completato")
        update_grace_timestamp()
        return True
    except OSError as e:
        logger.error(f"Errore scrittura file licenza: {e}")
        return False
