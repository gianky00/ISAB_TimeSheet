"""
SyncroJob - Confirmation Dialog
Dialogo standard per le conferme (Sì/No) o messaggi importanti.
Sostituisce QMessageBox per mantenere uno stile coerente con il design d'élite del progetto.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path, get_colored_icon


class ConfirmationDialog(QDialog):
    """
    Dialogo versatile per conferme e avvisi.
    Supporta diverse varianti (INFO, WARNING, ERROR, QUESTION) con icone e colori tematici.
    """

    class Variant:
        """Costanti per definire la tipologia del messaggio."""

        INFO = "info"
        WARNING = "warning"
        ERROR = "error"
        QUESTION = "question"

    def __init__(
        self,
        parent: QWidget | None = None,
        title: str = "",
        message: str = "",
        variant: str = Variant.QUESTION,
        is_rich_text: bool = False,
    ) -> None:
        """
        Inizializza il dialogo di conferma.

        Args:
            parent: Widget genitore.
            title: Titolo della finestra.
            message: Messaggio da visualizzare.
            variant: Variante del dialogo (es. Variant.QUESTION).
            is_rich_text: Se True, abilita il rendering HTML (sanificato).
        """
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(380)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        # Forza stile Light a livello di Dialog
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS["bg_white"]};
                border: 1px solid {COLORS["border_medium"]};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)

        # Header con icona e messaggio
        header_layout = QHBoxLayout()
        header_layout.setSpacing(15)

        icon_label = QLabel()
        icon_path = self._get_icon_path(variant)
        icon_color = self._get_icon_color(variant)
        if icon_path:
            icon_label.setPixmap(get_colored_icon(icon_path, icon_color).pixmap(32, 32))
            icon_label.setFixedSize(32, 32)
            header_layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignTop)

        msg_label = QLabel()
        msg_label.setWordWrap(True)

        if is_rich_text:
            # Sanificazione minima per prevenire UI Injection/XSS
            safe_msg = self._sanitize_html(message)
            msg_label.setTextFormat(Qt.TextFormat.RichText)
            msg_label.setText(safe_msg)
        else:
            msg_label.setTextFormat(Qt.TextFormat.PlainText)
            msg_label.setText(message)

        msg_label.setStyleSheet(f"font-size: 14px; color: {COLORS['text_dark']};")
        header_layout.addWidget(msg_label, 1)

        layout.addLayout(header_layout)

        # Pulsanti
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
            self.btn_ok = ModernButton("OK", variant=ModernButton.Variant.PRIMARY)
            self.btn_ok.clicked.connect(self.accept)
            btn_layout.addWidget(self.btn_ok)

        layout.addLayout(btn_layout)

    def _get_icon_path(self, variant: str) -> str | None:
        """Restituisce il percorso dell'icona corrispondente alla variante."""
        if variant == self.Variant.INFO:
            return get_asset_path(Icons.INFO)
        if variant == self.Variant.WARNING:
            return get_asset_path(Icons.ALERT_TRIANGLE)
        if variant == self.Variant.ERROR:
            return get_asset_path(Icons.X_CIRCLE)
        if variant == self.Variant.QUESTION:
            return get_asset_path(Icons.HELP)
        return None

    def _get_icon_color(self, variant: str) -> str:
        """Restituisce il colore CSS corrispondente alla variante."""
        if variant == self.Variant.INFO:
            return COLORS["info_blue"]
        if variant == self.Variant.WARNING:
            return COLORS["warning_orange"]
        if variant == self.Variant.ERROR:
            return COLORS["error_red"]
        if variant == self.Variant.QUESTION:
            return COLORS["primary_dark"]
        return COLORS["text_dark"]

    def _sanitize_html(self, html: str) -> str:
        """Rimuove tag potenzialmente pericolosi (script, iframe, object) dall'HTML."""
        import re

        # Rimuove blocchi script completi
        clean = re.sub(r"<script.*?>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        # Rimuove tag singoli pericolosi
        clean = re.sub(
            r"<(script|iframe|object|embed|applet|meta|link|style).*?>",
            "",
            clean,
            flags=re.IGNORECASE,
        )
        # Rimuove attributi evento (onmouseover, onclick, etc)
        return re.sub(r"\son\w+?\s*=\s*['\"].*?['\"]", "", clean, flags=re.IGNORECASE)

    @staticmethod
    def confirm(parent: QWidget | None, title: str, message: str, is_rich_text: bool = False) -> bool:
        """
        Helper statico per mostrare rapidamente una richiesta di conferma Sì/No.

        Args:
            parent: Widget genitore.
            title: Titolo.
            message: Messaggio.
            is_rich_text: Se il messaggio contiene HTML.

        Returns:
            bool: True se l'utente ha confermato.
        """
        dlg = ConfirmationDialog(
            parent, title, message, variant=ConfirmationDialog.Variant.QUESTION, is_rich_text=is_rich_text
        )
        return dlg.exec() == QDialog.DialogCode.Accepted

    @staticmethod
    def show_info(parent: QWidget | None, title: str, message: str, is_rich_text: bool = False) -> None:
        """Mostra un messaggio informativo con pulsante OK."""
        dlg = ConfirmationDialog(
            parent, title, message, variant=ConfirmationDialog.Variant.INFO, is_rich_text=is_rich_text
        )
        dlg.exec()

    @staticmethod
    def show_warning(parent: QWidget | None, title: str, message: str, is_rich_text: bool = False) -> None:
        """Mostra un avviso con pulsante OK."""
        dlg = ConfirmationDialog(
            parent, title, message, variant=ConfirmationDialog.Variant.WARNING, is_rich_text=is_rich_text
        )
        dlg.exec()

    @staticmethod
    def show_error(parent: QWidget | None, title: str, message: str, is_rich_text: bool = False) -> None:
        """Mostra un messaggio di errore con pulsante OK."""
        dlg = ConfirmationDialog(
            parent, title, message, variant=ConfirmationDialog.Variant.ERROR, is_rich_text=is_rich_text
        )
        dlg.exec()
