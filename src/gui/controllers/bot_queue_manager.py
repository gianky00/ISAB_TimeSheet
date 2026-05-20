"""
SyncroJob - Bot Queue Manager
Gestore della coda di esecuzione dei bot con vincoli di parallelismo per sito.
Garantisce che venga eseguito un solo bot Selenium per volta sullo stesso portale.
"""

import logging
from contextlib import suppress
from typing import Any

logger = logging.getLogger(__name__)


class BotQueueManager:
    """Gestisce l'accodamento e l'esecuzione sequenziale dei bot per sito."""

    def __init__(self) -> None:
        self.running_bots_by_site: dict[str, list[str]] = {"portale_fornitori": [], "safework": []}
        self.pending_bots_by_site: dict[str, list[tuple[str, Any, str]]] = {
            "portale_fornitori": [],
            "safework": [],
        }

    def schedule_bot(self, bot_id: str, panel: Any, site: str, log_message: str) -> None:
        """Gestisce l'accodamento di un bot rispettando i vincoli di un'unica istanza Selenium per sito."""
        if self.running_bots_by_site.get(site):
            self.pending_bots_by_site[site].append((bot_id, panel, log_message))
            if hasattr(panel, "log_widget"):
                panel.log_widget.append(f"    Bot in coda. Sito {site.replace('_', ' ').title()} occupato.")
            logger.info(f"Bot {bot_id} accodato per il sito {site}.")
        else:
            self._start_bot(bot_id, panel, site, log_message)

    def _start_bot(self, bot_id: str, panel: Any, site: str, log_message: str) -> None:
        """Avvia l'esecuzione del bot e registra il callback per la gestione della coda al termine."""
        if hasattr(panel, "start_btn") and not panel.start_btn.isEnabled():
            logger.warning(f"Impossibile avviare {bot_id}: pulsante avvio disabilitato.")
            return

        self.running_bots_by_site[site].append(bot_id)
        if hasattr(panel, "log_widget"):
            panel.log_widget.append(log_message)

        if hasattr(panel, "status_changed"):
            # Rimuoviamo eventuali callback precedenti per sicurezza
            if hasattr(panel, "_service_callback") and panel._service_callback:
                with suppress(Exception):
                    panel.status_changed.disconnect(panel._service_callback)

            def on_finished(st: str, msg: str) -> None:
                # Stati di completamento (sia slug che colori legacy)
                if st in ("completed", "error", "stopped", "#2E7D32", "#C62828", "#ffc107"):
                    self._on_bot_completed(bot_id, site, panel)

            panel._service_callback = on_finished
            panel.status_changed.connect(on_finished)

        if hasattr(panel, "_on_start"):
            panel._on_start()
        logger.info(f"Bot {bot_id} avviato per il sito {site}.")

    def _on_bot_completed(self, bot_id: str, site: str, panel: Any) -> None:
        """Rimuove il bot concluso dalla lista attiva e avvia il prossimo elemento in coda per quel sito."""
        if bot_id in self.running_bots_by_site[site]:
            self.running_bots_by_site[site].remove(bot_id)

        # Disconnessione callback
        if hasattr(panel, "_service_callback") and panel._service_callback:
            with suppress(Exception):
                panel.status_changed.disconnect(panel._service_callback)
                panel._service_callback = None

        logger.info(f"Bot {bot_id} completato sul sito {site}.")

        # Avvio prossimo in coda
        if self.pending_bots_by_site.get(site):
            nxt_id, nxt_p, nxt_msg = self.pending_bots_by_site[site].pop(0)
            if hasattr(nxt_p, "log_widget"):
                nxt_p.log_widget.append("    Avvio da coda...")
            self._start_bot(nxt_id, nxt_p, site, nxt_msg)
