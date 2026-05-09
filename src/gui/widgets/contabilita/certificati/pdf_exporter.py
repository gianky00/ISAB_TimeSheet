# mypy: disable-error-code="no-untyped-def, no-untyped-call, unused-ignore, arg-type"
"""
SyncroJob - Certificati PDF Exporter
Motore di esportazione specializzato per la generazione di report PDF multipagina.
"""

import os
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from PySide6.QtCore import QMarginsF, Qt
from PySide6.QtGui import QColor, QFont, QPageLayout, QPageSize, QPainter, QPdfWriter, QTextDocument

from src.core.config_manager import get_config_value
from src.gui.styles import COLORS


@dataclass
class PageDimensions:
    """Raggruppa le dimensioni della pagina per il disegno."""

    width: float
    height: float


# Soglie giorni per scadenze (coerenti con certificati_analysis_dialog.py)
THRESHOLD_URGENT = 15
THRESHOLD_ATTENTION = 30


class CertificatiPdfExporter:
    """Motore di esportazione PDF per certificati campione."""

    def __init__(
        self, data: list[dict[str, Any]], include_history: bool = False, print_exclusions: Any = False
    ) -> None:
        self.data = data
        self.include_history = include_history
        self.print_exclusions = print_exclusions
        self._cert_links_cache: dict[str, str] = {}

    def export(self, output_path: str) -> tuple[bool, str]:
        """Esegue l'esportazione completa dei dati in formato PDF."""
        try:
            writer = QPdfWriter(output_path)
            layout = QPageLayout()
            layout.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            layout.setOrientation(QPageLayout.Orientation.Landscape)
            layout.setMargins(QMarginsF(0, 0, 0, 0))
            writer.setPageLayout(layout)

            doc = QTextDocument()
            paint_rect_pt = layout.paintRectPoints()
            width_pt = paint_rect_pt.width()
            doc.setTextWidth(width_pt)

            pages_html = self._build_paginated_html(doc, width_pt, paint_rect_pt.height())
            if not pages_html:
                return False, "Nessun dato da esportare."

            dims = PageDimensions(width=width_pt, height=paint_rect_pt.height())
            return self._run_painter_loop(writer, doc, pages_html, layout, dims)

        except Exception as e:
            return False, f"Errore durante l'esportazione PDF: {e!s}"

    def _run_painter_loop(
        self,
        writer: QPdfWriter,
        doc: QTextDocument,
        pages_html: list[str],
        layout: QPageLayout,
        dims: PageDimensions,
    ) -> tuple[bool, str]:
        """Esegue il ciclo di disegno del PDF."""
        painter = QPainter(writer)
        dpi = writer.resolution()
        painter.setViewport(layout.paintRectPixels(dpi))
        painter.setWindow(0, 0, int(dims.width), int(dims.height))

        total_pages = len(pages_html)
        for page_idx, page_html in enumerate(pages_html):
            if page_idx > 0:
                writer.newPage()

            doc.setHtml(page_html)
            painter.save()
            doc.drawContents(painter)
            painter.restore()

            self._draw_footer(painter, page_idx + 1, total_pages, dims.width, dims.height)

        painter.end()
        return True, "Esportazione PDF completata con successo."

    def _get_certificate_link(self, cert_name: str) -> str:
        """Cerca il file del certificato nella cartella di rete e restituisce l'URI."""
        if not cert_name:
            return ""

        cert_name = cert_name.strip().replace("  ", "-").replace("  ", "-").replace(" ", "")
        if not cert_name or cert_name.upper() in ("N/D", "NESSUNO"):
            return ""

        if cert_name in self._cert_links_cache:
            return self._cert_links_cache[cert_name]

        cert_folder = str(get_config_value("certificates_repo", ""))
        if not cert_folder or not os.path.exists(cert_folder):
            return ""

        # Ricerca ricorsiva limitata per performance
        for root, _, files in os.walk(cert_folder):
            for file in files:
                if file.lower().endswith(".pdf") and cert_name.lower() in file.lower():
                    uri = f"file:///{os.path.join(root, file).replace(os.sep, '/')}"
                    self._cert_links_cache[cert_name] = uri
                    return uri

        return ""

    def _get_year_from_name(self, cert_name: str) -> str:
        """Estrae l'anno dal nome del certificato."""
        min_parts_for_year = 2
        parts = cert_name.split("-")
        if len(parts) >= min_parts_for_year:
            year_part = parts[-1]
            if year_part.isdigit():
                return year_part
        return ""

    def _build_paginated_html(self, doc: QTextDocument, width: float, height: float) -> list[str]:
        """Divide i dati in pagine HTML basandosi sull'altezza disponibile."""
        pages = []
        rows_per_page = 22  # Valore conservativo per layout landscape A4
        data_chunks = [self.data[i : i + rows_per_page] for i in range(0, len(self.data), rows_per_page)]

        for chunk in data_chunks:
            html = self._generate_page_html(chunk)
            pages.append(html)

        return pages

    def _generate_page_html(self, items: list[dict[str, Any]]) -> str:
        """Genera l'HTML per una singola pagina del report."""
        timestamp = datetime.now(UTC).astimezone().strftime("%d/%m/%Y %H:%M")

        rows_html = ""
        for i, item in enumerate(items):
            bg_class = "row-even" if i % 2 == 0 else "row-odd"
            days = item.get("days")
            status_style = ""
            status_text = "N/D"

            if days is not None:
                if days < 0:
                    status_style = f"color: {COLORS['error_red']}; font-weight: bold;"
                    status_text = f"Scaduto da {abs(days)} gg"
                elif days <= THRESHOLD_URGENT:
                    status_style = f"color: {COLORS['warning_orange']}; font-weight: bold;"
                    status_text = f"Scade tra {days} gg"
                elif days <= THRESHOLD_ATTENTION:
                    status_style = f"color: {COLORS['warning_yellow']}; font-weight: bold;"
                    status_text = f"Scade tra {days} gg"
                else:
                    status_style = f"color: {COLORS['success_dark']};"
                    status_text = f"Scade tra {days} gg"

            cert_uri = self._get_certificate_link(item.get("id_strumento", ""))
            cert_id_html = item.get("id_strumento", "N/D")
            if cert_uri:
                cert_id_html = f'<a href="{cert_uri}" style="color: {COLORS["primary_blue"]}; text-decoration: none;">{cert_id_html}</a>'

            rows_html += f"""
            <tr class="{bg_class}">
                <td width="10%">{cert_id_html}</td>
                <td width="15%">{item.get("costruttore", "N/A")}</td>
                <td width="35%">{item.get("modello", "N/A")}</td>
                <td width="20%">{item.get("matricola", "N/A")}</td>
                <td width="20%" align="right" style="{status_style}">{status_text}</td>
            </tr>
            """

        return f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #333; margin: 0; padding: 20px; }}
                .header {{ border-bottom: 2px solid {COLORS["primary_blue"]}; margin-bottom: 20px; padding-bottom: 10px; }}
                .title {{ color: {COLORS["primary_blue"]}; font-size: 20px; font-weight: bold; }}
                .timestamp {{ font-size: 10px; color: #777; float: right; }}
                table {{ width: 100%; border-collapse: collapse; font-size: 10px; }}
                th {{ background-color: {COLORS["bg_alt"]}; color: {COLORS["text_dark"]}; text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }}
                td {{ padding: 8px; border-bottom: 1px solid #eee; }}
                .row-even {{ background-color: #ffffff; }}
                .row-odd {{ background-color: #fcfcfc; }}
                .footer {{ position: fixed; bottom: 0; width: 100%; font-size: 9px; color: #999; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="header">
                <span class="timestamp">Generato il {timestamp}</span>
                <div class="title">SyncroJob - Report Scadenze Certificati</div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>ID-STRUMENTO</th>
                        <th>COSTRUTTORE</th>
                        <th>MODELLO / TIPO</th>
                        <th>MATRICOLA</th>
                        <th align="right">STATO SCADENZA</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </body>
        </html>
        """

    def _draw_footer(
        self, painter: QPainter, page_num: int, total_pages: int, width: float, height: float
    ) -> None:
        """Disegna il footer di pagina con il numero di pagina."""
        painter.save()
        font = QFont("Segoe UI", 8)
        painter.setFont(font)
        painter.setPen(QColor("#999999"))

        footer_text = f"Pagina {page_num} di {total_pages}"
        # Calcola posizione (centrato in basso)
        painter.drawText(0, int(height - 20), int(width), 20, Qt.AlignmentFlag.AlignCenter, footer_text)

        branding = "Generato da SyncroJob"
        painter.drawText(
            30,
            int(height - 20),
            int(width - 60),
            20,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            branding,
        )

        painter.restore()
