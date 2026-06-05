"""SyncroJob - Weather Widget (Premium V10.0 - Atmospheric Glassmorphism).

Visualizza le previsioni meteo locali (Priolo Gargallo) utilizzando il servizio dedicato.
V10.0: SRP Compliant, con sfondi atmosferici dinamici, mini-gauge circolari,
visualizzatore termico interattivo ed effetti particellari animati reali a 60fps.
"""

# ruff: noqa: PLR0915, C901
from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from PySide6.QtCore import QEasingCurve, QPointF, QPropertyAnimation, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPaintEvent,
    QPen,
)
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsOpacityEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from src.application.services.constants import Icons
from src.application.services.weather_service import WeatherService
from src.gui.styles import BUTTON_ICON_ONLY, COLORS
from src.gui.styles.palette_helpers import hex_to_rgba
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.modern_card import ModernCard
from src.infrastructure.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)

# Soglie Qualità Aria
AQI_MODERATE = 40
AQI_UNHEALTHY_SENSITIVE = 60
AQI_UNHEALTHY = 80

# Stile forzato per evitare il bug della Dark Mode / Tooltip nero in PySide6.
TOOLTIP_CSS = """
QToolTip {
  background-color: #FFFFFF;
  color: #212121;
  border: 1px solid #CCCCCC;
  border-radius: 6px;
  padding: 8px 12px;
}
"""


class HseMetricBar(QWidget):
    """Visualizzatore grafico premium a barra orizzontale per inquinanti e pollini.

    Inizializza la barra metrica HSE.
    """

    def __init__(
        self,
        name: str,
        unit: str,
        max_val: float,
        accent_color: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.name = name
        self.unit = unit
        self.max_val = max_val
        self.accent_color = accent_color
        self.value = 0.0
        self.setFixedHeight(26)

    def set_value(self, val: float) -> None:
        """Aggiorna il valore corrente e forza il ridisegno."""
        self.value = val
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Esegue il rendering della barra orizzontale stile dashboard."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        w = float(rect.width())

        # Testo: Nome a sinistra, Valore + Unità a destra
        font = QFont()
        font.setPointSize(7)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor(COLORS["text_dark"]))

        # Disegna Nome
        painter.drawText(
            QRectF(0, 0, w, 11), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.name
        )

        # Disegna Valore
        val_str = f"{self.value:.1f} {self.unit}" if self.value > 0 else f"-- {self.unit}"
        painter.setPen(QColor(COLORS["text_muted"]))
        painter.drawText(
            QRectF(0, 0, w, 11), Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, val_str
        )

        # Disegna Sfondo Barra
        bar_y = 15.0
        bar_h = 3.5
        bg_rect = QRectF(0.0, bar_y, w, bar_h)
        painter.setBrush(QBrush(QColor(COLORS["border_light"])))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(bg_rect, 1.8, 1.8)

        # Disegna Progresso
        pct = self.value / self.max_val if self.max_val > 0 else 0.0
        pct = max(0.0, min(1.0, pct))
        if pct > 0:
            fill_rect = QRectF(0.0, bar_y, w * pct, bar_h)
            painter.setBrush(QBrush(QColor(self.accent_color)))
            painter.drawRoundedRect(fill_rect, 1.8, 1.8)

        painter.end()


class WindCompass(QWidget):
    """Bussola anemometrica premium con indicatore di direzione rotante a 360°.

    Inizializza la bussola del vento.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedSize(86, 86)
        self.direction = 0.0
        self.speed = 0.0
        self.setToolTip("<b>Direzione e Intensità Vento</b><br/>L'angolo reale di provenienza ed intensità.")
        self.setStyleSheet(TOOLTIP_CSS)

    def set_values(self, direction: float, speed: float) -> None:
        """Configura la direzione e velocità per la bussola."""
        self.direction = direction
        self.speed = speed
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Disegna la bussola e l'indicatore di direzione rotante."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        cx = float(rect.width()) / 2.0
        cy = float(rect.height()) / 2.0
        r = min(cx, cy) - 5.0

        # Disegna il cerchio di sfondo della bussola
        painter.setPen(QPen(QColor(COLORS["border_light"]), 1.5))
        painter.setBrush(QBrush(QColor("#fbfcfd")))
        painter.drawEllipse(QPointF(cx, cy), r, r)

        # Disegna le direzioni cardinali (N, E, S, W)
        font = QFont()
        font.setPointSize(6)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor(COLORS["text_muted"]))

        painter.drawText(QRectF(cx - 10, cy - r + 1, 20, 10), Qt.AlignmentFlag.AlignCenter, "N")
        painter.drawText(QRectF(cx + r - 11, cy - 5, 10, 10), Qt.AlignmentFlag.AlignCenter, "E")
        painter.drawText(QRectF(cx - 10, cy + r - 11, 20, 10), Qt.AlignmentFlag.AlignCenter, "S")
        painter.drawText(QRectF(cx - r + 1, cy - 5, 10, 10), Qt.AlignmentFlag.AlignCenter, "W")

        # Disegna il valore di velocità del vento al centro
        font_val = QFont()
        font_val.setPointSize(7)
        font_val.setBold(True)
        painter.setFont(font_val)
        painter.setPen(QColor(COLORS["text_dark"]))
        painter.drawText(QRectF(cx - 25, cy - 12, 50, 12), Qt.AlignmentFlag.AlignCenter, str(int(self.speed)))

        font_unit = QFont()
        font_unit.setPointSize(5)
        font_unit.setBold(True)
        painter.setFont(font_unit)
        painter.setPen(QColor(COLORS["text_muted"]))
        painter.drawText(QRectF(cx - 25, cy + 1, 50, 10), Qt.AlignmentFlag.AlignCenter, "km/h")

        # Disegna l'indicatore di direzione (Freccia / Cursore rotante)
        painter.save()
        painter.translate(cx, cy)
        # 0 gradi è in alto (Nord)
        painter.rotate(self.direction)

        arrow_pen = QPen(QColor(COLORS["primary_blue"]), 1.5)
        painter.setPen(arrow_pen)
        painter.setBrush(QBrush(QColor(COLORS["primary_blue"])))

        # Coordinate della freccia
        arrow_path = QPainterPath()
        arrow_path.moveTo(0.0, -r + 4.0)
        arrow_path.lineTo(-4.0, -r + 12.0)
        arrow_path.lineTo(4.0, -r + 12.0)
        arrow_path.closeSubpath()
        painter.drawPath(arrow_path)

        painter.restore()
        painter.end()


class TemperatureVisualizer(QWidget):
    """Visualizzatore grafico premium del divario tra temperatura reale e percepita.

    Inizializza il visualizzatore termico.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(14)
        self.setMinimumWidth(120)
        self.temp_min = 10.0
        self.temp_max = 35.0
        self.temp_curr = 20.0
        self.temp_app = 22.0

    def set_values(self, current: float, apparent: float, min_val: float, max_val: float) -> None:
        """Configura i valori termici per il disegno della barra."""
        self.temp_curr = current
        self.temp_app = apparent
        self.temp_min = min_val
        self.temp_max = max_val
        if self.temp_max <= self.temp_min:
            self.temp_max = self.temp_min + 10.0
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Disegna la barra a gradiente con i cursori di temperatura reale e percepita."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        bar_height = 4.0
        bar_y = (rect.height() - bar_height) / 2.0
        bar_rect = QRectF(0.0, bar_y, float(rect.width()), bar_height)

        # Gradiente termico (freddo -> caldo)
        grad = QLinearGradient(0, 0, rect.width(), 0)
        grad.setColorAt(0.0, QColor("#3b82f6"))  # Blu freddo
        grad.setColorAt(0.5, QColor("#eab308"))  # Giallo temperato
        grad.setColorAt(1.0, QColor("#ef4444"))  # Rosso caldo

        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(bar_rect, 2.0, 2.0)

        # Calcolo delle posizioni orizzontali dei cursori
        def get_x(val: float) -> float:
            """Calcola la posizione X proporzionale al valore termico nell'area del widget."""
            ratio = (val - self.temp_min) / (self.temp_max - self.temp_min)
            ratio = max(0.0, min(1.0, ratio))
            return ratio * float(rect.width())

        x_curr = get_x(self.temp_curr)
        x_app = get_x(self.temp_app)

        # 1. Cursore Temperatura Reale (Cerchio bianco con bordo blu ciano)
        painter.setBrush(QBrush(QColor("#ffffff")))
        painter.setPen(QPen(QColor(COLORS["primary_blue"]), 2.0))
        painter.drawEllipse(QRectF(x_curr - 4.5, (float(rect.height()) - 9.0) / 2.0, 9.0, 9.0))

        # 2. Cursore Temperatura Percepita (Cerchio tratteggiato arancione con glow)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(COLORS["warning_orange"]), 1.5, Qt.PenStyle.DashLine))
        painter.drawEllipse(QRectF(x_app - 5.5, (float(rect.height()) - 11.0) / 2.0, 11.0, 11.0))

        painter.end()


class MiniRadialGauge(QWidget):
    """Micro indicatore circolare premium ad arco per le metriche ambientali.

    Inizializza il micro gauge radiale.
    """

    def __init__(
        self,
        title: str,
        max_val: float,
        accent_color: str,
        tooltip: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setFixedSize(58, 58)
        self.title = title
        self.val_text = ""
        self.value = 0.0
        self.max_val = max_val
        self.accent_color = accent_color
        self.setToolTip(tooltip)
        self.setStyleSheet(TOOLTIP_CSS)

    def set_value(self, value: float, display_text: str) -> None:
        """Aggiorna il valore corrente e la stringa visualizzata."""
        self.value = value
        self.val_text = display_text
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        """Rendering dell'arco di progresso radiale."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        margin = 4.0
        gauge_rect = QRectF(
            margin, margin, float(rect.width()) - 2.0 * margin, float(rect.height()) - 2.0 * margin
        )

        # 1. Arco di sfondo (grigio discreto)
        bg_pen = QPen(QColor(COLORS["border_light"]), 3.0)
        bg_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawArc(gauge_rect, -135 * 16, -270 * 16)

        # 2. Calcolo arco attivo (percentuale)
        pct = self.value / self.max_val if self.max_val > 0 else 0.0
        pct = max(0.0, min(1.0, pct))
        span_angle = -270.0 * pct

        # 3. Arco attivo colorato
        active_pen = QPen(QColor(self.accent_color), 3.0)
        active_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(active_pen)
        painter.drawArc(gauge_rect, -135 * 16, int(span_angle * 16))

        # 4. Testo della metrica al centro
        font = QFont()
        font.setPointSize(7)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor(COLORS["text_dark"]))
        text_rect = QRectF(0, float(rect.height()) / 2.0 - 7.0, float(rect.width()), 11.0)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.val_text)

        # 5. Titolo sotto l'arco
        font_sub = QFont()
        font_sub.setPointSize(6)
        font_sub.setBold(True)
        painter.setFont(font_sub)
        painter.setPen(QColor(COLORS["text_muted"]))
        sub_rect = QRectF(0, float(rect.height()) - 10.0, float(rect.width()), 9.0)
        painter.drawText(sub_rect, Qt.AlignmentFlag.AlignCenter, self.title)

        painter.end()


class WeatherWidget(ModernCard):
    """Widget meteo premium con metriche cantiere e sfondi atmosferici cangianti.

    Inizializza il widget meteo configurando i servizi e avviando i timer di animazione.

    Args:
      parent: Widget genitore opzionale.

    Attributes:
        refresh_requested: Segnale o attributo della classe.
    """

    refresh_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(elevation=5, parent=parent)
        self.setMinimumWidth(360)

        # Inizializzazione parametri dinamici
        self.weather_service = WeatherService.instance()
        self._is_loading = False
        self._current_weather_style = "default"
        from src.application.services.config_manager import get_config_value

        self._showing_details = bool(get_config_value("weather_show_details", False))
        self._transitioning = False

        # Effetto particellare pioggia (Inizializzazione deterministica senza pseudo-random crittografici)
        self._rain_particles: list[list[float]] = [
            [(i * 20.0) % 360.0, -10.0 - (i * 15.0), 5.0 + (i % 4)] for i in range(18)
        ]

        self._setup_ui()
        self._connect_signals()

        # Timer di aggiornamento automatico (1 ora)
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.fetch_weather)
        self.refresh_timer.start(3600000)

        # Timer dell'orologio (1 secondo)
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self._update_clock)
        self.clock_timer.start(1000)

        # Timer per l'animazione degli effetti meteo (50ms ~ 20 FPS stabili)
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._animate_particles)
        self.anim_timer.start(50)

        # Primo avvio differito
        QTimer.singleShot(2000, self.fetch_weather)

    def _connect_signals(self) -> None:
        """Collega i segnali del servizio meteo alla UI del widget."""
        self.weather_service.weather_data_ready.connect(self._render_ui)
        self.weather_service.error_occurred.connect(self._handle_api_error)

    def _update_clock(self) -> None:
        """Aggiorna l'orologio dell'header in tempo reale."""
        if hasattr(self, "lbl_clock"):
            self.lbl_clock.setText(datetime.now(UTC).astimezone().strftime("%d/%m/%Y %H:%M"))

    def _animate_particles(self) -> None:
        """Aggiorna le posizioni delle particelle di pioggia in modo deterministico."""
        if self._current_weather_style == "rainy":
            for p in self._rain_particles:
                p[1] += p[2]
                if p[1] > self.height():
                    p[1] = -10.0
                    p[0] = (p[0] + 37.0) % float(self.width()) if self.width() > 0 else 100.0
            self.update()

    def _setup_ui(self) -> None:
        """Inizializza l'interfaccia grafica del widget."""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 12, 15, 10)
        self.main_layout.setSpacing(8)

        # 0. Alert Banner
        self._build_alert_banner()

        # 1. Header
        self._build_header()

        # 2. Body
        self._build_body()

        # 3. Separatore
        self._add_gradient_separator()

        # 4. Forecast Row
        self._build_forecast_area()

        # 5. Footer
        self._build_footer()

    def _build_alert_banner(self) -> None:
        """Costruisce il banner per le allerte meteo critiche."""
        self.alert_frame = QFrame()
        self.alert_frame.setObjectName("alert_banner")
        self.alert_frame.setStyleSheet(
            f"#alert_banner {{ background-color: #FFF3E0; border: 1px solid {COLORS['warning_orange']}; border-radius: 6px; }}"
        )
        self.alert_frame.hide()

        h = QHBoxLayout(self.alert_frame)
        h.setContentsMargins(8, 6, 8, 6)
        h.setSpacing(6)

        icon = QLabel()
        icon.setPixmap(get_colored_icon(get_asset_path(Icons.ALERT), COLORS["warning_orange"]).pixmap(16, 16))
        h.addWidget(icon)

        self.lbl_alert_msg = QLabel("Nessuna allerta")
        self.lbl_alert_msg.setObjectName("lbl_alert_msg")
        self.lbl_alert_msg.setStyleSheet(
            f"#lbl_alert_msg {{ color: {COLORS['warning_orange']}; font-size: 11px; font-weight: 800; }}"
        )
        h.addWidget(self.lbl_alert_msg)
        h.addStretch()

        self.main_layout.addWidget(self.alert_frame)

    def _build_header(self) -> None:
        """Costruisce l'intestazione del widget con orologio, alba/tramonto e pulsanti."""
        header_h = QHBoxLayout()
        header_h.setSpacing(8)

        badge = self._create_icon_badge(Icons.GLOBE, COLORS["primary_blue"], "#e8f4fd")
        header_h.addWidget(badge)

        lbl_title = QLabel("METEO CANTIERE")
        lbl_title.setObjectName("lbl_title")
        lbl_title.setStyleSheet(
            f"#lbl_title {{ color: {COLORS['text_dark']}; font-size: 13px; font-weight: 800; letter-spacing: 1.2px; background: transparent; border: none; }}"
        )
        header_h.addWidget(lbl_title)

        self.btn_refresh = QPushButton()
        self.btn_refresh.setIcon(get_colored_icon(get_asset_path(Icons.REFRESH), COLORS["text_muted"]))
        self.btn_refresh.setFixedSize(24, 24)
        self.btn_refresh.setObjectName("btn_refresh")
        self.btn_refresh.setStyleSheet(f"{TOOLTIP_CSS}\n{BUTTON_ICON_ONLY}")
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh.setToolTip("Aggiorna ora")
        self.btn_refresh.clicked.connect(self.fetch_weather)
        header_h.addWidget(self.btn_refresh)

        self.btn_details = QPushButton()
        self.btn_details.setIcon(get_colored_icon(get_asset_path(Icons.EYE), COLORS["text_muted"]))
        self.btn_details.setFixedSize(24, 24)
        self.btn_details.setObjectName("btn_details")
        self.btn_details.setStyleSheet(f"{TOOLTIP_CSS}\n{BUTTON_ICON_ONLY}")
        self.btn_details.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_details.setToolTip("Mostra dettagli avanzati HSE")
        self.btn_details.clicked.connect(self.toggle_details_view)
        header_h.addWidget(self.btn_details)

        header_h.addStretch()

        self.lbl_clock = QLabel()
        self.lbl_clock.setObjectName("lbl_clock")
        self.lbl_clock.setStyleSheet(
            f"#lbl_clock {{ color: {COLORS['text_muted']}; font-size: 12px; font-weight: 700; background: transparent; border: none; letter-spacing: 0.5px; }}"
        )
        self._update_clock()
        header_h.addWidget(self.lbl_clock)

        header_h.addSpacing(10)

        self.lbl_icon_sunrise = QLabel()
        self.lbl_icon_sunrise.setPixmap(
            get_colored_icon("assets/ui/icons/sunrise.svg", COLORS["text_muted"]).pixmap(12, 12)
        )
        header_h.addWidget(self.lbl_icon_sunrise)

        self.lbl_sunrise = QLabel("--:--")
        self.lbl_sunrise.setObjectName("lbl_sunrise")
        self.lbl_sunrise.setStyleSheet(
            f"#lbl_sunrise {{ color: {COLORS['text_muted']}; font-size: 11px; font-weight: 600; background: transparent; border: none; }}"
        )
        header_h.addWidget(self.lbl_sunrise)

        header_h.addSpacing(6)

        self.lbl_icon_sunset = QLabel()
        self.lbl_icon_sunset.setPixmap(
            get_colored_icon("assets/ui/icons/sunset.svg", COLORS["text_muted"]).pixmap(12, 12)
        )
        header_h.addWidget(self.lbl_icon_sunset)

        self.lbl_sunset = QLabel("--:--")
        self.lbl_sunset.setObjectName("lbl_sunset")
        self.lbl_sunset.setStyleSheet(
            f"#lbl_sunset {{ color: {COLORS['text_muted']}; font-size: 11px; font-weight: 600; background: transparent; border: none; }}"
        )
        header_h.addWidget(self.lbl_sunset)

        header_h.addStretch()

        self.lbl_location = QLabel("Priolo G. (SR)")
        self.lbl_location.setObjectName("lbl_location")
        self.lbl_location.setStyleSheet(
            f"#lbl_location {{ color: {COLORS['text_muted']}; font-size: 12px; font-weight: 700; background: transparent; border: none; }}"
        )
        header_h.addWidget(self.lbl_location)
        self.main_layout.addLayout(header_h)

    def _build_body(self) -> None:
        """Inizializza il corpo centrale della card con supporto QStackedWidget (SRP)."""
        body_h = QHBoxLayout()
        body_h.setSpacing(10)
        body_h.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # Colonna Sinistra (Statico: Icona principale e Temperatura)
        icon_v = QVBoxLayout()
        icon_v.setSpacing(2)
        icon_v.setContentsMargins(0, 0, 0, 0)

        lbl_today = QLabel("OGGI")
        lbl_today.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 10px; font-weight: 900; letter-spacing: 1.5px; background: transparent;"
        )
        lbl_today.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_v.addWidget(lbl_today, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.lbl_main_icon = QLabel()
        self.lbl_main_icon.setFixedSize(64, 64)
        self.lbl_main_icon.setObjectName("lbl_main_icon")
        self.lbl_main_icon.setStyleSheet(
            f"{TOOLTIP_CSS}\n#lbl_main_icon {{ background: transparent; border: none; }}"
        )
        icon_v.addWidget(self.lbl_main_icon, alignment=Qt.AlignmentFlag.AlignHCenter)
        body_h.addLayout(icon_v)

        temp_v = QVBoxLayout()
        temp_v.setSpacing(1)
        temp_v.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.lbl_temp = QLabel("--.- C")
        self.lbl_temp.setObjectName("lbl_temp")
        self.lbl_temp.setStyleSheet(
            f"#lbl_temp {{ color: {COLORS['text_dark']}; font-size: 36px; font-weight: 900; line-height: 1; background: transparent; border: none; }}"
        )

        self.temp_visualizer = TemperatureVisualizer()
        self.temp_visualizer.setToolTip("Divario visivo tra Temperatura Reale (◯) e Percepita (⚬)")
        self.temp_visualizer.setStyleSheet(TOOLTIP_CSS)

        self.lbl_apparent = QLabel("Percepita: -- ")
        self.lbl_apparent.setObjectName("lbl_apparent")
        self.lbl_apparent.setStyleSheet(
            f"#lbl_apparent {{ color: {COLORS['text_muted']}; font-size: 11px; font-weight: 600; background: transparent; border: none; }}"
        )

        self.lbl_condition = QLabel("Sincronizzazione...")
        self.lbl_condition.setObjectName("lbl_condition")
        self.lbl_condition.setStyleSheet(
            f"#lbl_condition {{ color: {COLORS['primary_blue']}; font-size: 12px; font-weight: 800; text-transform: uppercase; margin-top: 2px; background: transparent; border: none; }}"
        )

        temp_v.addWidget(self.lbl_temp)
        temp_v.addWidget(self.temp_visualizer)
        temp_v.addWidget(self.lbl_apparent)
        temp_v.addWidget(self.lbl_condition)
        body_h.addLayout(temp_v)

        # Stack Widget per alternare tra pannello standard e pannello dettagli avanzati
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("content_stack")
        self.content_stack.setStyleSheet("#content_stack { background: transparent; border: none; }")

        # ─── 1. PANNELLO STANDARD ───
        self.panel_standard = QFrame()
        self.panel_standard.setObjectName("panel_standard")
        self.panel_standard.setStyleSheet("#panel_standard { background: transparent; border: none; }")
        std_layout = QHBoxLayout(self.panel_standard)
        std_layout.setContentsMargins(0, 0, 0, 0)
        std_layout.setSpacing(6)

        # Contenitore verticale per Don Ciro e il bottone Dettagli
        don_ciro_container = QWidget()
        don_ciro_container.setObjectName("don_ciro_container")
        don_ciro_container.setStyleSheet("#don_ciro_container { background: transparent; border: none; }")
        don_ciro_v = QVBoxLayout(don_ciro_container)
        don_ciro_v.setContentsMargins(0, 0, 0, 0)
        don_ciro_v.setSpacing(4)
        don_ciro_v.setAlignment(Qt.AlignmentFlag.AlignCenter)

        from src.gui.widgets.dashboard.don_ciro_widget import DonCiroWidget

        self.don_ciro = DonCiroWidget()
        don_ciro_v.addWidget(self.don_ciro, alignment=Qt.AlignmentFlag.AlignCenter)

        self.btn_action_details = ModernButton(
            "Analisi Avanzata HSE ➔",
            variant=ModernButton.Variant.GHOST,
            size=ModernButton.Size.SMALL,
        )
        self.btn_action_details.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_action_details.setToolTip("Mostra l'analisi avanzata di inquinanti, vento e pollini")
        self.btn_action_details.clicked.connect(self.toggle_details_view)
        don_ciro_v.addWidget(self.btn_action_details, alignment=Qt.AlignmentFlag.AlignCenter)

        std_layout.addWidget(don_ciro_container)

        self._setup_metrics_gauges()
        std_layout.addWidget(self.gauges_container)
        self.content_stack.addWidget(self.panel_standard)

        # ─── 2. PANNELLO DETTAGLI AVANZATI ───
        self.panel_details = QFrame()
        self.panel_details.setObjectName("panel_details")
        self.panel_details.setStyleSheet("#panel_details { background: transparent; border: none; }")

        details_layout = QHBoxLayout(self.panel_details)
        details_layout.setContentsMargins(5, 0, 5, 0)
        details_layout.setSpacing(12)

        # Colonna Sinistra (Metriche Gas e Pollini HSE)
        gas_container = QFrame()
        gas_layout = QVBoxLayout(gas_container)
        gas_layout.setContentsMargins(0, 0, 0, 0)
        gas_layout.setSpacing(6)
        gas_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.bar_no2 = HseMetricBar("NO₂ (Biossido Azoto)", "µg/m³", 200.0, COLORS["warning_yellow"])
        self.bar_so2 = HseMetricBar("SO₂ (Anidride Solforosa)", "µg/m³", 350.0, COLORS["warning_orange"])
        self.bar_co = HseMetricBar("CO (Monossido Carbonio)", "µg/m³", 2000.0, COLORS["info_blue"])
        self.bar_olive = HseMetricBar("Pollini di Olivo", "grains/m³", 200.0, COLORS["teal_accent"])

        gas_layout.addWidget(self.bar_no2)
        gas_layout.addWidget(self.bar_so2)
        gas_layout.addWidget(self.bar_co)
        gas_layout.addWidget(self.bar_olive)
        details_layout.addWidget(gas_container)

        # Colonna Destra (Bussola e Pioggia/Nubi)
        right_container = QFrame()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(4)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.wind_compass = WindCompass()
        right_layout.addWidget(self.wind_compass, alignment=Qt.AlignmentFlag.AlignCenter)

        # Badges per Pioggia e Copertura Nuvolosa
        badges_h = QHBoxLayout()
        badges_h.setSpacing(4)
        badges_h.setContentsMargins(0, 2, 0, 0)

        badge_style = f"""
            color: {COLORS["text_dark"]};
            font-size: 8px;
            font-weight: 800;
            background-color: rgba(0, 0, 0, 0.03);
            border: 1px solid {COLORS["border_light"]};
            border-radius: 4px;
            padding: 3px 5px;
        """

        self.lbl_det_rain = QLabel("0.0 mm")
        self.lbl_det_rain.setToolTip("Precipitazioni reali cumulate")
        self.lbl_det_rain.setStyleSheet(badge_style + TOOLTIP_CSS)

        self.lbl_det_clouds = QLabel("0% NUBI")
        self.lbl_det_clouds.setToolTip("Copertura nuvolosa totale")
        self.lbl_det_clouds.setStyleSheet(badge_style + TOOLTIP_CSS)

        badges_h.addWidget(self.lbl_det_rain)
        badges_h.addWidget(self.lbl_det_clouds)
        right_layout.addLayout(badges_h)

        # Bottone di ritorno alla mascotte
        self.btn_back_to_mascot = ModernButton(
            "⬅ Torna alla Mascotte",
            variant=ModernButton.Variant.GHOST,
            size=ModernButton.Size.SMALL,
        )
        self.btn_back_to_mascot.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_back_to_mascot.setToolTip(
            "Ritorna alla visualizzazione della mascotte e delle metriche principali"
        )
        self.btn_back_to_mascot.clicked.connect(self.toggle_details_view)
        right_layout.addSpacing(4)
        right_layout.addWidget(self.btn_back_to_mascot, alignment=Qt.AlignmentFlag.AlignCenter)

        details_layout.addWidget(right_container)
        self.content_stack.addWidget(self.panel_details)

        # Aggiungiamo lo stack al layout orizzontale del corpo
        body_h.addWidget(self.content_stack)
        self.main_layout.addLayout(body_h)

        # Ripristina lo stato persistente dei dettagli del meteo
        if self._showing_details:
            self.content_stack.setCurrentIndex(1)
            self.btn_details.setIcon(get_colored_icon(get_asset_path(Icons.EYE_OFF), COLORS["primary_blue"]))
        else:
            self.content_stack.setCurrentIndex(0)
            self.btn_details.setIcon(get_colored_icon(get_asset_path(Icons.EYE), COLORS["text_muted"]))

    def _setup_metrics_gauges(self) -> None:
        """Configura la griglia 2x2 dei Mini Radial Gauge ambientali all'interno di un contenitore QFrame (SRP)."""
        self.gauges_container = QFrame()
        self.gauges_container.setObjectName("gauges_container")
        self.gauges_container.setStyleSheet("#gauges_container { background: transparent; border: none; }")

        self.grid_metrics = QGridLayout(self.gauges_container)
        self.grid_metrics.setSpacing(4)
        self.grid_metrics.setContentsMargins(0, 0, 0, 0)

        self.gauge_wind = MiniRadialGauge(
            "VENTO", 80.0, COLORS["info_blue"], "<b>Vento</b><br/>Velocità vento"
        )
        self.gauge_hum = MiniRadialGauge(
            "UMIDITÀ", 100.0, COLORS["teal_accent"], "<b>Umidità</b><br/>Umidità relativa"
        )
        self.gauge_uv = MiniRadialGauge(
            "UV INDEX", 12.0, COLORS["warning_orange"], "<b>Indice UV</b><br/>Radiazioni UV"
        )
        self.gauge_aqi = MiniRadialGauge(
            "AQI", 100.0, COLORS["success_green"], "<b>Qualità Aria</b><br/>Indice EU (0-100+)"
        )

        self.grid_metrics.addWidget(self.gauge_wind, 0, 0)
        self.grid_metrics.addWidget(self.gauge_hum, 0, 1)
        self.grid_metrics.addWidget(self.gauge_uv, 1, 0)
        self.grid_metrics.addWidget(self.gauge_aqi, 1, 1)

    def toggle_details_view(self) -> None:
        """Esegue una spettacolare animazione di rotazione del Don Ciro e dissolvenza dei dettagli."""
        if self._transitioning:
            return

        self._transitioning = True
        self.btn_details.setEnabled(False)
        if hasattr(self, "btn_action_details"):
            self.btn_action_details.setEnabled(False)
        if hasattr(self, "btn_back_to_mascot"):
            self.btn_back_to_mascot.setEnabled(False)

        if not self._showing_details:
            # Transizione a Dettagli Avanzati
            self.btn_details.setIcon(get_colored_icon(get_asset_path(Icons.EYE_OFF), COLORS["primary_blue"]))

            # 1. Configura l'effetto opacità per pannello standard
            self.opacity_standard = QGraphicsOpacityEffect(self.panel_standard)
            self.panel_standard.setGraphicsEffect(self.opacity_standard)

            # 2. Animazione Opacità Pannello Standard (fade out)
            self.anim_fade_std = QPropertyAnimation(self.opacity_standard, b"opacity")
            self.anim_fade_std.setDuration(500)
            self.anim_fade_std.setStartValue(1.0)
            self.anim_fade_std.setEndValue(0.0)
            self.anim_fade_std.setEasingCurve(QEasingCurve.Type.OutQuad)

            # 3. Animazione Rotazione Spettacolare di Don Ciro (spin)
            self.anim_spin_don = QPropertyAnimation(self.don_ciro, b"yaw_angle")
            self.anim_spin_don.setDuration(600)
            self.anim_spin_don.setStartValue(self.don_ciro._yaw_angle)
            self.anim_spin_don.setEndValue(self.don_ciro._yaw_angle + 720.0)
            self.anim_spin_don.setEasingCurve(QEasingCurve.Type.InOutCubic)

            # Collegamento al termine dell'animazione
            def on_std_fade_finished() -> None:
                """Callback al termine della dissolvenza del pannello standard."""
                self.content_stack.setCurrentIndex(1)

                # Configura l'effetto opacità per pannello dettagli
                self.opacity_details = QGraphicsOpacityEffect(self.panel_details)
                self.panel_details.setGraphicsEffect(self.opacity_details)

                # Animazione Opacità Pannello Dettagli (fade in)
                self.anim_fade_det = QPropertyAnimation(self.opacity_details, b"opacity")
                self.anim_fade_det.setDuration(400)
                self.anim_fade_det.setStartValue(0.0)
                self.anim_fade_det.setEndValue(1.0)
                self.anim_fade_det.setEasingCurve(QEasingCurve.Type.InQuad)

                def on_det_fade_finished() -> None:
                    """Callback al termine della comparsa dei dettagli avanzati."""
                    self.btn_details.setEnabled(True)
                    if hasattr(self, "btn_action_details"):
                        self.btn_action_details.setEnabled(True)
                    if hasattr(self, "btn_back_to_mascot"):
                        self.btn_back_to_mascot.setEnabled(True)
                    self._transitioning = False
                    self._showing_details = True
                    # Rimuoviamo l'effetto per non impattare sulle performance grafiche
                    self.panel_details.setGraphicsEffect(None)  # type: ignore[arg-type]
                    # Salva lo stato
                    from src.application.services.config_manager import set_config_value

                    set_config_value("weather_show_details", True)

                self.anim_fade_det.finished.connect(on_det_fade_finished)
                self.anim_fade_det.start()

            self.anim_fade_std.finished.connect(on_std_fade_finished)
            self.anim_fade_std.start()
            self.anim_spin_don.start()
        else:
            # Transizione di Ritorno alla Visualizzazione Standard
            self.btn_details.setIcon(get_colored_icon(get_asset_path(Icons.EYE), COLORS["text_muted"]))

            # 1. Configura l'effetto opacità per pannello dettagli
            self.opacity_details = QGraphicsOpacityEffect(self.panel_details)
            self.panel_details.setGraphicsEffect(self.opacity_details)

            # 2. Animazione Opacità Pannello Dettagli (fade out)
            self.anim_fade_det = QPropertyAnimation(self.opacity_details, b"opacity")
            self.anim_fade_det.setDuration(400)
            self.anim_fade_det.setStartValue(1.0)
            self.anim_fade_det.setEndValue(0.0)
            self.anim_fade_det.setEasingCurve(QEasingCurve.Type.OutQuad)

            def on_det_fade_out_finished() -> None:
                """Callback al termine della dissolvenza dei dettagli avanzati."""
                self.content_stack.setCurrentIndex(0)

                # Configura l'effetto opacità per pannello standard
                self.opacity_standard = QGraphicsOpacityEffect(self.panel_standard)
                self.panel_standard.setGraphicsEffect(self.opacity_standard)

                # Riavvolgiamo la rotazione di Don Ciro ruotando al contrario
                self.anim_spin_don = QPropertyAnimation(self.don_ciro, b"yaw_angle")
                self.anim_spin_don.setDuration(600)
                self.anim_spin_don.setStartValue(self.don_ciro._yaw_angle)
                self.anim_spin_don.setEndValue(self.don_ciro._yaw_angle - 720.0)
                self.anim_spin_don.setEasingCurve(QEasingCurve.Type.InOutCubic)

                # Animazione Opacità Pannello Standard (fade in)
                self.anim_fade_std = QPropertyAnimation(self.opacity_standard, b"opacity")
                self.anim_fade_std.setDuration(500)
                self.anim_fade_std.setStartValue(0.0)
                self.anim_fade_std.setEndValue(1.0)
                self.anim_fade_std.setEasingCurve(QEasingCurve.Type.InQuad)

                def on_std_fade_in_finished() -> None:
                    """Callback al termine della ricomparsa del pannello standard."""
                    self.btn_details.setEnabled(True)
                    if hasattr(self, "btn_action_details"):
                        self.btn_action_details.setEnabled(True)
                    if hasattr(self, "btn_back_to_mascot"):
                        self.btn_back_to_mascot.setEnabled(True)
                    self._transitioning = False
                    self._showing_details = False
                    self.panel_standard.setGraphicsEffect(None)  # type: ignore[arg-type]
                    # Normalizziamo l'angolo di Don Ciro
                    self.don_ciro.set_yaw_angle(0.0)
                    # Salva lo stato
                    from src.application.services.config_manager import set_config_value

                    set_config_value("weather_show_details", False)

                self.anim_fade_std.finished.connect(on_std_fade_in_finished)
                self.anim_fade_std.start()
                self.anim_spin_don.start()

            self.anim_fade_det.finished.connect(on_det_fade_out_finished)
            self.anim_fade_det.start()

    def _build_forecast_area(self) -> None:
        """Configura l'area dedicata alle previsioni meteo per i prossimi giorni."""
        self.forecast_container = QWidget()
        self.forecast_container.setObjectName("forecast_container")
        self.forecast_container.setStyleSheet(
            "#forecast_container { background: transparent; border: none; }"
        )
        self.forecast_h = QHBoxLayout(self.forecast_container)
        self.forecast_h.setContentsMargins(0, 4, 0, 0)
        self.forecast_h.setSpacing(6)
        self.main_layout.addWidget(self.forecast_container)

    def _build_footer(self) -> None:
        footer_h = QHBoxLayout()
        footer_h.setSpacing(6)

        self.lbl_updated = QLabel("In attesa di dati...")
        self.lbl_updated.setObjectName("lbl_updated")
        self.lbl_updated.setStyleSheet(
            f"#lbl_updated {{ color: {COLORS['text_light']}; font-size: 11px; font-style: italic; background: transparent; border: none; }}"
        )

        footer_h.addStretch()
        footer_h.addWidget(self.lbl_updated)
        self.main_layout.addLayout(footer_h)

    def _create_icon_badge(self, icon_key: str, icon_color: str, bg_color: str) -> QLabel:
        """Crea un piccolo badge circolare con un'icona SVG colorata."""
        badge = QLabel()
        badge.setFixedSize(28, 28)
        badge.setObjectName("icon_badge")
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(
            f"#icon_badge {{ background-color: {bg_color}; border-radius: 14px; border: none; }}"
        )
        badge.setPixmap(get_colored_icon(get_asset_path(icon_key), icon_color).pixmap(14, 14))
        return badge

    def _add_gradient_separator(self) -> None:
        """Aggiunge una sottile linea di separazione con gradiente orizzontale."""
        sep = QFrame()
        sep.setObjectName("gradient_sep")
        sep.setFixedHeight(1)
        sep.setStyleSheet(
            f"#gradient_sep {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 transparent, stop:0.2 {COLORS['border_light']}, stop:0.8 {COLORS['border_light']}, stop:1 transparent); border: none; }}"
        )
        self.main_layout.addWidget(sep)

    def fetch_weather(self) -> None:
        """Richiede l'aggiornamento dei dati meteo al servizio dedicato."""
        if self._is_loading:
            return

        self._is_loading = True
        self.btn_refresh.setEnabled(False)
        self.lbl_condition.setText("Aggiornamento...")
        self.weather_service.fetch_weather()

    def _handle_api_error(self, msg: str) -> None:
        """Gestisce gli errori notificati dal servizio."""
        self._is_loading = False
        self.btn_refresh.setEnabled(True)
        self.lbl_condition.setText(msg)
        self.lbl_condition.setStyleSheet(
            f"#lbl_condition {{ color: {COLORS['error_red']}; font-weight: 800; background: transparent; border: none; }}"
        )

    def _is_night(self, daily: dict[str, Any]) -> bool:
        try:
            sunrise_raw = daily.get("sunrise", [""])[0] if "sunrise" in daily else ""
            sunset_raw = daily.get("sunset", [""])[0] if "sunset" in daily else ""
            if sunrise_raw and sunset_raw:
                now_dt = datetime.now(UTC)
                s_rise_dt = datetime.strptime(sunrise_raw, "%Y-%m-%dT%H:%M").replace(tzinfo=UTC)
                s_set_dt = datetime.strptime(sunset_raw, "%Y-%m-%dT%H:%M").replace(tzinfo=UTC)

                now_time = now_dt.time()
                rise_time = s_rise_dt.time()
                set_time = s_set_dt.time()
                return now_time < rise_time or now_time > set_time
        except Exception:
            h = datetime.now(UTC).hour
            return h < 6 or h > 20
        return False

    def _determine_weather_style(self, code: int, daily: dict[str, Any]) -> str:
        """Determina lo stile del gradiente atmosferico."""
        if self._is_night(daily):
            return "night"

        sunny_code = 0
        if code == sunny_code:
            return "sunny"

        rain_start = 50
        if code >= rain_start:
            return "rainy"

        return "cloudy"

    def _render_ui(self, weather: dict[str, Any], aqi_res: dict[str, Any]) -> None:
        """Rendering finale dei dati ricevuti dal servizio meteo."""
        try:
            self._is_loading = False
            self.btn_refresh.setEnabled(True)

            curr = weather.get("current", {})
            daily = weather.get("daily", {})
            aqi_curr = aqi_res.get("current", {})

            # Estrazione dati correnti
            temp = float(curr.get("temperature_2m", 0.0))
            apparent = float(curr.get("apparent_temperature", 0.0))
            code = int(curr.get("weather_code", 0))
            wind = float(curr.get("wind_speed_10m", 0.0))
            gusts = float(curr.get("wind_gusts_10m", 0.0))
            hum = int(curr.get("relative_humidity_2m", 0))

            # Estrazione dati aggiuntivi per i dettagli cantiere
            precipitation = float(curr.get("precipitation", 0.0))
            cloud_cover = int(curr.get("cloud_cover", 0))
            wind_dir = float(curr.get("wind_direction_10m", 0.0))

            no2 = float(aqi_curr.get("nitrogen_dioxide", 0.0))
            so2 = float(aqi_curr.get("sulphur_dioxide", 0.0))
            co = float(aqi_curr.get("carbon_monoxide", 0.0))
            olive_pollen = float(aqi_curr.get("olive_pollen", 0.0))

            # Aggiornamento dei widget di dettaglio avanzati
            self.wind_compass.set_values(wind_dir, wind)
            self.bar_no2.set_value(no2)
            self.bar_so2.set_value(so2)
            self.bar_co.set_value(co)
            self.bar_olive.set_value(olive_pollen)
            self.lbl_det_rain.setText(f"{precipitation:.1f} mm")
            self.lbl_det_clouds.setText(f"{cloud_cover}% NUBI")

            # Estrazione range giornaliero per visualizzatore
            t_max_arr = daily.get("temperature_2m_max", [])
            t_min_arr = daily.get("temperature_2m_min", [])
            t_max = float(t_max_arr[0]) if t_max_arr else temp + 5.0
            t_min = float(t_min_arr[0]) if t_min_arr else temp - 5.0

            uv = float(daily.get("uv_index_max", [0.0])[0]) if daily else 0.0
            aqi_raw = aqi_curr.get("european_aqi", "--")
            aqi = 0.0 if aqi_raw == "--" else float(aqi_raw)

            # Aggiornamento dello stile atmosferico dinamico
            self._current_weather_style = self._determine_weather_style(code, daily)
            self.update()

            # Aggiornamento testi e termometro
            self.lbl_temp.setText(f"{int(temp)}°C")
            self.lbl_apparent.setText(f"Percepita: {int(apparent)}°")
            self.temp_visualizer.set_values(temp, apparent, t_min, t_max)

            self.lbl_condition.setText(self._get_condition_text(code))
            self.lbl_condition.setStyleSheet(
                f"#lbl_condition {{ color: {COLORS['primary_blue']}; font-weight: 800; background: transparent; border: none; }}"
            )

            # Aggiornamento metriche
            self._update_metrics(wind, gusts, hum, uv, aqi)
            self._evaluate_alerts(code, gusts)
            self._update_main_icon(code)
            self._update_forecast(daily)
            self._update_footer_info(daily)

        except Exception:
            logger.exception("Render UI Error in WeatherWidget")
            self._handle_api_error("Errore Visualizzazione")

    def _update_main_icon(self, code: int) -> None:
        """Aggiorna l'icona principale basata sul codice meteo."""
        icon_path, icon_color = self._get_weather_style(code)
        icon_size = 64
        self.lbl_main_icon.setPixmap(get_colored_icon(icon_path, icon_color).pixmap(icon_size, icon_size))
        self.lbl_main_icon.setToolTip(f"<b>Meteo Attuale</b><br/>{self._get_condition_text(code)}")

    def _update_footer_info(self, daily: dict[str, Any]) -> None:
        """Aggiorna le info di alba/tramonto e timestamp ultimo aggiornamento."""
        sunrise_raw = daily.get("sunrise", [""])[0] if "sunrise" in daily else ""
        sunset_raw = daily.get("sunset", [""])[0] if "sunset" in daily else ""

        if sunrise_raw and sunset_raw:
            s_rise = sunrise_raw.split("T")[1]
            s_set = sunset_raw.split("T")[1]
            self.lbl_sunrise.setText(s_rise)
            self.lbl_sunset.setText(s_set)
        else:
            self.lbl_sunrise.setText("--:--")
            self.lbl_sunset.setText("--:--")

        now_str = datetime.now().strftime("%H:%M")
        self.lbl_updated.setText(f"Aggiornato alle {now_str}")

    def _evaluate_alerts(self, code: int, gusts: float) -> None:
        """Valuta se le condizioni meteo attuali giustificano l'attivazione di un'allerta visiva."""
        alerts = []
        wind_gust_threshold = 45.0
        if gusts > wind_gust_threshold:
            alerts.append(f"Vento Forte ({gusts} km/h)")

        extreme_weather_codes = (65, 80, 81, 82, 95, 96, 99)
        if code in extreme_weather_codes:
            alerts.append("Precipitazioni Estreme")

        if alerts:
            self.lbl_alert_msg.setText(" - ".join(alerts))
            self.alert_frame.show()
        else:
            self.alert_frame.hide()

    def _update_metrics(self, wind: float, gusts: float, hum: int, uv: float, aqi: float) -> None:
        """Aggiorna i valori dei Mini Radial Gauge ambientali con i dati correnti."""
        self.gauge_wind.set_value(wind, str(int(wind)))
        self.gauge_wind.setToolTip(f"<b>Vento</b><br/>Medio: {wind} km/h<br/>Raffiche max: {gusts} km/h")

        self.gauge_hum.set_value(float(hum), f"{hum}%")

        self.gauge_uv.set_value(uv, str(uv))

        aqi_color = COLORS["success_green"]
        if aqi > AQI_MODERATE:
            aqi_color = COLORS["warning_yellow"]
        if aqi > AQI_UNHEALTHY_SENSITIVE:
            aqi_color = COLORS["warning_orange"]
        if aqi > AQI_UNHEALTHY:
            aqi_color = COLORS["error_red"]

        self.gauge_aqi.accent_color = aqi_color
        self.gauge_aqi.set_value(aqi, str(int(aqi)))

    def _update_forecast(self, daily: dict[str, Any]) -> None:
        """Ricarica la riga delle previsioni per i giorni successivi."""
        while self.forecast_h.count():
            child = self.forecast_h.takeAt(0)
            if child and (w := child.widget()):
                w.deleteLater()

        dates = daily.get("time", [])
        forecast_days = 5
        for i in range(1, forecast_days):
            if i >= len(dates):
                break
            self._add_forecast_item(i, dates[i], daily)

    def _add_forecast_item(self, i: int, date_str: str, daily: dict[str, Any]) -> None:
        """Aggiunge una bellissima mini-card Glassmorphic per il giorno delle previsioni."""
        t_max: list[float] = daily.get("temperature_2m_max", [])
        t_min: list[float] = daily.get("temperature_2m_min", [])
        codes: list[int] = daily.get("weather_code", [])
        pops: list[int] = daily.get("precipitation_probability_max", [])

        # Creazione mini-card individuale Glassmorphic
        item = QFrame()
        item.setObjectName(f"forecast_item_{i}")
        item.setStyleSheet(f"""
            #forecast_item_{i} {{
                background-color: rgba(255, 255, 255, 0.07);
                border: 1px solid {COLORS["border_light"]};
                border-radius: 8px;
            }}
            #forecast_item_{i}:hover {{
                background-color: rgba(255, 255, 255, 0.15);
                border: 1px solid {hex_to_rgba(COLORS["primary_blue"], 0.4)};
            }}
        """)

        v = QVBoxLayout(item)
        v.setContentsMargins(6, 6, 6, 6)
        v.setSpacing(3)
        v.setAlignment(Qt.AlignmentFlag.AlignCenter)

        dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=UTC)
        days = ["LUN", "MAR", "MER", "GIO", "VEN", "SAB", "DOM"]
        lbl_d = QLabel(days[dt.weekday()])
        lbl_d.setObjectName("forecast_day")
        lbl_d.setStyleSheet(
            f"#forecast_day {{ color: {COLORS['text_muted']}; font-size: 10px; font-weight: 800; background: transparent; border: none; }}"
        )
        lbl_d.setAlignment(Qt.AlignmentFlag.AlignCenter)

        f_code = codes[i] if i < len(codes) else 0
        path, color = self._get_weather_style(f_code)
        lbl_i = QLabel()
        forecast_icon_size = 20
        lbl_i.setPixmap(get_colored_icon(path, color).pixmap(forecast_icon_size, forecast_icon_size))
        lbl_i.setStyleSheet("background: transparent; border: none;")
        lbl_i.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pop_val = pops[i] if i < len(pops) else 0
        pop_threshold = 30
        lbl_pop = QLabel(f"{pop_val}%" if pop_val > pop_threshold else "")
        lbl_pop.setStyleSheet(
            f"color: {COLORS['primary_blue']}; font-size: 8px; font-weight: 900; background: transparent; border: none;"
        )
        lbl_pop.setAlignment(Qt.AlignmentFlag.AlignCenter)

        mx, mn = int(t_max[i]), int(t_min[i])
        lbl_t = QLabel(f"{mx}°/{mn}°")
        lbl_t.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-size: 10px; font-weight: 800; background: transparent; border: none;"
        )
        lbl_t.setAlignment(Qt.AlignmentFlag.AlignCenter)

        v.addWidget(lbl_d)
        v.addWidget(lbl_i)
        v.addWidget(lbl_pop)
        v.addWidget(lbl_t)
        self.forecast_h.addWidget(item)

    def _get_weather_style(self, code: int) -> tuple[str, str]:
        """Ritorna il percorso dell'icona e il colore associato al codice meteo WMO."""
        sunny_code = 0
        if code == sunny_code:
            return "assets/ui/icons/sun.svg", COLORS["warning_yellow"]
        cloudy_codes = (1, 2, 3)
        if code in cloudy_codes:
            return "assets/ui/icons/cloud-sun.svg", COLORS["primary_blue"]
        fog_codes = (45, 48)
        if code in fog_codes:
            return "assets/ui/icons/cloud-fog.svg", COLORS["text_muted"]
        rain_start = 50
        rain_end = 95
        if rain_start <= code < rain_end:
            return "assets/ui/icons/cloud-rain.svg", COLORS["primary_blue"]
        storm_start = 95
        if code >= storm_start:
            return "assets/ui/icons/cloud-lightning.svg", COLORS["warning_yellow"]
        return "assets/ui/icons/cloud.svg", COLORS["text_dark"]

    def _get_condition_text(self, code: int) -> str:
        """Traduce il codice meteo numerico WMO in una descrizione testuale in italiano."""
        return {
            0: "Sereno",
            1: "Quasi Sereno",
            2: "Parz. Nuvoloso",
            3: "Coperto",
            45: "Nebbia",
            51: "Pioggerellina",
            61: "Pioggia",
            65: "Pioggia Forte",
            80: "Rovesci",
            95: "Temporale",
        }.get(code, "Variabile")

    def paintEvent(self, event: QPaintEvent) -> None:
        """Esegue il rendering della pioggia live sopra lo sfondo standard di ModernCard."""
        # Chiamiamo prima super().paintEvent per disegnare lo sfondo e il bordo standard
        super().paintEvent(event)

        # Rendering degli effetti meteo live (pioggia inclinata leggera deterministica)
        if self._current_weather_style == "rainy":
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            rain_color = QColor(147, 197, 253, 90)  # Celeste pioggia semitrasparente
            painter.setPen(QPen(rain_color, 1.0))
            for p in self._rain_particles:
                painter.drawLine(int(p[0]), int(p[1]), int(p[0] - 2.0), int(p[1] + 6.0))

            painter.end()
