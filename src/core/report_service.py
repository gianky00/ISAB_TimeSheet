"""SyncroJob - Report Service.

Logica di business per la generazione e l'invio di report email tramite Outlook.
"""

import logging
import operator
import os
import re
from collections.abc import Sequence
from contextlib import suppress
from datetime import UTC, datetime, timedelta
from typing import Any, Final

from src.core import config_manager
from src.core.database import db_manager
from src.core.notification_manager import NotificationManager
from src.core.report_history import ReportHistory

try:
    import win32com.client as win32_client
except ImportError:
    win32_client = None  # type: ignore

logger = logging.getLogger(__name__)


class ReportService:
    """Gestisce la generazione e l'invio di report analitici."""

    REPORT_WARNING_MIN: Final[int] = 21
    REPORT_EXPIRED_MIN: Final[int] = 30
    DEFAULT_INTERVAL_DAYS: Final[int] = 7

    @classmethod
    def send_scheduled_report_email(cls) -> None:
        """Esegue l'analisi degli accessi mancanti e invia il report HTML via Outlook."""
        try:
            w_list, e_list = cls._collect_employee_status_lists()

            if not w_list and not e_list:
                logger.info("Nessun dipendente in scadenza o scaduto da segnalare.")
                return

            if os.name != "nt":
                logger.warning("Invio email Outlook supportato solo su Windows.")
                return

            cls._dispatch_outlook_email(w_list, e_list)

            ReportHistory.save_report(w_list, e_list)
            config_manager.set_config_value(
                "report_email_autopilot_last_sent", datetime.now(UTC).astimezone().isoformat()
            )
            NotificationManager.instance().add_notification(
                title="Report Email Inviato",
                message=f"Inviati {len(w_list)} warning e {len(e_list)} expired.",
                level="success",
            )
        except Exception:
            logger.exception("Errore durante la generazione o l'invio del report email")
            NotificationManager.instance().add_notification(
                title="Errore Report Email", message="Errore durante l'invio automatico", level="error"
            )

    @classmethod
    def _collect_employee_status_lists(cls) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Esegue le query e calcola i giorni di assenza per ogni dipendente monitorato."""
        dipendenti = db_manager.execute_query(
            db_manager.DB_DIPENDENTI,
            "SELECT id_risorsa, cognome, nome, codice_fiscale, badge, data_assunzione FROM dipendenti WHERE monitoraggio_attivo = 1 OR monitoraggio_attivo IS NULL",
        )
        accessi = db_manager.execute_query(
            db_manager.DB_TIMBRATURE, "SELECT cognome, nome, codice_fiscale, data FROM timbrature"
        )
        l_cf, l_nm = cls._build_access_maps(accessi)

        w_list: list[dict[str, Any]] = []
        e_list: list[dict[str, Any]] = []
        for d in dipendenti:
            df = l_cf.get(cls._norm_text(d[3] or "")) or l_nm.get(
                (cls._norm_text(d[1] or ""), cls._norm_text(d[2] or ""))
            )
            if df is None:
                continue
            item = {
                "id": d[0],
                "cognome": d[1],
                "nome": d[2],
                "badge": d[4] or "-",
                "giorni": df,
                "data": (datetime.now(UTC).astimezone() - timedelta(days=df)).strftime("%d/%m/%Y"),
            }
            if cls.REPORT_WARNING_MIN <= df <= cls.REPORT_EXPIRED_MIN:
                w_list.append(item)
            elif df > cls.REPORT_EXPIRED_MIN:
                e_list.append(item)

        w_list.sort(key=operator.itemgetter("giorni"), reverse=True)
        e_list.sort(key=operator.itemgetter("giorni"), reverse=True)
        return w_list, e_list

    @classmethod
    def _build_access_maps(
        cls, accessi: Sequence[Sequence[Any]]
    ) -> tuple[dict[str, int], dict[tuple[str, str], int]]:
        """Costruisce mappe di accesso per ricerca rapida per CF o Nome/Cognome."""
        today = datetime.now(UTC)
        l_cf: dict[str, int] = {}
        l_nm: dict[tuple[str, str], int] = {}
        for r in accessi:
            d_str = str(r[3])
            if d_str:
                nk = (cls._norm_text(r[0]), cls._norm_text(r[1]))
                ncf = r[2].strip().upper() if r[2] else None
                with suppress(Exception):
                    dp = d_str.split(" ")[0]
                    d_dt = None
                    for f in ("%Y-%m-%d", "%d/%m/%Y"):
                        with suppress(ValueError):
                            d_dt = datetime.strptime(dp, f).replace(tzinfo=UTC)
                            break
                    if d_dt:
                        df = (today - d_dt).days
                        if ncf and (ncf not in l_cf or df < l_cf[ncf]):
                            l_cf[ncf] = df
                        if nk not in l_nm or df < l_nm[nk]:
                            l_nm[nk] = df
        return l_cf, l_nm

    @staticmethod
    def _norm_text(t: Any) -> str:
        """Normalizza il testo rimuovendo spazi extra e convertendo in maiuscolo."""
        return re.sub(r"\s+", " ", str(t).strip().upper())

    @classmethod
    def _dispatch_outlook_email(cls, w_list: list[dict[str, Any]], e_list: list[dict[str, Any]]) -> None:
        """Utilizza le API COM di Windows per inviare l'email tramite Outlook."""
        if not win32_client:
            logger.error("win32com.client non disponibile per l'invio email.")
            return

        body = (
            f"<html><body style='font-family: Segoe UI;'><h2>Report Accessi ISAB</h2><p>Generato il {datetime.now(UTC).astimezone().strftime('%d/%m/%Y %H:%M')}</p>"
            + "<h3>In Scadenza (21-30 gg)</h3><ul>"
            + "".join(
                [f"<li>{x['cognome']} {x['nome']} - {x['giorni']}gg ({x['data']})</li>" for x in w_list[:20]]
            )
            + "</ul>"
            + "<h3>Scaduti (&gt; 30 gg)</h3><ul>"
            + "".join(
                [f"<li>{x['cognome']} {x['nome']} - {x['giorni']}gg ({x['data']})</li>" for x in e_list[:20]]
            )
            + "</ul></body></html>"
        )

        m = win32_client.Dispatch("Outlook.Application").CreateItem(0)
        m.To = "supporto@syncrojob.it"
        m.CC = ""
        m.Subject = f"[AUTO] Report Monitoraggio ISAB - {datetime.now(UTC).astimezone().strftime('%d/%m/%Y')}"
        m.HTMLBody = body
        m.Send()
