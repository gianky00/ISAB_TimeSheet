from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from src.gui.widgets.modern_button import ModernButton


class StandardInputDialog(QDialog):
    """
    Dialog standard per l'input di testo singolo.
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

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        if label:
            lbl = QLabel(label)
            lbl.setStyleSheet("font-size: 14px; color: #333;")
            layout.addWidget(lbl)

        self.input_field = QLineEdit(text)
        self.input_field.setMinimumHeight(35)
        self.input_field.setStyleSheet(
            """
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #0d6efd;
            }
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
        """Metodo statico di utilità simile a QInputDialog.getText."""
        dlg = StandardInputDialog(parent, title, label, text)
        result = dlg.exec()
        return dlg.get_text(), result == QDialog.DialogCode.Accepted
