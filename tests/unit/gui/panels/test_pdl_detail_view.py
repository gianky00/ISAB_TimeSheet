"""Unit tests for PDLDetailView."""

from src.gui.panels.pdl.pdl_detail_view import PDLDetailView


class TestPDLDetailView:
    """Test suite per PDLDetailView."""

    def test_initialization(self, qtbot):
        """Verifica lbl'inizializzazione con gli headers forniti."""
        headers = ["ID", "Area", "Stato"]
        view = PDLDetailView(headers)
        qtbot.addWidget(view)

        assert len(view.detail_labels) == 3
        assert "ID" in view.detail_labels
        assert view.detail_labels["ID"].text() == "-"
        assert view.cron_table.columnCount() == 5

    def test_update_details(self, qtbot):
        """Verifica lbl'aggiornamento dei dati e della cronologia."""
        headers = ["ID", "Area", "Importato il"]
        view = PDLDetailView(headers)
        qtbot.addWidget(view)

        data = ["PDL-123", "Area Nord", "2026-05-24 10:00:00"]
        interventions = [
            {
                "data": "24/05/2026",
                "fonte": "Validato",
                "tecnico": "Mario",
                "ore_lavoro": 4.5,
                "descrizione": "Lavoro",
            }
        ]

        view.update_details(data, interventions)

        assert view.detail_labels["ID"].text() == "PDL-123"
        assert view.detail_labels["Area"].text() == "Area Nord"
        # Verifica formattazione data
        assert view.detail_labels["Importato il"].text() == "24/05/2026 10:00:00"

        assert view.cron_table.rowCount() == 1
        assert view.cron_table.item(0, 2).text() == "Mario"
        assert view.cron_table.item(0, 1).text() == "Validato"

    def test_clear(self, qtbot):
        """Verifica la pulizia della vista."""
        headers = ["ID"]
        view = PDLDetailView(headers)
        qtbot.addWidget(view)

        view.update_details(["X"], [{"data": "1"}])
        view.clear()

        assert view.detail_labels["ID"].text() == "-"
        assert view.cron_table.rowCount() == 0

    def test_none_nan_handling(self, qtbot):
        """Verifica la gestione di valori None o NaN."""
        headers = ["H1", "H2"]
        view = PDLDetailView(headers)
        qtbot.addWidget(view)

        view.update_details(["None", "NaN"])
        assert view.detail_labels["H1"].text() == ""
        assert view.detail_labels["H2"].text() == ""
