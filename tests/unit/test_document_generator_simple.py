import pytest
from src.utils.document_generator import generate_pdf_from_html
from unittest.mock import MagicMock, patch

class TestDocumentGeneratorSimple:
    def test_generate_pdf_from_html(self, qapp):
        # We test the logic without real printing if possible
        # but since it uses QPrinter, we mock it
        with patch("src.utils.document_generator.QPrinter") as mock_printer:
            mock_p = mock_printer.return_value
            generate_pdf_from_html("<h1>Test</h1>", "test.pdf")
            
            mock_p.setOutputFileName.assert_called_with("test.pdf")
            assert mock_p.setOutputFormat.called
