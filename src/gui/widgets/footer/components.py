"""
SyncroJob - Footer UI Components
Collezione di widget e componenti grafici utilizzati per comporre la barra di stato (footer).
"""

from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QEnterEvent, QMouseEvent
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QWidget,
)

from src.gui.styles import COLORS


class FooterItemWidget(QWidget):
    """
    Elemento informativo composto da un tag (etichetta) e un valore.
    Usato per visualizzare metadati semplici nel footer.
    """

    def __init__(
        self, label: str, value: str = "", color: str | None = None, parent: QWidget | None = None
    ) -> None:
        """
        Inizializza l'elemento del footer.

        Args:
            label: Etichetta del dato.
            value: Valore iniziale.
            color: Colore dell'etichetta (default: text_muted).
            parent: Widget genitore.
        """
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)
        self.lbl_tag = QLabel(label)
        accent = color or COLORS["text_muted"]
        self.lbl_tag.setStyleSheet(
            f"color: {accent}; font-weight: bold; font-size: 11px; background: transparent;"
        )
        layout.addWidget(self.lbl_tag)
        self.lbl_val = QLabel(value)
        self.lbl_val.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 11px; background: transparent;")
        layout.addWidget(self.lbl_val)

    def set_text(self, text: str) -> None:
        """
        Aggiorna il testo del valore.

        Args:
            text: Nuovo testo da visualizzare.
        """
        self.lbl_val.setText(text)


class StartupConsole(QLabel):
    """
    Console per log di sistema nel footer (FASE 1: Boot).
    Visualizza i messaggi di inizializzazione durante l'avvio dell'applicazione.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza la console di startup.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.setText("Sistema Operativo Pronto")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-family: 'Segoe UI Semibold'; font-size: 10px; padding: 0 15px; background: transparent;"
        )
        self._log_queue: list[tuple[str, bool]] = []

    def log(self, message: str, is_error: bool = False) -> None:
        """
        Invia un messaggio alla console del footer.

        Args:
            message: Testo del log.
            is_error: Se True, visualizza il messaggio in rosso.
        """
        color = COLORS["error_red"] if is_error else COLORS["text_dark"]
        self.setText(message)
        self.setStyleSheet(
            f"color: {color}; font-family: 'Consolas', monospace; font-size: 13px; padding: 0 10px;"
        )
        self._log_queue.append((message, is_error))
        if len(self._log_queue) > 100:
            self._log_queue.pop(0)


class ClickableLabel(QLabel):
    """
    Label interattiva con effetti hover e segnale di click.
    Utilizzata per i dati del footer che richiedono un'azione (es. cambio account).
    """

    clicked = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza la label cliccabile.

        Args:
            parent: Widget genitore.
        """
        super().__init__(parent)
        self._base_style = ""
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def setBaseStyle(self, style: str) -> None:
        """
        Imposta lo stile base CSS.

        Args:
            style: Stringa di stili CSS.
        """
        self._base_style = style
        self.setStyleSheet(style)

    def enterEvent(self, event: QEnterEvent | None) -> None:
        """Gestisce l'evento hover-in cambiando lo sfondo."""
        self.setStyleSheet(
            self._base_style
            + f" background-color: {COLORS['bg_hover']}; border-radius: 3px; padding: 2px 4px;"
        )
        super().enterEvent(event)

    def leaveEvent(self, event: Any | None) -> None:
        """Gestisce l'evento hover-out ripristinando lo stile base."""
        self.setStyleSheet(self._base_style)
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        """Gestisce il click del mouse emettendo il segnale 'clicked'."""
        if event and event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class StatsCard(QFrame):
    """
    Widget card per la visualizzazione di una singola metrica statistica nel footer espandibile.
    """

    def __init__(self, title: str, value: str, icon: Any, parent: QWidget | None = None) -> None:
        """
        Inizializza la card statistica.

        Args:
            title: Titolo della metrica.
            value: Valore della metrica.
            icon: Icona associata.
            parent: Widget genitore.
        """
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
