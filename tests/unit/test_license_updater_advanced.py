
import os
import pytest
import requests
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from src.core.license_updater import (
    get_github_token, 
    update_grace_timestamp, 
    check_grace_period, 
    check_emergency_grace_period,
    run_update,
    _get_validity_token_path,
    _get_emergency_grace_token_path
)

class TestLicenseUpdaterAdvanced:
    @pytest.fixture
    def mock_license_dir(self, tmp_path):
        """Mock della directory licenza usando un path temporaneo."""
        with patch("src.core.license_updater.get_license_dir", return_value=str(tmp_path)):
            yield tmp_path

    def test_github_token_reconstruction(self):
        """Verifica che il token venga ricostruito correttamente dai codici ASCII."""
        token = get_github_token()
        assert token.startswith("ghp_")
        assert len(token) == 40

    def test_check_grace_period_success(self, mock_license_dir, mocker):
        """Verifica successo periodo di grazia entro i 3 giorni."""
        # Setup: timestamp di 1 giorno fa
        past_time = datetime.now() - timedelta(days=1)
        mocker.patch("src.core.time_manager.get_trusted_time", return_value=(datetime.now(), True))
        
        # Salva timestamp (usa la logica interna di cifratura)
        with patch("src.core.time_manager.get_trusted_time", return_value=(past_time, True)):
            update_grace_timestamp()
            
        # Verifica
        assert check_grace_period() is True

    def test_check_grace_period_expired(self, mock_license_dir, mocker):
        """Verifica fallimento periodo di grazia dopo 3 giorni."""
        # Setup: timestamp di 4 giorni fa
        past_time = datetime.now() - timedelta(days=4)
        mocker.patch("src.core.time_manager.get_trusted_time", return_value=(datetime.now(), True))
        
        with patch("src.core.time_manager.get_trusted_time", return_value=(past_time, True)):
            update_grace_timestamp()
            
        with pytest.raises(Exception, match="SCADUTO"):
            check_grace_period()

    def test_check_grace_period_clock_rollback(self, mock_license_dir, mocker):
        """Verifica blocco in caso di rollback dell'orologio di sistema."""
        # Setup: timestamp di oggi
        now = datetime.now()
        mocker.patch("src.core.time_manager.get_trusted_time", return_value=(now - timedelta(hours=1), True))
        
        with patch("src.core.time_manager.get_trusted_time", return_value=(now, True)):
            update_grace_timestamp()
            
        # Il tempo "fidato" ora è 1 ora indietro rispetto al timestamp salvato
        with pytest.raises(Exception, match="incoerenza orologio"):
            check_grace_period()

    def test_emergency_grace_period_flow(self, mock_license_dir, mocker):
        """Verifica il ciclo di vita del periodo di emergenza."""
        mocker.patch("src.core.time_manager.get_trusted_time", return_value=(datetime.now(), True))
        
        # 1. Creazione
        allowed, msg, days = check_emergency_grace_period()
        assert allowed is True
        assert days == 3
        assert os.path.exists(_get_emergency_grace_token_path())
        
        # 2. Verifica (dopo 1 giorno)
        mocker.patch("src.core.time_manager.get_trusted_time", return_value=(datetime.now() + timedelta(days=1), True))
        allowed, msg, days = check_emergency_grace_period()
        assert allowed is True
        assert days == 2

    def test_run_update_full_success(self, mock_license_dir, mocker):
        """Verifica aggiornamento completo con successo da GitHub."""
        mocker.patch("src.core.license_validator.get_hardware_id", return_value="FAKE-HWID")
        
        mock_resp_ok = MagicMock()
        mock_resp_ok.status_code = 200
        mock_resp_ok.content = b"fake-content"
        
        with patch("requests.get", return_value=mock_resp_ok):
            success = run_update()
            
        assert success is True
        assert os.path.exists(os.path.join(mock_license_dir, "config.dat"))
        assert os.path.exists(os.path.join(mock_license_dir, "manifest.json"))

    def test_run_update_partial_404(self, mock_license_dir, mocker):
        """Verifica che un 404 su un file interrompa l'aggiornamento."""
        mocker.patch("src.core.license_validator.get_hardware_id", return_value="FAKE-HWID")
        
        def mock_get(url, **kwargs):
            resp = MagicMock()
            if "manifest.json" in url:
                resp.status_code = 404
            else:
                resp.status_code = 200
                resp.content = b"data"
            return resp
            
        with patch("requests.get", side_effect=mock_get):
            success = run_update()
            
        assert success is False
        # Non dovrebbero essere stati scritti i file se incompleto
        assert not os.path.exists(os.path.join(mock_license_dir, "config.dat"))

    def test_run_update_network_error(self, mock_license_dir, mocker):
        """Verifica gestione errore di rete (timeout)."""
        mocker.patch("src.core.license_validator.get_hardware_id", return_value="FAKE-HWID")
        
        with patch("requests.get", side_effect=requests.exceptions.Timeout("Timeout")):
            success = run_update()
            
        assert success is False
        assert "Offline" in mocker.patch("builtins.print").call_args_list[-2][0][0]
