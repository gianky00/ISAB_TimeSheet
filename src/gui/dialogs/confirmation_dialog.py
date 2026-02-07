from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from src.core.constants import Icons
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path, get_colored_icon


class ConfirmationDialog(QDialog):
    """
    Dialog standard per le conferme (Sì/No) o messaggi importanti.
    Sostituisce QMessageBox.question/warning/information per mantenere lo stile.
    """

    class Variant:
        INFO = "info"
        WARNING = "warning"
        ERROR = "error"
        QUESTION = "question"

    def __init__(self, parent=None, title="", message="", variant=Variant.QUESTION):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(380)
        # Rimuovi pulsante aiuto
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)

        # Header con icona (Opzionale) o solo testo
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)

        icon_label = QLabel()
        icon_path = self._get_icon_path(variant)
        icon_color = self._get_icon_color(variant)
        if icon_path:
            icon_label.setPixmap(get_colored_icon(icon_path, icon_color).pixmap(32, 32))
            icon_label.setFixedSize(32, 32)
            header_layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignTop)

        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        msg_label.setTextFormat(Qt.TextFormat.RichText)
        msg_label.setStyleSheet("font-size: 14px; color: #333;")
        header_layout.addWidget(msg_label, 1)

        layout.addLayout(header_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_layout.addStretch()

        if variant == self.Variant.QUESTION:
            self.btn_cancel = ModernButton("Annulla", variant=ModernButton.Variant.GHOST)
            self.btn_cancel.clicked.connect(self.reject)
            btn_layout.addWidget(self.btn_cancel)

            self.btn_ok = ModernButton("Conferma", variant=ModernButton.Variant.PRIMARY)
            self.btn_ok.clicked.connect(self.accept)
            btn_layout.addWidget(self.btn_ok)
        else:
            # Info/Warning/Error usually have just OK
            self.btn_ok = ModernButton("OK", variant=ModernButton.Variant.PRIMARY)
            self.btn_ok.clicked.connect(self.accept)
            btn_layout.addWidget(self.btn_ok)

        layout.addLayout(btn_layout)

    def _get_icon_path(self, variant):
        if variant == self.Variant.INFO:
            return get_asset_path(Icons.INFO)
        if variant == self.Variant.WARNING:
            return get_asset_path(Icons.ALERT_TRIANGLE)
        if variant == self.Variant.ERROR:
            return get_asset_path(Icons.X_CIRCLE)
        if variant == self.Variant.QUESTION:
            return get_asset_path(Icons.HELP_CIRCLE)
        return None

    def _get_icon_color(self, variant):
        if variant == self.Variant.INFO:
            return "#0d6efd"
        if variant == self.Variant.WARNING:
            return "#fd7e14"
        if variant == self.Variant.ERROR:
            return "#dc3545"
        if variant == self.Variant.QUESTION:
            return "#0d6efd"
        return "#333"

    @staticmethod
    def confirm(parent, title, message) -> bool:
        """Helper statico per conferme."""
        dlg = ConfirmationDialog(parent, title, message, variant=ConfirmationDialog.Variant.QUESTION)
        return dlg.exec() == QDialog.DialogCode.Accepted

    @staticmethod
    def show_info(parent, title, message):
        dlg = ConfirmationDialog(parent, title, message, variant=ConfirmationDialog.Variant.INFO)
        dlg.exec()

    @staticmethod
    def show_warning(parent, title, message):
        dlg = ConfirmationDialog(parent, title, message, variant=ConfirmationDialog.Variant.WARNING)
        dlg.exec()

    @staticmethod
    def show_error(parent, title, message):
        dlg = ConfirmationDialog(parent, title, message, variant=ConfirmationDialog.Variant.ERROR)
        dlg.exec()
