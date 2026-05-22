"""
SyncroJob - Anagrafica Controller
Logica di business per il caricamento, filtraggio e processing dei dati dipendenti.
"""

import logging
from datetime import UTC, datetime
from typing import Any

from src.core.constants import REPORT_COLORS as COLORS, THRESHOLD_DAYS
from src.core.database import db_manager
from src.core.database.repositories import EmployeeRepository
from src.core.dipendenti.data_helpers import (
    build_timbrature_maps,
    compute_employee_status,
    normalize_name,
)
from src.core.dipendenti.employee_dto import EmployeeDTO
from src.models.employee import EmployeeRecord

logger = logging.getLogger(__name__)


class AnagraficaController:
    """Controller per la gestione dei dati dell'anagrafica dipendenti."""

    def __init__(self) -> None:
        self.repository = EmployeeRepository()

    def get_employees(self, search_text: str = "") -> list[EmployeeRecord]:
        """Recupera la lista dei dipendenti tramite repository."""
        results = self.repository.get_filtered(search_text=search_text, as_objects=True)
        # Type narrowing for mypy
        return [r for r in results if isinstance(r, EmployeeRecord)]

    def process_rows(
        self, records: list[EmployeeRecord], current_filter: str | None = None
    ) -> tuple[list[EmployeeDTO], dict[str, int]]:
        """Processa i record dei dipendenti restituendo una lista di DTO tipizzati."""
        last_by_cf, last_by_name, normalize = self._get_timbrature_maps()

        dtos: list[EmployeeDTO] = []
        counts = {"ok": 0, "warning": 0, "expired": 0, "excluded": 0}

        for record in records:
            # Adattiamo record a riga per compatibilità con compute_employee_status se necessario
            # o aggiorniamo i componenti a valle. Per ora facciamo un cast leggero.
            row = (
                record.id_risorsa,
                record.cognome,
                record.nome,
                record.data_nascita,
                record.badge,
                record.data_assunzione,
                None,
                record.codice_fiscale,
                record.monitoraggio_attivo,
            )

            is_monitored = bool(record.monitoraggio_attivo)
            status_data = compute_employee_status(row, last_by_cf, last_by_name, normalize)
            diff_days, cf_warning, last_date = status_data[0], status_data[1], status_data[2]

            # 1. Update Global Counts
            self._update_status_counts(counts, is_monitored, diff_days)

            # 2. Filter Logic
            if current_filter and self._should_skip_row(is_monitored, diff_days, current_filter):
                continue

            # 3. Create DTO
            dto = self._create_employee_dto(record, is_monitored, diff_days, cf_warning, last_date)
            dtos.append(dto)

        return dtos, counts

    def _get_timbrature_maps(self) -> tuple[dict[str, tuple[int, str]], dict[tuple[str, str], tuple[int, str]], Any]:
        """Recupera le mappe delle timbrature dal DB."""
        query_timb = "SELECT cognome, nome, codice_fiscale, data FROM timbrature"
        accessi = db_manager.execute_query(db_manager.DB_TIMBRATURE, query_timb)
        return build_timbrature_maps(accessi)

    def _update_status_counts(
        self, counts: dict[str, int], is_monitored: bool, diff_days: int | None
    ) -> None:
        """Aggiorna il dizionario dei conteggi basandosi sullo stato del dipendente."""
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

    def _should_skip_row(self, is_monitored: bool, diff_days: int | None, current_filter: str) -> bool:
        """Determina se la riga deve essere saltata in base al filtro corrente."""
        if current_filter == "excluded":
            return is_monitored

        # Se non è monitorato o non ha giorni (mai entrato), lo saltiamo per i filtri di stato
        if not is_monitored or diff_days is None:
            return True

        return self._check_status_filter(diff_days, current_filter)

    def _check_status_filter(self, diff_days: int, current_filter: str) -> bool:
        """Helper per verificare il filtro basato sui giorni di assenza."""
        if current_filter == "ok":
            return diff_days > THRESHOLD_DAYS["warning"]
        if current_filter == "warning":
            return diff_days <= THRESHOLD_DAYS["warning"] or diff_days > THRESHOLD_DAYS["expired"]
        if current_filter == "expired":
            return diff_days <= THRESHOLD_DAYS["expired"]
        return False

    def _create_employee_dto(
        self,
        record: EmployeeRecord,
        is_monitored: bool,
        diff_days: int | None,
        cf_warning: bool,
        last_date: str | None = None,
    ) -> EmployeeDTO:
        """Crea un oggetto EmployeeDTO dal record."""
        inactivation_val = THRESHOLD_DAYS["expired"] - diff_days if diff_days is not None else None
        return EmployeeDTO(
            id_risorsa=str(record.id_risorsa),
            cognome=record.cognome,
            nome=record.nome,
            data_nascita=record.data_nascita,
            badge=record.badge,
            data_assunzione=record.data_assunzione,
            codice_fiscale=record.codice_fiscale,
            monitoraggio_attivo=is_monitored,
            inactivation_days_left=inactivation_val,
            cf_warning=cf_warning,
            last_access_isab=last_date,
        )

    def get_last_isab_access(self, cognome: str, nome: str) -> tuple[str, int, str]:
        """Recupera l'ultimo accesso ISAB per un dipendente."""

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
            logger.exception("Errore recupero ultimo accesso")
            return "Errore", -1, COLORS["text_muted"]

    def toggle_monitoring(self, id_risorsa: str, enable: bool) -> bool:
        """Attiva/disattiva il monitoraggio tramite repository."""
        try:
            return self.repository.toggle_monitoring(id_risorsa, enable)
        except Exception:
            logger.exception("Errore toggle monitoraggio")
            return False
