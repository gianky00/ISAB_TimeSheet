"""
SyncroJob - Service Controller
Controller per il coordinamento dei servizi di background, l'automazione dei report e la gestione del parallelismo bot.
Implementa una logica di scheduling intelligente che permette l'esecuzione contemporanea di bot su portali diversi
(es. Portale Fornitori e SafeWork) garantendo al contempo la sequenzialità delle operazioni sullo stesso sito.
Gestisce inoltre l'inoltro automatico delle notifiche critiche al bot Telegram e il check periodico degli aggiornamenti.
"""

import logging
import operator
import os
import re
from contextlib import suppress
from datetime import UTC, datetime, timedelta
from typing import Any, Final

from PyQt6.QtCore import QObject, QTimer

from src.core import config_manager
from src.core.app_updater import check_for_updates
from src.core.database import db_manager
from src.core.notification_manager import NotificationManager
from src.core.report_history import ReportHistory

logger = logging.getLogger(__name__)


class ServiceController(QObject):
    """
    Gestore del ciclo di vita dei servizi asincroni e dei task pianificati (Autopilot).
    Coordina:
    - TelegramService per il monitoraggio remoto e l'invio di documenti.
    - Scheduler dei Bot per lo scarico automatico di timbrature, OdA e PDL.
    - Generazione e invio automatico dei report email via Outlook.
    """

    REPORT_WARNING_MIN: Final[int] = 21
    REPORT_EXPIRED_MIN: Final[int] = 30
    DEFAULT_INTERVAL_DAYS: Final[int] = 7

    def __init__(self, main_window: Any, telegram_service: Any) -> None:
        """
        Inizializza il controller dei servizi e le code di gestione del parallelismo.

        Args:
            main_window: Riferimento alla MainWindow dell'applicazione.
            telegram_service: Istanza del servizio Telegram.
        """
        super().__init__(main_window)
        self.mw = main_window
        self.telegram = telegram_service

        self.running_bots_by_site: dict[str, list[str]] = {"portale_fornitori": [], "safework": []}
        self.pending_bots_by_site: dict[str, list[tuple[str, Any, str]]] = {
            "portale_fornitori": [],
            "safework": [],
        }
        self.scheduler_timer: QTimer | None = None

    def start_all(self) -> None:
        """Avvia la sequenza di attivazione dei servizi di background con ritardi differiti per non saturare lo startup."""
        QTimer.singleShot(1000, self.telegram.start_service)
        QTimer.singleShot(3000, self._check_updates)

        NotificationManager.instance().notification_added.connect(self._forward_notification_to_telegram)

        self.scheduler_timer = QTimer(self)
        self.scheduler_timer.timeout.connect(self._check_scheduled_tasks)
        self.scheduler_timer.start(60000)

    def stop_all(self) -> None:
        """Ferma tutti i servizi e i timer attivi."""
        if self.scheduler_timer:
            self.scheduler_timer.stop()

        if self.telegram:
            self.telegram.stop_service()

        logger.info("Tutti i servizi di background sono stati arrestati.")

    def _check_scheduled_tasks(self) -> None:
        """
        Verifica il match orario per i bot configurati in modalità Autopilot.
        Applica la logica di parallelismo intelligente per l'accodamento dei task.
        """
        config = config_manager.load_config()
        now = datetime.now(UTC).astimezone().strftime("%H:%M")

        scheduled_bots = [
            (
                "timbrature",
                "timbrature_bot_panel",
                "portale_fornitori",
                str(config.get("timbrature_autopilot_time", "09:00")),
                bool(config.get("timbrature_autopilot_enabled", False)),
                None,
            ),
            (
                "scarico_oda_generale",
                "dettagli_panel",
                "portale_fornitori",
                str(config.get("scarico_oda_generale_autopilot_time", "09:00")),
                bool(config.get("scarico_oda_generale_autopilot_enabled", False)),
                self._prepare_scarico_oda_generale,
            ),
            (
                "ricerca_pdl",
                "pdl_search_panel",
                "safework",
                str(config.get("ricerca_pdl_autopilot_time", "09:00")),
                bool(config.get("ricerca_pdl_autopilot_enabled", False)),
                None,
            ),
        ]

        for bot_id, panel_attr, site, target_time, enabled, prepare_cb in scheduled_bots:
            if enabled and now == target_time and hasattr(self.mw, panel_attr):
                panel = getattr(self.mw, panel_attr)
                if prepare_cb:
                    prepare_cb(panel)
                self._schedule_bot_with_parallelism(
                    bot_id, panel, site, f"Avvio pianificato automatico ({now})..."
                )

        self._check_report_email_schedule(config, now)

    def _check_report_email_schedule(self, config: dict[str, Any], now_time: str) -> None:
        """Gestisce l'invio del report email basandosi su orario e intervallo di giorni configurati."""
        if not config.get("report_email_autopilot_enabled", False):
            return
        if now_time != str(config.get("report_email_autopilot_time", "08:00")):
            return

        interval = int(config.get("report_email_autopilot_interval_days", self.DEFAULT_INTERVAL_DAYS))
        last_sent = config.get("report_email_autopilot_last_sent")

        should_send = last_sent is None
        if not should_send:
            with suppress(Exception):
                last_sent_dt = datetime.fromisoformat(str(last_sent))
                if (datetime.now(UTC).astimezone() - last_sent_dt).days >= interval:
                    should_send = True

        if should_send:
            self._send_scheduled_report_email()

    def _send_scheduled_report_email(self) -> None:
        """Esegue l'analisi degli accessi mancanti e invia il report HTML via Outlook dispatch."""
        try:
            w_list, e_list = self._collect_employee_status_lists()

            if not w_list and not e_list:
                return

            if os.name != "nt":
                return

            self._dispatch_outlook_email(w_list, e_list)

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
            logger.exception("Errore report email")
            NotificationManager.instance().add_notification(
                title="Errore Report Email", message="Errore durante l'invio automatico", level="error"
            )

    def _collect_employee_status_lists(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Esegue le query e calcola i giorni di assenza per ogni dipendente monitorato."""
        dipendenti = db_manager.execute_query(
            db_manager.DB_DIPENDENTI,
            "SELECT id_risorsa, cognome, nome, codice_fiscale, badge, data_assunzione FROM dipendenti WHERE monitoraggio_attivo = 1 OR monitoraggio_attivo IS NULL",
        )
        accessi = db_manager.execute_query(
            db_manager.DB_TIMBRATURE, "SELECT cognome, nome, codice_fiscale, data FROM timbrature"
        )
        l_cf, l_nm = self._build_access_maps(accessi)

        w_list: list[dict[str, Any]] = []
        e_list: list[dict[str, Any]] = []
        for d in dipendenti:
            df = l_cf.get(self._norm_text(d[3] or "")) or l_nm.get(
                (self._norm_text(d[1] or ""), self._norm_text(d[2] or ""))
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
            if self.REPORT_WARNING_MIN <= df <= self.REPORT_EXPIRED_MIN:
                w_list.append(item)
            elif df > self.REPORT_EXPIRED_MIN:
                e_list.append(item)

        w_list.sort(key=operator.itemgetter("giorni"), reverse=True)
        e_list.sort(key=operator.itemgetter("giorni"), reverse=True)
        return w_list, e_list

    def _build_access_maps(
        self, accessi: list[tuple[Any, ...]]
    ) -> tuple[dict[str, int], dict[tuple[str, str], int]]:
        """Costruisce mappe di accesso per ricerca rapida per CF o Nome/Cognome."""
        today = datetime.now(UTC)
        l_cf: dict[str, int] = {}
        l_nm: dict[tuple[str, str], int] = {}
        for r in accessi:
            d_str = str(r[3])
            if d_str:
                nk = (self._norm_text(r[0]), self._norm_text(r[1]))
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

    def _norm_text(self, t: Any) -> str:
        """Normalizza il testo rimuovendo spazi extra e convertendo in maiuscolo."""
        return re.sub(r"\s+", " ", str(t).strip().upper())

    def _dispatch_outlook_email(self, w_list: list[dict[str, Any]], e_list: list[dict[str, Any]]) -> None:
        """Utilizza le API COM di Windows per inviare l'email tramite Outlook."""
        import win32com.client  # noqa: PLC0415

        body = f"<html><body style='font-family: Segoe UI;'><h2>Report Accessi ISAB</h2><p>Generato il {datetime.now(UTC).astimezone().strftime('%d/%m/%Y %H:%M')}</p>"
        body += (
            "<h3>In Scadenza (21-30 gg)</h3><ul>"
            + "".join(
                [f"<li>{x['cognome']} {x['nome']} - {x['giorni']}gg ({x['data']})</li>" for x in w_list[:20]]
            )
            + "</ul>"
        )
        body += (
            "<h3>Scaduti (&gt; 30 gg)</h3><ul>"
            + "".join(
                [f"<li>{x['cognome']} {x['nome']} - {x['giorni']}gg ({x['data']})</li>" for x in e_list[:20]]
            )
            + "</ul></body></html>"
        )

        out = win32com.client.Dispatch("Outlook.Application")
        m = out.CreateItem(0)
        m.To = "luca.riccio@coemi.it"
        m.CC = "isabsud@coemi.it"
        m.Subject = f"[AUTO] Report Monitoraggio ISAB - {datetime.now(UTC).astimezone().strftime('%d/%m/%Y')}"
        m.HTMLBody = body
        m.Send()

    def _prepare_scarico_oda_generale(self, panel: Any) -> None:
        """Configura il pannello Dettagli OdA per uno scarico massivo senza filtri specifici."""
        if hasattr(panel, "data_table"):
            panel.data_table.set_data([])
            panel.log_widget.append("🧹 Tabella pulita per scarico generale (senza filtro OdA)")

    def _schedule_bot_with_parallelism(self, bot_id: str, panel: Any, site: str, log_message: str) -> None:
        """Gestisce l'accodamento di un bot rispettando i vincoli di un'unica istanza Selenium per sito."""
        if self.running_bots_by_site[site]:
            self.pending_bots_by_site[site].append((bot_id, panel, log_message))
            panel.log_widget.append(f"⏸️ Bot in coda. Sito {site.replace('_', ' ').title()} occupato.")
        else:
            self._start_bot(bot_id, panel, site, log_message)

    def _start_bot(self, bot_id: str, panel: Any, site: str, log_message: str) -> None:
        """Avvia l'esecuzione del bot e registra il callback per la gestione della coda al termine."""
        if not panel.start_btn.isEnabled():
            return
        self.running_bots_by_site[site].append(bot_id)
        panel.log_widget.append(log_message)

        if hasattr(panel, "status_changed"):
            if hasattr(panel, "_service_callback") and panel._service_callback:
                with suppress(Exception):
                    panel.status_changed.disconnect(panel._service_callback)

            def on_finished(st: str, msg: str) -> None:
                if st in ("completed", "error", "stopped", "#2E7D32", "#C62828", "#ffc107"):
                    self._on_bot_completed(bot_id, site, panel)

            panel._service_callback = on_finished
            panel.status_changed.connect(on_finished)
        panel._on_start()

    def _on_bot_completed(self, bot_id: str, site: str, panel: Any) -> None:
        """Rimuove il bot concluso dalla lista attiva e avvia il prossimo elemento in coda per quel sito."""
        if bot_id in self.running_bots_by_site[site]:
            self.running_bots_by_site[site].remove(bot_id)
        if hasattr(panel, "_service_callback") and panel._service_callback:
            with suppress(Exception):
                panel.status_changed.disconnect(panel._service_callback)
                panel._service_callback = None
        if self.pending_bots_by_site[site]:
            nxt_id, nxt_p, nxt_msg = self.pending_bots_by_site[site].pop(0)
            nxt_p.log_widget.append("▶️ Avvio da coda...")
            self._start_bot(nxt_id, nxt_p, site, nxt_msg)

    def _check_updates(self) -> None:
        """Interroga il server per verificare la presenza di nuove release software."""
        check_for_updates(parent=self.mw, silent=True, callback=self.mw._show_update_banner)

    def _forward_notification_to_telegram(self, notification: dict[str, Any]) -> None:
        """Inoltra i messaggi di sistema con criticità elevata al bot Telegram registrato."""
        if notification.get("title") == "Telegram":
            return
        level = notification.get("level", "info")
        if level in ("success", "error", "warning"):
            icon = "[OK]" if level == "success" else "[ERR]" if level == "error" else "[!]"
            self.telegram.send_message_sync(
                f"{icon} *{notification.get('title', 'Notifica')}*\n{notification.get('message', '')}"
            )
