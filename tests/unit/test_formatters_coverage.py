import pytest
from PyQt6.QtCore import Qt

from src.gui.formatters import FastTableModel


class TestFastTableModel:
    """Test coverage for src/gui/formatters.py"""

    @pytest.fixture
    def sample_data(self):
        return [["Row1Col1", "Row1Col2"], ["Row2Col1", "Row2Col2"]]

    @pytest.fixture
    def headers(self):
        return ["Header1", "Header2"]

    def test_init(self, sample_data, headers):
        model = FastTableModel(sample_data, headers)
        assert model.rowCount() == 2
        assert model.columnCount() == 2

    def test_init_empty(self):
        model = FastTableModel()
        assert model.rowCount() == 0
        assert model.columnCount() == 0

    def test_data_display(self, sample_data, headers):
        model = FastTableModel(sample_data, headers)

        # Create index mock or use model.index if QApplication is active (but we want to avoid Qt dependence if possible)
        # FastTableModel inherits QAbstractTableModel. We can call data() directly with a mock index?
        # QModelIndex cannot be easily mocked in pure python without PyQt setup.
        # But we can try to use model.createIndex which is protected, or simply use model.index(r, c)
        # Note: model.index requires a QAbstractItemModel parent, which FastTableModel is.
        # But creating indices usually requires a QGuiApplication instance for some meta-object stuff?
        # Let's try mocking the index object since FastTableModel.data just calls index.row() and index.column().

        class MockIndex:
            def __init__(self, r, c, valid=True):
                self._r = r
                self._c = c
                self._valid = valid

            def row(self):
                return self._r

            def column(self):
                return self._c

            def isValid(self):
                return self._valid

        idx = MockIndex(0, 1)
        assert model.data(idx, Qt.ItemDataRole.DisplayRole) == "Row1Col2"

        idx_invalid = MockIndex(0, 0, False)
        assert model.data(idx_invalid, Qt.ItemDataRole.DisplayRole) is None

        # Test invalid role
        assert model.data(idx, Qt.ItemDataRole.ToolTipRole) is None

    def test_data_alignment(self, sample_data):
        model = FastTableModel(sample_data)

        class MockIndex:
            def __init__(self, r, c):
                self._r = r
                self._c = c

            def row(self):
                return self._r

            def column(self):
                return self._c

            def isValid(self):
                return True

        idx = MockIndex(0, 0)
        align = model.data(idx, Qt.ItemDataRole.TextAlignmentRole)
        assert align == Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

    def test_header_data(self, headers):
        model = FastTableModel([], headers)
        assert model.headerData(0, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) == "Header1"
        assert model.headerData(1, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) == "Header2"

        # Wrong orientation/role
        assert model.headerData(0, Qt.Orientation.Vertical, Qt.ItemDataRole.DisplayRole) is None
        assert model.headerData(0, Qt.Orientation.Horizontal, Qt.ItemDataRole.UserRole) is None

    def test_update_data(self, sample_data):
        model = FastTableModel(sample_data)
        new_data = [["New1", "New2"]]

        # We can't easily check if signals (beginResetModel) are emitted without QTest,
        # but we can check the state change.
        model.update_data(new_data)
        assert model.rowCount() == 1
        assert model._data == new_data
