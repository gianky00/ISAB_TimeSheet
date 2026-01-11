from pathlib import Path
from unittest.mock import MagicMock, patch

from src.bots.portale_fornitori.dettagli_oda.pages.dettagli_oda_page import (
    DettagliOdAPage,
)


class TestBotPagesDeep:
    def test_dettagli_oda_page_init(self):
        mock_driver = MagicMock()
        page = DettagliOdAPage(mock_driver)
        assert page.driver == mock_driver
        assert page.wait is not None

    def test_dettagli_oda_process_logic(self):
        mock_driver = MagicMock()
        page = DettagliOdAPage(mock_driver)

        # Mock dependencies for process_oda
        with patch.object(page, "_wait_for_overlay"), \
             patch.object(page, "_download", return_value=True) as mock_download, \
             patch.object(page, "_close_all_tabs"):

            # Mock find_element for labels
            mock_label = MagicMock()
            mock_label.text = "Trovati : 10"
            page.wait.until = MagicMock(return_value=mock_label)

            res = page.process_oda("12345", "Contract1", "01.01.2024", "31.12.2024", Path("."), Path("."))
            assert res is True
            mock_download.assert_called()

    @patch("src.bots.portale_fornitori.scarico_ts.pages.scarico_ts_page.WebDriverWait")
    def test_scarico_ts_page_init(self, mock_wait):
        from src.bots.portale_fornitori.scarico_ts.pages.scarico_ts_page import (
            ScaricoTSPage,
        )
        mock_driver = MagicMock()
        page = ScaricoTSPage(mock_driver, MagicMock())
        assert page is not None
