import pytest
from unittest.mock import MagicMock, patch, ANY
from src.bots.base.base_bot import BaseBot
from src.core.constants import BotStatus

class ConcreteBot(BaseBot):
    """Implementazione minima per testare BaseBot."""
    @property
    def name(self): return "TestBot"
    @property
    def description(self): return "Test Description"
    
    def run(self, data):
        # Simulazione logica bot
        self.log("Running bot...")
        if data.get("fail"):
            raise Exception("Run failed")
        return True

    def _handle_unsaved_changes_popup(self):
        pass

@pytest.fixture
def bot(tmp_path):
    # Mock config
    with patch("src.core.config_manager.load_config", return_value={}):
        return ConcreteBot("user", "pass")

def test_bot_initialization(bot):
    assert bot.status == BotStatus.IDLE
    assert bot.username == "user"
    assert bot.password == "pass"

def test_init_driver_success(bot):
    """Test inizializzazione driver con mock completi."""
    with (
        patch("selenium.webdriver.Chrome") as mock_chrome,
        patch("webdriver_manager.chrome.ChromeDriverManager.install", return_value="/path/to/driver"),
        patch("selenium.webdriver.chrome.service.Service") as mock_service
    ):
        bot._init_driver()
        
        mock_chrome.assert_called_once()
        assert bot.driver is not None
        assert bot.wait is not None
        assert bot.status == BotStatus.INITIALIZING

def test_login_flow_success(bot):
    """Test flusso di login riuscito."""
    # Mock driver & components
    bot.driver = MagicMock()
    bot.login_page = MagicMock()
    bot.login_page.login.return_value = True
    
    # Mock _init_driver per non fare nulla (già abbiamo il driver mockato)
    with patch.object(bot, "_init_driver"):
        success = bot._safe_login_with_retry()
    
    assert success is True
    # BaseBot doesn't expose is_logged_in property, relying on return value
    # But we can verify login_page.login was called
    bot.login_page.login.assert_called_with("user", "pass")

def test_login_flow_failure_retry(bot):
    """Test fallimento login e retry."""
    bot.driver = MagicMock()
    bot.login_page = MagicMock()
    # Primo fallisce, secondo riesce
    bot.login_page.login.side_effect = [False, True]
    
    with (
        patch.object(bot, "_init_driver"),
        patch.object(bot, "cleanup")
    ):
        success = bot._safe_login_with_retry(max_retries=2)
        
    assert success is True
    assert bot.login_page.login.call_count == 2

def test_execute_workflow_success(bot):
    """Test intero flusso execute()."""
    # Mock passaggi interni
    with (
        patch.object(bot, "_safe_login_with_retry", return_value=True),
        patch.object(bot, "_init_driver"),
        patch.object(bot, "cleanup")
    ):
        res = bot.execute({"data": "ok"})
        
    assert res is True
    assert bot.status == BotStatus.COMPLETED

def test_execute_workflow_login_fail(bot):
    """Test fallimento execute se login fallisce."""
    with (
        patch.object(bot, "_safe_login_with_retry", return_value=False),
        patch.object(bot, "_init_driver"),
        patch.object(bot, "cleanup")
    ):
        res = bot.execute({})
        
    assert res is False
    assert bot.status == BotStatus.ERROR

def test_execute_workflow_run_fail(bot):
    """Test eccezione durante run()."""
    with (
        patch.object(bot, "_safe_login_with_retry", return_value=True),
        patch.object(bot, "_init_driver"),
        patch.object(bot, "cleanup"),
        patch.object(bot, "_save_error_state") as mock_save_err
    ):
        res = bot.execute({"fail": True})
        
    assert res is False
    assert bot.status == BotStatus.ERROR
    mock_save_err.assert_called_once() # Deve salvare screenshot errore

def test_stop_request(bot):
    """Test richiesta di stop."""
    bot.request_stop()
    assert bot._stop_requested is True
    
    # Verify check_stop raises
    with pytest.raises(InterruptedError):
        bot._check_stop()