from datetime import datetime

from PyQt6.QtCore import QMarginsF, QRectF, Qt
from PyQt6.QtGui import QPageLayout, QPageSize, QPainter, QPdfWriter, QTextDocument
from PyQt6.QtWidgets import QTreeWidget

from src.core.contabilita.certificati_engine import CertificatiEngine
from src.core.version import __version__


class CertificatiPdfExporter:
    """Genera report PDF professionale per i certificati campione."""

    def __init__(self, tree: QTreeWidget, show_excluded: bool):
        self.tree = tree
        self.show_excluded = show_excluded
        self._html_content = ""

    def export(self, file_path: str) -> tuple[bool, str]:
        """Esporta il TreeWidget in un file PDF con numerazione X/Y."""
        try:
            self._build_html()

            # Setup PDF Writer
            writer = QPdfWriter(file_path)
            writer.setResolution(300)

            # Setup Page Layout Landscape
            layout = QPageLayout()
            layout.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            layout.setOrientation(QPageLayout.Orientation.Landscape)
            layout.setMargins(QMarginsF(10, 10, 10, 10))
            writer.setPageLayout(layout)

            # Setup Text Document
            doc = QTextDocument()
            paint_rect_pt = layout.paintRectPoints()
            width_pt = paint_rect_pt.width()
            doc.setTextWidth(width_pt)
            doc.setHtml(self._html_content)

            # Printing with Page Numbering
            painter = QPainter(writer)
            dpi = writer.resolution()

            # Spazio per il footer (30 punti)
            footer_height_pt = 30
            content_height_pt = paint_rect_pt.height() - footer_height_pt

            doc_height_pt = doc.size().height()
            total_pages = int((doc_height_pt + content_height_pt - 0.1) / content_height_pt)
            if total_pages == 0:
                total_pages = 1

            # Mapping coordinate logiche (punti) su area fisica (pixel)
            painter.setViewport(layout.paintRectPixels(dpi))
            painter.setWindow(0, 0, int(width_pt), int(paint_rect_pt.height()))

            for page_idx in range(total_pages):
                if page_idx > 0:
                    writer.newPage()
                    painter.setViewport(layout.paintRectPixels(dpi))
                    painter.setWindow(0, 0, int(width_pt), int(paint_rect_pt.height()))

                painter.save()
                # Clip area contenuto (in punti)
                painter.setClipRect(QRectF(0, 0, width_pt, content_height_pt))

                # Spostamento per la pagina corrente (in punti)
                scroll_y = page_idx * content_height_pt
                painter.translate(0, -scroll_y)

                # Disegno
                doc.drawContents(painter)
                painter.restore()

                # Footer (Pagina X / Y)
                self._draw_footer(painter, page_idx + 1, total_pages, width_pt, paint_rect_pt.height())

            painter.end()
            return True, "Esportazione PDF completata con successo."
        except Exception as e:
            return False, f"Errore durante l'esportazione PDF: {e!s}"

    def _draw_footer(self, painter: QPainter, current: int, total: int, width: float, height: float):
        """Disegna il footer con la numerazione delle pagine."""
        painter.save()
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.darkGray)

        page_text = f"Pagina {current} / {total}"
        # Footer rect in fondo alla Window (coordinate in punti)
        footer_rect = QRectF(0, height - 25, width, 20)
        painter.drawText(footer_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, page_text)
        painter.restore()

    def _build_html(self) -> None:
        """Costruisce il contenuto HTML per il PDF."""
        now_str = datetime.now().strftime("%d/%m/%Y alle %H:%M:%S")
        title = "Lista Strumenti Campione Secondari assegnati al cantiere ISAB SUD"
        meta_info = f"Generato il: {now_str} dal software Syncrojob v{__version__}"

        html = [
            "<html>",
            "<head>",
            "<style>",
            "body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 8pt; color: #1e293b; margin: 0; }",
            "h1 { color: #1e3a8a; text-align: center; margin-bottom: 2px; font-size: 16pt; }",
            ".timestamp { text-align: center; color: #64748b; font-size: 8pt; margin-bottom: 10px; }",
            "table { width: 100%; border-collapse: collapse; border: 0.5pt solid #94a3b8; table-layout: fixed; }",
            "th { background-color: #f1f5f9; color: #0f172a; font-weight: bold; padding: 6pt 2pt; border: 0.5pt solid #cbd5e1; text-align: left; font-size: 7pt; }",
            "td { padding: 5pt 2pt; border: 1px solid #e2e8f0; font-size: 7pt; vertical-align: middle; word-wrap: break-word; }",
            ".historical-row { background-color: #ffffff; color: #94a3b8; }",
            ".current-row { background-color: #f0fdf4; color: #0f172a; font-weight: bold; }",
            ".status-yes { color: #15803d; font-weight: bold; text-align: center; background-color: #dcfce7; }",
            ".status-no { color: #b91c1c; font-weight: bold; text-align: center; background-color: #fee2e2; }",
            ".text-center { text-align: center; }",
            ".col-stato { font-weight: bold; font-size: 7pt; }",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{title}</h1>",
            f"<div class='timestamp'>{meta_info}</div>",
            "<table>",
            "<thead>",
            "<tr>",
            "<th style='width: 15%;'>Modello / Tipo</th>",
            "<th style='width: 10%;'>Costruttore</th>",
            "<th style='width: 8%;'>Matricola</th>",
            "<th style='width: 8%;'>Range Strumento</th>",
            "<th style='width: 5%;' class='text-center'>Err %</th>",
            "<th style='width: 10%;'>Certificato</th>",
            "<th style='width: 8%;'>Scadenza</th>",
            "<th style='width: 8%;'>Emissione</th>",
            "<th style='width: 5%;' class='text-center'>ID</th>",
            "<th style='width: 10%;'>Stato Scadenza</th>",
            "<th style='width: 5%;'>Annotazioni</th>",
            "<th style='width: 5%;'>Ubic.</th>",
            "<th style='width: 3%;' class='text-center'>UTIL</th>",
            "</tr>",
            "</thead>",
            "<tbody>",
        ]

        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            if not parent or parent.isHidden():
                continue

            is_excluded = "[ESCLUSO]" in parent.text(0).upper()
            if is_excluded and not self.show_excluded:
                continue

            for j in range(parent.childCount()):
                child = parent.child(j)
                if not child:
                    continue

                is_current = j == 0
                row_class = "current-row" if is_current else "historical-row"
                prefix = "" if is_current else "&raquo; "

                html.append(f"<tr class='{row_class}'>")
                html.append(f"<td>{prefix}{child.text(0)}</td>")
                html.extend(f"<td>{child.text(col)}</td>" for col in range(1, 9))

                # Calcolo Stato Scadenza
                scadenza_str = child.text(6)
                days, _ = CertificatiEngine.calculate_days_and_status(scadenza_str)

                if is_current:
                    stato_display = CertificatiEngine.format_days_text_short(days)
                    # Pulizia emoji per PDF Enterprise
                    for emoji in ["✅", "🔴", "🟠", "🟡", "❌"]:
                        stato_display = stato_display.replace(emoji, "")
                    stato_display = stato_display.strip()
                else:
                    stato_display = "STORICO"

                html.append(f"<td class='col-stato'>{stato_display}</td>")
                html.append(f"<td>{child.text(10)}</td>")
                html.append(f"<td>{child.text(11)}</td>")

                # UTILIZZATO
                is_valid = days is not None and days != -9999 and days >= 0
                utilizzato = "SI" if (is_current and is_valid) else "NO"
                status_class = "status-yes" if utilizzato == "SI" else "status-no"
                html.append(f"<td class='{status_class}'>{utilizzato}</td>")
                html.append("</tr>")

        html.append("</tbody></table></body></html>")
        self._html_content = "".join(html)
