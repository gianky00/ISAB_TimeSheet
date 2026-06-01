from unittest.mock import MagicMock, patch

import pytest

from src.core.exceptions import LicenseError
from src.core.initialization.license_verifier import LicenseVerifier
from src.core.license_validator import LicenseStatus


class TestLicenseVerifier:
    @patch("src.core.initialization.license_verifier.get_detailed_license_status")
    @patch("src.core.initialization.license_verifier.get_hardware_id")
    @patch("src.core.initialization.license_verifier.run_update")
    def test_verify_license_valid(self, mock_update, mock_hwid, mock_status):
        mock_status.return_value = (LicenseStatus.VALID, "OK")
        step = MagicMock()

        LicenseVerifier.verify_license(step)
        assert mock_hwid.called
        assert mock_status.called
        assert step.call_count == 3

    @patch("src.core.initialization.license_verifier.get_detailed_license_status")
    @patch("src.core.initialization.license_verifier.get_hardware_id")
    @patch("src.core.initialization.license_verifier.run_update")
    def test_verify_license_invalid(self, mock_update, mock_hwid, mock_status):
        mock_status.return_value = (LicenseStatus.INVALID, "Wrong HWID")
        step = MagicMock()

        with pytest.raises(LicenseError, match="Licenza non valida: Wrong HWID"):
            LicenseVerifier.verify_license(step)

    @patch("src.core.initialization.license_verifier.run_update")
    @patch("src.core.initialization.license_verifier.LicenseVerifier._trigger_revocation_shutdown")
    def test_async_handshake_revocation(self, mock_shutdown, mock_update):
        # Testiamo la logica interna di _async_handshake
        mock_update.side_effect = Exception("REVOCATA")

        # Non possiamo testare facilmente il thread asincrono direttamente da verify_license
        # ma possiamo invocare la logica che verrebbe eseguita nel thread

        # Recuperiamo la funzione definita localmente in verify_license? No, meglio
        # rifattorizzare o patchare threading.Thread per eseguire subito

        with patch("threading.Thread") as mock_thread:
            # Eseguiamo verify_license per far spawnare il thread
            with patch(
                "src.core.initialization.license_verifier.get_detailed_license_status",
                return_value=(LicenseStatus.VALID, ""),
            ):
                LicenseVerifier.verify_license(MagicMock())

            # Recuperiamo il target del thread (la funzione _async_handshake)
            target_func = mock_thread.call_args[1]["target"]
            target_func()  # Eseguiamo manualmente la logica del thread

            assert mock_shutdown.called

    @patch("src.core.initialization.license_verifier.run_update")
    @patch("src.core.initialization.license_verifier.logger")
    def test_async_handshake_generic_error(self, mock_logger, mock_update):
        mock_update.side_effect = Exception("Network timeout")

        with patch("threading.Thread") as mock_thread:
            with patch(
                "src.core.initialization.license_verifier.get_detailed_license_status",
                return_value=(LicenseStatus.VALID, ""),
            ):
                LicenseVerifier.verify_license(MagicMock())

            target_func = mock_thread.call_args[1]["target"]
            target_func()

            assert mock_logger.warning.called

    @patch("src.core.initialization.license_verifier.QApplication")
    @patch("src.core.initialization.license_verifier.QTimer")
    @patch("src.core.initialization.license_verifier.sys.exit")
    def test_trigger_revocation_shutdown(self, mock_exit, mock_timer, mock_qapp):
        mock_qapp.instance.return_value = MagicMock()

        LicenseVerifier._trigger_revocation_shutdown()

        assert mock_timer.singleShot.called
        # La funzione passata a singleShot dovrebbe chiamare sys.exit(1)
        shutdown_func = mock_timer.singleShot.call_args[0][1]

        with patch("src.gui.dialogs.confirmation_dialog.ConfirmationDialog.show_error") as mock_dialog:
            shutdown_func()
            assert mock_dialog.called
            assert mock_exit.called
