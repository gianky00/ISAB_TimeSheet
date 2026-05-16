import sqlite3
from typing import Any

from src.core.database import db_manager
from src.core.logging import get_logger
from src.models import EmployeeRecord

logger = get_logger(__name__)


class EmployeeRepository:
    """Repository per l'accesso ai dati dell'Anagrafica Dipendenti."""

    def __init__(self, db_manager_instance: Any = None) -> None:
        self.db = db_manager_instance or db_manager
        self.columns = [
            "id_risorsa",
            "cognome",
            "nome",
            "badge",
            "codice_fiscale",
            "data_assunzione",
            "monitoraggio_attivo",
            "data_nascita",
        ]

    def get_all(
        self, active_only: bool = True, as_objects: bool = True
    ) -> list[EmployeeRecord] | list[dict[str, Any]]:
        """Restituisce tutti i dipendenti, opzionalmente filtrati per quelli attivi."""
        query = f"SELECT {', '.join(self.columns)} FROM dipendenti"

        try:
            if active_only:
                query += " WHERE monitoraggio_attivo = 1"
            query += " ORDER BY cognome, nome"

            rows = self.db.execute_query(self.db.DB_DIPENDENTI, query)

            results: list[dict[str, Any]] = []
            for row in rows:
                try:
                    # Tenta conversione Row -> dict
                    d = dict(row)
                except (TypeError, ValueError):
                    # Fallback per tuple (es. mock nei test)
                    d = dict(zip(self.columns, row, strict=False))
                results.append(d)

            if as_objects:
                return [EmployeeRecord(**d) for d in results]
        except sqlite3.OperationalError:
            # Fallback per schema vecchio (se mancano colonne come monitoraggio_attivo o data_nascita)
            logger.warning("Repository Employee: schema DB non allineato, uso fallback")
            query_fallback = "SELECT id_risorsa, cognome, nome, badge, codice_fiscale, data_assunzione FROM dipendenti ORDER BY cognome, nome"
            rows = self.db.execute_query(self.db.DB_DIPENDENTI, query_fallback)

            if as_objects:
                obj_results: list[EmployeeRecord] = []
                for row in rows:
                    data = {
                        "id_risorsa": row[0],
                        "cognome": row[1],
                        "nome": row[2],
                        "badge": row[3],
                        "codice_fiscale": row[4],
                        "data_assunzione": row[5],
                        "monitoraggio_attivo": 1,
                        "data_nascita": None,
                    }
                    obj_results.append(EmployeeRecord(**data))
                return obj_results
            dict_results: list[dict[str, Any]] = []
            for row in rows:
                data = {
                    "id_risorsa": row[0],
                    "cognome": row[1],
                    "nome": row[2],
                    "badge": row[3],
                    "codice_fiscale": row[4],
                    "data_assunzione": row[5],
                    "monitoraggio_attivo": 1,
                    "data_nascita": None,
                }
                dict_results.append(data)
            return dict_results
        except Exception:
            logger.exception("Errore repository Employee get_all")
            return []
        else:
            return results

    def get_filtered(
        self, search_text: str = "", active_only: bool = False, as_objects: bool = True
    ) -> list[EmployeeRecord] | list[dict[str, Any]]:
        """Recupera i dipendenti filtrati per testo e stato monitoraggio."""
        query = f"SELECT {', '.join(self.columns)} FROM dipendenti WHERE 1=1"
        params = []

        if active_only:
            query += " AND monitoraggio_attivo = 1"

        if search_text:
            terms = search_text.lower().strip().split()
            for term in terms:
                p = f"%{term}%"
                query += " AND (cognome LIKE ? OR nome LIKE ? OR badge LIKE ? OR codice_fiscale LIKE ?)"
                params.extend([p, p, p, p])

        query += " ORDER BY cognome ASC, nome ASC"

        try:
            rows = self.db.execute_query(self.db.DB_DIPENDENTI, query, tuple(params))
            if as_objects:
                return [EmployeeRecord(**dict(row)) for row in rows]
        except Exception:
            logger.exception("Errore repository Employee get_filtered")
            return []
        else:
            return [dict(row) for row in rows]

    def get_by_badge(self, badge: str) -> EmployeeRecord | None:
        """Cerca un dipendente per numero di badge."""
        query = f"SELECT {', '.join(self.columns)} FROM dipendenti WHERE badge = ?"
        try:
            results = self.db.execute_query(self.db.DB_DIPENDENTI, query, (badge,))
            if results:
                return EmployeeRecord(**dict(results[0]))
        except Exception:
            return None
        else:
            return None

    def save(self, employee: EmployeeRecord) -> bool:
        """Salva o aggiorna un dipendente nel database."""
        if employee.id_risorsa:
            # Update - Usiamo una copia dei dati per non modificare l'oggetto originale
            data = dict(vars(employee))
            id_risorsa = data.pop("id_risorsa")
            fields = [f"{k} = ?" for k in data]
            values = list(data.values())
            values.append(id_risorsa)

            query = f"UPDATE dipendenti SET {', '.join(fields)} WHERE id_risorsa = ?"
            try:
                self.db.execute_query(self.db.DB_DIPENDENTI, query, tuple(values))
            except Exception:
                logger.exception(f"Errore aggiornamento dipendente {employee.id_risorsa}")
                return False
            else:
                return True
        else:
            # Insert
            # Escludiamo id_risorsa (primo elemento) per l'insert se None
            cols = self.columns[1:]
            query = f"""
                INSERT INTO dipendenti ({", ".join(cols)})
                VALUES ({", ".join(["?"] * len(cols))})
            """
            params = (
                employee.cognome.upper(),
                employee.nome.upper(),
                employee.badge,
                employee.codice_fiscale.upper() if employee.codice_fiscale else None,
                employee.data_assunzione,
                employee.monitoraggio_attivo,
                employee.data_nascita,
            )
            try:
                self.db.execute_query(self.db.DB_DIPENDENTI, query, params)
            except Exception:
                logger.exception("Errore inserimento dipendente")
                return False
            else:
                return True

    def toggle_monitoring(self, id_risorsa: int | str, enable: bool) -> bool:
        """Attiva/disattiva il monitoraggio di un dipendente."""
        query = "UPDATE dipendenti SET monitoraggio_attivo = ? WHERE id_risorsa = ?"
        try:
            self.db.execute_query(self.db.DB_DIPENDENTI, query, (1 if enable else 0, id_risorsa))
        except Exception:
            return False
        else:
            return True
