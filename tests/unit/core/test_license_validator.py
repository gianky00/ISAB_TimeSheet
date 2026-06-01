import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import patch

import pytest
from cryptography.fernet import Fernet

from src.core.license_validator import (
    LicenseStatus,
    _calculate_sha256,
    _check_and_migrate_local_license,
    get_detailed_license_status,
    get_license_client,
    get_license_expiry,
    verify_license,
)


class TestLicenseValidator:
    @pytest.fixture(autouse=True)
    def setup_license_env(self, fs):
        self.data_dir = Path("/data")
        self.license_dir = self.data_dir / "Licenza"
        fs.create_dir(str(self.license_dir))

        self.config_path = self.license_dir / "config.dat"
        self.manifest_path = self.license_dir / "manifest.json"

        # Genera chiave per il test
        self.test_key = Fernet.generate_key()
        self.cipher = Fernet(self.test_key)

        with patch("src.core.license_validator.get_data_path", return_value=str(self.data_dir)):
            with patch("src.core.secrets_manager.SecretsManager.get_license_key", return_value=self.test_key):
                yield

    def _create_valid_license(self, hwid="HWID_TEST", expiry="01/01/2050"):
        payload = {"Cliente": "TestClient", "Scadenza Licenza": expiry, "Hardware ID": hwid}
        encrypted = self.cipher.encrypt(json.dumps(payload).encode("utf-8"))
        self.config_path.write_bytes(encrypted)

        hash_val = _calculate_sha256(str(self.config_path))
        self.manifest_path.write_text(json.dumps({"config.dat": hash_val}))

    def test_calculate_sha256(self, fs):
        fs.create_file("/test.bin", contents="testdata")
        # SHA256 di "testdata" = 810ff...
        h = _calculate_sha256("/test.bin")
        assert len(h) == 64

    def test_check_and_migrate_local_license(self, fs):
        # Simula licenza in AppData vecchi
        old_dir = Path("/appdata/BotTS/Licenza")
        fs.create_dir(str(old_dir))
        fs.create_file(str(old_dir / "config.dat"), contents="DAT")
        fs.create_file(str(old_dir / "manifest.json"), contents="MAN")

        with patch("os.environ.get", return_value="/appdata"):
            paths = {"dir": self.license_dir, "config": self.config_path, "manifest": self.manifest_path}
            res = _check_and_migrate_local_license(paths)
            assert res is True
            assert self.config_path.exists()
            assert self.manifest_path.exists()

    @patch("src.core.license_validator.get_hardware_id", return_value="HWID_TEST")
    @patch("src.core.license_validator.get_trusted_time")
    def test_get_detailed_license_status_valid(self, mock_time, mock_hwid):
        mock_time.return_value = (datetime.now(UTC), True)
        self._create_valid_license()

        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.VALID
        assert "TestClient" in msg

    def test_get_detailed_license_status_missing(self):
        status, _msg = get_detailed_license_status()
        assert status == LicenseStatus.MISSING

    @patch("src.core.license_validator.get_hardware_id", return_value="HWID_TEST")
    @patch("src.core.license_validator.get_trusted_time")
    def test_get_detailed_license_status_expired(self, mock_time, mock_hwid):
        # Data nel passato
        past_date = datetime.now(UTC) - timedelta(days=10)
        expiry_str = f"{past_date.day:02d}/{past_date.month:02d}/{past_date.year}"

        mock_time.return_value = (datetime.now(UTC), True)
        self._create_valid_license(expiry=expiry_str)

        status, _msg = get_detailed_license_status()
        assert status == LicenseStatus.EXPIRED

    @patch("src.core.license_validator.get_hardware_id", return_value="HWID_DIFFERENT")
    @patch("src.core.license_validator.get_trusted_time")
    def test_get_detailed_license_status_hwid_mismatch(self, mock_time, mock_hwid):
        mock_time.return_value = (datetime.now(UTC), True)
        self._create_valid_license(hwid="HWID_EXPECTED")

        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.INVALID
        assert "Hardware ID" in msg

    @patch("src.core.license_validator.get_hardware_id", return_value="HWID_TEST")
    def test_get_detailed_license_status_corrupted_hash(self, mock_hwid):
        self._create_valid_license()
        # Modifica il file config.dat senza aggiornare il manifest
        self.config_path.write_bytes(b"CORRUPTED")

        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.INVALID
        assert "Integrità" in msg

    def test_verify_license_wrapper(self):
        with patch("src.core.license_validator.get_detailed_license_status") as mock_det:
            mock_det.return_value = (LicenseStatus.VALID, "OK")
            assert verify_license() == (True, "OK")

            mock_det.return_value = (LicenseStatus.EXPIRED, "NO")
            assert verify_license() == (False, "NO")

    def test_get_license_info_and_accessors(self):
        self._create_valid_license()

        assert get_license_client() == "TestClient"
        assert get_license_expiry() == "01/01/2050"

        # Test file missing
        self.config_path.unlink()
        assert get_license_client() == "N/D"
        assert get_license_expiry() == "N/D"
