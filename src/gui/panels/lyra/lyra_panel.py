import os
from io import StringIO
from pathlib import Path

import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.constants import URLs
from src.core.secrets_manager import SecretsManager
from src.gui.styles import COLORS
from src.utils.document_processor import DocumentProcessor

from .chat_area import ChatArea
from .header import LyraHeader
from .input_bar import ChatInputBar
from .workers import LyraWorker, ModelListWorker


class LyraPanel(QWidget):
    """Pannello principale coordinatore per Lyra AI."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model_worker: ModelListWorker | None = None
        self.worker: LyraWorker | None = None
        self.last_table_data = None
        self.attached_file = None
        self.attached_images = []
        self.setAcceptDrops(True)
        self._setup_ui()
        self._fetch_models()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # 1. Header
        self.header = LyraHeader()
        self.header.refresh_models_clicked.connect(self._fetch_models)
        self.header.export_chat_clicked.connect(self._export_chat)
        self.header.model_changed.connect(self._on_model_changed)
        layout.addWidget(self.header)

        # 2. Chat Area
        self.chat_area = ChatArea()
        self.chat_area.table_detected.connect(self._on_table_detected)
        layout.addWidget(self.chat_area)

        # 3. Table Export Toolbar (Hidden)
        self.table_toolbar = QWidget()
        self.table_toolbar.setVisible(False)
        tb_layout = QHBoxLayout(self.table_toolbar)
        self.btn_export_table = QPushButton("Esporta ultima tabella Excel")
        self.btn_export_table.setStyleSheet(
            f"background-color: {COLORS['success_dark']}; color: white; padding: 5px 10px; font-weight: bold; border-radius: 4px;"
        )
        self.btn_export_table.clicked.connect(self._export_excel)
        tb_layout.addWidget(self.btn_export_table)
        tb_layout.addStretch()
        layout.addWidget(self.table_toolbar)

        # 4. Attachment Frame (Hidden)
        self.attachment_frame = QFrame()
        self.attachment_frame.setVisible(False)
        self.attachment_frame.setStyleSheet(
            f"background-color: {COLORS['bg_alt']}; border: 1px dashed {COLORS['purple']}; border-radius: 6px; margin-bottom: 5px;"
        )
        att_layout = QHBoxLayout(self.attachment_frame)
        self.att_label = QLabel("")
        self.att_label.setStyleSheet(f"color: {COLORS['purple_deep']}; font-weight: bold;")
        att_layout.addWidget(self.att_label)
        att_layout.addStretch()
        btn_remove = QPushButton("X")
        btn_remove.setFixedSize(20, 20)
        btn_remove.clicked.connect(self._remove_attachment)
        att_layout.addWidget(btn_remove)
        layout.addWidget(self.attachment_frame)

        # 5. Quick Actions
        actions_widget = self._create_quick_actions()
        layout.addWidget(actions_widget)

        # 6. Input Bar
        self.input_bar = ChatInputBar()
        self.input_bar.send_clicked.connect(self.ask_lyra)
        self.input_bar.attach_clicked.connect(self._attach_file)
        layout.addWidget(self.input_bar)

        self.chat_area.append_message(
            "Lyra",
            "Ciao! Sono pronta ad analizzare i tuoi dati e i tuoi documenti. Cosa vuoi sapere oggi?",
        )

    def _create_quick_actions(self):
        w = QWidget()
        layout = QHBoxLayout(w)
        layout.setContentsMargins(20, 0, 20, 0)
        actions = [
            (
                "Estrai Tabella Giornaliere",
                "Analizza il documento allegato ed estrai i dati in una tabella Markdown.",
            ),
            (
                "Trova Anomalie",
                "Verifica se ci sono incongruenze nel documento allegato.",
            ),
            ("Sintesi PDF", "Dammi un breve riepilogo del contenuto."),
        ]
        for name, prompt in actions:
            btn = QPushButton(name)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    border: 1px solid {COLORS['purple']};
                    border-radius: 15px;
                    padding: 6px 15px;
                    font-size: 11px;
                    font-weight: 600;
                    color: {COLORS['purple']};
                    background: transparent;
                }}
                QPushButton:hover {{
                    background: {COLORS['purple']}10;
                }}
                """
            )
            btn.clicked.connect(lambda _, p=prompt: self.input_bar.input_field.setText(p))
            layout.addWidget(btn)
        layout.addStretch()
        w.setFixedHeight(40)
        return w

    def _fetch_models(self):
        if self.model_worker and self.model_worker.isRunning():
            return

        provider = config_manager.get_config_value("ai_provider", "gemini")
        api_key = SecretsManager.get_gemini_api_key()
        ollama_url = config_manager.get_config_value("ollama_url", URLs.OLLAMA_DEFAULT)

        # Se è gemini e manca la chiave, non possiamo fare nulla
        if provider == "gemini" and not api_key:
            return

        self.model_worker = ModelListWorker(api_key, provider=provider, ollama_url=ollama_url)
        self.model_worker.finished.connect(self._populate_models)
        self.model_worker.start()

    def _populate_models(self, models):
        self.header.model_combo.clear()
        if not models:
            return
        ordered = sorted(models, reverse=True)  # Semplificato
        self.header.model_combo.addItems(ordered)
        saved = config_manager.get_config_value("ai_model", "")
        if saved in ordered:
            self.header.model_combo.setCurrentText(saved)

    def _on_model_changed(self, name):
        if name:
            config_manager.set_config_value("ai_model", name)

    def _on_table_detected(self, text):
        self.last_table_data = text
        self.table_toolbar.setVisible(True)

    def _attach_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Allega PDF", "", "Documenti (*.pdf)")
        if file_path:
            self._handle_file(file_path)

    def _handle_file(self, file_path):
        p = Path(file_path)
        self.attached_file = p
        self.att_label.setText(f"Allegato: {p.name}")
        self.attachment_frame.setVisible(True)
        self.attached_images = DocumentProcessor.get_pages_as_images(p)
        self.input_bar.input_field.setText("Analizza questo documento.")

    def _remove_attachment(self):
        self.attached_file = None
        self.attached_images = []
        self.attachment_frame.setVisible(False)

    def ask_lyra(self, question: str):
        """Invia una domanda all'assistente AI Lyra, includendo eventuali allegati e contesto PDF."""
        if self.worker and self.worker.isRunning():
            return

        self.chat_area.append_message("Tu", question)

        # Feedback visivo immediato (Nuovo indicatore animato)
        self.chat_area.set_typing(True)

        context = ""
        if self.attached_file and DocumentProcessor.is_pdf_searchable(self.attached_file):
            context = DocumentProcessor.extract_text(self.attached_file)

        self.input_bar.set_enabled(False)

        provider = config_manager.get_config_value("ai_provider", "gemini")
        api_key = SecretsManager.get_gemini_api_key()
        ollama_url = config_manager.get_config_value("ollama_url", URLs.OLLAMA_DEFAULT)
        model = config_manager.get_config_value("ai_model", "")

        if provider == "gemini" and not api_key:
            self.chat_area.append_message(
                "Lyra", "⚠️ Errore: Chiave API Gemini non configurata nelle impostazioni."
            )
            self.input_bar.set_enabled(True)
            return

        self.worker = LyraWorker(
            api_key=api_key,
            question=question,
            context=context,
            images=self.attached_images,
            provider=provider,
            model_name=model,
            ollama_url=ollama_url,
        )
        self.worker.finished.connect(self._on_answer)
        self.worker.start()

    def _on_answer(self, text):
        self.chat_area.set_typing(False)
        self.chat_area.append_message("Lyra", text)
        self.input_bar.set_enabled(True)

    def dragEnterEvent(self, event):
        """Accetta l'evento di drag se contiene URL (file)."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Gestisce il rilascio di un file PDF nell'area chat per l'analisi."""
        urls = event.mimeData().urls()
        if urls:
            self._handle_file(urls[0].toLocalFile())

    def _export_chat(self):
        # Logica export semplificata o portata dal vecchio file se necessario
        pass

    def _export_excel(self):
        if not self.last_table_data:
            return
        try:
            lines = self.last_table_data.split("\n")
            table_lines = [line for line in lines if "|" in line and "---" not in line]
            data = StringIO("\n".join(table_lines))
            df = pd.read_csv(data, sep="|", engine="python").dropna(axis=1, how="all")
            filename, _ = QFileDialog.getSaveFileName(self, "Salva Excel", "analisi.xlsx", "Excel (*.xlsx)")
            if filename:
                df.to_excel(filename, index=False)
                os.startfile(filename)  # noqa: S606
        except Exception as e:
            QMessageBox.warning(self, "Errore", str(e))
