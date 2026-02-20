"""
SyncroJob - License Updater
Modulo dedicato all'aggiornamento e alla sincronizzazione dei file di licenza dal repository GitHub.
Gestisce i periodi di grazia offline tramite token cifrati e garantisce la validità temporale del software.
"""

from datetime import UTC, datetime, timedelta
from pathlib import Path

import requests
from cryptography.fernet import Fernet

from src.core.logging import get_logger

from . import config_manager, license_validator, time_manager

logger = get_logger(__name__)

# Chiave per cifratura token grace period
GRACE_PERIOD_KEY = b"8kHs_rmwqaRUk1AQLGX65g4AEkWUDapWVsMFUQpN9Ek="


def get_github_token() -> str:
    """
    Ricostruisce dinamicamente il token GitHub offuscato utilizzato per l'accesso ai file di licenza.

    Returns:
        str: Il token di autenticazione GitHub.
    """
    chars = [103, 104, 112, 95, 99, 57, 68, 103, 54, 116, 79, 67, 75, 104, 57, 89, 106, 112, 97, 70, 117, 66, 54, 73, 52, 79, 66, 121, 107, 103, 120, 114, 113, 98, 49, 85, 106, 106, 65, 105]
    return "".join(chr(c) for c in chars)


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

        cipher = Fernet(GRACE_PERIOD_KEY)
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
        raise Exception("Nessuna validazione online precedente.\nConnessione internet richiesta per il primo avvio.")

    try:
        encrypted_data = token_path.read_bytes()
        cipher = Fernet(GRACE_PERIOD_KEY)
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
            cipher = Fernet(GRACE_PERIOD_KEY)
            encrypted_start = cipher.encrypt(current_time.isoformat().encode("utf-8"))
            token_path.parent.mkdir(parents=True, exist_ok=True)
            token_path.write_bytes(encrypted_start)
            return True, "Periodo di grazia attivato (3 giorni)", 3
        except Exception as e:
            return False, f"Errore attivazione periodo di grazia: {e}", 0

    try:
        encrypted_data = token_path.read_bytes()
        cipher = Fernet(GRACE_PERIOD_KEY)
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
    Recupera l'Hardware ID, interroga le API di GitHub e scarica i file necessari se presenti.

    Returns:
        bool: True se l'aggiornamento è andato a buon fine.
    """
    logger.info("Tentativo aggiornamento licenza...")
    hw_id = license_validator.get_hardware_id().strip().rstrip(".")
    license_dir = get_license_dir()

    if not _ensure_license_dir(license_dir):
        return False

    base_url = f"https://api.github.com/repos/gianky00/intelleo-licenses/contents/licenses/{hw_id}"
    downloaded, error = _download_license_files(base_url)

    if error:
        logger.error(error)
        return False
    if downloaded:
        return _save_license_files(license_dir, downloaded)
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


def _download_license_files(base_url: str) -> tuple[dict[str, bytes], str | None]:
    """Interroga GitHub per scaricare il payload binario della licenza."""
    token = get_github_token()
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3.raw"}
    files = {"config.dat": "config.dat", "manifest.json": "manifest.json"}

    downloaded = {}
    for remote, local in files.items():
        try:
            res = requests.get(f"{base_url}/{remote}", headers=headers, timeout=10)
            if res.status_code == 200:
                downloaded[local] = res.content
                logger.info(f"✓ {remote} scaricato")
            else:
                return {}, f"File {remote} non trovato o errore HTTP {res.status_code}"
        except requests.RequestException:
            return {}, "Offline - Impossibile aggiornare"
    return downloaded, None


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
