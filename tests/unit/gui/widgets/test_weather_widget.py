"""Unit tests for WeatherWidget."""

from unittest.mock import MagicMock

import pytest

from src.gui.widgets.dashboard.weather_widget import HseMetricBar, MiniRadialGauge, WeatherWidget


@pytest.fixture
def mock_weather_service(mocker):
    """Fixture per mockare WeatherService."""
    mock_instance = mocker.patch("src.core.weather_service.WeatherService.instance")
    service = MagicMock()
    mock_instance.return_value = service
    return service


@pytest.fixture
def weather_data():
    """Mock dei dati meteo."""
    return {
        "current": {
            "temperature_2m": 25.5,
            "apparent_temperature": 27.0,
            "weather_code": 0,
            "wind_speed_10m": 12.0,
            "wind_gusts_10m": 20.0,
            "relative_humidity_2m": 60,
            "precipitation": 0.0,
            "cloud_cover": 10,
            "wind_direction_10m": 180.0,
        },
        "daily": {
            "time": ["2026-05-24", "2026-05-25", "2026-05-26", "2026-05-27", "2026-05-28"],
            "temperature_2m_max": [28.0, 29.0, 27.0, 26.0, 25.0],
            "temperature_2m_min": [18.0, 19.0, 17.0, 16.0, 15.0],
            "weather_code": [0, 1, 3, 61, 0],
            "uv_index_max": [8.0, 7.5, 5.0, 2.0, 9.0],
            "precipitation_probability_max": [0, 10, 40, 80, 5],
            "sunrise": ["2026-05-24T05:45"],
            "sunset": ["2026-05-24T20:15"],
        },
    }


@pytest.fixture
def aqi_data():
    """Mock dei dati AQI."""
    return {
        "current": {
            "european_aqi": 35,
            "nitrogen_dioxide": 15.0,
            "sulphur_dioxide": 5.0,
            "carbon_monoxide": 300.0,
            "olive_pollen": 10.0,
        }
    }


class TestWeatherWidget:
    """Test suite per WeatherWidget."""

    def test_initialization(self, qtbot, mock_weather_service):
        """Verifica lbl'inizializzazione del widget."""
        widget = WeatherWidget()
        qtbot.addWidget(widget)

        assert widget.lbl_location.text() == "Priolo G. (SR)"
        assert widget.content_stack.count() == 2
        assert widget.refresh_timer.isActive()

    def test_render_ui_updates_labels(self, qtbot, mock_weather_service, weather_data, aqi_data):
        """Verifica che il rendering aggiorni correttamente le label principali."""
        widget = WeatherWidget()
        qtbot.addWidget(widget)

        # Simuliamo lbl'arrivo dei dati
        widget._render_ui(weather_data, aqi_data)

        assert "25°C" in widget.lbl_temp.text()
        assert "Percepita: 27°" in widget.lbl_apparent.text()
        assert "Sereno" in widget.lbl_condition.text()
        assert "05:45" in widget.lbl_sunrise.text()
        assert "20:15" in widget.lbl_sunset.text()

    def test_render_ui_updates_gauges(self, qtbot, mock_weather_service, weather_data, aqi_data):
        """Verifica lbl'aggiornamento dei micro-gauge."""
        widget = WeatherWidget()
        qtbot.addWidget(widget)

        widget._render_ui(weather_data, aqi_data)

        assert widget.gauge_wind.value == 12.0
        assert widget.gauge_hum.value == 60.0
        assert widget.gauge_uv.value == 8.0
        assert widget.gauge_aqi.value == 35.0

    def test_toggle_details_view(self, qtbot, mock_weather_service):
        """Verifica la transizione tra pannello standard e dettagli."""
        widget = WeatherWidget()
        qtbot.addWidget(widget)
        widget.show()

        # Stato iniziale: Standard (index 0)
        assert widget.content_stack.currentIndex() == 0

        # Toggle a dettagli
        widget.toggle_details_view()

        # Attendiamo la fine della prima animazione (fade out std)
        qtbot.wait(650)
        # Attendiamo la fine della seconda animazione (fade in det)
        qtbot.wait(550)

        assert widget.content_stack.currentIndex() == 1
        assert widget._showing_details is True

    def test_weather_style_determination(self, qtbot, mock_weather_service, mocker):
        """Verifica la logica di determinazione dello stile atmosferico."""
        from datetime import UTC, datetime

        # Mocking datetime.now to be at 12:00 UTC (daytime)
        mock_now = datetime(2026, 5, 24, 12, 0, tzinfo=UTC)
        mocker.patch("src.gui.widgets.dashboard.weather_widget.datetime", mocker.Mock(wraps=datetime))
        import src.gui.widgets.dashboard.weather_widget as ww

        ww.datetime.now.return_value = mock_now

        widget = WeatherWidget()
        qtbot.addWidget(widget)

        daily = {"sunrise": ["2026-05-24T06:00"], "sunset": ["2026-05-24T20:00"]}

        # Sunny
        assert widget._determine_weather_style(0, daily) == "sunny"
        # Rainy
        assert widget._determine_weather_style(61, daily) == "rainy"
        # Cloudy
        assert widget._determine_weather_style(3, daily) == "cloudy"

    def test_alert_banner_visibility(self, qtbot, mock_weather_service, weather_data, aqi_data):
        """Verifica lbl'attivazione del banner allerta per vento forte."""
        widget = WeatherWidget()
        qtbot.addWidget(widget)
        widget.show()

        # Forza vento forte
        weather_data["current"]["wind_gusts_10m"] = 80.0
        widget._render_ui(weather_data, aqi_data)

        assert widget.alert_frame.isVisible()
        assert "Vento Forte" in widget.lbl_alert_msg.text()

    def test_particle_animation_rain(self, qtbot, mock_weather_service):
        """Verifica che le particelle si muovano in modalità rain."""
        widget = WeatherWidget()
        qtbot.addWidget(widget)
        widget._current_weather_style = "rainy"
        widget.setFixedSize(400, 400)

        initial_y = widget._rain_particles[0][1]

        # Eseguiamo un ciclo di animazione
        widget._animate_particles()

        assert widget._rain_particles[0][1] > initial_y

    def test_api_error_handling(self, qtbot, mock_weather_service):
        """Verifica la gestione degli errori API."""
        from src.gui.styles import COLORS

        widget = WeatherWidget()
        qtbot.addWidget(widget)

        widget._handle_api_error("Connection Timeout")

        assert widget.lbl_condition.text() == "Connection Timeout"
        # Verifica colore errore (dc3545 o simile)
        assert COLORS["error_red"].lower() in widget.lbl_condition.styleSheet().lower()


class TestHseMetricBar:
    """Test per il widget HseMetricBar."""

    def test_hse_bar_rendering(self, qtbot):
        """Verifica impostazione valore e ridisegno."""
        bar = HseMetricBar("NO2", "ug", 100, "#ff0000")
        qtbot.addWidget(bar)

        bar.set_value(50.5)
        assert bar.value == 50.5


class TestMiniRadialGauge:
    """Test per il widget MiniRadialGauge."""

    def test_gauge_value(self, qtbot):
        """Verifica impostazione valore."""
        gauge = MiniRadialGauge("TEST", 100, "#00ff00", "tip")
        qtbot.addWidget(gauge)

        gauge.set_value(75, "75%")
        assert gauge.value == 75
        assert gauge.val_text == "75%"
