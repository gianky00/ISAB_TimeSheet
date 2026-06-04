"""Modulo Account Dialog."""

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from src.application.services.constants import Icons
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import FilterComboBox, IconButton, StandardInput
from src.gui.widgets.modern_button import ModernButton
from src.infrastructure.utils.helpers import get_asset_path, get_colored_icon


class AccountDialog(QDialog):
    """Dialog per aggiungere/modificare un account.

    Inizializza la classe.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
        username: str = "",
        password: str = "",  # nosec B107
        account_type: str = "",
        show_type: bool = False,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Account")
        self.setFixedWidth(350)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self._apply_dialog_style()

        # Main Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        self._setup_form(main_layout, username, password, account_type, show_type)
        self._setup_buttons(main_layout)

    def _apply_dialog_style(self) -> None:
        """Applica lo stile QSS al dialogo."""
        self.setStyleSheet(f"""
      QDialog {{
        background-color: {COLORS["bg_white"]};
        border-radius: 12px;
      }}
      QLabel {{
        color: {COLORS["text_dark"]};
        font-weight: 500;
        font-size: 13px;
      }}
    """)

    def _setup_form(
        self, layout: QVBoxLayout, username: str, password: str, account_type: str, show_type: bool
    ) -> None:
        """Configura il form con i campiùdi input."""
        form = QFormLayout()
        form.setSpacing(10)

        # Username
        self.username_edit = StandardInput(username)
        self.username_edit.setMinimumHeight(35)
        form.addRow("Username:", self.username_edit)

        # Password logic
        self._setup_password_field(form, password)

        # Account Type (Optional)
        self.type_combo = FilterComboBox()
        self.type_combo.addItems(["Esecutore", "ISAB"])
        self.type_combo.setMinimumHeight(35)
        if account_type:
            self.type_combo.setCurrentText(account_type)

        if not show_type:
            self.type_combo.hide()
        else:
            form.addRow("Tipo Account:", self.type_combo)

        layout.addLayout(form)

    def _setup_password_field(self, form: QFormLayout, password: str) -> None:
        """Configura il campo password con il pulsante di visibilit ."""
        self.password_edit = StandardInput(password)
        self.password_edit.setMinimumHeight(35)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        pass_layout = QHBoxLayout()
        pass_layout.setContentsMargins(0, 0, 0, 0)
        pass_layout.setSpacing(5)
        pass_layout.addWidget(self.password_edit)

        self.toggle_pass_btn = IconButton()
        self.toggle_pass_btn.setIcon(get_colored_icon(get_asset_path(Icons.EYE), COLORS["text_muted"]))
        self.toggle_pass_btn.setIconSize(QSize(20, 20))
        self.toggle_pass_btn.setToolTip("Mostra/Nascondi password")
        self.toggle_pass_btn.setFixedSize(35, 35)
        self.toggle_pass_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_pass_btn.setStyleSheet(f"""
      QPushButton {{
        background-color: {COLORS["bg_white"]};
        border: 1px solid {COLORS["border_medium"]};
        border-radius: 4px;
      }}
      QPushButton:hover {{
        background-color: {COLORS["bg_light"]};
        border-color: {COLORS["border_dark"]};
      }}
    """)

        self.toggle_pass_btn.clicked.connect(self._toggle_password_visibility)
        pass_layout.addWidget(self.toggle_pass_btn)

        form.addRow("Password:", pass_layout)

    def _setup_buttons(self, layout: QVBoxLayout) -> None:
        """Configura i pulsanti di conferma/annullamento."""
        btns = QHBoxLayout()
        btns.setSpacing(10)
        btns.addStretch()

        cancel_btn = ModernButton("Annulla", variant=ModernButton.Variant.GHOST)
        cancel_btn.clicked.connect(self.reject)

        ok_btn = ModernButton("Salva", variant=ModernButton.Variant.PRIMARY)
        ok_btn.clicked.connect(self.accept)

        btns.addWidget(cancel_btn)
        btns.addWidget(ok_btn)
        layout.addLayout(btns)

    def _toggle_password_visibility(self) -> None:
        if self.password_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_pass_btn.setIcon(get_colored_icon(get_asset_path(Icons.LOCK), COLORS["text_muted"]))
            self.toggle_pass_btn.setToolTip("Nascondi password")
        else:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_pass_btn.setIcon(get_colored_icon(get_asset_path(Icons.EYE), COLORS["text_muted"]))
            self.toggle_pass_btn.setToolTip("Mostra password")

    def get_data(self) -> tuple[str, str, str]:
        """Restituisce (username, password, type)."""
        return (
            self.username_edit.text(),
            self.password_edit.text(),
            self.type_combo.currentText(),
        )
