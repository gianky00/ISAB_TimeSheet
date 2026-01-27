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
        # Usa percorsi assoluti mockati per evitare confusione con resolve()
        source_dir = Path("/fake/source")
        dest_dir = Path("/fake/dest")

        # Mock per simulare:
        # 1. Cartella esiste
        # 2. Presenza di .crdownload al primo controllo
        # 3. Comparsa del file .xlsx finale al secondo controllo
        mocker.patch("pathlib.Path.exists", return_value=True)
        mocker.patch("pathlib.Path.mkdir")
        mocker.patch("pathlib.Path.resolve", return_value=source_dir)
        
        mock_iter = mocker.patch("pathlib.Path.iterdir")
        mocker.patch("time.time", side_effect=range(100, 200))
        mocker.patch("time.sleep")
        mocker.patch("shutil.move")

        # Mock per il file finale
        mock_file = mocker.MagicMock(spec=Path)
        mock_file.suffix = ".xlsx"
        mock_file.name = "test.xlsx"
        mock_file.is_file.return_value = True
        mock_file.stat.return_value.st_mtime = 1500
        mock_file.__str__.return_value = "/fake/source/test.xlsx"
        mock_file.parent = source_dir

        # Configurazione sequenza iterdir
        # 1. files_before in _download
        # 2. any(.crdownload) in _wait_for_download (giro 1)
        # 3. any(.crdownload) in _wait_for_download (giro 2) -> False
        # 4. current in _wait_for_download (giro 2)
        # 5. iterdir in process_oda results count (se usato) o cleanup
        mock_iter.side_effect = [
            [],  # files_before
            [mocker.MagicMock(suffix=".crdownload")],  # Loop 1: ancora in download
            [mock_file],  # Loop 2: any() -> no crdownload
            [mock_file],  # Loop 2: current -> trovato!
            [], # eventuale iterdir extra
        ]

        # Mock del driver e degli elementi UI
        page.wait = MagicMock()
        mock_btn = MagicMock()
        page.wait.until.return_value = mock_btn
        mock_btn.text = "Trovati : 1" # Per il conteggio risultati
        
        page._wait_for_overlay = MagicMock()

        # Evita loop in _close_all_tabs
        mock_close_btn = MagicMock()
        mock_close_btn.is_displayed.return_value = False
        with patch.object(page.driver, "find_element", return_value=mock_close_btn):
            res = page.process_oda(
                "123", "C1", "01.01.2024", "01.01.2025", source_dir, dest_dir
            )

        assert res is not None
        assert res.name == "dettaglio_oda_123.xlsx"


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
