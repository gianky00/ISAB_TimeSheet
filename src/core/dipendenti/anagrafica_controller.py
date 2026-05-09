"""
SyncroJob - Anagrafica Controller
Logica di business per il caricamento, filtraggio e processing dei dati dipendenti.
"""

import logging
from datetime import UTC, datetime
from typing import Any, Final

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

    MONITORING_COLUMN_INDEX: Final[int] = 8

    @staticmethod
    def get_employees(search_text: str = "") -> list[tuple[Any, ...]]:
        """Recupera la lista dei dipendenti dal database filtrando per testo."""
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
        full_rows: list[tuple[Any, ...]], current_filter: str | None = None
    ) -> tuple[list[EmployeeDTO], dict[str, int]]:
        """Processa le righe del DB restituendo una lista di DTO tipizzati."""
        last_by_cf, last_by_name, normalize = AnagraficaController._get_timbrature_maps()

        dtos: list[EmployeeDTO] = []
        counts = {"ok": 0, "warning": 0, "expired": 0, "excluded": 0}

        for r in full_rows:
            is_monitored = AnagraficaController._is_employee_monitored(r)
            status_data = compute_employee_status(r, last_by_cf, last_by_name, normalize)
            diff_days, cf_warning = status_data[0], status_data[1]

            # 1. Update Global Counts
            AnagraficaController._update_status_counts(counts, is_monitored, diff_days)

            # 2. Filter Logic
            if current_filter and AnagraficaController._should_skip_row(
                is_monitored, diff_days, current_filter
            ):
                continue

            # 3. Create DTO
            dto = AnagraficaController._create_employee_dto(r, is_monitored, diff_days, cf_warning)
            dtos.append(dto)

        return dtos, counts

    @staticmethod
    def _get_timbrature_maps() -> tuple[dict[str, int], dict[tuple[str, str], int], Any]:
        """Recupera le mappe delle timbrature dal DB."""
        query_timb = "SELECT cognome, nome, codice_fiscale, data FROM timbrature"
        accessi = db_manager.execute_query(db_manager.DB_TIMBRATURE, query_timb)
        return build_timbrature_maps(accessi)

    @staticmethod
    def _is_employee_monitored(row: tuple[Any, ...]) -> bool:
        """Verifica se il monitoraggio  attivo per la riga data."""
        idx = AnagraficaController.MONITORING_COLUMN_INDEX
        return bool(row[idx]) if len(row) > idx and row[idx] is not None else True

    @staticmethod
    def _update_status_counts(counts: dict[str, int], is_monitored: bool, diff_days: int | None) -> None:
        """Aggiorna il dizionario dei conteggia'basandosi sullo stato del dipendente."""
        if not is_monitored:
            counts["excluded"] += 1
            return

        if diff_days is None:
            return

        if diff_days <= THRESHOLD_DAYS["warning"]:
            counts["ok"] += 1
        elif diff_days <= THRESHOLD_DAYS["expired"]:
            counts["warning"] += 1
        else:
            counts["expired"] += 1

    @staticmethod
    def _should_skip_row(is_monitored: bool, diff_days: int | None, current_filter: str) -> bool:
        """Determina se la riga deve essere saltata in base al filtro corrente."""
        if current_filter == "excluded":
            return is_monitored

        # Se non  monitorato o non ha giorni (mai entrato), lo saltiamo per i filtri di stato
        if not is_monitored or diff_days is None:
            return True

        return AnagraficaController._check_status_filter(diff_days, current_filter)

    @staticmethod
    def _check_status_filter(diff_days: int, current_filter: str) -> bool:
        """Helper per verificare il filtro basato sui giorni di assenza."""
        if current_filter == "ok":
            return diff_days > THRESHOLD_DAYS["warning"]
        if current_filter == "warning":
            return diff_days <= THRESHOLD_DAYS["warning"] or diff_days > THRESHOLD_DAYS["expired"]
        if current_filter == "expired":
            return diff_days <= THRESHOLD_DAYS["expired"]
        return False

    @staticmethod
    def _create_employee_dto(
        row: tuple[Any, ...], is_monitored: bool, diff_days: int | None, cf_warning: bool
    ) -> EmployeeDTO:
        """Crea un oggetto EmployeeDTO dalla riga del DB."""
        inactivation_val = THRESHOLD_DAYS["expired"] - diff_days if diff_days is not None else None
        return EmployeeDTO(
            id_risorsa=str(row[0]),
            cognome=str(row[1]),
            nome=str(row[2]),
            data_nascita=str(row[3]),
            badge=str(row[4]),
            data_assunzione=str(row[5]),
            codice_fiscale=str(row[7]),
            monitoraggio_attivo=is_monitored,
            inactivation_days_left=inactivation_val,
            cf_warning=cf_warning,
        )

    @staticmethod
    def get_last_isab_access(cognome: str, nome: str) -> tuple[str, int, str]:
        """Recupera l'ultimo accesso ISAB per un dipendente."""
        from src.core.constants import REPORT_COLORS as COLORS  # noqa: PLC0415

        norm_cognome, norm_nome = normalize_name(cognome), normalize_name(nome)
        query = """
      SELECT data FROM timbrature
      WHERE UPPER(REPLACE(REPLACE(TRIM(cognome), ' ', ' '), ' ', ' ')) = ?
       AND UPPER(REPLACE(REPLACE(TRIM(nome), ' ', ' '), ' ', ' ')) = ?
      ORDER BY data DESC LIMIT 1
    """

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

            delta = (datetime.now(UTC).date() - last_date.date()).days
            formatted_date = last_date.strftime("%d/%m/%Y")

            if delta <= THRESHOLD_DAYS["warning"]:
                return f"{formatted_date} ({delta} gg fa)", delta, COLORS["success_dark"]
            if delta <= THRESHOLD_DAYS["expired"]:
                return f"{formatted_date} ({delta} gg fa)", delta, COLORS["warning_orange"]

            return f"{formatted_date} (SCADUTA - {delta} gg fa)", delta, COLORS["error_red"]
        except Exception:
            logger.exception("Errore recuperòultimo accesso")
            return "Errore", -1, COLORS["text_muted"]

    @staticmethod
    def toggle_monitoring(id_risorsa: str, enable: bool) -> bool:
        """Attiva/disattiva il monitoraggio di un dipendente."""
        try:
            query = "UPDATE dipendenti SET monitoraggio_attivo = ? WHERE id_risorsa = ?"
            db_manager.execute_query(db_manager.DB_DIPENDENTI, query, (1 if enable else 0, id_risorsa))
        except Exception:
            return False
        else:
            return True
