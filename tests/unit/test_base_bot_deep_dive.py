
from unittest.mock import MagicMock

import pytest

from src.bots.base.base_bot import BaseBot
from src.core.constants import BotStatus


class ConcreteBot(BaseBot):
    """Implementazione concreta per testare la classe base."""
    @property
    def name(self): return "TestBot"
    @property
    def description(self): return "Bot di test"
    def run(self, data): return True
    def _handle_unsaved_changes_popup(self): pass

class TestBaseBotDeepDive:
    @pytest.fixture
    def bot(self):
        return ConcreteBot("user", "pass")

    def test_safe_login_retry_on_driver_error(self, bot, mocker):
        """Verifica che il bot riprovi il login se il driver crasha all'avvio."""
        m_init = mocker.patch.object(bot, "_init_driver")
        m_login = mocker.patch.object(bot, "_login")
        m_cleanup = mocker.patch.object(bot, "cleanup")
        mocker.patch("time.sleep")
        mocker.patch.object(bot, "_check_stop")

        # Primo tentativo: errore driver
        # Secondo tentativo: successo
        m_init.side_effect = [Exception("Driver Crash"), None]
        m_login.return_value = True

        res = bot._safe_login_with_retry(max_retries=2)

        assert res is True
        assert m_init.call_count == 2
        assert m_cleanup.call_count == 1 # Chiamato dopo il primo fallimento

    def test_execute_full_lifecycle_success(self, bot, mocker):
        """Verifica la transizione degli stati durante un'esecuzione corretta."""
        mocker.patch.object(bot, "_safe_login_with_retry", return_value=True)
        mocker.patch.object(bot, "run", return_value=True)
        m_cleanup = mocker.patch.object(bot, "cleanup")

        success = bot.execute([{"data": 1}])

        assert success is True
        assert bot.status == BotStatus.COMPLETED
        m_cleanup.assert_called_once()

    def test_execute_validation_failure(self, bot, mocker):
        """Verifica che il bot si fermi se la validazione dati fallisce."""
        mocker.patch.object(bot, "validate_data", return_value=(False, "Errore dati"))

        success = bot.execute([{}])

        assert success is False
        assert bot.status == BotStatus.ERROR

    def test_save_error_state(self, bot, mocker, tmp_path):
        """Verifica il salvataggio di screenshot e HTML in caso di errore."""
        bot.driver = MagicMock()
        bot.driver.page_source = "<html>Error</html>"

        mock_config_dir = tmp_path / "config"
        mocker.patch("src.core.config_manager.CONFIG_DIR", mock_config_dir)

        bot._save_error_state("Fatal error")

        error_dir = mock_config_dir / "logs" / "errors"
        assert error_dir.exists()
        # Verifichiamo la creazione fisica dell'HTML
        files = list(error_dir.glob("*"))
        assert any(f.suffix == ".html" for f in files)
        # Per lo screenshot, verifichiamo la chiamata al driver (mockato)
        bot.driver.save_screenshot.assert_called_once()

    def test_login_page_proxy_error_detection(self, mocker):
        """Verifica il rilevamento del Proxy Error nel portale."""
        mock_driver = MagicMock()
        mock_driver.title = "502 Proxy Error"

        from src.bots.base.login_page import LoginPage
        lp = LoginPage(mock_driver, MagicMock(), isab_url="http://isab")

        res = lp.login("u", "p")
        assert res is False
        # Non deve aver nemmeno provato a cercare i campi
        mock_driver.get.assert_called_once()

    def test_login_page_session_popup_handling(self, mocker):
        """Verifica il click automatico sul popup di sessione esistente."""
        mock_driver = MagicMock()
        # Mocking WebDriverWait direttamente nel modulo per precisione
        mock_wait_cls = mocker.patch("src.bots.base.login_page.WebDriverWait")
        mock_wait_inst = mock_wait_cls.return_value

        mock_yes_btn = MagicMock()
        mock_wait_inst.until.return_value = mock_yes_btn

        from src.bots.base.login_page import LoginPage
        lp = LoginPage(mock_driver, MagicMock())
        lp._check_and_handle_session_popup()

        # Verifica che il bottone sia stato cliccato
        mock_yes_btn.click.assert_called_once()

    def test_safe_login_full_retry_logic(self, bot, mocker):
        """Verifica che il bot provi 2 volte e poi fallisca se tutto va male."""
        mocker.patch.object(bot, "_init_driver")
        mocker.patch.object(bot, "_login", return_value=False) # Fallimento costante
        mocker.patch.object(bot, "cleanup")
        mocker.patch("time.sleep")
        mocker.patch.object(bot, "_check_stop")

        res = bot._safe_login_with_retry(max_retries=2)

        assert res is False
        assert bot._login.call_count == 2
        assert bot.cleanup.call_count == 2
