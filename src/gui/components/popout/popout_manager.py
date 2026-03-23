"""
Componenti per la gestione dei pannelli sganciati (Pop-out).
Consente di separare i widget dallo stack centrale della MainWindow e renderizzarli in finestre di livello OS.
"""

from collections.abc import Callable

from PyQt6.QtCore import QPoint, Qt, pyqtSignal
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.gui.widgets.modern_button import ModernButton
from src.utils.helpers import get_asset_path


class DetachedPanelWindow(QMainWindow):
    """
    Finestra indipendente che ospita un pannello precedentemente residente nello SlidingStackedWidget.
    Utiilzza il frame di sistema OS per prevenire il noto crash PyQt6 (Access Violation) durante il reparenting C++.
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

        # Configura il widget centrale in modo elementare e solido
        self.panel.setParent(self)
        self.setCentralWidget(self.panel)
        self.panel.show()

    def closeEvent(self, event: QCloseEvent | None) -> None:
        """
        Intercetta la chiusura della finestra per avviare il riaggancio.
        """
        if event:
            import logging  # noqa: PLC0415

            logging.getLogger(__name__).info("Popout finestra esterna chiusa, innesco reattach...")
            self.panel_closed_signal.emit(self.original_index)
            super().closeEvent(event)


class PopoutPlaceholderWidget(QWidget):
    """Placeholder per lo stack centrale."""

    def __init__(self, title: str, on_reattach: Callable[[], None], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui(title, on_reattach)

    def _setup_ui(self, title: str, on_reattach: Callable[[], None]) -> None:  # noqa: PLR0915
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

        from PyQt6.QtWidgets import QGraphicsDropShadowEffect  # noqa: PLC0415

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(Qt.GlobalColor.black)
        shadow.setOffset(0, 10)
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(50, 60, 50, 60)
        card_layout.setSpacing(20)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo_container = QWidget()
        self.logo_container.setFixedSize(140, 140)
        logo_layout = QVBoxLayout(self.logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        try:
            from PyQt6.QtGui import QIcon  # noqa: PLC0415

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
                self.logo_label.setText("🚀")
                self.logo_label.setStyleSheet("font-size: 72px;")
        except Exception:
            self.logo_label.setText("🚀")
            self.logo_label.setStyleSheet("font-size: 72px;")

        logo_layout.addWidget(self.logo_label)

        badge_label = QLabel("IN ESECUZIONE")
        badge_label.setStyleSheet(
            f"background-color: {COLORS['bg_hover']}; color: {COLORS['primary_blue']}; padding: 6px 12px; border-radius: 12px; font-weight: 800; font-size: 11px; letter-spacing: 1px;"
        )
        badge_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(f"Modulo '{title}' attivo")
        title_label.setStyleSheet(f"font-size: 26px; font-weight: 900; color: {COLORS['text_dark']};")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        desc_label = QLabel(
            "Il modulo selezionato è in esecuzione in una <b>finestra indipendente</b>.<br><br>Puoi utilizzare il menu laterale per continuare a navigare e lavorare all'interno di questa finestra principale."
        )
        desc_label.setStyleSheet(f"font-size: 14.5px; color: {COLORS['text_muted']}; line-height: 1.6;")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.reattach_btn = ModernButton(
            "TORNA ALLA VISTA PRINCIPALE",
            icon=get_asset_path(Icons.CHEVRON_DOWN),
            variant=ModernButton.Variant.PRIMARY,
            parent=self,
        )
        self.reattach_btn.setFixedWidth(320)
        self.reattach_btn.setMinimumHeight(50)
        self.reattach_btn.clicked.connect(on_reattach)

        card_layout.addWidget(self.logo_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        card_layout.addWidget(badge_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        card_layout.addSpacing(5)
        card_layout.addWidget(title_label)
        card_layout.addWidget(desc_label)
        card_layout.addSpacing(25)
        card_layout.addWidget(self.reattach_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        main_layout.addWidget(self.card)

        # Animazioni
        from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QSequentialAnimationGroup  # noqa: PLC0415
        from PyQt6.QtWidgets import QGraphicsOpacityEffect  # noqa: PLC0415

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
