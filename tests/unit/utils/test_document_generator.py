from unittest.mock import patch

from src.utils.document_generator import generate_pdf_from_html


class TestDocumentGenerator:
    @patch("src.utils.document_generator.QPrinter")
    @patch("src.utils.document_generator.QTextDocument")
    def test_generate_pdf_from_html_success(self, mock_doc_class, mock_printer_class, fs):
        mock_doc = mock_doc_class.return_value
        mock_printer = mock_printer_class.return_value

        res = generate_pdf_from_html("<h1>Test</h1>", "test.pdf")

        assert res is True
        assert mock_doc.setHtml.called
        assert mock_printer.setOutputFileName.called
        assert mock_doc.print_.called

    @patch("src.utils.document_generator.QTextDocument.setHtml", side_effect=Exception("Render fail"))
    def test_generate_pdf_from_html_failure(self, mock_set, fs):
        res = generate_pdf_from_html("<h1>Fail</h1>", "fail.pdf")
        assert res is False
