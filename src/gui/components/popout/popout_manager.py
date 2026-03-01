"""
Componenti per la gestione dei pannelli sganciati (Pop-out).
Consente di separare i widget dallo stack centrale della MainWindow e renderizzarli in finestre di livello OS.
"""

from collections.abc import Callable

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCloseEvent, QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS, card_style
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path


class DetachedPanelWindow(QMainWindow):
    """
    Finestra indipendente che ospita un pannello precedentemente residente nello SlidingStackedWidget.
    """

    panel_closed_signal = pyqtSignal(int)  # Indice originale del pannello

    def __init__(
        self, original_index: int, panel: QWidget, title: str, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.original_index = original_index
        self.panel = panel

        self.setWindowTitle(f"{title} - SyncroJob (Finestra Esterna)")
        self.setMinimumSize(1000, 700)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # Configura il widget centrale
        self.panel.setParent(self)
        self.setCentralWidget(self.panel)
        self.panel.show()

    def closeEvent(self, event: QCloseEvent | None):
        """
        Intercetta la chiusura della finestra per avviare il riaggancio.
        """
        if event:
            self.panel_closed_signal.emit(self.original_index)
            super().closeEvent(event)


class PopoutPlaceholderWidget(QWidget):
    """
    Widget visualizzato nello StackedWidget centrale quando il suo contenuto nativo
    è stato spostato in una DetachedPanelWindow.
    """

    def __init__(self, title: str, on_reattach: Callable[[], None], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui(title, on_reattach)

    def _setup_ui(self, title: str, on_reattach: Callable[[], None]) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Container Card Centrale
        self.card = QFrame()
        self.card.setStyleSheet(card_style(border_color=COLORS["border_light"]))
        self.card.setFixedWidth(600)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40, 50, 40, 50)
        card_layout.setSpacing(25)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo SyncroJob
        logo_label = QLabel()
        logo_pixmap = QPixmap("logo menu laterale.png")
        if not logo_pixmap.isNull():
            logo_label.setPixmap(
                logo_pixmap.scaled(
                    180, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
                )
            )
        else:
            logo_label.setText("SYNCROJOB")
            logo_label.setStyleSheet(f"font-size: 32px; font-weight: 900; color: {COLORS['primary_blue']};")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Titolo
        title_label = QLabel(f"Modulo '{title}' attivo in finestra esterna")
        title_label.setStyleSheet(f"font-size: 20px; font-weight: 700; color: {COLORS['text_dark']};")
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Descrizione
        desc_label = QLabel(
            "La modalità Multi-Window ti permette di lavorare su più moduli contemporaneamente.\nPuoi chiudere la finestra esterna o cliccare il pulsante qui sotto per ripristinare la vista."
        )
        desc_label.setStyleSheet(f"font-size: 13px; color: {COLORS['text_muted']}; line-height: 1.4;")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Bottone di "Ricongiungimento"
        self.reattach_btn = ModernButton(
            "TORNA ALLA VISTA PRINCIPALE",
            icon=get_asset_path(Icons.CHEVRON_DOWN),
            variant=ModernButton.Variant.PRIMARY,
            parent=self,
        )
        self.reattach_btn.setToolTip("Riporta questo pannello all'interno della finestra principale.")
        self.reattach_btn.setFixedWidth(280)
        self.reattach_btn.setMinimumHeight(45)
        self.reattach_btn.clicked.connect(on_reattach)

        # Layout Card
        card_layout.addWidget(logo_label)
        card_layout.addSpacing(10)
        card_layout.addWidget(title_label)
        card_layout.addWidget(desc_label)
        card_layout.addSpacing(15)

        btn_h = QHBoxLayout()
        btn_h.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_h.addWidget(self.reattach_btn)
        card_layout.addLayout(btn_h)

        main_layout.addWidget(self.card)
