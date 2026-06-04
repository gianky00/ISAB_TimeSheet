"""Generatore di documenti PDF da HTML."""

import logging

from PySide6.QtGui import QPageLayout, QPageSize, QTextDocument
from PySide6.QtPrintSupport import QPrinter

from src.gui.styles import COLORS

logger = logging.getLogger(__name__)


def generate_pdf_from_html(html_content: str, output_path: str, landscape: bool = True) -> bool:
    """Genera un PDF da contenuto HTML."""
    try:
        doc = QTextDocument()

        # Aggiungi stili CSS globali per garantire leggibilit  (tematizzati)
        header_style = f"""
    <style>
      body {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 18pt; color: {COLORS["text_dark"]}; }}
      h2 {{ font-size: 30pt; color: {COLORS["text_dark"]}; }}
      h3 {{ font-size: 24pt; color: {COLORS["primary_dark"]}; margin-top: 20px; }}
      p {{ font-size: 18pt; color: {COLORS["text_muted"]}; }}
      table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
      th {{ background-color: {COLORS["bg_alt"]}; color: {COLORS["text_dark"]}; font-weight: bold; padding: 12px; font-size: 16pt; border: 1px solid {COLORS["border_light"]}; }}
      td {{ padding: 10px; font-size: 16pt; border: 1px solid {COLORS["border_light"]}; color: black; }}
    </style>
    """
        doc.setHtml(header_style + html_content)

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(output_path)
        printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))

        orientation = QPageLayout.Orientation.Landscape if landscape else QPageLayout.Orientation.Portrait
        printer.setPageOrientation(orientation)

        doc.print_(printer)
    except Exception:
        logger.exception("Errore generazione PDF")
        return False
    else:
        return True
