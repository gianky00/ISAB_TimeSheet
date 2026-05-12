from unittest.mock import MagicMock, patch


class TestPrintingUtilities:
    @patch("src.utils.printing.win32print.EnumPrinters")
    def test_get_installed_printers(self, mock_enum):
        mock_enum.return_value = [
            (0, 0, "HP LaserJet", None),
            (0, 0, "Epson WorkForce", None),
        ]

        from src.utils.printing import get_installed_printers

        result = get_installed_printers()

        assert len(result) == 2
        assert "HP LaserJet" in result
        assert "Epson WorkForce" in result

    @patch("src.utils.printing.win32print.EnumPrinters")
    def test_get_installed_printers_error(self, mock_enum):
        mock_enum.side_effect = Exception("API Error")

        from src.utils.printing import get_installed_printers

        result = get_installed_printers()

        assert result == []

    @patch("src.utils.printing.subprocess.run")
    def test_run_powershell(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="Success")

        from src.utils.printing import _run_powershell

        result = _run_powershell("Get-Printer")

        assert result is not None
        mock_run.assert_called_once()

    @patch("src.utils.printing.subprocess.run")
    def test_run_powershell_error(self, mock_run):
        mock_run.side_effect = Exception("PS Error")

        from src.utils.printing import _run_powershell

        result = _run_powershell("Get-Printer")

        assert result is None

    @patch("src.utils.printing._run_powershell")
    def test_set_printer_duplex_powershell(self, mock_ps):
        from src.utils.printing import _set_printer_duplex_powershell

        _set_printer_duplex_powershell("HP LaserJet", "OneSided")

        mock_ps.assert_called_once()
        call_args = mock_ps.call_args[0][0]
        assert "HP LaserJet" in call_args
        assert "OneSided" in call_args

    def test_print_pdf_file_not_exists(self, tmp_path):
        from src.utils.printing import print_pdf

        result = print_pdf(str(tmp_path / "nonexistent.pdf"), "Any Printer")

        assert result is False


class TestPrintPDFWithMocking:
    @patch("src.utils.printing.os.startfile")
    @patch("src.utils.printing.fitz.open")
    @patch("src.utils.printing._set_printer_duplex_powershell")
    @patch("src.utils.printing.win32print.GetDefaultPrinter")
    def test_print_pdf_fallback(self, mock_default, mock_duplex, mock_fitz, mock_startfile, tmp_path):
        # Create dummy PDF file
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"dummy pdf content")

        mock_default.return_value = "Default Printer"
        mock_fitz.side_effect = Exception("Fitz error")
        mock_startfile.return_value = None

        from src.utils.printing import print_pdf

        print_pdf(str(pdf_file), None)

        # Should fall back to os.startfile
        mock_startfile.assert_called()
