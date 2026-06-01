"""Unit tests for PDLDelegate."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStyleOptionViewItem, QTableWidget

from src.gui.panels.pdl.pdl_delegate import PDLDelegate


class TestPDLDelegate:
    """Test suite per PDLDelegate."""

    def test_init_style_option_wrap(self, qtbot):
        """Verifica lbl'abilitazione del wrap per colonne non-date."""
        delegate = PDLDelegate(date_columns=[0])  # Colonna 0 è data

        # Setup mock environment
        table = QTableWidget(1, 2)
        idx_wrapped = table.model().index(0, 1)  # Colonna 1: deve avere wrap

        option = QStyleOptionViewItem()
        delegate.initStyleOption(option, idx_wrapped)

        assert option.textElideMode == Qt.TextElideMode.ElideNone

    def test_init_style_option_date_no_wrap(self, qtbot):
        """Verifica che le colonne data usino lbl'elide."""
        delegate = PDLDelegate(date_columns=[0])

        table = QTableWidget(1, 1)
        idx_date = table.model().index(0, 0)

        option = QStyleOptionViewItem()
        delegate.initStyleOption(option, idx_date)

        assert option.textElideMode == Qt.TextElideMode.ElideRight
