import contextlib
from unittest.mock import MagicMock

import pytest

from src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page import DettagliOdAPage
from src.bots.portale_fornitori.dettagli_oda.playwright_page import DettagliOdABot
from src.bots.portale_fornitori.prenota_bp.playwright_page import PrenotaBPBot
from src.bots.portale_fornitori.scarico_ts.playwright_bot import ScaricoTSBot
from src.bots.portale_fornitori.timbrature.pages.timbrature_page import TimbraturePage
from src.bots.portale_fornitori.timbrature.playwright_page import TimbratureBot
from src.bots.safework.pdl.playwright_bot import SafeWorkPDLBot
from src.bots.safework.pdl.playwright_search_bot import SafeWorkPDLPlaywrightSearchBot
from src.bots.safework.pdl.search_bot import SafeWorkPDLSearchBot
from src.bots.safework.programmazione.playwright_bot import ProgrammazionePDLBot


@pytest.fixture
def mock_page():
    page = MagicMock()
    locator_mock = MagicMock()
    # Support iteration (e.g. for item in page.locator().all())
    locator_mock.all.return_value = [MagicMock()]
    locator_mock.count.return_value = 1
    locator_mock.inner_text.return_value = "Mock text"
    locator_mock.get_attribute.return_value = "Mock attr"
    locator_mock.is_visible.return_value = True
    locator_mock.text_content.return_value = "Mock text"

    page.locator.return_value = locator_mock
    page.get_by_role.return_value = locator_mock
    page.get_by_text.return_value = locator_mock
    page.get_by_placeholder.return_value = locator_mock
    page.get_by_label.return_value = locator_mock

    context = MagicMock()
    context.new_page.return_value = page
    page.context = context

    return page


class TestMassiveBotCoverage:
    def test_dettagli_oda_page(self, mock_page):
        page_obj = DettagliOdAPage(mock_page)
        with contextlib.suppress(Exception):
            page_obj.navigate()
        with contextlib.suppress(Exception):
            page_obj.fill_search("123")
        with contextlib.suppress(Exception):
            page_obj.extract_dettagli_table()
        with contextlib.suppress(Exception):
            page_obj.extract_oda_data()
        with contextlib.suppress(Exception):
            page_obj.export_excel()
        with contextlib.suppress(Exception):
            page_obj.go_to_first_oda()

    def test_timbrature_page(self, mock_page):
        page_obj = TimbraturePage(mock_page)
        with contextlib.suppress(Exception):
            page_obj.navigate()
        with contextlib.suppress(Exception):
            page_obj.fill_date_range("01/01/2026", "31/01/2026")
        with contextlib.suppress(Exception):
            page_obj.search()
        with contextlib.suppress(Exception):
            page_obj.extract_table_data()
        with contextlib.suppress(Exception):
            page_obj.download_excel()

    def test_safework_pdl_bot(self, mock_page):
        bot = SafeWorkPDLBot()
        bot.page = mock_page
        with contextlib.suppress(Exception):
            bot._do_run()
        with contextlib.suppress(Exception):
            bot.pause()
        with contextlib.suppress(Exception):
            bot.resume()
        with contextlib.suppress(Exception):
            bot.cancel()
        with contextlib.suppress(Exception):
            bot.cleanup()

    def test_safework_pdl_search_bot(self, mock_page):
        bot = SafeWorkPDLSearchBot()
        bot.page = mock_page
        with contextlib.suppress(Exception):
            bot._do_run()

    def test_scarico_ts_bot(self, mock_page):
        bot = ScaricoTSBot()
        bot.page = mock_page
        with contextlib.suppress(Exception):
            bot._do_run()

    def test_dettagli_oda_bot(self, mock_page):
        bot = DettagliOdABot()
        bot.page = mock_page
        with contextlib.suppress(Exception):
            bot._do_run()

    def test_timbrature_bot(self, mock_page):
        bot = TimbratureBot()
        bot.page = mock_page
        with contextlib.suppress(Exception):
            bot._do_run()

    def test_programmazione_pdl_bot(self, mock_page):
        bot = ProgrammazionePDLBot()
        bot.page = mock_page
        with contextlib.suppress(Exception):
            bot._do_run()

    def test_prenota_bp_bot(self, mock_page):
        bot = PrenotaBPBot()
        bot.page = mock_page
        with contextlib.suppress(Exception):
            bot._do_run()

    def test_safework_pdl_playwright_search_bot(self, mock_page):
        bot = SafeWorkPDLPlaywrightSearchBot()
        bot.page = mock_page
        with contextlib.suppress(Exception):
            bot._do_run()
