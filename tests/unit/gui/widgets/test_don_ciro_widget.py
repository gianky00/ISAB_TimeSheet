"""Unit tests for DonCiroWidget."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QPropertyAnimation

from src.core.mascot.don_ciro_engine import DonState, WeatherCond
from src.gui.widgets.dashboard.don_ciro_widget import DonCiroWidget


@pytest.fixture
def mock_weather_service(mocker):
    """Fixture per mockare WeatherService."""
    mock_instance = mocker.patch("src.core.weather_service.WeatherService.instance")
    service = MagicMock()
    mock_instance.return_value = service
    return service


@pytest.fixture
def widget(qtbot, mock_weather_service, mocker):
    """Istanza di DonCiroWidget con engine mockato."""
    # Mock dell'engine per evitare thread fisici
    mocker.patch("src.gui.widgets.dashboard.don_ciro_widget.DonCiroEngine")
    w = DonCiroWidget()
    qtbot.addWidget(w)
    return w


class TestDonCiroWidget:
    """Test suite per DonCiroWidget."""

    def test_initialization(self, widget):
        """Verifica lbl'inizializzazione del widget."""
        assert widget.width() == 280
        assert widget.height() == 180
        assert widget.renderer is not None
        assert widget.walk_anim.state() == QPropertyAnimation.State.Running

    def test_properties_and_signals(self, qtbot, widget):
        """Verifica le proprietà animate e i segnali associati."""
        # Walk phase
        with qtbot.waitSignal(widget.walk_phase_changed):
            widget.set_walk_phase(0.75)
        assert widget.get_walk_phase() == 0.75

        # Action phase
        with qtbot.waitSignal(widget.action_phase_changed):
            widget.set_action_phase(0.5)
        assert widget.get_action_phase() == 0.5

        # Yaw angle
        with qtbot.waitSignal(widget.yaw_angle_changed):
            widget.set_yaw_angle(180.0)
        assert widget.get_yaw_angle() == 180.0

        # Blink
        with qtbot.waitSignal(widget.blink_changed):
            widget.set_blink(0.0)
        assert widget.get_blink() == 0.0

    def test_on_real_weather_received(self, widget):
        """Verifica lbl'adattamento al meteo reale."""
        # Simuliamo pioggia
        weather = {"current": {"weather_code": 61, "wind_gusts_10m": 10.0}}
        widget._on_real_weather_received(weather, {})
        assert widget.engine.weather == WeatherCond.RAINY

        # Simuliamo vento forte
        weather = {"current": {"weather_code": 0, "wind_gusts_10m": 50.0}}
        widget._on_real_weather_received(weather, {})
        assert widget.engine.weather == WeatherCond.WINDY

        # Simuliamo sereno
        weather = {"current": {"weather_code": 0, "wind_gusts_10m": 5.0}}
        widget._on_real_weather_received(weather, {})
        assert widget.engine.weather == WeatherCond.SUNNY

    def test_engine_state_sync_walking(self, widget):
        """Verifica la sincronizzazione animazione walk."""
        # Se lbl'engine va in IDLE, lbl'animazione camminata deve mettersi in pausa
        widget._on_engine_state_changed(DonState.IDLE)
        assert widget.walk_anim.state() == QPropertyAnimation.State.Paused

        # Se torna in WALKING, deve riprendere
        widget._on_engine_state_changed(DonState.WALKING)
        assert widget.walk_anim.state() == QPropertyAnimation.State.Running

    def test_trigger_ui_turn(self, qtbot, widget):
        """Verifica lbl'attivazione dell'animazione di rotazione."""
        widget.engine.look_dir = 1
        widget._yaw_angle = 0.0

        widget._trigger_ui_turn()

        assert hasattr(widget, "ta")
        assert widget.ta.endValue() == 180.0
        assert widget.ta.state() == QPropertyAnimation.State.Running

    def test_trigger_ui_action(self, widget):
        """Verifica lbl'attivazione dell'animazione azione."""
        widget._trigger_ui_action()

        assert hasattr(widget, "act")
        assert widget.act.startValue() == 0.0
        assert widget.act.endValue() == 1.0

    def test_do_blink(self, widget):
        """Verifica il battito di ciglia."""
        widget._do_blink()

        assert hasattr(widget, "ba")
        assert widget.ba.state() == QPropertyAnimation.State.Running

    def test_paint_event_delegation(self, widget, mocker):
        """Verifica che paintEvent deleghi al renderer."""
        # Mocking renderer per non fare disegno reale
        mock_render = mocker.patch.object(widget.renderer, "render")

        # Chiamata manuale a paintEvent (richiede un QPaintEvent, ma passiamo None per triggerare)
        # In alternativa chiamiamo update() e facciamo processare gli eventi
        widget.update()
        # Per i test unitari GUI, a volte è meglio chiamare direttamente il metodo protetto
        widget.paintEvent(None)

        assert mock_render.called
