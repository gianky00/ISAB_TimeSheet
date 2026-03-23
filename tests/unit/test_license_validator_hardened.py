"""
Hardened tests for LicenseValidator.
Verifies hardware ID checks, expiration, and integrity.
"""

import json
from datetime import datetime

import pytest
from cryptography.fernet import Fernet

from src.core.license_validator import (
    LicenseStatus,
    get_detailed_license_status,
)


class TestLicenseValidatorHardened:
    @pytest.fixture
    def license_setup(self, tmp_path, mocker):  # noqa: ANN001
        """Setup base per i file di licenza."""
        license_dir = tmp_path / "Licenza"
        license_dir.mkdir()

        config_path = license_dir / "config.dat"
        manifest_path = license_dir / "manifest.json"

        paths = {"dir": license_dir, "config": config_path, "manifest": manifest_path}

        # Mock paths in validator
        mocker.patch("src.core.license_validator._get_license_paths", return_value=paths)
        # Mock license key
        fake_key = Fernet.generate_key()
        mocker.patch("src.core.secrets_manager.SecretsManager.get_license_key", return_value=fake_key)

        return paths, fake_key

    def _create_license_files(self, paths, key, payload):  # noqa: ANN001, ANN202
        cipher = Fernet(key)
        encrypted = cipher.encrypt(json.dumps(payload).encode())

        paths["config"].write_bytes(encrypted)

        from src.core.license_validator import _calculate_sha256  # noqa: PLC0415

        manifest = {"config.dat": _calculate_sha256(paths["config"])}
        paths["manifest"].write_text(json.dumps(manifest))

    def test_valid_license(self, license_setup, mocker):  # noqa: ANN001
        """Verifica una licenza perfettamente valida."""
        paths, key = license_setup
        payload = {"Hardware ID": "MY-HW-ID", "Scadenza Licenza": "31/12/2099", "Cliente": "Test User"}
        self._create_license_files(paths, key, payload)

        mocker.patch("src.core.license_validator.get_hardware_id", return_value="MY-HW-ID")
        # trusted time in futuro per non scedere
        mocker.patch("src.core.license_validator.get_trusted_time", return_value=(datetime(2026, 1, 1), True))

        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.VALID
        assert "Test User" in msg

    def test_hardware_mismatch(self, license_setup, mocker):  # noqa: ANN001
        """Verifica il blocco se l'hardware ID è diverso."""
        paths, key = license_setup
        payload = {"Hardware ID": "EXPECTED-ID", "Scadenza Licenza": "31/12/2099"}
        self._create_license_files(paths, key, payload)

        mocker.patch("src.core.license_validator.get_hardware_id", return_value="WRONG-ID")
        mocker.patch("src.core.license_validator.get_trusted_time", return_value=(datetime(2026, 1, 1), True))

        # Patch AuditManager to verify logging
        mock_audit = mocker.patch("src.core.audit_manager.AuditManager.instance")

        status, _ = get_detailed_license_status()
        assert status == LicenseStatus.INVALID
        # Deve aver loggato l'azione di violazione
        assert mock_audit.return_value.log_action.called

    def test_expired_license(self, license_setup, mocker):  # noqa: ANN001
        """Verifica il blocco se la licenza è scaduta."""
        paths, key = license_setup
        payload = {"Hardware ID": "ID", "Scadenza Licenza": "01/01/2020"}
        self._create_license_files(paths, key, payload)

        mocker.patch("src.core.license_validator.get_hardware_id", return_value="ID")
        mocker.patch("src.core.license_validator.get_trusted_time", return_value=(datetime(2026, 1, 1), True))

        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.EXPIRED
        assert "SCADUTA" in msg

    def test_manifest_tampering(self, license_setup, mocker):  # noqa: ANN001
        """Verifica il rilevamento di manomissione del file config.dat."""
        paths, key = license_setup
        payload = {"Hardware ID": "ID", "Scadenza Licenza": "31/12/2099"}
        self._create_license_files(paths, key, payload)

        # Manometti config.dat (cambia un byte)
        data = bytearray(paths["config"].read_bytes())
        data[0] ^= 0xFF
        paths["config"].write_bytes(bytes(data))

        status, msg = get_detailed_license_status()
        assert status == LicenseStatus.INVALID
        assert "Integrità" in msg
