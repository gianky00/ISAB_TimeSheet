"""
SyncroJob - Universal Search Service
Servizio CORE per l'esecuzione di ricerche centralizzate su tutti i database.
Agnostico rispetto alla GUI.
"""

import logging
import sqlite3
from typing import Any

from src.bots.portale_fornitori.timbrature.storage import TimbratureStorage
from src.core.audit_manager import AuditManager
from src.core.contabilita_manager import ContabilitaManager
from src.core.database import db_manager
from src.core.paths import CONFIG_DIR

logger = logging.getLogger(__name__)


class SearchService:
    """Servizio per la ricerca globale tra i vari moduli del sistema."""

    @staticmethod
    def search_all(query: str, limit: int = 10) -> dict[str, Any]:
        """
        Esegue la ricerca su tutti i database supportati.

        Args:
          query: La stringa di ricerca.
          limit: Limite massimo di risultati per categoria.

        Returns:
          Dict con i risultati raggruppati per categoria.
        """
        results: dict[str, Any] = {
            "oda": SearchService._search_oda(query, limit),
            "extended": SearchService._search_extended(query, limit),
            "employees": SearchService._search_employees(query, limit),
            "storico_oda": SearchService._search_storico_oda(query, limit),
            "attivita_programmate": SearchService._search_attivita_programmate(query, limit),
            "pdl": SearchService._search_pdl(query, limit),
            "audit": SearchService._search_audit(query, limit),
        }
        return results

    @staticmethod
    def _search_oda(query: str, limit: int) -> list[dict[str, Any]]:
        try:
            matches = ContabilitaManager.search_oda(query)
            return matches[:limit]
        except Exception as e:
            logger.error(f"SearchService ODA error: {e}")  # noqa: TRY400
            return []

    @staticmethod
    def _search_extended(query: str, limit: int) -> dict[str, list[dict[str, Any]]]:
        try:
            return ContabilitaManager.search_extended(query, limit=limit)
        except Exception as e:
            logger.error(f"SearchService Extended error: {e}")  # noqa: TRY400
            return {}

    @staticmethod
    def _search_employees(query: str, limit: int) -> list[dict[str, Any]]:
        try:
            # Cast dict results to common format
            matches = TimbratureStorage().search_employees(query)
            return matches[:limit]
        except Exception as e:
            logger.error(f"SearchService Employees error: {e}")  # noqa: TRY400
            return []

    @staticmethod
    def _search_storico_oda(query: str, limit: int) -> list[dict[str, Any]]:
        db_path = CONFIG_DIR / "data" / "storico_oda.db"
        if not db_path.exists():
            return []

        try:
            with db_manager.get_connection(db_path, read_only=True) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                search_pattern = f"%{query}%"
                cursor.execute(
                    """
          SELECT oda, descrizione, pos_oda
          FROM storico_oda
          WHERE CAST(oda AS TEXT) LIKE ? OR
             descrizione LIKE ? OR
             testo_breve LIKE ? OR
             CAST(contratto AS TEXT) LIKE ? OR
             descrizione_fornitore LIKE ?
          LIMIT ?
          """,
                    [search_pattern] * 5 + [limit],
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"SearchService Storico ODA error: {e}")  # noqa: TRY400
            return []

    @staticmethod
    def _search_attivita_programmate(query: str, limit: int) -> list[dict[str, Any]]:
        db_path = CONFIG_DIR / "data" / "contabilita.db"
        if not db_path.exists():
            return []

        try:
            with db_manager.get_connection(db_path, read_only=True) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                search_pattern = f"%{query}%"
                cursor.execute(
                    """
          SELECT area, pdl, descrizione_attivita
          FROM attivita_programmate
          WHERE area LIKE ? OR
             pdl LIKE ? OR
             descrizione_attivita LIKE ? OR
             stato_pdl LIKE ? OR
             stato_attivita LIKE ?
          LIMIT ?
          """,
                    [search_pattern] * 5 + [limit],
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"SearchService Attivita'Programmate error: {e}")  # noqa: TRY400
            return []

    @staticmethod
    def _search_pdl(query: str, limit: int) -> list[dict[str, Any]]:
        db_path = CONFIG_DIR / "data" / "pdl.db"
        if not db_path.exists():
            return []

        try:
            with db_manager.get_connection(db_path, read_only=True) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                search_pattern = f"%{query}%"
                cursor.execute(
                    """
          SELECT odl, descrizione, unita_tecnica
          FROM pdl
          WHERE CAST(odl AS TEXT) LIKE ? OR
             descrizione LIKE ? OR
             unita_tecnica LIKE ? OR
             stato LIKE ?
          LIMIT ?
          """,
                    [search_pattern] * 4 + [limit],
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"SearchService PDL error: {e}")  # noqa: TRY400
            return []

    @staticmethod
    def _search_audit(query: str, limit: int) -> list[dict[str, Any]]:
        try:
            audit_logs = AuditManager.instance().get_logs(limit=100)
            matches = [
                log
                for log in audit_logs
                if query.lower() in str(log["action"]).lower() or query.lower() in str(log["entity"]).lower()
            ]
            return matches[:limit]
        except Exception as e:
            logger.error(f"SearchService Audit error: {e}")  # noqa: TRY400
            return []
