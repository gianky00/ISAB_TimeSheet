"""SyncroJob - Telegram Bridge System Handler (Refactored).

Gestisce screenshot, report PDF e stati via interfacce agnostiche.
Agnostico rispetto a PySide6.
"""

import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.core import config_manager
from src.core.contabilita_manager import ContabilitaManager
from src.core.telegram.bridge.interfaces import AppStatusProvider, ScreenshotProvider
from src.utils.document_generator import generate_pdf_from_html

logger = logging.getLogger(__name__)


class TelegramSystemHandler:
    """Gestisce operazioni di sistema e generazione report per Telegram."""

    def __init__(
        self,
        telegram_service: Any,
        screenshot_provider: ScreenshotProvider,
        app_status_provider: AppStatusProvider,
        # Supporto per fetch dati (provvisorio per mantenere funzionalita)
        data_bridge: Any = None,
    ) -> None:
        self.telegram = telegram_service
        self.screenshot_provider = screenshot_provider
        self.status_provider = app_status_provider
        self.data_bridge = data_bridge

    def handle_status(self) -> None:
        """Invia lo stato corrente dell'applicazione."""
        bot_name, status, msg = self.status_provider.get_system_status()
        if bot_name == "Idle":
            text = "   **Stato Sistema**\n\nIl sistema  in attesa (Idle)."
        else:
            text = f"   **Stato Sistema**\n\nAttività: {bot_name}\nStato: {status}\nDettaglio: {msg}"
        self.telegram.send_message_sync(text)

    def handle_screenshot(self, mode: str = "app") -> None:
        """Cattura e invia uno screenshot tramite il provider GUI."""
        try:
            if mode == "app":
                data = self.screenshot_provider.capture_app_screenshot()
                caption = "Solo App"
            else:
                data = self.screenshot_provider.capture_desktop_screenshot()
                caption = "Desktop"

            self.telegram.send_photo_sync(data, caption=f"   **Screenshot: {caption}**")
        except Exception as e:
            self.telegram.send_message_sync(f"❌ Errore screenshot: {e}")

    def handle_search_db_pdf(self, params: dict[str, Any]) -> None:
        """Genera e invia un report PDF."""
        db_type = params.get("db", "")
        query_text = params.get("query", "")
        year_filter = params.get("year")

        self.telegram.send_message_sync(f"[CERCA] Ricerca in corso in **{db_type}** per: `{query_text}`...")

        try:
            report_data = self._fetch_report_data(db_type, query_text, year_filter)
            if not report_data:
                self.telegram.send_message_sync("❌ Nessun risultato trovato.")
                return

            html = self._generate_report_html(db_type, report_data)
            self._send_pdf_report(db_type, html)
        except Exception as e:
            self.telegram.send_message_sync(f"❌ Errore: {e}")

    def _fetch_report_data(self, db_type: str, query: str, year: int | str | None) -> Any:
        # Se abbiamo il data_bridge (che punta alla MainWindow o Storage), lo usiamo
        if db_type == "timbrature" and self.data_bridge:
            panel = getattr(self.data_bridge, "timbrature_db_panel", None)
            if panel and hasattr(panel, "storage"):
                return panel.storage.get_timbrature_with_reparto(limit=500, filter_text=query)
        if db_type == "strumentale":
            return ContabilitaManager.search_extended(query, year=(int(year) if year else None), limit=500)
        return None

    def _generate_report_html(self, db_type: str, data: Any) -> str:
        if db_type == "timbrature":
            html = "<h2>Report Timbrature</h2><table><thead><tr><th>Data</th><th>Ingresso</th><th>Uscita</th><th>Nominativo</th></tr></thead><tbody>"
            for r in data:
                html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[4]} {r[3]}</td></tr>"
            return html + "</tbody></table>"

        if db_type == "strumentale":
            if not data or not data.get("GIORNALIERE"):
                return ""
            html = "<h2>Report Contabilità</h2><h3>Giornaliere</h3><table>"
            for g in data["GIORNALIERE"]:
                html += f"<tr><td>{g['data']}</td><td>{g['personale']}</td><td>{g['descrizione']}</td></tr>"
            return html + "</table>"
        return ""

    def _send_pdf_report(self, db_type: str, html: str) -> None:
        if not html:
            self.telegram.send_message_sync("❌ Errore: Dati non validi per il report.")
            return

        filename = f"report_{db_type}_{int(datetime.now(UTC).timestamp())}.pdf"
        temp_dir = config_manager.CONFIG_DIR / "temp"
        temp_dir.mkdir(exist_ok=True)
        path = str(temp_dir / filename)

        generate_pdf_from_html(html, path)
        if Path(path).exists():
            self.telegram.send_document_sync(path, caption=f"   Report {db_type}")
        else:
            self.telegram.send_message_sync("❌ Errore generazione PDF.")

    def handle_restart_app(self) -> None:
        """Riavvia l'applicazione delegando alla GUI."""
        self.status_provider.restart_application()
