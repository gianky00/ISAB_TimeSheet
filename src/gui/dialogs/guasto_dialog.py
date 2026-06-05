"""SyncroJob - Dialog per la segnalazione guasti strumenti campione."""

from datetime import datetime

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.application.services.constants import TipoAnomalia
from src.gui.styles import COLORS
from src.gui.widgets.calendar_date_edit import CalendarDateEdit
from src.gui.widgets.core_widgets import PrimaryButton


class GuastoDialog(QDialog):
    """Dialog per la segnalazione o rimozione guasto di uno strumento campione."""

    def __init__(  # noqa: PLR0913
        self,
        id_coemi: str,
        matricola: str,
        modello: str,
        parent: QWidget | None = None,
        *,
        current_tipo: str = "",
        current_data: str = "",
        current_note: str = "",
        stato_dialog: int = 1,
    ) -> None:
        """Inizializza il dialog con i dati dello strumento.

        Args:
            id_coemi: Identificativo COEMI dello strumento.
            matricola: Matricola dello strumento.
            modello: Modello dello strumento.
            parent: Widget genitore opzionale.
            current_tipo: Tipo anomalia corrente (per modifica).
            current_data: Data rilevamento corrente (per modifica).
            current_note: Note correnti (per modifica).
            stato_dialog: 1 per Guasto, 2 per Controllo, 3 per Dismesso.
        """
        super().__init__(parent)
        self.id_coemi = id_coemi
        self.matricola = matricola
        self.modello = modello
        self.stato_dialog = stato_dialog
        self._result_data: dict[str, str] = {}
        self._setup_ui(current_tipo, current_data, current_note)

    def _setup_ui(self, current_tipo: str, current_data: str, current_note: str) -> None:  # noqa: PLR0915, PLR0912, C901
        """Configura l'interfaccia del dialog.

        Args:
            current_tipo: Tipo anomalia preimpostato.
            current_data: Data rilevamento preimpostata.
            current_note: Note preimpostate.
        """
        if self.stato_dialog == 2:
            self.setWindowTitle("Valutazione Tecnica")
            header_text = "🔍 In Valutazione Tecnica"
            header_color = "#DAA520"  # GoldenRod / Orange
        elif self.stato_dialog == 3:
            self.setWindowTitle("Dismetti Strumento")
            header_text = "🚫 Segnala Strumento Dismesso"
            header_color = COLORS["text_muted"]
        else:
            self.setWindowTitle("Segnala Guasto Strumento")
            header_text = "⚠️ Segnala Guasto Strumento"
            header_color = COLORS["error_red"]

        self.setMinimumWidth(480)
        self.setStyleSheet(f"QDialog {{ background-color: {COLORS['bg_white']}; }}")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)

        # Header
        header = QLabel(header_text)
        header.setStyleSheet(
            f"color: {header_color}; font-size: 18px; font-weight: bold; padding-bottom: 5px;"
        )
        layout.addWidget(header)

        # Form
        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        label_style = f"color: {COLORS['text_dark']}; font-size: 13px; font-weight: 600;"
        readonly_style = (
            f"background-color: {COLORS['bg_alt']}; border: 1px solid {COLORS['border_light']}; "
            f"border-radius: 6px; padding: 8px; color: {COLORS['text_muted']}; font-size: 13px;"
        )
        input_style = (
            f"border: 1px solid {COLORS['border_medium']}; border-radius: 6px; "
            f"padding: 8px; font-size: 13px; background-color: {COLORS['bg_white']}; "
            f"color: {COLORS['text_dark']};"
        )

        # Campi readonly
        for label_text, value in [
            ("ID COEMI", self.id_coemi),
            ("Matricola", self.matricola),
            ("Modello", self.modello),
        ]:
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            field = QLineEdit(value)
            field.setReadOnly(True)
            field.setStyleSheet(readonly_style)
            form.addRow(lbl, field)

        # Tipo anomalia / controllo
        lbl_tipo = QLabel(
            "Motivo Valutazione"
            if self.stato_dialog == 2
            else "Motivo Dismissione"
            if self.stato_dialog == 3
            else "Tipo Anomalia"
        )
        lbl_tipo.setStyleSheet(label_style)
        self.combo_tipo = QComboBox()
        if self.stato_dialog == 2:
            self.combo_tipo.addItems(
                [
                    "Verifica pre-scadenza",
                    "Controllo visivo",
                    "Sospetta deriva misure",
                    "Misure instabili",
                    "Altro",
                ]
            )
        elif self.stato_dialog == 3:
            self.combo_tipo.addItems(
                [
                    "Dismissione definitiva",
                    "Furto/Smarrimento",
                    "Dismissione per obsolescenza",
                    "Vendita",
                    "Altro",
                ]
            )
        else:
            self.combo_tipo.addItems([t.value for t in TipoAnomalia])
        self.combo_tipo.setStyleSheet(input_style)
        if current_tipo:
            idx = self.combo_tipo.findText(current_tipo)
            if idx >= 0:
                self.combo_tipo.setCurrentIndex(idx)
        form.addRow(lbl_tipo, self.combo_tipo)

        # Data rilevamento
        lbl_data = QLabel("Data Rilevamento")
        lbl_data.setStyleSheet(label_style)
        self.date_edit = CalendarDateEdit()
        if current_data:
            try:
                dt = datetime.strptime(current_data, "%d/%m/%Y")  # noqa: DTZ007
                self.date_edit.setDate(QDate(dt.year, dt.month, dt.day))
            except ValueError:
                self.date_edit.setDate(QDate.currentDate())
        else:
            self.date_edit.setDate(QDate.currentDate())
        form.addRow(lbl_data, self.date_edit)

        # Note
        lbl_note = QLabel("Note")
        lbl_note.setStyleSheet(label_style)
        self.text_note = QPlainTextEdit()
        self.text_note.setPlaceholderText("Descrivi l'anomalia riscontrata...")
        # Remove padding from CSS to prevent Qt box-sizing bugs that squish text
        text_style = input_style.replace("padding: 8px;", "padding: 4px;")
        self.text_note.setStyleSheet(text_style + " min-height: 80px; line-height: 1.5;")
        self.text_note.setMaximumHeight(120)
        if current_note:
            self.text_note.setPlainText(current_note)
        form.addRow(lbl_note, self.text_note)

        layout.addLayout(form)
        layout.addSpacing(10)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancel = PrimaryButton("Annulla")
        btn_cancel.setStyleSheet(
            f"QPushButton {{ background-color: {COLORS['bg_alt']}; color: {COLORS['text_dark']}; "
            f"border: 1px solid {COLORS['border_medium']}; border-radius: 6px; padding: 10px 25px; font-size: 13px; }}"
            f"QPushButton:hover {{ background-color: {COLORS['bg_hover']}; }}"
        )
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)

        btn_layout.addSpacing(10)

        if self.stato_dialog == 2:
            btn_confirm = PrimaryButton("🔍 Imposta Valutazione")
        elif self.stato_dialog == 3:
            btn_confirm = PrimaryButton("🚫 Conferma Dismissione")
        else:
            btn_confirm = PrimaryButton("⚠️ Conferma Guasto")
        btn_confirm.setStyleSheet(
            f"QPushButton {{ background-color: {COLORS['error_red']}; color: white; "
            f"border: none; border-radius: 6px; padding: 10px 25px; font-weight: bold; font-size: 13px; }}"
            f"QPushButton:hover {{ background-color: #b91c1c; }}"
        )
        btn_confirm.clicked.connect(self._on_confirm)
        btn_layout.addWidget(btn_confirm)

        layout.addLayout(btn_layout)

    def _on_confirm(self) -> None:
        """Salva i dati e accetta il dialog."""
        self._result_data = {
            "guasto_tipo": self.combo_tipo.currentText(),
            "guasto_data": self.date_edit.date().toString("dd/MM/yyyy"),
            "guasto_note": self.text_note.toPlainText().strip(),
        }
        self.accept()

    def get_result(self) -> dict[str, str]:
        """Restituisce i dati del guasto inseriti dall'utente."""
        return self._result_data
