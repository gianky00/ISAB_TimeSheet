"""
SyncroJob - Consuntivo Workflow Widgets
Componenti grafici per la visualizzazione del processo di automazione.
"""

from typing import Any, ClassVar, cast

from PySide6.QtCore import Property, QEasingCurve, QEvent, QPropertyAnimation, Qt, Signal
from PySide6.QtGui import QColor, QEnterEvent, QFont, QMouseEvent
from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.gui.styles import COLORS


class WorkflowStepButton(QFrame):
    """Card pulsante premium per uno step del workflow consuntivo con animazione Glow."""

    clicked = Signal(str)

    class State:
        """Costanti per gli stati del pulsante del workflow."""

        IDLE = "idle"
        ACTIVE = "active"
        COMPLETED = "completed"
        ERROR = "error"

    def __init__(  # noqa: PLR0913
        self,
        step_id: str,
        step_number: int,
        title: str,
        description: str,
        is_action: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        """
        Inizializza la card dello step.

        Args:
          step_id: Identificativo unico dello step.
          step_number: Numero d'ordine visualizzato.
          title: Titolo breve dello step.
          description: Descrizione estesa.
          is_action: Se True, applica uno stile pulsante d'azione (gradiente).
          parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self._step_id = step_id
        self._step_number = step_number
        self._state = self.State.IDLE
        self._glow_opacity = 0.0
        self._is_action = is_action

        if is_action:
            self.setFixedSize(200, 110)
        else:
            self.setFixedSize(165, 130)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(f"Step {step_number}: {description}")

        self._setup_ui(step_number, title, description)
        self._setup_glow_animation()
        self._apply_style()

    def _setup_ui(self, number: int, title: str, description: str) -> None:
        """Inizializza i componenti grafici interni (badge, titoli, descrizioni)."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        top_row = QHBoxLayout()
        top_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._number_badge = QLabel(str(number))
        self._number_badge.setFixedSize(28, 28)
        self._number_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._number_badge.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        top_row.addWidget(self._number_badge)
        layout.addLayout(top_row)

        self._title_label = QLabel(title)
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self._title_label.setWordWrap(True)
        layout.addWidget(self._title_label)

        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setFont(QFont("Segoe UI", 9))
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(f"color: {COLORS['text_muted']}; background: transparent;")
        layout.addWidget(desc_label)

    def _setup_glow_animation(self) -> None:
        """Configura l'animazione di pulsazione per lo stato attivo."""
        self._glow_anim = QPropertyAnimation(self, b"glowOpacity")
        self._glow_anim.setDuration(1200)
        self._glow_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self._glow_anim.setStartValue(0.3)
        self._glow_anim.setEndValue(1.0)
        self._glow_anim.setLoopCount(-1)

    def get_glow_opacity(self) -> float:
        """Restituisce il valore corrente dell'opacit  del glow."""
        return self._glow_opacity

    def set_glow_opacity(self, value: float) -> None:
        """Imposta l'opacit  del glow e forza il ridisegno."""
        self._glow_opacity = value
        self.update()

    glowOpacity = Property(float, fget=get_glow_opacity, fset=set_glow_opacity)  # noqa: N815

    def set_state(self, state: str) -> None:
        """
        Cambia lo stato visivo dello step.

        Args:
          state: Uno degli stati definiti in WorkflowStepButton.State.
        """
        self._state = state
        self._apply_style()
        if state == self.State.ACTIVE:
            self._glow_anim.start()
        else:
            self._glow_anim.stop()
            self._glow_opacity = 0.0

    def _apply_style(self) -> None:
        """Applica il foglio di stile QSS in base allo stato corrente."""
        state_styles: dict[str, dict[str, Any]] = {
            self.State.IDLE: {
                "bg": "#ffffff",
                "border": COLORS["border_light"],
                "badge_bg": "#f1f3f5",
                "badge_color": COLORS["text_muted"],
                "title_color": COLORS["text_dark"],
                "shadow_color": QColor(0, 0, 0, 25),
            },
            self.State.ACTIVE: {
                "bg": "#e8f5e9",
                "border": "#4CAF50",
                "badge_bg": "#4CAF50",
                "badge_color": "#ffffff",
                "title_color": "#2E7D32",
                "shadow_color": QColor(76, 175, 80, 80),
            },
            self.State.COMPLETED: {
                "bg": "#f0fdf4",
                "border": "#2E7D32",
                "badge_bg": "#2E7D32",
                "badge_color": "#ffffff",
                "title_color": "#1b5e20",
                "shadow_color": QColor(46, 125, 50, 60),
            },
            self.State.ERROR: {
                "bg": "#fef2f2",
                "border": COLORS["error_red"],
                "badge_bg": COLORS["error_red"],
                "badge_color": "#ffffff",
                "title_color": COLORS["error_red"],
                "shadow_color": QColor(220, 53, 69, 60),
            },
        }
        s = state_styles.get(self._state, state_styles[self.State.IDLE])

        if self._is_action:
            self.setStyleSheet("""
        WorkflowStepButton {
          background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #1a237e, stop:0.5 #283593, stop:1 #1565c0);
          border: 2px solid #1a237e; border-radius: 14px;
        }
        WorkflowStepButton:hover {
          border: 2px solid #42a5f5;
          background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 #283593, stop:0.5 #1565c0, stop:1 #1976d2);
        }
      """)
            self._number_badge.setStyleSheet(
                "background: rgba(255,255,255,0.2); color: #ffffff; "
                "border-radius: 14px; border: 1px solid rgba(255,255,255,0.3);"
            )
            self._title_label.setStyleSheet("color: #ffffff; background: transparent;")
        else:
            self.setStyleSheet(f"""
        WorkflowStepButton {{
          background-color: {s["bg"]}; border: 2px solid {s["border"]};
          border-radius: 14px;
        }}
        WorkflowStepButton:hover {{
          border: 2px solid #009688; background-color: #e0f2f1;
        }}
      """)
            self._number_badge.setStyleSheet(
                f"background-color: {s['badge_bg']}; color: {s['badge_color']}; "
                f"border-radius: 14px; border: none;"
            )
            self._title_label.setStyleSheet(f"color: {s['title_color']}; background: transparent;")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 4)
        shadow.setColor(cast("QColor", s["shadow_color"]))
        self.setGraphicsEffect(shadow)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Emette il segnale di clic quando viene premuto il tasto sinistro del mouse."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._step_id)
        super().mousePressEvent(event)

    def enterEvent(self, event: QEnterEvent) -> None:
        """Evidenzia lo step con un'ombra piu' marcata al passaggio del mouse."""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 150, 136, 100))
        self.setGraphicsEffect(shadow)
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        """Ripristina lo stile originale all'uscita del mouse."""
        self._apply_style()
        super().leaveEvent(event)


class WorkflowMapWidget(QWidget):
    """Widget mappa workflow con step connessi da frecce."""

    step_clicked = Signal(str)

    STEPS: ClassVar[list[tuple[str, int, str, str]]] = [
        ("carica_dati", 1, "CARICA\nDATI", "CaricaDatiMultiplo"),
        ("elabora_dati", 2, "ELABORA\nDATI", "elaboraDati"),
        ("compila_consuntivo", 3, "COMPILA\nCONSUNTIVO", "EseguiTuttiSmista"),
        ("verifica", 4, "VERIFICA", "VerificaConsuntivo"),
        ("stampa", 5, "STAMPA", "verificaEstampaFogli"),
    ]

    ACTIONS: ClassVar[list[tuple[str, int, str, str]]] = [
        ("esegui_1_4", 6, "[AVVIO] ESEGUI\n1  4", "Carica   Elabora   Compila   Verifica"),
        ("esegui_1_5", 7, "[AVVIO] ESEGUI\n1  5", "Intero workflow completo"),
    ]

    # Mapping step_id   lista macro VBA da eseguire
    MACRO_MAP: ClassVar[dict[str, list[str]]] = {
        "carica_dati": ["CaricaDatiMultiplo"],
        "elabora_dati": ["elaboraDati"],
        "compila_consuntivo": ["EseguiTuttiSmista"],
        "verifica": ["VerificaConsuntivo"],
        "stampa": ["verificaEstampaFogli"],
        "esegui_1_4": ["CaricaDatiMultiplo", "elaboraDati", "EseguiTuttiSmista", "VerificaConsuntivo"],
        "esegui_1_5": [
            "CaricaDatiMultiplo",
            "elaboraDati",
            "EseguiTuttiSmista",
            "VerificaConsuntivo",
            "verificaEstampaFogli",
        ],
    }

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza la mappa del workflow.

        Args:
          parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self.setMinimumHeight(300)
        self._step_buttons: dict[str, WorkflowStepButton] = {}
        self._setup_ui()

    def _setup_ui(self) -> None:  # noqa: PLR0915
        """Costruisce il layout della pipeline con step e azioni complesse."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        container = QFrame()
        container.setObjectName("workflowContainer")
        container.setStyleSheet("""
      QFrame#workflowContainer {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
          stop:0 #f8fffe, stop:0.3 #e8f5e9, stop:0.7 #e0f7fa, stop:1 #f3e5f5);
        border: 1px solid rgba(0, 150, 136, 0.15);
        border-radius: 20px;
      }
    """)
        shadow = QGraphicsDropShadowEffect(container)
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 20))
        container.setGraphicsEffect(shadow)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(24, 20, 24, 20)
        container_layout.setSpacing(16)

        title = QLabel("  WORKFLOW PIPELINE")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {COLORS['text_dark']}; background: transparent; letter-spacing: 2px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(title)

        # Riga principale: 5 step
        main_row = QHBoxLayout()
        main_row.setSpacing(0)
        main_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for i, (sid, num, label, desc) in enumerate(self.STEPS):
            btn = WorkflowStepButton(sid, num, label, desc)
            btn.clicked.connect(lambda text: self.step_clicked.emit(text))
            self._step_buttons[sid] = btn
            main_row.addWidget(btn)
            if i < len(self.STEPS) - 1:
                arrow = self._create_arrow_label()
                main_row.addWidget(arrow)

        container_layout.addLayout(main_row)

        # Riga azioni complesse
        action_row = QHBoxLayout()
        action_row.setSpacing(16)
        action_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for sid, num, label, desc in self.ACTIONS:
            btn = WorkflowStepButton(sid, num, label, desc, is_action=True)
            btn.setFixedSize(190, 100)
            btn.clicked.connect(lambda text: self.step_clicked.emit(text))
            self._step_buttons[sid] = btn
            action_row.addWidget(btn)

        # Separatore verticale
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.VLine)
        sep.setFixedHeight(70)
        sep.setStyleSheet("background: rgba(0,0,0,0.12); max-width: 2px; min-width: 2px;")
        action_row.addWidget(sep)

        # Extra macro buttons con label complete
        extras = [
            ("email_gen", 8, "   Email\nGenerica", "InviaEmailGenerico"),
            ("email_chiamata", 9, "   Email\nChiamata", "InviaEmailConsuntivoChiamata"),
            ("relazione", 10, "   Relazione\nTecnica", "CreaEConvertiRelazioneTecnica"),
        ]
        for sid, num, label, desc in extras:
            btn = WorkflowStepButton(sid, num, label, desc, is_action=True)
            btn.setFixedSize(140, 80)
            btn.clicked.connect(lambda text: self.step_clicked.emit(text))
            self._step_buttons[sid] = btn
            action_row.addWidget(btn)

        container_layout.addLayout(action_row)
        main_layout.addWidget(container)

    def _create_arrow_label(self, color: str = "#009688") -> QLabel:
        """Crea una label visuale per la freccia di connessione."""
        arrow = QLabel("  ")
        arrow.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        arrow.setStyleSheet(f"color: {color}; background: transparent; padding: 0 6px;")
        arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
        arrow.setFixedWidth(40)
        return arrow

    def set_step_state(self, step_id: str, state: str) -> None:
        """
        Imposta lo stato di un pulsante step specifico.

        Args:
          step_id: Identificativo dello step.
          state: Nuovo stato (active, completed, error, ecc.).
        """
        if btn := self._step_buttons.get(step_id):
            btn.set_state(state)

    def reset_all(self) -> None:
        """Ripristina tutti i pulsanti della mappa allo stato IDLE."""
        for btn in self._step_buttons.values():
            btn.set_state(WorkflowStepButton.State.IDLE)

    def get_macros_for_step(self, step_id: str) -> list[str]:
        """
        Restituisce la lista di macro VBA per lo step indicato.

        Args:
          step_id: Identificativo dello step.

        Returns:
          list[str]: Nomi delle macro VBA associate.
        """
        extra_map: dict[str, list[str]] = {
            "email_gen": ["InviaEmailGenerico"],
            "email_chiamata": ["InviaEmailConsuntivoChiamata"],
            "relazione": ["CreaEConvertiRelazioneTecnica"],
        }
        return self.MACRO_MAP.get(step_id, extra_map.get(step_id, []))
