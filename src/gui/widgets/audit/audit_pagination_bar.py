from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

from src.gui.styles import COLORS
from src.gui.widgets.modern_button import ModernButton


class AuditPaginationBar(QWidget):
    """Barra di paginazione per l'Audit Log con stile Enterprise."""

    page_changed = pyqtSignal(int)  # offset (1 per next, -1 per prev)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 5)

        self.prev_btn = ModernButton(
            "PRECEDENTE", variant=ModernButton.Variant.GHOST, size=ModernButton.Size.SMALL
        )
        self.prev_btn.setEnabled(False)
        self.prev_btn.clicked.connect(lambda: self.page_changed.emit(-1))

        self.page_lbl = QLabel("PAGINA 1")
        self.page_lbl.setStyleSheet(
            f"font-weight: 800; color: {COLORS['text_muted']}; font-size: 11px; letter-spacing: 1px;"
        )
        self.page_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.next_btn = ModernButton(
            "SUCCESSIVA", variant=ModernButton.Variant.GHOST, size=ModernButton.Size.SMALL
        )
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(lambda: self.page_changed.emit(1))

        layout.addWidget(self.prev_btn)
        layout.addStretch()
        layout.addWidget(self.page_lbl)
        layout.addStretch()
        layout.addWidget(self.next_btn)

    def update_state(self, current_page: int, total_logs: int, page_size: int) -> None:
        """
        Aggiorna lo stato visivo della barra (label e abilitazione pulsanti).
        """
        total_pages = (total_logs + page_size - 1) // page_size
        if total_pages < 1:
            total_pages = 1

        disp = current_page + 1
        self.page_lbl.setText(f"PAGINA {disp} DI {total_pages} (TOTALE LOG: {total_logs})")
        self.prev_btn.setEnabled(current_page > 0)
        self.next_btn.setEnabled(disp < total_pages)

    def set_enabled(self, enabled: bool) -> None:
        """Abilita o disabilita i pulsanti della barra."""
        self.prev_btn.setEnabled(enabled)
        self.next_btn.setEnabled(enabled)
