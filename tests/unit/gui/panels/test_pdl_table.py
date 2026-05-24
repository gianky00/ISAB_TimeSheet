"""Unit tests for PDLTableView."""

import pytest
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QHeaderView

from src.gui.panels.pdl.widgets.pdl_table import PDLTableView


@pytest.fixture
def mock_model():
    model = QStandardItemModel(2, 2)
    model.setItem(0, 0, QStandardItem("Row 1"))
    model.setItem(1, 0, QStandardItem("Row 2"))
    return model


class TestPDLTableView:
    """Test suite per PDLTableView."""

    def test_initialization(self, qtbot, mock_model):
        """Verifica lbl'inizializzazione del widget."""
        view = PDLTableView(mock_model)
        qtbot.addWidget(view)

        assert view.model() == mock_model
        assert view.alternatingRowColors() is True
        assert view.selectionBehavior() == PDLTableView.SelectionBehavior.SelectRows

    def test_signals_emission(self, qtbot, mock_model):
        """Verifica lbl'emissione dei segnali personalizzati."""
        view = PDLTableView(mock_model)
        qtbot.addWidget(view)

        # Test double click signal
        with qtbot.waitSignal(view.row_double_clicked):
            idx = mock_model.index(0, 0)
            view.doubleClicked.emit(idx)

        # Test header clicked
        with qtbot.waitSignal(view.header_clicked) as blocker:
            view.horizontalHeader().sectionClicked.emit(1)
        assert blocker.args[0] == 1

    def test_selection_changed_signal(self, qtbot, mock_model):
        """Verifica lbl'emissione del segnale di cambio selezione."""
        view = PDLTableView(mock_model)
        qtbot.addWidget(view)

        with qtbot.waitSignal(view.selection_changed_custom):
            view.selectRow(1)

    def test_optimize_columns(self, qtbot, mock_model):
        """Verifica lbl'ottimizzazione delle colonne (smoke test)."""
        view = PDLTableView(mock_model)
        qtbot.addWidget(view)

        # Chiamata asincrona via QTimer.singleShot(0)
        view.optimize_columns(2)

        # Attendiamo un ciclo di eventi
        qtbot.wait(100)

        # Verifica che il resize mode sia stato impostato (Interactive è il default per resizeColumnsToContents in questo contesto)
        assert view.horizontalHeader().sectionResizeMode(0) == QHeaderView.ResizeMode.Interactive
