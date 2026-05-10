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


def build_timbrature_maps(
    accessi: Sequence[Sequence[Any]],
) -> tuple[dict[str, int], dict[tuple[str, str], int], Callable[[Any], str]]:
    """
    Costruisce mappe di lookup per le timbrature indicizzate per CF e per Nome/Cognome.

    Args:
      accessi: Lista di tuple (cognome, nome, cf, data_ora).

    Returns:
      tuple: (mappa_cf, mappa_nomi, funzione_normalize).
    """
    today = datetime.now(UTC)
    last_by_cf: dict[str, int] = {}
    last_by_name: dict[tuple[str, str], int] = {}

    def normalize(t: Any) -> str:
        """Funzione locale di normalizzazione rapida."""
        return normalize_name(t)

    for cog, nom, cf, d_str in accessi:
        if d_str:
            norm_key = (normalize(cog), normalize(nom))
            norm_cf = cf.strip().upper() if cf and cf.strip() else None
            with suppress(Exception):
                date_part = d_str.split(" ")[0]
                d_dt = None
                for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                    try:
                        d_dt = datetime.strptime(date_part, fmt).replace(tzinfo=UTC)
                        break
                    except ValueError:
                        continue
                if d_dt:
                    diff = (today - d_dt).days
                    if norm_cf and (norm_cf not in last_by_cf or diff < last_by_cf[norm_cf]):
                        last_by_cf[norm_cf] = diff

                    if norm_key not in last_by_name or diff < last_by_name[norm_key]:
                        last_by_name[norm_key] = diff
    return last_by_cf, last_by_name, normalize


def compute_employee_status(
    r: tuple[Any, ...],
    last_by_cf: dict[str, int],
    last_by_name: dict[tuple[str, str], int],
    normalize: Callable[[Any], str],
) -> tuple[int | None, bool, str, str, str]:
    """Calcola lo stato del dipendente basandosi su timbrature e anagrafica."""
    # r indexes: 1=Cognome, 2=Nome, 7=CodiceFiscale
    cf_val = str(r[7]).strip().upper() if r[7] else ""
    cog_val = normalize(r[1])
    nom_val = normalize(r[2])
    diff_days = None
    cf_warning = False

    if cf_val:
        diff_days = last_by_cf.get(cf_val)
    if diff_days is None:
        diff_days = last_by_name.get((cog_val, nom_val))
        if diff_days is not None and not cf_val:
            cf_warning = True
    return diff_days, cf_warning, cog_val, nom_val, cf_val


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
