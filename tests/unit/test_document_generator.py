from unittest.mock import MagicMock, patch

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
        assert "<style>" in call_args  # Injected CSS

        # Verify printer configuration
        mock_printer.setOutputFormat.assert_called()
        mock_printer.setOutputFileName.assert_called_with("output.pdf")

        # Verify printing call
        mock_doc.print.assert_called_with(mock_printer)

    @patch("src.utils.document_generator.QPrinter")
    @patch("src.utils.document_generator.QTextDocument")
    @patch("src.utils.document_generator.QPageLayout")
    def test_generate_pdf_orientation_portrait(self, mock_layout, mock_doc_class, mock_printer_class):
        mock_printer = MagicMock()
        mock_printer_class.return_value = mock_printer

        generate_pdf_from_html("Test", "out.pdf", landscape=False)

        # Orientation should be portrait (default behavior of the logic)
        # We can't easily assert the enum value if it's mocked, but we can check if setPageOrientation was called
        mock_printer.setPageOrientation.assert_called()

    @patch("src.utils.document_generator.QPrinter")
    @patch("src.utils.document_generator.QTextDocument")
    def test_generate_pdf_injects_styles(self, mock_doc_class, mock_printer_class):
        mock_doc = MagicMock()
        mock_doc_class.return_value = mock_doc

        generate_pdf_from_html("<p>Hello</p>", "styles.pdf")

        html_input = mock_doc.setHtml.call_args[0][0]
        assert "font-family: Arial" in html_input
        assert "color: #0d6efd" in html_input  # Blue h3 style
