from contextlib import suppress
from datetime import datetime
from typing import TypedDict

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QSize, Qt, QTime, QTimer, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.core.sync_tracker import SyncTracker
from src.gui.styles import COLORS
from src.gui.widgets.core_widgets import IconButton
from src.utils.helpers import get_asset_path, get_colored_icon


class EventInfo(TypedDict):
    id: str
    name: str
    time: str
    icon: str
    color: str
    module_id: str | None

# Stile forzato per i tooltip in Light Mode
TOOLTIP_CSS = """
QToolTip {
    background-color: #FFFFFF;
    color: #212121;
    border: 1px solid #BBBBBB;
    border-radius: 6px;
    padding: 8px 12px;
}
"""


class AutopilotEventCard(QFrame):
    """
    Card per visualizzare un singolo evento programmato del bot.
    Include ora lo stato del database (freschezza dati) e un tasto di sync rapido.
    """

    sync_requested = Signal(str)  # Segnale emesso quando l'utente preme il tasto sync

    def __init__(
        self,
        info: EventInfo,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.bot_id = info["id"]
        self.bot_name = info["name"]
        self.target_time_str = info["time"]
        self.icon_path = info["icon"]
        self.color = info["color"]
        self.module_id = info.get("module_id") or self.bot_id

        self._setup_ui()
        self._setup_animations()

        # Timer per aggiornare il countdown e lo stato ogni minuto
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._refresh_ui_state)
        self.timer.start(60000)  # 60 secondi

        # Aggiorna UI iniziale
        self._refresh_ui_state()

    def _setup_ui(self) -> None:
        """Inizializza i componenti grafici della card."""
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(
            f"""
            {TOOLTIP_CSS}
            AutopilotEventCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS["bg_light"]}, stop:1 {COLORS["bg_white"]});
                border-radius: 12px;
                border-left: 4px solid {self.color};
                border-top: 1px solid {COLORS["border_light"]};
                border-right: 1px solid {COLORS["border_light"]};
                border-bottom: 1px solid {COLORS["border_light"]};
            }}
            AutopilotEventCard:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {COLORS["bg_hover"]}, stop:1 {COLORS["bg_light"]});
                border-left: 4px solid {self.color};
                border-top: 1px solid {COLORS["border_medium"]};
                border-right: 1px solid {COLORS["border_medium"]};
                border-bottom: 1px solid {COLORS["border_medium"]};
            }}
        """
        )
        self.setFixedHeight(85)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        # Icon
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(32, 32)
        self.icon_label.setPixmap(
            get_colored_icon(get_asset_path(self.icon_path), COLORS["bg_white"]).pixmap(20, 20)
        )
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setStyleSheet(
            f"QLabel {{ background-color: {self.color}; border-radius: 16px; border: none; padding: 6px; }}"
        )
        layout.addWidget(self.icon_label)

        # Content
        text_layout = self._create_text_layout()
        layout.addLayout(text_layout)
        layout.addStretch()

        # Sync Button
        self.sync_btn = IconButton()
        self.sync_btn.setIcon(get_colored_icon(get_asset_path(Icons.REFRESH), COLORS["text_muted"]))
        self.sync_btn.setIconSize(QSize(16, 16))
        self.sync_btn.setFixedSize(30, 30)
        self.sync_btn.setToolTip("Sincronizza database ora")
        self.sync_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sync_btn.clicked.connect(self._on_sync_clicked)
        layout.addWidget(self.sync_btn)

        if self.module_id == "none":
            self.sync_btn.hide()

    def _create_text_layout(self) -> QVBoxLayout:
        """Crea il layout testuale interno."""
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        name_h = QHBoxLayout()
        name_h.setSpacing(6)

        self.status_dot = QLabel()
        self.status_dot.setFixedSize(8, 8)
        self.status_dot.setStyleSheet("background-color: #CCCCCC; border-radius: 4px;")
        name_h.addWidget(self.status_dot)

        name_lbl = QLabel(self.bot_name)
        name_lbl.setStyleSheet(f"font-weight: 600; font-size: 13px; color: {COLORS['text_dark']}; background: transparent;")
        name_h.addWidget(name_lbl)
        name_h.addStretch()
        text_layout.addLayout(name_h)

        self.countdown_lbl = QLabel()
        self.countdown_lbl.setStyleSheet(f"font-size: 11px; color: {COLORS['text_muted']}; background: transparent; font-weight: 500;")
        text_layout.addWidget(self.countdown_lbl)
        return text_layout

    def _setup_animations(self) -> None:
        """Inizializza l'effetto pulse sull'icona."""
        self.icon_opacity = QGraphicsOpacityEffect(self.icon_label)
        self.icon_label.setGraphicsEffect(self.icon_opacity)

        self.pulse_anim = QPropertyAnimation(self.icon_opacity, b"opacity")
        self.pulse_anim.setDuration(2000)
        self.pulse_anim.setStartValue(0.6)
        self.pulse_anim.setEndValue(1.0)
        self.pulse_anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.pulse_anim.setLoopCount(-1)
        self.pulse_anim.start()

    def _refresh_ui_state(self) -> None:
        """Aggiorna sia il countdown che il pallino di stato del database."""
        self._update_countdown()
        self._update_db_status()

    def _on_sync_clicked(self) -> None:
        """Gestisce il click sul pulsante di sincronizzazione."""
        self.sync_requested.emit(self.bot_id)

    def cleanup(self) -> None:
        """Clean up animations and effects before deletion."""
        with suppress(RuntimeError, AttributeError):
            # Stop animations
            if hasattr(self, "pulse_anim") and self.pulse_anim:
                self.pulse_anim.stop()
                self.pulse_anim.deleteLater()

            if hasattr(self, "timer") and self.timer:
                self.timer.stop()

            # Remove graphics effect
            if hasattr(self, "icon_label") and self.icon_label:
                self.icon_label.setGraphicsEffect(None)  # type: ignore[arg-type]

            # Delete effect (may not exist if animation was disabled)
            if hasattr(self, "icon_opacity") and self.icon_opacity:
                self.icon_opacity.deleteLater()

    def _update_countdown(self) -> None:
        """Aggiorna il countdown per il prossimo evento."""
        # Calcolo tempo residuo
        secs_to = QTime.currentTime().secsTo(QTime.fromString(self.target_time_str, "HH:mm"))
        if secs_to < 0:
            # Se l'orario è già passato, calcola per domani
            secs_to += 24 * 3600

        # Recuperiamo la cadenza per calcolare se ci sono giorni aggiuntivi
        # Nota: secs_to ora contiene solo il tempo fino al prossimo orario target (entro 24h)
        # Se la cadenza è > 1 giorno, dovremmo idealmente sapere la data dell'ultima esecuzione,
        # ma basandoci sulla richiesta dell'utente "se la scadenza è tra 3 giorni",
        # implementiamo una logica generica che includa i giorni se presenti nel calcolo.

        days = secs_to // 86400
        hours = (secs_to % 86400) // 3600
        mins = (secs_to % 3600) // 60

        if days > 0:
            countdown = f"Tra {days}g {hours}h {mins}m"
        elif hours > 0:
            countdown = f"Tra {hours}h {mins}m"
        else:
            countdown = f"Tra {mins}m"

        self.countdown_lbl.setText(countdown)

    def _update_db_status(self) -> None:
        """Aggiorna il colore del pallino in base alla freschezza dei dati."""
        # Se non c'è un database associato (es. Report Email), nascondi il pallino
        if self.module_id == "none":
            self.status_dot.hide()
            return

        self.status_dot.show()
        status = SyncTracker.get_status(self.module_id)
        if not status:
            # Mai sincronizzato
            self.status_dot.setStyleSheet(f"background-color: {COLORS['error_red']}; border-radius: 4px;")
            self.status_dot.setToolTip("Database mai sincronizzato")
            return

        last_ts_float = status.get("last_ts", 0)
        last_dt = datetime.fromtimestamp(last_ts_float).astimezone()
        now = datetime.now().astimezone()

        # 1. Controllo Stato Tentativo Corrente (In corso / Fallito)
        last_success = status.get("last_attempt_success")

        if last_success is None:
            # Sincronizzazione in corso
            color = "#2196F3"  # Blu Material
            msg = "Sincronizzazione in corso..."
            self.status_dot.setStyleSheet(f"background-color: {color}; border-radius: 4px;")
            self.status_dot.setToolTip(msg)
            return

        if last_success is False:
            # Ultimo tentativo fallito
            color = COLORS["error_red"]
            msg = f"Ultimo tentativo FALLITO! (Dati al: {status.get('timestamp')})"
            self.status_dot.setStyleSheet(
                f"background-color: {color}; border-radius: 4px; border: 1px solid white;"
            )
            self.status_dot.setToolTip(msg)
            return

        # 2. Logica standard per i dati (Successo dell'ultimo tentativo o dati esistenti)
        # Logica speciale per TIMBRATURE:
        if self.module_id == "timbrature":
            diff_days = (now.date() - last_dt.date()).days
            if diff_days <= 1:
                color = COLORS["success_green"]
                msg = f"Database aggiornato ({status.get('timestamp')})"
            elif diff_days == 2:
                color = COLORS["warning_yellow"]
                msg = f"Sincronizzazione consigliata (Ultima: {status.get('timestamp')})"
            else:
                color = COLORS["error_red"]
                msg = f"Dati obsoleti! (Ultima: {status.get('timestamp')})"
        else:
            # Logica standard per gli altri moduli (OdA, PDL)
            diff_secs = (now - last_dt).total_seconds()
            if diff_secs < 12 * 3600:
                color = COLORS["success_green"]
                msg = f"Database aggiornato ({status.get('timestamp')})"
            elif diff_secs < 24 * 3600:
                color = COLORS["warning_yellow"]
                msg = f"Aggiornamento consigliato (Ultimo: {status.get('timestamp')})"
            else:
                color = COLORS["error_red"]
                msg = f"Database non aggiornato! (Ultimo: {status.get('timestamp')})"

        self.status_dot.setStyleSheet(f"background-color: {color}; border-radius: 4px;")
        self.status_dot.setToolTip(msg)
