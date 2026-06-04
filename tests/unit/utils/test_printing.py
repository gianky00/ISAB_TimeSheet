from unittest.mock import MagicMock, patch

from src.infrastructure.utils.printing import (
    _run_powershell,
    _set_printer_duplex_powershell,
    get_installed_printers,
    print_pdf,
)


class TestPrinting:
    @patch("src.infrastructure.utils.printing.win32print.EnumPrinters")
    def test_get_installed_printers(self, mock_enum):
        mock_enum.return_value = [(None, None, "Printer1", None), (None, None, "Printer2", None)]
        res = get_installed_printers()
        assert res == ["Printer1", "Printer2"]

    @patch("src.infrastructure.utils.printing.subprocess.run")
    def test_run_powershell_success(self, mock_run):
        mock_res = MagicMock()
        mock_res.returncode = 0
        mock_run.return_value = mock_res

        res = _run_powershell("Get-Date")
        assert res is not None
        assert mock_run.called

    @patch("src.infrastructure.utils.printing._run_powershell")
    def test_set_printer_duplex_powershell(self, mock_ps):
        res = _set_printer_duplex_powershell("PRN1", "OneSided")
        assert res is True
        assert "Set-PrintConfiguration" in mock_ps.call_args[0][0]

    @patch("src.infrastructure.utils.printing.win32print.GetDefaultPrinter", return_value="DEFAULT")
    @patch("src.infrastructure.utils.printing.fitz.open")
    @patch("src.infrastructure.utils.printing.win32ui")
    @patch("src.infrastructure.utils.printing.Image")
    @patch("src.infrastructure.utils.printing.ImageWin")
    def test_print_pdf_success(self, mock_imgwin, mock_img, mock_ui, mock_fitz, mock_def, fs):  # noqa: PLR0913
        fs.create_file("test.pdf", contents=b"pdf")

        # Setup mock doc
        mock_doc = MagicMock()
        mock_doc.__len__.return_value = 1
        mock_page = MagicMock()
        mock_doc.__getitem__.return_value = mock_page
        mock_fitz.return_value = mock_doc

        # Setup mock DC (Device Context)
        mock_hdc = MagicMock()
        mock_ui.CreateDC.return_value = mock_hdc

        res = print_pdf("test.pdf", "PRN1")

        assert res is True
        assert mock_hdc.StartDoc.called
        assert mock_hdc.EndDoc.called

    @patch("src.infrastructure.utils.printing.os.startfile")
    def test_print_pdf_fallback(self, mock_start, fs):
        fs.create_file("test.pdf")
        # Forziamo errore nel blocco principale simulando win32ui None
        with patch("src.infrastructure.utils.printing.win32ui", None):
            res = print_pdf("test.pdf", "PRN1")
            assert res is True
            assert mock_start.called

    def test_print_pdf_not_found(self):
        assert print_pdf("missing.pdf", "PRN1") is False
