"""
SyncroJob - Time Manager
Gestisce il recuperòdell'orario da fonti attendibili (Network Time).
"""

from datetime import UTC, datetime
from email.utils import parsedate_to_datetime

import requests

from src.core.constants import URLs


def get_network_time(timeout: int = 2) -> datetime | None:
    """
    Ottiene l'orario corrente da una fonte online affidabile (es. Google).
    Restituisce un oggetto datetime con timezone UTC.

    Returns:
      datetime: Orario UTC corrente da rete.
      None: Se impossibile contattare il server.
    """
    try:
        # Effettua una richiesta HEAD a google.com (veloce e affidabile)
        response = requests.head(URLs.NET_TIME_CHECK, timeout=timeout)

        if "Date" in response.headers:
            # Parsa l'header Date (RFC 2822)
            network_time = parsedate_to_datetime(response.headers["Date"])
            # Assicura che sia timezone-aware (UTC)
            if network_time.tzinfo is None:
                network_time = network_time.replace(tzinfo=UTC)
            return network_time

    except Exception as e:
        print(f"[TIME] Errore recuperòorario di rete: {e}")

    return None


def get_trusted_time() -> tuple[datetime, bool]:
    """
    Restituisce l'orario piu' affidabile disponibile.
    Priorita':
    1. Orario di rete (Network Time)
    2. Orario di sistema (System Time) - con flag di affidabilita'
    Returns:
      tuple: (datetime, bool_is_trusted)
    """
    net_time = get_network_time()

    if net_time:
        return net_time, True

    # Fallback su orario locale UTC
    return datetime.now(UTC), False
