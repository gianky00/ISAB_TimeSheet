from unittest.mock import MagicMock, patch

from src.infrastructure.bots.portale_fornitori.prenota_bp.bot import PrenotaBPBot


class TestPrenotaBPBot:
    def test_validate_data_missing_bp(self):
        bot = PrenotaBPBot(username="u", password="p")
        valid, msg = bot.validate_data([{"note": "test"}])
        assert valid is False
        assert "Numero BP mancante" in msg

    def test_validate_data_success(self):
        bot = PrenotaBPBot(username="u", password="p")
        valid, _msg = bot.validate_data([{"numero_bp": "BP001"}])
        assert valid is True

    @patch("src.infrastructure.bots.portale_fornitori.prenota_bp.bot.PrenotaBPPage")
    def test_run_success_flow(self, mock_page_class):
        bot = PrenotaBPBot(username="u", password="p")
        bot.update_step = MagicMock()
        bot.driver = MagicMock()  # FIX: Inizializza driver

        mock_page = mock_page_class.return_value
        data = [{"numero_bp": "BP1"}]

        res = bot.run(data)

        assert res is True
        mock_page.navigate_to_gestione_bp.assert_called_once()
        mock_page.filtra_buoni_prelievo.assert_called_once()

        assert mock_page.apri_dettagli_bp.called
        assert mock_page.gestisci_creazione_richiesta.called

    @patch("src.infrastructure.bots.portale_fornitori.prenota_bp.bot.PrenotaBPPage")
    def test_run_navigation_fail(self, mock_page_class):
        bot = PrenotaBPBot(username="u", password="p")
        mock_page = mock_page_class.return_value
        mock_page.navigate_to_gestione_bp.side_effect = Exception("Nav error")

        res = bot.run([{"numero_bp": "BP1"}])
        assert res is False

    def test_get_row_value_variations(self):
        bot = PrenotaBPBot()
        row = {"NUMERO_BP": "123", "note_ritiro ": "  some note  "}

        assert bot._get_row_value(row, "numero_bp") == "123"
        assert bot._get_row_value(row, "note_ritiro") == "some note"
        assert bot._get_row_value(row, "invalid") == ""
