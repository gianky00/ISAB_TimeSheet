import re
from datetime import datetime

from PyQt6.QtCore import QMarginsF, QRectF, Qt
from PyQt6.QtGui import QPageLayout, QPageSize, QPainter, QPdfWriter, QTextDocument
from PyQt6.QtWidgets import QTreeWidget

from src.core.contabilita.certificati_engine import CertificatiEngine
from src.core.version import __version__


class CertificatiPdfExporter:
    """Genera report PDF professionale per i certificati campione."""

    def __init__(self, tree: QTreeWidget, show_excluded: bool, include_history: bool = True, print_exclusions: set[str] | None = None):
        self.tree = tree
        self.show_excluded = show_excluded
        self.include_history = include_history
        self.print_exclusions = print_exclusions or set()

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
            painter.setWindow(0, 0, width_pt, paint_rect_pt.height())

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

        # Helper per ordinamento naturale (alfanumerico)
        def natural_sort_key(text: str):
            parts = re.split(r"(\d+)", text)
            # Usiamo tuple (is_int, value) per forzare confronti omogenei (bool con bool, int con int, str con str)
            return [(True, int(c)) if c.isdigit() else (False, c.lower()) for c in parts if c]

        # Estraiamo e filtriamo i top level items per il calcolo globale e l'ordinamento
        all_parents = []
        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            if not parent or parent.isHidden():
                continue

            # Parsing matricola dalla label del padre per il check esclusioni
            # La label ha formato: MATRICOLA  •  COSTRUTTORE  •  MODELLO  •  STATO
            label_text = parent.text(0)
            matricola = label_text.split("  •  ")[0].strip()

            is_excluded = "[ESCLUSO]" in label_text.upper()
            if is_excluded and not self.show_excluded:
                continue

            # Filtro Esclusione Stampa
            if matricola in self.print_exclusions:
                continue

            all_parents.append(parent)

        # FIX ORDINAMENTO: Prendiamo l'ID-COEMI dal primo figlio (child 0, col 0)
        def get_id_coemi(p):
            if p.childCount() > 0:
                child = p.child(0)
                if child:
                    return child.text(0)
            return ""

        # Ordinamento GLOBALE per ID-COEMI crescente
        all_parents.sort(key=lambda x: natural_sort_key(get_id_coemi(x)))

        # Calcolo Statistiche
        tot_attivi = 0
        tot_in_scadenza = 0
        tot_da_rinnovare = 0
        tot_guasti = 0
        tot_ufficio = 0
        tot_officina = 0
        tot_campo = 0
        tot_strumenti = 0

        for parent in all_parents:
            tot_strumenti += 1
            if parent.childCount() > 0:
                child = parent.child(0)
                if child is not None:
                    scadenza_str = child.text(8)
                    days, _ = CertificatiEngine.calculate_days_and_status(scadenza_str)

                    if days == -9999:
                        tot_guasti += 1
                    elif days is None or days < 0:
                        tot_da_rinnovare += 1
                    elif 0 <= days <= 30:
                        tot_in_scadenza += 1
                    else:
                        tot_attivi += 1

                    ubicazione = child.text(10).upper()
                    if "UFFICIO" in ubicazione:
                        tot_ufficio += 1
                    elif "OFFICINA" in ubicazione:
                        tot_officina += 1
                    elif "TECNICO" in ubicazione:
                        tot_campo += 1
        style_html = """
        <html>
        <head>
        <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 7pt; color: #1e293b; margin: 10px; margin-bottom: 0px; }
        h1 { color: #1e3a8a; text-align: left; margin-top: 5px; margin-bottom: 5px; font-size: 6.5pt; font-weight: bold; }
        .timestamp { text-align: right; color: #64748b; font-size: 7pt; margin-bottom: 5px; margin-right: 5px; }
        table { border-collapse: collapse; }
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
        .col-stato { font-weight: bold; font-size: 6pt; }
        .col-err { white-space: nowrap; }
        .summary-table { width: 100%; border: 0.5pt solid #cbd5e1; background-color: #f8fafc; font-size: 5pt; }
        .summary-table td { padding: 2px 4px; border: none; font-size: 5.5pt; }
        .summary-title { font-weight: bold; font-size: 5.5pt; border-bottom: 0.5pt solid #cbd5e1; padding-bottom: 2px; margin-bottom: 2px; display: inline-block; width: 100%; }
        </style>
        </head>
        <body>
        """

        summary_html = f"""
        <div class='timestamp'>{meta_info}</div>
        <table width="100%" style="border: none; margin-bottom: 8px;">
            <tr>
                <td style="border: none; vertical-align: middle; width: 45%;">
                    <h1>{title}</h1>
                </td>
                <td style="border: none; vertical-align: top; width: 55%;">
                    <table class="summary-table">
                        <tr>
                            <td style="width: 35%; vertical-align: top; border-right: 0.5pt solid #cbd5e1;">
                                <div class="summary-title">CERTIFICATI</div>
                            </td>
                            <td style="width: 40%; vertical-align: top; border-right: 0.5pt solid #cbd5e1;">
                                <div class="summary-title">UBICAZIONE</div>
                            </td>
                            <td style="width: 25%; vertical-align: middle; text-align: center;" rowspan="2">
                                Totale Strumenti<br>
                                <span style="font-size: 9pt; font-weight: bold;">{tot_strumenti}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="vertical-align: top; border-right: 0.5pt solid #cbd5e1;">
                                <span style="color: #15803d;">&#11044;</span> Attivi: <b>{tot_attivi}</b><br>
                                <span style="color: #d97706;">&#11044;</span> In Scadenza: <b>{tot_in_scadenza}</b><br>
                                <span style="color: #b91c1c;">&#11044;</span> Da rinnovare: <b>{tot_da_rinnovare}</b><br>
                                <span style="color: #000000;">&#11044;</span> Guasti: <b>{tot_guasti}</b>
                            </td>
                            <td style="vertical-align: top; border-right: 0.5pt solid #cbd5e1;">
                                &#127970; Ufficio: <b>{tot_ufficio}</b><br>
                                &#128736; Officina: <b>{tot_officina}</b><br>
                                &#128119; In campo: <b>{tot_campo}</b>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
        """

        page_header_html = """
        <table width="100%">
        <thead>
        <tr>
        <th width="8%" class='text-center'>ID-COEMI</th>
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
        </tr>
        </thead>
        <tbody>
        """

        page_footer_html = "</tbody></table></body></html>"

        # FIX PAGINAZIONE: Riserva molto spazio per header e footer (circa 180pt)
        available_height = height_pt - 180

        pages_html: list[str] = []
        current_rows: list[str] = []
        current_page_height = 0

        for parent in all_parents:
            group_html_blocks = []

            for j in range(parent.childCount()):
                # Se non vogliamo lo storico, esportiamo solo il primo certificato (quello corrente)
                if not self.include_history and j > 0:
                    break

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
                    if stato_display.startswith("Scaduto ("):
                        stato_display = stato_display.replace("Scaduto (", "Scaduto da<br>").replace(")", "")
                    elif stato_display.startswith("Attivo ("):
                        stato_display = stato_display.replace("Attivo (", "Attivo<br>").replace(")", "")
                    elif stato_display.startswith("Scade tra "):
                        stato_display = stato_display.replace("Scade tra ", "In scadenza<br>tra ")

                    if utilizzato == "SI":
                        row_class = "parent-warning" if days is not None and 0 <= days <= 30 else "parent-yes"
                    else:
                        row_class = "parent-no"
                else:
                    stato_display = "STORICO"
                    row_class = "historical-row"

                # Fix Modello/Tipo formatting
                modello = child.text(2).strip()
                if " " in modello:
                    parts = modello.split(" ", 1)
                    modello = f"{parts[0]}<br>{parts[1]}"

                # Fix Ubicazione formatting per evitare ASSEGNAT O AL TECNICO
                ubicazione_raw = child.text(10).strip()
                if "ASSEGNATO AL TECNICO" in ubicazione_raw:
                    # Lo trasformiamo in ASSEGNATO <br> AL TECNICO <br> (NOME)
                    ubicazione = ubicazione_raw.replace("ASSEGNATO AL TECNICO ", "ASSEGNATO<br>AL TECNICO<br>")
                    if ubicazione == ubicazione_raw: # Nessuno spazio dopo
                         ubicazione = ubicazione_raw.replace("ASSEGNATO AL TECNICO", "ASSEGNATO<br>AL TECNICO")
                else:
                    ubicazione = ubicazione_raw

                row_html = f"<tr class='{row_class}'>"

                if is_current:
                    row_html += f"<td class='text-center'>{child.text(0)}</td>"
                    row_html += f"<td>{child.text(1)}</td>"
                    row_html += f"<td>{modello}</td>"
                    row_html += f"<td>{child.text(3)}</td>"
                    row_html += f"<td>{child.text(4)}</td>"
                    row_html += f"<td>{child.text(5)}</td>"
                    row_html += f"<td class='text-center col-err'>{child.text(6)}</td>"
                    row_html += f"<td>{child.text(7)}</td>"
                    row_html += f"<td>{child.text(8)}</td>"
                    row_html += f"<td class='col-stato'>{stato_display}</td>"
                    row_html += f"<td>{ubicazione}</td>"
                    row_html += f"<td>{child.text(11)}</td>"
                    row_html += f"<td class='text-center'>{'SI' if utilizzato == 'SI' else 'NO'}</td>"
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

            # Stima altezza: 35pt per padre, 22pt per figlio (conservativa)
            group_est_height = 35 + (len(group_html_blocks) - 1) * 22

            if current_page_height + group_est_height > available_height and current_rows:
                pages_html.append(style_html + summary_html + page_header_html + "".join(current_rows) + page_footer_html)
                current_rows = []
                current_page_height = 0

            current_rows.extend(group_html_blocks)
            current_page_height += group_est_height

        if current_rows:
            pages_html.append(style_html + summary_html + page_header_html + "".join(current_rows) + page_footer_html)

        return pages_html
