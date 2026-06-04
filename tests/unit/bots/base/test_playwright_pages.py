from unittest.mock import MagicMock, patch

from src.infrastructure.bots.base.playwright_base_page import PlaywrightBasePage
from src.infrastructure.bots.base.playwright_login_page import PlaywrightLoginPage
from src.infrastructure.bots.portale_fornitori.common.locators import LoginLocators


class TestPlaywrightBasePage:
    def test_wait_overlay(self):
        mock_page = MagicMock()
        page_obj = PlaywrightBasePage(mock_page)

        page_obj._wait_overlay(timeout_ms=100)
        assert mock_page.wait_for_selector.called
        # Check if xpath is used correctly
        args, kwargs = mock_page.wait_for_selector.call_args
        assert "xpath=" in args[0]
        assert kwargs["state"] == "hidden"

    def test_select_combobox_item_success(self):
        mock_page = MagicMock()
        page_obj = PlaywrightBasePage(mock_page)

        # Mock locator chain: page.locator().first
        mock_arrow = MagicMock()
        mock_option = MagicMock()

        # page.locator(s) -> mock_locator
        # mock_locator.first -> mock_element
        mock_locator_arrow = MagicMock()
        mock_locator_arrow.first = mock_arrow

        mock_locator_option = MagicMock()
        mock_locator_option.first = mock_option

        mock_page.locator.side_effect = lambda s: mock_locator_option if "li[" in s else mock_locator_arrow

        res = page_obj._select_combobox_item("input", "arrow", "Item 1")
        assert res is True
        assert mock_option.evaluate.called
        assert "click" in mock_option.evaluate.call_args[0][0]


class TestPlaywrightLoginPage:
    def test_login_session_already_active(self):
        mock_page = MagicMock()
        login_page = PlaywrightLoginPage(mock_page, isab_url="http://isab.it")

        # Simula sessione già attiva (Settings button trovato)
        mock_page.goto.return_value = MagicMock(status=200)
        mock_page.locator.return_value.is_visible.return_value = True  # Username field visible

        # Mock verify_logged_in_via_ui success
        with patch.object(PlaywrightLoginPage, "_verify_logged_in_via_ui", return_value=True):
            res = login_page.login("user", "pass")
            assert res is True

    def test_login_full_flow(self):
        mock_page = MagicMock()
        login_page = PlaywrightLoginPage(mock_page, isab_url="http://isab.it")

        mock_page.goto.return_value = MagicMock(status=200)
        # 1. verify false
        # 2. perform action
        # 3. verify true
        with patch.object(PlaywrightLoginPage, "_verify_logged_in_via_ui") as mock_verify:
            mock_verify.side_effect = [False, True]

            with patch.object(PlaywrightLoginPage, "_perform_login_form_action") as mock_action:
                res = login_page.login("user", "pass")
                assert res is True
                assert mock_action.called

    def test_perform_login_form_action(self):
        mock_page = MagicMock()
        login_page = PlaywrightLoginPage(mock_page)

        login_page._perform_login_form_action("user", "pass", "ISAB")

        assert mock_page.fill.call_count >= 2
        # Check username and password fill
        mock_page.fill.assert_any_call(login_page._get_selector(LoginLocators.USERNAME_FIELD), "user")
        assert mock_page.locator.return_value.click.called
