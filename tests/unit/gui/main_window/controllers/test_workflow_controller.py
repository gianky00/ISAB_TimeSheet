from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QDate, QObject

from src.gui.main_window.controllers.workflow_controller import WorkflowController


@pytest.fixture
def mock_mainwindow():
    # Usiamo QObject reale come parent per soddisfare il costruttore di QObject
    mw = MagicMock(spec=["navigation_controller", "status_bar_component"])
    # Non mockiamo 'parent', è un metodo di QObject, non dobbiamo sovrascriverlo
    return mw


def test_workflow_controller_init(mock_mainwindow):
    # La classe WorkflowController eredita da QObject.
    # Il mock_mainwindow deve comportarsi come un QObject valido o essere passato come parent corretto.
    # Proviamo a passare un QObject reale come parent.
    parent_obj = QObject()
    controller = WorkflowController(parent_obj)
    controller.mw = mock_mainwindow
    assert controller.mw == mock_mainwindow


def test_run_timbrature_bot_ieri(mock_mainwindow):
    controller = WorkflowController(QObject())
    controller.mw = mock_mainwindow

    mock_panel = MagicMock()
    mock_mainwindow.timbrature_bot_panel = mock_panel

    controller.run_timbrature_bot("ieri")

    expected_date = QDate.currentDate().addDays(-1).toString("dd.MM.yyyy")
    mock_panel.run_externally.assert_called_with({"data_da": expected_date, "data_a": expected_date})
