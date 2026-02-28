"""
SyncroJob - Weather Widget
Visualizza le previsioni meteo locali (Priolo Gargallo) utilizzando Open-Meteo.
V3.0: Design premium con badge icona, pill info, separatore gradient e forecast avanzato.
"""

import json
import logging
from datetime import UTC, datetime
from typing import Any

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.gui.widgets.modern_card import ModernCard
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class WeatherWidget(ModernCard):
    """Widget meteo avanzato con badge icona, pill info, e forecast min/max."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(elevation=5, parent=parent)
        self.setMinimumWidth(340)
        self.network_manager = QNetworkAccessManager(self)
        self._setup_ui()

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.fetch_weather)
        self.refresh_timer.start(3600000)

        QTimer.singleShot(3000, self.fetch_weather)

    # ── UI Setup ──────────────────────────────────────────────────────────

    def _setup_ui(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 12, 15, 10)
        self.main_layout.setSpacing(8)

        # 1. Header: Badge + Title + Location
        self._build_header()

        # 2. Body: Icon + Temp + Condition + Extra Info Pills
        self._build_body()

        # 3. Gradient Separator
        self._add_gradient_separator()

        # 4. Forecast Row (4 giorni)
        self._build_forecast_area()

        # 5. Footer aggiornamento
        self._build_footer()

    def _build_header(self) -> None:
        header_h = QHBoxLayout()
        header_h.setSpacing(10)

        # Badge icona circolare
        badge = self._create_icon_badge(Icons.GLOBE, COLORS["primary_blue"], "#e8f4fd")
        header_h.addWidget(badge)

        lbl_title = QLabel("METEO CANTIERE")
        lbl_title.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-size: 13px; font-weight: 800;"
            " letter-spacing: 1.2px; background: transparent; border: none;"
        )
        header_h.addWidget(lbl_title)
        header_h.addStretch()

        self.lbl_location = QLabel("Priolo G. (SR)")
        self.lbl_location.setStyleSheet(
            f"color: {COLORS['text_muted']}; font-size: 12px; font-weight: 700;"
            " background: transparent; border: none;"
        )
        header_h.addWidget(self.lbl_location)
        self.main_layout.addLayout(header_h)

    def _build_body(self) -> None:
        body_h = QHBoxLayout()
        body_h.setSpacing(16)

        # Icona meteo grande
        self.lbl_main_icon = QLabel()
        self.lbl_main_icon.setFixedSize(56, 56)
        self.lbl_main_icon.setStyleSheet("background: transparent; border: none;")
        body_h.addWidget(self.lbl_main_icon)

        # Temp + Condizione
        temp_v = QVBoxLayout()
        temp_v.setSpacing(2)

        self.lbl_temp = QLabel("--.-°C")
        self.lbl_temp.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-size: 42px; font-weight: 900;"
            " line-height: 1; background: transparent; border: none;"
        )
        self.lbl_condition = QLabel("Sincronizzazione...")
        self.lbl_condition.setStyleSheet(
            f"color: {COLORS['primary_blue']}; font-size: 14px; font-weight: 800;"
            " text-transform: uppercase; background: transparent; border: none;"
        )
        temp_v.addWidget(self.lbl_temp)
        temp_v.addWidget(self.lbl_condition)
        body_h.addLayout(temp_v)

        body_h.addStretch()

        # Extra Info Pills (Vento + Umidità)
        pills_v = QVBoxLayout()
        pills_v.setSpacing(6)
        pills_v.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.pill_wind = self._create_info_pill(Icons.ACTIVITY, "-- km/h", COLORS["info_blue"])
        self.pill_hum = self._create_info_pill(Icons.INFO, "--% UR", COLORS["teal_accent"])

        pills_v.addWidget(self.pill_wind)
        pills_v.addWidget(self.pill_hum)
        body_h.addLayout(pills_v)

        self.main_layout.addLayout(body_h)

    def _build_forecast_area(self) -> None:
        self.forecast_container = QWidget()
        self.forecast_container.setStyleSheet("background: transparent; border: none;")
        self.forecast_h = QHBoxLayout(self.forecast_container)
        self.forecast_h.setContentsMargins(0, 4, 0, 0)
        self.forecast_h.setSpacing(0)
        self.main_layout.addWidget(self.forecast_container)

    def _build_footer(self) -> None:
        self.lbl_updated = QLabel("In attesa di dati...")
        self.lbl_updated.setStyleSheet(
            f"color: {COLORS['text_light']}; font-size: 11px; font-style: italic;"
            " background: transparent; border: none;"
        )
        self.lbl_updated.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(self.lbl_updated)

    # ── Helpers di costruzione widget ─────────────────────────────────────

    def _create_icon_badge(self, icon_key: str, icon_color: str, bg_color: str) -> QLabel:
        """Badge circolare con icona SVG colorata."""
        badge = QLabel()
        badge.setFixedSize(28, 28)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(f"background-color: {bg_color}; border-radius: 14px; border: none;")
        icon_path = get_asset_path(icon_key)
        badge.setPixmap(get_colored_icon(icon_path, icon_color).pixmap(14, 14))
        return badge

    def _create_info_pill(self, icon_key: str, text: str, accent: str) -> QFrame:
        """Pill arrotondato con icona + testo per info secondarie."""
        pill = QFrame()
        pill.setStyleSheet(
            f"background-color: {COLORS['bg_light']}; border-radius: 14px;"
            f" border: 1px solid {COLORS['border_light']}; padding: 0px;"
        )
        pill.setFixedHeight(28)

        h = QHBoxLayout(pill)
        h.setContentsMargins(8, 0, 10, 0)
        h.setSpacing(5)

        icon_path = get_asset_path(icon_key)
        lbl_icon = QLabel()
        lbl_icon.setPixmap(get_colored_icon(icon_path, accent).pixmap(14, 14))
        lbl_icon.setStyleSheet("background: transparent; border: none;")
        h.addWidget(lbl_icon)

        lbl = QLabel(text)
        lbl.setObjectName("pill_text")
        lbl.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-size: 12px; font-weight: 700;"
            " background: transparent; border: none;"
        )
        h.addWidget(lbl)
        return pill

    def _add_gradient_separator(self) -> None:
        """Linea separatrice con gradient orizzontale."""
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(
            "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
            f" stop:0 transparent, stop:0.2 {COLORS['border_light']},"
            f" stop:0.8 {COLORS['border_light']}, stop:1 transparent);"
            " border: none;"
        )
        self.main_layout.addWidget(sep)

    # ── Network ───────────────────────────────────────────────────────────

    def fetch_weather(self) -> None:
        """Richiede i dati a Open-Meteo includendo vento, umidità e temp min."""
        url = (
            "https://api.open-meteo.com/v1/forecast?"
            "latitude=37.15&longitude=15.18&current_weather=True&"
            "hourly=relative_humidity_2m&"
            "daily=temperature_2m_max,temperature_2m_min,weathercode&"
            "timezone=Europe%2FRome"
        )
        request = QNetworkRequest(QUrl(url))
        reply = self.network_manager.get(request)
        if reply:
            reply.finished.connect(self._on_weather_received)

    def _on_weather_received(self) -> None:
        reply = self.sender()
        if not isinstance(reply, QNetworkReply):
            return

        try:
            if reply.error() != QNetworkReply.NetworkError.NoError:
                self.lbl_condition.setText("In attesa dati...")
                return

            raw_data = reply.readAll().data()
            if not raw_data:
                return

            data = json.loads(raw_data.decode("utf-8"))
            current = data.get("current_weather", {})

            temp = current.get("temperature", "--")
            code = current.get("weathercode", 0)
            wind = current.get("windspeed", 0.0)

            # Estrai umidità dall'ora corrente del blocco hourly
            hum = self._extract_current_humidity(data)

            self.lbl_temp.setText(f"{temp}°C")
            self.lbl_condition.setText(self._get_condition_text(code))
            self._update_pills(wind, hum)

            # Icona principale
            icon_path, icon_color = self._get_weather_style(code)
            self.lbl_main_icon.setPixmap(get_colored_icon(icon_path, icon_color).pixmap(56, 56))

            self._update_forecast(data.get("daily", {}))

            # Footer aggiornamento
            now = datetime.now(tz=UTC).strftime("%H:%M")
            self.lbl_updated.setText(f"Aggiornato alle {now}")

        except Exception as e:
            logger.error(f"Weather Update Error: {e}")
        finally:
            reply.deleteLater()

    def _extract_current_humidity(self, data: dict[str, Any]) -> int:
        """Estrae l'umidità relativa dall'ora corrente del blocco hourly."""
        try:
            hourly = data.get("hourly", {})
            hum_values = hourly.get("relative_humidity_2m", [])
            times = hourly.get("time", [])
            now_hour = datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:00")

            for i, t in enumerate(times):
                if t == now_hour and i < len(hum_values):
                    return int(hum_values[i])
        except Exception as e:
            logger.debug(f"Errore parsing umidita: {e}")
        return 65  # Default costiero Priolo

    def _update_pills(self, wind: float, hum: int) -> None:
        """Aggiorna il testo all'interno delle pill info."""
        wind_lbl = self.pill_wind.findChild(QLabel, "pill_text")
        hum_lbl = self.pill_hum.findChild(QLabel, "pill_text")
        if wind_lbl:
            wind_lbl.setText(f"{wind} km/h")
        if hum_lbl:
            hum_lbl.setText(f"{hum}% UR")

    def _update_forecast(self, daily: dict[str, Any]) -> None:
        # Pulizia robusta
        while self.forecast_h.count():
            child = self.forecast_h.takeAt(0)
            if child and (w := child.widget()):
                w.deleteLater()

        t_max = daily.get("temperature_2m_max", [])
        t_min = daily.get("temperature_2m_min", [])
        codes = daily.get("weathercode", [])
        dates = daily.get("time", [])

        for i in range(1, 5):
            if i >= len(dates):
                break

            item_widget = QWidget()
            item_widget.setStyleSheet("background: transparent; border: none;")
            item_v = QVBoxLayout(item_widget)
            item_v.setContentsMargins(0, 0, 0, 0)
            item_v.setSpacing(3)
            item_v.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Giorno
            dt = datetime.strptime(dates[i], "%Y-%m-%d").replace(tzinfo=UTC)
            # datetime.weekday() restituisce 0 per Lunedi, quindi correggiamo:
            ita_days_corr = ["LUN", "MAR", "MER", "GIO", "VEN", "SAB", "DOM"]
            d_name = ita_days_corr[dt.weekday()]
            lbl_d = QLabel(d_name)
            lbl_d.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_d.setStyleSheet(
                f"color: {COLORS['text_muted']}; font-size: 11px; font-weight: 800;"
                " background: transparent; border: none;"
            )

            # Icona meteo
            f_code = codes[i] if i < len(codes) else 0
            f_icon_path, f_color = self._get_weather_style(f_code)
            lbl_icon = QLabel()
            lbl_icon.setPixmap(get_colored_icon(f_icon_path, f_color).pixmap(24, 24))
            lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_icon.setStyleSheet("background: transparent; border: none;")

            # Temperatura Max / Min
            max_t = int(t_max[i]) if i < len(t_max) else "--"
            min_t = int(t_min[i]) if i < len(t_min) else "--"

            lbl_max = QLabel(f"{max_t}°")
            lbl_max.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_max.setStyleSheet(
                f"color: {COLORS['text_dark']}; font-size: 14px; font-weight: 800;"
                " background: transparent; border: none;"
            )

            lbl_min = QLabel(f"{min_t}°")
            lbl_min.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_min.setStyleSheet(
                f"color: {COLORS['text_light']}; font-size: 12px; font-weight: 600;"
                " background: transparent; border: none;"
            )

            item_v.addWidget(lbl_d)
            item_v.addWidget(lbl_icon)
            item_v.addWidget(lbl_max)
            item_v.addWidget(lbl_min)
            self.forecast_h.addWidget(item_widget)

    # ── Mapping meteo ─────────────────────────────────────────────────────

    def _get_weather_style(self, code: int) -> tuple[str, str]:
        """Mappa codice meteo a icona e colore."""
        if code == 0:
            return "assets/icons/sun.svg", COLORS["warning_yellow"]
        if code in (1, 2, 3):
            return "assets/icons/cloud-sun.svg", COLORS["primary_blue"]
        if code in (45, 48):
            return "assets/icons/cloud-fog.svg", COLORS["text_muted"]
        if 50 <= code < 95:
            return "assets/icons/cloud-rain.svg", COLORS["primary_blue"]
        if code >= 95:
            return "assets/icons/cloud-lightning.svg", COLORS["warning_yellow"]
        return "assets/icons/cloud.svg", COLORS["text_dark"]

    def _get_condition_text(self, code: int) -> str:
        return {
            0: "Sereno",
            1: "Prevalente sereno",
            2: "Nuvoloso",
            3: "Coperto",
            45: "Nebbia",
            48: "Nebbia fitta",
            51: "Pioggerellina",
            53: "Pioggia leggera",
            55: "Pioggia densa",
            61: "Pioggia",
            63: "Pioggia",
            65: "Pioggia Forte",
            80: "Rovesci",
            95: "Temporale",
        }.get(code, "Variabile")
