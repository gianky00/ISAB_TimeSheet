import pytest

from src.gui.panels.scarico_ore_panel import ScaricoOrePanel


class TestScaricoOrePanelDeep:
    @pytest.fixture
    def panel(self, qapp, mocker):
        # Mock del caricamento dati iniziale per evitare accessi a file reali
        mocker.patch.object(ScaricoOrePanel, "_load_data")
        return ScaricoOrePanel()

    def test_update_selection_totals(self, panel, mocker):
        """Verifica il calcolo della somma ore per la selezione."""
        # Configura dati nel modello (Column 7 è Totale Ore)
        mock_data = [
            (
                "2024-01-01",
                "P1",
                "P2",
                "ODC1",
                "10",
                "08:00",
                "16:00",
                "8.0",
                "Desc",
                "S",
                "C1",
            ),
            (
                "2024-01-01",
                "P1",
                "P2",
                "ODC1",
                "10",
                "08:00",
                "12:00",
                "4.5",
                "Desc",
                "S",
                "C1",
            ),
        ]
        panel.source_model.set_data(mock_data)

        # Simula selezione colonna 7 per entrambe le righe
        selection_model = panel.table_view.selectionModel()
        idx1 = panel.source_model.index(0, 7)
        idx2 = panel.source_model.index(1, 7)

        # Usa il flag di selezione corretto per PyQt6
        from PyQt6.QtCore import QItemSelectionModel

        selection_model.select(idx1, QItemSelectionModel.SelectionFlag.Select)
        selection_model.select(idx2, QItemSelectionModel.SelectionFlag.Select)

        panel._update_selection_totals()

        assert "12.5" in panel.lbl_selection_total.text()

    def test_header_filter_changed_logic(self, panel, mocker):
        """Verifica che il cambio filtro dell'intestazione aggiorni il modello."""
        mock_set_filter = mocker.patch.object(panel.source_model, "set_filter")

        # Simula filtro su colonna 1 (Persona 1)
        panel._on_header_filter_changed(1, ["ROSSI", "VERDI"])

        assert 1 in panel._current_col_filters
        assert "rossi" in panel._current_col_filters[1]
        mock_set_filter.assert_called_once()

    def test_worker_progress_format(self, panel):
        """Verifica che il pannello accetti i messaggi di progresso dal worker."""
        msg = "⏳ Importazione: 50% completato (500/1000) • Tempo stimato: 1m 30s"
        panel._on_loading_progress(msg)
        assert panel.status_label.text() == msg

    def test_copy_selection_tsv_format(self, panel, mocker):
        """Verifica che la copia della selezione generi il formato TSV corretto."""
        mock_data = [
            (
                "D1",
                "P1",
                "P2",
                "ODC",
                "POS",
                "8:00",
                "17:00",
                "9.0",
                "DESC",
                "FIN",
                "COM",
            )
        ]
        panel.source_model.set_data(mock_data)

        # Seleziona riga
        panel.table_view.selectAll()

        # Mocking QApplication.clipboard().setText()
        mock_clipboard = mocker.MagicMock()
        mocker.patch("PyQt6.QtWidgets.QApplication.clipboard", return_value=mock_clipboard)

        panel._copy_selection()

        # Verifica chiamata
        mock_clipboard.setText.assert_called_once()
        call_args = mock_clipboard.setText.call_args[0][0]
        assert "P1" in call_args
        assert "9.0" in call_args

    def test_update_finished_ui_restore(self, panel, mocker):
        """Verifica il ripristino della UI dopo l'aggiornamento."""
        from pathlib import Path

        mocker.patch.object(Path, "exists", return_value=True)
        mocker.patch.object(Path, "unlink")

        panel._on_update_finished(True, "Successo", added=10, removed=2, duration=15.5)

        assert panel.update_btn.isEnabled()
        # Il nuovo formato usa font color invece di emoji
        status_text = panel.status_label.text()
        assert "color='green'" in status_text
        assert "+10" in status_text
        assert "-2" in status_text
        assert "15.5s" in status_text
