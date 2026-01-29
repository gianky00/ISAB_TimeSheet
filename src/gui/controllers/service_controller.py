"""
Controller per il coordinamento dei servizi di background (Telegram, Lyra, Update).
"""

from PyQt6.QtCore import QObject, QTimer

from src.core.app_updater import check_for_updates
from src.core.notification_manager import NotificationManager


class ServiceController(QObject):
    """
    Gestisce il ciclo di vita dei servizi di background e
    il coordinamento delle notifiche.
    """

    def __init__(self, main_window, telegram_service, lyra_sentinel):
        super().__init__(main_window)
        self.mw = main_window
        self.telegram = telegram_service
        self.sentinel = lyra_sentinel

        # Tracking bot in esecuzione per sito (per parallelismo intelligente)
        self.running_bots_by_site = {
            "portale_fornitori": [],  # Lista di bot_id in esecuzione
            "safework": [],
        }

        # Coda bot in attesa per sito (quando un sito è occupato)
        self.pending_bots_by_site = {
            "portale_fornitori": [],  # Lista di (bot_id, panel, callback)
            "safework": [],
        }

    def start_all(self):
        """Avvia tutti i servizi in background con i relativi ritardi."""
        # Lyra Sentinel
        self.sentinel.anomalies_found.connect(self.mw._on_anomalies_found)
        QTimer.singleShot(2000, self.sentinel.start)

        # Telegram
        QTimer.singleShot(1000, self.telegram.start_service)

        # Aggiornamenti
        QTimer.singleShot(3000, self._check_updates)

        # Collegamento notifiche globali -> Telegram
        NotificationManager.instance().notification_added.connect(self._forward_notification_to_telegram)

        # Scheduler (ogni 60s) per task pianificati
        self.scheduler_timer = QTimer(self)
        self.scheduler_timer.timeout.connect(self._check_scheduled_tasks)
        self.scheduler_timer.start(60000)  # 1 minuto

    def _check_scheduled_tasks(self):
        """
        Controlla se ci sono task pianificati da eseguire ora.
        Implementa parallelismo intelligente: bot su siti diversi possono
        andare in parallelo, bot sullo stesso sito vanno in sequenza.
        """
        from datetime import datetime

        from src.core import config_manager

        config = config_manager.load_config()
        now = datetime.now().strftime("%H:%M")

        # Lista di bot da schedulare (bot_id, panel_attr, site, target_time)
        scheduled_bots = [
            (
                "timbrature",
                "timbrature_bot_panel",
                "portale_fornitori",
                config.get("timbrature_autopilot_time", "09:00"),
                config.get("timbrature_autopilot_enabled", False),
                None,  # Nessuna preparazione speciale
            ),
            (
                "scarico_oda_generale",
                "dettagli_oda_bot_panel",
                "portale_fornitori",
                config.get("scarico_oda_generale_autopilot_time", "09:00"),
                config.get("scarico_oda_generale_autopilot_enabled", False),
                self._prepare_scarico_oda_generale,  # Callback di preparazione
            ),
            (
                "ricerca_pdl",
                "ricerca_pdl_bot_panel",
                "safework",
                config.get("ricerca_pdl_autopilot_time", "09:00"),
                config.get("ricerca_pdl_autopilot_enabled", False),
                None,  # Nessuna preparazione speciale
            ),
        ]

        # Controlla ogni bot schedulato
        for (
            bot_id,
            panel_attr,
            site,
            target_time,
            enabled,
            prepare_callback,
        ) in scheduled_bots:
            if not enabled:
                continue

            if now == target_time:
                # Verifica che il pannello sia disponibile
                if hasattr(self.mw, panel_attr):
                    panel = getattr(self.mw, panel_attr)

                    # Esegui preparazione specifica se richiesta
                    if prepare_callback:
                        prepare_callback(panel)

                    # Schedula con logica di parallelismo
                    self._schedule_bot_with_parallelism(
                        bot_id, panel, site, f"Avvio pianificato automatico ({now})..."
                    )

        # === REPORT EMAIL SCHEDULATO (con intervallo giorni) ===
        self._check_report_email_schedule(config, now)

    def _check_report_email_schedule(self, config, now_time):
        """
        Controlla e gestisce l'invio schedulato del report email.
        Questo task usa un intervallo in giorni invece di essere giornaliero.
        """
        if not config.get("report_email_autopilot_enabled", False):
            return

        target_time = config.get("report_email_autopilot_time", "08:00")

        # Verifica prima l'orario
        if now_time != target_time:
            return

        # Verifica intervallo giorni
        interval_days = config.get("report_email_autopilot_interval_days", 7)
        last_sent_str = config.get("report_email_autopilot_last_sent")

        should_send = False
        if last_sent_str is None:
            # Mai inviato prima, invia ora
            should_send = True
        else:
            try:
                from datetime import datetime

                last_dt = datetime.fromisoformat(last_sent_str)
                days_passed = (datetime.now() - last_dt).days
                if days_passed >= interval_days:
                    should_send = True
            except (ValueError, TypeError):
                # Data invalida, invia comunque
                should_send = True

        if should_send:
            self._send_scheduled_report_email()

    def _send_scheduled_report_email(self):
        """Genera e invia il report email automaticamente (senza UI)."""
        import logging
        from datetime import datetime

        from src.core import config_manager
        from src.core.notification_manager import NotificationManager

        logger = logging.getLogger(__name__)

        try:
            # Importa le dipendenze necessarie
            # Importa funzione helper per costruire le mappe timbrature
            # (la logica è duplicata per evitare dipendenze circolari)
            import re
            from contextlib import suppress
            from datetime import timedelta

            from src.core.database import db_manager
            from src.core.report_history import ReportHistory

            def normalize(t):
                return re.sub(r"\s+", " ", str(t).strip().upper())

            def build_timbrature_maps(accessi):
                today = datetime.now()
                last_by_cf = {}
                last_by_name = {}

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
                return last_by_cf, last_by_name

            # Query dipendenti monitorati
            query = """
                SELECT id_risorsa, cognome, nome, codice_fiscale, badge, data_assunzione
                FROM dipendenti
                WHERE monitoraggio_attivo = 1 OR monitoraggio_attivo IS NULL
                ORDER BY cognome ASC, nome ASC
            """
            dipendenti = db_manager.execute_query(db_manager.DB_DIPENDENTI, query)

            # Recupera accessi
            query_timb = "SELECT cognome, nome, codice_fiscale, data FROM timbrature"
            accessi = db_manager.execute_query(db_manager.DB_TIMBRATURE, query_timb)
            last_by_cf, last_by_name = build_timbrature_maps(accessi)

            warning_list = []
            expired_list = []

            for dip in dipendenti:
                id_ris, cog, nom, cf, badge, data_ass = dip
                cf_norm = normalize(cf or "")
                name_key = (normalize(cog or ""), normalize(nom or ""))

                diff_days = last_by_cf.get(cf_norm) or last_by_name.get(name_key)
                if diff_days is None:
                    continue

                last_access_date = datetime.now() - timedelta(days=diff_days)
                formatted_date = last_access_date.strftime("%d/%m/%Y")

                item = {
                    "id": id_ris,
                    "cognome": cog,
                    "nome": nom,
                    "badge": badge if badge else "-",
                    "giorni": diff_days,
                    "data": formatted_date,
                }

                if 21 <= diff_days <= 30:
                    warning_list.append(item)
                elif diff_days > 30:
                    expired_list.append(item)

            # Se non ci sono dipendenti da segnalare, non inviare
            if not warning_list and not expired_list:
                logger.info("Report email schedulato: nessun dipendente da segnalare")
                return

            # Ordina per urgenza
            warning_list.sort(key=lambda x: x["giorni"], reverse=True)
            expired_list.sort(key=lambda x: x["giorni"], reverse=True)

            # Invia report via Outlook
            import os

            if os.name != "nt":
                logger.warning("Report email schedulato disponibile solo su Windows")
                return

            import win32com.client

            from src.core.version import __version__

            # Costruisci HTML semplificato per invio automatico
            current_date = datetime.now().strftime("%d/%m/%Y %H:%M")

            body_html = f"""
            <html>
            <body style="font-family: 'Segoe UI', Arial, sans-serif; color: #1f2937;">
                <h2 style="color: #0d6efd;">Report Automatico Monitoraggio Accessi ISAB</h2>
                <p style="color: #6b7280;">Generato automaticamente il {current_date} da SyncroJob v{__version__}</p>

                <p><strong>Riepilogo:</strong> {len(warning_list)} in scadenza, {len(expired_list)} scaduti</p>

                <h3 style="color: #fd7e14;">In Scadenza (21-30 gg)</h3>
                <ul>
            """
            for dip in warning_list[:20]:  # Limita a 20 per email automatica
                body_html += f"<li>{dip['cognome']} {dip['nome']} - {dip['giorni']}gg ({dip['data']})</li>"
            if len(warning_list) > 20:
                body_html += f"<li><em>... e altri {len(warning_list) - 20}</em></li>"
            body_html += "</ul>"

            body_html += "<h3 style='color: #dc3545;'>Scaduti (&gt; 30 gg)</h3><ul>"
            for dip in expired_list[:20]:
                body_html += f"<li>{dip['cognome']} {dip['nome']} - {dip['giorni']}gg ({dip['data']})</li>"
            if len(expired_list) > 20:
                body_html += f"<li><em>... e altri {len(expired_list) - 20}</em></li>"
            body_html += "</ul>"

            body_html += """
                <p style="color: #6b7280; font-size: 12px; margin-top: 20px;">
                    Questo report è stato inviato automaticamente dal sistema Autopilot di SyncroJob.
                </p>
            </body>
            </html>
            """

            subject = f"[AUTO] Report Monitoraggio ISAB - {datetime.now().strftime('%d/%m/%Y')}"

            outlook = win32com.client.Dispatch("Outlook.Application")
            mail = outlook.CreateItem(0)
            mail.To = "luca.riccio@coemi.it"
            mail.CC = "isabsud@coemi.it"
            mail.Subject = subject
            mail.HTMLBody = body_html
            mail.Send()  # Invio automatico (non Display)

            # Salva snapshot per trend
            ReportHistory.save_report(warning_list, expired_list)

            # Aggiorna timestamp ultimo invio
            config_manager.set_config_value("report_email_autopilot_last_sent", datetime.now().isoformat())

            # Notifica
            NotificationManager.instance().add_notification(
                title="Report Email Inviato",
                message=f"Report automatico inviato: {len(warning_list)} in scadenza, {len(expired_list)} scaduti",
                level="success",
            )

            logger.info(
                f"Report email schedulato inviato: {len(warning_list)} warning, {len(expired_list)} expired"
            )

        except Exception as e:
            logger.error(f"Errore invio report email schedulato: {e}")
            NotificationManager.instance().add_notification(
                title="Errore Report Email",
                message=f"Impossibile inviare report automatico: {e}",
                level="error",
            )

    def _prepare_scarico_oda_generale(self, panel):
        """
        Prepara il pannello Scarico OdA Generale:
        - Pulisce la tabella (rimuove tutti i dati)
        - In questo modo il bot scaricherà l'Excel generale (senza numero OdA)
        """
        if hasattr(panel, "table"):
            # Pulisci la tabella completamente
            panel.table.setRowCount(0)
            panel.log_widget.append("🧹 Tabella pulita per scarico generale (senza filtro OdA)")

    def _schedule_bot_with_parallelism(self, bot_id, panel, site, log_message):
        """
        Schedula un bot con logica di parallelismo intelligente.

        Regole:
        - Bot su siti DIVERSI possono essere eseguiti IN PARALLELO
        - Bot sullo STESSO sito devono essere eseguiti IN SEQUENZA

        Args:
            bot_id: Identificatore del bot
            panel: Pannello del bot da avviare
            site: Sito su cui opera il bot ("portale_fornitori" o "safework")
            log_message: Messaggio da loggare all'avvio
        """
        # Verifica se ci sono bot in esecuzione sullo stesso sito
        if self.running_bots_by_site[site]:
            # Sito occupato: metti in coda
            self.pending_bots_by_site[site].append((bot_id, panel, log_message))
            panel.log_widget.append(
                f"⏸️ Bot in coda. Sito {site.replace('_', ' ').title()} occupato da: {', '.join(self.running_bots_by_site[site])}"
            )
        else:
            # Sito libero: avvia immediatamente
            self._start_bot(bot_id, panel, site, log_message)

    def _start_bot(self, bot_id, panel, site, log_message):
        """
        Avvia un bot e traccia la sua esecuzione.

        Args:
            bot_id: Identificatore del bot
            panel: Pannello del bot da avviare
            site: Sito su cui opera il bot
            log_message: Messaggio da loggare all'avvio
        """
        # Verifica che non sia già in esecuzione
        if not panel.start_btn.isEnabled():
            panel.log_widget.append("⚠️ Bot già in esecuzione, salto.")
            return

        # Aggiungi ai bot in esecuzione
        self.running_bots_by_site[site].append(bot_id)

        # Log avvio
        panel.log_widget.append(log_message)
        panel.log_widget.append(
            f"🚀 Avvio parallelo: {len(self.running_bots_by_site['portale_fornitori'])} bot Portale, {len(self.running_bots_by_site['safework'])} bot SafeWork"
        )

        # Connetti segnale di completamento per gestire la coda
        if hasattr(panel, "status_changed"):
            # Rimuovi eventuali callback precedenti di ServiceController per questo pannello
            # per evitare esecuzioni multiple, senza disconnettere altri listener (es. BotController)
            if hasattr(panel, "_service_callback") and panel._service_callback:
                try:
                    panel.status_changed.disconnect(panel._service_callback)
                except Exception:
                    pass

            # Crea una funzione di callback che cattura bot_id e site
            def on_bot_finished(status, message):
                # Note: status is the color code from BaseBotPanel
                # #2E7D32 = Success, #C62828 = Error, #ffc107 = Stopped/Pending
                is_finished = status in ["completed", "error", "stopped"] or status in [
                    "#2E7D32",
                    "#C62828",
                    "#ffc107",
                ]

                if is_finished:
                    self._on_bot_completed(bot_id, site, panel)

            # Salva il riferimento per poterlo scollegare in futuro
            panel._service_callback = on_bot_finished
            panel.status_changed.connect(on_bot_finished)

        # Avvia il bot
        panel._on_start()

    def _on_bot_completed(self, bot_id, site, panel):
        """
        Gestisce il completamento di un bot: rimuove dal tracking e
        avvia il prossimo bot in coda per lo stesso sito.

        Args:
            bot_id: Identificatore del bot completato
            site: Sito su cui operava il bot
            panel: Pannello del bot (per disconnettere segnali)
        """
        # Rimuovi dai bot in esecuzione
        if bot_id in self.running_bots_by_site[site]:
            self.running_bots_by_site[site].remove(bot_id)

        # Disconnetti solo la callback specifica di questo controller
        if hasattr(panel, "_service_callback") and panel._service_callback:
            try:
                panel.status_changed.disconnect(panel._service_callback)
                panel._service_callback = None
            except Exception:
                pass

        # Controlla se ci sono bot in coda per questo sito
        if self.pending_bots_by_site[site]:
            # Avvia il prossimo bot in coda
            next_bot_id, next_panel, next_log_message = self.pending_bots_by_site[site].pop(0)
            next_panel.log_widget.append("▶️ Bot precedente completato. Avvio da coda...")
            self._start_bot(next_bot_id, next_panel, site, next_log_message)

    def _check_updates(self):
        """Controlla gli aggiornamenti in background."""
        check_for_updates(parent=self.mw, silent=True, callback=self.mw._show_update_banner)

    def _forward_notification_to_telegram(self, notification):
        """Inoltra notifiche importanti al bot Telegram."""
        if notification.get("title") == "Telegram":
            return

        level = notification.get("level", "info")
        if level in ["success", "error", "warning"]:
            title = notification.get("title", "Notifica")
            msg = notification.get("message", "")
            icon = "[OK]" if level == "success" else "[ERR]" if level == "error" else "[!]"
            text = f"{icon} *{title}*\n{msg}"
            self.telegram.send_message_sync(text)
