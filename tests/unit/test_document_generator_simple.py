import pytest
from unittest.mock import MagicMock, patch
from src.utils.document_generator import generate_pdf_from_html
from PyQt6.QtGui import QTextDocument

class TestDocumentGeneratorSimple:
    def test_generate_pdf_from_html(self, qapp):
        # We test the logic without real printing by mocking QPrinter and QTextDocument.print
        with patch("src.utils.document_generator.QPrinter") as mock_printer:
            with patch.object(QTextDocument, "print") as mock_print_method:
                generate_pdf_from_html("<h1>Test</h1>", "test.pdf")
                # Check if print was called
                assert mock_print_method.called
                # Check if printer was configured
                mock_printer.return_value.setOutputFileName.assert_called_with("test.pdf")