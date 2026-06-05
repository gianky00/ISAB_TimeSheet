"""SyncroJob - Auth Monitor.

Monitoraggio proattivo delle abilitazioni ISAB basato sulle timbrature.
"""

import re
from collections.abc import Sequence
from contextlib import suppress
from datetime import UTC, datetime
from typing import Any

from src.application.services.constants import THRESHOLD_DAYS
from src.application.services.database import db_manager
from src.application.services.logging import get_logger

logger = get_logger(__name__)


def _normalize(t: Any) -> str:
    return re.sub(r"\s+", " ", str(t).strip().upper())


def _parse_date(last_date_str: Any) -> datetime | None:
    """Helper per il parsing flessibile delle date."""
    date_part = str(last_date_str).split(" ")[0]
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_part, fmt).replace(tzinfo=UTC)
        except ValueError:
            continue
    return None


def _build_access_maps(
    accessi_raw: Sequence[Sequence[Any]],
) -> tuple[dict[str, tuple[int, str]], dict[tuple[str, str], tuple[int, str]]]:
    """Costruisce le mappe di ultimo accesso: per CF e per (Cognome, Nome)."""
    last_by_cf: dict[str, tuple[int, str]] = {}
    last_by_name: dict[tuple[str, str], tuple[int, str]] = {}
    today = datetime.now(UTC)

    for cog, nom, cf, last_date_str in accessi_raw:
        last_date = _parse_date(last_date_str)
        if not last_date:
            continue

        delta = (today - last_date).days
        formatted_date = last_date.strftime("%d/%m/%Y")

        # Salva per CF
        if cf and cf.strip():
            norm_cf = cf.strip().upper()
            if norm_cf not in last_by_cf or delta < last_by_cf[norm_cf][0]:
                last_by_cf[norm_cf] = (delta, formatted_date)

        # Salva per Nome/Cognome (sempre, come fallback)
        with suppress(Exception):
            norm_key = (_normalize(cog), _normalize(nom))
            if norm_key not in last_by_name or delta < last_by_name[norm_key][0]:
                last_by_name[norm_key] = (delta, formatted_date)

    return last_by_cf, last_by_name


def _find_match_data(
    cog: str,
    nom: str,
    cf: str,
    last_by_cf: dict[str, tuple[int, str]],
    last_by_name: dict[tuple[str, str], tuple[int, str]],
) -> tuple[int | None, str | None, bool]:
    if cf and cf.strip():
        norm_cf = cf.strip().upper()
        if norm_cf in last_by_cf:
            delta, f_date = last_by_cf[norm_cf]
            return delta, f_date, False

    norm_key = (_normalize(cog), _normalize(nom))
    if norm_key in last_by_name:
        delta, f_date = last_by_name[norm_key]
        missing_cf = not bool(cf and cf.strip())
        return delta, f_date, missing_cf

    return None, None, False


def _process_employee_match(
    cog: str,
    nom: str,
    cf: str,
    last_by_cf: dict[str, tuple[int, str]],
    last_by_name: dict[tuple[str, str], tuple[int, str]],
) -> dict[str, Any] | None:
    """Determina se un dipendente ha un'abilitazione in scadenza e ritorna il record."""
    delta, f_date, missing_cf_flag = _find_match_data(cog, nom, cf, last_by_cf, last_by_name)

    if delta is None or delta <= THRESHOLD_DAYS["warning"]:
        return None

    stat = "SCADUTA" if delta > THRESHOLD_DAYS["expired"] else "IN SCADENZA"

    return {
        "cognome": cog.upper(),
        "nome": nom.upper(),
        "ultima_data": f_date,
        "giorni_trascorsi": delta,
        "stato": stat,
        "cf_mancante": missing_cf_flag,
    }


def check_expiring_isab_authorizations() -> list[dict[str, Any]]:
    """Scansiona tutti i dipendenti per identificare chi ha l'abilitazione ISAB in scadenza.

    Priorità:
    1. Match per Codice Fiscale (Infallibile)
    2. Fallback per Nome/Cognome (se CF assente in Dipendenti).
    """
    try:
        # 1. Recupera anagrafica dipendenti
        query_dip = "SELECT cognome, nome, codice_fiscale FROM dipendenti"
        dipendenti = db_manager.execute_query(db_manager.DB_DIPENDENTI, query_dip)

        # 2. Recupera tutte le timbrature
        query_timb = (
            "SELECT cognome, nome, codice_fiscale, data FROM timbrature WHERE data IS NOT NULL AND data != ''"
        )
        accessi_raw = db_manager.execute_query(db_manager.DB_TIMBRATURE, query_timb)

        # 3. Costruisci mappe
        last_by_cf, last_by_name = _build_access_maps(accessi_raw)

        results = []
        for cog, nom, cf in dipendenti:
            res = _process_employee_match(cog, nom, cf, last_by_cf, last_by_name)
            if res:
                results.append(res)

    except Exception:
        logger.exception("Errore durante il controllo autorizzazioni ISAB")
        return []

    return results
