"""
Bot TS - Basic Tests
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))


class TestVersion:
    """Test version module."""
    
    def test_version_exists(self):
        """Version string should exist."""
        from src.core.version import __version__
        assert __version__ is not None
        assert isinstance(__version__, str)
    
    def test_version_format(self):
        """Version should be in semver format."""
        from src.core.version import __version__
        parts = __version__.split('.')
        assert len(parts) == 3
        assert all(part.isdigit() for part in parts)
    
    def test_update_url_exists(self):
        """Update URL should be configured."""
        from src.core.version import UPDATE_URL
        assert UPDATE_URL is not None
        assert UPDATE_URL.startswith('https://')


class TestConfigManager:
    """Test configuration manager."""
    
    def test_default_config_exists(self):
        """Default config should have required keys."""
        from src.core.config_manager import DEFAULT_CONFIG
        
        required_keys = [
            'download_path',
            'isab_username',
            'isab_password',
            'browser_headless',
            'browser_timeout',
        ]
        
        for key in required_keys:
            assert key in DEFAULT_CONFIG
    
    def test_get_data_path(self):
        """Data path should be a valid directory path."""
        from src.core.config_manager import get_data_path
        
        path = get_data_path()
        assert path is not None
        assert isinstance(path, str)
        assert len(path) > 0


class TestLicenseValidator:
    """Test license validation."""
    
    def test_get_hardware_id(self):
        """Hardware ID should be retrievable."""
        from src.core.license_validator import get_hardware_id
        
        hw_id = get_hardware_id()
        assert hw_id is not None
        assert isinstance(hw_id, str)
        assert len(hw_id) > 0
        assert hw_id != "ERROR_GETTING_ID"


class TestBotRegistry:
    """Test bot registration system."""
    
    def test_registry_exists(self):
        """Bot registry should exist."""
        from src.bots import BOT_REGISTRY
        assert BOT_REGISTRY is not None
        assert isinstance(BOT_REGISTRY, dict)
    
    def test_scarico_ts_registered(self):
        """Scarico TS bot should be registered."""
        from src.bots import BOT_REGISTRY
        assert 'scarico_ts' in BOT_REGISTRY
    
    def test_dettagli_oda_registered(self):
        """Dettagli OdA bot should be registered."""
        from src.bots import BOT_REGISTRY
        assert 'dettagli_oda' in BOT_REGISTRY
    
    def test_carico_ts_registered(self):
        """Carico TS bot should be registered."""
        from src.bots import BOT_REGISTRY
        assert 'carico_ts' in BOT_REGISTRY
    
    def test_get_available_bots(self):
        """Should return dict of available bots."""
        from src.bots import get_available_bots
        
        bots = get_available_bots()
        assert isinstance(bots, dict)
        assert len(bots) >= 3


class TestBaseBot:
    """Test base bot functionality."""
    
    def test_bot_status_enum(self):
        """BotStatus enum should have expected values."""
        from src.bots.base import BotStatus
        
        assert hasattr(BotStatus, 'IDLE')
        assert hasattr(BotStatus, 'RUNNING')
        assert hasattr(BotStatus, 'COMPLETED')
        assert hasattr(BotStatus, 'ERROR')
        assert hasattr(BotStatus, 'STOPPED')


class TestScaricaTSBot:
    """Test Scarico TS bot."""
    
    def test_bot_columns(self):
        """Should have correct column configuration."""
        from src.bots.scarico_ts import ScaricaTSBot
        
        columns = ScaricaTSBot.get_columns()
        assert len(columns) == 2
        
        column_names = [col['name'] for col in columns]
        assert 'Numero OdA' in column_names
        assert 'Posizione OdA' in column_names
    
    def test_bot_metadata(self):
        """Should have correct metadata."""
        from src.bots.scarico_ts import ScaricaTSBot
        
        assert ScaricaTSBot.get_name() == "Scarico TS"
        assert ScaricaTSBot.get_description() is not None


class TestDettagliOdABot:
    """Test Dettagli OdA bot."""
    
    def test_bot_columns(self):
        """Should have correct column configuration."""
        from src.bots.dettagli_oda import DettagliOdABot
        
        columns = DettagliOdABot.get_columns()
        assert len(columns) == 1
        
        column_names = [col['name'] for col in columns]
        assert 'Numero OdA' in column_names
    
    def test_bot_metadata(self):
        """Should have correct metadata."""
        from src.bots.dettagli_oda import DettagliOdABot
        
        assert DettagliOdABot.get_name() == "Dettagli OdA"
        assert DettagliOdABot.get_description() is not None


class TestCaricoTSBot:
    """Test Carico TS bot."""
    
    def test_bot_columns(self):
        """Should have correct column configuration."""
        from src.bots.carico_ts import CaricoTSBot
        
        columns = CaricoTSBot.get_columns()
        assert len(columns) == 17
        
        column_names = [col['name'] for col in columns]
        assert 'Numero OdA' in column_names
        assert 'Codice Fiscale' in column_names
        assert 'G T' in column_names
    
    def test_bot_metadata(self):
        """Should have correct metadata."""
        from src.bots.carico_ts import CaricoTSBot
        
        assert CaricoTSBot.get_name() == "Carico TS"
        assert CaricoTSBot.get_description() is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
