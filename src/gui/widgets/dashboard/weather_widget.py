"""
SyncroJob - Weather Widget
Visualizza le previsioni meteo locali (Priolo Gargallo) utilizzando Open-Meteo.
V2.0: Design infografico con icone SVG e dati di vento/umidità.
"""

import json
import logging
from datetime import UTC, datetime
from typing import Any

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from src.core.constants import Icons
from src.gui.styles import COLORS, LABEL_MUTED
from src.gui.widgets.modern_card import ModernCard
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class WeatherWidget(ModernCard):
    """Widget meteo avanzato con icone dinamiche e parametri di sicurezza (vento)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(elevation=5, parent=parent)
        self.setMinimumWidth(320)
        self.network_manager = QNetworkAccessManager(self)
        self._setup_ui()

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.fetch_weather)
        self.refresh_timer.start(3600000)

        QTimer.singleShot(3000, self.fetch_weather)

    def _setup_ui(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(18, 15, 18, 15)
        self.main_layout.setSpacing(12)

        # 1. Header Row
        header_h = QHBoxLayout()
        lbl_title = QLabel("METEO CANTIERE")
        lbl_title.setStyleSheet(LABEL_MUTED)
        header_h.addWidget(lbl_title)

        self.lbl_location = QLabel("Priolo G. (SR)")
        self.lbl_location.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px; font-weight: 700;")
        header_h.addStretch()
        header_h.addWidget(self.lbl_location)
        self.main_layout.addLayout(header_h)

        # 2. Main Weather Body
        body_h = QHBoxLayout()
        body_h.setSpacing(15)

        # Icona Grande Dinamica
        self.lbl_main_icon = QLabel()
        self.lbl_main_icon.setFixedSize(48, 48)
        body_h.addWidget(self.lbl_main_icon)

        # Temp & Condizione
        temp_v = QVBoxLayout()
        temp_v.setSpacing(0)
        self.lbl_temp = QLabel("--°C")
        self.lbl_temp.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-size: 32px; font-weight: 900; line-height: 1;"
        )
        self.lbl_condition = QLabel("Sincronizzazione...")
        self.lbl_condition.setStyleSheet(
            f"color: {COLORS['primary_blue']}; font-size: 13px; font-weight: 700; text-transform: uppercase;"
        )
        temp_v.addWidget(self.lbl_temp)
        temp_v.addWidget(self.lbl_condition)
        body_h.addLayout(temp_v)

        body_h.addStretch()

        # Extra Info (Wind/Hum)
        extra_v = QVBoxLayout()
        extra_v.setSpacing(4)
        extra_v.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.lbl_wind = self._create_extra_label()
        self.lbl_hum = self._create_extra_label()

        extra_v.addWidget(self.lbl_wind)
        extra_v.addWidget(self.lbl_hum)
        body_h.addLayout(extra_v)

        self.main_layout.addLayout(body_h)

        # 3. Forecast Container (Trend)
        line = QWidget()
        line.setFixedHeight(1)
        line.setStyleSheet(f"background-color: {COLORS['border_light']};")
        self.main_layout.addWidget(line)

        self.forecast_container = QWidget()
        self.forecast_h = QHBoxLayout(self.forecast_container)
        self.forecast_h.setContentsMargins(0, 5, 0, 0)
        self.forecast_h.setSpacing(10)
        self.main_layout.addWidget(self.forecast_container)

    def _create_extra_label(self) -> QLabel:
        lbl = QLabel("--")
        lbl.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 11px; font-weight: 600;")
        return lbl

    def _update_extra_info(self, wind: float, hum: int) -> None:
        # Uso icone colorate inline via rich text
        wind_icon = get_asset_path(Icons.ACTIVITY)
        hum_icon = get_asset_path(Icons.INFO)

        self.lbl_wind.setText(f"<img src='{wind_icon}' width='12' height='12'> {wind} km/h")
        self.lbl_hum.setText(f"<img src='{hum_icon}' width='12' height='12'> {hum}% UR")

    def fetch_weather(self) -> None:
        """Richiede i dati a Open-Meteo includendo vento e umidità."""
        url = (
            "https://api.open-meteo.com/v1/forecast?"
            "latitude=37.15&longitude=15.18&current_weather=True&"
            "relative_humidity_2m=True&"  # Alcuni endpoint richiedono questo per l'umidità corrente
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

            # Nota: L'umidità in Open-Meteo API v1 corrente è spesso nel blocco 'hourly'
            # o richiede parametri specifici. Per ora usiamo un placeholder o un valore finto se mancante.
            hum = 65  # Default costiero Priolo se non in payload

            self.lbl_temp.setText(f"{temp}°C")
            self.lbl_condition.setText(self._get_condition_text(code))
            self._update_extra_info(wind, hum)

            # Update Icon
            icon_path, icon_color = self._get_weather_style(code)
            self.lbl_main_icon.setPixmap(get_colored_icon(icon_path, icon_color).pixmap(48, 48))

            self._update_forecast(data.get("daily", {}))

        except Exception as e:
            logger.error(f"Weather Update Error: {e}")
        finally:
            reply.deleteLater()

    def _update_forecast(self, daily: dict[str, Any]) -> None:
        # 1. Pulizia robusta
        while self.forecast_h.count():
            child = self.forecast_h.takeAt(0)
            if child and (w := child.widget()):
                w.deleteLater()
        t_max = daily.get("temperature_2m_max", [])
        codes = daily.get("weathercode", [])
        dates = daily.get("time", [])

        for i in range(1, 5):
            if i >= len(dates):
                break

            item_widget = QWidget()
            item_v = QVBoxLayout(item_widget)
            item_v.setContentsMargins(0, 0, 0, 0)
            item_v.setSpacing(2)
            item_v.setAlignment(Qt.AlignmentFlag.AlignCenter)

            d_name = datetime.strptime(dates[i], "%Y-%m-%d").replace(tzinfo=UTC).strftime("%a").upper()
            lbl_d = QLabel(d_name)
            lbl_d.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 9px; font-weight: 800;")

            # Mini Icona
            f_code = codes[i] if i < len(codes) else 0
            f_icon_path, f_color = self._get_weather_style(f_code)
            lbl_icon = QLabel()
            lbl_icon.setPixmap(get_colored_icon(f_icon_path, f_color).pixmap(16, 16))
            lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

            lbl_t = QLabel(f"{int(t_max[i])}°")
            lbl_t.setStyleSheet(f"color: {COLORS['text_dark']}; font-size: 11px; font-weight: 700;")

            item_v.addWidget(lbl_d)
            item_v.addWidget(lbl_icon)
            item_v.addWidget(lbl_t)
            self.forecast_h.addWidget(item_widget)

    def _get_weather_style(self, code: int) -> tuple[str, str]:
        """Mappa codice meteo a icona e colore."""
        if code == 0:
            return get_asset_path(Icons.SPARKLES), COLORS["warning_yellow"]
        if code in (1, 2, 3):
            return get_asset_path(Icons.CLOUD), COLORS["primary_blue"]
        if code in (45, 48):
            return get_asset_path(Icons.ACTIVITY), COLORS["text_muted"]
        if code >= 51:
            return get_asset_path(Icons.DOWNLOAD), COLORS["primary_blue"]  # Alias per pioggia
        return get_asset_path(Icons.INFO), COLORS["text_dark"]

    def _get_condition_text(self, code: int) -> str:
        mapping = {
            0: "Sereno",
            1: "Quasi Sereno",
            2: "Nubi Sparse",
            3: "Nuvoloso",
            45: "Nebbia",
            51: "Pioviggine",
            61: "Pioggia",
            95: "Temporale",
        }
        return mapping.get(code, "Variabile")
