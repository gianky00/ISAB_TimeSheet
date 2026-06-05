"""Modulo Data Helpers."""

import re
from collections.abc import Callable, Sequence
from contextlib import suppress
from datetime import UTC, datetime
from typing import Any


def normalize_name(text: Any) -> str:
    """Normalizza una stringa rimuovendo spazi multipli e convertendola in maiuscolo."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text).strip().upper())


def _parse_date_and_diff(d_str: str, today: datetime) -> tuple[int, str] | None:
    """Estrae la differenza in giorni e la stringa formattata dalla data del DB."""
    date_part = d_str.split(" ")[0]
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            d_dt = datetime.strptime(date_part, fmt).replace(tzinfo=UTC)
            return (today - d_dt).days, d_dt.strftime("%d/%m/%Y")
        except ValueError:
            continue
    return None


def _process_single_accesso(  # noqa: PLR0913
    cog: Any,
    nom: Any,
    cf: Any,
    d_str: str | None,
    today: datetime,
    last_by_cf: dict[str, tuple[int, str]],
    last_by_name: dict[tuple[str, str], tuple[int, str]],
) -> None:
    """Elabora una singola riga di timbratura aggiornando le mappe di stato."""
    if not d_str:
        return

    norm_key = (normalize_name(cog), normalize_name(nom))
    norm_cf = str(cf).strip().upper() if cf and str(cf).strip() else None

    with suppress(Exception):
        parsed = _parse_date_and_diff(d_str, today)
        if not parsed:
            return

        diff, pretty_date = parsed

        if norm_cf and (norm_cf not in last_by_cf or diff < last_by_cf[norm_cf][0]):
            last_by_cf[norm_cf] = (diff, pretty_date)

        if norm_key not in last_by_name or diff < last_by_name[norm_key][0]:
            last_by_name[norm_key] = (diff, pretty_date)


def build_timbrature_maps(
    accessi: Sequence[Sequence[Any]],
) -> tuple[dict[str, tuple[int, str]], dict[tuple[str, str], tuple[int, str]], Callable[[Any], str]]:
    """Costruisce mappe di lookup per le timbrature indicizzate per CF e per Nome/Cognome.

    Args:
      accessi: Lista di tuple (cognome, nome, cf, data_ora).

    Returns:
      tuple: (mappa_cf, mappa_nomi, funzione_normalize).
             Mappe contengono tuple (diff_days, data_str).
    """
    today = datetime.now(UTC)
    last_by_cf: dict[str, tuple[int, str]] = {}
    last_by_name: dict[tuple[str, str], tuple[int, str]] = {}

    def normalize(t: Any) -> str:
        """Funzione locale di normalizzazione rapida."""
        return normalize_name(t)

    for cog, nom, cf, d_str in accessi:
        _process_single_accesso(cog, nom, cf, d_str, today, last_by_cf, last_by_name)

    return last_by_cf, last_by_name, normalize


def compute_employee_status(
    r: Sequence[Any],
    last_by_cf: dict[str, tuple[int, str]],
    last_by_name: dict[tuple[str, str], tuple[int, str]],
    normalize: Callable[[Any], str],
) -> tuple[int | None, bool, str | None, str, str, str]:
    """Calcola lo stato del dipendente basandosi su timbrature e anagrafica."""
    # r indexes: 1=Cognome, 2=Nome, 7=CodiceFiscale
    cf_val = str(r[7]).strip().upper() if r[7] else ""
    cog_val = normalize(r[1])
    nom_val = normalize(r[2])
    diff_days = None
    last_date = None
    cf_warning = False

    access_info = None
    if cf_val:
        access_info = last_by_cf.get(cf_val)
    if access_info is None:
        access_info = last_by_name.get((cog_val, nom_val))
        if access_info is not None and not cf_val:
            cf_warning = True

    if access_info:
        diff_days, last_date = access_info

    return diff_days, cf_warning, last_date, cog_val, nom_val, cf_val


def format_db_date(date_str: str | None) -> str:
    """Formatta una data proveniente dal database in formato leggibile DD/MM/YYYY HH:MM:SS."""
    if not date_str or date_str == "None":
        return "-"
    try:
        return (
            datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC).strftime("%d/%m/%Y %H:%M:%S")
        )
    except Exception:
        return date_str
