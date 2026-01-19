"""
SyncroJob - Auth Monitor
Monitoraggio proattivo delle abilitazioni ISAB basato sulle timbrature.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

from src.core.database import db_manager

logger = logging.getLogger(__name__)


def check_expiring_isab_authorizations() -> List[Dict[str, Any]]:
    """
    Scansiona tutti i dipendenti per identificare chi ha l'abilitazione ISAB in scadenza.
    Un'abilitazione è a rischio se l'ultimo ingresso è avvenuto tra 20 e 30 giorni fa.
    Vengono considerati solo i dipendenti che hanno ALMENO un ingresso registrato.
    """
    try:
        # Recupera l'ultimo accesso per ogni coppia nome/cognome presente in timbrature
        query_timb = """
            SELECT cognome, nome, MAX(data) as ultima_data
            FROM timbrature
            WHERE data IS NOT NULL AND data != ''
            GROUP BY UPPER(cognome), UPPER(nome)
        """
        accessi = db_manager.execute_query(db_manager.DB_TIMBRATURE, query_timb)

        results = []
        today = datetime.now()

        for cognome, nome, last_date_str in accessi:
            try:
                # Formato atteso YYYY-MM-DD
                last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
                delta = (today - last_date).days

                # Monitoraggio: 20-30 giorni (In Scadenza) o 31-45 giorni (Appena Scaduti)
                if 20 <= delta <= 45:
                    results.append(
                        {
                            "cognome": cognome.strip().upper(),
                            "nome": nome.strip().upper(),
                            "ultima_data": last_date.strftime("%d/%m/%Y"),
                            "giorni_trascorsi": delta,
                            "stato": "SCADUTA" if delta > 30 else "IN SCADENZA",
                        }
                    )
            except Exception:
                # Ignoriamo record con date malformate
                continue

        return results

    except Exception as e:
        logger.error(f"Errore durante il controllo autorizzazioni ISAB: {e}")
        return []
