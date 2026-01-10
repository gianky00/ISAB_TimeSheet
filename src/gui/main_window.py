"""
Bot TS - Main Window
Finestra principale dell'applicazione SyncroJob.
Implementa Lazy Loading dei pannelli per prestazioni ottimali.
"""

from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QStackedWidget,
    QStatusBar,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.backup_manager import BackupManager
from src.core.lyra_sentinel import LyraSentinel
from src.core.notification_manager import NotificationManager
from src.core.telegram_bridge import TelegramUIBridge
from src.core.telegram_manager import TelegramService
from src.gui.controllers.bot_controller import BotController
from src.gui.controllers.navigation_controller import NavigationController
from src.gui.controllers.search_controller import SearchController
from src.gui.controllers.service_controller import ServiceController
from src.gui.controllers.tray_controller import TrayController
from src.gui.styles import apply_theme
from src.gui.widgets.sidebar_widget import SidebarWidget
from src.gui.widgets.toast import ToastManager
from src.gui.widgets.update_banner import UpdateBanner


class MainWindow(QMainWindow):
    """Finestra principale dell'applicazione SyncroJob."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SyncroJob")
        self.setMinimumSize(1200, 800)

        # Configurazione Stili
        self._load_styles()
        apply_theme(QApplication.instance(), "light")
        self.setAcceptDrops(True)

        self._current_page_index = -1
        self._force_quit = False

        # --- SERVIZI ---
        self.sentinel = LyraSentinel()
        self.telegram = TelegramService()
        self.telegram_bridge = TelegramUIBridge(self)
        self.telegram_bridge.setup_connections()

        # --- CONTROLLERS ---
        self.tray_controller = TrayController(self)
        self.search_controller = SearchController(self)
        self.navigation_controller = NavigationController(self)
        self.bot_controller = BotController(self, self.telegram)
        self.service_controller = ServiceController(self, self.telegram, self.sentinel)

        # --- UI SETUP ---
        self._setup_ui()
        self._connect_signals()
        self._setup_shortcuts()

        # Avvio servizi
        self.service_controller.start_all()

        # Navigazione iniziale (Dashboard)
        self.navigation_controller.navigate_to(0)

        # Avvio automatico importazione contabilità se abilitato
        QTimer.singleShot(2000, self._check_and_start_contabilita_update)

        # EAGER LOADING: Pre-carica tutti i pannelli per evitare lag durante l'uso
        QTimer.singleShot(100, self._preload_all_panels)

<<<<<<< HEAD
        # === AUTOPILOT TIMER ===
        self.last_autopilot_trigger = ""
        self.autopilot_timer = QTimer(self)
        self.autopilot_timer.timeout.connect(self._check_autopilot)
        self.autopilot_timer.start(10000) # Check ogni 10 secondi

    def _check_autopilot(self):
        """Controlla se è l'ora di eseguire l'Autopilot Timbrature."""
        config = config_manager.load_config()
        
        if not config.get("timbrature_autopilot_enabled", False):
            return

        target_time_str = config.get("timbrature_autopilot_time", "09:00")
        current_time_str = datetime.now().strftime("%H:%M")

        # Evita esecuzioni multiple nello stesso minuto
        if current_time_str == self.last_autopilot_trigger:
            return

        if current_time_str == target_time_str:
            self.last_autopilot_trigger = current_time_str
            
            # 1. Verifica stato bot (non deve essere già in esecuzione)
            status, _ = self.timbrature_bot_panel.get_current_status()
            if status == "RUNNING":
                print(f"[AUTOPILOT] Skipped {current_time_str}: Bot già in esecuzione.")
                return

            # 2. Pre-Validazione Parametri
            ready, msg = self.timbrature_bot_panel.validate_ready()
            if not ready:
                self.show_toast(f"Autopilot Errore: {msg}", "error")
                return

            # 3. Avvio
            self.show_toast(f"🤖 Autopilot: Avvio Timbrature...", "info")
            
            # Naviga al pannello per mostrare l'attività
            self.navigate_to_panel("timbrature")

            # Imposta modalità silenziosa per Telegram (solo per questa esecuzione)
            self.timbrature_bot_panel.silent_telegram = True

            # Ritarda l'avvio effettivo per permettere alla UI di aggiornarsi (Toast + Tab Switch)
            def trigger_start():
                btn = self.timbrature_bot_panel.start_btn
                print(f"[AUTOPILOT] Tentativo click Avvia. Abilitato? {btn.isEnabled()}")
                if btn.isEnabled():
                    btn.click()
                else:
                    print("[AUTOPILOT] Errore: Pulsante Avvia disabilitato (Bot già in corso?)")
            
            QTimer.singleShot(500, trigger_start)

    def _handle_bot_results(self, bot_id, results):
        """Gestisce i risultati prodotti dai bot (es. file scaricati) e li invia a Telegram."""
        if bot_id == "scarico_pdl":
            for file_path in results:
                if os.path.exists(file_path):
                    self.telegram.send_document_sync(
                        file_path, caption=f"📄 **PDL Scaricato**\nFile: `{os.path.basename(file_path)}`"
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
                    if res.valid:
                        valid_pdl.append({"numero_pdl": res.sanitized_value})

                if valid_pdl:
                    self.pdl_panel.add_rows_simple(valid_pdl)
                    self.show_toast(f"Telegram: aggiunti {len(valid_pdl)} PDL via AI")

            elif obj == "oda":
                valid_oda = []
                for i in items:
                    res = InputValidator.validate_oda(i)
                    if res.valid:
                        valid_oda.append({"numero_oda": res.sanitized_value})

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
                keyboard = [
                    [InlineKeyboardButton(f"🖨️ {p[:30]}", callback_data=f"sel_print_run_{p[:25]}")]
                    for p in printers[:6]
                ]
                self.telegram.send_message_sync(
                    "✅ Ho aggiunto i PDL. **Quale stampante utilizzo?**",
                    # Nota: TelegramService gestisce la tastiera se passata? No, devo aggiungerlo o farlo via callback
                )
                # Fallback: se non posso mandare la tastiera da qui facilmente, emetto un comando di richiesta stampante
                self.telegram.send_message_sync(
                    "⚠️ Seleziona la stampante dal menu PDL -> Avvia (Stampa ON) oppure usa i bottoni nel menu Impostazioni."
                )
                # Implementazione più pulita: chiamiamo un metodo interno di telegram
                asyncio.run_coroutine_threadsafe(
                    self.telegram.app.bot.send_message(
                        chat_id=chat_id,
                        text=f"✅ PDL {', '.join(items)} pronti. **Quale stampante uso?**",
                        reply_markup=InlineKeyboardMarkup(keyboard),
                    ),
                    self.telegram.loop,
                )

        elif action == "download":
            if obj == "pdl":
                # Chiedi se vuole stampare
                from telegram import InlineKeyboardButton, InlineKeyboardMarkup

                keyboard = [
                    [
                        InlineKeyboardButton("✅ Sì, stampa", callback_data="confirm_print_yes"),
                        InlineKeyboardButton("❌ No, solo download", callback_data="confirm_print_no"),
                    ]
                ]
                asyncio.run_coroutine_threadsafe(
                    self.telegram.app.bot.send_message(
                        chat_id=chat_id,
                        text="Aggiunti PDL. **Vuoi che li stampi anche?**",
                        reply_markup=InlineKeyboardMarkup(keyboard),
                    ),
                    self.telegram.loop,
                )
            elif obj == "oda":
                self._handle_telegram_command("run_ts", {})
            elif obj == "timbrature":
                self._handle_telegram_command("run_timbrature", {"period": "today"})

        elif action == "status":
            self._handle_telegram_status(chat_id)

        elif action == "restart":
            self._handle_telegram_command("restart_app", {})

    def _generate_pdf_from_html(self, html_content: str, output_path: str):
        """Genera un PDF da contenuto HTML."""
        doc = QTextDocument()
        
        # Aggiungi stili CSS globali per garantire leggibilità
        header_style = """
        <style>
            body { font-family: Arial, sans-serif; font-size: 18pt; }
            h2 { font-size: 30pt; color: #333; }
            h3 { font-size: 24pt; color: #0d6efd; margin-top: 20px; }
            p { font-size: 18pt; color: #555; }
            table { width: 100%; border-collapse: collapse; margin-top: 15px; }
            th { background-color: #f2f2f2; color: #333; font-weight: bold; padding: 12px; font-size: 16pt; border: 1px solid #ddd; }
            td { padding: 10px; font-size: 16pt; border: 1px solid #ddd; color: #000; }
        </style>
        """
        doc.setHtml(header_style + html_content)

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(output_path)
        printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        printer.setPageOrientation(QPageLayout.Orientation.Landscape) # Landscape per tabelle larghe
        
        doc.print(printer)

    def _handle_telegram_command(self, command, params):
        if command == "search_db_pdf":
            db_type = params.get("db", "")
            query_text = params.get("query", "")
            chat_id = params.get("chat_id", "")
            year_filter = params.get("year")
            
            msg_text = f"🔍 Ricerca in corso in **{db_type.capitalize()}**"
            if year_filter:
                msg_text += f" ({year_filter})"
            msg_text += f" per: `{query_text}`..."
            
            self.telegram.send_message_sync(msg_text)
            
            try:
                # Logica Specifica per Database
                html_report = ""
                filename = f"report_{db_type}_{int(datetime.now().timestamp())}.pdf"
                temp_pdf = str(config_manager.CONFIG_DIR / "temp" / filename)
                
                # Assicura che la temp dir esista
                (config_manager.CONFIG_DIR / "temp").mkdir(exist_ok=True)

                if db_type == "timbrature":
                    # Cerca in Timbrature
                    rows = self.timbrature_db_panel.storage.get_timbrature_with_reparto(limit=500, filter_text=query_text)
                    
                    if not rows:
                        self.telegram.send_message_sync("❌ Nessun risultato trovato.")
                        return

                    # Costruisci HTML
                    html_report = f"""
                    <h2>Report Timbrature</h2>
                    <p><b>Filtro:</b> {query_text}<br><b>Data Generazione:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                    <table>
                        <thead>
                            <tr>
                                <th>Data</th>
                                <th>Ingresso</th>
                                <th>Uscita</th>
                                <th>Nominativo</th>
                                <th>Sito</th>
                            </tr>
                        </thead>
                        <tbody>
                    """
                    for r in rows:
                        full_name = f"{r[4]} {r[3]}"
                        html_report += f"""
                            <tr>
                                <td>{r[0]}</td>
                                <td>{r[1]}</td>
                                <td>{r[2]}</td>
                                <td>{full_name}</td>
                                <td>{r[6]}</td>
                            </tr>
                        """
                    html_report += "</tbody></table>"

                elif db_type == "strumentale":
                    from src.core.contabilita_manager import ContabilitaManager
                    
                    year_val = int(year_filter) if year_filter else None
                    matches = ContabilitaManager.search_extended(query_text, year=year_val, limit=500)
                    
                    if not matches or (not matches.get("GIORNALIERE") and not matches.get("CANTIERE")):
                        self.telegram.send_message_sync("❌ Nessun risultato trovato.")
                        return
                        
                    html_report = f"""
                    <h2>Report Contabilità {year_filter if year_filter else ''}</h2>
                    <p><b>Filtro:</b> {query_text}<br><b>Data Generazione:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                    """
                    
                    if matches.get("GIORNALIERE"):
                        html_report += "<h3>Giornaliere</h3><table><thead><tr><th>Data</th><th>Personale</th><th>Descrizione</th></tr></thead><tbody>"
                        for g in matches["GIORNALIERE"]:
                            html_report += f"<tr><td>{g['data']}</td><td>{g['personale']}</td><td>{g['descrizione']}</td></tr>"
                        html_report += "</tbody></table>"

                    if matches.get("CANTIERE"):
                        html_report += "<h3>Cantiere</h3><table><thead><tr><th>Data</th><th>Personale</th><th>Commessa</th><th>Ore</th></tr></thead><tbody>"
                        for c in matches["CANTIERE"]:
                            html_report += f"<tr><td>{c['data']}</td><td>{c['personale']}</td><td>{c['commessa']}</td><td>{c.get('totale_ore','')}</td></tr>"
                        html_report += "</tbody></table>"

                else:
                    self.telegram.send_message_sync(f"⚠️ Report PDF non supportato per {db_type}.")
                    return

                # Genera PDF
                self._generate_pdf_from_html(html_report, temp_pdf)
                
                # Invia PDF
                if os.path.exists(temp_pdf):
                    caption = f"📄 Report {db_type.capitalize()} - {query_text}"
                    self.telegram.send_document_sync(temp_pdf, caption)
                else:
                    self.telegram.send_message_sync("❌ Errore generazione file PDF.")

            except Exception as e:
                import traceback
                traceback.print_exc()
                self.telegram.send_message_sync(f"❌ Errore imprevisto: {e}")

        elif command == "run_pdl":
            self.navigate_to_panel("scarico_pdl")
            print_enabled = params.get("print", False)
            merge_and_send = params.get("merge_and_send", False)
            merge_all = params.get("merge_all", False)

            self.pdl_panel.print_check.setChecked(print_enabled)
            # Passa i parametri direttamente al pannello via attributi temporanei
            self.pdl_panel.merge_and_send_from_telegram = merge_and_send
            self.pdl_panel.merge_all_session_from_telegram = merge_all

            ready, msg = self.pdl_panel.validate_ready()
            if not ready:
                self.telegram.send_message_sync(
                    f"⚠️ Impossibile avviare Scarico PDL.\nMotivo: {msg}\nUsa '➕ Inserisci PDL' per aggiungere dati."
                )
                # Pulisci gli attributi temporanei se la validazione fallisce
                if hasattr(self.pdl_panel, "merge_and_send_from_telegram"):
                    del self.pdl_panel.merge_and_send_from_telegram
                if hasattr(self.pdl_panel, "merge_all_session_from_telegram"):
                    del self.pdl_panel.merge_all_session_from_telegram
                return
            self.pdl_panel.start_btn.click()
            self.telegram.send_message_sync(
                f"✅ Comando ricevuto. Avvio Scarico PDL (Stampa={print_enabled}, Unisci PDF e invia={merge_and_send}, Merge Sessione={merge_all})"
            )

        elif command == "list_pdl":
            data = self.pdl_panel.data_table.get_data()
            if not data:
                self.telegram.send_message_sync("📋 **Lista PDL Vuota**")
            else:
                items = []
                for row in data:
                    # Estrai il valore dalla prima colonna, indipendentemente dal nome
                    if row and isinstance(row, dict):
                        first_key = next(iter(row))
                        item_value = row.get(first_key)
                        if item_value:  # Filtra valori vuoti o None
                            items.append(str(item_value))
                text = "📋 **Lista PDL Corrente:**\n" + "\n".join([f"• `{i}`" for i in items[:20]])
                if len(items) > 20:
                    text += f"\n...ed altri {len(items)-20}"
                self.telegram.send_message_sync(text)

        elif command == "clear_pdl":
            self.pdl_panel.clear_rows_simple()
            self.telegram.send_message_sync("🗑️ Tabella PDL svuotata.")

        elif command == "run_ts":
            self.navigate_to_panel("scarico_ts")
            ready, msg = self.scarico_panel.validate_ready()
            if not ready:
                self.telegram.send_message_sync(
                    f"⚠️ Impossibile avviare Scarico TS.\nMotivo: {msg}\nUsa '➕ Aggiungi OdA' per aggiungere dati."
                )
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
                if len(items) > 20:
                    text += f"\n...ed altri {len(items)-20}"
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
                if hasattr(self, "lyra_panel"):
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
                    "SafeWork": "https://safework.isab.com/",
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
                if hasattr(self, "pdl_panel"):
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
            if panel and hasattr(panel, "stop_btn") and panel.stop_btn.isEnabled():
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
        else:  # oda
            panel = self.scarico_panel
            field_name = "numero_oda"
            validator = InputValidator.validate_oda

        # 1. Recupera dati esistenti per controllo duplicati
        existing_data = []
        if hasattr(panel, "data_table"):
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
            if len(errors) > 5:
                feedback.append(f"...ed altri {len(errors)-5}")

        if not feedback:
            feedback = ["⚠️ Nessun dato valido inserito."]

        self.telegram.send_message_sync("\n".join(feedback))

    def _handle_telegram_status(self, chat_id):
        """Invia lo stato corrente al bot."""
        panel = self._get_active_bot_panel()
        if panel and hasattr(panel, "get_current_status"):
            status, msg = panel.get_current_status()
            text = f"📊 **Stato Sistema**\n\nAttività: {panel.bot_name}\nStato: {status}\nDettaglio: {msg}"
        else:
            text = "📊 **Stato Sistema**\n\nIl sistema è in attesa (Idle)."

        self.telegram.send_message_sync(text)

    def _handle_telegram_screenshot(self, mode="app"):
        """Cattura lo screenshot (App o Intero Desktop) e lo invia a Telegram."""
=======
    def _preload_all_panels(self):
        """Forza l'inizializzazione di tutti i pannelli."""
        # Mostra un cursore di attesa o un messaggio nella status bar
        self.status_bar.showMessage("⏳ Pre-caricamento moduli in corso... (Attendere)")
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
>>>>>>> refactor/code-optimization
        try:
            # Indices: 0=Dashboard, 1=Automazioni, 2=Lyra, 3=Database, 4=Settings, 5=Help, 6=Notifications
            for i in range(7):
                self.navigation_controller.get_panel(i)
                QApplication.processEvents() # Mantiene la UI viva (opzionale)
            
            # Collegamento automatico aggiornamento Timbrature
            if hasattr(self, "timbrature_bot_panel") and hasattr(self, "timbrature_db_panel"):
                self.timbrature_bot_panel.data_updated.connect(self.timbrature_db_panel.refresh_data)

            self.status_bar.showMessage("✅ Sistema pronto.", 3000)
        finally:
            QApplication.restoreOverrideCursor()

    def _on_anomalies_found(self, count):
        """Gestisce le anomalie trovate da Lyra."""
        if hasattr(self, "sidebar"):
            self.sidebar.btn_lyra.set_badge(count)
        if count > 0:
            ToastManager.instance().show(
                f"⚠️ Lyra ha rilevato {count} anomalie", "warning"
            )

    def _show_update_banner(self, new_version, download_url, changelog):
        """Mostra un banner informativo per la nuova versione."""
        if hasattr(self, "update_banner"):
            self.update_banner.show_update(new_version, download_url, changelog)

        # Notifica tray tramite controller
        if hasattr(self, "tray_controller"):
            self.tray_controller.show_message(
                "Aggiornamento Disponibile",
                f"È uscita la versione {new_version}. Clicca qui per scaricarla.",
            )

    def show_background_notification(
        self, title: str, message: str, is_error: bool = False
    ):
        """
        Mostra una notifica di sistema (Toast) se l'applicazione non è attiva.
        """
        is_active = self.isActiveWindow() and not self.isMinimized()

        if not is_active and hasattr(self, "tray_controller"):
            icon = (
                QSystemTrayIcon.MessageIcon.Critical
                if is_error
                else QSystemTrayIcon.MessageIcon.Information
            )
            self.tray_controller.show_message(title, message, icon, 5000)
            QApplication.alert(self, 0)

<<<<<<< HEAD
    def show_toast(self, message: str, level: str = "info", duration: int = 3000):
        """Mostra una notifica toast (Wrapper for backward compatibility)."""
        # Supporto retrocompatibilità: se il secondo argomento è un intero, è la durata
        if isinstance(level, int):
            duration = level
            level = "info"
            
        ToastManager.instance().show(message, level, duration)
=======
    def show_toast(self, message: str, duration: int = 3000):
        """Mostra una notifica toast."""
        ToastManager.instance().show(message, "info", duration)
>>>>>>> refactor/code-optimization

    def _load_styles(self):
        """Carica i fogli di stile QSS."""
        for qss in ["main_window.qss", "message_box.qss"]:
            path = Path(f"assets/styles/{qss}")
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    self.setStyleSheet(self.styleSheet() + f.read())

    def _setup_ui(self):
        """Configura l'interfaccia con Placeholders per Lazy Loading."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.status_bar.addPermanentWidget(self.progress_bar)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # SIDEBAR
        self.sidebar = SidebarWidget()
        self.sidebar.navigation_requested.connect(
            self.navigation_controller.navigate_to
        )
        main_layout.addWidget(self.sidebar)

        # CONTENT AREA
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)

        self.update_banner = UpdateBanner()
        self.update_banner.download_requested.connect(self._on_download_update_clicked)
        content_layout.addWidget(self.update_banner)

        self.global_search = QLineEdit()
        self.global_search.setPlaceholderText(
            "🔍 Ricerca Universale (OdA, Dipendenti, Log...) - Ctrl+F"
        )
        self.global_search.setMinimumHeight(40)
        self.global_search.returnPressed.connect(
            lambda: self.search_controller.perform_search(self.global_search.text())
        )
        content_layout.addWidget(self.global_search)

        # Page Stack con Placeholder
        self.page_stack = QStackedWidget()
        for i in range(7):
            placeholder = QWidget()
            # Inseriamo un layout per indicare il caricamento se necessario
            self.page_stack.addWidget(placeholder)
            setattr(self, f"_panel_initialized_{i}", False)

        content_layout.addWidget(self.page_stack)
        main_layout.addWidget(content_area)

    def _connect_signals(self):
        """Collega i segnali globali."""
        NotificationManager.instance().unread_count_changed.connect(
            self.sidebar.btn_notifications.set_badge
        )
        self.sidebar.btn_notifications.set_badge(
            NotificationManager.instance().get_unread_count()
        )

    def _setup_shortcuts(self):
        """Configura le scorciatoie da tastiera globali."""
        self.shortcut_f5 = QShortcut(QKeySequence(Qt.Key.Key_F5), self)
        self.shortcut_f5.activated.connect(self._handle_f5)

        self.shortcut_search = QShortcut(QKeySequence("Ctrl+F"), self)
        self.shortcut_search.activated.connect(self._handle_ctrl_f)

    def _handle_f5(self):
        """Gestisce F5."""
        idx = self.page_stack.currentIndex()
        if idx == 0 and hasattr(self, "dashboard_panel"):
            self.dashboard_panel.refresh_data()
        elif idx == 3 and hasattr(self, "database_widget"):
            tab_idx = self.database_widget.currentIndex()
            if tab_idx == 0:
                self.timbrature_db_panel.refresh_data()
            elif tab_idx == 1:
                self.contabilita_panel.refresh_tabs()
            elif tab_idx == 2:
                self.scarico_ore_panel._start_update()

    def _handle_ctrl_f(self):
        """Gestisce Ctrl+F."""
        self.global_search.setFocus()
        self.global_search.selectAll()

    def _on_help_requested(self, section_title):
        self.navigation_controller.navigate_to(5)
        self.help_panel.open_section(section_title)

    def _on_settings_saved(self):
<<<<<<< HEAD
        """Aggiorna i pannelli quando le impostazioni vengono salvate."""
        self.scarico_panel.refresh_fornitori()
        self.dettagli_panel.refresh_fornitori()
        self.timbrature_bot_panel.refresh_fornitori()

        # Riavvia il servizio Telegram per applicare eventuali nuovi token
        # Nota: lo facciamo solo se necessario o con un debounce? Per ora lasciamo così.
        self.telegram.start_service()

        # Feedback Toast rimosso perché i salvataggi sono automatici e continui
        # ToastManager.instance().show("Impostazioni salvate con successo!", "success")

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
=======
        if hasattr(self, "scarico_panel"):
>>>>>>> refactor/code-optimization
            self.scarico_panel.refresh_fornitori()
        if hasattr(self, "dettagli_panel"):
            self.dettagli_panel.refresh_fornitori()
        if hasattr(self, "timbrature_bot_panel"):
            self.timbrature_bot_panel.refresh_fornitori()
        self.telegram.start_service()
        ToastManager.instance().show("Impostazioni salvate!", "success")

    def _check_and_start_contabilita_update(self):
        config = config_manager.load_config()
        if config.get("enable_auto_update_contabilita", False):
            # Assicuriamoci che il pannello sia caricato se dobbiamo avviarlo
            self.navigation_controller.get_panel(3)
            self.contabilita_panel.start_import_process()

    def _on_download_update_clicked(self, url):
        import webbrowser

        webbrowser.open(url)

    # Wrapper per compatibilità
    def navigate_to_panel(self, panel_key: str):
        self.navigation_controller.navigate_to_panel(panel_key)

    def analyze_with_lyra(self, context_text: str):
        self.navigation_controller.analyze_with_lyra(context_text)

    def show_settings(self):
        self.navigation_controller.navigate_to(4)

    def closeEvent(self, event):
        if self._force_quit:
            if self.telegram:
                self.telegram.stop_service()
            config = config_manager.load_config()
            if config.get("auto_backup", True):
                BackupManager.create_backup()
            event.accept()
            return
        if self.isVisible():
            self.hide()
            event.ignore()
