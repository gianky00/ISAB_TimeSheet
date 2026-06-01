"""Unit tests for OdaFilterWidget."""

from PySide6.QtCore import Qt

from src.gui.panels.storico_oda.oda_filter_widget import OdaFilterWidget


class TestOdaFilterWidget:
    """Test suite per OdaFilterWidget."""

    def test_initialization(self, qtbot):
        """Verifica lbl'inizializzazione del widget."""
        widget = OdaFilterWidget()
        qtbot.addWidget(widget)

        assert widget.search_input.placeholderText() == "OdA, Fornitore, Descrizione..."
        assert "Ultimo Sync" in widget.lbl_sync_status.text()

    def test_search_signal(self, qtbot):
        """Verifica lbl'emissione del segnale di ricerca."""
        widget = OdaFilterWidget()
        qtbot.addWidget(widget)

        with qtbot.waitSignal(widget.search_changed) as blocker:
            widget.search_input.setText("ODA-TEST")
        assert blocker.args[0] == "ODA-TEST"

    def test_button_signals(self, qtbot):
        """Verifica i segnali dei bottoni."""
        widget = OdaFilterWidget()
        qtbot.addWidget(widget)

        # Import
        with qtbot.waitSignal(widget.import_clicked):
            qtbot.mouseClick(widget.btn_import, Qt.MouseButton.LeftButton)

        # Update
        with qtbot.waitSignal(widget.update_clicked):
            qtbot.mouseClick(widget.btn_bot_update, Qt.MouseButton.LeftButton)

        # Export
        with qtbot.waitSignal(widget.export_clicked):
            qtbot.mouseClick(widget.export_btn, Qt.MouseButton.LeftButton)

    def test_set_sync_status(self, qtbot):
        """Verifica lbl'aggiornamento della label di sync."""
        widget = OdaFilterWidget()
        qtbot.addWidget(widget)

        widget.set_sync_status("Sync: 24/05/2026")
        assert widget.lbl_sync_status.text() == "Sync: 24/05/2026"
