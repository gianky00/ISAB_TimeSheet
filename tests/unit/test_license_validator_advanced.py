import base64
import hashlib
import json
from datetime import datetime

import pytest
from cryptography.fernet import Fernet

from src.core.license_validator import (
    LicenseStatus,
    _calculate_sha256,
    get_detailed_license_status,
    get_hardware_id,
)


class TestLicenseValidatorAdvanced:

    @pytest.fixture
    def license_env(self, tmp_path, mocker):
        """Setup ambiente licenza isolato."""
        lic_dir = tmp_path / "Licenza"
        lic_dir.mkdir()
        config_file = lic_dir / "config.dat"
        manifest_file = lic_dir / "manifest.json"

        paths = {
            "dir": str(lic_dir),
            "config": str(config_file),
            "manifest": str(manifest_file)
        }
        mocker.patch("src.core.license_validator._get_license_paths", return_value=paths)

        # Patch os.path.exists per far credere che i file esistano sempre in questo test
        mock_exists = mocker.patch("src.core.license_validator.os.path.exists")
        mock_exists.side_effect = lambda p: str(p) in [str(lic_dir), str(config_file), str(manifest_file)]
        mocker.patch("src.core.license_validator.os.makedirs")

        return lic_dir, config_file, manifest_file

    def test_get_hardware_id_windows_wmic(self, mocker):
        """Test: Recupero HWID su Windows tramite WMIC mockato."""
        mocker.patch("platform.system", return_value="Windows")
        mock_output = b"SerialNumber\nXYZ-123-SERIAL\n"
        mocker.patch("src.core.license_validator.subprocess.check_output", return_value=mock_output)

        hwid = get_hardware_id()
        assert hwid == "XYZ-123-SERIAL"

    def test_calculate_sha256(self, tmp_path):
        """Test: Calcolo hash SHA256 di un file."""
        f = tmp_path / "test.txt"
        f.write_text("SyncroJob2026")
        expected = hashlib.sha256(b"SyncroJob2026").hexdigest()
        assert _calculate_sha256(str(f)) == expected

    def test_license_integrity_failure(self, license_env, mocker):
        """Test: Fallimento validazione se l'hash del file config non corrisponde al manifest."""
        lic_dir, config_file, manifest_file = license_env
        config_file.write_text("tampered data")
        manifest_file.write_text(json.dumps({"config.dat": "wrong_hash"}))
        mocker.patch("src.core.license_validator.AuditManager")

        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.INVALID
        assert "Integrità" in msg

    def test_license_data_validation_flow(self, license_env, mocker):
        """Test: Workflow completo di validazione (Integrity -> Decrypt -> Data)."""
        lic_dir, config_file, manifest_file = license_env

        # 1. Setup Chiave e Fernet
        key = Fernet.generate_key()
        raw_key = base64.urlsafe_b64decode(key)
        mocker.patch("src.core.license_validator.SecretsManager.get_license_key", return_value=raw_key)

        # 2. Prepara Dati Licenza
        payload = {
            "Hardware ID": "MY-HWID",
            "Scadenza Licenza": "31/12/2099",
            "Cliente": "Test Client"
        }
        cipher = Fernet(key)
        encrypted_data = cipher.encrypt(json.dumps(payload).encode())
        config_file.write_bytes(encrypted_data)

        # 3. Prepara Manifest
        conf_hash = hashlib.sha256(encrypted_data).hexdigest()
        manifest_file.write_text(json.dumps({"config.dat": conf_hash}))

        # 4. Mock HWID Corrente e Trusted Time
        mocker.patch("src.core.license_validator.get_hardware_id", return_value="MY-HWID")
        mock_dt = datetime(2026, 1, 1)
        mocker.patch("src.core.license_validator.get_trusted_time", return_value=(mock_dt, True))

        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.VALID

    def test_license_hardware_mismatch(self, license_env, mocker):
        """Test: Fallimento se HWID nella licenza è diverso da quello attuale."""
        lic_dir, config_file, manifest_file = license_env
        payload = {"Hardware ID": "WRONG-ID", "Scadenza Licenza": "31/12/2099"}
        mocker.patch("src.core.license_validator.get_license_info", return_value=payload)
        mocker.patch("src.core.license_validator.get_hardware_id", return_value="ACTUAL-ID")
        mocker.patch("src.core.license_validator._check_integrity_with_manifest", return_value=(LicenseStatus.VALID, ""))
        mocker.patch("src.core.license_validator.AuditManager")

        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.INVALID
        assert "Hardware ID non valido" in msg
