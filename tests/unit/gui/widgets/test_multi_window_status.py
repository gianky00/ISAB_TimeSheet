"""Unit tests for MultiWindowStatusWidget."""

import pytest
from PySide6.QtCore import Qt

from src.gui.widgets.dashboard.multi_window_status import DetachedModuleItem, MultiWindowStatusWidget


class TestMultiWindowStatusWidget:
    """Test suite per MultiWindowStatusWidget."""

    def test_initialization(self, qtbot):
        """Verifica lbl'inizializzazione del widget."""
        widget = MultiWindowStatusWidget()
        qtbot.addWidget(widget)

        assert widget.isHidden()
        assert widget.count_badge.text() == "0"

    def test_update_modules_shows_widget(self, qtbot):
        """Verifica che la card si mostri quando ci sono moduli sganciati."""
        widget = MultiWindowStatusWidget()
        qtbot.addWidget(widget)

        mock_win = pytest.importorskip("PySide6.QtWidgets").QWidget()
        mock_win.setWindowTitle("Test Panel - SyncroJob (Finestra Esterna)")

        detached = {1: {"window": mock_win}}

        widget.update_modules(detached)

        assert widget.isVisible()
        assert widget.count_badge.text() == "1"
        assert widget.items_container.count() == 1

    def test_update_modules_empty_hides_widget(self, qtbot):
        """Verifica che la card si nasconda se la lista è vuota."""
        widget = MultiWindowStatusWidget()
        qtbot.addWidget(widget)
        widget.show()

        widget.update_modules({})
        assert widget.isHidden()

    def test_reattach_single_signal(self, qtbot):
        """Verifica lbl'emissione del segnale di riaggancio singolo."""
        widget = MultiWindowStatusWidget()
        qtbot.addWidget(widget)

        mock_win = pytest.importorskip("PySide6.QtWidgets").QWidget()
        mock_win.setWindowTitle("Panel 1")

        widget.update_modules({5: {"window": mock_win}})

        # Trova lbl'item creato
        item = widget.findChild(DetachedModuleItem)
        assert item is not None

        with qtbot.waitSignal(widget.reattach_single_requested) as blocker:
            qtbot.mouseClick(item.btn, Qt.MouseButton.LeftButton)

        assert blocker.args[0] == 5

    def test_reattach_all_signal(self, qtbot):
        """Verifica lbl'emissione del segnale di riaggancio totale."""
        widget = MultiWindowStatusWidget()
        qtbot.addWidget(widget)

        with qtbot.waitSignal(widget.reattach_all_requested):
            qtbot.mouseClick(widget.reattach_all_btn, Qt.MouseButton.LeftButton)


class TestDetachedModuleItem:
    """Test suite per DetachedModuleItem."""

    def test_item_initialization(self, qtbot):
        item = DetachedModuleItem(index=10, title="Module X")
        qtbot.addWidget(item)

        # Cerchiamo la label del titolo
        from PySide6.QtWidgets import QLabel

        labels = item.findChildren(QLabel)
        assert any("Module X" in lbl.text() for lbl in labels)

    def test_btn_click_emits(self, qtbot):
        item = DetachedModuleItem(index=42, title="T")
        qtbot.addWidget(item)

        with qtbot.waitSignal(item.reattach_requested) as blocker:
            qtbot.mouseClick(item.btn, Qt.MouseButton.LeftButton)

        assert blocker.args[0] == 42
