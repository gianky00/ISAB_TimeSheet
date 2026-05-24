"""Unit tests for AttivitaProgrammateTab."""

import json

import pytest
from PySide6.QtCore import Qt

from src.gui.widgets.contabilita.attivita_tab import AttivitaProgrammateTab


@pytest.fixture
def mock_data():
    """Dati di test simulati dal database."""
    # Mapping in AttivitaImporter (lowercase):
    # ps, area, pdl, imp, descrizione, lun, mar, mer, gio, ven, stato_pdl, stato_attivita, data_controllo, personale, po, avviso
    # + 1 colonna per stili JSON
    row1 = (
        "X",
        "Area 1",
        "PDL01",
        "10",
        "Desc 1",
        "1",
        "0",
        "0",
        "0",
        "0",
        "Aperto",
        "In corso",
        "2026-05-24 10:00:00",
        "Pippo",
        "Y",
        "AVV01",
        json.dumps({"pdl": {"fg": "#ff0000"}}),
    )
    row2 = (
        "",
        "Area 2",
        "PDL02",
        "5",
        "Desc 2",
        "0",
        "1",
        "0",
        "0",
        "0",
        "Chiuso",
        "Completato",
        "2026-05-23 09:00:00",
        "Pluto",
        "",
        "AVV02",
        None,
    )
    return [row1, row2]


class TestAttivitaProgrammateTab:
    """Test suite per AttivitaProgrammateTab."""

    def test_initialization(self, qtbot, mocker):
        """Verifica lbl'inizializzazione del tab."""
        mocker.patch("src.gui.workers.contabilita_data_worker.ContabilitaDataWorker.start")

        widget = AttivitaProgrammateTab()
        qtbot.addWidget(widget)

        assert widget.table.columnCount() == len(widget.COLUMNS)
        assert widget.combo_area.currentText() == "Tutte"

    def test_on_data_ready_populates_table(self, qtbot, mock_data, mocker):
        """Verifica che la tabella venga popolata correttamente dai dati del worker."""
        mocker.patch("src.gui.workers.contabilita_data_worker.ContabilitaDataWorker.start")
        widget = AttivitaProgrammateTab()
        qtbot.addWidget(widget)

        widget._on_data_ready(mock_data)

        assert widget.table.rowCount() == 2
        assert widget.table.item(0, 2).text() == "PDL01"
        assert widget.table.item(1, 2).text() == "PDL02"

        # Verifica formattazione data (Colonna 12)
        assert widget.table.item(0, 12).text() == "24/05/2026"

        # Verifica stili (Colonna PdL è indice 2)
        assert widget.table.item(0, 2).foreground().color().name() == "#ff0000"

    def test_filter_area(self, qtbot, mock_data, mocker):
        """Verifica il filtro per Area."""
        mocker.patch("src.gui.workers.contabilita_data_worker.ContabilitaDataWorker.start")
        widget = AttivitaProgrammateTab()
        qtbot.addWidget(widget)
        widget._on_data_ready(mock_data)

        widget.combo_area.setCurrentText("Area 1")

        assert not widget.table.isRowHidden(0)
        assert widget.table.isRowHidden(1)

    def test_filter_ps_po(self, qtbot, mock_data, mocker):
        """Verifica i filtri checkbox PS e PO."""
        mocker.patch("src.gui.workers.contabilita_data_worker.ContabilitaDataWorker.start")
        widget = AttivitaProgrammateTab()
        qtbot.addWidget(widget)
        widget._on_data_ready(mock_data)

        widget.chk_ps.setChecked(True)
        assert not widget.table.isRowHidden(0)
        assert widget.table.isRowHidden(1)

        widget.chk_ps.setChecked(False)
        widget.chk_po.setChecked(True)
        assert not widget.table.isRowHidden(0)
        assert widget.table.isRowHidden(1)

    def test_reset_filters(self, qtbot, mock_data, mocker):
        """Verifica il reset dei filtri."""
        mocker.patch("src.gui.workers.contabilita_data_worker.ContabilitaDataWorker.start")
        widget = AttivitaProgrammateTab()
        qtbot.addWidget(widget)
        widget._on_data_ready(mock_data)

        widget.chk_ps.setChecked(True)
        widget.combo_area.setCurrentText("Area 1")

        qtbot.mouseClick(widget.btn_reset, Qt.MouseButton.LeftButton)

        assert not widget.chk_ps.isChecked()
        assert widget.combo_area.currentIndex() == 0
        assert not widget.table.isRowHidden(0)
        assert not widget.table.isRowHidden(1)

    def test_global_search(self, qtbot, mock_data, mocker):
        """Verifica la ricerca testuale globale."""
        mocker.patch("src.gui.workers.contabilita_data_worker.ContabilitaDataWorker.start")
        widget = AttivitaProgrammateTab()
        qtbot.addWidget(widget)
        widget._on_data_ready(mock_data)

        widget.filter_data("Pippo")
        assert not widget.table.isRowHidden(0)
        assert widget.table.isRowHidden(1)

        widget.filter_data("Desc")
        assert not widget.table.isRowHidden(0)
        assert not widget.table.isRowHidden(1)

    def test_worker_error_handling(self, qtbot, mocker):
        """Verifica che lbl'errore del worker non rompa la UI."""
        mocker.patch("src.gui.workers.contabilita_data_worker.ContabilitaDataWorker.start")
        widget = AttivitaProgrammateTab()
        qtbot.addWidget(widget)

        # Simuliamo errore
        if widget.worker:
            widget.worker.error_signal.emit("Database Lock")

        # In caso di errore, il placeholder dovrebbe indicare il caricamento fallito o terminato
        # Poiché placeholderText() non esiste, verifichiamo lbl'attributo suggerito o che non crashi
        assert hasattr(widget.table, "_placeholder_text")
        assert "Caricamento" in widget.table._placeholder_text
