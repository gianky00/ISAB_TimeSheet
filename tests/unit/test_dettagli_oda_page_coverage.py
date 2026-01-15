from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page import (
    DettagliOdAPage,
)


class TestDettagliOdaPageCoverage:
    @pytest.fixture
    def page(self):
        driver = MagicMock()
        return DettagliOdAPage(driver)

    def test_close_all_tabs_logic(self, page):
        """Verifica la logica di chiusura ciclica dei tab."""
        mock_close_btn = MagicMock()
        # Simula 2 tab aperti, poi nessuno
        mock_close_btn.is_displayed.side_effect = [True, True, False]

        with patch.object(page.driver, "find_element", return_value=mock_close_btn):
            page._close_all_tabs()

        # Deve aver tentato di cliccare tramite JS per ogni tab visualizzato
        assert page.driver.execute_script.call_count >= 2

    def test_download_with_crdownload_wait(self, page, mocker):
        """Verifica che il download aspetti la scomparsa dei file temporanei Chrome."""
        source_dir = Path("source")
        dest_dir = Path("dest")

        # Mock per simulare:
        # 1. Bottone trovato
        # 2. Presenza di .crdownload al primo controllo
        # 3. Comparsa del file .xlsx finale al secondo controllo
        mock_iter = mocker.patch("pathlib.Path.iterdir")
        mocker.patch("time.time", side_effect=[100, 101, 102, 103, 104, 105, 200])
        mocker.patch("time.sleep")
        mocker.patch("shutil.move")

        # Mock per Path.exists: deve restituire True per il file finale
        # Usiamo un mock per l'oggetto Path restituito da max()
        mock_file = mocker.MagicMock(spec=Path)
        mock_file.exists.return_value = True
        mock_file.suffix = ".xlsx"
        mock_file.stat.return_value.st_mtime = 1000
        mock_file.name = "file.xlsx"

        mock_iter.side_effect = [
            [],  # files_before
            [mocker.MagicMock(suffix=".crdownload")],  # primo giro loop: in corso
            [mock_file],  # secondo giro loop: finito
            [mock_file],  # terzo giro: conferma
        ]

        # Mock del bottone export
        page.wait = MagicMock()
        page.wait.until.return_value = MagicMock()

        res = page._download(source_dir, dest_dir, "test.xlsx", ("id", "btn"))
        assert res is True

    def test_navigate_to_dettagli_second_row_retry(self, page):
        """Verifica la strategia di robustezza per righe successive alla prima."""
        page.wait = MagicMock()
        # Mock per expand_sidebar_if_collapsed
        with (
            patch.object(page, "expand_sidebar_if_collapsed"),
            patch.object(page, "_wait_for_overlay"),
        ):
            # Simula navigazione per la seconda riga (is_first_row=False)
            page.navigate_to_dettagli(is_first_row=False)

            # Ci aspettiamo 2 click sul menu Report (strategia di attivazione ExtJS)
            # Nota: nel codice ci sono 2 chiamate execute_script per il report_btn
            assert page.driver.execute_script.call_count >= 2

    def test_logout_with_confirmation_flow(self, page):
        """Verifica il flusso completo di logout con popup di conferma."""
        page.wait = MagicMock()
        mock_btn = MagicMock()
        page.wait.until.return_value = mock_btn

        with patch("time.sleep"):
            page.logout()

        # Verifica che abbia tentato di cliccare impostazioni, logout e conferma SI
        assert page.driver.execute_script.call_count >= 3

    def test_expand_sidebar_if_collapsed(self, page):
        """Verifica l'espansione automatica se il menu è nascosto."""
        mock_expand_btn = MagicMock()
        mock_expand_btn.is_displayed.return_value = True

        with (
            patch.object(page.driver, "find_element", return_value=mock_expand_btn),
            patch("time.sleep"),
        ):
            page.expand_sidebar_if_collapsed()

        # Deve aver cliccato il pulsante di espansione
        page.driver.execute_script.assert_called_with(
            "arguments[0].click();", mock_expand_btn
        )
