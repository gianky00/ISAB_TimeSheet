from unittest.mock import patch

import pytest
from PySide6.QtCore import QRect
from PySide6.QtGui import QPaintEvent

from src.gui.widgets.simple_chart import DonutChart, StatCard


def test_donut_chart_initialization(qtbot):
    chart = DonutChart(title="Test Chart")
    qtbot.addWidget(chart)

    assert chart.title == "Test Chart"
    assert chart.values == [0, 0]
    assert chart.minimumWidth() >= 200
    assert chart.minimumHeight() >= 200


def test_donut_chart_set_data(qtbot):
    chart = DonutChart()
    qtbot.addWidget(chart)

    with patch.object(chart, "update") as mock_update:
        chart.set_data(10, 5)

        assert chart.values == [10, 5]
        assert mock_update.called


def test_donut_chart_paint_empty(qtbot):
    chart = DonutChart()
    qtbot.addWidget(chart)

    # Valori a 0 (default)
    event = QPaintEvent(QRect(0, 0, 200, 200))

    # Evoca paintEvent; non crasherà e disegnerà "N/A"
    try:
        chart.paintEvent(event)
    except Exception as e:
        pytest.fail(f"paintEvent empty crashed: {e}")


def test_donut_chart_paint_with_data(qtbot):
    chart = DonutChart()
    qtbot.addWidget(chart)

    chart.set_data(75, 25)

    event = QPaintEvent(QRect(0, 0, 200, 200))

    try:
        chart.paintEvent(event)
    except Exception as e:
        pytest.fail(f"paintEvent with data crashed: {e}")


def test_donut_chart_paint_partial_data(qtbot):
    chart = DonutChart()
    qtbot.addWidget(chart)

    # Errori a 0 (testa il continue nel loop di disegno)
    chart.set_data(100, 0)

    event = QPaintEvent(QRect(0, 0, 200, 200))

    try:
        chart.paintEvent(event)
    except Exception as e:
        pytest.fail(f"paintEvent with partial data crashed: {e}")


def test_stat_card_initialization(qtbot):
    card = StatCard(title="Test Stat")
    qtbot.addWidget(card)

    assert card.layout() is not None
    assert card.chart is not None
    assert isinstance(card.chart, DonutChart)
