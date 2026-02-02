import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests
from cryptography.fernet import Fernet

from src.core import license_updater
from src.core.license_updater import GRACE_PERIOD_KEY


class TestLicenseUpdaterRobust:
    @pytest.fixture
    def mock_data_dir(self, tmp_path):
        """Mocka la directory dei dati."""
        data_dir = tmp_path / "AppData"
        license_dir = data_dir / "Licenza"
        license_dir.mkdir(parents=True)
        
        with patch("src.core.config_manager.get_data_path", return_value=str(data_dir)):
            yield license_dir

    @pytest.fixture
    def mock_time(self):
        """Mocka il tempo fidato."""
        now = datetime.now(timezone.utc)
        with patch("src.core.time_manager.get_trusted_time") as mock:
            mock.return_value = (now, True)
            yield mock

    @pytest.fixture
    def mock_requests(self):
        with patch("requests.get") as mock:
            yield mock

    def test_get_github_token(self):
        """Verifica ricostruzione token."""
        token = license_updater.get_github_token()
        assert token.startswith("ghp_")
        assert len(token) > 10

    def test_run_update_success(self, mock_requests, mock_data_dir, mock_time):
        """Test aggiornamento licenza con successo."""
        # Setup mock responses for config.dat and manifest.json
        def side_effect(url, **kwargs):
            resp = MagicMock()
            resp.status_code = 200
            if "config.dat" in url:
                resp.content = b"fake_config_content"
            elif "manifest.json" in url:
                resp.content = b'{"valid": true}'
            return resp
            
        mock_requests.side_effect = side_effect
        
        with patch("src.core.license_validator.get_hardware_id", return_value="HWID123"):
            success = license_updater.run_update()
            
        assert success is True
        assert (mock_data_dir / "config.dat").exists()
        assert (mock_data_dir / "manifest.json").exists()
        # Verifica che il grace timestamp sia stato aggiornato
        assert (mock_data_dir / "validity.token").exists()

    def test_run_update_offline(self, mock_requests, mock_data_dir):
        """Test fallimento aggiornamento per offline."""
        mock_requests.side_effect = requests.RequestException("Connection Error")
        
        with patch("src.core.license_validator.get_hardware_id", return_value="HWID123"):
            success = license_updater.run_update()
            
        assert success is False
        assert not (mock_data_dir / "config.dat").exists()

    def test_run_update_not_found(self, mock_requests, mock_data_dir):
        """Test file non trovati su GitHub (404)."""
        resp = MagicMock()
        resp.status_code = 404
        mock_requests.return_value = resp
        
        with patch("src.core.license_validator.get_hardware_id", return_value="HWID123"):
            success = license_updater.run_update()
            
        assert success is False

    def test_grace_period_valid(self, mock_data_dir, mock_time):
        """Test periodo di grazia valido."""
        # Crea token valido (1 giorno fa)
        cipher = Fernet(GRACE_PERIOD_KEY)
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)
        token = cipher.encrypt(yesterday.isoformat().encode("utf-8"))
        (mock_data_dir / "validity.token").write_bytes(token)
        
        assert license_updater.check_grace_period() is True

    def test_grace_period_expired(self, mock_data_dir, mock_time):
        """Test periodo di grazia scaduto (>3 giorni)."""
        # Crea token vecchio (4 giorni fa)
        cipher = Fernet(GRACE_PERIOD_KEY)
        old_time = datetime.now(timezone.utc) - timedelta(days=4)
        token = cipher.encrypt(old_time.isoformat().encode("utf-8"))
        (mock_data_dir / "validity.token").write_bytes(token)
        
        with pytest.raises(Exception, match="SCADUTO"):
            license_updater.check_grace_period()

    def test_grace_period_clock_manipulation(self, mock_data_dir, mock_time):
        """Test manipolazione orologio (token nel futuro)."""
        # Crea token futuro
        cipher = Fernet(GRACE_PERIOD_KEY)
        future_time = datetime.now(timezone.utc) + timedelta(days=1)
        token = cipher.encrypt(future_time.isoformat().encode("utf-8"))
        (mock_data_dir / "validity.token").write_bytes(token)
        
        with pytest.raises(Exception, match="incoerenza"):
            license_updater.check_grace_period()

    def test_check_emergency_grace_period_activation(self, mock_data_dir, mock_time):
        """Test attivazione primo periodo di grazia di emergenza."""
        # Nessun token esiste
        success, msg, days = license_updater.check_emergency_grace_period()
        
        assert success is True
        assert "attivato" in msg
        assert days == 3
        assert (mock_data_dir / "emergency_grace.token").exists()

    def test_check_emergency_grace_period_existing(self, mock_data_dir, mock_time):
        """Test verifica periodo di emergenza esistente."""
        # Usa il tempo del mock come riferimento
        now = mock_time.return_value[0]
        
        # Crea token (1 giorno fa rispetto al mock)
        cipher = Fernet(GRACE_PERIOD_KEY)
        yesterday = now - timedelta(days=1)
        token = cipher.encrypt(yesterday.isoformat().encode("utf-8"))
        (mock_data_dir / "emergency_grace.token").write_bytes(token)
        
        success, msg, days = license_updater.check_emergency_grace_period()
        assert success is True
        assert "attivo" in msg
        assert days == 2 # 3 - 1 = 2

    def test_check_emergency_grace_period_expired(self, mock_data_dir, mock_time):
        """Test periodo emergenza scaduto."""
        # Crea token vecchio
        cipher = Fernet(GRACE_PERIOD_KEY)
        old = datetime.now(timezone.utc) - timedelta(days=4)
        token = cipher.encrypt(old.isoformat().encode("utf-8"))
        (mock_data_dir / "emergency_grace.token").write_bytes(token)
        
        success, msg, days = license_updater.check_emergency_grace_period()
        assert success is False
        assert "SCADUTO" in msg

    def test_is_license_folder_empty(self, mock_data_dir):
        """Test controllo cartella vuota."""
        assert license_updater.is_license_folder_empty() is True
        
        (mock_data_dir / "config.dat").touch()
        assert license_updater.is_license_folder_empty() is True # Manca manifest
        
        (mock_data_dir / "manifest.json").touch()
        assert license_updater.is_license_folder_empty() is False
