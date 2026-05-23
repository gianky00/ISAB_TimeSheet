"""SyncroJob - Legenda Colori OdA.

Widget compatto che spiega il significato dei colori visualizzati
nel Storico OdA (stato righe madri e figlie).
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from src.gui.styles import COLORS

_LEGEND_ITEMS: list[tuple[str, str, str]] = [
    (COLORS["bg_error_pastel"], COLORS["error_red"], "Cancellato"),
    (COLORS["bg_warning_pastel"], COLORS["warning_orange"], "In attesa di rilascio"),
    (COLORS["bg_white"], COLORS["text_muted"], "Normale / Rilasciato"),
]


class OdaLegendWidget(QWidget):
    """Barra legenda orizzontale con indicatori colorati per il Storico OdA.

    Mostra in forma compatta il significato cromatico delle righe padre.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza la legenda con gli item di default."""
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Costruisce la UI della legenda."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        prefix = QLabel("Legenda:")
        prefix.setStyleSheet(f"font-size: 11px; font-weight: 600; color: {COLORS['text_muted']};")
        layout.addWidget(prefix)

        for bg_color, border_color, label_text in _LEGEND_ITEMS:
            item = self._make_item(bg_color, border_color, label_text)
            layout.addWidget(item)

        layout.addStretch()

        self.setStyleSheet(
            f"""
            OdaLegendWidget {{
                background-color: {COLORS["bg_light"]};
                border: 1px solid {COLORS["border_light"]};
                border-radius: 6px;
            }}
            """
        )
        self.setFixedHeight(34)

    def _make_item(self, bg_color: str, border_color: str, text: str) -> QWidget:
        """Crea un singolo elemento legenda (quadratino colorato + etichetta).

        Args:
            bg_color: Colore di sfondo del quadratino.
            border_color: Colore del bordo del quadratino.
            text: Testo descrittivo dell'elemento.

        Returns:
            Un QWidget contenente l'indicatore colorato e il testo.
        """
        container = QWidget()
        row = QHBoxLayout(container)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(5)

        swatch = QLabel()
        swatch.setFixedSize(14, 14)
        swatch.setStyleSheet(
            f"""
            background-color: {bg_color};
            border: 1.5px solid {border_color};
            border-radius: 3px;
            """
        )

        label = QLabel(text)
        label.setStyleSheet(f"font-size: 11px; color: {COLORS['text_dark']};")

        row.addWidget(swatch)
        row.addWidget(label)
        return container
