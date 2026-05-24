"""Unit tests for OdaLegendWidget."""

from PySide6.QtWidgets import QLabel

from src.gui.panels.storico_oda.oda_legend import OdaLegendWidget


class TestOdaLegendWidget:
    """Test suite per OdaLegendWidget."""

    def test_initialization(self, qtbot):
        """Verifica lbl'inizializzazione della legenda."""
        widget = OdaLegendWidget()
        qtbot.addWidget(widget)

        # Verifica altezza (setFixedHeight impostato a 34)
        assert widget.height() == 34

        # Ci devono essere 3 item + il prefisso "Legenda:"
        labels = widget.findChildren(QLabel)
        assert len(labels) >= 4

        texts = [lbl.text() for lbl in labels]
        assert any("Legenda:" in t for t in texts)
        assert any("Cancellato" in t for t in texts)
        assert any("In attesa di rilascio" in t for t in texts)

    def test_item_rendering(self, qtbot):
        """Verifica la creazione dei singoli item."""
        widget = OdaLegendWidget()
        qtbot.addWidget(widget)

        # Test diretto di _make_item
        item = widget._make_item("#ff0000", "#000000", "Red Item")
        labels = item.findChildren(QLabel)
        assert any("Red Item" in lbl.text() for lbl in labels)

        # Verifica stile dello swatch
        swatch = next(lbl for lbl in labels if not lbl.text())
        assert "background-color: #ff0000" in swatch.styleSheet()
