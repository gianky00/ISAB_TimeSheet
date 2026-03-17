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

    def export(self, file_path: str) -> tuple[bool, str]:
        """Esporta il TreeWidget in un file PDF con paginazione intelligente."""
        try:
            # Setup PDF Writer
            writer = QPdfWriter(file_path)
            writer.setResolution(300)

            # Setup Page Layout Landscape
            layout = QPageLayout()
            layout.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
            layout.setOrientation(QPageLayout.Orientation.Landscape)
            layout.setMargins(QMarginsF(0, 0, 0, 0))
            writer.setPageLayout(layout)

            # Setup Text Document
            doc = QTextDocument()
            paint_rect_pt = layout.paintRectPoints()
            width_pt = paint_rect_pt.width()
            doc.setTextWidth(width_pt)

            pages_html = self._build_paginated_html(doc, width_pt, paint_rect_pt.height())
            if not pages_html:
                return False, "Nessun dato da esportare."

            # Printing with Page Numbering
            painter = QPainter(writer)
            dpi = writer.resolution()

            # Mapping coordinate logiche (punti) su area fisica (pixel)
            painter.setViewport(layout.paintRectPixels(dpi))
            painter.setWindow(0, 0, int(width_pt), int(paint_rect_pt.height()))

            total_pages = len(pages_html)

            for page_idx, page_html in enumerate(pages_html):
                if page_idx > 0:
                    writer.newPage()

                doc.setHtml(page_html)

                painter.save()
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
        # setPixelSize garantisce la dimensione esatta indipendentemente dalla scalatura
        font.setPixelSize(8)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.darkGray)

        page_text = f"Pagina {current} / {total}"
        footer_rect = QRectF(0, height - 20, width - 15, 20)
        painter.drawText(footer_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, page_text)
        painter.restore()

    def _build_paginated_html(self, doc: QTextDocument, width_pt: float, height_pt: float) -> list[str]:
        """Costruisce i blocchi HTML divisi per pagina calcolandone l'altezza dinamicamente."""
        now_str = datetime.now().strftime("%d/%m/%Y alle %H:%M:%S")
        title = "Lista Strumenti Campione Secondari<br>assegnati al cantiere ISAB SUD"
        meta_info = f"Generato il: {now_str} dal software Syncrojob v{__version__}"

        style_html = """
        <html>
        <head>
        <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 7pt; color: #1e293b; margin: 10px; margin-bottom: 0px; }
        h1 { color: #1e3a8a; text-align: center; margin-top: 5px; margin-bottom: 5px; font-size: 8pt; font-weight: bold; }
        .timestamp { text-align: right; color: #64748b; font-size: 7pt; margin-bottom: 5px; margin-right: 5px; }
        table { width: 100%; border-collapse: collapse; }
        th { background-color: #f8fafc; color: #0f172a; font-weight: bold; padding: 6px 8px; border-bottom: 1.5pt solid #cbd5e1; text-align: left; font-size: 6pt; }
        td { padding: 5px 8px; font-size: 6pt; vertical-align: middle; word-wrap: break-word; }
        .historical-row td { color: #64748b; border-top: none; }
        .parent-yes td { background-color: #dcfce7; color: #0f172a; font-weight: bold; border-top: 1pt solid #94a3b8; }
        .parent-no td { background-color: #fee2e2; color: #0f172a; font-weight: bold; border-top: 1pt solid #94a3b8; }
        .status-yes { color: #15803d; font-weight: bold; text-align: center; }
        .status-no { color: #b91c1c; font-weight: bold; text-align: center; }
        .text-center { text-align: center; }
        .col-stato { font-weight: bold; font-size: 6pt; }
        </style>
        </head>
        <body>
        """

        page_header_html = f"""
        <div class='timestamp'>{meta_info}</div>
        <h1>{title}</h1>
        <table>
        <thead>
        <tr>
        <th style='width: 9%;' class='text-center'>ID</th>
        <th style='width: 10%;'>Certificato</th>
        <th style='width: 14%;'>Modello / Tipo</th>
        <th style='width: 9%;'>Costruttore</th>
        <th style='width: 8%;'>Matricola</th>
        <th style='width: 7%;'>Range Strumento</th>
        <th style='width: 4%;' class='text-center'>Err %</th>
        <th style='width: 8%;'>Emissione</th>
        <th style='width: 8%;'>Scadenza</th>
        <th style='width: 8%;'>Stato</th>
        <th style='width: 7%;'>Ubicazione</th>
        <th style='width: 8%;'>Annotazioni</th>
        <th style='width: 4%;' class='text-center'>UTILIZZATO</th>
        </tr>
        </thead>
        <tbody>
        """

        page_footer_html = "</tbody></table></body></html>"

        footer_height_pt = 30
        content_height_limit = height_pt - footer_height_pt

        pages_html: list[str] = []
        current_blocks: list[str] = []

        groups_data = []
        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            if not parent or parent.isHidden():
                continue

            is_excluded = "[ESCLUSO]" in parent.text(0).upper()
            if is_excluded and not self.show_excluded:
                continue

            group_html_blocks = []

            for j in range(parent.childCount()):
                child = parent.child(j)
                if not child:
                    continue

                is_current = j == 0
                scadenza_str = child.text(8)
                days, _ = CertificatiEngine.calculate_days_and_status(scadenza_str)

                is_valid = days is not None and days != -9999 and days >= 0
                utilizzato = "SI" if (is_current and is_valid) else "NO"

                if is_current:
                    stato_display = CertificatiEngine.format_days_text_short(days)
                    for emoji in ("✅", "🔴", "🟠", "🟡", "❌"):
                        stato_display = stato_display.replace(emoji, "")
                    stato_display = stato_display.strip()

                    # Add line break after Attivo/Scaduto/Scade
                    if " (" in stato_display:
                        stato_display = stato_display.replace(" (", "<br>(")
                    elif " tra " in stato_display:
                        stato_display = stato_display.replace(" tra ", "<br>tra ")
                    elif " oggi" in stato_display:
                        stato_display = stato_display.replace(" oggi", "<br>oggi")

                    row_class = "parent-yes" if utilizzato == "SI" else "parent-no"
                else:
                    stato_display = "STORICO"
                    row_class = "historical-row"

                # Fix Modello/Tipo formatting
                modello = child.text(2).strip()
                if " " in modello:
                    parts = modello.split(" ", 1)
                    modello = f"{parts[0]}<br>{parts[1]}"

                row_html = f"<tr class='{row_class}'>"

                if is_current:
                    row_html += f"<td class='text-center'>{child.text(0)}</td>"
                    row_html += f"<td>{child.text(1)}</td>"
                    row_html += f"<td>{modello}</td>"
                    row_html += f"<td>{child.text(3)}</td>"
                    row_html += f"<td>{child.text(4)}</td>"
                    row_html += f"<td>{child.text(5)}</td>"
                    row_html += f"<td class='text-center'>{child.text(6)}</td>"
                    row_html += f"<td>{child.text(7)}</td>"
                    row_html += f"<td>{child.text(8)}</td>"
                    row_html += f"<td class='col-stato'>{stato_display}</td>"
                    row_html += f"<td>{child.text(10)}</td>"
                    row_html += f"<td>{child.text(11)}</td>"
                    status_class = "status-yes" if utilizzato == "SI" else "status-no"
                    row_html += f"<td class='{status_class}'>{utilizzato}</td>"
                else:
                    row_html += "<td></td>"
                    row_html += f"<td>&raquo; {child.text(1)}</td>"
                    row_html += "<td></td>"
                    row_html += "<td></td>"
                    row_html += "<td></td>"
                    row_html += "<td></td>"
                    row_html += "<td></td>"
                    row_html += f"<td>{child.text(7)}</td>"
                    row_html += f"<td>{child.text(8)}</td>"
                    row_html += f"<td class='col-stato'>{stato_display}</td>"
                    row_html += "<td></td>"
                    row_html += "<td></td>"
                    row_html += "<td></td>"

                row_html += "</tr>"
                group_html_blocks.append(row_html)

            groups_data.append(group_html_blocks)

        def check_height(blocks: list[str]) -> float:
            doc.setHtml(style_html + page_header_html + "".join(blocks) + page_footer_html)
            return doc.size().height()

        for group_blocks in groups_data:
            if check_height(current_blocks + group_blocks) <= content_height_limit:
                current_blocks.extend(group_blocks)
            else:
                if not current_blocks:
                    # Anche da solo questo gruppo sfora. Proviamo riga per riga.
                    for row in group_blocks:
                        if check_height([*current_blocks, row]) <= content_height_limit:
                            current_blocks.append(row)
                        else:
                            pages_html.append(style_html + page_header_html + "".join(current_blocks) + page_footer_html)
                            current_blocks = [row]
                else:
                    # Inizia una nuova pagina con l'intero gruppo se possibile
                    pages_html.append(style_html + page_header_html + "".join(current_blocks) + page_footer_html)
                    current_blocks = []

                    if check_height(group_blocks) <= content_height_limit:
                        current_blocks = group_blocks
                    else:
                        for row in group_blocks:
                            if check_height([*current_blocks, row]) <= content_height_limit:
                                current_blocks.append(row)
                            else:
                                pages_html.append(style_html + page_header_html + "".join(current_blocks) + page_footer_html)
                                current_blocks = [row]

        if current_blocks:
            pages_html.append(style_html + page_header_html + "".join(current_blocks) + page_footer_html)

        return pages_html
