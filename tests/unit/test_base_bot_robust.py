from unittest.mock import MagicMock, patch

import pytest

from src.bots.base.base_bot import BaseBot
from src.core.constants import BotStatus, Timeouts


# Classe concreta minima per testare BaseBot (che è astratta)
class ConcreteBot(BaseBot):
    @property
    def name(self) -> str:
        return "TestBot"

    @property
    def description(self) -> str:
        return "A bot for testing BaseBot"

    @staticmethod
    def get_columns():  # noqa: ANN205
        return []

    def run(self, data):  # noqa: ANN001
        return True


class TestBaseBotRobust:
    @pytest.fixture
    def mock_driver_cls(self):
        with patch("src.bots.base.base_bot.webdriver.Chrome") as mock:
            yield mock

    @pytest.fixture
    def mock_service(self):
        with patch("src.bots.base.base_bot.Service") as mock:
            yield mock

    @pytest.fixture
    def mock_options(self):
        with patch("src.bots.base.base_bot.Options") as mock:
            yield mock

    @pytest.fixture
    def mock_chrome_manager(self):
        with (
            patch("webdriver_manager.chrome.ChromeDriverManager") as mock,
            patch("src.bots.base.base_bot.Path.exists", return_value=False),
        ):
            mock.return_value.install.return_value = "/path/to/chromedriver.exe"
            yield mock

    @pytest.fixture
    def bot(self):
        return ConcreteBot("user", "pass")

    # --- Init Tests ---

    def test_init_defaults(self, bot):  # noqa: ANN001
        """Test inizializzazione default."""
        assert bot.username == "user"
        assert bot.password == "pass"
        assert bot.headless is False
        assert bot.timeout == Timeouts.DEFAULT
        assert bot.status == BotStatus.IDLE
        assert bot._stop_requested is False

    # --- Driver Init Tests ---

    def test_init_driver_success(self, bot, mock_driver_cls, mock_service, mock_chrome_manager, mock_options):  # noqa: ANN001
        """Test inizializzazione driver con successo."""
        # Mock chromedriver path
        mock_chrome_manager.return_value.install.return_value = "C:/drivers/chromedriver.exe"

        # Call
        bot._init_driver()

        # Assertions
        mock_chrome_manager.return_value.install.assert_called_once()
        mock_service.assert_called_with("C:/drivers/chromedriver.exe")
        mock_driver_cls.assert_called_once()

        # Check options
        # Options() viene istanziato
        # Ci aspettiamo che add_argument sia stato chiamato
        mock_opts_instance = mock_options.return_value
        assert mock_opts_instance.add_argument.call_count > 0

        # Verifica anti-detection script
        bot.driver.execute_cdp_cmd.assert_called_with(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
        )
        assert bot.status == BotStatus.INITIALIZING

    def test_init_driver_headless_config(self, mock_driver_cls, mock_service, mock_chrome_manager):  # noqa: ANN001
        """Test configurazione headless."""
        bot = ConcreteBot("user", "pass", headless=True)

        with patch("src.bots.base.base_bot.config_manager.load_config", return_value={}):
            bot._init_driver()

            # Recupera options passate al driver
            _, _kwargs = mock_driver_cls.call_args
            # options = kwargs["options"]  # Unused variable removed  # noqa: ERA001

            # Verifica che --headless=new sia stato aggiunto
            # Nota: Options è mockato, quindi dobbiamo vedere le chiamate su di esso
            # Ma qui Options è istanziato dentro _init_driver -> _get_chrome_options
            # Dobbiamo intercettare l'istanza di Options creata dentro.
            # Siccome non ho mockato Options in questo test specifico, uso un altro approccio
            # (Il test precedente copriva le chiamate generiche, per headless specifico meglio mockare Options)

    def test_get_chrome_options_headless(self, bot):  # noqa: ANN001
        """Test _get_chrome_options logica headless."""
        bot.headless = True
        with patch("src.bots.base.base_bot.config_manager.load_config", return_value={}):
            # Mock Options class inside the method context or assume it returns a mock if patched globally
            # Qui Options è reale (non mockato nella fixture globale di questo test method)
            # ma selenium.webdriver.chrome.options.Options è una classe reale.

            options = bot._get_chrome_options()

            # Verifica argomenti
            # selenium Options usa .arguments (lista) o ._arguments
            args = list(options.arguments)
            assert "--headless=new" in args
            assert "--no-sandbox" in args

    def test_driver_error_handling(self, bot, mock_chrome_manager):  # noqa: ANN001
        """Test gestione errore init driver."""
        mock_chrome_manager.return_value.install.side_effect = Exception("Download failed")

        # Dovrebbe catturare l'eccezione interna, fallire il download e poi fallire init service
        # perché non trova neanche driver locale (assumendo default mock environment)
        with pytest.raises(RuntimeError, match="Chromedriver service non disponibile"):
            bot._init_driver()

    # --- Execution Flow Tests ---

    @patch("src.core.license_validator.verify_license", return_value=(True, "OK"))
    @patch("src.core.license_updater.run_update")
    @patch("src.bots.base.base_bot.LoginPage")
    def test_execute_success(self, mock_login_page_cls, mock_update, mock_verify, bot):  # noqa: ANN001
        """Test flusso execute completo con successo."""
        # Setup mocks
        bot._init_driver = MagicMock()
        bot._login = MagicMock(return_value=True)
        bot.cleanup = MagicMock()
        bot.run = MagicMock(return_value=True)

        data = [{"id": 1}]

        # Execute
        res = bot.execute(data)

        assert res is True
        bot._init_driver.assert_called_once()
        bot._login.assert_called_once()
        bot.run.assert_called_once_with(data)
        bot.cleanup.assert_called_once()
        mock_update.assert_called_once()
        mock_verify.assert_called_once()
        assert bot.status == BotStatus.COMPLETED

    @patch("src.core.license_validator.verify_license", return_value=(True, "OK"))
    @patch("src.core.license_updater.run_update")
    def test_execute_validation_fail(self, mock_update, mock_verify, bot):  # noqa: ANN001
        """Test fallimento validazione."""
        bot.validate_data = MagicMock(return_value=(False, "Bad data"))
        bot.cleanup = MagicMock()

        res = bot.execute([{"id": 1}])

        assert res is False
        assert bot.status == BotStatus.ERROR
        # Cleanup non deve essere chiamato perché validation fallisce PRIMA del blocco try/finally del driver
        bot.cleanup.assert_not_called()

    @patch("src.core.license_validator.verify_license", return_value=(True, "OK"))
    @patch("src.core.license_updater.run_update")
    @patch("src.bots.base.base_bot.LoginPage")
    def test_execute_login_fail(self, mock_login_page_cls, mock_update, mock_verify, bot):  # noqa: ANN001
        """Test fallimento login."""
        bot._init_driver = MagicMock()
        bot._login = MagicMock(return_value=False)
        bot.cleanup = MagicMock()

        res = bot.execute([{"id": 1}])

        assert res is False
        assert bot.status == BotStatus.ERROR
        bot.cleanup.assert_called()  # Chiamato da _safe_login_with_retry o finally?

    @patch("src.core.license_validator.verify_license", return_value=(True, "OK"))
    @patch("src.core.license_updater.run_update")
    def test_execute_exception_during_run(self, mock_update, mock_verify, bot):  # noqa: ANN001
        """Test eccezione durante run."""
        bot._init_driver = MagicMock()
        bot._login = MagicMock(return_value=True)
        bot.run = MagicMock(side_effect=Exception("Boom"))
        bot._save_error_state = MagicMock()

        res = bot.execute([{"id": 1}])

        assert res is False
        assert bot.status == BotStatus.ERROR
        bot._save_error_state.assert_called()

    # --- Stop Mechanism Tests ---

    def test_request_stop(self, bot):  # noqa: ANN001
        """Test richiesta stop."""
        bot.request_stop()
        assert bot._stop_requested is True

        with pytest.raises(InterruptedError, match="Bot interrotto dall'utente"):
            bot._check_stop()

    # --- Cleanup Tests ---

    def test_cleanup(self, bot):  # noqa: ANN001
        """Test cleanup chiude driver."""
        mock_driver = MagicMock()
        bot.driver = mock_driver

        bot.cleanup()

        mock_driver.quit.assert_called_once()
        assert bot.driver is None

    def test_cleanup_safe(self, bot):  # noqa: ANN001
        """Test cleanup non esplode se driver è None o quit fallisce."""
        bot.driver = None
        bot.cleanup()  # No error

        mock_driver = MagicMock()
        mock_driver.quit.side_effect = Exception("Error closing")
        bot.driver = mock_driver
        bot.cleanup()  # No error propagate
        assert bot.driver is None

    # --- Safe Login Tests ---

    def test_safe_login_retry_success(self, bot):  # noqa: ANN001
        """Test login riesce al secondo tentativo."""
        bot._init_driver = MagicMock()
        # Primo tentativo fallisce (raise Exception), secondo riesce (return None), poi _login True
        # _init_driver non ritorna nulla. Se fallisce alza eccezione.
        # _login ritorna bool.

        # Tentativo 1: init ok, login fail -> cleanup, retry
        # Tentativo 2: init ok, login success -> return True

        # Mock _login: False, True
        bot._login = MagicMock(side_effect=[False, True])
        bot.cleanup = MagicMock()

        res = bot._safe_login_with_retry(max_retries=2)

        assert res is True
        assert bot._init_driver.call_count == 2  # noqa: PLR2004
        assert bot._login.call_count == 2  # noqa: PLR2004
        assert bot.cleanup.call_count == 1  # Chiamato dopo il primo fallimento

    def test_safe_login_retry_fail(self, bot):  # noqa: ANN001
        """Test login fallisce dopo tutti i tentativi."""
        bot._init_driver = MagicMock()
        bot._login = MagicMock(return_value=False)
        bot.cleanup = MagicMock()

        res = bot._safe_login_with_retry(max_retries=2)

        assert res is False
        assert bot._init_driver.call_count == 2  # noqa: PLR2004
        assert bot._login.call_count == 2  # noqa: PLR2004
        assert bot.cleanup.call_count == 2  # Chiamato dopo ogni fallimento  # noqa: PLR2004
