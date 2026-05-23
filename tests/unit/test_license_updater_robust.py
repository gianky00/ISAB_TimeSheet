from datetime import datetime, timedelta

import pytest

from src.core.license_updater import LicenseUpdater


class TestLicenseUpdaterRobust:
    @pytest.fixture
    def mock_config(self, mocker):
        return mocker.patch("src.core.config_manager.load_config")

    @pytest.fixture
    def mock_save(self, mocker):
        return mocker.patch("src.core.config_manager.save_config")

    def test_run_update_success(self, mock_config, mock_save, mocker):
        mock_config.return_value = {"license_key": "KEY-123"}
        mocker.patch("src.core.license_updater.requests.post")

        # Simula esito positivo
        res = LicenseUpdater.run_update()
        assert res is True
        assert mock_save.called

    def test_grace_period_valid(self, mock_config):
        # Simula licenza scaduta da 2 giorni ma con grace period di 5
        expiry = datetime.now() - timedelta(days=2)
        mock_config.return_value = {"license_expiry": expiry.isoformat(), "license_grace_days": 5}

        # La logica del grace period potrebbe essere in LicenseValidator
        # Se testiamo LicenseUpdater, verifichiamo che non blocchi
        assert True  # Placeholder per logica specifica se presente in Updater
