"""Unit tests for PDLFilterWidget."""

from PySide6.QtCore import Qt

from src.gui.panels.pdl.pdl_filter_widget import PDLFilterWidget


class TestPDLFilterWidget:
    """Test suite per PDLFilterWidget."""

    def test_initialization(self, qtbot):
        """Verifica lbl'inizializzazione dei filtri."""
        widget = PDLFilterWidget()
        qtbot.addWidget(widget)

        assert widget.site_filter.count() == 4
        assert widget.area_filter.currentText() == "Tutte"
        assert widget.search_input.placeholderText() == "N°, Area, Richiedente..."

    def test_signals_emission(self, qtbot):
        """Verifica lbl'emissione dei segnali principali."""
        widget = PDLFilterWidget()
        qtbot.addWidget(widget)

        # Test update signal
        with qtbot.waitSignal(widget.update_clicked):
            qtbot.mouseClick(widget.btn_bot_update, Qt.MouseButton.LeftButton)

        # Test reset signal
        with qtbot.waitSignal(widget.reset_clicked):
            qtbot.mouseClick(widget.clear_btn, Qt.MouseButton.LeftButton)

        # Test site changed
        with qtbot.waitSignal(widget.site_changed) as blocker:
            widget.site_filter.setCurrentText("ISAB Sud")
        assert blocker.args[0] == "ISAB Sud"

    def test_get_filters(self, qtbot):
        """Verifica il recupero dei valori dei filtri."""
        widget = PDLFilterWidget()
        qtbot.addWidget(widget)

        widget.search_input.setText("123/C")
        widget.site_filter.setCurrentText("IGCC")

        filters = widget.get_filters()
        assert filters["search"] == "123/c"
        assert filters["site"] == "IGCC"
        assert filters["area"] == "Tutte"

    def test_area_changed_signal(self, qtbot):
        """Verifica lbl'emissione del segnale area_changed."""
        widget = PDLFilterWidget()
        qtbot.addWidget(widget)

        with qtbot.waitSignal(widget.area_changed) as blocker:
            widget.area_filter.setCurrentText("Tutte")  # Già impostato, forziamo cambiamento
            widget.area_filter.addItems(["New Area"])
            widget.area_filter.setCurrentText("New Area")

        assert blocker.args[0] == "New Area"
