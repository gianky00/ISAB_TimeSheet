from unittest.mock import MagicMock

import pytest

from src.infrastructure.bots.safework.pdl.bot import SafeWorkPDLBot


class TestSafeWorkPDLIntegration:
    @pytest.fixture(autouse=True)
    def mock_license(self, mocker):
        # Mock globale per evitare InvalidToken in integrazione
        mocker.patch(
            "src.application.services.initialization.license_verifier.LicenseVerifier.verify_license",
            return_value=True,
        )
        mocker.patch(
            "src.infrastructure.bots.base.execution_guard.ExecutionGuard.check_environment",
            return_value=(True, ""),
        )

    def test_full_pdl_flow_simulation(self, mocker):
        # 1. Setup
        mock_driver = MagicMock()
        mocker.patch("selenium.webdriver.Chrome", return_value=mock_driver)

        bot = SafeWorkPDLBot("username", "password", download_path="/tmp/downloads")

        # Mock delle Page Objects interne
        mocker.patch.object(bot, "_login", return_value=True)
        mocker.patch.object(bot, "_esegui_ricerca_pdl", return_value=True)
        mocker.patch.object(bot, "_scarica_parte_prima", return_value="/tmp/p1.pdf")
        mocker.patch.object(bot, "_scarica_parte_seconda", return_value="/tmp/p2.pdf")
        mocker.patch.object(bot, "_unisci_e_stampa", return_value=True)
        mocker.patch.object(bot, "_handle_session_merge")
        mocker.patch.object(bot, "_safe_remove")

        # 2. Esecuzione
        data = [{"numero_pdl": "566360", "merge_all_session": True}]
        success = bot.execute(data)

        # 3. Verifiche
        assert success is True

    def test_pdl_flow_with_search_failure(self, mocker):
        mock_driver = MagicMock()
        mocker.patch("selenium.webdriver.Chrome", return_value=mock_driver)
        bot = SafeWorkPDLBot("u", "p")

        mocker.patch.object(bot, "_login", return_value=True)
        mocker.patch.object(bot, "_esegui_ricerca_pdl", return_value=False)

        success = bot.execute([{"numero_pdl": "999"}])
        assert success is False
