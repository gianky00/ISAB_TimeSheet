"""
Bot TS - Lyra AI Panel
Interfaccia di chat per l'assistente IA.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel,
    QFrame, QScrollArea, QFileDialog, QMenu, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMargins
from PyQt6.QtGui import QAction, QTextDocument
from src.core.lyra_client import LyraClient
import markdown
import pandas as pd
from io import StringIO
import re

class LyraWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, question, context=""):
        super().__init__()
        self.question = question
        self.context = context
        self.client = LyraClient()

    def run(self):
        answer = self.client.ask(self.question, self.context)
        self.finished.emit(answer)

class LyraPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_table_data = None # Store latest table for export
        self._setup_ui()
        self.worker = None

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header = QFrame()
        header.setStyleSheet("background-color: #6f42c1; border-radius: 8px; padding: 10px 15px;")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(0,0,0,0)

        title = QLabel("✨ Lyra AI")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        h_layout.addWidget(title)

        sub = QLabel("Esperta Contabile")
        sub.setStyleSheet("color: rgba(255,255,255,0.8);")
        h_layout.addWidget(sub)

        h_layout.addStretch()

        # Export Button in Header
        export_btn = QPushButton("Esporta Chat")
        export_btn.setStyleSheet("""
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
        """)
        export_btn.clicked.connect(self._export_chat)
        h_layout.addWidget(export_btn)

        layout.addWidget(header)

        # Chat History
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        # Custom CSS for Tables within QTextEdit
        self.chat_area.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
                font-size: 15px;
            }
        """)
        layout.addWidget(self.chat_area)

        # Quick Actions Scroll Area
        scroll_container = QWidget()
        scroll_layout = QHBoxLayout(scroll_container)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(10)

        # Define Quick Actions
        actions = [
            ("Analisi Margini", "Analizza i margini operativi per l'anno corrente evidenziando le criticità."),
            ("Riepilogo Costi", "Dammi un riepilogo dettagliato dei costi stimati rispetto al preventivato."),
            ("Stato Commesse", "Qual è lo stato di avanzamento globale delle commesse? Ci sono blocchi?"),
            ("Top 5 Performance", "Quali sono le 5 commesse con la resa migliore?"),
            ("Errori Comuni", "Verifica se ci sono incongruenze nei dati (es. ODC mancanti, rese anomale).")
        ]

        for btn_text, prompt_text in actions:
            btn = QPushButton(btn_text)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #e9ecef;
                    color: #495057;
                    border: 1px solid #ced4da;
                    border-radius: 15px;
                    padding: 5px 15px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #dee2e6;
                    border-color: #adb5bd;
                    color: #212529;
                }
            """)
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
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Chiedi a Lyra (es. 'Come sta andando il margine quest'anno?')")
        self.input_field.setMinimumHeight(45)
        self.input_field.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ced4da;
                border-radius: 22px;
                padding: 0 15px;
                font-size: 15px;
            }
            QLineEdit:focus {
                border-color: #6f42c1;
            }
        """)
        self.input_field.returnPressed.connect(self._send_message)
        input_layout.addWidget(self.input_field)

        self.send_btn = QPushButton("Invia")
        self.send_btn.setMinimumHeight(45)
        self.send_btn.setStyleSheet("""
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
        """)
        self.send_btn.clicked.connect(self._send_message)
        input_layout.addWidget(self.send_btn)

        layout.addLayout(input_layout)

        # Welcome message
        self._append_message("Lyra", "Ciao! Sono pronta ad analizzare i tuoi dati. Cosa vuoi sapere oggi?")

    def _set_input(self, text):
        """Imposta il testo nell'input field."""
        self.input_field.setText(text)
        self.input_field.setFocus()

    def _send_message(self):
        text = self.input_field.text().strip()
        if not text: return
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
            html = markdown.markdown(text, extensions=['tables', 'fenced_code'])

            # Post-process for styling (since we can't inject CSS classes easily into the lib output)
            # Add basic style to tables
            style_table = 'border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse; width: 100%; margin-top: 10px; margin-bottom: 10px; border-color: #dee2e6;"'
            style_th = 'style="background-color: #f8f9fa; color: #495057; font-weight: bold; padding: 8px;"'
            style_td = 'style="padding: 8px;"'

            html = html.replace('<table>', f'<table {style_table}>')
            html = html.replace('<th>', f'<th {style_th}>')
            html = html.replace('<td>', f'<td {style_td}>')

            # Detect tables for export context (simple heuristic)
            if '<table>' in html:
                self.last_table_data = text # Store original MD for parsing or just flag it

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

        # Show menu at cursor position relative to the button
        # But button logic is internal to this method call? No, it's called by button click.
        # We need the button position or just show under mouse.
        menu.exec(QAction.staticMetaObject.cast(self.sender()).parentWidget().mapToGlobal(self.sender().pos()))


    def _export_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Salva Chat PDF", "chat_lyra.pdf", "PDF Files (*.pdf)")
        if filename:
            try:
                printer = self.chat_area.document()
                # Qt6 printing requires QPrinter, but QTextDocument has print method? No.
                # Simplified: Save HTML?
                # Better: Use QPdfWriter or simple print to pdf if available.
                # Since dependencies are minimal, let's use a simpler approach: Print to PDF using QPrinter if available
                # or just save HTML.

                # Using QPrinter (requires PyQt6.QtPrintSupport)
                from PyQt6.QtPrintSupport import QPrinter
                printer = QPrinter(QPrinter.PrinterMode.HighResolution)
                printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
                printer.setOutputFileName(filename)

                self.chat_area.document().print(printer)
                QMessageBox.information(self, "Successo", "Chat esportata correttamente!")
            except Exception as e:
                # Fallback: Save as HTML
                html_file = filename.replace('.pdf', '.html')
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(self.chat_area.toHtml())
                QMessageBox.warning(self, "Info", f"PDF driver non trovato. Salvato come HTML: {html_file}\nErr: {e}")

    def _export_excel(self):
        """Exports the last table found in the chat history to Excel."""
        # Retrieve full text or just inspect self.last_table_data
        # Parsing Markdown table is tricky without regex or dedicated lib.
        # Let's try to extract tables from the entire Markdown history if possible?
        # Actually, self.last_table_data stores the markdown chunk of the last message if it contained a table.
        # But we need the clean markdown table.

        # Simpler: Ask user to paste the table? No.
        # Robust: Parse self.chat_area.toPlainText() looking for Markdown table patterns.

        text = self.chat_area.toPlainText()
        # Find last occurrence of a markdown table pattern
        # Lines starting with |
        lines = text.split('\n')
        table_lines = []
        capturing = False

        # Capture the LAST table block
        current_block = []
        for line in lines:
            if line.strip().startswith('|'):
                current_block.append(line)
            else:
                if current_block:
                    # Check if it looks like a table (at least 2 lines)
                    if len(current_block) >= 2:
                        table_lines = current_block # Keep replacing to get the last one
                    current_block = []

        if current_block: # End of file case
             if len(current_block) >= 2:
                table_lines = current_block

        if not table_lines:
            QMessageBox.warning(self, "Nessuna tabella", "Non ho trovato tabelle recenti da esportare.")
            return

        try:
            # Convert markdown table lines to dataframe
            # Remove separator line (e.g., |---|---|)
            cleaned_lines = [l for l in table_lines if '---' not in l]

            data = StringIO("\n".join(cleaned_lines))
            # Use pandas read_csv with sep='|'
            # Note: Markdown tables often have leading/trailing pipes which create empty cols
            df = pd.read_csv(data, sep='|', header=0, engine='python')

            # Clean up empty columns (first and last usually)
            df = df.dropna(axis=1, how='all')
            # Clean whitespace from headers and cells
            df.columns = df.columns.str.strip()
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

            filename, _ = QFileDialog.getSaveFileName(self, "Salva Tabella Excel", "analisi_lyra.xlsx", "Excel Files (*.xlsx)")
            if filename:
                df.to_excel(filename, index=False)
                QMessageBox.information(self, "Successo", "Tabella esportata correttamente!")

        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile esportare la tabella: {e}")
