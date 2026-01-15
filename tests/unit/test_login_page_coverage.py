import unittest
from unittest.mock import MagicMock, patch

from selenium.common.exceptions import (
    TimeoutException,
)

from src.bots.base.login_page import LoginPage


class TestLoginPageCoverage(unittest.TestCase):
    def setUp(self):
        self.mock_driver = MagicMock()
        self.mock_wait = MagicMock()
        self.logger_mock = MagicMock()
        self.page = LoginPage(
            driver=self.mock_driver,
            wait=self.mock_wait,
            logger=self.logger_mock,
            isab_url="http://test.url"
        )

    def test_attendi_scomparsa_overlay_success(self):
        # Setup mock for WebDriverWait inside the method
        with patch('src.bots.base.login_page.WebDriverWait') as MockWait:
            mock_wait_instance = MockWait.return_value
            self.page._attendi_scomparsa_overlay(5)
            mock_wait_instance.until.assert_called()
            self.logger_mock.assert_any_call(" -> Overlay di caricamento scomparso.")

    def test_attendi_scomparsa_overlay_timeout(self):
        with patch('src.bots.base.login_page.WebDriverWait') as MockWait:
            mock_wait_instance = MockWait.return_value
            mock_wait_instance.until.side_effect = TimeoutException()
            res = self.page._attendi_scomparsa_overlay(5)
            self.assertFalse(res)
            self.logger_mock.assert_any_call("⚠ Timeout (5s) attesa overlay. Proseguo con cautela.")

    def test_perform_login_form_action_success(self):
        mock_user = MagicMock()
        mock_pass = MagicMock()
        mock_btn = MagicMock()

        # Mock wait.until logic sequence
        # 1. user field, 2. pass field, 3. login btn
        self.mock_wait.until.side_effect = [mock_user, mock_pass, mock_btn]

        # Patch internal calls
        self.page._check_and_handle_session_popup = MagicMock()
        self.page._attendi_scomparsa_overlay = MagicMock()

        self.page._perform_login_form_action("u", "p")

        mock_user.send_keys.assert_called_with("u")
        mock_pass.send_keys.assert_called_with("p")
        mock_btn.click.assert_called()
        self.page._check_and_handle_session_popup.assert_called()

    def test_perform_login_form_action_fallback_js(self):
        mock_user = MagicMock()
        mock_pass = MagicMock()

        # 1. user, 2. pass, 3. btn (raises)
        self.mock_wait.until.side_effect = [
            mock_user,
            mock_pass,
            TimeoutException()
        ]

        self.mock_driver.find_element.return_value = "fallback_element"
        self.page._check_and_handle_session_popup = MagicMock()
        self.page._attendi_scomparsa_overlay = MagicMock()

        self.page._perform_login_form_action("u", "p")

        self.mock_driver.execute_script.assert_called_with("arguments[0].click();", "fallback_element")

    def test_check_and_handle_session_popup_found(self):
        with patch('src.bots.base.login_page.WebDriverWait') as MockWait:
            mock_wait_instance = MockWait.return_value
            mock_yes = MagicMock()
            mock_wait_instance.until.return_value = mock_yes

            with patch('time.sleep'):
                self.page._check_and_handle_session_popup()
                mock_yes.click.assert_called()
                self.logger_mock.assert_any_call("⚠️ Rilevata sessione precedente. Clicco su 'Si' per forzare l'accesso.")

    def test_verify_logged_in_via_ui_false(self):
        with patch('src.bots.base.login_page.WebDriverWait') as MockWait:
            MockWait.return_value.until.side_effect = Exception("Not found")
            self.assertFalse(self.page._verify_logged_in_via_ui())

    def test_login_proxy_error(self):
        self.mock_driver.title = "Proxy Error"
        res = self.page.login("u", "p")
        self.assertFalse(res)
        self.logger_mock.assert_any_call("⚠ Rilevato 'Proxy Error' durante l'accesso iniziale.")

    def test_login_already_logged_in(self):
        self.page._attendi_scomparsa_overlay = MagicMock()
        self.page._verify_logged_in_via_ui = MagicMock(return_value=True)

        # First wait raises Timeout (username field not found), triggering already logged check
        with patch('src.bots.base.login_page.WebDriverWait') as MockWait:
             MockWait.return_value.until.side_effect = TimeoutException()

             res = self.page.login("u", "p")
             self.assertTrue(res)
             self.logger_mock.assert_any_call("✓ Rilevata sessione attiva (skip login).")

    def test_login_retry_refresh(self):
        self.page._attendi_scomparsa_overlay = MagicMock()
        self.page._verify_logged_in_via_ui = MagicMock(return_value=False)
        self.page._perform_login_form_action = MagicMock()

        # First wait raises Timeout
        with patch('src.bots.base.login_page.WebDriverWait') as MockWait:
             MockWait.return_value.until.side_effect = TimeoutException()

             res = self.page.login("u", "p")

             self.mock_driver.refresh.assert_called()
             self.page._perform_login_form_action.assert_called_with("u", "p")
             self.assertTrue(res)

    def test_login_timeout_general(self):
        self.page._attendi_scomparsa_overlay = MagicMock()

        # First wait raises Timeout
        with patch('src.bots.base.login_page.WebDriverWait') as MockWait:
             MockWait.return_value.until.side_effect = TimeoutException()
             self.page._verify_logged_in_via_ui = MagicMock(return_value=False)
             self.page._perform_login_form_action = MagicMock(side_effect=Exception("Refresh failed"))

             res = self.page.login("u", "p")
             self.assertFalse(res)

    def test_login_exception_generic(self):
        self.mock_driver.get.side_effect = Exception("Boom")
        res = self.page.login("u", "p")
        self.assertFalse(res)
        self.logger_mock.assert_any_call("✗ Errore login: Boom")
