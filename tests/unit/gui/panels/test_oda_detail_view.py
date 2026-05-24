"""Unit tests for OdaDetailView."""

from src.gui.panels.storico_oda.oda_detail_view import OdaDetailView


class TestOdaDetailView:
    """Test suite per OdaDetailView."""

    def test_initialization(self, qtbot):
        """Verifica lbl'inizializzazione con gli headers forniti."""
        headers = ["Numero", "Fornitore", "Valore"]
        view = OdaDetailView(headers)
        qtbot.addWidget(view)

        assert len(view.detail_labels) == 3
        assert "Numero" in view.detail_labels
        assert view.detail_labels["Numero"].text() == "-"

    def test_update_details(self, qtbot):
        """Verifica lbl'aggiornamento e la formattazione dei dati."""
        headers = ["Data ODA", "Valore Totale", "Fornitore"]
        view = OdaDetailView(headers)
        qtbot.addWidget(view)

        data = ["2026-05-24", "1250.50", "COEMI"]
        view.update_details(data)

        # Formattazione data (format_date_it)
        assert "24/05/2026" in view.detail_labels["Data ODA"].text()

        # Formattazione valuta (format_currency_smart)
        assert "1.250" in view.detail_labels["Valore Totale"].text()

        assert view.detail_labels["Fornitore"].text() == "COEMI"

    def test_clear(self, qtbot):
        """Verifica la pulizia della vista."""
        headers = ["ID"]
        view = OdaDetailView(headers)
        qtbot.addWidget(view)

        view.update_details(["X"])
        view.clear()

        assert view.detail_labels["ID"].text() == "-"

    def test_none_nan_handling(self, qtbot):
        """Verifica la gestione di valori None o NaN."""
        headers = ["H1"]
        view = OdaDetailView(headers)
        qtbot.addWidget(view)

        view.update_details(["None"])
        assert view.detail_labels["H1"].text() == ""
