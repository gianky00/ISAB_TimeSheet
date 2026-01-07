from unittest.mock import MagicMock, patch

from src.utils.printing import get_installed_printers, print_pdf


class TestPrinting:

    @patch("src.utils.printing.win32print")
    def test_get_installed_printers(self, mock_win32print):
        mock_win32print.EnumPrinters.return_value = [(0, 0, "Printer1", 0)]
        printers = get_installed_printers()
        assert "Printer1" in printers

    @patch("src.utils.printing.fitz")
    @patch("src.utils.printing.ImageWin")
    @patch("src.utils.printing.Image")
    @patch("src.utils.printing.win32ui")
    @patch("src.utils.printing.win32print")
    @patch("src.utils.printing.subprocess.run")
    @patch("src.utils.printing.os.path.exists")
    @patch("src.utils.printing.time.sleep")
    def test_print_pdf_split_jobs(
        self,
        mock_sleep,
        mock_exists,
        mock_run,
        mock_win32print,
        mock_win32ui,
        mock_image,
        mock_imagewin,
        mock_fitz,
    ):
        mock_exists.return_value = True
        mock_win32print.GetDefaultPrinter.return_value = "DefaultPrinter"

        # Mock DC
        mock_dc = MagicMock()
        mock_win32ui.CreateDC.return_value = mock_dc
        mock_dc.GetDeviceCaps.return_value = 1000

        # Mock Fitz with 2 pages
        mock_doc = MagicMock()
        mock_fitz.open.return_value = mock_doc
        mock_doc.__len__.return_value = 2  # 2 Pages
        mock_page = MagicMock()
        mock_doc.__getitem__.return_value = mock_page

        # Run
        result = print_pdf("C:\\doc.pdf", "TargetPrinter")

        assert result is True

        # Verify CreateDC called twice (once per page)
        assert mock_win32ui.CreateDC.call_count == 2

        # Verify StartDoc called twice
        assert mock_dc.StartDoc.call_count == 2

        # Verify EndDoc called twice
        assert mock_dc.EndDoc.call_count == 2

        # Verify DeleteDC called twice
        assert mock_dc.DeleteDC.call_count == 2

    @patch("src.utils.printing.os.startfile")
    @patch("src.utils.printing.win32print")
    @patch("src.utils.printing.os.path.exists")
    def test_print_pdf_fallback(self, mock_exists, mock_win32print, mock_startfile):
        mock_exists.return_value = True
        # Force error
        mock_win32print.GetDefaultPrinter.side_effect = Exception("Fail")

        result = print_pdf("C:\\doc.pdf", "Printer")

        assert result is True
        mock_startfile.assert_called()
