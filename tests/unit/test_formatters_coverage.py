import pytest
from PyQt6.QtCore import Qt
from src.gui.formatters import FastTableModel

class TestFastTableModel:
    """Test suite for FastTableModel in src/gui/formatters.py"""

    def test_init_defaults(self):
        model = FastTableModel()
        assert model.rowCount() == 0
        assert model.columnCount() == 0

    def test_init_with_data(self):
        data = [["A1", "B1"], ["A2", "B2"]]
        headers = ["Col1", "Col2"]
        model = FastTableModel(data, headers)
        assert model.rowCount() == 2
        assert model.columnCount() == 2
        
    def test_data_display_role(self):
        data = [[10, 20]]
        model = FastTableModel(data, ["H1", "H2"])
        index = model.index(0, 0)
        
        # Should return string representation
        assert model.data(index, Qt.ItemDataRole.DisplayRole) == "10"
        
        # Test None value
        model.update_data([[None]])
        index_none = model.index(0, 0)
        assert model.data(index_none, Qt.ItemDataRole.DisplayRole) == ""

    def test_data_alignment_role(self):
        model = FastTableModel([["val"]], ["Col1"])
        index = model.index(0, 0)
        align = model.data(index, Qt.ItemDataRole.TextAlignmentRole)
        expected = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        assert align == expected

    def test_data_invalid_index(self):
        model = FastTableModel()
        assert model.data(model.index(0, 0), Qt.ItemDataRole.DisplayRole) is None

    def test_header_data(self):
        headers = ["H1", "H2"]
        model = FastTableModel([], headers)
        
        assert model.headerData(0, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) == "H1"
        assert model.headerData(1, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole) == "H2"
        
        # Wrong orientation
        assert model.headerData(0, Qt.Orientation.Vertical, Qt.ItemDataRole.DisplayRole) is None
        # Wrong role
        assert model.headerData(0, Qt.Orientation.Horizontal, Qt.ItemDataRole.UserRole) is None

    def test_update_data(self, qtbot):
        """Test atomic update with signal emission."""
        model = FastTableModel([["Old"]], ["Col1"])
        
        # Check that signals are emitted
        with qtbot.waitSignals([model.modelAboutToBeReset, model.modelReset]):
            model.update_data([["New"], ["Row2"]])
            
        assert model.rowCount() == 2
        # Ensure column count persists or logic handles it (headers didn't change)
        assert model.data(model.index(0, 0), Qt.ItemDataRole.DisplayRole) == "New"
