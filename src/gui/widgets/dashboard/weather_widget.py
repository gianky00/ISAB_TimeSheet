"""
SyncroJob - Weather Widget
Visualizza le previsioni meteo locali (Priolo Gargallo) utilizzando Open-Meteo.
V5.0: Alert Banner, AQI, Probabilità Pioggia, Raffiche di Vento e Alba/Tramonto.
"""

import json
import logging
from datetime import UTC, datetime
from typing import Any

from PyQt6.QtCore import Qt, QTimer, QUrl, pyqtSignal
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import BUTTON_ICON_ONLY, COLORS
from src.gui.widgets.modern_card import ModernCard
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)

# Stile forzato per evitare il bug della Dark Mode / Tooltip nero in PyQt6.
TOOLTIP_CSS = """
QToolTip {
    background-color: #FFFFFF;
    color: #212121;
    border: 1px solid #BBBBBB;
    border-radius: 6px;
    padding: 8px 12px;
}
"""

class WeatherWidget(ModernCard):
    """Widget meteo premium con metriche industriali per il cantiere."""

    refresh_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(elevation=5, parent=parent)
        self.setMinimumWidth(350)
        self.network_manager = QNetworkAccessManager(self)
        self._is_loading = False
        self._temp_weather_data: dict[str, Any] = {}
        self._setup_ui()

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.fetch_weather)
        self.refresh_timer.start(3600000)

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self._update_clock)
        self.clock_timer.start(1000)

        QTimer.singleShot(2000, self.fetch_weather)

    def _update_clock(self) -> None:
        """Aggiorna l'orologio dell'header in tempo reale."""
        if hasattr(self, "lbl_clock"):
            self.lbl_clock.setText(datetime.now().strftime("%d/%m/%Y %H:%M"))

    def _setup_ui(self) -> None:
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 12, 15, 10)
        self.main_layout.setSpacing(8)

        # 0. Alert Banner (Nascosto di default)
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
        self.lbl_alert_msg.setStyleSheet(f"#lbl_alert_msg {{ color: {COLORS['warning_orange']}; font-size: 11px; font-weight: 800; }}")
        h.addWidget(self.lbl_alert_msg)
        h.addStretch()

        self.main_layout.addWidget(self.alert_frame)

    def _build_header(self) -> None:
        header_h = QHBoxLayout()
        header_h.setSpacing(8)

        badge = self._create_icon_badge(Icons.GLOBE, COLORS["primary_blue"], "#e8f4fd")
        header_h.addWidget(badge)

        lbl_title = QLabel("METEO CANTIERE")
        lbl_title.setObjectName("lbl_title")
        lbl_title.setStyleSheet(f"#lbl_title {{ color: {COLORS['text_dark']}; font-size: 13px; font-weight: 800; letter-spacing: 1.2px; background: transparent; border: none; }}")
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

        header_h.addStretch()

        # Data e Ora
        self.lbl_clock = QLabel()
        self.lbl_clock.setObjectName("lbl_clock")
        self.lbl_clock.setStyleSheet(f"#lbl_clock {{ color: {COLORS['text_muted']}; font-size: 12px; font-weight: 700; background: transparent; border: none; letter-spacing: 0.5px; }}")
        self._update_clock()
        header_h.addWidget(self.lbl_clock)

        # Alba e Tramonto (Spostati qui per compattezza)
        header_h.addSpacing(10)

        self.lbl_icon_sunrise = QLabel()
        self.lbl_icon_sunrise.setPixmap(get_colored_icon("assets/icons/sunrise.svg", COLORS["text_muted"]).pixmap(12, 12))
        header_h.addWidget(self.lbl_icon_sunrise)

        self.lbl_sunrise = QLabel("--:--")
        self.lbl_sunrise.setObjectName("lbl_sunrise")
        self.lbl_sunrise.setStyleSheet(f"#lbl_sunrise {{ color: {COLORS['text_muted']}; font-size: 11px; font-weight: 600; background: transparent; border: none; }}")
        header_h.addWidget(self.lbl_sunrise)

        header_h.addSpacing(6)

        self.lbl_icon_sunset = QLabel()
        self.lbl_icon_sunset.setPixmap(get_colored_icon("assets/icons/sunset.svg", COLORS["text_muted"]).pixmap(12, 12))
        header_h.addWidget(self.lbl_icon_sunset)

        self.lbl_sunset = QLabel("--:--")
        self.lbl_sunset.setObjectName("lbl_sunset")
        self.lbl_sunset.setStyleSheet(f"#lbl_sunset {{ color: {COLORS['text_muted']}; font-size: 11px; font-weight: 600; background: transparent; border: none; }}")
        header_h.addWidget(self.lbl_sunset)

        header_h.addStretch()

        self.lbl_location = QLabel("Priolo G. (SR)")
        self.lbl_location.setObjectName("lbl_location")
        self.lbl_location.setStyleSheet(f"#lbl_location {{ color: {COLORS['text_muted']}; font-size: 12px; font-weight: 700; background: transparent; border: none; }}")
        header_h.addWidget(self.lbl_location)
        self.main_layout.addLayout(header_h)

    def _build_body(self) -> None:
        body_h = QHBoxLayout()
        body_h.setSpacing(16)
        body_h.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # Icona principale con etichetta "OGGI" centralizzata
        icon_v = QVBoxLayout()
        icon_v.setSpacing(2)
        icon_v.setContentsMargins(0, 0, 0, 0)

        lbl_today = QLabel("OGGI")
        lbl_today.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px; font-weight: 900; letter-spacing: 1.5px; background: transparent;")
        lbl_today.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_v.addWidget(lbl_today, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.lbl_main_icon = QLabel()
        self.lbl_main_icon.setFixedSize(64, 64)
        self.lbl_main_icon.setObjectName("lbl_main_icon")
        self.lbl_main_icon.setStyleSheet(f"{TOOLTIP_CSS}\n#lbl_main_icon {{ background: transparent; border: none; }}")
        icon_v.addWidget(self.lbl_main_icon, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        body_h.addLayout(icon_v)

        temp_v = QVBoxLayout()
        temp_v.setSpacing(0)
        temp_v.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.lbl_temp = QLabel("--.-°C")
        self.lbl_temp.setObjectName("lbl_temp")
        self.lbl_temp.setStyleSheet(f"#lbl_temp {{ color: {COLORS['text_dark']}; font-size: 38px; font-weight: 900; line-height: 1; background: transparent; border: none; }}")

        self.lbl_apparent = QLabel("Percepita: --°")
        self.lbl_apparent.setObjectName("lbl_apparent")
        self.lbl_apparent.setStyleSheet(f"#lbl_apparent {{ color: {COLORS['text_muted']}; font-size: 12px; font-weight: 600; background: transparent; border: none; }}")

        self.lbl_condition = QLabel("Sincronizzazione...")
        self.lbl_condition.setObjectName("lbl_condition")
        self.lbl_condition.setStyleSheet(f"#lbl_condition {{ color: {COLORS['primary_blue']}; font-size: 13px; font-weight: 800; text-transform: uppercase; margin-top: 4px; background: transparent; border: none; }}")

        temp_v.addWidget(self.lbl_temp)
        temp_v.addWidget(self.lbl_apparent)
        temp_v.addWidget(self.lbl_condition)
        body_h.addLayout(temp_v)

        body_h.addStretch()

        # 4 Pills: Vento, Umidità, UV, AQI
        pills_v = QVBoxLayout()
        pills_v.setSpacing(3)
        pills_v.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.pill_wind = self._create_info_pill(Icons.ACTIVITY, "-- km/h", COLORS["info_blue"], "<b>Vento</b><br/>Velocità attuale")
        self.pill_hum = self._create_info_pill(Icons.CLOUD, "--% UR", COLORS["teal_accent"], "<b>Umidità</b><br/>Umidità relativa")
        self.pill_uv = self._create_info_pill(Icons.SPARKLES, "UV: --", COLORS["warning_orange"], "<b>Indice UV</b><br/>Radiazioni UV")
        self.pill_aqi = self._create_info_pill(Icons.GLOBE, "AQI: --", COLORS["success_green"], "<b>Qualità Aria</b><br/>Indice EU (0-100+)")

        pills_v.addWidget(self.pill_wind)
        pills_v.addWidget(self.pill_hum)
        pills_v.addWidget(self.pill_uv)
        pills_v.addWidget(self.pill_aqi)
        body_h.addLayout(pills_v)

        self.main_layout.addLayout(body_h)

    def _build_forecast_area(self) -> None:
        self.forecast_container = QWidget()
        self.forecast_container.setObjectName("forecast_container")
        self.forecast_container.setStyleSheet("#forecast_container { background: transparent; border: none; }")
        self.forecast_h = QHBoxLayout(self.forecast_container)
        self.forecast_h.setContentsMargins(0, 4, 0, 0)
        self.forecast_h.setSpacing(0)
        self.main_layout.addWidget(self.forecast_container)

    def _build_footer(self) -> None:
        footer_h = QHBoxLayout()
        footer_h.setSpacing(6)

        self.lbl_updated = QLabel("In attesa di dati...")
        self.lbl_updated.setObjectName("lbl_updated")
        self.lbl_updated.setStyleSheet(f"#lbl_updated {{ color: {COLORS['text_light']}; font-size: 11px; font-style: italic; background: transparent; border: none; }}")

        footer_h.addStretch()
        footer_h.addWidget(self.lbl_updated)
        self.main_layout.addLayout(footer_h)

    # ── Helpers UI ────────────────────────────────────────────────────────

    def _create_icon_badge(self, icon_key: str, icon_color: str, bg_color: str) -> QLabel:
        badge = QLabel()
        badge.setFixedSize(28, 28)
        badge.setObjectName("icon_badge")
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(f"#icon_badge {{ background-color: {bg_color}; border-radius: 14px; border: none; }}")
        badge.setPixmap(get_colored_icon(get_asset_path(icon_key), icon_color).pixmap(14, 14))
        return badge

    def _create_info_pill(self, icon_key: str, text: str, accent: str, tooltip: str) -> QFrame:
        pill = QFrame()
        pill.setObjectName("info_pill")
        pill.setToolTip(tooltip)
        pill.setStyleSheet(f"{TOOLTIP_CSS}\n#info_pill {{ background-color: {COLORS['bg_light']}; border-radius: 10px; border: 1px solid {COLORS['border_light']}; padding: 0px; }}")
        pill.setFixedHeight(22) # Più compatto per ospitare 4 pill

        h = QHBoxLayout(pill)
        h.setContentsMargins(8, 0, 10, 0)
        h.setSpacing(5)

        lbl_icon = QLabel()
        lbl_icon.setObjectName("pill_icon")
        lbl_icon.setPixmap(get_colored_icon(get_asset_path(icon_key), accent).pixmap(11, 11))
        lbl_icon.setStyleSheet("#pill_icon { background: transparent; border: none; }")
        h.addWidget(lbl_icon)

        lbl = QLabel(text)
        lbl.setObjectName("pill_text")
        lbl.setStyleSheet(f"#pill_text {{ color: {COLORS['text_dark']}; font-size: 10px; font-weight: 700; background: transparent; border: none; }}")
        h.addWidget(lbl)
        return pill

    def _add_gradient_separator(self) -> None:
        sep = QFrame()
        sep.setObjectName("gradient_sep")
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"#gradient_sep {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 transparent, stop:0.2 {COLORS['border_light']}, stop:0.8 {COLORS['border_light']}, stop:1 transparent); border: none; }}")
        self.main_layout.addWidget(sep)

    # ── Logica API Chained ────────────────────────────────────────────────

    def fetch_weather(self) -> None:
        """Richiede i dati meteo principali (Step 1)."""
        if self._is_loading:
            return

        self._is_loading = True
        self.btn_refresh.setEnabled(False)
        self.lbl_condition.setText("Aggiornamento...")

        url_weather = (
            "https://api.open-meteo.com/v1/forecast?"
            "latitude=37.15&longitude=15.18&"
            "current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m,wind_gusts_10m&"
            "daily=temperature_2m_max,temperature_2m_min,weather_code,uv_index_max,precipitation_probability_max,sunrise,sunset&"
            "timezone=Europe%2FRome"
        )
        req = QNetworkRequest(QUrl(url_weather))
        reply = self.network_manager.get(req)
        if reply:
            reply.finished.connect(self._on_weather_received)

    def _on_weather_received(self) -> None:
        reply = self.sender()
        if not isinstance(reply, QNetworkReply):
            return

        if reply.error() != QNetworkReply.NetworkError.NoError:
            self._handle_api_error("Errore Rete")
            reply.deleteLater()
            return

        try:
            self._temp_weather_data = json.loads(reply.readAll().data().decode("utf-8"))
            # Step 2: Fetch Air Quality (AQI)
            url_aqi = (
                "https://air-quality-api.open-meteo.com/v1/air-quality?"
                "latitude=37.15&longitude=15.18&"
                "current=european_aqi,pm10,pm2_5&"
                "timezone=Europe%2FRome"
            )
            req_aqi = QNetworkRequest(QUrl(url_aqi))
            reply_aqi = self.network_manager.get(req_aqi)
            if reply_aqi:
                reply_aqi.finished.connect(self._on_aqi_received)
        except Exception as e:
            logger.error(f"Parse error Weather: {e}")
            self._handle_api_error("Errore Parsing")
        finally:
            reply.deleteLater()

    def _on_aqi_received(self) -> None:
        """Riceve l'AQI e aggiorna la UI combinando i due dataset (Step 2)."""
        reply = self.sender()
        if not isinstance(reply, QNetworkReply):
            return

        aqi_data = {}
        if reply.error() == QNetworkReply.NetworkError.NoError:
            try:
                aqi_data = json.loads(reply.readAll().data().decode("utf-8"))
            except Exception as e:
                logger.error(f"Errore caricamento dati AQI: {e}")

        reply.deleteLater()
        self._is_loading = False
        self.btn_refresh.setEnabled(True)
        self._render_ui(self._temp_weather_data, aqi_data)

    def _handle_api_error(self, msg: str) -> None:
        self._is_loading = False
        self.btn_refresh.setEnabled(True)
        self.lbl_condition.setText(msg)
        self.lbl_condition.setStyleSheet(f"#lbl_condition {{ color: {COLORS['error_red']}; font-weight: 800; }}")

    # ── Rendering UI ──────────────────────────────────────────────────────

    def _render_ui(self, weather: dict[str, Any], aqi_res: dict[str, Any]) -> None:
        try:
            curr = weather.get("current", {})
            daily = weather.get("daily", {})
            aqi_curr = aqi_res.get("current", {})

            # Dati Correnti
            temp = curr.get("temperature_2m", "--")
            apparent = curr.get("apparent_temperature", "--")
            code = curr.get("weather_code", 0)
            wind = curr.get("wind_speed_10m", 0.0)
            gusts = curr.get("wind_gusts_10m", 0.0)
            hum = curr.get("relative_humidity_2m", 0)
            uv = daily.get("uv_index_max", [0])[0] if daily else 0
            aqi = aqi_curr.get("european_aqi", "--")

            self.lbl_temp.setText(f"{temp}°C")
            self.lbl_apparent.setText(f"Percepita: {apparent}°")
            self.lbl_condition.setText(self._get_condition_text(code))
            self.lbl_condition.setStyleSheet(f"#lbl_condition {{ color: {COLORS['primary_blue']}; font-weight: 800; }}")

            self._update_pills(wind, gusts, hum, uv, aqi)
            self._evaluate_alerts(code, gusts)

            # Icona principale
            icon_path, icon_color = self._get_weather_style(code)
            self.lbl_main_icon.setPixmap(get_colored_icon(icon_path, icon_color).pixmap(64, 64))
            self.lbl_main_icon.setToolTip(f"<b>Meteo Attuale</b><br/>{self._get_condition_text(code)}")

            self._update_forecast(daily)

            # Footer: Alba/Tramonto e Orario
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

            now = datetime.now(tz=UTC).strftime("%H:%M")
            self.lbl_updated.setText(f"Aggiornato alle {now}")

        except Exception as e:
            logger.error(f"Render UI Error: {e}")
            self._handle_api_error("Errore Visualizzazione")

    def _evaluate_alerts(self, code: int, gusts: float) -> None:
        """Mostra il banner di allerta se ci sono condizioni estreme."""
        alerts = []
        if gusts > 45.0:
            alerts.append(f"Vento Forte (Raffiche {gusts} km/h)")
        if code in (65, 80, 81, 82, 95, 96, 99):
            alerts.append("Precipitazioni Estreme/Temporale")

        if alerts:
            self.lbl_alert_msg.setText(" - ".join(alerts))
            self.alert_frame.show()
        else:
            self.alert_frame.hide()

    def _update_pills(self, wind: float, gusts: float, hum: int, uv: float, aqi: Any) -> None:
        w_lbl = self.pill_wind.findChild(QLabel, "pill_text")
        h_lbl = self.pill_hum.findChild(QLabel, "pill_text")
        u_lbl = self.pill_uv.findChild(QLabel, "pill_text")
        a_lbl = self.pill_aqi.findChild(QLabel, "pill_text")

        if w_lbl:
            w_lbl.setText(f"{wind} km/h")
            self.pill_wind.setToolTip(f"<b>Vento</b><br/>Medio: {wind} km/h<br/>Raffiche max: {gusts} km/h")
        if h_lbl:
            h_lbl.setText(f"{hum}% UR")
        if u_lbl:
            u_lbl.setText(f"UV: {uv}")
        if a_lbl:
            a_lbl.setText(f"AQI: {aqi}")

            # Dinamismo colore AQI
            aqi_color = COLORS["success_green"]
            aqi_val = 0 if aqi == "--" else int(aqi)
            if aqi_val > 40:
                aqi_color = COLORS["warning_yellow"]
            if aqi_val > 60:
                aqi_color = COLORS["warning_orange"]
            if aqi_val > 80:
                aqi_color = COLORS["error_red"]

            i_lbl = self.pill_aqi.findChild(QLabel, "pill_icon")
            if i_lbl:
                i_lbl.setPixmap(get_colored_icon(get_asset_path(Icons.GLOBE), aqi_color).pixmap(11, 11))

    def _update_forecast(self, daily: dict[str, Any]) -> None:
        while self.forecast_h.count():
            child = self.forecast_h.takeAt(0)
            if child and (w := child.widget()):
                w.deleteLater()

        t_max = daily.get("temperature_2m_max", [])
        t_min = daily.get("temperature_2m_min", [])
        codes = daily.get("weather_code", [])
        pops = daily.get("precipitation_probability_max", [])
        dates = daily.get("time", [])

        for i in range(1, 5):
            if i >= len(dates):
                break

            item = QWidget()
            item.setObjectName(f"forecast_item_{i}")
            item.setStyleSheet(f"{TOOLTIP_CSS}\n#forecast_item_{i} {{ background: transparent; border: none; }}")

            v = QVBoxLayout(item)
            v.setContentsMargins(0, 0, 0, 0)
            v.setSpacing(1)
            v.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Giorno
            dt = datetime.strptime(dates[i], "%Y-%m-%d").replace(tzinfo=UTC)
            days = ["LUN", "MAR", "MER", "GIO", "VEN", "SAB", "DOM"]
            lbl_d = QLabel(days[dt.weekday()])
            lbl_d.setObjectName("forecast_day")
            lbl_d.setStyleSheet(f"#forecast_day {{ color: {COLORS['text_muted']}; font-size: 10px; font-weight: 800; }}")
            lbl_d.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Icona
            f_code = codes[i] if i < len(codes) else 0
            path, color = self._get_weather_style(f_code)
            lbl_i = QLabel()
            lbl_i.setPixmap(get_colored_icon(path, color).pixmap(22, 22))
            lbl_i.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # POP (Probabilità Pioggia)
            pop_val = pops[i] if i < len(pops) else 0
            lbl_pop = QLabel(f"💧 {pop_val}%" if pop_val > 0 else "")
            lbl_pop.setObjectName("forecast_pop")
            pop_color = COLORS['primary_blue'] if pop_val > 40 else COLORS['text_muted']
            lbl_pop.setStyleSheet(f"#forecast_pop {{ color: {pop_color}; font-size: 9px; font-weight: 800; }}")
            lbl_pop.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Temp
            mx, mn = int(t_max[i]), int(t_min[i])
            lbl_t = QLabel(f"{mx}°/{mn}°")
            lbl_t.setObjectName("forecast_temp")
            lbl_t.setStyleSheet(f"#forecast_temp {{ color: {COLORS['text_dark']}; font-size: 11px; font-weight: 700; }}")
            lbl_t.setAlignment(Qt.AlignmentFlag.AlignCenter)

            v.addWidget(lbl_d)
            v.addWidget(lbl_i)
            if pop_val > 0:
                v.addWidget(lbl_pop) # Aggiunge POP solo se > 0%
            v.addWidget(lbl_t)

            pop_text = f"<br/>Pioggia: {pop_val}%" if pop_val > 0 else ""
            item.setToolTip(f"<b>Previsione {days[dt.weekday()]}</b><br/>{self._get_condition_text(f_code)}{pop_text}")
            self.forecast_h.addWidget(item)

    def _get_weather_style(self, code: int) -> tuple[str, str]:
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
