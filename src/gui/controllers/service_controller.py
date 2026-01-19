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
        NotificationManager.instance().notification_added.connect(
            self._forward_notification_to_telegram
        )

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

    def _prepare_scarico_oda_generale(self, panel):
        """
        Prepara il pannello Scarico OdA Generale:
        - Pulisce la tabella (rimuove tutti i dati)
        - In questo modo il bot scaricherà l'Excel generale (senza numero OdA)
        """
        if hasattr(panel, "table"):
            # Pulisci la tabella completamente
            panel.table.setRowCount(0)
            panel.log_widget.append(
                "🧹 Tabella pulita per scarico generale (senza filtro OdA)"
            )

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
            # Crea una funzione di callback che cattura bot_id e site
            def on_bot_finished(status, message):
                if status in ["completed", "error", "stopped"]:
                    self._on_bot_completed(bot_id, site, panel)

            # Disconnetti eventuali connessioni precedenti per evitare duplicati
            try:
                panel.status_changed.disconnect()
            except Exception:
                pass

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

        # Disconnetti il segnale per evitare loop
        try:
            panel.status_changed.disconnect()
        except Exception:
            pass

        # Controlla se ci sono bot in coda per questo sito
        if self.pending_bots_by_site[site]:
            # Avvia il prossimo bot in coda
            next_bot_id, next_panel, next_log_message = self.pending_bots_by_site[
                site
            ].pop(0)
            next_panel.log_widget.append(
                "▶️ Bot precedente completato. Avvio da coda..."
            )
            self._start_bot(next_bot_id, next_panel, site, next_log_message)

    def _check_updates(self):
        """Controlla gli aggiornamenti in background."""
        check_for_updates(
            parent=self.mw, silent=True, callback=self.mw._show_update_banner
        )

    def _forward_notification_to_telegram(self, notification):
        """Inoltra notifiche importanti al bot Telegram."""
        if notification.get("title") == "Telegram":
            return

        level = notification.get("level", "info")
        if level in ["success", "error", "warning"]:
            title = notification.get("title", "Notifica")
            msg = notification.get("message", "")
            icon = (
                "[OK]" if level == "success" else "[ERR]" if level == "error" else "[!]"
            )
            text = f"{icon} *{title}*\n{msg}"
            self.telegram.send_message_sync(text)
