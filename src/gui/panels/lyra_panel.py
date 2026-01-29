from io import StringIO
from pathlib import Path
from typing import Any, List, Optional

import markdown
import pandas as pd
from PyQt6.QtCore import QSize, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QColor
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.constants import Icons
from src.core.lyra_client import LyraClient
from src.core.secrets_manager import SecretsManager
from src.gui.widgets.message_bubble import MessageBubble
from src.utils.document_processor import DocumentProcessor
from src.utils.helpers import get_asset_path, get_colored_icon


# MessageBubble è stata estratta in src/gui/widgets/message_bubble.py


class LyraWorker(QThread):
    """
    Thread worker dedicato all'interazione con l'API di Lyra (Gemini).
    Gestisce l'invio della domanda, del contesto testuale e delle immagini in background.
    """

    finished = pyqtSignal(str)

    def __init__(
        self,
        api_key: str,
        question: str,
        context: str = "",
        images: Optional[List[Any]] = None,
    ):
        """
        Inizializza il worker.

        Args:
            api_key: Chiave API per l'autenticazione.
            question: Testo della domanda dell'utente.
            context: Contesto aggiuntivo estratto dai documenti.
            images: Lista di immagini (pagine PDF convertite) da inviare.
        """
        super().__init__()
        self.api_key = api_key
        self.question = question
        self.context = context
        self.images = images or []

    def run(self):
        """Esegue la chiamata all'API e segnala la risposta finale."""
        try:
            if not self.api_key:
                self.finished.emit(
                    "Errore critico: Chiave API Gemini non trovata. Configurala nelle Impostazioni."
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
            self.finished.emit(
                f"Errore critico nel Worker di Lyra:\n{str(e)}\n\n{error_details}"
            )


class ModelListWorker(QThread):
    """
    Thread worker per il recupero asincrono della lista dei modelli disponibili.
    """

    finished = pyqtSignal(list)

    def __init__(self, api_key: str):
        """Inizializza il worker con la chiave API."""
        super().__init__()
        self.api_key = api_key

    def run(self):
        """Recupera la lista dei modelli dal client Lyra."""
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
    """
    Pannello dell'interfaccia utente per l'assistente IA Lyra.
    Fornisce una chat interattiva, supporto per allegati PDF,
    e strumenti di esportazione dati.
    """

    def __init__(self, parent=None):
        """Inizializza l'interfaccia e avvia il caricamento dei modelli."""
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
        """Configura tutti i widget dell'interfaccia utente (header, chat, input)."""
        layout = QVBoxLayout(self)

        # Header
        header = QFrame()
        header.setStyleSheet(
            "background-color: #6f42c1; border-radius: 8px; padding: 10px 15px;"
        )
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Lyra AI")
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
        refresh_models_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.REFRESH), "#000000")
        )
        refresh_models_btn.setFixedSize(32, 32)
        refresh_models_btn.setIconSize(QSize(18, 18))
        refresh_models_btn.setToolTip("Aggiorna lista modelli")
        refresh_models_btn.setStyleSheet(
            "QPushButton { background-color: transparent; border: none; }"
        )
        refresh_models_btn.clicked.connect(self._fetch_models)
        h_layout.addWidget(refresh_models_btn)

        sub = QLabel("Esperta Contabile")
        sub.setStyleSheet(
            "color: rgba(255,255,255,0.8); margin-left: 10px;"
        )  # Added margin for spacing
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

        # Chat History - Now a Scroll Area for Bubbles
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.chat_scroll.setStyleSheet(
            "background-color: white; border: 1px solid #dee2e6; border-radius: 8px;"
        )

        self.chat_container = QWidget()
        self.chat_container.setStyleSheet("background-color: white;")
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(5, 10, 5, 10)
        self.chat_layout.setSpacing(5)
        self.chat_layout.addStretch()

        self.chat_scroll.setWidget(self.chat_container)
        layout.addWidget(self.chat_scroll)

        # Tool Bar for Table Actions
        self.table_actions_layout = QHBoxLayout()
        self.table_actions_layout.setContentsMargins(0, 5, 0, 5)
        self.btn_export_last_table = QPushButton("Esporta ultima tabella Excel")
        self.btn_export_last_table.setIcon(
            get_colored_icon(get_asset_path(Icons.BAR_CHART), "#000000")
        )
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
        self.att_label = QLabel("Documento allegato: nome_file.pdf")
        self.att_label.setStyleSheet("color: #4b2c85; font-weight: bold; border: none;")
        att_layout.addWidget(self.att_label)

        att_layout.addStretch()

        self.btn_remove_att = QPushButton()
        self.btn_remove_att.setIcon(
            get_colored_icon(get_asset_path(Icons.X_CIRCLE), "#000000")
        )
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
            (
                "Sintesi PDF",
                "Dammi un breve riepilogo del contenuto di questo documento.",
            ),
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

        self.attach_btn = QPushButton()
        self.attach_btn.setIcon(
            get_colored_icon(get_asset_path(Icons.PLUS), "#000000")
        )  # Use PLUS as a placeholder for attach
        self.attach_btn.setFixedSize(45, 45)
        self.attach_btn.setIconSize(QSize(24, 24))
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
            "Lyra",
            "Ciao! Sono pronta ad analizzare i tuoi dati e i tuoi documenti. Cosa vuoi sapere oggi?",
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
        if (
            model_name
            and "Caricamento" not in model_name
            and "mancante" not in model_name
        ):
            config_manager.set_config_value("ai_model", model_name)

    def _populate_models_dropdown(self, models):
        """Popola il menu a discesa con i modelli AI filtrati e ordinati."""
        self.model_combo.blockSignals(True)
        self.model_combo.clear()

        if not models:
            self.model_combo.addItem("Nessun modello trovato")
            self.model_combo.setEnabled(False)
            self.model_combo.blockSignals(False)
            return

        ordered_models = self._sort_ai_models(models)
        self.model_combo.addItems(ordered_models)

        # Selezione automatica
        saved_model = config_manager.get_config_value("ai_model", "")
        if saved_model in ordered_models:
            self.model_combo.setCurrentText(saved_model)
        else:
            self.model_combo.setCurrentIndex(0)

        self.model_combo.setEnabled(True)
        self.model_combo.blockSignals(False)

    def _sort_ai_models(self, models: list) -> list:
        """Ordina i modelli per priorità: Pro -> Flash -> Others."""
        pro = sorted([m for m in models if "pro" in m], reverse=True)
        flash = sorted([m for m in models if "flash" in m], reverse=True)
        others = sorted([m for m in models if "pro" not in m and "flash" not in m])
        return pro + flash + others

    def _attach_file(self):
        """Apre un dialogo per selezionare e allegare un file PDF o immagine."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Allega Documento", "", "Documenti (*.pdf *.png *.jpg)"
        )
        if file_path:
            self._handle_file(file_path)

    def _handle_file(self, file_path):
        """Processa il file selezionato e prepara le immagini per il worker."""
        p = Path(file_path)
        if p.suffix.lower() == ".pdf":
            self.attached_file = p
            self.att_label.setText(f"PDF allegato: {p.name}")
            self.attachment_frame.setVisible(True)

            # Pre-processing: converts PDF to images for better OCR if needed
            # Or just send text if searchable. LyraClient will handle.
            # For now, let's prepare images to be safe (Vision is better for tables)
            self.attached_images = DocumentProcessor.get_pages_as_images(p)

            # Automatic prompt suggestion
            self.input_field.setText(
                "Analizza questo documento ed estrai i dati principali in una tabella."
            )
            self.input_field.setFocus()
        else:
            QMessageBox.warning(
                self,
                "Formato non supportato",
                "Lyra al momento analizza solo file PDF.",
            )

    def _remove_attachment(self):
        """Rimuove l'allegato corrente e nasconde la barra delle info."""
        self.attached_file = None
        self.attached_images = []
        self.attachment_frame.setVisible(False)

    def dragEnterEvent(self, event):
        """Gestisce l'ingresso di un file trascinato nel pannello."""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        """Gestisce il rilascio di un file trascinato nel pannello."""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self._handle_file(file_path)

    def _set_input(self, text):
        """Imposta il testo nell'input field."""
        self.input_field.setText(text)
        self.input_field.setFocus()

    def _send_message(self):
        """Prepara e invia il messaggio all'IA."""
        text = self.input_field.text().strip()
        if not text and not self.attached_file:
            return

        self.ask_lyra(text)
        self.input_field.clear()

    def ask_lyra(self, question: str, context: str = ""):
        """
        Avvia una richiesta a Lyra gestendo l'UI e il thread worker.

        Args:
            question: La domanda dell'utente.
            context: Testo opzionale per arricchire la richiesta.
        """
        self._append_message("Tu", question)

        final_images = self.attached_images.copy()

        if self.attached_file:
            self._append_message(
                "Sistema", f"<i>[Documento allegato: {self.attached_file.name}]</i>"
            )
            # If the PDF is text-searchable, we can also append the text to context
            if DocumentProcessor.is_pdf_searchable(self.attached_file):
                pdf_text = DocumentProcessor.extract_text(self.attached_file)
                context += f"\n\nCONTENUTO TESTUALE DOCUMENTO:\n{pdf_text}\n"

        self.input_field.setDisabled(True)
        self.attach_btn.setDisabled(True)
        self.chat_scroll.setFocus()

        # Preleva la chiave API nel thread principale e la passa al worker
        api_key = SecretsManager.get_gemini_api_key()

        self.worker = LyraWorker(api_key, question, context, final_images)
        self.worker.finished.connect(self._on_answer)
        self.worker.start()

        # NON rimuovere l'allegato automaticamente, permetti domande di follow-up

    def _on_answer(self, text):
        """Callback eseguito quando l'IA restituisce la risposta."""
        self._append_message("Lyra", text)
        self.input_field.setDisabled(False)
        self.attach_btn.setDisabled(False)
        self.input_field.setFocus()

    def _append_message(self, sender, text):
        """Aggiunge un messaggio alla cronologia della chat usando le bolle."""
        is_lyra = sender == "Lyra"
        bubble = MessageBubble(sender, text, is_lyra=is_lyra)

        # Inserisce prima dello stretch finale
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)

        # Scroll to bottom
        QApplication.processEvents()
        sb = self.chat_scroll.verticalScrollBar()
        sb.setValue(sb.maximum())

        # Check for tables in the text to enable export
        if "<table>" in markdown.markdown(text, extensions=["tables"]):
            self.last_table_data = text
            self.btn_export_last_table.setVisible(True)

    def _export_chat(self):
        """Mostra il menu per esportare la chat in PDF o l'ultima tabella in Excel."""
        menu = QMenu(self)

        pdf_action = QAction("Esporta come PDF", self)
        pdf_action.setIcon(get_colored_icon(get_asset_path(Icons.FILE_TEXT), "#000000"))
        pdf_action.triggered.connect(self._export_pdf)
        menu.addAction(pdf_action)

        excel_action = QAction("Esporta ultima tabella (Excel)", self)
        excel_action.setIcon(
            get_colored_icon(get_asset_path(Icons.BAR_CHART), "#000000")
        )
        excel_action.triggered.connect(self._export_excel)
        menu.addAction(excel_action)

        # Use sender to position
        sender = self.sender()
        if sender:
            # Calculate position below the button
            pos = sender.mapToGlobal(sender.rect().bottomLeft())
            menu.exec(pos)

    def _export_pdf(self):
        """Esporta l'intera cronologia della chat come file PDF."""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Salva Chat PDF", "chat_lyra.pdf", "PDF Files (*.pdf)"
        )
        if filename:
            try:
                # Per esportare i widget bolla dobbiamo creare un documento temporaneo
                from PyQt6.QtGui import QTextDocument
                from PyQt6.QtPrintSupport import QPrinter

                doc = QTextDocument()
                html_content = "<h1>Cronologia Chat Lyra AI</h1>"

                for i in range(self.chat_layout.count()):
                    widget = self.chat_layout.itemAt(i).widget()
                    if isinstance(widget, MessageBubble):
                        # Trova la label del messaggio
                        sender = widget.findChild(QLabel).text()
                        # Questo è un po' hacky, ma cerchiamo la seconda label (il messaggio)
                        labels = widget.findChildren(QLabel)
                        if len(labels) >= 2:
                            msg_html = labels[1].text()
                            html_content += (
                                f"<p><b>{sender}</b>:< br>{msg_html}</p><hr>"
                            )

                doc.setHtml(html_content)

                printer = QPrinter(QPrinter.PrinterMode.HighResolution)
                printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
                printer.setOutputFileName(filename)

                doc.print(printer)
                QMessageBox.information(
                    self, "Successo", "Chat esportata correttamente!"
                )
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Errore",
                    f"Impossibile esportare in PDF: {e}",
                )

    def _export_excel(self):
        """Esporta l'ultima tabella trovata nella cronologia chat in Excel."""
        if not self.last_table_data:
            QMessageBox.warning(
                self, "Nessuna tabella", "Non ho trovato tabelle recenti da esportare."
            )
            return

        table_lines = self._extract_table_lines(self.last_table_data)
        if not table_lines:
            QMessageBox.warning(
                self, "Nessuna tabella", "Non ho trovato tabelle valide nel messaggio."
            )
            return

        try:
            df = self._parse_markdown_table(table_lines)
            self._save_df_to_excel(df)
        except Exception as e:
            QMessageBox.critical(
                self, "Errore", f"Impossibile esportare la tabella: {e}"
            )

    def _extract_table_lines(self, text: str) -> List[str]:
        """Estrae le linee che compongono una tabella Markdown."""
        lines = text.split("\n")
        table_lines = []
        current_block = []

        for line in lines:
            if line.strip().startswith("|"):
                current_block.append(line)
            else:
                if len(current_block) >= 2:
                    table_lines = current_block
                current_block = []

        return current_block if len(current_block) >= 2 else table_lines

    def _parse_markdown_table(self, table_lines: List[str]) -> pd.DataFrame:
        """Parsa le linee Markdown in un DataFrame pandas."""
        cleaned = [line for line in table_lines if "---" not in line]
        data = StringIO("\n".join(cleaned))
        df = pd.read_csv(data, sep="|", header=0, engine="python")

        # Pulizia colonne e spazi
        df = df.dropna(axis=1, how="all")
        df.columns = df.columns.str.strip()
        # Usa apply su ogni colonna per strippare stringhe, garantendo il ritorno di un DataFrame
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].str.strip()
        return df

    def _save_df_to_excel(self, df: pd.DataFrame):
        """Mostra il dialog di salvataggio e scrive il file Excel."""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Salva Tabella Excel", "analisi_lyra.xlsx", "Excel Files (*.xlsx)"
        )
        if filename:
            df.to_excel(filename, index=False)
            QMessageBox.information(
                self, "Successo", "Tabella esportata correttamente!"
            )
