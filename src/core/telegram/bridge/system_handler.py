"""
SyncroJob - Telegram Bridge System Handler
Gestisce screenshot, report PDF, stati di sistema e restart.
"""

import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from PyQt6.QtCore import QBuffer, QIODevice, QObject, QRect, Qt
from PyQt6.QtGui import QGuiApplication, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication

from src.core import config_manager
from src.core.contabilita_manager import ContabilitaManager
from src.utils.document_generator import generate_pdf_from_html

if TYPE_CHECKING:
    from src.gui.main_window.main import MainWindow

logger = logging.getLogger(__name__)


class TelegramSystemHandler(QObject):
    """Gestisce operazioni di sistema e generazione report per Telegram."""

    def __init__(self, main_window: "MainWindow", telegram_service: Any) -> None:
        super().__init__(main_window)
        self.mw = main_window
        self.telegram = telegram_service

    def handle_status(self) -> None:
        """Invia lo stato corrente dell'applicazione."""
        panel = self.mw.bot_controller._get_active_bot_panel()
        if panel and hasattr(panel, "get_current_status"):
            status, msg = panel.get_current_status()
            bot_name = getattr(panel, "bot_name", "Sconosciuto")
            text = f"📊 **Stato Sistema**\n\nAttività: {bot_name}\nStato: {status}\nDettaglio: {msg}"
        else:
            text = "📊 **Stato Sistema**\n\nIl sistema è in attesa (Idle)."
        self.telegram.send_message_sync(text)

    def handle_screenshot(self, mode: str = "app") -> None:
        """Cattura e invia uno screenshot."""
        try:
            if mode == "app":
                pixmap = self.mw.grab()
                caption = "Solo App"
            else:
                screens = QGuiApplication.screens()
                total_rect = QRect()
                for s in screens:
                    total_rect = total_rect.united(s.geometry())
                combined = QPixmap(total_rect.size())
                combined.fill(Qt.GlobalColor.black)
                p = QPainter(combined)
                for s in screens:
                    p.drawPixmap(s.geometry().topLeft() - total_rect.topLeft(), s.grabWindow(cast("Any", 0)))
                p.end()
                pixmap = combined
                caption = f"Desktop ({len(screens)} monitor)"

            buf = QBuffer()
            buf.open(QIODevice.OpenModeFlag.WriteOnly)
            pixmap.save(buf, "PNG")
            self.telegram.send_photo_sync(buf.data().data(), caption=f"📸 **Screenshot: {caption}**")
        except Exception as e:
            self.telegram.send_message_sync(f"❌ Errore screenshot: {e}")

    def handle_search_db_pdf(self, params: dict[str, Any]) -> None:
        """Genera e invia un report PDF."""
        db_type = params.get("db", "")
        query_text = params.get("query", "")
        year_filter = params.get("year")

        self.telegram.send_message_sync(f"🔍 Ricerca in corso in **{db_type}** per: `{query_text}`...")

        try:
            report_data = self._fetch_report_data(db_type, query_text, year_filter)
            if not report_data:
                self.telegram.send_message_sync("❌ Nessun risultato trovato.")
                return

            html = self._generate_report_html(db_type, report_data)
            self._send_pdf_report(db_type, html)
        except Exception as e:
            self.telegram.send_message_sync(f"❌ Errore: {e}")

    def _fetch_report_data(self, db_type, query, year) -> Any:
        if db_type == "timbrature":
            panel = getattr(self.mw, "timbrature_db_panel", None)
            if panel and hasattr(panel, "storage"):
                return panel.storage.get_timbrature_with_reparto(limit=500, filter_text=query)
        if db_type == "strumentale":
            return ContabilitaManager.search_extended(query, year=(int(year) if year else None), limit=500)
        return None

    def _generate_report_html(self, db_type, data) -> str:
        if db_type == "timbrature":
            html = "<h2>Report Timbrature</h2><table><thead><tr><th>Data</th><th>Ingresso</th><th>Uscita</th><th>Nominativo</th></tr></thead><tbody>"
            for r in data:
                html += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[4]} {r[3]}</td></tr>"
            return html + "</tbody></table>"

        if db_type == "strumentale":
            if not data.get("GIORNALIERE"):
                return ""
            html = "<h2>Report Contabilità</h2><h3>Giornaliere</h3><table>"
            for g in data["GIORNALIERE"]:
                html += f"<tr><td>{g['data']}</td><td>{g['personale']}</td><td>{g['descrizione']}</td></tr>"
            return html + "</table>"
        return ""

    def _send_pdf_report(self, db_type, html):
        if not html:
            self.telegram.send_message_sync("❌ Errore: Dati non validi per il report.")
            return

        filename = f"report_{db_type}_{int(datetime.now().timestamp())}.pdf"
        temp_dir = config_manager.CONFIG_DIR / "temp"
        temp_dir.mkdir(exist_ok=True)
        path = str(temp_dir / filename)

        generate_pdf_from_html(html, path)
        if Path(path).exists():
            self.telegram.send_document_sync(path, caption=f"📄 Report {db_type}")
        else:
            self.telegram.send_message_sync("❌ Errore generazione PDF.")

    def handle_restart_app(self) -> None:
        """Riavvia l'applicazione."""
        try:
            subprocess.Popen(["cmd.exe", "/c", "start", os.path.abspath("avvio.bat")])
            QApplication.quit()
        except Exception as e:
            self.telegram.send_message_sync(f"❌ Errore riavvio: {e}")
