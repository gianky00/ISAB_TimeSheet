import re
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
        """Esporta il TreeWidget in un file PDF."""
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
        """Disegna il footer con la numerazione delle pagine e la dicitura ISO."""
        painter.save()
        font = painter.font()
        font.setPixelSize(8)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.darkGray)

        # Footer Sinistra: Dicitura Qualità
        footer_text_left = "Documento generato elettronicamente - Copia non controllata se stampata"
        footer_rect_left = QRectF(15, height - 20, width, 20)
        painter.drawText(footer_rect_left, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, footer_text_left)

        # Footer Destra: Pagina X / Y
        page_text = f"Pagina {current} / {total}"
        footer_rect_right = QRectF(0, height - 20, width - 15, 20)
        painter.drawText(footer_rect_right, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, page_text)
        painter.restore()

    def _build_paginated_html(self, doc: QTextDocument, width_pt: float, height_pt: float) -> list[str]:
        """Costruisce i blocchi HTML divisi per pagina calcolando le altezze."""
        now_str = datetime.now().strftime("%d/%m/%Y alle %H:%M:%S")
        title = "Lista Strumenti Campione Secondari<br>assegnati al cantiere ISAB SUD"
        meta_info = f"Generato il: {now_str} dal software Syncrojob v{__version__}"

        # Natural sort helper
        def natural_sort_key(text: str):
            parts = re.split(r"(\d+)", text)
            return [int(c) if c.isdigit() else c.lower() for c in parts if c]

        all_parents = []
        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            if not parent or parent.isHidden(): continue
            all_parents.append(parent)
        
        all_parents.sort(key=lambda x: natural_sort_key(x.text(0)))

        # Statistiche
        tot_attivi = tot_in_scadenza = tot_da_rinnovare = tot_guasti = 0
        tot_ufficio = tot_officina = tot_campo = tot_strumenti = 0

        for parent in all_parents:
            is_excluded = "[ESCLUSO]" in parent.text(0).upper()
            if is_excluded and not self.show_excluded: continue
            
            tot_strumenti += 1
            if parent.childCount() > 0:
                child = parent.child(0)
                if child:
                    days, _ = CertificatiEngine.calculate_days_and_status(child.text(8))
                    if days == -9999: tot_guasti += 1
                    elif days is None or days < 0: tot_da_rinnovare += 1
                    elif 0 <= days <= 30: tot_in_scadenza += 1
                    else: tot_attivi += 1
                    
                    ubic = child.text(10).upper()
                    if "UFFICIO" in ubic: tot_ufficio += 1
                    elif "OFFICINA" in ubic: tot_officina += 1
                    elif "TECNIC" in ubic: tot_campo += 1

        style_html = """
        <html><head><style>
        body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 7pt; color: #1e293b; margin: 10px; }
        h1 { color: #1e3a8a; text-align: left; margin: 5px 0; font-size: 6.5pt; font-weight: bold; }
        .timestamp { text-align: right; color: #64748b; font-size: 7pt; margin-bottom: 5px; }
        table { border-collapse: collapse; width: 100%; }
        th { background-color: #f8fafc; color: #0f172a; font-weight: bold; padding: 4px 3px; border-bottom: 1.5pt solid #cbd5e1; text-align: left; font-size: 6pt; }
        td { padding: 4px 3px; font-size: 6pt; vertical-align: middle; }
        .historical-row td { color: #64748b; border-top: none; }
        .parent-yes td { background-color: #dcfce7; color: #0f172a; font-weight: bold; border-top: 1pt solid #94a3b8; }
        .parent-no td { background-color: #fee2e2; color: #0f172a; font-weight: bold; border-top: 1pt solid #94a3b8; }
        .parent-warning td { background-color: #fef3c7; color: #0f172a; font-weight: bold; border-top: 1pt solid #94a3b8; }
        .status-yes { color: #15803d; font-weight: bold; text-align: center; }
        .status-no { color: #b91c1c; font-weight: bold; text-align: center; }
        .status-warning { color: #b45309; font-weight: bold; text-align: center; }
        .text-center { text-align: center; }
        .col-err { white-space: nowrap; }
        .summary-table { border: 0.5pt solid #cbd5e1; background-color: #f8fafc; margin-bottom: 8px; }
        .summary-table td { padding: 2px 4px; border: none; font-size: 5.5pt; }
        .summary-title { font-weight: bold; font-size: 5.5pt; border-bottom: 0.5pt solid #cbd5e1; padding-bottom: 2px; margin-bottom: 2px; display: inline-block; width: 100%; }
        </style></head><body>
        """

        summary_html = f"""
        <div class='timestamp'>{meta_info}</div>
        <table style="border: none; margin-bottom: 8px;">
            <tr>
                <td style="border: none; width: 45%;"><h1>{title}</h1></td>
                <td style="border: none; width: 55%;">
                    <table class="summary-table">
                        <tr>
                            <td style="width: 35%; border-right: 0.5pt solid #cbd5e1;">
                                <div class="summary-title">CERTIFICATI</div>
                                <span style="color: #15803d;">&#11044;</span> Attivi: <b>{tot_attivi}</b><br>
                                <span style="color: #d97706;">&#11044;</span> In Scadenza: <b>{tot_in_scadenza}</b><br>
                                <span style="color: #b91c1c;">&#11044;</span> Da rinnovare: <b>{tot_da_rinnovare}</b><br>
                                <span style="color: #000000;">&#11044;</span> Guasti: <b>{tot_guasti}</b>
                            </td>
                            <td style="width: 40%; border-right: 0.5pt solid #cbd5e1;">
                                <div class="summary-title">UBICAZIONE</div>
                                &#127970; Ufficio: <b>{tot_ufficio}</b><br>
                                &#128736; Officina: <b>{tot_officina}</b><br>
                                &#128119; In campo: <b>{tot_campo}</b>
                            </td>
                            <td style="width: 25%; text-align: center;">
                                Totale Strumenti<br><span style="font-size: 9pt; font-weight: bold;">{tot_strumenti}</span>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
        """

        table_start = """<table width="100%"><thead><tr>
        <th width="7%" class='text-center'>ID-COEMI</th>
        <th width="8%">Certificato</th>
        <th width="10%">Modello / Tipo</th>
        <th width="8.5%">Costruttore</th>
        <th width="8.5%">Matricola</th>
        <th width="8.5%">Range Strumento</th>
        <th width="4%" class='text-center col-err'>Err %</th>
        <th width="7%">Emissione</th>
        <th width="7%">Scadenza</th>
        <th width="8%">Stato</th>
        <th width="11%">Ubicazione</th>
        <th width="8%">Annotazioni</th>
        <th width="6%" class='text-center'>Utilizzato</th>
        </tr></thead><tbody>
        """
        table_end = "</tbody></table>"

        # Pre-calcola altezze fisse
        doc.setHtml(style_html + summary_html + table_start + table_end + "</body></html>")
        header_height = doc.size().height()
        
        # Stimiamo altezza riga per evitare setHtml continuo (lentissimo)
        # Una riga standard a 7pt con padding è alta circa 18-22 punti.
        # Usiamo un valore conservativo per forzare il salto pagina prima del disastro.
        available_height = height_pt - header_height - 40 # 40 di margine sicurezza per footer
        
        pages_html = []
        current_rows = []
        current_page_height = 0

        for parent in all_parents:
            is_excluded = "[ESCLUSO]" in parent.text(0).upper()
            if is_excluded and not self.show_excluded: continue

            group_rows = []
            for j in range(parent.childCount()):
                child = parent.child(j)
                if not child: continue
                
                is_current = (j == 0)
                days, _ = CertificatiEngine.calculate_days_and_status(child.text(8))
                is_valid = days is not None and days != -9999 and days >= 0
                utilizzato = "SI" if (is_current and is_valid) else "NO"
                
                if is_current:
                    stato = CertificatiEngine.format_days_text_short(days)
                    for e in ("✅", "🔴", "🟠", "🟡", "❌"): stato = stato.replace(e, "")
                    stato = stato.strip()
                    if stato.startswith("Scaduto ("): stato = stato.replace("Scaduto (", "Scaduto da<br>").replace(")", "")
                    elif stato.startswith("Attivo ("): stato = stato.replace("Attivo (", "Attivo<br>").replace(")", "")
                    elif stato.startswith("Scade tra "): stato = stato.replace("Scade tra ", "In scadenza<br>tra ")
                    row_cls = "parent-warning" if (utilizzato == "SI" and days is not None and 0 <= days <= 30) else ("parent-yes" if utilizzato == "SI" else "parent-no")
                else:
                    stato = "STORICO"
                    row_cls = "historical-row"
                
                mod = child.text(2).strip()
                if " " in mod: parts = mod.split(" ", 1); mod = f"{parts[0]}<br>{parts[1]}"
                
                ub_raw = child.text(10).strip()
                if "ASSEGNATO AL TECNICO" in ub_raw:
                    ub = ub_raw.replace("ASSEGNATO AL TECNICO ", "ASSEGNATO<br>AL TECNICO<br>")
                    if ub == ub_raw: ub = ub_raw.replace("ASSEGNATO AL TECNICO", "ASSEGNATO<br>AL TECNICO")
                else: ub = ub_raw

                r = f"<tr class='{row_cls}'>"
                if is_current:
                    r += f"<td class='text-center'>{child.text(0)}</td><td>{child.text(1)}</td><td>{mod}</td><td>{child.text(3)}</td><td>{child.text(4)}</td><td>{child.text(5)}</td><td class='text-center col-err'>{child.text(6)}</td><td>{child.text(7)}</td><td>{child.text(8)}</td><td class='col-stato'>{stato}</td><td>{ub}</td><td>{child.text(11)}</td><td class='text-center'>{'SI' if utilizzato == 'SI' else 'NO'}</td>"
                else:
                    r += f"<td></td><td>&raquo; {child.text(1)}</td><td></td><td></td><td></td><td></td><td></td><td>{child.text(7)}</td><td>{child.text(8)}</td><td class='col-stato'>{stato}</td><td></td><td></td><td></td>"
                r += "</tr>"
                group_rows.append(r)

            # Stima altezza gruppo: 22pt per riga padre, 18pt per riga storico
            group_est_height = 25 + (len(group_rows) - 1) * 18
            
            if current_page_height + group_est_height > available_height and current_rows:
                pages_html.append(style_html + summary_html + table_start + "".join(current_rows) + table_end + "</body></html>")
                current_rows = []
                current_page_height = 0

            current_rows.extend(group_rows)
            current_page_height += group_est_height

        if current_rows:
            pages_html.append(style_html + summary_html + table_start + "".join(current_rows) + table_end + "</body></html>")

        return pages_html
