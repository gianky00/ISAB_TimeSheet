from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from src.gui.styles import COLORS


class AuditPaginationBar(QWidget):
    """Barra di paginazione per l'Audit Log."""

    page_changed = pyqtSignal(int)  # offset (1 per next, -1 per prev)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.prev_btn = QPushButton("Precedente")
        self.prev_btn.setEnabled(False)
        self.prev_btn.clicked.connect(lambda: self.page_changed.emit(-1))

        self.page_lbl = QLabel("Pagina 1")
        self.page_lbl.setStyleSheet(f"font-weight: bold; color: {COLORS['text_dark']};")

        self.next_btn = QPushButton("Successiva")
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

        Args:
            current_page: Indice della pagina corrente (0-based).
            total_logs: Numero totale di log disponibili.
            page_size: Numero di log per pagina.
        """
        total_pages = (total_logs + page_size - 1) // page_size
        if total_pages < 1:
            total_pages = 1

        disp = current_page + 1
        self.page_lbl.setText(f"Pagina {disp} di {total_pages} (Tot: {total_logs})")
        self.prev_btn.setEnabled(current_page > 0)
        self.next_btn.setEnabled(disp < total_pages)

    def set_enabled(self, enabled: bool) -> None:
        """
        Abilita o disabilita i pulsanti di navigazione.

        Args:
            enabled: True per abilitare, False altrimenti.
        """
        self.prev_btn.setEnabled(enabled)
        self.next_btn.setEnabled(enabled)
