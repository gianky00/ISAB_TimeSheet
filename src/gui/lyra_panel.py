from io import StringIO
from pathlib import Path

import markdown
import pandas as pd
from PyQt6.QtCore import QSize, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.lyra_client import LyraClient
from src.core.secrets_manager import SecretsManager
from src.utils.document_processor import DocumentProcessor
from src.utils.helpers import get_asset_path


class LyraWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, api_key: str, question: str, context: str = "", images: list = None):
        super().__init__()
        self.api_key = api_key
        self.question = question
        self.context = context
        self.images = images or []

    def run(self):
        try:
            if not self.api_key:
                self.finished.emit(
                    "⚠️ Errore critico: Chiave API Gemini non trovata. Configurala nelle Impostazioni."
                )
                return

            # Inietta la chiave nel client
            client = LyraClient(api_key=self.api_key)

            # Esegui la richiesta
            answer = client.ask(self.question, self.context, self.images)
            self.finished.emit(answer)

        except Exception as e:
            import traceback

            error_details = traceback.format_exc()
            self.finished.emit(f"⚠️ Errore critico nel Worker di Lyra:\n{str(e)}\n\n{error_details}")


class ModelListWorker(QThread):
    finished = pyqtSignal(list)

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key

    def run(self):
        try:
            if not self.api_key:
                self.finished.emit([])
                return

            client = LyraClient(api_key=self.api_key)
            models = client.list_models()
            self.finished.emit(models)
        except Exception:
            self.finished.emit([])


class LyraPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_table_data = None
        self.attached_file = None
        self.attached_images = []
        self._setup_ui()
        self.worker = None
        self.setAcceptDrops(True)
        # Carica modelli all'avvio
        self._fetch_models()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header = QFrame()
        header.setStyleSheet("background-color: #6f42c1; border-radius: 8px; padding: 10px 15px;")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("✨ Lyra AI")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        h_layout.addWidget(title)

        # Model Selector
        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(180)
        self.model_combo.currentTextChanged.connect(self._on_model_changed)
        self.model_combo.setStyleSheet(
            """
            QComboBox { 
                background-color: rgba(255,255,255,0.2); 
                color: white; 
                border: 1px solid rgba(255,255,255,0.5);
                padding: 5px 10px;
                border-radius: 4px;
            }
            QComboBox::drop-down { border: none; }
        """
        )
        h_layout.addWidget(self.model_combo)

        refresh_models_btn = QPushButton()
        refresh_models_btn.setIcon(QIcon(get_asset_path("assets/icons/refresh.svg")))
        refresh_models_btn.setFixedSize(32, 32)
        refresh_models_btn.setIconSize(QSize(18, 18))
        refresh_models_btn.setToolTip("Aggiorna lista modelli")
        refresh_models_btn.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        refresh_models_btn.clicked.connect(self._fetch_models)
        h_layout.addWidget(refresh_models_btn)

        sub = QLabel("Esperta Contabile")
        sub.setStyleSheet("color: rgba(255,255,255,0.8); margin-left: 10px;")  # Added margin for spacing
        h_layout.addWidget(sub)

        h_layout.addStretch()

        # Export Button in Header
        export_btn = QPushButton("Esporta Chat")
        export_btn.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(255,255,255,0.2);
                color: white;
                border: 1px solid rgba(255,255,255,0.5);
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.3);
            }
        """
        )
        export_btn.clicked.connect(self._export_chat)
        h_layout.addWidget(export_btn)

        layout.addWidget(header)

        # Chat History
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        # Custom CSS for Tables within QTextEdit
        self.chat_area.setStyleSheet(
            """
            QTextEdit {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
                font-size: 15px;
            }
        """
        )
        layout.addWidget(self.chat_area)

        # Tool Bar for Table Actions
        self.table_actions_layout = QHBoxLayout()
        self.table_actions_layout.setContentsMargins(0, 5, 0, 5)
        self.btn_export_last_table = QPushButton("📊 Esporta Ultima Tabella Excel")
        self.btn_export_last_table.setVisible(False)
        self.btn_export_last_table.setStyleSheet(
            """
            QPushButton {
                background-color: #198754;
                color: white;
                border-radius: 4px;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #157347; }
        """
        )
        self.btn_export_last_table.clicked.connect(self._export_excel)
        self.table_actions_layout.addWidget(self.btn_export_last_table)
        self.table_actions_layout.addStretch()

        layout.addLayout(self.table_actions_layout)

        # Attachment Info Bar (Hidden by default)
        self.attachment_frame = QFrame()
        self.attachment_frame.setVisible(False)
        self.attachment_frame.setStyleSheet(
            """
            QFrame {
                background-color: #f1f3f9;
                border: 1px dashed #6f42c1;
                border-radius: 6px;
                margin-bottom: 5px;
            }
        """
        )
        att_layout = QHBoxLayout(self.attachment_frame)
        self.att_label = QLabel("📎 Documento allegato: nome_file.pdf")
        self.att_label.setStyleSheet("color: #4b2c85; font-weight: bold; border: none;")
        att_layout.addWidget(self.att_label)

        att_layout.addStretch()

        self.btn_remove_att = QPushButton("✕")
        self.btn_remove_att.setFixedSize(24, 24)
        self.btn_remove_att.setStyleSheet(
            "background: transparent; color: #dc3545; font-weight: bold; border: none;"
        )
        self.btn_remove_att.clicked.connect(self._remove_attachment)
        att_layout.addWidget(self.btn_remove_att)

        layout.addWidget(self.attachment_frame)

        # Quick Actions Scroll Area
        scroll_container = QWidget()
        scroll_layout = QHBoxLayout(scroll_container)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(10)

        # Define Quick Actions
        actions = [
            (
                "Estrai Tabella Giornaliere",
                "Analizza il documento allegato ed estrai i dati in una tabella Markdown pulita. Colonne suggerite: Data, Nome, Ore Lavorate, Commessa.",
            ),
            (
                "Trova Anomalie Documento",
                "Verifica se ci sono incongruenze o dati mancanti nel documento che ho allegato.",
            ),
            ("Sintesi PDF", "Dammi un breve riepilogo del contenuto di questo documento."),
        ]

        for btn_text, prompt_text in actions:
            btn = QPushButton(btn_text)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #f8f9fa;
                    color: #6f42c1;
                    border: 1px solid #6f42c1;
                    border-radius: 15px;
                    padding: 5px 15px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #6f42c1;
                    color: white;
                }
            """
            )
            btn.clicked.connect(lambda checked, t=prompt_text: self._set_input(t))
            scroll_layout.addWidget(btn)

        scroll_layout.addStretch()

        quick_scroll = QScrollArea()
        quick_scroll.setWidget(scroll_container)
        quick_scroll.setWidgetResizable(True)
        quick_scroll.setFixedHeight(50)
        quick_scroll.setFrameShape(QFrame.Shape.NoFrame)
        quick_scroll.setStyleSheet("background: transparent;")

        layout.addWidget(quick_scroll)

        # Input Area
        input_layout = QHBoxLayout()

        self.attach_btn = QPushButton("📎")
        self.attach_btn.setFixedSize(45, 45)
        self.attach_btn.setToolTip("Allega un documento (PDF)")
        self.attach_btn.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                border: 2px solid #ced4da;
                border-radius: 22px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                border-color: #6f42c1;
            }
        """
        )
        self.attach_btn.clicked.connect(self._attach_file)
        input_layout.addWidget(self.attach_btn)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Chiedi a Lyra o trascina qui un PDF...")
        self.input_field.setMinimumHeight(45)
        self.input_field.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #ced4da;
                border-radius: 22px;
                padding: 0 15px;
                font-size: 15px;
            }
            QLineEdit:focus {
                border-color: #6f42c1;
            }
        """
        )
        self.input_field.returnPressed.connect(self._send_message)
        input_layout.addWidget(self.input_field)

        self.send_btn = QPushButton("Invia")
        self.send_btn.setMinimumHeight(45)
        self.send_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #6f42c1;
                color: white;
                border-radius: 22px;
                padding: 0 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #59359a;
            }
        """
        )
        self.send_btn.clicked.connect(self._send_message)
        input_layout.addWidget(self.send_btn)

        layout.addLayout(input_layout)

        # Welcome message
        self._append_message(
            "Lyra", "Ciao! Sono pronta ad analizzare i tuoi dati e i tuoi documenti. Cosa vuoi sapere oggi?"
        )

    def _fetch_models(self):
        """Avvia il worker per recuperare la lista dei modelli."""
        api_key = SecretsManager.get_gemini_api_key()
        if not api_key:
            self.model_combo.clear()
            self.model_combo.addItem("API Key mancante")
            self.model_combo.setEnabled(False)
            return

        self.model_combo.clear()
        self.model_combo.addItem("Caricamento modelli...")
        self.model_combo.setEnabled(False)

        self.model_worker = ModelListWorker(api_key)
        self.model_worker.finished.connect(self._populate_models_dropdown)
        self.model_worker.start()

    def _on_model_changed(self, model_name):
        """Salva il modello scelto nella configurazione globale."""
        if model_name and "Caricamento" not in model_name and "mancante" not in model_name:
            config_manager.set_config_value("ai_model", model_name)

    def _populate_models_dropdown(self, models):
        self.model_combo.blockSignals(True)  # Evita loop durante popolamento
        self.model_combo.clear()
        if models:
            # Filtra per i modelli che ci interessano di più
            pro_models = sorted([m for m in models if "pro" in m], reverse=True)
            flash_models = sorted([m for m in models if "flash" in m], reverse=True)
            other_models = sorted([m for m in models if "pro" not in m and "flash" not in m])

            ordered_models = pro_models + flash_models + other_models
            self.model_combo.addItems(ordered_models)

            # Carica quello salvato
            saved_model = config_manager.get_config_value("ai_model", "")
            if saved_model and saved_model in ordered_models:
                self.model_combo.setCurrentText(saved_model)
            elif pro_models:
                self.model_combo.setCurrentText(pro_models[0])

            self.model_combo.setEnabled(True)
        else:
            self.model_combo.addItem("Nessun modello trovato")
            self.model_combo.setEnabled(False)
        self.model_combo.blockSignals(False)

    def _attach_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Allega Documento", "", "Documenti (*.pdf *.png *.jpg)"
        )
        if file_path:
            self._handle_file(file_path)

    def _handle_file(self, file_path):
        p = Path(file_path)
        if p.suffix.lower() == ".pdf":
            self.attached_file = p
            self.att_label.setText(f"📎 PDF allegato: {p.name}")
            self.attachment_frame.setVisible(True)

            # Pre-processing: converts PDF to images for better OCR if needed
            # Or just send text if searchable. LyraClient will handle.
            # For now, let's prepare images to be safe (Vision is better for tables)
            self.attached_images = DocumentProcessor.get_pages_as_images(p)

            # Automatic prompt suggestion
            self.input_field.setText("Analizza questo documento ed estrai i dati principali in una tabella.")
            self.input_field.setFocus()
        else:
            QMessageBox.warning(self, "Formato non supportato", "Lyra al momento analizza solo file PDF.")

    def _remove_attachment(self):
        self.attached_file = None
        self.attached_images = []
        self.attachment_frame.setVisible(False)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self._handle_file(file_path)

    def _set_input(self, text):
        """Imposta il testo nell'input field."""
        self.input_field.setText(text)
        self.input_field.setFocus()

    def _send_message(self):
        text = self.input_field.text().strip()
        if not text and not self.attached_file:
            return

        self.ask_lyra(text)
        self.input_field.clear()

    def ask_lyra(self, question: str, context: str = ""):
        """Avvia una richiesta a Lyra."""
        self._append_message("Tu", question)

        final_images = self.attached_images.copy()

        if self.attached_file:
            self._append_message("Sistema", f"<i>[Documento allegato: {self.attached_file.name}]</i>")
            # If the PDF is text-searchable, we can also append the text to context
            if DocumentProcessor.is_pdf_searchable(self.attached_file):
                pdf_text = DocumentProcessor.extract_text(self.attached_file)
                context += f"\n\nCONTENUTO TESTUALE DOCUMENTO:\n{pdf_text}\n"

        self.input_field.setDisabled(True)
        self.attach_btn.setDisabled(True)
        self.chat_area.setFocus()

        # Preleva la chiave API nel thread principale e la passa al worker
        api_key = SecretsManager.get_gemini_api_key()

        self.worker = LyraWorker(api_key, question, context, final_images)
        self.worker.finished.connect(self._on_answer)
        self.worker.start()

        # NON rimuovere l'allegato automaticamente, permetti domande di follow-up
        # self._remove_attachment()

    def _on_answer(self, text):
        self._append_message("Lyra", text)
        self.input_field.setDisabled(False)
        self.attach_btn.setDisabled(False)
        self.input_field.setFocus()

    def _format_markdown(self, text: str) -> str:
        """Uses 'markdown' library to convert MD to HTML with table extension."""
        try:
            # Enable 'tables' and 'fenced_code' extensions
            html = markdown.markdown(text, extensions=["tables", "fenced_code"])

            # Post-process for styling
            style_table = 'border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse; width: 100%; margin-top: 10px; margin-bottom: 10px; border-color: #dee2e6;"'
            style_th = 'style="background-color: #f8f9fa; color: #495057; font-weight: bold; padding: 8px;"'
            style_td = 'style="padding: 8px;"'

            html = html.replace("<table>", f"<table {style_table}>")
            html = html.replace("<th>", f"<th {style_th}>")
            html = html.replace("<td>", f"<td {style_td}>")

            # Detect tables for export context
            if "<table>" in html:
                self.last_table_data = text
                self.btn_export_last_table.setVisible(True)

            return html
        except Exception as e:
            print(f"Markdown error: {e}")
            return text

    def _append_message(self, sender, text):
        color = "#6f42c1" if sender == "Lyra" else "#495057"
        align = "left"

        formatted_html = self._format_markdown(text)

        # Reduced margin-bottom from 15px to 5px to compact the view
        html = f"""
        <div style="margin-bottom: 20px; text-align: {align};">
            <div style="font-weight: bold; color: {color}; font-size: 13px; margin-bottom: 2px;">{sender}</div>
            <div style="font-size: 15px; line-height: 1.5; color: #212529;">
                {formatted_html}
            </div>
        </div>
        """
        self.chat_area.append(html)

        # Scroll to bottom
        sb = self.chat_area.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _export_chat(self):
        """Esporta la chat in PDF o l'ultima tabella in Excel."""
        menu = QMenu(self)

        pdf_action = QAction("📄 Esporta come PDF", self)
        pdf_action.triggered.connect(self._export_pdf)
        menu.addAction(pdf_action)

        excel_action = QAction("📊 Esporta ultima tabella (Excel)", self)
        excel_action.triggered.connect(self._export_excel)
        menu.addAction(excel_action)

        # Use sender to position
        sender = self.sender()
        if sender:
            pos = sender.mapToGlobal(sender.rect().bottomLeft())
            menu.exec(pos)

    def _export_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Salva Chat PDF", "chat_lyra.pdf", "PDF Files (*.pdf)"
        )
        if filename:
            try:
                from PyQt6.QtPrintSupport import QPrinter

                printer = QPrinter(QPrinter.PrinterMode.HighResolution)
                printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
                printer.setOutputFileName(filename)

                self.chat_area.document().print(printer)
                QMessageBox.information(self, "Successo", "Chat esportata correttamente!")
            except Exception as e:
                # Fallback: Save as HTML
                html_file = filename.replace(".pdf", ".html")
                with open(html_file, "w", encoding="utf-8") as f:
                    f.write(self.chat_area.toHtml())
                QMessageBox.warning(
                    self, "Info", f"PDF driver non trovato. Salvato come HTML: {html_file}\nErr: {e}"
                )

    def _export_excel(self):
        """Exports the last table found in the chat history to Excel."""
        if not self.last_table_data:
            QMessageBox.warning(self, "Nessuna tabella", "Non ho trovato tabelle recenti da esportare.")
            return

        text = self.last_table_data
        lines = text.split("\n")
        table_lines = []

        current_block = []
        for line in lines:
            if line.strip().startswith("|"):
                current_block.append(line)
            else:
                if current_block:
                    if len(current_block) >= 2:
                        table_lines = current_block
                    current_block = []

        if current_block:
            if len(current_block) >= 2:
                table_lines = current_block

        if not table_lines:
            QMessageBox.warning(self, "Nessuna tabella", "Non ho trovato tabelle valide nel messaggio.")
            return

        try:
            cleaned_lines = [l for l in table_lines if "---" not in l]

            data = StringIO("\n".join(cleaned_lines))
            df = pd.read_csv(data, sep="|", header=0, engine="python")

            # Clean empty columns from pipes
            df = df.dropna(axis=1, how="all")
            df.columns = df.columns.str.strip()
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

            filename, _ = QFileDialog.getSaveFileName(
                self, "Salva Tabella Excel", "analisi_lyra.xlsx", "Excel Files (*.xlsx)"
            )
            if filename:
                df.to_excel(filename, index=False)
                QMessageBox.information(self, "Successo", "Tabella esportata correttamente!")

        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile esportare la tabella: {e}")

    def _set_input(self, text):
        """Imposta il testo nell'input field."""
        self.input_field.setText(text)
        self.input_field.setFocus()

    def _send_message(self):
        text = self.input_field.text().strip()
        if not text:
            return
        self.ask_lyra(text)
        self.input_field.clear()

    def ask_lyra(self, question: str, context: str = ""):
        """Avvia una richiesta a Lyra."""
        self._append_message("Tu", question)
        if context:
            self._append_message("Sistema", "<i>[Dati allegati all'analisi]</i>")

        self.input_field.setDisabled(True)
        self.chat_area.setFocus()

        self.worker = LyraWorker(question, context)
        self.worker.finished.connect(self._on_answer)
        self.worker.start()

    def _on_answer(self, text):
        self._append_message("Lyra", text)
        self.input_field.setDisabled(False)
        self.input_field.setFocus()

    def _format_markdown(self, text: str) -> str:
        """Uses 'markdown' library to convert MD to HTML with table extension."""
        try:
            # Enable 'tables' and 'fenced_code' extensions
            html = markdown.markdown(text, extensions=["tables", "fenced_code"])

            # Post-process for styling
            style_table = 'border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse; width: 100%; margin-top: 10px; margin-bottom: 10px; border-color: #dee2e6;"'
            style_th = 'style="background-color: #f8f9fa; color: #495057; font-weight: bold; padding: 8px;"'
            style_td = 'style="padding: 8px;"'

            html = html.replace("<table>", f"<table {style_table}>")
            html = html.replace("<th>", f"<th {style_th}>")
            html = html.replace("<td>", f"<td {style_td}>")

            # Detect tables for export context
            if "<table>" in html:
                self.last_table_data = text
                self.btn_export_last_table.setVisible(True)

            return html
        except Exception as e:
            print(f"Markdown error: {e}")
            return text

    def _append_message(self, sender, text):
        color = "#6f42c1" if sender == "Lyra" else "#495057"
        align = "left"

        formatted_html = self._format_markdown(text)

        # Reduced margin-bottom from 15px to 5px to compact the view
        html = f"""
        <div style="margin-bottom: 20px; text-align: {align};">
            <div style="font-weight: bold; color: {color}; font-size: 13px; margin-bottom: 2px;">{sender}</div>
            <div style="font-size: 15px; line-height: 1.5; color: #212529;">
                {formatted_html}
            </div>
        </div>
        """
        self.chat_area.append(html)

        # Scroll to bottom
        sb = self.chat_area.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _export_chat(self):
        """Esporta la chat in PDF o l'ultima tabella in Excel."""
        menu = QMenu(self)

        pdf_action = QAction("📄 Esporta come PDF", self)
        pdf_action.triggered.connect(self._export_pdf)
        menu.addAction(pdf_action)

        excel_action = QAction("📊 Esporta ultima tabella (Excel)", self)
        excel_action.triggered.connect(self._export_excel)
        menu.addAction(excel_action)

        # FIXED: Use sender directly instead of casting
        sender = self.sender()
        if sender:
            # Calculate position below the button
            pos = sender.mapToGlobal(sender.rect().bottomLeft())
            menu.exec(pos)

    def _export_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Salva Chat PDF", "chat_lyra.pdf", "PDF Files (*.pdf)"
        )
        if filename:
            try:
                # Using QPrinter (requires PyQt6.QtPrintSupport)
                from PyQt6.QtPrintSupport import QPrinter

                printer = QPrinter(QPrinter.PrinterMode.HighResolution)
                printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
                printer.setOutputFileName(filename)

                self.chat_area.document().print(printer)
                QMessageBox.information(self, "Successo", "Chat esportata correttamente!")
            except Exception as e:
                # Fallback: Save as HTML
                html_file = filename.replace(".pdf", ".html")
                with open(html_file, "w", encoding="utf-8") as f:
                    f.write(self.chat_area.toHtml())
                QMessageBox.warning(
                    self, "Info", f"PDF driver non trovato. Salvato come HTML: {html_file}\nErr: {e}"
                )

    def _export_excel(self):
        """Exports the last table found in the chat history to Excel."""
        # FIX: Use self.last_table_data which stores the raw Markdown
        if not self.last_table_data:
            QMessageBox.warning(self, "Nessuna tabella", "Non ho trovato tabelle recenti da esportare.")
            return

        text = self.last_table_data
        lines = text.split("\n")
        table_lines = []

        # Capture the table block from the stored markdown
        # Assuming the stored text IS mostly the table or contains it
        current_block = []
        for line in lines:
            if line.strip().startswith("|"):
                current_block.append(line)
            else:
                if current_block:
                    if len(current_block) >= 2:
                        table_lines = current_block
                        # We found a table, might be multiple, take the last one or all?
                        # Taking the last one found in the text chunk
                    current_block = []

        if current_block:
            if len(current_block) >= 2:
                table_lines = current_block

        if not table_lines:
            QMessageBox.warning(self, "Nessuna tabella", "Non ho trovato tabelle valide nel messaggio.")
            return

        try:
            cleaned_lines = [l for l in table_lines if "---" not in l]

            data = StringIO("\n".join(cleaned_lines))
            # Use pandas read_csv with sep='|'
            # Markdown tables often have leading/trailing pipes
            df = pd.read_csv(data, sep="|", header=0, engine="python")

            # Clean empty columns from pipes
            df = df.dropna(axis=1, how="all")
            df.columns = df.columns.str.strip()
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

            filename, _ = QFileDialog.getSaveFileName(
                self, "Salva Tabella Excel", "analisi_lyra.xlsx", "Excel Files (*.xlsx)"
            )
            if filename:
                df.to_excel(filename, index=False)
                QMessageBox.information(self, "Successo", "Tabella esportata correttamente!")

        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile esportare la tabella: {e}")
