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
        with (
            patch("src.bots.safework.base.SafeworkBaseBot._init_driver"),
            patch("src.bots.safework.pdl.bot.SafeWorkPDLBot.__init__", return_value=None),
        ):
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
        """Verifica la corretta attesa durante l'impostazione dei filtri in Scarico TS."""
        mock_el = MagicMock()
        mock_scarico_bot.wait.until.return_value = mock_el
        mock_scarico_bot.long_wait.until.return_value = mock_el

        with (
            patch("time.sleep"),
            patch.object(ScaricaTSBot, "_attendi_scomparsa_overlay") as mock_wait_overlay,
        ):
            with patch("src.bots.portale_fornitori.scarico_ts.bot.ActionChains"):
                mock_scarico_bot._setup_filters()

            # Non controlliamo più time.sleep(0.5) perché rimosso per efficienza.
            # Verifichiamo invece che venga chiamato il metodo corretto di attesa overlay.
            assert mock_wait_overlay.called

    def test_safework_pdl_search_timing(self, mock_safework_bot):
        """Verifica la pausa critica dopo la ricerca di un PDL."""
        with patch("time.sleep") as mock_sleep:
            # Setup driver/wait mock per arrivare allo sleep
            mock_safework_bot.wait.until.return_value = MagicMock()

            # Eseguiamo solo il metodo di ricerca che contiene lo sleep di 0.5s
            mock_safework_bot._esegui_ricerca_pdl("123456/S")

            calls = [c.args[0] for c in mock_sleep.call_args_list]
            assert 0.5 in calls

    def test_timbrature_navigation_timing(self, mock_timbrature_bot):
        """Verifica le attese durante la navigazione nel bot Timbrature."""
        from src.bots.portale_fornitori.timbrature.pages.timbrature_page import (
            TimbraturePage,
        )

        with (
            patch("time.sleep"),
            patch.object(TimbraturePage, "_wait_for_overlay") as mock_wait_overlay,
        ):
            page = TimbraturePage(mock_timbrature_bot.driver)
            # Mock elements
            mock_el = MagicMock()
            page.wait = MagicMock()
            page.wait.until.return_value = mock_el

            with patch("src.bots.portale_fornitori.timbrature.pages.timbrature_page.ActionChains"):
                page.navigate_to_timbrature()

            # Verifichiamo che _wait_for_overlay sia stato chiamato invece di time.sleep espliciti
            assert mock_wait_overlay.called

    def test_timbrature_supplier_selection_timing(self, mock_timbrature_bot):
        """Verifica l'attesa durante la selezione del fornitore."""
        from src.bots.portale_fornitori.timbrature.pages.timbrature_page import (
            TimbraturePage,
        )

        with (
            patch("time.sleep"),
            patch.object(TimbraturePage, "_wait_for_overlay") as mock_wait_overlay,
        ):
            page = TimbraturePage(mock_timbrature_bot.driver)
            page.wait = MagicMock()
            page.wait.until.return_value = MagicMock()

            # Mock WebDriverWait interno a _select_supplier
            with patch(
                "src.bots.portale_fornitori.timbrature.pages.timbrature_page.WebDriverWait"
            ) as mock_wait_class:
                mock_wait_instance = mock_wait_class.return_value
                mock_wait_instance.until.return_value = MagicMock()

                page._select_supplier("FORNITORE_TEST")

            # Verifichiamo che _wait_for_overlay sia stato chiamato invece di time.sleep espliciti
            assert mock_wait_overlay.called

    def test_regression_protection_scarico_ts(self, mock_scarico_bot):
        """Verifica che il polling di download esegua gli sleep."""
        source_dir = Path("source")
        files_before = set()

        with (
            patch("time.sleep") as mock_sleep,
            patch("time.time", side_effect=[0, 1, 2, 3, 4, 5, 40]),
            patch("pathlib.Path.iterdir") as mock_iter,
        ):
            # Simula: prima iterazione vede .crdownload, seconda iterazione vede solo file_before, terza timeout o successo
            mock_iter.side_effect = [[Path("f.crdownload")], [], []]

            mock_scarico_bot._wait_for_new_file(source_dir, files_before, timeout=10)
            assert any(c.args[0] == 0.5 for c in mock_sleep.call_args_list)
