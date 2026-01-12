from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.bots.portale_fornitori.scarico_ts.bot import ScaricaTSBot
from src.bots.portale_fornitori.timbrature.bot import TimbratureBot
from src.bots.safework.pdl.bot import SafeWorkPDLBot


class TestBotTimingSequences:
    """
    Questa suite di test verifica che le pause (time.sleep) critiche siano 
    presenti e chiamate nell'ordine corretto per tutti i bot.
    """

    @pytest.fixture(autouse=True)
    def cleanup_mocks(self):
        """Assicura che ogni test parta da uno stato pulito."""
        yield
        # Eventuale cleanup globale se necessario

    @pytest.fixture
    def mock_scarico_bot(self):
        with patch("src.bots.base.base_bot.BaseBot._init_driver"):
            bot = ScaricaTSBot(username="u", password="p", fornitore="F1")
            bot.driver = MagicMock()
            bot.wait = MagicMock()
            bot.long_wait = MagicMock()
            return bot

    @pytest.fixture
    def mock_safework_bot(self):
        with patch("src.bots.safework.base.SafeworkBaseBot._init_driver"), \
             patch("src.bots.safework.pdl.bot.SafeWorkPDLBot.__init__", return_value=None):
            bot = SafeWorkPDLBot("u", "p")
            bot.driver = MagicMock()
            bot.wait = MagicMock()
            bot.log = MagicMock()
            bot.download_path = "downloads"
            bot._stop_requested = False
            return bot

    @pytest.fixture
    def mock_timbrature_bot(self):
        with patch("src.bots.base.base_bot.BaseBot._init_driver"):
            bot = TimbratureBot(username="u", password="p", fornitore="F1")
            bot.driver = MagicMock()
            bot.wait = MagicMock()
            bot.long_wait = MagicMock()
            return bot

    def test_scarico_ts_filters_timing(self, mock_scarico_bot):
        """Verifica la pausa critica durante l'impostazione dei filtri in Scarico TS."""
        mock_el = MagicMock()
        mock_scarico_bot.wait.until.return_value = mock_el
        mock_scarico_bot.long_wait.until.return_value = mock_el

        with patch("time.sleep") as mock_sleep, \
             patch.object(ScaricaTSBot, "_attendi_scomparsa_overlay"):

            with patch("src.bots.portale_fornitori.scarico_ts.bot.ActionChains") as mock_action:
                mock_scarico_bot._setup_filters()

            assert any(c.args[0] == 0.5 for c in mock_sleep.call_args_list)

    def test_safework_pdl_search_timing(self, mock_safework_bot):
        """Verifica la pausa critica dopo la ricerca di un PDL."""
        data = [{"numero_pdl": "123456"}]

        with patch("time.sleep") as mock_sleep, \
             patch.object(SafeWorkPDLBot, "_gestisci_alert_ricerca", return_value=False), \
             patch.object(SafeWorkPDLBot, "_attendi_scomparsa_overlay"), \
             patch.object(SafeWorkPDLBot, "_attendi_e_ritorna_nuovo_pdf", return_value="f.pdf"), \
             patch("src.utils.document_processor.DocumentProcessor.merge_pdfs", return_value=True), \
             patch("os.rename"), patch("os.remove"), patch("os.path.exists", return_value=True), \
             patch("builtins.open"), patch("src.bots.safework.pdl.bot.fitz"), \
             patch.object(mock_safework_bot, "_check_stop"):

            mock_safework_bot.wait.until.return_value = MagicMock()
            mock_safework_bot.driver.find_element.return_value.is_displayed.return_value = True

            mock_safework_bot.run(data)

            calls = [c.args[0] for c in mock_sleep.call_args_list]
            assert 0.5 in calls
            assert 1 in calls

    def test_timbrature_navigation_timing(self, mock_timbrature_bot):
        """Verifica le pause durante la navigazione nel bot Timbrature."""
        from src.bots.portale_fornitori.timbrature.pages.timbrature_page import (
            TimbraturePage,
        )

        with patch("time.sleep") as mock_sleep, \
             patch.object(TimbraturePage, "_wait_for_overlay"):

            page = TimbraturePage(mock_timbrature_bot.driver)
            # Mock elements
            mock_el = MagicMock()
            page.wait = MagicMock()
            page.wait.until.return_value = mock_el

            with patch("src.bots.portale_fornitori.timbrature.pages.timbrature_page.ActionChains") as mock_action:
                page.navigate_to_timbrature()

            calls = [c.args[0] for c in mock_sleep.call_args_list]
            # Ci aspettiamo 1.5s dopo il click su Report e 1.0s dopo la navigazione tastiera
            assert 1.5 in calls
            assert 1.0 in calls

    def test_timbrature_supplier_selection_timing(self, mock_timbrature_bot):
        """Verifica la pausa durante la selezione del fornitore."""
        from src.bots.portale_fornitori.timbrature.pages.timbrature_page import (
            TimbraturePage,
        )

        with patch("time.sleep") as mock_sleep, \
             patch.object(TimbraturePage, "_wait_for_overlay"):

            page = TimbraturePage(mock_timbrature_bot.driver)
            page.wait = MagicMock()
            page.wait.until.return_value = MagicMock()

            # Mock WebDriverWait interno a _select_supplier
            with patch("src.bots.portale_fornitori.timbrature.pages.timbrature_page.WebDriverWait") as mock_wait_class:
                mock_wait_instance = mock_wait_class.return_value
                mock_wait_instance.until.return_value = MagicMock()

                page._select_supplier("FORNITORE_TEST")

            calls = [c.args[0] for c in mock_sleep.call_args_list]
            # Aspetta l'animazione della lista (0.5s) e lo scroll (0.3s)
            assert 0.5 in calls
            assert 0.3 in calls

    def test_regression_protection_scarico_ts(self, mock_scarico_bot):
        """Verifica che il polling di download esegua gli sleep."""
        source_dir = Path("source")
        dest_dir = Path("dest")
        mock_scarico_bot.wait.until.return_value = MagicMock()

        with patch("time.sleep") as mock_sleep, \
             patch("time.time", side_effect=[0, 1, 2, 3, 4, 5, 40]), \
             patch("pathlib.Path.iterdir") as mock_iter:

            mock_iter.side_effect = [[Path("f.crdownload")], [Path("f.crdownload")], []]

            mock_scarico_bot._download_excel(source_dir, dest_dir, "ODA", "10")
            assert any(c.args[0] == 0.5 for c in mock_sleep.call_args_list)
