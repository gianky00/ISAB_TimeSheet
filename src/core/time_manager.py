"""
Bot TS - Time Manager
Gestisce il recupero dell'orario da fonti attendibili (Network Time).
"""
import requests
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

def get_network_time(timeout=5):
    """
    Ottiene l'orario corrente da una fonte online affidabile (es. Google).
    Restituisce un oggetto datetime con timezone UTC.

    Returns:
        datetime: Orario UTC corrente da rete.
        None: Se impossibile contattare il server.
    """
    try:
        # Effettua una richiesta HEAD a google.com (veloce e affidabile)
        response = requests.head("https://www.google.com", timeout=timeout)

        if "Date" in response.headers:
            # Parsa l'header Date (RFC 2822)
            # Esempio: "Wed, 21 Oct 2015 07:28:00 GMT"
            network_time = parsedate_to_datetime(response.headers["Date"])
            # Assicura che sia timezone-aware (UTC)
            if network_time.tzinfo is None:
                network_time = network_time.replace(tzinfo=timezone.utc)
            return network_time

    except Exception as e:
        print(f"[TIME] Errore recupero orario di rete: {e}")

    return None

def get_trusted_time():
    """
    Restituisce l'orario più affidabile disponibile.
    Priorità:
    1. Orario di rete (Network Time)
    2. Orario di sistema (System Time) - con flag di affidabilità

    Returns:
        tuple: (datetime, bool_is_trusted)
    """
    net_time = get_network_time()

    if net_time:
        return net_time, True

    # Fallback su orario locale UTC
    return datetime.now(timezone.utc), False
