"""
SyncroJob - Anagrafica Controller
Logica di business per il caricamento, filtraggio e processing dei dati dipendenti.
"""

import logging
from datetime import UTC, datetime
from typing import Any

from src.core.constants import THRESHOLD_DAYS
from src.core.database import db_manager
from src.core.dipendenti.data_helpers import (
    build_timbrature_maps,
    compute_employee_status,
    normalize_name,
)
from src.core.dipendenti.employee_dto import EmployeeDTO

logger = logging.getLogger(__name__)


class AnagraficaController:
    """Controller per la gestione dei dati dell'anagrafica dipendenti."""

    @staticmethod
    def get_employees(search_text: str = "") -> list[Any]:
        # ... (resta invariato per ora in attesa di refactor totale query)
        query = """
            SELECT id_risorsa, cognome, nome, data_nascita, badge, data_assunzione, created_at, codice_fiscale, monitoraggio_attivo
            FROM dipendenti WHERE 1=1
        """
        params = []
        if search_text:
            terms = search_text.lower().strip().split()
            for term in terms:
                p = f"%{term}%"
                query += " AND (cognome LIKE ? OR nome LIKE ? OR badge LIKE ? OR codice_fiscale LIKE ?)"
                params.extend([p, p, p, p])

        query += " ORDER BY cognome ASC, nome ASC"
        return db_manager.execute_query(db_manager.DB_DIPENDENTI, query, tuple(params))

    @staticmethod
    def process_rows(
        full_rows: list[Any], current_filter: str | None = None
    ) -> tuple[list[EmployeeDTO], dict[str, int]]:
        """Processa le righe del DB restituendo una lista di DTO tipizzati."""
        query_timb = "SELECT cognome, nome, codice_fiscale, data FROM timbrature"
        accessi = db_manager.execute_query(db_manager.DB_TIMBRATURE, query_timb)
        last_by_cf, last_by_name, normalize = build_timbrature_maps(accessi)

        dtos: list[EmployeeDTO] = []
        counts = {"ok": 0, "warning": 0, "expired": 0, "excluded": 0}

        for r in full_rows:
            is_monitored = bool(r[8]) if len(r) > 8 and r[8] is not None else True
            diff_days, cf_warning, _, _, _ = compute_employee_status(r, last_by_cf, last_by_name, normalize)

            # Update Counts
            if not is_monitored:
                counts["excluded"] += 1
            elif diff_days is not None:
                if diff_days <= THRESHOLD_DAYS["warning"]:
                    counts["ok"] += 1
                elif diff_days <= THRESHOLD_DAYS["expired"]:
                    counts["warning"] += 1
                else:
                    counts["expired"] += 1

            # Filter Logic
            if current_filter:
                skip = False
                if current_filter == "excluded":
                    skip = is_monitored
                elif (
                    not is_monitored
                    or diff_days is None
                    or (current_filter == "ok" and diff_days > THRESHOLD_DAYS["warning"])
                    or (
                        current_filter == "warning"
                        and (diff_days <= THRESHOLD_DAYS["warning"] or diff_days > THRESHOLD_DAYS["expired"])
                    )
                    or (current_filter == "expired" and diff_days <= THRESHOLD_DAYS["expired"])
                ):
                    skip = True

                if skip:
                    continue

            inactivation_val = THRESHOLD_DAYS["expired"] - diff_days if diff_days is not None else None

            dto = EmployeeDTO(
                id_risorsa=str(r[0]),
                cognome=str(r[1]),
                nome=str(r[2]),
                data_nascita=str(r[3]),
                badge=str(r[4]),
                data_assunzione=str(r[5]),
                codice_fiscale=str(r[7]),
                monitoraggio_attivo=is_monitored,
                inactivation_days_left=inactivation_val,
                cf_warning=cf_warning,
            )
            dtos.append(dto)

        return dtos, counts

    @staticmethod
    def get_last_isab_access(cognome: str, nome: str) -> tuple[str, int, str]:
        """Recupera l'ultimo accesso ISAB per un dipendente."""
        norm_cognome, norm_nome = normalize_name(cognome), normalize_name(nome)
        query = """
            SELECT data FROM timbrature
            WHERE UPPER(REPLACE(REPLACE(TRIM(cognome), '  ', ' '), '  ', ' ')) = ?
              AND UPPER(REPLACE(REPLACE(TRIM(nome), '  ', ' '), '  ', ' ')) = ?
            ORDER BY data DESC LIMIT 1
        """
        from src.core.constants import REPORT_COLORS as COLORS

        try:
            res = db_manager.execute_query(db_manager.DB_TIMBRATURE, query, (norm_cognome, norm_nome))
            if not res:
                return "Mai effettuato", -1, COLORS["text_muted"]

            last_date_str = str(res[0][0])
            date_part = last_date_str.split(" ")[0]
            last_date = None
            for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                try:
                    last_date = datetime.strptime(date_part, fmt).replace(tzinfo=UTC)
                    break
                except ValueError:
                    continue

            if not last_date:
                return "Errore data", -1, COLORS["text_muted"]

            delta = (datetime.now(UTC) - last_date).days
            formatted_date = last_date.strftime("%d/%m/%Y")

            if delta <= THRESHOLD_DAYS["warning"]:
                return f"{formatted_date} ({delta} gg fa)", delta, COLORS["success_dark"]
            if delta <= THRESHOLD_DAYS["expired"]:
                return f"{formatted_date} ({delta} gg fa)", delta, COLORS["warning_orange"]

            return f"{formatted_date} (SCADUTA - {delta} gg fa)", delta, COLORS["error_red"]
        except Exception as e:
            logger.error(f"Errore recupero ultimo accesso: {e}")
            return "Errore", -1, COLORS["text_muted"]

    @staticmethod
    def toggle_monitoring(id_risorsa: str, enable: bool) -> bool:
        """Attiva/disattiva il monitoraggio di un dipendente."""
        try:
            query = "UPDATE dipendenti SET monitoraggio_attivo = ? WHERE id_risorsa = ?"
            db_manager.execute_query(db_manager.DB_DIPENDENTI, query, (1 if enable else 0, id_risorsa))
            return True
        except Exception:
            return False
