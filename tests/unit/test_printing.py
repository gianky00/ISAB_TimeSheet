from unittest.mock import MagicMock

from src.utils.printing import get_installed_printers, print_pdf


class TestPrinting:
    def test_get_installed_printers(self, mocker):
        mock_win32print = mocker.patch("src.utils.printing.win32print")
        mock_win32print.EnumPrinters.return_value = [(0, 0, "Printer1", 0)]
        printers = get_installed_printers()
        assert "Printer1" in printers

    def test_print_pdf_split_jobs(self, mocker):
        mocker.patch("src.utils.printing.Path.exists", return_value=True)
        mock_win32print = mocker.patch("src.utils.printing.win32print")
        mock_win32print.GetDefaultPrinter.return_value = "DefaultPrinter"

        mock_win32ui = mocker.patch("src.utils.printing.win32ui")
        mock_dc = MagicMock()
        mock_win32ui.CreateDC.return_value = mock_dc
        mock_dc.GetDeviceCaps.return_value = 1000

        mock_fitz = mocker.patch("src.utils.printing.fitz")
        mock_doc = MagicMock()
        mock_fitz.open.return_value = mock_doc
        mock_doc.__len__.return_value = 2

        mock_page = MagicMock()
        mock_pix = MagicMock()
        mock_pix.alpha = False
        mock_pix.width = 100
        mock_pix.height = 100
        mock_pix.samples = b"\x00" * 30000
        mock_page.get_pixmap.return_value = mock_pix
        mock_doc.__getitem__.return_value = mock_page

        mocker.patch("src.utils.printing.Image")
        mocker.patch("src.utils.printing.ImageWin")
        mocker.patch("src.utils.printing.time.sleep")
        mocker.patch("src.utils.printing._set_printer_duplex_powershell")

        result = print_pdf("C:/test.pdf", "TargetPrinter")
        assert result is True
        assert mock_win32ui.CreateDC.call_count == 2

    def test_print_pdf_fallback(self, mocker):
        mocker.patch("src.utils.printing.Path.exists", return_value=True)
        mocker.patch(
            "src.utils.printing.win32print.GetDefaultPrinter",
            side_effect=Exception("Fail"),
        )
        mock_startfile = mocker.patch("src.utils.printing.os.startfile", create=True)

        result = print_pdf("C:/test.pdf", "Printer")
        assert result is True
        assert mock_startfile.called
