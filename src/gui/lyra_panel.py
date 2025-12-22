"""
Bot TS - Lyra AI Panel
Interfaccia di chat per l'assistente IA.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from src.core.lyra_client import LyraClient
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
        self._setup_ui()
        self.worker = None

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header = QFrame()
        header.setStyleSheet("background-color: #6f42c1; border-radius: 8px; padding: 15px;")
        h_layout = QHBoxLayout(header)

        title = QLabel("✨ Lyra AI")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        h_layout.addWidget(title)

        sub = QLabel("Esperta Contabile")
        sub.setStyleSheet("color: rgba(255,255,255,0.8);")
        h_layout.addWidget(sub)
        h_layout.addStretch()

        layout.addWidget(header)

        # Chat History
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
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
            # Use default param in lambda to capture value
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

    def _format_markdown_to_html(self, text: str) -> str:
        """Converte Markdown di base in HTML."""
        # 1. Bold: **text** -> <b>text</b>
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

        # 2. Lists:
        # Unordered: - item or * item
        lines = text.split('\n')
        new_lines = []
        in_list = False

        for line in lines:
            line = line.strip()
            if line.startswith('- ') or line.startswith('* '):
                content = line[2:]
                if not in_list:
                    new_lines.append("<ul>")
                    in_list = True
                new_lines.append(f"<li>{content}</li>")
            else:
                if in_list:
                    new_lines.append("</ul>")
                    in_list = False
                new_lines.append(line)

        if in_list:
            new_lines.append("</ul>")

        text = "\n".join(new_lines)

        # 3. Newlines to <br> (only for non-list lines to avoid double spacing)
        # Replacing \n with <br> globally might break list HTML structure
        # Simplified approach: Just use replace, but <ul>/<li> handle their own spacing usually.
        # However, we need to handle paragraphs.

        # Better strategy: if line is not HTML tag, append <br>
        final_lines = []
        for line in text.split('\n'):
            if line.strip().startswith('<'):
                final_lines.append(line)
            else:
                final_lines.append(line + "<br>")

        return "".join(final_lines)

    def _append_message(self, sender, text):
        color = "#6f42c1" if sender == "Lyra" else "#495057"
        # Force ALL messages to be Left Aligned
        align = "left"

        formatted_text = self._format_markdown_to_html(text)

        html = f"""
        <div style="margin-bottom: 15px; text-align: {align};">
            <span style="font-weight: bold; color: {color}; font-size: 14px;">{sender}</span><br>
            <div style="padding: 5px 0; font-size: 15px; line-height: 1.4;">
                {formatted_text}
            </div>
        </div>
        """
        self.chat_area.append(html)
        # Scroll to bottom
        sb = self.chat_area.verticalScrollBar()
        sb.setValue(sb.maximum())
