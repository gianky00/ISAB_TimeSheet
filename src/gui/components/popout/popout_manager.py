"""
Componenti per la gestione dei pannelli sganciati (Pop-out).
Consente di separare i widget dallo stack centrale della MainWindow e renderizzarli in finestre di livello OS.
"""

from collections.abc import Callable

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
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
    Gestisce il proprio ciclo di vita e informa il controller alla chiusura per il riaggancio del widget.
    """

    panel_closed_signal = pyqtSignal(int)  # Indice originale del pannello

    def __init__(
        self, original_index: int, panel: QWidget, title: str, parent: QWidget | None = None
    ) -> None:
        """
        Inizializza la finestra esterna.

        Args:
            original_index: L'indice della pagina nello stack originale.
            panel: L'istanza del widget da visualizzare.
            title: Il titolo da mostrare nella barra del titolo.
            parent: Il widget genitore opzionale.
        """
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

        Args:
            event: L'evento di chiusura di Qt.
        """
        if event:
            self.panel_closed_signal.emit(self.original_index)
            super().closeEvent(event)


class PopoutPlaceholderWidget(QWidget):
    """
    Widget visualizzato nello StackedWidget centrale quando il suo contenuto nativo
    è stato spostato in una DetachedPanelWindow.
    Fornisce feedback visivo all'utente e un pulsante per il riaggancio manuale.
    """

    def __init__(self, title: str, on_reattach: Callable[[], None], parent: QWidget | None = None) -> None:
        """
        Inizializza il placeholder.

        Args:
            title: Il nome del modulo sganciato.
            on_reattach: La callback da eseguire per riagganciare il pannello.
            parent: Il widget genitore opzionale.
        """
        super().__init__(parent)
        self._setup_ui(title, on_reattach)

    def _setup_ui(self, title: str, on_reattach: Callable[[], None]) -> None:
        """Configura l'interfaccia grafica del placeholder."""
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Container Card Centrale
        self.card = QFrame()
        self.card.setObjectName("placeholderCard")
        self.card.setStyleSheet(f"""
            QFrame#placeholderCard {{
                background-color: {COLORS["bg_white"]};
                border: 1px solid {COLORS["border_light"]};
                border-top: 5px solid {COLORS["primary_blue"]};
                border-radius: 12px;
            }}
            QLabel {{
                border: none;
                background: transparent;
            }}
        """)
        self.card.setFixedWidth(560)

        # Shadow Effect
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(Qt.GlobalColor.black)
        shadow.setOffset(0, 10)
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(50, 60, 50, 60)
        card_layout.setSpacing(20)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Container per il Logo con animazione fluttuante
        self.logo_container = QWidget()
        self.logo_container.setFixedSize(140, 140)
        logo_layout = QVBoxLayout(self.logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        try:
            from PyQt6.QtGui import QIcon

            # Carica l'app.ico tramite QIcon per estrarre il layer ad alta risoluzione
            logo_path = get_asset_path("app.ico")
            icon = QIcon(logo_path)
            # Richiediamo una dimensione grande (es. 256x256) per evitare pixelation, poi la scaliamo morbidamente a 120x120
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

        # Badge di stato
        badge_label = QLabel("IN ESECUZIONE")
        badge_label.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS["bg_hover"]};
                color: {COLORS["primary_blue"]};
                padding: 6px 12px;
                border-radius: 12px;
                font-weight: 800;
                font-size: 11px;
                letter-spacing: 1px;
            }}
        """)
        badge_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        badge_layout = QHBoxLayout()
        badge_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge_layout.addWidget(badge_label)

        # Titolo
        title_label = QLabel(f"Modulo '{title}' attivo")
        title_label.setStyleSheet(f"font-size: 26px; font-weight: 900; color: {COLORS['text_dark']};")
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Descrizione
        desc_label = QLabel(
            "Il modulo selezionato è in esecuzione in una <b>finestra indipendente</b>.<br><br>"
            "Puoi utilizzare il menu laterale per continuare a navigare e lavorare all'interno di questa finestra principale, "
            "mantenendo la vista sganciata a tua disposizione."
        )
        desc_label.setStyleSheet(f"font-size: 14.5px; color: {COLORS['text_muted']}; line-height: 1.6;")
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
        self.reattach_btn.setFixedWidth(320)
        self.reattach_btn.setMinimumHeight(50)
        self.reattach_btn.setStyleSheet(
            self.reattach_btn.styleSheet() + "QPushButton { font-size: 14px; font-weight: bold; }"
        )
        self.reattach_btn.clicked.connect(on_reattach)

        # Assemblaggio Layout
        card_layout.addWidget(self.logo_container, alignment=Qt.AlignmentFlag.AlignHCenter)
        card_layout.addLayout(badge_layout)
        card_layout.addSpacing(5)
        card_layout.addWidget(title_label)
        card_layout.addWidget(desc_label)
        card_layout.addSpacing(25)

        btn_h = QHBoxLayout()
        btn_h.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_h.addWidget(self.reattach_btn)
        card_layout.addLayout(btn_h)

        main_layout.addWidget(self.card)

        # === ANIMAZIONI ===
        from PyQt6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, QSequentialAnimationGroup
        from PyQt6.QtWidgets import QGraphicsOpacityEffect

        # 1. Fade In della Card
        self.opacity_effect = QGraphicsOpacityEffect(self.card)
        self.card.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)

        self.fade_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_anim.setDuration(800)
        self.fade_anim.setStartValue(0.0)
        self.fade_anim.setEndValue(1.0)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_anim.start()

        # 2. Effetto "Levitazione" continua per il logo
        self.float_anim_up = QPropertyAnimation(self.logo_label, b"pos")
        self.float_anim_up.setDuration(1500)
        self.float_anim_up.setStartValue(self.logo_label.pos())
        self.float_anim_up.setEndValue(self.logo_label.pos() + QPoint(0, -10))
        self.float_anim_up.setEasingCurve(QEasingCurve.Type.InOutSine)

        self.float_anim_down = QPropertyAnimation(self.logo_label, b"pos")
        self.float_anim_down.setDuration(1500)
        self.float_anim_down.setStartValue(self.logo_label.pos() + QPoint(0, -10))
        self.float_anim_down.setEndValue(self.logo_label.pos())
        self.float_anim_down.setEasingCurve(QEasingCurve.Type.InOutSine)

        self.bounce_group = QSequentialAnimationGroup(self)
        self.bounce_group.addAnimation(self.float_anim_up)
        self.bounce_group.addAnimation(self.float_anim_down)
        self.bounce_group.setLoopCount(-1)  # Infinito
        self.bounce_group.start()
