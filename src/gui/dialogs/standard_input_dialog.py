"""Modulo Standard Input Dialog."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import StandardInput
from src.gui.widgets.modern_button import ModernButton


class StandardInputDialog(QDialog):
    """Dialog standard per l'input di testo singolo.

    Sostituisce QInputDialog per mantenere coerenza stilistica.
    """

    def __init__(
        self, parent: QWidget | None = None, title: str = "", label: str = "", text: str = ""
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedWidth(350)
        # Rimuovi pulsante aiuto
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        # Forza stile Light a livello di Dialog
        self.setStyleSheet(f"""
      QDialog {{
        background-color: {COLORS["bg_white"]};
        border: 1px solid {COLORS["border_medium"]};
      }}
    """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        if label:
            lbl = QLabel(label)
            lbl.setStyleSheet(f"font-size: 14px; color: {COLORS['text_dark']};")
            layout.addWidget(lbl)

        self.input_field = StandardInput(text)
        self.input_field.setMinimumHeight(35)
        self.input_field.setStyleSheet(
            f"""
      QLineEdit {{
        border: 1px solid {COLORS["border_medium"]};
        border-radius: 4px;
        padding: 5px;
        font-size: 14px;
        background-color: {COLORS["bg_white"]};
        color: {COLORS["text_dark"]};
      }}
      QLineEdit:focus {{
        border: 1px solid {COLORS["primary_dark"]};
      }}
      """
        )
        layout.addWidget(self.input_field)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addStretch()

        self.btn_cancel = ModernButton("Annulla", variant=ModernButton.Variant.GHOST)
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_ok = ModernButton("Salva", variant=ModernButton.Variant.PRIMARY)
        self.btn_ok.clicked.connect(self.accept)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_ok)

        layout.addLayout(btn_layout)

    def get_text(self) -> str:
        """Restituisce il testo inserito."""
        return self.input_field.text().strip()

    @staticmethod
    def get_input(parent: QWidget | None, title: str, label: str, text: str = "") -> tuple[str, bool]:
        """Metodo statico di utilit  simile a QInputDialog.getText."""
        dlg = StandardInputDialog(parent, title, label, text)
        result = dlg.exec()
        return dlg.get_text(), result == QDialog.DialogCode.Accepted
