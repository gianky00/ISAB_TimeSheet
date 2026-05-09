"""
SyncroJob - Footer Status Bar
Widget per la parte destra della barra di stato, contenente indicatori di progresso e stato dei portali.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from src.gui.styles import COLORS
from src.gui.widgets.animated_progress_bar import AnimatedProgressBar


class FooterRightWidget(QWidget):
    """
    Parte destra del footer: contiene la Progress Bar globale e le Status Cards dei Bot.
    Gestisce il passaggio tra la modalita' di caricamento e quella operativa.
    """

    def __init__(
        self, status_portale: QWidget, status_safework: QWidget, parent: QWidget | None = None
    ) -> None:
        """
        Inizializza il widget del footer destro.

        Args:
          status_portale: Widget che visualizza lo stato del portale ISAB.
          status_safework: Widget che visualizza lo stato del portale SafeWork.
          parent: Widget genitore.
        """
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 15, 0)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.progress_bar = AnimatedProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("0%")
        self.progress_label.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-family: 'Consolas', monospace; font-weight: bold; font-size: 13px;"
        )
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)

        self.status_portale = status_portale
        self.status_safework = status_safework
        layout.addWidget(status_portale)
        layout.addWidget(status_safework)

    def set_global_progress(self, value: int) -> None:
        """
        Aggiorna il valore della barra di progresso globale.

        Args:
          value: Valore intero (0-100).
        """
        value = max(0, min(value, 100))
        self.progress_bar.setValue(value)
        self.progress_label.setText(f"{value}%")

    def show_loading(self) -> None:
        """Visualizza la barra di progresso e nasconde le card di stato."""
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.status_portale.setVisible(False)
        self.status_safework.setVisible(False)

    def show_operational(self) -> None:
        """Nasconde la barra di progresso e visualizza le card di stato operative."""
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.status_portale.setVisible(True)
        self.status_safework.setVisible(True)
