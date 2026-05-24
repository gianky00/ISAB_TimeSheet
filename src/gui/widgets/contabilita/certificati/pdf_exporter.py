"""Modulo Pdf Exporter."""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from PySide6.QtCore import QMarginsF, QRectF, Qt
from PySide6.QtGui import QPageLayout, QPageSize, QPainter, QPdfWriter, QTextDocument
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

from src.core.constants import StatoCertificatoLabel, UbicazioneStrumenti
from src.core.contabilita.certificati_engine import CertificatiEngine
from src.core.version import __version__


class CertificatiPdfExporter:
    """Genera report PDF professionale per i certificati campione - Versione Legacy Ripristinata.

    Inizializza la classe.
    """

    def __init__(
        self,
        tree: QTreeWidget,
        show_excluded: bool,
        include_history: bool = True,
        print_exclusions: set[str] | None = None,
    ) -> None:
        self.tree = tree
        self.show_excluded = show_excluded
        self.include_history = include_history
        self.print_exclusions = print_exclusions or set()

    def _get_tree(self) -> Any:
        """Helper per accedere al tree come Any per evitare errori di attributi non definiti su QTreeWidget."""
        return self.tree

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

            pages_html, has_nd = self._build_paginated_html(doc, width_pt, paint_rect_pt.height())
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

                # Footer (Pagina X / Y) con eventuale postilla
                self._draw_footer(painter, page_idx + 1, total_pages, QRectF(paint_rect_pt), has_nd=has_nd)

            painter.end()
        except Exception as e:
            return False, f"Errore durante l'esportazione PDF: {e!s}"
        else:
            return True, "Esportazione PDF completata con successo."

    def _get_certificate_link(self, cert_name: str) -> str:
        """Cerca il file del certificato nella cartella di rete e restituisce l'URI per l'href."""
        if not cert_name:
            return ""

        # Pulizia profonda: strip, normalizzazione trattini e rimozione caratteri invisibili
        cert_name = cert_name.strip().replace("–", "-").replace("—", "-").replace(" ", "")
        if not cert_name or cert_name.upper() in ("N/D", "NESSUNO"):
            return ""

        from src.core.config_manager import get_config_value

        base_path_str = str(
            get_config_value(
                "certificati_root_path",
                r"\\192.168.11.251\Database_Tecnico_SMI\CERTIFICATI CAMPIONE",
            )
        )

        # Tentativo veloce basato sull'anno
        parts = cert_name.split("-")
        year = ""
        min_parts = 2
        short_year_len = 2
        if len(parts) >= min_parts:
            year_part = parts[-1]
            if year_part.isdigit():
                year = f"20{year_part}" if len(year_part) == short_year_len else year_part

        # Lista di possibili percorsi relativi (prioritari)
        possible_rel_paths: list[str] = []
        if year:
            possible_rel_paths.extend(
                (
                    os.path.join(year, f"{cert_name}.pdf"),
                    os.path.join(year, f"{cert_name}.PDF"),
                    os.path.join(year, cert_name, f"{cert_name}.pdf"),
                    os.path.join(year, cert_name, f"{cert_name}.PDF"),
                )
            )

        possible_rel_paths.extend((f"{cert_name}.pdf", f"{cert_name}.PDF"))

        # Verifica fisica dei file
        for rel in possible_rel_paths:
            full_path = os.path.join(base_path_str, rel)
            if Path(full_path).exists():
                return Path(full_path).as_uri()

        return ""

    def _draw_footer(
        self,
        painter: QPainter,
        current: int,
        total: int,
        rect: QRectF,
        *,
        has_nd: bool = False,
    ) -> None:
        """Disegna il footer con la numerazione delle pagine e l'eventuale postilla.

        Args:
          painter: L'oggetto QPainter per il disegno.
          current: Indice della pagina corrente.
          total: Numero totale di pagine.
          rect: Area di disegno della pagina.
          has_nd: Se True, aggiunge la nota per gli strumenti senza data.
        """
        painter.save()
        width = rect.width()
        height = rect.height()
        font = painter.font()
        font.setPixelSize(8)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.darkGray)

        # Postilla Audit (Angolo in basso a sinistra)
        if has_nd:
            disclaimer = (
                "(*) La dicitura 'Senza scadenza' identifica la strumentazione con certificazione "
                "in fase di aggiornamento documentale, attualmente esclusa dall'impiego operativo. "
                "Tutti gli apparati in elenco sono regolarmente tracciati e gestiti in piena "
                "conformità alle procedure di controllo qualità vigenti."
            )
            font.setPixelSize(6)  # Testo piccolo per la postilla
            painter.setFont(font)
            disclaimer_rect = QRectF(15, height - 20, width - 100, 20)
            painter.drawText(
                disclaimer_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, disclaimer
            )

            # Ripristina font per la numerazione
            font.setPixelSize(8)
            painter.setFont(font)

        # Numerazione Pagine (Angolo in basso a destra)
        page_text = f"Pagina {current} / {total}"
        footer_rect = QRectF(0, height - 20, width - 15, 20)
        painter.drawText(footer_rect, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, page_text)
        painter.restore()

    def _build_paginated_html(
        self, doc: QTextDocument, width_pt: float, height_pt: float
    ) -> tuple[list[str], bool]:
        """Costruisce i blocchi HTML divisi per pagina e segnala se ci sono strumenti N/D."""
        all_parents, raw_data_for_stats = self._gather_and_sort_data()
        stats = CertificatiEngine.get_statistics(raw_data_for_stats)
        has_nd = stats.get("senza_data", 0) > 0
        cert_links_cache: dict[str, str] = {}

        def get_cached_cert_link(c_name: str) -> str:
            if c_name not in cert_links_cache:
                cert_links_cache[c_name] = self._get_certificate_link(c_name)
            return cert_links_cache[c_name]

        style_html = self._get_style_html()
        summary_html = self._get_summary_html(stats)
        page_header_html = self._get_page_header_html()
        page_footer_html = "</tbody></table></body></html>"

        available_height = height_pt - 180
        pages_html: list[str] = []
        current_rows: list[str] = []
        current_page_height = 0

        for parent in all_parents:
            group_html_blocks = []
            if parent:
                for j in range(parent.childCount()):
                    if not self.include_history and j > 0:
                        break
                    child = parent.child(j)
                    if not child:
                        continue

                    row_html = self._build_row_html(child, j == 0, get_cached_cert_link)
                    group_html_blocks.append(row_html)

            group_est_height = 35 + (len(group_html_blocks) - 1) * 22
            if current_page_height + group_est_height > available_height and current_rows:
                pages_html.append(
                    style_html + summary_html + page_header_html + "".join(current_rows) + page_footer_html
                )
                current_rows = []
                current_page_height = 0

            current_rows.extend(group_html_blocks)
            current_page_height += group_est_height

        if current_rows:
            pages_html.append(
                style_html + summary_html + page_header_html + "".join(current_rows) + page_footer_html
            )

        return pages_html, has_nd

    def _gather_and_sort_data(self) -> tuple[list[QTreeWidgetItem], list[tuple[str, ...]]]:
        """Raccoglie e ordina i dati dal TreeWidget."""
        all_parents = []
        raw_data_for_stats = []

        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            if parent is None or self._should_skip_parent(parent):
                continue

            all_parents.append(parent)
            if parent.childCount() > 0:
                child = parent.child(0)
                if child:
                    row_tuple = tuple(child.text(col) for col in range(self.tree.columnCount()))
                    raw_data_for_stats.append(row_tuple)

        all_parents.sort(key=self._get_sort_key)
        return all_parents, raw_data_for_stats

    def _should_skip_parent(self, parent: QTreeWidgetItem) -> bool:
        """Determina se un nodo padre deve essere saltato."""
        if parent.isHidden():
            return True

        label_text = parent.text(0)
        data_user = parent.data(0, Qt.ItemDataRole.UserRole)
        matricola = data_user.get("matricola", "") if isinstance(data_user, dict) else ""

        if not matricola and parent.childCount() > 0:
            child_0 = parent.child(0)
            if child_0:
                matricola = child_0.text(4)

        if "[ESCLUSO]" in label_text.upper() and not self.show_excluded:
            return True

        return bool(matricola in self.print_exclusions)

    def _get_sort_key(self, parent: QTreeWidgetItem) -> list[Any]:
        """Restituisce la chiave di ordinamento naturale basata su ID COEMI."""
        id_coemi = ""
        if parent.childCount() > 0:
            child = parent.child(0)
            if child:
                id_coemi = child.text(0)

        parts = re.split(r"(\d+)", id_coemi)
        return [(True, int(c)) if c.isdigit() else (False, c.lower()) for c in parts if c]

    def _build_row_html(self, child: QTreeWidgetItem, is_current: bool, get_link_fn: Any) -> str:
        """Costruisce l'HTML per una singola riga (corrente o storica)."""
        tree_any = self._get_tree()
        scadenza_str = child.text(tree_any.IDX_SCADENZA)
        days, _ = CertificatiEngine.calculate_days_and_status(scadenza_str)

        if is_current:
            stato_display = self._format_status_display(days)
            row_class = self._get_status_row_class(days)
        else:
            stato_display = "STORICO"
            row_class = "historical-row"

        modello = self._format_modello(child.text(tree_any.IDX_MODELLO))
        ubicazione = self._format_ubicazione(child.text(tree_any.IDX_UBICAZIONE))

        cert_name = child.text(tree_any.IDX_CERTIFICATO)
        cert_link = get_link_fn(cert_name)
        cert_display = (
            f"<a href='{cert_link}' style='color: #2563eb; text-decoration: underline;'>{cert_name}</a>"
            if cert_link
            else cert_name
        )
        storico_display = (
            f"&raquo; <a href='{cert_link}' style='color: #64748b; text-decoration: underline;'>{cert_name}</a>"
            if cert_link
            else f"&raquo; {cert_name}"
        )

        row_html = f"<tr class='{row_class}'>"
        if is_current:
            row_html += f"<td class='text-center'>{child.text(tree_any.IDX_ID_STRUMENTO)}</td>"
            row_html += f"<td>{cert_display}</td>"
            row_html += f"<td>{modello}</td>"
            row_html += f"<td>{child.text(tree_any.IDX_COSTRUTTORE)}</td>"
            row_html += f"<td>{child.text(tree_any.IDX_MATRICOLA)}</td>"
            row_html += f"<td>{child.text(tree_any.IDX_RANGE)}</td>"
            row_html += f"<td class='text-center col-err'>{child.text(tree_any.IDX_ERRORE)}</td>"
            row_html += f"<td>{child.text(tree_any.IDX_EMISSIONE)}</td>"
            row_html += f"<td>{child.text(tree_any.IDX_SCADENZA)}</td>"
            row_html += f"<td class='col-stato'>{stato_display}</td>"
            row_html += f"<td>{ubicazione}</td>"
            row_html += f"<td>{child.text(tree_any.IDX_ANNOTAZIONI)}</td>"
        else:
            row_html += "<td></td>"
            row_html += f"<td>{storico_display}</td>"
            row_html += "<td></td>"
            row_html += "<td></td>"
            row_html += "<td></td>"
            row_html += "<td></td>"
            row_html += "<td></td>"
            row_html += f"<td>{child.text(tree_any.IDX_EMISSIONE)}</td>"
            row_html += f"<td>{child.text(tree_any.IDX_SCADENZA)}</td>"
            row_html += f"<td class='col-stato'>{stato_display}</td>"
            row_html += "<td></td>"
            row_html += "<td></td>"

        row_html += "</tr>"
        return row_html

    def _format_status_display(self, days: int | None) -> str:
        """Formatta il testo dello stato per la visualizzazione PDF."""
        stato_display = CertificatiEngine.format_days_text_short(days)
        for emoji in ("[OK]", "[ROSSO]", "[ARANCIONE]", "[GIALLO]", "[ERRORE]"):
            stato_display = stato_display.replace(emoji, "")
        stato_display = stato_display.strip()

        if stato_display.startswith(StatoCertificatoLabel.SCADUTO):
            return stato_display.replace(f"{StatoCertificatoLabel.SCADUTO} (", "Scaduto da<br>").replace(
                "gg fa)", " giorni"
            )
        if stato_display.startswith(StatoCertificatoLabel.ATTIVO):
            return stato_display.replace(f"{StatoCertificatoLabel.ATTIVO} (", "Attivo per<br>").replace(
                "gg rim.)", " giorni"
            )
        if stato_display.startswith(StatoCertificatoLabel.IN_SCADENZA):
            return stato_display.replace(f"{StatoCertificatoLabel.IN_SCADENZA} (", "In scadenza<br>").replace(
                "gg)", " giorni<br>rimanenti"
            )
        if StatoCertificatoLabel.SENZA_SCADENZA in stato_display:
            return "N/D *"
        return stato_display

    def _get_status_row_class(self, days: int | None) -> str:
        """Determina la classe CSS della riga basandosi sulla scadenza."""
        if days == CertificatiEngine.FAULTY_MARKER:
            return "parent-no"
        if days is None:
            return "parent-nd"
        if days < 0:
            return "parent-no"
        if 0 <= days <= 30:
            return "parent-warning"
        return "parent-yes"

    def _format_modello(self, text: str) -> str:
        """Formatta il modello per andare a capo se necessario."""
        modello = text.strip()
        if " " in modello:
            parts = modello.split(" ", 1)
            return f"{parts[0]}<br>{parts[1]}"
        return modello

    def _format_ubicazione(self, text: str) -> str:
        """Formatta l'ubicazione per andare a capo se necessario."""
        raw = text.strip()
        if UbicazioneStrumenti.TECNICO.value in raw:
            ubicazione = raw.replace(f"{UbicazioneStrumenti.TECNICO.value} ", "ASSEGNATO<br>AL TECNICO<br>")
            if ubicazione == raw:
                ubicazione = raw.replace(UbicazioneStrumenti.TECNICO.value, "ASSEGNATO<br>AL TECNICO")
            return ubicazione
        return raw

    def _get_style_html(self) -> str:
        """Restituisce il blocco CSS per l'HTML del PDF."""
        return """
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

    def _get_summary_html(self, s: dict[str, Any]) -> str:
        """Genera l'HTML del riepilogo statistiche in cima al documento."""
        now_str = datetime.now().strftime("%d/%m/%Y alle %H:%M:%S")
        title = "Lista Strumenti Campione Secondari<br>assegnati al cantiere ISAB SUD"
        meta_info = f"Generato il: {now_str} dal software Syncrojob v{__version__}"

        picco_html = (
            f'<div style="margin-top: 5px; border-top: 0.5pt solid #cbd5e1; padding-top: 3px; color: #b91c1c; font-size: 4.5pt; text-align: left;">⚠️ <b>Picco prossime tarature:</b><br>{s["picco_imminente"]["inizio"]} - {s["picco_imminente"]["fine"]} ({s["picco_imminente"]["count"]} tarature)</div>'
            if s.get("picco_imminente")
            else ""
        )

        return f"""
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
                                                &bull; Entro 30gg: <b>{s["prossime_tarature"]["30"]}</b><br>
                                                &bull; 31-60gg: <b>{s["prossime_tarature"]["60"]}</b><br>
                                                &bull; 61-90gg: <b>{s["prossime_tarature"]["90"]}</b><br>
                                                &bull; Oltre 90gg: <b>{s["prossime_tarature"]["oltre"]}</b>
                                            </div>
                                        </td>
                                        <td style="width: 40%; text-align: center; border: none; border-left: 0.5pt solid #cbd5e1; vertical-align: middle;">
                                            Totale Strumenti<br>
                                            <span style="font-size: 9pt; font-weight: bold;">{s["totale"]}</span>
                                            {picco_html}
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style="vertical-align: top; border-right: 0.5pt solid #cbd5e1;">
                                <span style="color: #15803d;">&#11044;</span> Attivi: <b>{s["attivi"]}</b><br>
                                <span style="color: #d97706;">&#11044;</span> In Scadenza: <b>{s["in_scadenza"]}</b><br>
                                <span style="color: #b91c1c;">&#11044;</span> Scaduti: <b>{s["scaduti"]}</b><br>
                                <span style="color: #64748b;">&#11044;</span> Senza Scadenza *: <b>{s["senza_data"]}</b><br>
                                <span style="color: #000000;">&#11044;</span> Guasti: <b>{s["guasti"]}</b>
                            </td>
                            <td style="vertical-align: top; border-right: 0.5pt solid #cbd5e1;">
                                &#127970; {UbicazioneStrumenti.UFFICIO_STRU.value}: <b>{s["ufficio_stru"]}</b><br>
                                &#128203; {UbicazioneStrumenti.UFFICIO_CC.value}: <b>{s["ufficio_cc"]}</b><br>
                                &#128736; {UbicazioneStrumenti.OFFICINA.value}: <b>{s["officina"]}</b><br>
                                &#127984; {UbicazioneStrumenti.SEDE.value}: <b>{s["sede"]}</b><br>
                                &#128119; {UbicazioneStrumenti.TECNICO.value}: <b>{s["tecnico"]}</b><br>
                                &#10060; {UbicazioneStrumenti.ASSENTE.value}: <b>{s["assenti"]}</b>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
        """

    def _get_page_header_html(self) -> str:
        """Restituisce l'intestazione della tabella per ogni pagina."""
        return """
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
