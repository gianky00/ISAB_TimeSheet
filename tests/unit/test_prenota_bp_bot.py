"""
Unit tests for PrenotaBPBot.
"""

from unittest.mock import MagicMock, patch

import pytest

from src.bots.portale_fornitori.prenota_bp.bot import PrenotaBPBot


class TestPrenotaBPBot:
    @pytest.fixture
    def bot(self):
        return PrenotaBPBot("user", "pass")

    def test_initialization(self, bot):
        assert bot.name == "Prenota BP"
        assert len(bot.get_columns()) > 0
        assert bot.data_da == "01.01.2024"

    def test_get_row_value_robustness(self, bot):
        """Verifica estrazione valori con chiavi sporche."""
        row = {"  Numero_BP ": "12345", "NoTe  ": "Note1"}

        val_bp = bot._get_row_value(row, "Numero BP")
        assert val_bp == "12345"

        val_note = bot._get_row_value(row, "Note")
        assert val_note == "Note1"

        assert bot._get_row_value(row, "Inesistente") == ""

    def test_init_run_data_dict(self, bot):
        """Verifica estrazione parametri da dizionario."""
        data = {"rows": [{"a": 1}], "data_da": "01.01.2020", "fornitore": "NuovoFornitore"}
        rows = bot._init_run_data(data)
        assert len(rows) == 1
        assert bot.data_da == "01.01.2020"
        assert bot.fornitore == "NuovoFornitore"

    def test_init_run_data_list(self, bot):
        """Verifica estrazione parametri da lista semplice."""
        data = [{"a": 1}, {"b": 2}]
        rows = bot._init_run_data(data)
        assert len(rows) == 2
        # Parametri restano default
        assert bot.data_da == "01.01.2024"

    @patch("src.bots.portale_fornitori.prenota_bp.bot.PrenotaBPPage")
    def test_run_full_flow(self, mock_page_cls, bot):
        """Verifica il ciclo di esecuzione completo."""
        mock_page = mock_page_cls.return_value
        bot.driver = MagicMock()

        data = [{"Numero BP": "BP1"}, {"Numero BP": ""}, {"Numero BP": "BP2"}]

        # Mock process single
        # 1. Success
        # 2. Skip (handled inside process_single but here we verify flow)
        # 3. Exception

        # Per testare run dobbiamo mockare _process_single_bp o lasciare che esegua
        # Se lasciamo eseguire, dobbiamo mockare i metodi della page

        # Setup page mocks for success path
        mock_page.filtra_buoni_prelievo.side_effect = [None, Exception("Filter fail")]

        bot.run(data)

        # Verifica chiamate
        mock_page.navigate_to_gestione_bp.assert_called_once()
        # Row 1: Valid -> Filter called
        # Row 2: Empty -> Skipped (Filter NOT called)
        # Row 3: Valid -> Filter called (and raises)

        assert mock_page.filtra_buoni_prelievo.call_count == 2
        # Riga 2 viene saltata PRIMA del try-except in _process_single_bp, quindi non aggiunge nulla a results
        assert len(bot.results) == 2
        assert bot.results[0]["STATO"] == "OK"
        assert bot.results[1]["STATO"] == "ERRORE"

    @patch("src.bots.portale_fornitori.prenota_bp.bot.PrenotaBPPage")
    def test_process_single_bp_success(self, mock_page_cls, bot):
        """Test processing di un singolo BP con successo."""
        mock_page = mock_page_cls.return_value
        row = {"Numero BP": "123", "Note di Ritiro": "Urgente"}

        res = bot._process_single_bp(mock_page, 0, row)

        assert res is True
        mock_page.filtra_buoni_prelievo.assert_called_with(bot.fornitore, "123", bot.data_da, bot.data_a)
        mock_page.apri_dettagli_bp.assert_called()
        mock_page.gestisci_creazione_richiesta.assert_called_with("Urgente")
        mock_page.chiudi_dettagli_bp.assert_called()

    @patch("src.bots.portale_fornitori.prenota_bp.bot.PrenotaBPPage")
    def test_process_single_bp_missing_id(self, mock_page_cls, bot):
        """Test skip se ID mancante."""
        res = bot._process_single_bp(MagicMock(), 0, {})
        assert res is False

    @patch("src.bots.portale_fornitori.prenota_bp.bot.PrenotaBPPage")
    def test_run_driver_missing(self, mock_page_cls, bot):
        bot.driver = None
        assert bot.run([]) is True  # Empty data returns True
        assert bot.run([{"a": 1}]) is False  # Data present but no driver returns False
