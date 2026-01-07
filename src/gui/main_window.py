"""
Bot TS - Main Window
Finestra principale dell'applicazione.
"""
import sys
import os
import subprocess
import requests
import asyncio
import threading
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QStackedWidget, QFrame, QSplashScreen, QApplication, QTabWidget,
    QProgressBar, QStatusBar, QLineEdit, QMenu, QSystemTrayIcon
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter, QKeySequence, QShortcut, QIcon, QAction
from datetime import datetime
from pathlib import Path

# Import Panels
from src.gui.panels import ScaricaTSPanel, CaricoTSPanel, DettagliOdAPanel, TimbratureBotPanel, TimbratureDBPanel, ScaricoPDLPanel
from src.gui.contabilita_panel import ContabilitaPanel
from src.gui.scarico_ore_panel import ScaricoOrePanel
from src.gui.settings_panel import SettingsPanel
from src.gui.help_panel import HelpPanel
from src.gui.dashboard_panel import DashboardPanel
from src.gui.lyra_panel import LyraPanel
from src.gui.notifications_panel import NotificationsPanel

# Import Core
from src.core.lyra_sentinel import LyraSentinel
from src.core.license_validator import get_license_info
from src.core.secrets_manager import SecretsManager
from src.core import config_manager
from src.core.app_updater import check_for_updates
from src.utils.validators import InputValidator
from src.core.notification_manager import NotificationManager
from src.core.backup_manager import BackupManager
from src.core.telegram_manager import TelegramService
from src.bots.portale_fornitori.timbrature.storage import TimbratureStorage
from src.utils.helpers import get_asset_path, get_app_icon_path

# Import UI/UX Components
from src.gui.widgets.toast import ToastManager
from src.gui.widgets.status_card import StatusCard
from src.gui.styles import apply_theme


class SidebarButton(QPushButton):
    """Pulsante personalizzato per la sidebar."""
    
    def __init__(self, text: str, icon: str = "", parent=None):
        super().__init__(parent)
        self.setText(f"{icon} {text}" if icon else text)
        self.setCheckable(True)
        self.setMinimumHeight(55)
        self.setMinimumWidth(180)
        self._original_text = f"{icon} {text}" if icon else text
        self._update_style()
        self.toggled.connect(self._update_style)
    
    def set_badge(self, count: int):
        """Imposta un badge di notifica."""
        if count > 0:
            self.setText(f"{self._original_text} 🔴 {count}")
        else:
            self.setText(self._original_text)

    def _update_style(self):
        """Aggiorna lo stile in base allo stato."""
        if self.isChecked():
            self.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.25);
                    color: #ffffff;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 8px;
                    padding: 12px 18px;
                    text-align: left;
                    font-weight: bold;
                    font-size: 16px;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #ffffff;
                    border: 1px solid transparent;
                    border-radius: 8px;
                    padding: 12px 18px;
                    text-align: left;
                    font-size: 16px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.15);
                    color: white;
                }
            """)


class MainWindow(QMainWindow):
    """Finestra principale dell'applicazione SyncroJob."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SyncroJob")
        self.setMinimumSize(1200, 800)
        
        # Load main_window.qss
        style_file_path = Path("assets/styles/main_window.qss")
        if style_file_path.exists():
            with open(style_file_path, "r", encoding="utf-8") as f:
                main_window_qss = f.read()
                self.setStyleSheet(main_window_qss)
        else:
            print(f"Warning: {style_file_path} not found.")

        # Load message_box.qss
        message_box_style_path = Path("assets/styles/message_box.qss")
        if message_box_style_path.exists():
            with open(message_box_style_path, "r", encoding="utf-8") as f:
                message_box_qss = f.read()
                # Append to existing stylesheet
                self.setStyleSheet(self.styleSheet() + message_box_qss)
        else:
            print(f"Warning: {message_box_style_path} not found.")

        # Apply Global Theme (light.qss)
        apply_theme(QApplication.instance(), "light")

        # Abilita Drag & Drop
        self.setAcceptDrops(True)

        self._current_page_index = 0
        self._force_quit = False # NEW: Controllo chiusura definitiva
        self._setup_ui()
        self._setup_tray_icon() # NEW: Tray Icon
        self._connect_signals()
        self._setup_shortcuts()

        # Toast notification system is now global via ToastManager
        # We can still expose a helper if needed, but components use ToastManager directly.

        # Lyra Sentinel (Monitoraggio Anomalie)
        self.sentinel = LyraSentinel()
        self.sentinel.anomalies_found.connect(self._on_anomalies_found)
        QTimer.singleShot(2000, self.sentinel.start) # Ritarda leggermente l'avvio

        # Telegram Service
        self.telegram = TelegramService()
        self.telegram.log_signal.connect(lambda m: NotificationManager.instance().add_notification("Telegram", m))
        self.telegram.command_received.connect(self._handle_telegram_command)
        self.telegram.data_received.connect(self._handle_telegram_data)
        self.telegram.status_requested.connect(self._handle_telegram_status)
        self.telegram.screenshot_requested.connect(self._handle_telegram_screenshot)
        self.telegram.query_received.connect(self._handle_telegram_ai_query)
        self.telegram.photo_received.connect(self._handle_telegram_photo)
        self.telegram.intent_received.connect(self._handle_telegram_intent)
        QTimer.singleShot(1000, self.telegram.start_service)

        # Inoltro notifiche a Telegram
        NotificationManager.instance().notification_added.connect(self._forward_notification_to_telegram)

        # Avvio automatico importazione contabilità se abilitato
        QTimer.singleShot(1000, self._check_and_start_contabilita_update)

        # Controllo aggiornamenti applicazione (dopo 3 secondi)
        QTimer.singleShot(3000, self._check_updates)
    
    def _handle_bot_results(self, bot_id, results):
        """Gestisce i risultati prodotti dai bot (es. file scaricati) e li invia a Telegram."""
        if bot_id == "scarico_pdl":
            for file_path in results:
                if os.path.exists(file_path):
                    self.telegram.send_document_sync(
                        file_path, 
                        caption=f"📄 **PDL Scaricato**\nFile: `{os.path.basename(file_path)}`"
                    )

    def _handle_telegram_intent(self, chat_id, intent):
        """Gestisce l'intento estratto dall'AI (testo o vocale)."""
        action = intent.get("action")
        obj = intent.get("object")
        items = intent.get("items", [])
        
        # 1. Aggiunta Dati (se presenti)
        if items:
            if obj == "pdl":
                # Validazione e aggiunta silenziosa (senza feedback immediato se c'è un'azione dopo)
                valid_pdl = []
                for i in items:
                    res = InputValidator.validate_pdl(i)
                    if res.valid: valid_pdl.append({"numero_pdl": res.sanitized_value})
                
                if valid_pdl:
                    self.pdl_panel.add_rows_simple(valid_pdl)
                    self.show_toast(f"Telegram: aggiunti {len(valid_pdl)} PDL via AI")
            
            elif obj == "oda":
                valid_oda = []
                for i in items:
                    res = InputValidator.validate_oda(i)
                    if res.valid: valid_oda.append({"numero_oda": res.sanitized_value})
                
                if valid_oda:
                    self.scarico_panel.add_rows_simple(valid_oda)
                    self.show_toast(f"Telegram: aggiunti {len(valid_oda)} OdA via AI")

        # 2. Esecuzione Azione
        if action == "print":
            if obj == "pdl":
                # Salva in pending e chiedi stampante
                self.telegram.pending_data[int(chat_id)] = {"action": "print", "items": items}
                from telegram import InlineKeyboardButton, InlineKeyboardMarkup
                from src.utils.printing import get_installed_printers
                printers = get_installed_printers()
                keyboard = [[InlineKeyboardButton(f"🖨️ {p[:30]}", callback_data=f"sel_print_run_{p[:25]}")] for p in printers[:6]]
                self.telegram.send_message_sync(f"✅ Ho aggiunto i PDL. **Quale stampante utilizzo?**", 
                                              # Nota: TelegramService gestisce la tastiera se passata? No, devo aggiungerlo o farlo via callback
                                              )
                # Fallback: se non posso mandare la tastiera da qui facilmente, emetto un comando di richiesta stampante
                self.telegram.send_message_sync("⚠️ Seleziona la stampante dal menu PDL -> Avvia (Stampa ON) oppure usa i bottoni nel menu Impostazioni.")
                # Implementazione più pulita: chiamiamo un metodo interno di telegram
                asyncio.run_coroutine_threadsafe(
                    self.telegram.app.bot.send_message(
                        chat_id=chat_id, 
                        text=f"✅ PDL {', '.join(items)} pronti. **Quale stampante uso?**",
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    ), 
                    self.telegram.loop
                )

        elif action == "download":
            if obj == "pdl":
                # Chiedi se vuole stampare
                from telegram import InlineKeyboardButton, InlineKeyboardMarkup
                keyboard = [[
                    InlineKeyboardButton("✅ Sì, stampa", callback_data="confirm_print_yes"),
                    InlineKeyboardButton("❌ No, solo download", callback_data="confirm_print_no")
                ]]
                asyncio.run_coroutine_threadsafe(
                    self.telegram.app.bot.send_message(
                        chat_id=chat_id, 
                        text=f"Aggiunti PDL. **Vuoi che li stampi anche?**",
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    ), 
                    self.telegram.loop
                )
            elif obj == "oda":
                self._handle_telegram_command("run_ts", {})
            elif obj == "timbrature":
                self._handle_telegram_command("run_timbrature", {"period": "today"})

        elif action == "status":
            self._handle_telegram_status(chat_id)
        
        elif action == "restart":
            self._handle_telegram_command("restart_app", {})

    def _handle_telegram_command(self, command, params):
        if command == "run_pdl":
            self.navigate_to_panel("scarico_pdl")
            print_enabled = params.get("print", False)
            self.pdl_panel.print_check.setChecked(print_enabled)
            ready, msg = self.pdl_panel.validate_ready()
            if not ready:
                self.telegram.send_message_sync(f"⚠️ Impossibile avviare Scarico PDL.\nMotivo: {msg}\nUsa '➕ Inserisci PDL' per aggiungere dati.")
                return
            self.pdl_panel.start_btn.click()
            self.telegram.send_message_sync(f"✅ Comando ricevuto. Avvio Scarico PDL (Stampa={print_enabled})")
            
        elif command == "list_pdl":
            data = self.pdl_panel.data_table.get_data()
            if not data:
                self.telegram.send_message_sync("📋 **Lista PDL Vuota**")
            else:
                items = [str(row.get("numero_pdl", "")) for row in data]
                text = "📋 **Lista PDL Corrente:**\n" + "\n".join([f"• `{i}`" for i in items[:20]])
                if len(items) > 20: text += f"\n...ed altri {len(items)-20}"
                self.telegram.send_message_sync(text)

        elif command == "clear_pdl":
            self.pdl_panel.clear_rows_simple()
            self.telegram.send_message_sync("🗑️ Tabella PDL svuotata.")

        elif command == "run_ts":
            self.navigate_to_panel("scarico_ts")
            ready, msg = self.scarico_panel.validate_ready()
            if not ready:
                self.telegram.send_message_sync(f"⚠️ Impossibile avviare Scarico TS.\nMotivo: {msg}\nUsa '➕ Aggiungi OdA' per aggiungere dati.")
                return
            self.scarico_panel.start_btn.click()
            self.telegram.send_message_sync("✅ Comando ricevuto. Avvio Scarico Timesheet.")

        elif command == "list_ts":
            data = self.scarico_panel.data_table.get_data()
            if not data:
                self.telegram.send_message_sync("📋 **Lista OdA Vuota**")
            else:
                items = [str(row.get("numero_oda", "")) for row in data]
                text = "📋 **Lista OdA Corrente:**\n" + "\n".join([f"• `{i}`" for i in items[:20]])
                if len(items) > 20: text += f"\n...ed altri {len(items)-20}"
                self.telegram.send_message_sync(text)

        elif command == "clear_ts":
            self.scarico_panel.clear_rows_simple()
            self.telegram.send_message_sync("🗑️ Tabella OdA svuotata.")

        elif command == "run_carico":
            self.navigate_to_panel("carico_ts")
            ready, msg = self.carico_panel.validate_ready()
            if not ready:
                self.telegram.send_message_sync(f"⚠️ Impossibile avviare Carico TS.\nMotivo: {msg}")
                return
            self.carico_panel.start_btn.click()
            self.telegram.send_message_sync("✅ Comando ricevuto. Avvio Carico Timesheet.")

        elif command == "run_oda_details":
            self.navigate_to_panel("dettagli_oda")
            ready, msg = self.dettagli_panel.validate_ready()
            if not ready:
                self.telegram.send_message_sync(f"⚠️ Impossibile avviare Dettagli OdA.\nMotivo: {msg}")
                return
            self.dettagli_panel.start_btn.click()
            self.telegram.send_message_sync("✅ Comando ricevuto. Avvio Scarico Dettagli OdA.")

        elif command == "set_fornitore":
            fornitore = params.get("fornitore")
            if fornitore:
                config_manager.set_config_value("last_ts_fornitore", fornitore)
                # Forza aggiornamento UI se necessario (i pannelli ricaricano la config all'avvio bot)
                self.show_toast(f"Telegram: Fornitore impostato su {fornitore}")
                # Aggiorna anche Lyra se attiva
                if hasattr(self, 'lyra_panel'):
                    self.lyra_panel.fornitore_combo.setCurrentText(fornitore)

        elif command == "set_autopilot":
            enabled = params.get("enabled")
            time_val = params.get("time")
            
            if enabled is not None:
                config_manager.set_config_value("timbrature_autopilot_enabled", enabled)
                # Sincronizza UI panel
                self.timbrature_bot_panel.autopilot_check.setChecked(enabled)
                status = "ATTIVATO" if enabled else "DISATTIVATO"
                self.telegram.send_message_sync(f"✅ Autopilot {status} correttamente.")
            
            if time_val:
                config_manager.set_config_value("timbrature_autopilot_time", time_val)
                # Sincronizza UI panel
                from PyQt6.QtCore import QTime
                self.timbrature_bot_panel.time_edit.setTime(QTime.fromString(time_val, "HH:mm"))
                self.telegram.send_message_sync(f"✅ Orario Autopilot impostato alle: {time_val}")

        elif command == "restart_app":
            # Avvia avvio.bat in un nuovo processo e chiudi questo
            try:
                bat_path = os.path.abspath("avvio.bat")
                subprocess.Popen(["cmd.exe", "/c", "start", bat_path], shell=True)
                QApplication.quit()
            except Exception as e:
                self.telegram.send_message_sync(f"❌ Errore durante il riavvio: {e}")

        elif command == "test_connectivity":
            def run_test():
                urls = {
                    "Google": "https://www.google.com",
                    "Portale ISAB": "https://portale-fornitori.isab.com/",
                    "SafeWork": "https://safework.isab.com/"
                }
                report = "🔌 **Test Connettività**\n───────────────────\n"
                for name, url in urls.items():
                    try:
                        res = requests.get(url, timeout=10)
                        status = "✅ OK" if res.status_code < 400 else f"⚠️ {res.status_code}"
                        report += f"• {name}: {status}\n"
                    except:
                        report += f"• {name}: ❌ NON RAGGIUNGIBILE\n"
                
                self.telegram.send_message_sync(report)
            
            threading.Thread(target=run_test, daemon=True).start()

        elif command == "set_printer":
            printer_name = params.get("printer")
            if printer_name:
                config_manager.set_config_value("pdl_printer_name", printer_name)
                # Sincronizza UI panel se caricato
                if hasattr(self, 'pdl_panel'):
                    idx = self.pdl_panel.printer_combo.findText(printer_name)
                    if idx >= 0:
                        self.pdl_panel.printer_combo.setCurrentIndex(idx)
                
                self.show_toast(f"Telegram: Stampante impostata su {printer_name}")
                self.telegram.send_message_sync(f"✅ Stampante predefinita impostata su: `{printer_name}`")
        elif command == "run_timbrature":
            self.navigate_to_panel("timbrature")
            period = params.get("period", "yesterday")
            
            # Imposta le date nel pannello
            from PyQt6.QtCore import QDate
            target_date = QDate.currentDate()
            if period == "yesterday":
                target_date = target_date.addDays(-1)
            
            self.timbrature_bot_panel.date_da_edit.setDate(target_date)
            self.timbrature_bot_panel.date_a_edit.setDate(target_date)
            
            ready, msg = self.timbrature_bot_panel.validate_ready()
            if not ready:
                self.telegram.send_message_sync(f"⚠️ Impossibile avviare Timbrature.\nMotivo: {msg}")
                return
            self.timbrature_bot_panel.start_btn.click()
            self.telegram.send_message_sync(f"✅ Comando ricevuto. Avvio Scarico Timbrature ({period}).")
        elif command == "stop_all":
            panel = self._get_active_bot_panel()
            if panel and hasattr(panel, 'stop_btn') and panel.stop_btn.isEnabled():
                panel.stop_btn.click()
                self.telegram.send_message_sync("🛑 Stop inviato.")
            else:
                self.telegram.send_message_sync("ℹ️ Nessun processo attivo.")

    def _handle_telegram_data(self, data_type, items):
        """Gestisce l'inserimento di dati grezzi da Telegram con validazione e deduplicazione."""
        valid_items = []
        errors = []
        duplicates = 0
        
        if data_type == "pdl":
            panel = self.pdl_panel
            field_name = "numero_pdl"
            validator = InputValidator.validate_pdl
        else: # oda
            panel = self.scarico_panel
            field_name = "numero_oda"
            validator = InputValidator.validate_oda

        # 1. Recupera dati esistenti per controllo duplicati
        existing_data = []
        if hasattr(panel, 'data_table'):
            existing_data = [str(row.get(field_name, "")) for row in panel.data_table.get_data()]

        # 2. Validazione e Filtro
        for item in items:
            res = validator(item)
            if res.valid:
                val = res.sanitized_value
                if val in existing_data or val in valid_items:
                    duplicates += 1
                else:
                    valid_items.append(val)
            else:
                errors.append(f"❌ `{item}`: {res.error}")

        # 3. Applicazione
        if valid_items:
            new_rows = [{field_name: val} for val in valid_items]
            panel.add_rows_simple(new_rows)
            self.navigate_to_panel(panel.bot_id)
            self.show_toast(f"Telegram: Aggiunti {len(valid_items)} elementi")

        # 4. Feedback via Telegram
        feedback = []
        if valid_items:
            feedback.append(f"✅ **Aggiunti {len(valid_items)} elementi**")
        if duplicates > 0:
            feedback.append(f"ℹ️ **{duplicates} duplicati saltati**")
        if errors:
            feedback.append(f"⚠️ **Errori ({len(errors)}):**\n" + "\n".join(errors[:5]))
            if len(errors) > 5: feedback.append(f"...ed altri {len(errors)-5}")

        if not feedback:
            feedback = ["⚠️ Nessun dato valido inserito."]
            
        self.telegram.send_message_sync("\n".join(feedback))

    def _handle_telegram_status(self, chat_id):
        """Invia lo stato corrente al bot."""
        panel = self._get_active_bot_panel()
        if panel and hasattr(panel, 'get_current_status'):
            status, msg = panel.get_current_status()
            text = f"📊 **Stato Sistema**\n\nAttività: {panel.bot_name}\nStato: {status}\nDettaglio: {msg}"
        else:
            text = "📊 **Stato Sistema**\n\nIl sistema è in attesa (Idle)."
        
        self.telegram.send_message_sync(text)

    def _handle_telegram_screenshot(self, mode="app"):
        """Cattura lo screenshot (App o Intero Desktop) e lo invia a Telegram."""
        try:
            from PyQt6.QtCore import QBuffer, QIODevice, QRect
            from PyQt6.QtGui import QGuiApplication, QScreen
            
            if mode == "app":
                # Cattura solo la finestra dell'applicazione
                pixmap = self.grab()
                caption_text = "Solo App"
            else:
                # Cattura intero desktop (tutti i monitor)
                screens = QGuiApplication.screens()
                if not screens:
                    raise Exception("Nessun monitor rilevato")
                
                # Calcola l'area totale che copre tutti i monitor
                total_rect = QRect()
                for screen in screens:
                    total_rect = total_rect.united(screen.geometry())
                
                # Crea una pixmap gigante per contenere tutto
                combined_pixmap = QPixmap(total_rect.size())
                combined_pixmap.fill(Qt.GlobalColor.black)
                painter = QPainter(combined_pixmap)
                
                for screen in screens:
                    screen_pixmap = screen.grabWindow(0)
                    # Disegna lo screenshot del monitor nella posizione corretta
                    # traslando le coordinate relative al rettangolo totale
                    painter.drawPixmap(
                        screen.geometry().topLeft() - total_rect.topLeft(), 
                        screen_pixmap
                    )
                painter.end()
                pixmap = combined_pixmap
                caption_text = f"Desktop Completo ({len(screens)} monitor)"
            
            # Converti in bytes (PNG)
            buffer = QBuffer()
            buffer.open(QIODevice.OpenModeFlag.WriteOnly)
            pixmap.save(buffer, "PNG")
            photo_bytes = buffer.data().data()
            
            # Invia
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.telegram.send_photo_sync(
                photo_bytes, 
                caption=f"📸 **Screenshot: {caption_text}**\nAcquisito alle {timestamp}"
            )
        except Exception as e:
            self.telegram.send_message_sync(f"❌ Errore acquisizione screenshot: {e}")
            import traceback
            traceback.print_exc()

    def _forward_notification_to_telegram(self, notification):
        """Inoltra notifiche importanti a Telegram (tranne quelle generate da Telegram stesso)."""
        if notification.get("title") == "Telegram":
            return
            
        level = notification.get("level", "info")
        # Inoltriamo solo successi, errori e avvisi (evitiamo spam di info generiche)
        if level in ["success", "error", "warning"]:
            title = notification.get("title", "Notifica")
            msg = notification.get("message", "")
            icon = "✅" if level == "success" else "❌" if level == "error" else "⚠️"
            
            text = f"{icon} *{title}*\n{msg}"
            self.telegram.send_message_sync(text)

    def _handle_telegram_ai_query(self, chat_id, query):
        """Gestisce le domande poste tramite Telegram usando Lyra AI."""
        # Recupera API Key
        api_key = SecretsManager.get_gemini_api_key()
        
        if not api_key:
            self.telegram.send_message_sync("⚠️ AI Coach non configurato. Inserisci la Gemini API Key nelle impostazioni del PC.")
            return

        # Funzione di worker da eseguire in thread
        def run_ai_query():
            try:
                from src.core.lyra_client import LyraClient
                client = LyraClient(api_key=api_key)
                # Chiedi a Lyra (include automaticamente il contesto del database)
                response = client.ask(query)
                self.telegram.send_message_sync(f"🤖 **AI Coach (Lyra)**\n\n{response}")
            except Exception as e:
                import traceback
                err = traceback.format_exc()
                self.telegram.send_message_sync(f"❌ Errore AI:\n{err}")

        # Esegui in thread per non bloccare la GUI
        threading.Thread(target=run_ai_query, daemon=True).start()

    def _handle_telegram_photo(self, chat_id, photo_bytes, caption):
        """Gestisce le immagini inviate tramite Telegram (Rapportini)."""
        api_key = SecretsManager.get_gemini_api_key()
        
        if not api_key:
            self.telegram.send_message_sync("⚠️ AI Vision non configurata. Inserisci la Gemini API Key.")
            return

        self.telegram.send_message_sync("🔍 **Analisi Documento in corso...**\nSto leggendo i dati dal rapportino, attendi un istante.")

        def run_vision_query():
            try:
                import base64
                from src.core.lyra_client import LyraClient
                
                # Converti bytes in base64
                img_b64 = base64.b64encode(photo_bytes).decode('utf-8')
                
                client = LyraClient(api_key=api_key)
                # Chiedi a Lyra di estrarre i dati
                prompt = "Estrai integralmente tutti i dati da questo rapportino giornaliero. Restituisci ESCLUSIVAMENTE una tabella Markdown."
                if caption:
                    prompt += f"\nNote aggiuntive dell'utente: {caption}"
                
                response = client.ask(prompt, images=[img_b64])
                
                self.telegram.send_message_sync(f"📝 **Dati Estratti (Anteprima)**\n\n{response}\n\n_I dati sono stati estratti tramite AI. Controlla la correttezza prima dell'uso._")
            except Exception as e:
                import traceback
                err = traceback.format_exc()
                self.telegram.send_message_sync(f"❌ Errore AI Vision:\n{err}")

        threading.Thread(target=run_vision_query, daemon=True).start()

    def _setup_tray_icon(self):
        """Configura l'icona nella system tray."""
        self.tray_icon = QSystemTrayIcon(self)
        
        icon_path = get_app_icon_path()
        if icon_path:
            self.tray_icon.setIcon(QIcon(icon_path))
        
        # Tray Menu
        tray_menu = QMenu()
        show_action = QAction("🖥️ Mostra SyncroJob", self)
        show_action.triggered.connect(self.showMaximized)
        show_action.triggered.connect(self.activateWindow)
        tray_menu.addAction(show_action)
        
        tray_menu.addSeparator()
        
        def force_quit_app():
            self._force_quit = True
            QApplication.instance().quit()

        quit_action = QAction("❌ Esci", self)
        quit_action.triggered.connect(force_quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._handle_tray_activation)
        self.tray_icon.show()

    def _handle_tray_activation(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.showMaximized()
                self.activateWindow()

    def _check_updates(self):
        """Avvia il controllo aggiornamenti in background."""
        # Usa il nuovo sistema a banner invece del popup bloccante
        check_for_updates(parent=self, silent=True, callback=self._show_update_banner)
    
    def _show_update_banner(self, new_version, download_url, changelog):
        """Mostra un banner informativo per la nuova versione."""
        self.update_banner.setVisible(True)
        self.update_label.setText(f"🚀 Nuova versione disponibile: v{new_version}")
        self.update_label.setToolTip(f"Novità:\n{changelog}" if changelog else "Clicca per scaricare")
        
        # Memorizza URL per il click
        self._update_download_url = download_url
        
        # Notifica tray
        self.tray_icon.showMessage(
            "Aggiornamento Disponibile",
            f"È uscita la versione {new_version}. Clicca qui per scaricarla.",
            QSystemTrayIcon.MessageIcon.Information,
            5000
        )
    
    def _on_anomalies_found(self, count):
        """Gestisce le anomalie trovate da Lyra."""
        self.btn_lyra.set_badge(count)
        if count > 0:
            ToastManager.instance().show(f"⚠️ Lyra ha rilevato {count} anomalie", "warning")

    def show_background_notification(self, title: str, message: str, is_error: bool = False):
        """
        Mostra una notifica di sistema (Toast) se l'applicazione non è attiva (in background o minimizzata).
        """
        # Controlla se l'applicazione è in primo piano
        is_active = self.isActiveWindow() and not self.isMinimized()
        
        if not is_active:
            icon = QSystemTrayIcon.MessageIcon.Critical if is_error else QSystemTrayIcon.MessageIcon.Information
            self.tray_icon.showMessage(title, message, icon, 5000)
            
            # Flash Taskbar come avviso visivo aggiuntivo
            QApplication.alert(self, 0)

    def show_toast(self, message: str, duration: int = 3000):
        """Mostra una notifica toast (Wrapper for backward compatibility)."""
        ToastManager.instance().show(message, "info", duration)

    def _setup_shortcuts(self):
        """Configura le scorciatoie da tastiera globali."""
        # F5 - Aggiorna / Avvia
        self.shortcut_f5 = QShortcut(QKeySequence(Qt.Key.Key_F5), self)
        self.shortcut_f5.activated.connect(self._handle_f5)

        # Ctrl+F - Cerca
        self.shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_search.activated.connect(self._handle_ctrl_f)

        # Ctrl+S - Salva Impostazioni
        self.shortcut_save = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut_save.activated.connect(self._handle_ctrl_s)

    def _handle_f5(self):
        """Gestisce F5 in base alla vista corrente."""
        idx = self.page_stack.currentIndex()

        if idx == 0: # Dashboard
            self.dashboard_panel.refresh_data()
            self.show_toast("Dashboard aggiornata")
        # Database Page (Index 3)
        elif idx == 3:
            tab_idx = self.database_widget.currentIndex()
            if tab_idx == 0: # Timbrature
                self.timbrature_db_panel.refresh_data()
                self.show_toast("Dati aggiornati")
            elif tab_idx == 1: # Contabilità
                self.contabilita_panel.refresh_tabs()
                self.show_toast("Contabilità aggiornata (Vista)")
            elif tab_idx == 2: # Scarico Ore
                self.scarico_ore_panel._start_update()

    def _handle_ctrl_f(self):
        """Gestisce Ctrl+F per il focus sulla ricerca."""
        idx = self.page_stack.currentIndex()

        # Database Page
        if idx == 3:
            tab_idx = self.database_widget.currentIndex()
            if tab_idx == 0: # Timbrature
                self.timbrature_db_panel.search_input.setFocus()
                self.timbrature_db_panel.search_input.selectAll()
            elif tab_idx == 1: # Contabilità
                if self.contabilita_panel.search_input.isVisible():
                    self.contabilita_panel.search_input.setFocus()
                    self.contabilita_panel.search_input.selectAll()
            elif tab_idx == 2: # Scarico Ore
                self.scarico_ore_panel.search_input.setFocus()
                self.scarico_ore_panel.search_input.selectAll()

    def _handle_ctrl_s(self):
        """Gestisce Ctrl+S per salvare le impostazioni."""
        if self.page_stack.currentIndex() == 4:
            self.settings_panel.save_btn.click()

    def _setup_ui(self):
        """Configura l'interfaccia."""
        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Global Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar") # Assegna objectName
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.status_bar.addPermanentWidget(self.progress_bar)

        # Widget centrale
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principale orizzontale
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # === SIDEBAR ===
        sidebar = QFrame()
        sidebar.setObjectName("sidebarFrame") # Assegna objectName
        sidebar.setFixedWidth(240)
        # FORCE STYLE TO ENSURE TEXT VISIBILITY
        sidebar.setStyleSheet("""
            QFrame#sidebarFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-right: 1px solid rgba(0,0,0,0.1);
            }
            QLabel { color: white; background: transparent; }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)
        
        # Logo/Titolo
        logo_label = QLabel("🚀 SyncroJob")
        logo_label.setObjectName("logoLabel") # Assegna objectName
        sidebar_layout.addWidget(logo_label)
        
        subtitle = QLabel("Work & Sync Manager")
        subtitle.setObjectName("subtitleLabel") # Assegna objectName
        sidebar_layout.addWidget(subtitle)
        
        # Separatore
        separator = QFrame()
        separator.setObjectName("sidebarSeparator") # Assegna objectName
        separator.setFrameShape(QFrame.Shape.HLine)
        sidebar_layout.addWidget(separator)
        
        sidebar_layout.addSpacing(15)
        
        # Pulsanti navigazione
        self.btn_home = SidebarButton("Home", "🏠")
        self.btn_home.setChecked(True)
        sidebar_layout.addWidget(self.btn_home)

        self.btn_automazioni = SidebarButton("Automazioni", "🤖")
        sidebar_layout.addWidget(self.btn_automazioni)

        self.btn_database = SidebarButton("Database", "🗄️")
        sidebar_layout.addWidget(self.btn_database)
        
        sidebar_layout.addStretch()

        self.btn_lyra = SidebarButton("Lyra AI", "✨")
        sidebar_layout.addWidget(self.btn_lyra)

        self.btn_notifications = SidebarButton("Notifiche", "🔔")
        sidebar_layout.addWidget(self.btn_notifications)

        self.btn_help = SidebarButton("Guida", "❓")
        sidebar_layout.addWidget(self.btn_help)

        sidebar_layout.addSpacing(10)

        # License Info
        license_info = get_license_info()
        if license_info:
            client = license_info.get("Cliente", "N/D")
            expiry = license_info.get("Scadenza Licenza", "N/D")

            # Get last login from config
            config = config_manager.load_config()
            last_login = config.get("last_login_date", "N/D")

            # Update last login date to NOW for next time
            now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
            config_manager.set_config_value("last_login_date", now_str)

            license_text = f"Licenza: {client}\nScadenza: {expiry}\nUltimo accesso: {last_login}"
        else:
            license_text = "Licenza non trovata"

        license_label = QLabel(license_text)
        license_label.setObjectName("licenseLabel") # Assegna objectName
        license_label.setWordWrap(True)
        sidebar_layout.addWidget(license_label)
        
        # Separatore
        separator2 = QFrame()
        separator2.setObjectName("sidebarSeparator") # Assegna objectName
        separator2.setFrameShape(QFrame.Shape.HLine)
        sidebar_layout.addWidget(separator2)
        
        sidebar_layout.addSpacing(10)
        
        # Impostazioni
        self.btn_settings = SidebarButton("Impostazioni", "⚙️")
        sidebar_layout.addWidget(self.btn_settings)
        
        # Versione
        from src.core.version import __version__
        version_label = QLabel(f"v{__version__}")
        version_label.setObjectName("versionLabel") # Assegna objectName
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(version_label)
        
        main_layout.addWidget(sidebar)
        
        # === CONTENT AREA ===
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # --- UPDATE BANNER (Hidden by default) ---
        self.update_banner = QFrame()
        self.update_banner.setObjectName("updateBanner")
        self.update_banner.setVisible(False)
        banner_layout = QHBoxLayout(self.update_banner)
        banner_layout.setContentsMargins(15, 10, 15, 10)
        
        self.update_label = QLabel("🚀 Nuova versione disponibile!")
        banner_layout.addWidget(self.update_label)
        
        banner_layout.addStretch()
        
        self.download_btn = QPushButton("Scarica e Installa")
        self.download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.download_btn.clicked.connect(self._on_download_update_clicked)
        banner_layout.addWidget(self.download_btn)
        
        content_layout.addWidget(self.update_banner)
        
        # --- GLOBAL SEARCH BAR ---
        search_container = QHBoxLayout()
        search_container.setContentsMargins(0, 0, 0, 10)
        
        self.global_search = QLineEdit()
        self.global_search.setObjectName("globalSearchInput") # Assegna objectName
        self.global_search.setPlaceholderText("🔍 Ricerca Universale (OdA, Dipendenti, Log...) - Ctrl+F")
        self.global_search.setMinimumHeight(40)
        # Connect search logic
        self.global_search.returnPressed.connect(self._perform_global_search)
        
        search_container.addWidget(self.global_search)
        content_layout.addLayout(search_container)
        
        # Stack per le pagine principali (Automazioni, Database, Settings)
        self.page_stack = QStackedWidget()
        
        # Crea i pannelli individuali
        self.dashboard_panel = DashboardPanel()
        self.scarico_panel = ScaricaTSPanel()
        self.carico_panel = CaricoTSPanel()
        self.dettagli_panel = DettagliOdAPanel()
        self.pdl_panel = ScaricoPDLPanel() # NEW
        self.pdl_panel.bot_results_ready.connect(self._handle_bot_results)
        self.timbrature_bot_panel = TimbratureBotPanel()
        self.timbrature_db_panel = TimbratureDBPanel()
        self.contabilita_panel = ContabilitaPanel()
        self.scarico_ore_panel = ScaricoOrePanel() # NEW: Scarico Ore Panel
        self.settings_panel = SettingsPanel()
        self.help_panel = HelpPanel()
        self.lyra_panel = LyraPanel()
        self.notifications_panel = NotificationsPanel()
        
        # Collega il segnale di update dal bot al database
        self.timbrature_bot_panel.data_updated.connect(self.timbrature_db_panel.refresh_data)

        # --- Page 1: Automazioni (Main Groups) ---
        self.automazioni_widget = QTabWidget()
        
        # Global Status Card (Corner Widget)
        self.global_status_card = StatusCard("Stato Attività")
        self.global_status_card.setMinimumWidth(350)
        self.global_status_card.setMaximumHeight(40) # Ensure it fits in tab bar
        self.automazioni_widget.setCornerWidget(self.global_status_card, Qt.Corner.TopRightCorner)
        
        # Group 1: Portale Fornitori
        self.tab_fornitori = QTabWidget()
        self.tab_fornitori.addTab(self.dettagli_panel, "📋 Dettagli OdA")
        self.tab_fornitori.addTab(self.scarico_panel, "📥 Scarico TS")
        self.tab_fornitori.addTab(self.timbrature_bot_panel, "⏱️ Timbrature")
        self.tab_fornitori.addTab(self.carico_panel, "📤 Carico TS")
        
        # Group 2: SafeWork
        self.tab_safework = QTabWidget()
        self.tab_safework.addTab(self.pdl_panel, "🛡️ Scarico PDL")
        
        self.automazioni_widget.addTab(self.tab_fornitori, "Portale Fornitori")
        self.automazioni_widget.addTab(self.tab_safework, "SafeWork")

        # Connect signals for Global Status Update
        self.automazioni_widget.currentChanged.connect(self._update_global_status)
        self.tab_fornitori.currentChanged.connect(self._update_global_status)
        self.tab_safework.currentChanged.connect(self._update_global_status)
        
        # Connect panel status changes
        for panel in [self.dettagli_panel, self.scarico_panel, self.timbrature_bot_panel, 
                      self.carico_panel, self.pdl_panel]:
            if hasattr(panel, 'status_changed'):
                panel.status_changed.connect(self._on_panel_status_changed)

        # --- Page 3: Database (Tab Widget) ---
        self.database_widget = QTabWidget()
        self.database_widget.addTab(self.timbrature_db_panel, "Timbrature Isab")
        self.database_widget.addTab(self.contabilita_panel, "Strumentale")
        self.database_widget.addTab(self.scarico_ore_panel, "DataEase") # Renamed from "Scarico Ore Cantiere"

        # Aggiungi le pagine allo stack
        # 0: Dashboard
        # 1: Automazioni
        # 2: Lyra
        # 3: Database
        # 4: Settings
        # 5: Help
        # 6: Notifications
        self.page_stack.addWidget(self.dashboard_panel)    # Index 0
        self.page_stack.addWidget(self.automazioni_widget) # Index 1
        self.page_stack.addWidget(self.lyra_panel)         # Index 2
        self.page_stack.addWidget(self.database_widget)    # Index 3
        self.page_stack.addWidget(self.settings_panel)     # Index 4
        self.page_stack.addWidget(self.help_panel)         # Index 5
        self.page_stack.addWidget(self.notifications_panel) # Index 6
        
        content_layout.addWidget(self.page_stack)
        
        main_layout.addWidget(content_area)
        
        # Lista pulsanti per gestione esclusiva
        self.nav_buttons = [
            self.btn_home,
            self.btn_automazioni,
            self.btn_lyra,
            self.btn_database,
            self.btn_settings,
            self.btn_help,
            self.btn_notifications
        ]
    
    def _perform_global_search(self):
        """Esegue la ricerca globale estesa su tutti i moduli."""
        query = self.global_search.text().strip()
        if not query or len(query) < 2: return

        results_menu = QMenu(self)
        results_menu.setStyleSheet("""
            QMenu { background-color: white; border: 1px solid #dee2e6; padding: 5px; min-width: 450px; }
            QMenu::item { padding: 8px 25px; font-size: 13px; }
            QMenu::item:selected { background-color: #0d6efd; color: white; }
            QMenu::separator { height: 1px; background: #e9ecef; margin: 5px 0; }
        """)

        found_count = 0

        # --- 1. Contabilità Strumentale (OdA) ---
        try:
            from src.core.contabilita_manager import ContabilitaManager
            oda_matches = ContabilitaManager.search_oda(query)
            if oda_matches:
                results_menu.addAction("📊 CONTABILITÀ STRUMENTALE (OdA):").setEnabled(False)
                for oda in oda_matches[:20]:
                    text = f"OdA {oda['codice_oda']} - {oda['descrizione'][:50]}..." # Increased trunc limit
                    action = results_menu.addAction(text)
                    action.triggered.connect(lambda _, o=oda['codice_oda']: self._navigate_to_oda(o))
                    found_count += 1
                results_menu.addSeparator()
        except: pass

        # --- 2. Contabilità Estesa (Giornaliere, Cantiere, Certificati) ---
        try:
            ext_matches = ContabilitaManager.search_extended(query)
            
            # Giornaliere
            if ext_matches.get("GIORNALIERE"):
                results_menu.addAction("📂 GIORNALIERE:").setEnabled(False)
                for g in ext_matches["GIORNALIERE"][:20]:
                    text = f"{g['data']} - {g['personale']} - {g['descrizione'][:40]}..."
                    action = results_menu.addAction(text)
                    action.triggered.connect(lambda _, q=query: self._navigate_to_extended(1, q)) # Tab 1 = Giornaliere
                    found_count += 1
                results_menu.addSeparator()

            # Cantiere (Scarico Ore)
            if ext_matches.get("CANTIERE"):
                results_menu.addAction("🏗️ CANTIERE (Scarico Ore):").setEnabled(False)
                for c in ext_matches["CANTIERE"][:20]:
                    text = f"{c['data']} - {c['personale']} - {c['commessa']}"
                    action = results_menu.addAction(text)
                    action.triggered.connect(lambda _, q=query: self._navigate_to_dataease(q))
                    found_count += 1
                results_menu.addSeparator()

            # Certificati
            if ext_matches.get("CERTIFICATI"):
                results_menu.addAction("📜 CERTIFICATI:").setEnabled(False)
                for c in ext_matches["CERTIFICATI"][:20]:
                    text = f"{c['matricola']} - {c['modello']} ({c['costruttore']})"
                    action = results_menu.addAction(text)
                    action.triggered.connect(lambda _, q=query: self._navigate_to_extended(3, q)) # Tab 3 = Certificati
                    found_count += 1
                results_menu.addSeparator()

        except: pass

        # --- 3. Dipendenti (Timbrature) ---
        try:
            emp_matches = TimbratureStorage().search_employees(query)
            if emp_matches:
                results_menu.addAction("👥 DIPENDENTI:").setEnabled(False)
                for emp in emp_matches[:20]:
                    text = f"{emp['cognome']} {emp['nome']}"
                    action = results_menu.addAction(text)
                    # Navigate to Timbrature DB and filter
                    action.triggered.connect(lambda _, q=text: self._navigate_to_timbrature(q))
                    found_count += 1
                results_menu.addSeparator()
        except: pass

        # --- 4. Audit Log ---
        try:
            from src.core.audit_manager import AuditManager
            audit_logs = AuditManager().get_logs(limit=100)
            matches = [l for l in audit_logs if query.lower() in str(l['action']).lower() or query.lower() in str(l['entity']).lower()]
            if matches:
                results_menu.addAction("🛡️ AUDIT LOG:").setEnabled(False)
                for log in matches[:3]:
                    action = results_menu.addAction(f"{log['action']} - {log['entity']}")
                    action.triggered.connect(lambda: self._navigate_to(6))
                    found_count += 1
        except: pass

        if found_count == 0:
            results_menu.addAction("❌ Nessun risultato trovato").setEnabled(False)

        pos = self.global_search.mapToGlobal(QPoint(0, self.global_search.height()))
        results_menu.exec(pos)

    def _navigate_to_extended(self, tab_idx, query):
        """Naviga a un tab specifico di Contabilità e imposta il filtro."""
        self._navigate_to(3) # Database
        self.database_widget.setCurrentIndex(1) # Contabilità
        self.contabilita_panel.main_tabs.setCurrentIndex(tab_idx)
        self.contabilita_panel.set_search_query(query)

    def _navigate_to_dataease(self, query):
        """Naviga a Scarico Ore (DataEase)."""
        self._navigate_to(3)
        self.database_widget.setCurrentIndex(2) # DataEase
        self.scarico_ore_panel.search_input.setText(query)

    def _navigate_to_timbrature(self, query):
        """Naviga a Timbrature DB."""
        self._navigate_to(3)
        self.database_widget.setCurrentIndex(0) # Timbrature
        self.timbrature_db_panel.search_input.setText(query)

    def _navigate_to_oda(self, oda_code):
        """Naviga al pannello contabilità e filtra per OdA."""
        self._navigate_to(3) # Database
        self.database_widget.setCurrentIndex(1) # Contabilità
        self.contabilita_panel.set_search_query(oda_code)

    def _get_active_bot_panel(self):
        """Recupera il pannello bot attualmente visibile."""
        main_idx = self.automazioni_widget.currentIndex()
        if main_idx == 0: # Portale Fornitori
            return self.tab_fornitori.currentWidget()
        elif main_idx == 1: # SafeWork
            return self.tab_safework.currentWidget()
        return None

    def _update_global_status(self):
        """Aggiorna la card di stato globale in base al pannello attivo."""
        panel = self._get_active_bot_panel()
        if panel and hasattr(panel, 'get_current_status'):
            status, message = panel.get_current_status()
            self.global_status_card.setStatus(status, message)
            
            # Change Global Status Card Title based on Panel Name?
            # User request: "Stato Attività" title constant.
            # But maybe we want to know WHICH activity.
            # "Stato Attività" is generic enough.
            # self.global_status_card._title_label.setText(f"Stato: {panel.bot_name}") 
            # Let's keep "Stato Attività" as per request.

    def _on_panel_status_changed(self, status, message):
        """Callback quando un pannello cambia stato."""
        sender = self.sender()
        active_panel = self._get_active_bot_panel()
        
        # Aggiorna solo se il segnale arriva dal pannello attivo
        if sender == active_panel:
            self.global_status_card.setStatus(status, message)

    def _connect_signals(self):
        """Collega i segnali."""
        self.btn_home.clicked.connect(lambda: self._navigate_to(0))
        self.btn_automazioni.clicked.connect(lambda: self._navigate_to(1))
        self.btn_lyra.clicked.connect(lambda: self._navigate_to(2))
        self.btn_database.clicked.connect(lambda: self._navigate_to(3))
        self.btn_settings.clicked.connect(lambda: self._navigate_to(4))
        self.btn_help.clicked.connect(lambda: self._navigate_to(5))
        self.btn_notifications.clicked.connect(lambda: self._navigate_to(6))

        # Notification Badge
        NotificationManager.instance().unread_count_changed.connect(self.btn_notifications.set_badge)
        # Init badge
        self.btn_notifications.set_badge(NotificationManager.instance().get_unread_count())

        # Aggiornamento live impostazioni
        self.settings_panel.settings_saved.connect(self._on_settings_saved)
        self.settings_panel.request_help_section.connect(self._on_help_requested)

    def _on_help_requested(self, section_title):
        """Gestisce la richiesta di apertura di una sezione specifica della guida."""
        self._navigate_to(5) # Index della pagina Help
        self.help_panel.open_section(section_title)

    def _on_settings_saved(self):
        """Aggiorna i pannelli quando le impostazioni vengono salvate."""
        self.scarico_panel.refresh_fornitori()
        self.dettagli_panel.refresh_fornitori()
        self.timbrature_bot_panel.refresh_fornitori()
        
        # Riavvia il servizio Telegram per applicare eventuali nuovi token
        self.telegram.start_service()

        # Feedback Toast
        ToastManager.instance().show("Impostazioni salvate con successo!", "success")
    
    def _navigate_to(self, index: int):
        """
        Naviga alla pagina specificata.
        
        Controlla se ci sono modifiche non salvate nelle impostazioni
        prima di cambiare pagina.
        """
        # Se stiamo già sulla pagina richiesta, non fare nulla
        if index == self._current_page_index:
            # Assicura che il pulsante sia checked
            self.nav_buttons[index].setChecked(True)
            return
        
        # Se stiamo lasciando la pagina delle impostazioni, controlla le modifiche
        if self._current_page_index == 4:  # Settings page is now index 4
            if self.settings_panel.has_unsaved_changes():
                can_proceed = self.settings_panel.prompt_save_if_needed()
                if not can_proceed:
                    # L'utente ha annullato - rimani sulla pagina corrente
                    self.nav_buttons[4].setChecked(True)
                    return
        
        # Procedi con la navigazione
        self._current_page_index = index
        self.page_stack.setCurrentIndex(index)
        
        # Aggiorna stato pulsanti
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
        
        # Se arriviamo su Automazioni (Index 1), potremmo voler aggiornare i fornitori
        if index == 1:
            self.scarico_panel.refresh_fornitori()

    def _check_and_start_contabilita_update(self):
        """Controlla la configurazione e avvia l'update contabilità se abilitato."""
        config = config_manager.load_config()
        if config.get("enable_auto_update_contabilita", False):
            self.contabilita_panel.start_import_process()
    
    def show_settings(self):
        """Metodo pubblico per navigare alle impostazioni."""
        self._navigate_to(4)

    def navigate_to_panel(self, panel_key: str):
        """
        Naviga a un pannello specifico (usato dalla Dashboard).
        Keys: 'dettagli_oda', 'scarico_ts', 'timbrature', 'carico_ts'
              'db_timbrature', 'db_strumentale', 'db_dataease'
        """
        # --- Automazioni (Index 1) ---
        # Map: key -> (MainTab Index, SubTab Index)
        # MainTab 0: Portale Fornitori
        # MainTab 1: SafeWork
        
        bot_map = {
            "dettagli_oda": (0, 0),
            "scarico_ts": (0, 1),
            "timbrature": (0, 2),
            "carico_ts": (0, 3),
            "scarico_pdl": (1, 0)
        }

        if panel_key in bot_map:
            main_idx, sub_idx = bot_map[panel_key]
            self._navigate_to(1)
            self.automazioni_widget.setCurrentIndex(main_idx)
            if main_idx == 0:
                self.tab_fornitori.setCurrentIndex(sub_idx)
            elif main_idx == 1:
                self.tab_safework.setCurrentIndex(sub_idx)
            return

        # --- Database (Index 3) ---
        db_map = {
            "db_timbrature": 0,
            "db_strumentale": 1,
            "db_dataease": 2
        }

        if panel_key in db_map:
            self._navigate_to(3)
            self.database_widget.setCurrentIndex(db_map[panel_key])
            return

    def analyze_with_lyra(self, context_text: str):
        """Passa alla vista Lyra e analizza il contesto fornito."""
        self._navigate_to(2) # Switch to Lyra
        self.lyra_panel.ask_lyra("Analizza questi dati e dimmi se ci sono anomalie o punti di attenzione.", context_text)
    
    def _on_download_update_clicked(self):
        """Gestisce il click sul pulsante scarica del banner."""
        if hasattr(self, '_update_download_url') and self._update_download_url:
            import webbrowser
            webbrowser.open(self._update_download_url)
            self.update_banner.setVisible(False)
            ToastManager.instance().show("Download avviato nel browser", "success")

    def closeEvent(self, event):
        """Gestisce la chiusura della finestra: minimizza nella tray se non è force_quit."""
        if self._force_quit:
            # Ferma servizi in background
            self.telegram.stop_service()
            
            # Auto Backup
            config = config_manager.load_config()
            if config.get("auto_backup", True):
                BackupManager.create_backup()

            # Controlla modifiche non salvate nelle impostazioni
            if self.settings_panel.has_unsaved_changes():
                can_close = self.settings_panel.prompt_save_if_needed()
                if not can_close:
                    event.ignore()
                    return
            
            event.accept()
            return

        # Altrimenti minimizza nella tray
        if self.isVisible():
            self.hide()
            
            # Mostra messaggio solo la prima volta
            config = config_manager.load_config()
            if not config.get("tray_hint_shown", False):
                self.tray_icon.showMessage(
                    "SyncroJob è ancora attivo",
                    "L'applicazione continua a lavorare in background.\nUsa il tasto destro sull'icona per chiudere definitivamente.",
                    QSystemTrayIcon.MessageIcon.Information,
                    5000
                )
                config_manager.set_config_value("tray_hint_shown", True)
            
            event.ignore()

    # --- Drag & Drop ---
    def dragEnterEvent(self, event):
        """Accetta file Excel trascinati."""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().endswith(('.xlsx', '.xls')):
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Gestisce il drop del file."""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            file_path = urls[0].toLocalFile()

            lower_path = file_path.lower()
            if "timbrature" in lower_path:
                self._import_timbrature(file_path)
            elif "contabilita" in lower_path or "consuntivo" in lower_path:
                self._import_contabilita(file_path)
            else:
                ToastManager.instance().show("Tipo file non riconosciuto. Rinominare con 'Timbrature' o 'Contabilita'.", "warning")

    def _import_timbrature(self, path):
        # Usa il metodo statico del bot timbrature
        try:
            from src.bots.portale_fornitori.timbrature.bot import TimbratureBot

            db_path = config_manager.CONFIG_DIR / "data" / "timbrature_Isab.db"
            success = TimbratureBot.import_to_db_static(path, db_path, lambda x: None)
            if success:
                self.timbrature_db_panel.refresh_data()
                ToastManager.instance().show("Timbrature importate con successo!", "success")
            else:
                ToastManager.instance().show("Errore importazione Timbrature.", "error")
        except Exception as e:
            ToastManager.instance().show(f"Errore: {e}", "error")

    def _import_contabilita(self, path):
        # Usa il manager contabilità
        try:
            from src.core.contabilita_manager import ContabilitaManager
            success, msg = ContabilitaManager.import_data_from_excel(path)
            if success:
                self.contabilita_panel.refresh_tabs()
                ToastManager.instance().show("Contabilità importata con successo!", "success")
            else:
                ToastManager.instance().show(f"Errore: {msg}", "error")
        except Exception as e:
            ToastManager.instance().show(f"Errore: {e}", "error")


def create_splash_screen() -> QSplashScreen:
    """Crea e restituisce una splash screen."""
    # Crea un pixmap per la splash
    splash_pixmap = QPixmap(400, 250)
    splash_pixmap.fill(QColor("#667eea"))
    
    painter = QPainter(splash_pixmap)
    painter.setPen(QColor("white"))
    
    # Titolo
    font_title = QFont("Arial", 28, QFont.Weight.Bold)
    painter.setFont(font_title)
    painter.drawText(splash_pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "🤖 Bot TS")
    
    # Sottotitolo
    font_sub = QFont("Arial", 12)
    painter.setFont(font_sub)
    painter.setPen(QColor(255, 255, 255, 180))
    sub_rect = splash_pixmap.rect()
    sub_rect.setTop(sub_rect.center().y() + 30)
    painter.drawText(sub_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, 
                    "ISAB Timesheet Manager\nCaricamento...")
    
    painter.end()
    
    splash = QSplashScreen(splash_pixmap)
    splash.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
    
    splash.show() # Ensure it's shown if created
    return splash
