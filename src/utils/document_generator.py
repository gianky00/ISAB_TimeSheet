"""
Generatore di documenti PDF da HTML.
"""

from PyQt6.QtGui import QPageLayout, QPageSize, QTextDocument
from PyQt6.QtPrintSupport import QPrinter


def generate_pdf_from_html(html_content: str, output_path: str, landscape: bool = True):
    """Genera un PDF da contenuto HTML."""
    doc = QTextDocument()

    # Aggiungi stili CSS globali per garantire leggibilità
    header_style = """
    <style>
        body { font-family: Arial, sans-serif; font-size: 18pt; }
        h2 { font-size: 30pt; color: #333; }
        h3 { font-size: 24pt; color: #0d6efd; margin-top: 20px; }
        p { font-size: 18pt; color: #555; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th { background-color: #f2f2f2; color: #333; font-weight: bold; padding: 12px; font-size: 16pt; border: 1px solid #ddd; }
        td { padding: 10px; font-size: 16pt; border: 1px solid #ddd; color: #000; }
    </style>
    """
    doc.setHtml(header_style + html_content)

    printer = QPrinter(QPrinter.PrinterMode.HighResolution)
    printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
    printer.setOutputFileName(output_path)
    printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))

    orientation = QPageLayout.Orientation.Landscape if landscape else QPageLayout.Orientation.Portrait
    printer.setPageOrientation(orientation)

    doc.print(printer)
