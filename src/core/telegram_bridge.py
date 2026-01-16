import asyncio
import base64  # Moved from _handle_photo
import os
import threading
from datetime import datetime
from typing import Any

from PyQt6.QtCore import QBuffer, QIODevice, QObject, QRect, Qt
from PyQt6.QtGui import QGuiApplication, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.core import config_manager
from src.core.contabilita_manager import ContabilitaManager
from src.core.lyra_client import LyraClient
from src.core.notification_manager import NotificationManager
from src.core.secrets_manager import SecretsManager
from src.utils.document_generator import generate_pdf_from_html
from src.utils.printing import get_installed_printers
from src.utils.validators import InputValidator


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
        action = intent.get("action")
        obj = intent.get("object")
        items = intent.get("items", [])

        # 1. Processamento Dati
        if items:
            self._process_intent_data(obj, items)

        # 2. Processamento Azione
        if action == "print" and obj == "pdl":
            self._handle_intent_print_pdl(chat_id, items)
        elif action == "download" and obj == "pdl":
            self._handle_intent_download_pdl(chat_id)
        elif action == "download":
            self._handle_intent_generic_download(obj)
        elif action == "status":
            self._handle_status(chat_id)
        elif action == "restart":
            self._handle_command("restart_app", {})

    def _process_intent_data(self, obj, items):
        """Valida e aggiunge dati ai pannelli corrispondenti."""
        if obj == "pdl":
            valid = [i for i in items if InputValidator.validate_pdl(i).valid]
            if valid:
                self.mw.pdl_panel.add_rows_simple(
                    [{"numero_pdl": InputValidator.validate_pdl(v).sanitized_value} for v in valid]
                )
                self.mw.show_toast(f"Telegram: aggiunti {len(valid)} PDL")
        elif obj == "oda":
            valid = [i for i in items if InputValidator.validate_oda(i).valid]
            if valid:
                self.mw.scarico_panel.add_rows_simple(
                    [{"numero_oda": InputValidator.validate_oda(v).sanitized_value} for v in valid]
                )
                self.mw.show_toast(f"Telegram: aggiunti {len(valid)} OdA")

    def _handle_intent_print_pdl(self, chat_id, items):
        self.telegram.pending_data[int(chat_id)] = {"action": "print", "items": items}
        printers = get_installed_printers()[:6]
        keyboard = [
            [InlineKeyboardButton(f"🖨️ {p[:30]}", callback_data=f"sel_print_run_{p[:25]}")] for p in printers
        ]

        self.telegram.send_message_sync("✅ Ho aggiunto i PDL. **Quale stampante utilizzo?**")
        coro = self.telegram.app.bot.send_message(
            chat_id=chat_id,
            text=f"✅ PDL {', '.join(items)} pronti. **Quale stampante uso?**",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        # Compatibilità per test: se coro non è una coroutine (mock), lo wrappiamo
        if not asyncio.iscoroutine(coro):

            async def _fake():
                return None

            coro = _fake()

        asyncio.run_coroutine_threadsafe(coro, self.telegram.loop)

    def _handle_intent_download_pdl(self, chat_id):
        keyboard = [
            [
                InlineKeyboardButton("✅ Sì, stampa", callback_data="confirm_print_yes"),
                InlineKeyboardButton("❌ No, solo download", callback_data="confirm_print_no"),
            ]
        ]
        coro = self.telegram.app.bot.send_message(
            chat_id=chat_id,
            text="Aggiunti PDL. **Vuoi che li stampi anche?**",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        # Compatibilità per test: se coro non è una coroutine (mock), lo wrappiamo
        if not asyncio.iscoroutine(coro):

            async def _fake():
                return None

            coro = _fake()

        asyncio.run_coroutine_threadsafe(coro, self.telegram.loop)

    def _handle_intent_generic_download(self, obj):
        if obj == "oda":
            self._handle_command("run_ts", {})
        elif obj == "timbrature":
            self._handle_command("run_timbrature", {"period": "today"})

    def _handle_command(self, command, params):
        """Gestisce i comandi testuali da Telegram."""
        if command == "search_db_pdf":
            self._handle_search_db_pdf(params)
        elif command == "run_pdl":
            self._handle_run_pdl(params)
        elif command == "list_pdl":
            self._handle_list_pdl()
        elif command == "clear_pdl":
            self._handle_clear_pdl()
        elif command == "run_ts":
            self._handle_run_ts()
        elif command == "run_carico":
            self._handle_run_carico()
        elif command == "run_prenota_bp":
            self._handle_run_prenota_bp()
        elif command == "run_timbrature":
            self._handle_run_timbrature(params)
        elif command == "restart_app":
            self._handle_restart_app()
        elif command == "stop_all":
            self._handle_stop_all()

    def _handle_run_pdl(self, params):
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

    def _handle_list_pdl(self):
        data = self.mw.pdl_panel.data_table.get_data()
        items = [str(row.get(next(iter(row)))) for row in data if row][:20]
        text = "📋 **Lista PDL Corrente:**\n" + "\n".join([f"• `{i}`" for i in items])
        self.telegram.send_message_sync(text)

    def _handle_clear_pdl(self):
        self.mw.pdl_panel.clear_rows_simple()
        self.telegram.send_message_sync("🗑️ Tabella PDL svuotata.")

    def _handle_run_ts(self):
        self.mw.navigate_to_panel("scarico_ts")
        ready, msg = self.mw.scarico_panel.validate_ready()
        if not ready:
            self.telegram.send_message_sync(f"⚠️ Impossibile avviare Scarico TS.\nMotivo: {msg}")
            return
        self.mw.scarico_panel.start_btn.click()
        self.telegram.send_message_sync("✅ Avvio Scarico Timesheet.")

    def _handle_run_carico(self):
        self.mw.navigate_to_panel("carico_ts")
        ready, msg = self.mw.carico_panel.validate_ready()
        if not ready:
            self.telegram.send_message_sync(f"⚠️ Impossibile avviare Carico TS.\nMotivo: {msg}")
            return
        self.mw.carico_panel.start_btn.click()
        self.telegram.send_message_sync("✅ Avvio Carico Timesheet.")

    def _handle_run_prenota_bp(self):
        self.mw.navigate_to_panel("prenota_bp")
        # In main_window.py navigate_to_panel("prenota_bp") maps to index (0, 3)
        # We need to access the panel instance.
        # It's inside mw.tab_fornitori (index 3)

        # Accessing via bot_controller helper would be cleaner but let's use direct access for now
        # waiting for the UI to switch
        QApplication.processEvents()

        # Access panel
        panel = self.mw.tab_fornitori.widget(3)  # Index 3 as per map

        if not panel:
            self.telegram.send_message_sync("⚠️ Errore interno: Pannello Prenota BP non trovato.")
            return

        ready, msg = panel.validate_ready()
        if not ready:
            self.telegram.send_message_sync(f"⚠️ Impossibile avviare Prenota BP.\nMotivo: {msg}")
            return
        panel.start_btn.click()
        self.telegram.send_message_sync("✅ Avvio Prenotazione BP.")

    def _handle_restart_app(self):
        try:
            import subprocess

            subprocess.Popen(["cmd.exe", "/c", "start", os.path.abspath("avvio.bat")])
            QApplication.quit()
        except Exception as e:
            self.telegram.send_message_sync(f"❌ Errore riavvio: {e}")

    def _handle_stop_all(self):
        panel = self.mw.bot_controller._get_active_bot_panel()
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
            return self.mw.timbrature_db_panel.storage.get_timbrature_with_reparto(
                limit=500, filter_text=query
            )
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
        if os.path.exists(path):
            self.telegram.send_document_sync(path, caption=f"📄 Report {db_type}")
        else:
            self.telegram.send_message_sync("❌ Errore generazione PDF.")

    def _handle_data(self, data_type, items):
        """Gestisce l'inserimento dati da Telegram."""
        if data_type == "pdl":
            self._process_pdl_items(items)
        elif data_type == "oda":
            self._process_oda_items(items)
        elif data_type == "bp":
            self._process_bp_items(items)

    def _process_pdl_items(self, items):
        """Processa i PDL da Telegram."""
        valid_items, duplicates, errors = self._validate_and_filter_items(
            items, "numero_pdl", InputValidator.validate_pdl, self.mw.pdl_panel
        )
        if valid_items:
            self.mw.pdl_panel.add_rows_simple([{"numero_pdl": v} for v in valid_items])
            self.mw.navigate_to_panel("scarico_pdl")
        self._send_data_feedback(len(valid_items), duplicates, errors)

    def _process_oda_items(self, items):
        """Processa gli OdA da Telegram."""
        valid_items, duplicates, errors = self._validate_and_filter_items(
            items, "numero_oda", InputValidator.validate_oda, self.mw.scarico_panel
        )
        if valid_items:
            self.mw.scarico_panel.add_rows_simple([{"numero_oda": v} for v in valid_items])
            self.mw.navigate_to_panel("scarico_ts")
        self._send_data_feedback(len(valid_items), duplicates, errors)

    def _process_bp_items(self, items):
        """Processa i BP da Telegram."""
        self.mw.navigate_to_panel("prenota_bp")
        panel = self.mw.tab_fornitori.widget(3)
        if not panel:
            return

        valid_items, duplicates = [], 0

        for item in items:
            item = item.strip()
            if not item:
                continue
            parts = item.split(" ", 1)
            bp_num = parts[0].strip()
            bp_note = parts[1].strip() if len(parts) > 1 else ""

            if any(v.get("NUMERO BP") == bp_num for v in valid_items):
                duplicates += 1
            else:
                valid_items.append({"NUMERO BP": bp_num, "NOTE DI RITIRO": bp_note})

        if valid_items:
            panel.data_table.set_data(valid_items)
            if hasattr(panel, "_save_data"):
                panel._save_data()
            self.mw.show_toast(f"Telegram: Impostati {len(valid_items)} BP")

        self._send_data_feedback(len(valid_items), duplicates, [])

    def _validate_and_filter_items(self, items, field, validator_func, panel):
        """Valida e filtra i dati in ingresso."""
        valid_items, duplicates, errors = [], 0, []
        existing = [str(row.get(field, "")) for row in panel.data_table.get_data()]

        for item in items:
            res = validator_func(item)
            if res.valid:
                val = res.sanitized_value
                if val in existing or val in valid_items:
                    duplicates += 1
                else:
                    valid_items.append(val)
            else:
                errors.append(f"❌ `{item}`: {res.error}")
        return valid_items, duplicates, errors

    def _send_data_feedback(self, count_valid, duplicates, errors):
        """Invia feedback a Telegram."""
        feedback = []
        if count_valid:
            feedback.append(f"✅ Aggiunti/Impostati {count_valid}")
        if duplicates:
            feedback.append(f"ℹ️ {duplicates} duplicati ignorati")
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
                img_b64 = base64.b64encode(photo_bytes).decode("utf-8")
                prompt = "Estrai dati da questo rapportino. Tabella Markdown."
                if caption:
                    prompt += f"\nNote: {caption}"
                resp = LyraClient(api_key=api_key).ask(prompt, images=[img_b64])
                self.telegram.send_message_sync(f"📝 **Dati Estratti**\n\n{resp}")
            except Exception as e:
                self.telegram.send_message_sync(f"❌ Errore: {e}")

        threading.Thread(target=run, daemon=True).start()
