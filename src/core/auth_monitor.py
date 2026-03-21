"""
SyncroJob - Auth Monitor
Monitoraggio proattivo delle abilitazioni ISAB basato sulle timbrature.
"""

import logging
import re
from contextlib import suppress
from datetime import UTC, datetime
from typing import Any

from src.core.database import db_manager

logger = logging.getLogger(__name__)


def _normalize(t: Any) -> str:
    return re.sub(r"\s+", " ", str(t).strip().upper())


def _build_access_maps(
    accessi_raw: list[tuple[Any, ...]],
) -> tuple[dict[str, tuple[int, str]], dict[tuple[str, str], tuple[int, str]]]:
    """Costruisce le mappe di ultimo accesso: per CF e per (Cognome, Nome)."""
    last_by_cf: dict[str, tuple[int, str]] = {}
    last_by_name: dict[tuple[str, str], tuple[int, str]] = {}
    today = datetime.now(UTC)

    for cog, nom, cf, last_date_str in accessi_raw:
        date_part = str(last_date_str).split(" ")[0]
        last_date = None
        for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                last_date = datetime.strptime(date_part, fmt).replace(tzinfo=UTC)
                break
            except ValueError:
                continue

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


def check_expiring_isab_authorizations() -> list[dict[str, Any]]:
    """
    Scansiona tutti i dipendenti per identificare chi ha l'abilitazione ISAB in scadenza.
    Priorità:
    1. Match per Codice Fiscale (Infallibile)
    2. Fallback per Nome/Cognome (se CF assente in Dipendenti)
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
        last_by_cf, _last_by_name = _build_access_maps(accessi_raw)
        _, last_by_name = _build_access_maps(accessi_raw)

        results = []
        for cog, nom, cf in dipendenti:
            match_found = False
            delta: int | None = None
            f_date: str | None = None
            missing_cf_flag = False

            # Tenta Match primario: CF
            if cf and cf.strip():
                norm_cf = cf.strip().upper()
                if norm_cf in last_by_cf:
                    delta, f_date = last_by_cf[norm_cf]
                    match_found = True

            # Tenta Match secondario: Nome/Cognome
            if not match_found:
                norm_key = (_normalize(cog), _normalize(nom))
                if norm_key in last_by_name:
                    delta, f_date = last_by_name[norm_key]
                    match_found = True
                    # Segnala mancanza CF solo se abbiamo trovato match per nome ma non per CF (perché mancante)
                    if not cf or not cf.strip():
                        missing_cf_flag = True

            if match_found and delta is not None:
                from src.core.constants import THRESHOLD_DAYS

                # Monitoraggio basato su soglie centralizzate
                if delta <= THRESHOLD_DAYS["warning"]:
                    continue

                stat = "IN SCADENZA"
                if delta > THRESHOLD_DAYS["expired"]:
                    stat = "SCADUTA"

                results.append(
                    {
                        "cognome": cog.upper(),
                        "nome": nom.upper(),
                        "ultima_data": f_date,
                        "giorni_trascorsi": delta,
                        "stato": stat,
                        "cf_mancante": missing_cf_flag,
                    }
                )

        return results

    except Exception as e:
        logger.error(f"Errore durante il controllo autorizzazioni ISAB: {e}")
        return []
