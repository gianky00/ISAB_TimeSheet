from unittest.mock import MagicMock, patch

from src.gui.styles import COLORS
from src.utils.document_generator import generate_pdf_from_html


class TestDocumentGenerator:
    @patch("src.utils.document_generator.QPrinter")
    @patch("src.utils.document_generator.QTextDocument")
    def test_generate_pdf_from_html(self, mock_doc_class, mock_printer_class):
        mock_doc = MagicMock()
        mock_doc_class.return_value = mock_doc
        mock_printer = MagicMock()
        mock_printer_class.return_value = mock_printer

        generate_pdf_from_html("<h1>Test</h1>", "output.pdf", landscape=True)

        # Verify HTML was set
        mock_doc.setHtml.assert_called()
        call_args = mock_doc.setHtml.call_args[0][0]
        assert "<h1>Test</h1>" in call_args
        assert "<style>" in call_args

        # Verify printer configuration
        mock_printer.setOutputFileName.assert_called_with("output.pdf")
        mock_doc.print_.assert_called_with(mock_printer)

    @patch("src.utils.document_generator.QPrinter")
    @patch("src.utils.document_generator.QTextDocument")
    def test_generate_pdf_orientation_portrait(self, mock_doc_class, mock_printer_class):
        mock_printer = MagicMock()
        mock_printer_class.return_value = mock_printer

        generate_pdf_from_html("Test", "out.pdf", landscape=False)

        # Verifica che sia stata impostata un'orientazione (Portrait è il default se landscape=False)
        mock_printer.setPageOrientation.assert_called()

    @patch("src.utils.document_generator.QPrinter")
    @patch("src.utils.document_generator.QTextDocument")
    def test_generate_pdf_injects_styles(self, mock_doc_class, mock_printer_class):
        mock_doc = MagicMock()
        mock_doc_class.return_value = mock_doc

        generate_pdf_from_html("<p>Hello</p>", "styles.pdf")

        html_input = mock_doc.setHtml.call_args[0][0]
        # Verifichiamo la presenza dei font e colori del Design System V9.0
        assert "Segoe UI" in html_input
        assert COLORS["primary_dark"] in html_input
        assert COLORS["text_muted"] in html_input
