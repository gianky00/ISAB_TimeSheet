"""Componenti per la gestione dei pannelli sganciati (Pop-out).

Consente di separare i widget dallo stack centrale della MainWindow e renderizzarli in finestre di livello OS.
"""

import logging
from collections.abc import Callable

from PySide6.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QSequentialAnimationGroup,
    Qt,
    Signal,
)
from PySide6.QtGui import QCloseEvent, QIcon
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path

logger = logging.getLogger(__name__)


class DetachedPanelWindow(QMainWindow):
    """Finestra indipendente che ospita un pannello precedentemente residente nello SlidingStackedWidget.

    Utilizza il frame di sistema OS per prevenire il noto crash PySide6 (Access Violation) durante il reparenting C++.

    Inizializza la classe.
    """

    panel_closed_signal = Signal(int)  # Indice originale del pannello

    def __init__(
        self, original_index: int, panel: QWidget, title: str, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.original_index = original_index
        self.panel = panel

        self.setWindowTitle(f"{title} - SyncroJob (Finestra Esterna)")
        self.setMinimumSize(1000, 700)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        # Configura il widget centrale in modo elementare e solido
        self.panel.setParent(self)
        self.setCentralWidget(self.panel)
        self.panel.show()

    def closeEvent(self, event: QCloseEvent | None) -> None:
        """Intercetta la chiusura della finestra per avviare il riaggancio."""
        if event:
            logger.info("Popout finestra esterna chiusa, innesco reattach...")
            self.panel_closed_signal.emit(self.original_index)
            super().closeEvent(event)


class PopoutPlaceholderWidget(QWidget):
    """Placeholder per lo stack centrale.

    Inizializza la classe.
    """

    def __init__(self, title: str, on_reattach: Callable[[], None], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui(title, on_reattach)

    def _setup_ui(self, title: str, on_reattach: Callable[[], None]) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)

        self.card = QFrame()
        self.card.setObjectName("placeholderCard")
        self.card.setStyleSheet(f"""
      QFrame#placeholderCard {{
        background-color: {COLORS["bg_white"]};
        border: 1px solid {COLORS["border_light"]};
        border-top: 5px solid {COLORS["primary_blue"]};
        border-radius: 12px;
      }}
      QLabel {{ border: none; background: transparent; }}
    """)

        self.card.setFixedWidth(560)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(Qt.GlobalColor.black)
        shadow.setOffset(0, 10)
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(50, 60, 50, 60)
        card_layout.setSpacing(20)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._setup_logo(card_layout)
        self._setup_labels(card_layout, title)
        self._setup_button(card_layout, on_reattach)

        main_layout.addWidget(self.card)
        self._setup_animations()

    def _setup_logo(self, layout: QVBoxLayout) -> None:
        """Configura l'area del logo nell'header della card."""
        self.logo_container = QWidget()
        self.logo_container.setFixedSize(140, 140)
        logo_layout = QVBoxLayout(self.logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        try:
            logo_path = get_asset_path("app.ico")
            icon = QIcon(logo_path)
            pixmap = icon.pixmap(256, 256)
            if not pixmap.isNull():
                self.logo_label.setPixmap(
                    pixmap.scaled(
                        110,
                        110,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
            else:
                self.logo_label.setText("[AVVIO]")
                self.logo_label.setStyleSheet("font-size: 72px;")
        except Exception:
            self.logo_label.setText("[AVVIO]")
            self.logo_label.setStyleSheet("font-size: 72px;")

        logo_layout.addWidget(self.logo_label)
        layout.addWidget(self.logo_container, alignment=Qt.AlignmentFlag.AlignHCenter)

    def _setup_labels(self, layout: QVBoxLayout, title: str) -> None:
        """Inizializza le label di testo informative."""
        badge_label = QLabel("IN ESECUZIONE")
        badge_label.setStyleSheet(
            f"background-color: {COLORS['bg_hover']}; color: {COLORS['primary_blue']}; padding: 6px 12px; border-radius: 12px; font-weight: 800; font-size: 11px; letter-spacing: 1px;"
        )
        badge_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(f"Modulo '{title}' attivo")
        title_label.setStyleSheet(f"font-size: 26px; font-weight: 900; color: {COLORS['text_dark']};")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        desc_label = QLabel(
            "Il modulo selezionato  in esecuzione in una <b>finestra indipendente</b>.<br><br>Puoi utilizzare il menu laterale per continuare a navigare e lavorare all'interno di questa finestra principale."
        )
        desc_label.setStyleSheet(f"font-size: 14.5px; color: {COLORS['text_muted']}; line-height: 1.6;")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(badge_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(5)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)

    def _setup_button(self, layout: QVBoxLayout, on_reattach: Callable[[], None]) -> None:
        """Configura il pulsante di riaggancio."""
        self.reattach_btn = ModernButton(
            "TORNA ALLA VISTA PRINCIPALE",
            icon=get_asset_path(Icons.CHEVRON_DOWN),
            variant=ModernButton.Variant.PRIMARY,
            parent=self,
        )
        self.reattach_btn.setFixedWidth(320)
        self.reattach_btn.setMinimumHeight(50)
        self.reattach_btn.clicked.connect(on_reattach)

        layout.addSpacing(25)
        layout.addWidget(self.reattach_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

    def _setup_animations(self) -> None:
        """Configura le animazioni visive della card."""
        self.opacity_effect = QGraphicsOpacityEffect(self.card)
        self.card.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)
        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(800)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_anim.start()

        self.float_anim_up = QPropertyAnimation(self.logo_label, b"pos")
        self.float_anim_up.setDuration(1500)
        self.float_anim_up.setStartValue(QPoint(0, 0))
        self.float_anim_up.setEndValue(QPoint(0, -10))
        self.float_anim_up.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.float_anim_down = QPropertyAnimation(self.logo_label, b"pos")
        self.float_anim_down.setDuration(1500)
        self.float_anim_down.setStartValue(QPoint(0, -10))
        self.float_anim_down.setEndValue(QPoint(0, 0))
        self.float_anim_down.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.bounce_group = QSequentialAnimationGroup(self)
        self.bounce_group.addAnimation(self.float_anim_up)
        self.bounce_group.addAnimation(self.float_anim_down)
        self.bounce_group.setLoopCount(-1)
        self.bounce_group.start()
