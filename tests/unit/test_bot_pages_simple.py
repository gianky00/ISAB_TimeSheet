from unittest.mock import MagicMock, patch

from src.bots.portale_fornitori.scarico_ts.pages.scarico_ts_page import ScaricoTSPage


class TestBotPagesSimpleLogic:
    def test_scarico_ts_navigation_logic(self):
        mock_driver = MagicMock()
        page = ScaricoTSPage(mock_driver)

        with patch.object(page, "_wait_for_overlay"):
            # Mock find_element/wait.until to avoid real selenium errors
            page.wait = MagicMock()
            res = page.navigate_to_timesheet()
            assert res is True
            assert page.wait.until.called

    def test_scarico_ts_setup_filters(self):
        mock_driver = MagicMock()
        page = ScaricoTSPage(mock_driver)
        page.wait = MagicMock()
        page.long_wait = MagicMock()

        with (
            patch.object(page, "_wait_for_overlay"),
            patch(
                "src.bots.portale_fornitori.scarico_ts.pages.scarico_ts_page.ActionChains"
            ) as mock_ac,
        ):
            res = page.setup_filters("KK123", "01.01.2024")
            assert res is True
            assert mock_ac.called

    def test_timbrature_page_init(self):
        from src.bots.portale_fornitori.timbrature.pages.timbrature_page import (
            TimbraturePage,
        )

        mock_driver = MagicMock()
        page = TimbraturePage(mock_driver)
        assert page is not None
        assert page.wait is not None
