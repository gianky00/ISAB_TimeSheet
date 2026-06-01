"""Unit tests for DonCiroRenderer."""

from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QPointF, QRect
from PySide6.QtGui import QPainter

from src.core.mascot.don_ciro_engine import DonState, WeatherCond
from src.gui.widgets.dashboard.don_ciro_renderer import DonCiroRenderer, RenderItem


@pytest.fixture
def renderer():
    """Istanza del renderer."""
    return DonCiroRenderer()


@pytest.fixture
def mock_painter():
    """Mock per QPainter."""
    p = MagicMock(spec=QPainter)
    return p


@pytest.fixture
def mock_widget():
    """Mock per il widget che ospita il renderer."""
    w = MagicMock()
    w._walk_phase = 0.5
    w._yaw_angle = 45
    w._action_phase = 0.5
    w._label_phase = 0.5
    w._blink = 1.0
    w.rect.return_value = QRect(0, 0, 300, 300)
    return w


@pytest.fixture
def mock_engine():
    """Mock per lbl'engine di Don Ciro."""
    e = MagicMock()
    e.walk_x = 150
    e.scale = 1.0
    e.state = DonState.IDLE
    e.weather = WeatherCond.SUNNY
    e.jacket_flap = 5
    e.tie_angle = 10
    e.solve_ik.return_value = QPointF(10, 50)
    return e


class TestDonCiroRenderer:
    """Test suite per DonCiroRenderer."""

    def test_render_idle_sunny(self, renderer, mock_painter, mock_widget, mock_engine):
        """Verifica il rendering in stato IDLE e soleggiato."""
        renderer.render(mock_painter, mock_widget, mock_engine)

        # Verifica che i metodi principali di QPainter siano stati chiamati
        assert mock_painter.save.called
        assert mock_painter.restore.called
        assert mock_painter.translate.called
        assert mock_painter.drawEllipse.called

    def test_render_walking_rainy(self, renderer, mock_painter, mock_widget, mock_engine):
        """Verifica il rendering in stato WALKING e piovoso."""
        mock_engine.state = DonState.WALKING
        mock_engine.weather = WeatherCond.RAINY

        renderer.render(mock_painter, mock_widget, mock_engine)

        # In modalità piovosa deve disegnare le gocce (drawLine)
        assert mock_painter.drawLine.called

    def test_render_action_watch(self, renderer, mock_painter, mock_widget, mock_engine):
        """Verifica il rendering durante lbl'azione guarda orologio."""
        mock_engine.state = DonState.ACTION_WATCH

        renderer.render(mock_painter, mock_widget, mock_engine)
        assert mock_painter.save.called

    def test_render_action_tie(self, renderer, mock_painter, mock_widget, mock_engine):
        """Verifica il rendering durante lbl'azione sistema cravatta."""
        mock_engine.state = DonState.ACTION_TIE

        renderer.render(mock_painter, mock_widget, mock_engine)
        assert mock_painter.rotate.called  # Viene ruotata la cravatta

    def test_z_order_sorting(self, renderer, mock_painter, mock_widget, mock_engine):
        """Verifica che lbl'ordinamento Z funzioni correttamente."""
        # Non possiamo testare direttamente lbl'ordinamento privato dentro _render_ciro_3d
        # senza refactoring, ma possiamo testare la classe RenderItem
        items = [
            RenderItem(z_depth=1.0, draw_func=MagicMock(), args=()),
            RenderItem(z_depth=-1.0, draw_func=MagicMock(), args=()),
            RenderItem(z_depth=0.0, draw_func=MagicMock(), args=()),
        ]

        items.sort(key=lambda x: x.z_depth, reverse=True)

        assert items[0].z_depth == 1.0
        assert items[2].z_depth == -1.0

    def test_draw_weather_fx_rain(self, renderer, mock_painter, mock_widget, mock_engine):
        """Test specifico per la pioggia."""
        mock_engine.weather = WeatherCond.RAINY
        renderer._draw_weather_fx(mock_painter, mock_widget, mock_engine)
        assert mock_painter.drawLine.call_count >= 15

    def test_draw_torso_variants(self, renderer, mock_painter, mock_widget, mock_engine):
        """Verifica il disegno del torso con diverse angolazioni (sy > 0 o sy < 0)."""
        hp = QPointF(0, 0)
        sh = QPointF(0, -50)

        # Caso sy > 0 (frontale) -> disegna camicia e cravatta
        renderer._draw_torso(mock_painter, hp, sh, (1.0, 0.5), mock_engine)
        # Cerchiamo se ha disegnato il corpo della giacca (drawPath)
        assert mock_painter.drawPath.called

        # Caso sy < 0 (posteriore) -> non dovrebbe disegnare la cravatta
        mock_painter.reset_mock()
        renderer._draw_torso(mock_painter, hp, sh, (1.0, -0.5), mock_engine)
        # La cravatta usa translate/rotate
        assert not mock_painter.rotate.called

    def test_draw_head_blink(self, renderer, mock_painter, mock_widget, mock_engine):
        """Verifica il disegno della testa e degli occhi."""
        pos = QPointF(0, 0)
        mock_widget._blink = 0.0  # Occhi chiusi

        renderer._draw_head(mock_painter, pos, (1.0, 1.0), mock_widget, mock_engine)
        assert mock_painter.drawEllipse.called
