from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtWidgets import QWidget

from src.gui.widgets.contabilita.giornaliere_tab import GiornaliereYearTab


class MockTable(QWidget):
    """Real QWidget for ExcelTableWidget."""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setColumnCount = MagicMock()
        self.setHorizontalHeaderLabels = MagicMock()
        self.setWordWrap = MagicMock()
        self.setTextElideMode = MagicMock()
        self.setSelectionBehavior = MagicMock()
        self.setSelectionMode = MagicMock()
        self.setFocusPolicy = MagicMock()
        self.horizontalHeader = MagicMock(return_value=MagicMock())
        self.verticalHeader = MagicMock(return_value=MagicMock())
        self.setColumnWidth = MagicMock()
        self.setContextMenuPolicy = MagicMock()
        self.setEditTriggers = MagicMock()
        self.setSortingEnabled = MagicMock()
        self.clearContents = MagicMock()
        self.setRowCount = MagicMock()
        self.rowCount = MagicMock(return_value=0)
        self.columnCount = MagicMock(return_value=10)
        self.setPlaceholderText = MagicMock()
        self.blockSignals = MagicMock()
        self.setItem = MagicMock()
        self.item = MagicMock()
        self.insertRow = MagicMock()
        self.isRowHidden = MagicMock(return_value=False)
        self.setRowHidden = MagicMock()
        self.smart_resize = MagicMock()
        self.visualItemRect = MagicMock()
        self.viewport = MagicMock()
        self.auto_copy_headers = True

    def itemAt(self, pos):  # noqa: N802
        return None


@pytest.fixture
def tab(qtbot, mocker):
    """Istanza di GiornaliereYearTab con dipendenze mockate."""
    mocker.patch("src.gui.widgets.contabilita.giornaliere_tab.ExcelTableWidget", return_value=MockTable())
    mocker.patch("src.gui.workers.contabilita_data_worker.ContabilitaDataWorker.start")
    mocker.patch("src.application.services.config_manager.load_config", return_value={})

    t = GiornaliereYearTab(year=2024)
    qtbot.addWidget(t)
    return t


class TestGiornaliereYearTab:
    """Test suite per GiornaliereYearTab."""

    def test_initialization(self, tab):
        """Verifica l'inizializzazione corretta."""
        assert tab.year == 2024
        assert tab.table.setColumnCount.called

    def test_on_data_ready(self, tab, mocker):
        """Verifica il popolamento della tabella."""
        mock_data = [("24/05/2026", "Rossi", "TCL1", "Desc", "1", "O1", "P1", "08", "17", "8", "file.pdf")]

        # Simuliamo che rowCount() cresca quando inseriamo dati (se necessario)
        tab.table.rowCount.return_value = 1

        tab._on_data_ready(mock_data)

        assert tab.table.setRowCount.called
        assert tab.table.setItem.called
        assert tab.table.smart_resize.called

    def test_update_totals_logic(self, tab, mocker):
        """Verifica la logica di somma dei totali."""
        # Configuriamo il mock della tabella
        tab.table.rowCount.return_value = 3  # 2 dati + 1 totali

        mock_total_item = MagicMock()
        mock_total_item.text.return_value = "TOTALI"
        tab.table.item.side_effect = (
            lambda r, c: mock_total_item if r == 2 and c == 0 else MagicMock(text=lambda: "8,0")
        )

        tab.table.isRowHidden.return_value = False

        # Mock del metodo format
        tab._format_number = MagicMock(return_value="16,0")

        # Reset side_effect per catturare l'item dei totali in colonna 9
        target_total_item = MagicMock()

        def get_item(r, c):
            if r == 2 and c == 0:
                return mock_total_item
            if r == 2 and c == 9:
                return target_total_item
            m = MagicMock()
            m.text.return_value = "8,0"
            return m

        tab.table.item.side_effect = get_item

        tab._update_totals()

        assert target_total_item.setText.called

    def test_filter_data_delegation(self, tab):
        """Verifica che il filtro scorra le righe."""
        tab.table.rowCount.return_value = 3
        mock_total_item = MagicMock()
        mock_total_item.text.return_value = "TOTALI"

        def get_item(r, c):
            if r == 2 and c == 0:
                return mock_total_item
            m = MagicMock()
            m.text.return_value = "Content"
            return m

        tab.table.item.side_effect = get_item

        tab.filter_data("search")
        assert tab.table.setRowHidden.called

    def test_open_giornaliera_flow(self, tab, mocker):
        """Verifica il flusso di apertura file."""
        mocker.patch("src.application.services.config_manager.load_config", return_value={"giornaliere_path": "C:/fake"})
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("pathlib.Path.exists", return_value=True)
        mock_start = mocker.patch("os.startfile")

        # Test successo (trovato in cartella anno)
        with patch("os.path.join", return_value="C:/fake/file.pdf"):
            tab._open_giornaliera("file.pdf")
            assert mock_start.called
