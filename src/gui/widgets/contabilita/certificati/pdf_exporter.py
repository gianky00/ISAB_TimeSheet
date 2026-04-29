import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from PyQt6.QtCore import QMarginsF, QRectF, Qt
from PyQt6.QtGui import QPageLayout, QPageSize, QPainter, QPdfWriter, QTextDocument
from PyQt6.QtWidgets import QTreeWidget

from src.core.constants import StatoCertificatoLabel, UbicazioneStrumenti
from src.core.contabilita.certificati_engine import CertificatiEngine
from src.core.version import __version__


class CertificatiPdfExporter:
    """Genera report PDF professionale per i certificati campione."""

    def __init__(  # noqa: ANN204
        self,
        tree: QTreeWidget,
        show_excluded: bool,
        include_history: bool = True,
        print_exclusions: set[str] | None = None,
    ):
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
            return True, "Esportazione PDF completata con successo."  # noqa: TRY300
        except Exception as e:
            return False, f"Errore durante l'esportazione PDF: {e!s}"

    def _get_certificate_link(self, cert_name: str) -> str:
        """
        Cerca il file del certificato nella cartella di rete e restituisce l'URI per l'href.
        Versione ultra-robusta per percorsi UNC e varianti di estensione.
        """
        if not cert_name:
            return ""

        # Pulizia profonda: strip, normalizzazione trattini e rimozione caratteri invisibili
        cert_name = cert_name.strip().replace('–', '-').replace('—', '-').replace(' ', '')
        if not cert_name or cert_name.upper() in ("N/D", "NESSUNO"):
            return ""

        base_path_str = r"\\192.168.11.251\Database_Tecnico_SMI\CERTIFICATI CAMPIONE"

        # Tentativo veloce basato sull'anno
        parts = cert_name.split('-')
        year = ""
        min_parts = 2
        short_year_len = 2
        if len(parts) >= min_parts:
            year_part = parts[-1]
            if year_part.isdigit():
                year = f"20{year_part}" if len(year_part) == short_year_len else year_part

        # Lista di possibili percorsi relativi (prioritari)
        possible_rel_paths = []
        if year:
            possible_rel_paths.append(os.path.join(year, f"{cert_name}.pdf"))
            possible_rel_paths.append(os.path.join(year, f"{cert_name}.PDF"))
            possible_rel_paths.append(os.path.join(year, cert_name, f"{cert_name}.pdf"))
            possible_rel_paths.append(os.path.join(year, cert_name, f"{cert_name}.PDF"))

        possible_rel_paths.append(f"{cert_name}.pdf")
        possible_rel_paths.append(f"{cert_name}.PDF")

        # Verifica fisica dei file
        for rel in possible_rel_paths:
            full_path = os.path.join(base_path_str, rel)
            if os.path.exists(full_path):
                return Path(full_path).as_uri()

        # Fallback finale: ricerca ricorsiva limitata se abbiamo l'anno
        try:
            search_root = os.path.join(base_path_str, year) if year else base_path_str
            if os.path.exists(search_root):
                target_file_lower = f"{cert_name}.pdf".lower()
                for root, _, files in os.walk(search_root):
                    for f in files:
                        if f.lower() == target_file_lower:
                            found_path = os.path.join(root, f)
                            return Path(found_path).as_uri()
        except Exception:  # noqa: S110
            pass

        return ""

    def _draw_footer(self, painter: QPainter, current: int, total: int, width: float, height: float) -> None:
        """Disegna il footer con la numerazione delle pagine."""
        painter.save()
        font = painter.font()
        font.setPixelSize(8)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.darkGray)

        page_text = f"Pagina {current} / {total}"
        footer_rect = QRectF(0, height - 20, width - 15, 20)
        painter.drawText(footer_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, page_text)
        painter.restore()

    def _build_paginated_html(self, doc: QTextDocument, width_pt: float, height_pt: float) -> list[str]:  # noqa: PLR0912, PLR0915
        """Costruisce i blocchi HTML divisi per pagina calcolandone l'altezza dinamicamente."""
        now_str = datetime.now().strftime("%d/%m/%Y alle %H:%M:%S")
        title = "Lista Strumenti Campione Secondari<br>assegnati al cantiere ISAB SUD"
        meta_info = f"Generato il: {now_str} dal software Syncrojob v{__version__}"

        def natural_sort_key(text: str) -> list[Any]:
            parts = re.split(r"(\d+)", text)
            return [(True, int(c)) if c.isdigit() else (False, c.lower()) for c in parts if c]

        all_parents = []
        raw_data_for_stats = []

        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            if not parent or parent.isHidden():
                continue

            label_text = parent.text(0)
            data_user = parent.data(0, Qt.ItemDataRole.UserRole)
            matricola = data_user.get("matricola", "") if isinstance(data_user, dict) else ""

            if not matricola and parent.childCount() > 0:
                child_0 = parent.child(0)
                if child_0:
                    matricola = child_0.text(4)
            is_excluded = "[ESCLUSO]" in label_text.upper()
            if is_excluded and not self.show_excluded:
                continue

            if matricola in self.print_exclusions:
                continue

            all_parents.append(parent)

            if parent.childCount() > 0:
                child = parent.child(0)
                if child:
                    row_tuple = tuple(child.text(col) for col in range(12))
                    raw_data_for_stats.append(row_tuple)

        def get_id_coemi(p: Any) -> str:
            if p.childCount() > 0:
                child = p.child(0)
                if child:
                    return str(child.text(0))
            return ""

        all_parents.sort(key=lambda x: natural_sort_key(get_id_coemi(x)))

        s = CertificatiEngine.get_statistics(raw_data_for_stats)
        cert_links_cache: dict[str, str] = {}

        def get_cached_cert_link(c_name: str) -> str:
            if c_name not in cert_links_cache:
                cert_links_cache[c_name] = self._get_certificate_link(c_name)
            return cert_links_cache[c_name]

        style_html = """
        <html>
        <head>
        <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 7pt; color: #1e293b; margin: 10px; margin-bottom: 0px; }
        h1 { color: #1e3a8a; text-align: left; margin-top: 5px; margin-bottom: 5px; font-size: 3.0pt; font-weight: bold; white-space: nowrap; }
        .timestamp { text-align: right; color: #64748b; font-size: 7pt; margin-bottom: 5px; margin-right: 5px; }
        table { border-collapse: collapse; }
        th { background-color: #f8fafc; color: #0f172a; font-weight: bold; padding: 4px 3px; border-bottom: 1.5pt solid #cbd5e1; text-align: left; font-size: 6pt; }
        td { padding: 4px 3px; font-size: 6pt; vertical-align: middle; }
        .historical-row td { color: #64748b; border-top: none; }
        .parent-yes td { background-color: #dcfce7; color: #0f172a; font-weight: bold; border-top: 1pt solid #94a3b8; }
        .parent-no td { background-color: #fee2e2; color: #0f172a; font-weight: bold; border-top: 1pt solid #94a3b8; }
        .parent-warning td { background-color: #fef3c7; color: #0f172a; font-weight: bold; border-top: 1pt solid #94a3b8; }
        .parent-nd td { background-color: #f1f5f9; color: #0f172a; font-weight: bold; border-top: 1pt solid #94a3b8; }
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
                <td style="border: none; vertical-align: middle; width: 40%;">
                    <h1 style="font-size: 4.5pt;">{title}</h1>
                </td>
                <td style="border: none; vertical-align: top; width: 60%;">
                    <table class="summary-table">
                        <tr>
                            <td style="width: 25%; vertical-align: top; border-right: 0.5pt solid #cbd5e1;">
                                <div class="summary-title">STATO CERTIFICATI</div>
                            </td>
                            <td style="width: 40%; vertical-align: top; border-right: 0.5pt solid #cbd5e1;">
                                <div class="summary-title">UBICAZIONE</div>
                            </td>
                            <td style="width: 35%; vertical-align: top; text-align: center;" rowspan="2">
                                <table width="100%" style="border: none;">
                                    <tr>
                                        <td style="width: 60%; text-align: left; border: none; padding-right: 5px;">
                                            <div style="font-size: 5pt;">
                                                <b>Prossime tarature:</b><br>
                                                &bull; Entro 30gg: <b>{s['prossime_tarature']['30']}</b><br>
                                                &bull; 31-60gg: <b>{s['prossime_tarature']['60']}</b><br>
                                                &bull; 61-90gg: <b>{s['prossime_tarature']['90']}</b><br>
                                                &bull; Oltre 90gg: <b>{s['prossime_tarature']['oltre']}</b>
                                            </div>
                                        </td>
                                        <td style="width: 40%; text-align: center; border: none; border-left: 0.5pt solid #cbd5e1; vertical-align: middle;">
                                            Totale Strumenti<br>
                                            <span style="font-size: 9pt; font-weight: bold;">{s['totale']}</span>
                                            {f'<div style="margin-top: 5px; border-top: 0.5pt solid #cbd5e1; padding-top: 3px; color: #b91c1c; font-size: 4.5pt; text-align: left;">⚠️ <b>Picco prossime tarature:</b><br>{s["picco_imminente"]["inizio"]} - {s["picco_imminente"]["fine"]} ({s["picco_imminente"]["count"]} tarature programmate)</div>' if s.get('picco_imminente') else ''}
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style="vertical-align: top; border-right: 0.5pt solid #cbd5e1;">
                                <span style="color: #15803d;">&#11044;</span> Attivi: <b>{s['attivi']}</b><br>
                                <span style="color: #d97706;">&#11044;</span> In Scadenza: <b>{s['in_scadenza']}</b><br>
                                <span style="color: #b91c1c;">&#11044;</span> Scaduti: <b>{s['scaduti']}</b><br>
                                <span style="color: #64748b;">&#11044;</span> Senza Scadenza: <b>{s['senza_data']}</b><br>
                                <span style="color: #000000;">&#11044;</span> Guasti: <b>{s['guasti']}</b>
                            </td>
                            <td style="vertical-align: top; border-right: 0.5pt solid #cbd5e1;">
                                &#127970; {UbicazioneStrumenti.UFFICIO_STRU.value}: <b>{s['ufficio_stru']}</b><br>
                                &#128203; {UbicazioneStrumenti.UFFICIO_CC.value}: <b>{s['ufficio_cc']}</b><br>
                                &#128736; {UbicazioneStrumenti.OFFICINA.value}: <b>{s['officina']}</b><br>
                                &#127984; {UbicazioneStrumenti.SEDE.value}: <b>{s['sede']}</b><br>
                                &#128119; {UbicazioneStrumenti.TECNICO.value}: <b>{s['tecnico']}</b><br>
                                &#10060; {UbicazioneStrumenti.ASSENTE.value}: <b>{s['assenti']}</b>
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
        <th width="6%" class='text-center'>ID-COEMI</th>
        <th width="6%">Certificato</th>
        <th width="10%">Modello / Tipo</th>
        <th width="8%">Costruttore</th>
        <th width="8%">Matricola</th>
        <th width="8%">Range Strumento</th>
        <th width="4%" class='text-center col-err'>Err %</th>
        <th width="7%">Emissione</th>
        <th width="7%">Scadenza</th>
        <th width="8%">Stato</th>
        <th width="10%">Ubicazione</th>
        <th width="18%">Annotazioni</th>
        </tr>
        </thead>
        <tbody>
        """

        page_footer_html = "</tbody></table></body></html>"
        available_height = height_pt - 180
        pages_html: list[str] = []
        current_rows: list[str] = []
        current_page_height = 0

        for parent in all_parents:
            group_html_blocks = []
            for j in range(parent.childCount()):
                if not self.include_history and j > 0:
                    break
                child = parent.child(j)
                if not child:
                    continue

                is_current = j == 0
                scadenza_str = child.text(8)
                days, _ = CertificatiEngine.calculate_days_and_status(scadenza_str)

                if is_current:
                    stato_display = CertificatiEngine.format_days_text_short(days)
                    for emoji in ("[OK]", "[ROSSO]", "[ARANCIONE]", "[GIALLO]", "[ERRORE]"):
                        stato_display = stato_display.replace(emoji, "")
                    stato_display = stato_display.strip()

                    if stato_display.startswith(StatoCertificatoLabel.SCADUTO):
                        stato_display = stato_display.replace(f"{StatoCertificatoLabel.SCADUTO} (", "Scaduto da<br>").replace("gg fa)", " giorni")
                    elif stato_display.startswith(StatoCertificatoLabel.ATTIVO):
                        stato_display = stato_display.replace(f"{StatoCertificatoLabel.ATTIVO} (", "Attivo per<br>").replace("gg rim.)", " giorni")
                    elif stato_display.startswith(StatoCertificatoLabel.IN_SCADENZA):
                        stato_display = stato_display.replace(f"{StatoCertificatoLabel.IN_SCADENZA} (", "In scadenza<br>").replace("gg)", " giorni<br>rimanenti")
                    elif StatoCertificatoLabel.SENZA_SCADENZA in stato_display:
                        stato_display = "N/D"

                    if days == -9999:  # noqa: PLR2004
                        row_class = "parent-no"
                    elif days is None:
                        row_class = "parent-nd"
                    elif days < 0:
                        row_class = "parent-no"
                    elif 0 <= days <= 30:  # noqa: PLR2004
                        row_class = "parent-warning"
                    else:
                        row_class = "parent-yes"
                else:
                    stato_display = "STORICO"
                    row_class = "historical-row"

                modello = child.text(2).strip()
                if " " in modello:
                    parts = modello.split(" ", 1)
                    modello = f"{parts[0]}<br>{parts[1]}"

                ubicazione_raw = child.text(10).strip()
                if UbicazioneStrumenti.TECNICO.value in ubicazione_raw:
                    ubicazione = ubicazione_raw.replace(f"{UbicazioneStrumenti.TECNICO.value} ", "ASSEGNATO<br>AL TECNICO<br>")
                    if ubicazione == ubicazione_raw:
                        ubicazione = ubicazione_raw.replace(UbicazioneStrumenti.TECNICO.value, "ASSEGNATO<br>AL TECNICO")
                else:
                    ubicazione = ubicazione_raw

                row_html = f"<tr class='{row_class}'>"
                cert_name = child.text(1)
                cert_link = get_cached_cert_link(cert_name)

                if cert_link:
                    cert_display = f"<a href='{cert_link}' style='color: #2563eb; text-decoration: underline;'>{cert_name}</a>"
                    storico_display = f"&raquo; <a href='{cert_link}' style='color: #64748b; text-decoration: underline;'>{cert_name}</a>"
                else:
                    cert_display = cert_name
                    storico_display = f"&raquo; {cert_name}"

                if is_current:
                    row_html += f"<td class='text-center'>{child.text(0)}</td>"
                    row_html += f"<td>{cert_display}</td>"
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
                else:
                    row_html += "<td></td>"
                    row_html += f"<td>{storico_display}</td>"
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

                row_html += "</tr>"
                group_html_blocks.append(row_html)

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
