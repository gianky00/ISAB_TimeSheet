"""Unit tests for StatisticsWidget."""

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLabel

from src.gui.widgets.statistics_widget import StatisticsWidget


@pytest.fixture
def mock_stats_manager(mocker):
    """Fixture per mockare StatsManager."""
    mock_mgr = mocker.patch("src.gui.widgets.statistics_widget.StatsManager")
    instance = mocker.MagicMock()
    mock_mgr.return_value = instance
    return instance


class TestStatisticsWidget:
    """Test suite per StatisticsWidget."""

    def test_initialization(self, qtbot, mock_stats_manager):
        """Verifica lbl'inizializzazione del widget."""
        mock_stats_manager.get_all_stats.return_value = {}

        widget = StatisticsWidget()
        qtbot.addWidget(widget)

        assert widget.table.columnCount() == 4
        assert widget.cards_layout.count() == 2  # Esecuzioni Totali e Errori Totali

    def test_refresh_populates_data(self, qtbot, mock_stats_manager):
        """Verifica che il refresh popoli card e tabella."""
        mock_stats_manager.get_all_stats.return_value = {
            "timbrature": {"runs": 10, "errors": 2, "last_run": "2026-05-24T10:00:00"},
            "scarico_ts": {"runs": 5, "errors": 0, "last_run": ""},
        }

        widget = StatisticsWidget()
        qtbot.addWidget(widget)
        widget.refresh()

        # Verifica card (10+5=15 runs, 2+0=2 errors)
        def get_card_value(layout_item):
            card = layout_item.widget()
            labels = card.findChildren(QLabel)
            # Cerchiamo la label che contiene solo numeri
            for lbl in labels:
                txt = lbl.text().strip()
                if txt.isdigit():
                    return txt
            return None

        assert get_card_value(widget.cards_layout.itemAt(0)) == "15"
        assert get_card_value(widget.cards_layout.itemAt(1)) == "2"

        # Verifica tabella
        assert widget.table.rowCount() == 2
        # Troviamo la riga per Timbrature (lbl'ordine potrebbe variare per sorted keys)
        row_idx = -1
        for r in range(widget.table.rowCount()):
            if widget.table.item(r, 0).text() == "Timbrature":
                row_idx = r
                break

        assert row_idx != -1
        assert widget.table.item(row_idx, 1).text() == "10"
        assert widget.table.item(row_idx, 2).text() == "2"
        assert "24/05/2026" in widget.table.item(row_idx, 3).text()

        # Verifica fallback data vuota
        other_row = 1 - row_idx
        assert widget.table.item(other_row, 3).text() == "Mai"

    def test_error_formatting_in_table(self, qtbot, mock_stats_manager):
        """Verifica che gli errori siano evidenziati in rosso."""
        mock_stats_manager.get_all_stats.return_value = {
            "buggy_bot": {"runs": 1, "errors": 1, "last_run": ""}
        }

        widget = StatisticsWidget()
        qtbot.addWidget(widget)
        widget.refresh()

        err_item = widget.table.item(0, 2)
        assert err_item.foreground().color() == QColor(Qt.GlobalColor.red)
