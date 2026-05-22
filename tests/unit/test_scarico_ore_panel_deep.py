from unittest.mock import MagicMock

import pytest

from src.core.contabilita.scarico_ore.controller import ScaricoOreController
from src.gui.panels.scarico_ore_panel import ScaricoOrePanel


class TestScaricoOrePanelDeep:
    @pytest.fixture
    def panel(self, qapp, monkeypatch):
        monkeypatch.setattr(ScaricoOrePanel, "_load_data", lambda self: None)
        mock_controller = MagicMock(spec=ScaricoOreController)
        mock_controller.format_number.side_effect = lambda x: f"{x:.1f}".replace(".", ",")
        p = ScaricoOrePanel(controller=mock_controller)
        return p

    def test_update_selection_totals(self, panel):
        """Verifica il calcolo della somma ore per la selezione."""
        # In V9.0 il metodo riceve direttamente il totale
        panel._update_selection_totals(12.5)

        text = panel.filters.lbl_selection.text()
        # Verifichiamo il valore formattato (12,5)
        assert "12,5" in text

    def test_header_filter_changed_logic(self, panel, mocker):
        """Verifica che il cambio filtro dell'intestazione aggiorni il modello."""
        mock_set_filter = mocker.patch.object(panel.source_model, "set_filter")
        panel._on_header_filter_changed(1, ["ROSSI"])
        assert 1 in panel._current_col_filters
        mock_set_filter.assert_called_once()

    def test_worker_progress_format(self, panel):
        """Verifica che il pannello accetti i messaggi di progresso."""
        msg = "[ATTESA] Test Progress"
        panel._on_loading_progress(msg)
        assert panel.filters.status_label.text() == msg

    def test_update_finished_ui_restore(self, panel, mocker):
        """Verifica il ripristino della UI dopo l'aggiornamento."""
        mocker.patch("src.gui.panels.scarico_ore_panel.ScaricoOreTableModel.CACHE_PATH")

        panel._on_update_finished(True, "OK")
        assert panel.filters.update_btn.isEnabled()
        assert "OK" in panel.filters.status_label.text()

    def test_set_search_query_flow(self, panel, mocker):
        """Verifica che set_search_query attivi il filtraggio."""
        mock_perform = mocker.patch.object(panel, "_perform_search")
        panel.set_search_query("123")
        assert panel.filters.search_input.text() == "123"
        mock_perform.assert_called_with("123")
