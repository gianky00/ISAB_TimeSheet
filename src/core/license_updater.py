"""
Bot TS - License Updater
Gestisce l'aggiornamento e la validazione della licenza.
"""
import os
import requests
from datetime import datetime, timedelta, timezone
from cryptography.fernet import Fernet
from . import license_validator
from . import config_manager
from . import time_manager

# Chiave per cifratura token grace period
GRACE_PERIOD_KEY = b'8kHs_rmwqaRUk1AQLGX65g4AEkWUDapWVsMFUQpN9Ek='


def get_github_token():
    """Ricostruisce il token GitHub offuscato."""
    # Token per accesso al repo gianky00/bot-ts-licenses
    chars = [
        103, 104, 112, 95, 50, 98, 75, 119, 107, 75, 87, 118, 115, 70, 99, 99,
        52, 82, 66, 79, 79, 71, 65, 110, 111, 118, 80, 114, 67, 70, 53, 75, 72,
        99, 48, 49, 112, 71, 103, 107
    ]
    return "".join(chr(c) for c in chars)


def get_license_dir():
    """Restituisce il percorso della cartella Licenza (in AppData)."""
    base_dir = config_manager.get_data_path()
    return os.path.join(base_dir, "Licenza")


def _get_validity_token_path():
    """Restituisce il percorso del token di validità."""
    return os.path.join(get_license_dir(), "validity.token")


def _get_emergency_grace_token_path():
    """Restituisce il percorso del token di grazia di emergenza (3 giorni)."""
    return os.path.join(get_license_dir(), "emergency_grace.token")


def update_grace_timestamp():
    """Salva il timestamp corrente cifrato per il periodo di grazia offline (per licenze valide)."""
    try:
        token_path = _get_validity_token_path()
        current_time, is_trusted = time_manager.get_trusted_time()

        # Se non abbiamo un orario affidabile (offline) e stiamo solo aggiornando
        # il timestamp di validità, usiamo l'orario locale (che è meglio di niente)
        # ma questo metodo dovrebbe essere chiamato solo dopo un successo online.

        cipher = Fernet(GRACE_PERIOD_KEY)
        encrypted_time = cipher.encrypt(current_time.isoformat().encode('utf-8'))

        os.makedirs(os.path.dirname(token_path), exist_ok=True)

        with open(token_path, "wb") as f:
            f.write(encrypted_time)

        # Se abbiamo una licenza valida, rimuoviamo l'eventuale token di emergenza
        emergency_token = _get_emergency_grace_token_path()
        if os.path.exists(emergency_token):
            os.remove(emergency_token)

    except Exception as e:
        print(f"[AVVISO] Errore aggiornamento timestamp: {e}")


def check_grace_period():
    """
    Verifica se l'applicazione può funzionare offline (con licenza valida in precedenza).
    """
    token_path = _get_validity_token_path()

    if not os.path.exists(token_path):
        raise Exception(
            "Nessuna validazione online precedente.\n"
            "Connessione internet richiesta per il primo avvio."
        )

    try:
        with open(token_path, "rb") as f:
            encrypted_data = f.read()

        cipher = Fernet(GRACE_PERIOD_KEY)
        decrypted_data = cipher.decrypt(encrypted_data).decode('utf-8')
        last_online = datetime.fromisoformat(decrypted_data)

        # Usa time_manager per ottenere l'ora, preferibilmente da rete
        now, is_trusted = time_manager.get_trusted_time()

        # Controllo rollback orologio (solo se abbiamo un orario locale)
        # Se is_trusted è False, 'now' è locale.
        if now < last_online - timedelta(minutes=5):
            raise Exception("Rilevata incoerenza orologio di sistema.")

        # Controllo 3 giorni
        days_offline = (now - last_online).days
        if days_offline >= 3:
            raise Exception(
                "Periodo di grazia offline (3 giorni) SCADUTO.\n"
                "Connettiti a internet per rinnovare la licenza."
            )

        remaining_days = 3 - days_offline
        print(f"[LICENZA] Modalità offline: {remaining_days} giorni rimanenti")
        return True

    except Exception as e:
        if any(x in str(e) for x in ["SCADUTO", "incoerenza", "Nessuna validazione"]):
            raise e
        raise Exception(f"Errore verifica periodo di grazia: {e}")


def check_emergency_grace_period():
    """
    Gestisce il periodo di grazia di 3 giorni per licenze mancanti o invalide.
    Restituisce (allowed: bool, message: str, remaining_days: int)
    """
    token_path = _get_emergency_grace_token_path()

    current_time, is_trusted = time_manager.get_trusted_time()

    # Se il token non esiste, lo creiamo (inizio periodo di grazia)
    if not os.path.exists(token_path):
        try:
            cipher = Fernet(GRACE_PERIOD_KEY)
            # Salviamo l'inizio del periodo
            encrypted_start = cipher.encrypt(current_time.isoformat().encode('utf-8'))

            os.makedirs(os.path.dirname(token_path), exist_ok=True)
            with open(token_path, "wb") as f:
                f.write(encrypted_start)

            return True, "Periodo di grazia attivato (3 giorni)", 3
        except Exception as e:
            return False, f"Errore attivazione periodo di grazia: {e}", 0

    # Se esiste, verifichiamo quanto tempo è passato
    try:
        with open(token_path, "rb") as f:
            encrypted_data = f.read()

        cipher = Fernet(GRACE_PERIOD_KEY)
        decrypted_data = cipher.decrypt(encrypted_data).decode('utf-8')
        start_time = datetime.fromisoformat(decrypted_data)

        # Controllo manipolazione orologio (se locale)
        if current_time < start_time - timedelta(minutes=60): # Tolleranza di 1h
             return False, "Rilevata manipolazione orologio di sistema", 0

        elapsed = current_time - start_time

        if elapsed.days >= 3:
            return False, "Periodo di grazia di 3 giorni SCADUTO.", 0

        remaining_days = 3 - elapsed.days
        return True, f"Periodo di grazia attivo ({remaining_days} giorni rimanenti)", remaining_days

    except Exception as e:
        return False, f"Errore lettura periodo di grazia: {e}", 0


def is_running_from_source() -> bool:
    """Verifica se l'applicazione è in esecuzione dai sorgenti."""
    import sys
    return not getattr(sys, 'frozen', False)


def is_license_folder_empty() -> bool:
    """Verifica se la cartella licenza è vuota o non esiste."""
    license_dir = get_license_dir()
    
    if not os.path.exists(license_dir):
        return True
    
    # Controlla se ci sono i file necessari
    config_dat = os.path.join(license_dir, "config.dat")
    manifest_json = os.path.join(license_dir, "manifest.json")
    
    return not (os.path.exists(config_dat) and os.path.exists(manifest_json))


def auto_download_license_if_needed():
    """
    Compatibilità backward: wrapper per run_update, ma ora non blocca se cartella piena.
    Lasciato per non rompere import esistenti, ma la logica principale sarà in run_update.
    """
    pass # Deprecato, logica spostata in main.py che chiama run_update direttamente se serve


def run_update():
    """
    Controlla e scarica aggiornamenti licenza da GitHub.
    Restituisce True se il download è avvenuto con successo (file trovati e scaricati).
    """
    print("[LICENZA] ═══════════════════════════════════════════════")
    print("[LICENZA] Tentativo aggiornamento licenza...")

    hw_id = license_validator.get_hardware_id().strip().rstrip('.')
    license_dir = get_license_dir()

    print(f"[LICENZA] Hardware ID: {hw_id[:20]}...")

    if not os.path.exists(license_dir):
        try:
            os.makedirs(license_dir)
            print("[LICENZA] Cartella licenza creata")
        except OSError as e:
            print(f"[ERRORE] Creazione cartella licenza: {e}")
            return False

    # Repository per Bot TS licenses
    base_url = f"https://api.github.com/repos/gianky00/intelleo-licenses/contents/licenses/{hw_id}"
    token = get_github_token()
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.raw"
    }

    # Solo config.dat e manifest.json (no pyarmor.rkey)
    files_map = {
        "config.dat": "config.dat",
        "manifest.json": "manifest.json"
    }

    downloaded_content = {}
    incomplete_update = False
    network_error_occurred = False

    # Tentativo download
    for remote_name, local_name in files_map.items():
        url = f"{base_url}/{remote_name}"

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                downloaded_content[local_name] = response.content
                print(f"[LICENZA] ✓ {remote_name} scaricato")
            elif response.status_code == 404:
                print(f"[LICENZA] ⚠ {remote_name} non trovato")
                incomplete_update = True
            elif response.status_code == 401:
                print("[ERRORE] Token autenticazione non valido")
                incomplete_update = True
                break
            else:
                print(f"[AVVISO] {remote_name}: HTTP {response.status_code}")
                incomplete_update = True

        except requests.RequestException as e:
            print(f"[AVVISO] Connessione fallita: {e}")
            network_error_occurred = True
            break

    success = False
    if network_error_occurred:
        print("[LICENZA] Offline - Impossibile aggiornare")
    elif incomplete_update:
        print("[LICENZA] Licenza incompleta o non trovata su GitHub")
    else:
        try:
            for local_name, content in downloaded_content.items():
                full_path = os.path.join(license_dir, local_name)
                with open(full_path, "wb") as f:
                    f.write(content)
            print("[LICENZA] ✓ Aggiornamento completato")
            update_grace_timestamp()
            success = True
        except OSError as e:
            print(f"[ERRORE] Scrittura file licenza: {e}")

    print("[LICENZA] ═══════════════════════════════════════════════")
    return success


if __name__ == "__main__":
    try:
        run_update()
    except Exception as e:
        print(f"[ERRORE] Aggiornamento: {e}")
