import re
from contextlib import suppress
from datetime import datetime


def normalize_name(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text).strip().upper())


def build_timbrature_maps(accessi):
    today = datetime.now()
    last_by_cf = {}
    last_by_name = {}

    def normalize(t):
        return normalize_name(t)

    for cog, nom, cf, d_str in accessi:
        if d_str:
            norm_key = (normalize(cog), normalize(nom))
            norm_cf = cf.strip().upper() if cf and cf.strip() else None
            with suppress(Exception):
                date_part = str(d_str).split(" ")[0]
                d_dt = None
                for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                    try:
                        d_dt = datetime.strptime(date_part, fmt)
                        break
                    except ValueError:
                        continue
                if d_dt:
                    diff = (today - d_dt).days
                    if norm_cf:
                        if norm_cf not in last_by_cf or diff < last_by_cf[norm_cf]:
                            last_by_cf[norm_cf] = diff
                    if norm_key not in last_by_name or diff < last_by_name[norm_key]:
                        last_by_name[norm_key] = diff
    return last_by_cf, last_by_name, normalize


def compute_employee_status(r, last_by_cf, last_by_name, normalize):
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


def format_db_date(date_str):
    if not date_str or date_str == "None":
        return "-"
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").strftime(
            "%d/%m/%Y %H:%M:%S"
        )
    except Exception:
        return date_str
