import asyncio
import os
import subprocess
import threading
from datetime import datetime

from PyQt6.QtCore import QObject, Qt
from PyQt6.QtGui import QGuiApplication, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication

from src.core import config_manager
from src.core.notification_manager import NotificationManager
from src.core.secrets_manager import SecretsManager
from src.utils.document_generator import generate_pdf_from_html


class TelegramUIBridge(QObject):
    """Ponte tra il servizio Telegram e l'interfaccia utente (MainWindow)."""

    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window
        self.telegram = main_window.telegram

    def setup_connections(self):
        """Collega i segnali del servizio Telegram agli handler."""
        self.telegram.log_signal.connect(
            lambda m: NotificationManager.instance().add_notification("Telegram", m)
        )
        self.telegram.command_received.connect(self._handle_command)
        self.telegram.data_received.connect(self._handle_data)
        self.telegram.status_requested.connect(self._handle_status)
        self.telegram.screenshot_requested.connect(self._handle_screenshot)
        self.telegram.query_received.connect(self._handle_ai_query)
        self.telegram.photo_received.connect(self._handle_photo)
        self.telegram.intent_received.connect(self._handle_intent)

    def _handle_intent(self, chat_id, intent):
        """Gestisce l'intento estratto dall'AI."""
        from src.utils.validators import InputValidator
        action = intent.get("action")
        obj = intent.get("object")
        items = intent.get("items", [])

        # 1. Aggiunta Dati
        if items:
            if obj == "pdl":
                valid_pdl = []
                for i in items:
                    res = InputValidator.validate_pdl(i)
                    if res.valid:
                        valid_pdl.append({"numero_pdl": res.sanitized_value})
                if valid_pdl:
                    self.mw.pdl_panel.add_rows_simple(valid_pdl)
                    self.mw.show_toast(f"Telegram: aggiunti {len(valid_pdl)} PDL via AI")
            elif obj == "oda":
                valid_oda = []
                for i in items:
                    res = InputValidator.validate_oda(i)
                    if res.valid:
                        valid_oda.append({"numero_oda": res.sanitized_value})
                if valid_oda:
                    self.mw.scarico_panel.add_rows_simple(valid_oda)
                    self.mw.show_toast(f"Telegram: aggiunti {len(valid_oda)} OdA via AI")

        # 2. Esecuzione Azione
        if action == "print" and obj == "pdl":
            self.telegram.pending_data[int(chat_id)] = {"action": "print", "items": items}
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup

            from src.utils.printing import get_installed_printers
            printers = get_installed_printers()
            keyboard = [[InlineKeyboardButton(f"🖨️ {p[:30]}", callback_data=f"sel_print_run_{p[:25]}")] for p in printers[:6]]
            self.telegram.send_message_sync("✅ Ho aggiunto i PDL. **Quale stampante utilizzo?**")
            asyncio.run_coroutine_threadsafe(
                self.telegram.app.bot.send_message(
                    chat_id=chat_id,
                    text=f"✅ PDL {', '.join(items)} pronti. **Quale stampante uso?**",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                ),
                self.telegram.loop,
            )
        elif action == "download" and obj == "pdl":
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            keyboard = [[InlineKeyboardButton("✅ Sì, stampa", callback_data="confirm_print_yes"),
                         InlineKeyboardButton("❌ No, solo download", callback_data="confirm_print_no")]]
            asyncio.run_coroutine_threadsafe(
                self.telegram.app.bot.send_message(chat_id=chat_id, text="Aggiunti PDL. **Vuoi che li stampi anche?**", reply_markup=InlineKeyboardMarkup(keyboard)),
                self.telegram.loop,
            )
        elif action == "download" and obj == "oda":
            self._handle_command("run_ts", {})
        elif action == "download" and obj == "timbrature":
            self._handle_command("run_timbrature", {"period": "today"})
        elif action == "status":
            self._handle_status(chat_id)
        elif action == "restart":
            self._handle_command("restart_app", {})

    def _handle_command(self, command, params):
        """Gestisce i comandi testuali da Telegram."""
        if command == "search_db_pdf":
            self._handle_search_db_pdf(params)
        elif command == "run_pdl":
            self.mw.navigate_to_panel("scarico_pdl")
            print_enabled = params.get("print", False)
            self.mw.pdl_panel.print_check.setChecked(print_enabled)
            self.mw.pdl_panel.merge_and_send_from_telegram = params.get("merge_and_send", False)
            self.mw.pdl_panel.merge_all_session_from_telegram = params.get("merge_all", False)
            ready, msg = self.mw.pdl_panel.validate_ready()
            if not ready:
                self.telegram.send_message_sync(f"⚠️ Impossibile avviare Scarico PDL.\nMotivo: {msg}")
                return
            self.mw.pdl_panel.start_btn.click()
            self.telegram.send_message_sync(f"✅ Avvio Scarico PDL (Stampa={print_enabled})")
        elif command == "list_pdl":
            data = self.mw.pdl_panel.data_table.get_data()
            items = [str(row.get(next(iter(row)))) for row in data if row][:20]
            text = "📋 **Lista PDL Corrente:**\n" + "\n".join([f"• `{i}`" for i in items])
            self.telegram.send_message_sync(text)
        elif command == "clear_pdl":
            self.mw.pdl_panel.clear_rows_simple()
            self.telegram.send_message_sync("🗑️ Tabella PDL svuotata.")
        elif command == "run_ts":
            self.mw.navigate_to_panel("scarico_ts")
            ready, msg = self.mw.scarico_panel.validate_ready()
            if not ready:
                self.telegram.send_message_sync(f"⚠️ Impossibile avviare Scarico TS.\nMotivo: {msg}")
                return
            self.mw.scarico_panel.start_btn.click()
            self.telegram.send_message_sync("✅ Avvio Scarico Timesheet.")
        elif command == "run_carico":
            self.mw.navigate_to_panel("carico_ts")
            ready, msg = self.mw.carico_panel.validate_ready()
            if not ready:
                self.telegram.send_message_sync(f"⚠️ Impossibile avviare Carico TS.\nMotivo: {msg}")
                return
            self.mw.carico_panel.start_btn.click()
            self.telegram.send_message_sync("✅ Avvio Carico Timesheet.")
        elif command == "run_timbrature":
            self.mw.navigate_to_panel("timbrature")
            from PyQt6.QtCore import QDate
            period = params.get("period", "yesterday")
            target_date = QDate.currentDate()
            if period == "yesterday":
                target_date = target_date.addDays(-1)
            self.mw.timbrature_bot_panel.date_da_edit.setDate(target_date)
            self.mw.timbrature_bot_panel.date_a_edit.setDate(target_date)
            ready, msg = self.mw.timbrature_bot_panel.validate_ready()
            if not ready:
                self.telegram.send_message_sync(f"⚠️ Errore: {msg}")
                return
            self.mw.timbrature_bot_panel.start_btn.click()
            self.telegram.send_message_sync(f"✅ Avvio Scarico Timbrature ({period}).")
        elif command == "restart_app":
            try:
                subprocess.Popen(["cmd.exe", "/c", "start", os.path.abspath("avvio.bat")], shell=True)
                QApplication.quit()
            except Exception as e:
                self.telegram.send_message_sync(f"❌ Errore riavvio: {e}")
        elif command == "stop_all":
            panel = self.mw._get_active_bot_panel()
            if panel and hasattr(panel, "stop_btn") and panel.stop_btn.isEnabled():
                panel.stop_btn.click()
                self.telegram.send_message_sync("🛑 Stop inviato.")
            else:
                self.telegram.send_message_sync("ℹ️ Nessun processo attivo.")

    def _handle_search_db_pdf(self, params):
        """Genera e invia un report PDF via Telegram."""
        db_type = params.get("db", "")
        query_text = params.get("query", "")
        year_filter = params.get("year")
        self.telegram.send_message_sync(f"🔍 Ricerca in corso in **{db_type}** per: `{query_text}`...")

        try:
            html_report = ""
            filename = f"report_{db_type}_{int(datetime.now().timestamp())}.pdf"
            temp_dir = config_manager.CONFIG_DIR / "temp"
            temp_dir.mkdir(exist_ok=True)
            temp_pdf = str(temp_dir / filename)

            if db_type == "timbrature":
                rows = self.mw.timbrature_db_panel.storage.get_timbrature_with_reparto(limit=500, filter_text=query_text)
                if not rows:
                    self.telegram.send_message_sync("❌ Nessun risultato trovato.")
                    return
                html_report = "<h2>Report Timbrature</h2><table><thead><tr><th>Data</th><th>Ingresso</th><th>Uscita</th><th>Nominativo</th></tr></thead><tbody>"
                for r in rows:
                    html_report += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[4]} {r[3]}</td></tr>"
                html_report += "</tbody></table>"
            elif db_type == "strumentale":
                from src.core.contabilita_manager import ContabilitaManager
                matches = ContabilitaManager.search_extended(query_text, year=int(year_filter) if year_filter else None, limit=500)
                if not matches or (not matches.get("GIORNALIERE") and not matches.get("CANTIERE")):
                    self.telegram.send_message_sync("❌ Nessun risultato.")
                    return
                html_report = "<h2>Report Contabilità</h2>"
                if matches.get("GIORNALIERE"):
                    html_report += "<h3>Giornaliere</h3><table>"
                    for g in matches["GIORNALIERE"]:
                        html_report += f"<tr><td>{g['data']}</td><td>{g['personale']}</td><td>{g['descrizione']}</td></tr>"
                    html_report += "</table>"

            if html_report:
                generate_pdf_from_html(html_report, temp_pdf)
                if os.path.exists(temp_pdf):
                    self.telegram.send_document_sync(temp_pdf, caption=f"📄 Report {db_type}")
                else:
                    self.telegram.send_message_sync("❌ Errore generazione PDF.")
        except Exception as e:
            self.telegram.send_message_sync(f"❌ Errore: {e}")

    def _handle_data(self, data_type, items):
        """Gestisce l'inserimento dati da Telegram."""
        from src.utils.validators import InputValidator
        valid_items, duplicates, errors = [], 0, []
        panel = self.mw.pdl_panel if data_type == "pdl" else self.mw.scarico_panel
        field = "numero_pdl" if data_type == "pdl" else "numero_oda"
        validator = InputValidator.validate_pdl if data_type == "pdl" else InputValidator.validate_oda

        existing = [str(row.get(field, "")) for row in panel.data_table.get_data()]
        for item in items:
            res = validator(item)
            if res.valid:
                val = res.sanitized_value
                if val in existing or val in valid_items:
                    duplicates += 1
                else:
                    valid_items.append(val)
            else:
                errors.append(f"❌ `{item}`: {res.error}")

        if valid_items:
            panel.add_rows_simple([{field: v} for v in valid_items])
            self.mw.navigate_to_panel(panel.bot_id)
            self.mw.show_toast(f"Telegram: Aggiunti {len(valid_items)} elementi")

        feedback = [f"✅ Aggiunti {len(valid_items)}"] if valid_items else []
        if duplicates:
            feedback.append(f"ℹ️ {duplicates} duplicati saltati")
        if errors:
            feedback.append("⚠️ Errori:\n" + "\n".join(errors[:5]))
        self.telegram.send_message_sync("\n".join(feedback) if feedback else "⚠️ Nessun dato valido.")

    def _handle_status(self, chat_id):
        panel = self.mw._get_active_bot_panel()
        if panel and hasattr(panel, "get_current_status"):
            status, msg = panel.get_current_status()
            text = f"📊 **Stato Sistema**\n\nAttività: {panel.bot_name}\nStato: {status}\nDettaglio: {msg}"
        else:
            text = "📊 **Stato Sistema**\n\nIl sistema è in attesa (Idle)."
        self.telegram.send_message_sync(text)

    def _handle_screenshot(self, mode="app"):
        try:
            from PyQt6.QtCore import QBuffer, QIODevice, QRect
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
                    p.drawPixmap(s.geometry().topLeft() - total_rect.topLeft(), s.grabWindow(0))
                p.end()
                pixmap = combined
                caption = f"Desktop ({len(screens)} monitor)"

            buf = QBuffer()
            buf.open(QIODevice.OpenModeFlag.WriteOnly)
            pixmap.save(buf, "PNG")
            self.telegram.send_photo_sync(buf.data().data(), caption=f"📸 **Screenshot: {caption}**")
        except Exception as e:
            self.telegram.send_message_sync(f"❌ Errore screenshot: {e}")

    def _handle_ai_query(self, chat_id, query):
        api_key = SecretsManager.get_gemini_api_key()
        if not api_key:
            self.telegram.send_message_sync("⚠️ API Key mancante.")
            return
        def run():
            try:
                from src.core.lyra_client import LyraClient
                resp = LyraClient(api_key=api_key).ask(query)
                self.telegram.send_message_sync(f"🤖 **AI Coach**\n\n{resp}")
            except Exception as e:
                self.telegram.send_message_sync(f"❌ Errore AI: {e}")
        threading.Thread(target=run, daemon=True).start()

    def _handle_photo(self, chat_id, photo_bytes, caption):
        api_key = SecretsManager.get_gemini_api_key()
        if not api_key:
            self.telegram.send_message_sync("⚠️ API Key mancante.")
            return
        self.telegram.send_message_sync("🔍 **Analisi Documento...**")
        def run():
            try:
                import base64

                from src.core.lyra_client import LyraClient
                img_b64 = base64.b64encode(photo_bytes).decode("utf-8")
                prompt = "Estrai dati da questo rapportino. Tabella Markdown."
                if caption:
                    prompt += f"\nNote: {caption}"
                resp = LyraClient(api_key=api_key).ask(prompt, images=[img_b64])
                self.telegram.send_message_sync(f"📝 **Dati Estratti**\n\n{resp}")
            except Exception as e:
                self.telegram.send_message_sync(f"❌ Errore: {e}")
        threading.Thread(target=run, daemon=True).start()
