import pytest
from unittest.mock import patch, MagicMock
from src.utils.printing import get_installed_printers, print_pdf

class TestPrinting:
    
    @patch('src.utils.printing.win32print')
    def test_get_installed_printers(self, mock_win32print):
        # Setup mock
        mock_win32print.EnumPrinters.return_value = [
            (0, 0, "Printer1", 0),
            (0, 0, "Printer2", 0)
        ]
        
        printers = get_installed_printers()
        assert len(printers) == 2
        assert "Printer1" in printers
        assert "Printer2" in printers
        
        mock_win32print.EnumPrinters.assert_called_with(2) # 2 = PRINTER_ENUM_LOCAL

    @patch('src.utils.printing.win32print')
    def test_get_installed_printers_error(self, mock_win32print):
        mock_win32print.EnumPrinters.side_effect = Exception("Boom")
        printers = get_installed_printers()
        assert printers == []

    @patch('src.utils.printing.os.startfile')
    @patch('src.utils.printing.os.path.exists')
    @patch('src.utils.printing.win32print')
    def test_print_pdf_success(self, mock_win32print, mock_exists, mock_startfile):
        mock_exists.return_value = True
        mock_win32print.GetDefaultPrinter.return_value = "DefaultPrinter"
        
        result = print_pdf("C:\\dummy.pdf", "TargetPrinter")
        
        assert result is True
        mock_win32print.SetDefaultPrinter.assert_any_call("TargetPrinter")
        mock_startfile.assert_called_with("C:\\dummy.pdf", "print")
        # Ensure it switches back
        mock_win32print.SetDefaultPrinter.assert_called_with("DefaultPrinter")

    @patch('src.utils.printing.os.path.exists')
    def test_print_pdf_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        assert print_pdf("C:\\ghost.pdf", "Printer") is False
