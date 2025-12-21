"""
Bot TS - Lyra AI Panel
Interfaccia di chat per l'assistente IA.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from src.core.lyra_client import LyraClient

class LyraWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, question):
        super().__init__()
        self.question = question
        self.client = LyraClient()

    def run(self):
        answer = self.client.ask(self.question)
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

    def _send_message(self):
        text = self.input_field.text().strip()
        if not text: return

        self._append_message("Tu", text)
        self.input_field.clear()
        self.input_field.setDisabled(True)
        self.chat_area.setFocus() # Keep focus in window

        self.worker = LyraWorker(text)
        self.worker.finished.connect(self._on_answer)
        self.worker.start()

    def _on_answer(self, text):
        self._append_message("Lyra", text)
        self.input_field.setDisabled(False)
        self.input_field.setFocus()

    def _append_message(self, sender, text):
        color = "#6f42c1" if sender == "Lyra" else "#495057"
        align = "left" if sender == "Lyra" else "right"
        bg = "#f3f0ff" if sender == "Lyra" else "#e9ecef"

        # Converti newline in <br> per HTML
        formatted_text = text.replace('\n', '<br>')

        html = f"""
        <div style="margin-bottom: 10px; text-align: {align};">
            <span style="font-weight: bold; color: {color};">{sender}</span><br>
            <span style="background-color: {bg}; padding: 8px 12px; border-radius: 10px; display: inline-block;">
                {formatted_text}
            </span>
        </div>
        """
        self.chat_area.append(html)
        # Scroll to bottom
        sb = self.chat_area.verticalScrollBar()
        sb.setValue(sb.maximum())
