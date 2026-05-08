import os
import re
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from typing import Any

from PyQt6.QtCore import QMarginsF, QRectF, Qt
from PyQt6.QtGui import QPageLayout, QPageSize, QPainter, QPdfWriter, QTextDocument
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem

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
        self._cert_links_cache: dict[str, str] = {}

    def export(self, file_path: str) -> tuple[bool, str]:
        """Esporta il TreeWidget in un file PDF con paginazione intelligente."""
        try:
            writer = QPdfWriter(file_path)
            writer.setResolution(300)

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

            return self._run_painter_loop(writer, doc, pages_html, layout, width_pt, paint_rect_pt.height())

        except Exception as e:
            return False, f"Errore durante l'esportazione PDF: {e!s}"

    def _run_painter_loop(
        self,
        writer: QPdfWriter,
        doc: QTextDocument,
        pages_html: list[str],
        layout: QPageLayout,
        width: float,
        height: float,
    ) -> tuple[bool, str]:
        """Esegue il ciclo di disegno del PDF."""
        painter = QPainter(writer)
        dpi = writer.resolution()
        painter.setViewport(layout.paintRectPixels(dpi))
        painter.setWindow(0, 0, int(width), int(height))

        total_pages = len(pages_html)
        for page_idx, page_html in enumerate(pages_html):
            if page_idx > 0:
                writer.newPage()

            doc.setHtml(page_html)
            painter.save()
            doc.drawContents(painter)
            painter.restore()

            self._draw_footer(painter, page_idx + 1, total_pages, width, height)

        painter.end()
        return True, "Esportazione PDF completata con successo."

    def _get_certificate_link(self, cert_name: str) -> str:
        """Cerca il file del certificato nella cartella di rete e restituisce l'URI."""
        if not cert_name:
            return ""

        cert_name = cert_name.strip().replace("–", "-").replace("—", "-").replace(" ", "")
        if not cert_name or cert_name.upper() in ("N/D", "NESSUNO"):
            return ""

        if cert_name in self._cert_links_cache:
            return self._cert_links_cache[cert_name]

        base_path = r"\\192.168.11.251\Database_Tecnico_SMI\CERTIFICATI CAMPIONE"
        year = self._extract_year(cert_name)

        possible_paths = self._get_potential_paths(base_path, cert_name, year)
        for path in possible_paths:
            if Path(path).exists():
                uri = Path(path).as_uri()
                self._cert_links_cache[cert_name] = uri
                return uri

        # Fallback ricorsivo
        uri = self._recursive_search(base_path, cert_name, year)
        self._cert_links_cache[cert_name] = uri
        return uri

    def _extract_year(self, cert_name: str) -> str:
        """Estrae l'anno dal nome del certificato."""
        parts = cert_name.split("-")
        if len(parts) >= 2:
            year_part = parts[-1]
            if year_part.isdigit():
                return f"20{year_part}" if len(year_part) == 2 else year_part  # noqa: PLR2004
        return ""

    def _get_potential_paths(self, base: str, name: str, year: str) -> list[str]:
        """Ritorna una lista di possibili percorsi per il file."""
        paths = []
        if year:
            paths.extend(
                [
                    os.path.join(base, year, f"{name}.pdf"),
                    os.path.join(base, year, f"{name}.PDF"),
                    os.path.join(base, year, name, f"{name}.pdf"),
                    os.path.join(base, year, name, f"{name}.PDF"),
                ]
            )
        paths.extend([os.path.join(base, f"{name}.pdf"), os.path.join(base, f"{name}.PDF")])
        return paths

    def _recursive_search(self, base: str, name: str, year: str) -> str:
        """Esegue una ricerca ricorsiva limitata."""
        with suppress(Exception):
            search_root = os.path.join(base, year) if year else base
            if Path(search_root).exists():
                target = f"{name}.pdf".lower()
                for root, _, files in os.walk(search_root):
                    for f in files:
                        if f.lower() == target:
                            return Path(os.path.join(root, f)).as_uri()
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

    def _build_paginated_html(self, doc: QTextDocument, width_pt: float, height_pt: float) -> list[str]:
        """Costruisce i blocchi HTML divisi per pagina calcolandone l'altezza dinamicamente."""
        all_parents = self._get_visible_parents()
        raw_data = self._extract_raw_data(all_parents)
        stats = CertificatiEngine.get_statistics(raw_data)

        style = self._get_html_styles()
        summary = self._get_summary_html(stats)
        header = self._get_table_header_html()
        footer = "</tbody></table></body></html>"

        available_height = height_pt - 180
        pages_html: list[str] = []
        current_rows: list[str] = []
        current_page_height = 0

        for parent in all_parents:
            group_rows = self._build_group_html_rows(parent)
            group_est_height = 35 + (len(group_rows) - 1) * 22

            if current_page_height + group_est_height > available_height and current_rows:
                pages_html.append(style + summary + header + "".join(current_rows) + footer)
                current_rows, current_page_height = [], 0

            current_rows.extend(group_rows)
            current_page_height += group_est_height

        if current_rows:
            pages_html.append(style + summary + header + "".join(current_rows) + footer)

        return pages_html

    def _get_visible_parents(self) -> list[QTreeWidgetItem]:
        """Ritorna gli item padre visibili e ordinati."""

        def natural_sort_key(text: str) -> list[Any]:
            parts = re.split(r"(\d+)", text)
            return [(True, int(c)) if c.isdigit() else (False, c.lower()) for c in parts if c]

        def get_id_coemi(p: QTreeWidgetItem) -> str:
            if p.childCount() > 0:
                child = p.child(0)
                if child:
                    return child.text(0)
            return ""

        parents = []
        for i in range(self.tree.topLevelItemCount()):
            p = self.tree.topLevelItem(i)
            if p and not p.isHidden():
                label = p.text(0).upper()
                data = p.data(0, Qt.ItemDataRole.UserRole)
                matricola = data.get("matricola", "") if isinstance(data, dict) else ""

                if "[ESCLUSO]" in label and not self.show_excluded:
                    continue
                if matricola in self.print_exclusions:
                    continue
                parents.append(p)

        parents.sort(key=lambda x: natural_sort_key(get_id_coemi(x)))
        return parents

    def _extract_raw_data(self, parents: list[QTreeWidgetItem]) -> list[tuple[str, ...]]:
        """Estrae i dati grezzi per il calcolo delle statistiche."""
        data = []
        for p in parents:
            if p.childCount() > 0:
                c = p.child(0)
                if c:
                    data.append(tuple(c.text(col) for col in range(12)))
        return data

    def _build_group_html_rows(self, parent: QTreeWidgetItem) -> list[str]:
        """Costruisce le righe HTML per un gruppo (certificato corrente + storico)."""
        rows = []
        for j in range(parent.childCount()):
            if not self.include_history and j > 0:
                break
            child = parent.child(j)
            if child:
                rows.append(self._build_single_row_html(child, is_current=(j == 0)))
        return rows

    def _build_single_row_html(self, child: QTreeWidgetItem, is_current: bool) -> str:
        """Genera l'HTML per una singola riga di certificato."""
        scadenza = child.text(8)
        days, _ = CertificatiEngine.calculate_days_and_status(scadenza)

        if is_current:
            stato_txt = self._format_status_for_pdf(days)
            row_class = self._get_row_class(days)
            modello = self._format_multiline(child.text(2))
            ubicazione = self._format_ubicazione(child.text(10))
            cert_display = self._get_link_html(child.text(1), is_storico=False)

            return f"""<tr class='{row_class}'>
                <td class='text-center'>{child.text(0)}</td>
                <td>{cert_display}</td>
                <td>{modello}</td>
                <td>{child.text(3)}</td>
                <td>{child.text(4)}</td>
                <td>{child.text(5)}</td>
                <td class='text-center col-err'>{child.text(6)}</td>
                <td>{child.text(7)}</td>
                <td>{child.text(8)}</td>
                <td class='col-stato'>{stato_txt}</td>
                <td>{ubicazione}</td>
                <td>{child.text(11)}</td>
            </tr>"""

        # Storico
        row_class = "historical-row"
        storico_display = self._get_link_html(child.text(1), is_storico=True)
        return f"""<tr class='{row_class}'>
            <td></td><td>{storico_display}</td><td></td><td></td><td></td><td></td><td></td>
            <td>{child.text(7)}</td><td>{child.text(8)}</td>
            <td class='col-stato'>STORICO</td><td></td><td></td>
        </tr>"""

    def _format_status_for_pdf(self, days: int | None) -> str:
        """Formatta lo stato per la visualizzazione PDF rimpiazzando emoji."""
        txt = CertificatiEngine.format_days_text_short(days)
        for e in ("[OK]", "[ROSSO]", "[ARANCIONE]", "[GIALLO]", "[ERRORE]"):
            txt = txt.replace(e, "")
        txt = txt.strip()

        if txt.startswith(StatoCertificatoLabel.SCADUTO):
            return txt.replace(f"{StatoCertificatoLabel.SCADUTO} (", "Scaduto da<br>").replace(
                "gg fa)", " gg"
            )
        if txt.startswith(StatoCertificatoLabel.ATTIVO):
            return txt.replace(f"{StatoCertificatoLabel.ATTIVO} (", "Attivo per<br>").replace(
                "gg rim.)", " gg"
            )
        if txt.startswith(StatoCertificatoLabel.IN_SCADENZA):
            return txt.replace(f"{StatoCertificatoLabel.IN_SCADENZA} (", "In scadenza<br>").replace(
                "gg)", " gg"
            )
        return "N/D" if StatoCertificatoLabel.SENZA_SCADENZA in txt else txt

    def _get_row_class(self, days: int | None) -> str:
        """Ritorna la classe CSS basata sui giorni alla scadenza."""
        if days == -9999:  # noqa: PLR2004
            return "parent-no"
        if days is None:
            return "parent-nd"
        if days < 0:
            return "parent-no"
        if days <= 30:  # noqa: PLR2004
            return "parent-warning"
        return "parent-yes"

    def _format_multiline(self, text: str) -> str:
        """Inserisce breakline se necessario."""
        t = text.strip()
        return t.replace(" ", "<br>", 1) if " " in t else t

    def _format_ubicazione(self, text: str) -> str:
        """Formatta l'ubicazione per il PDF."""
        t = text.strip()
        if UbicazioneStrumenti.TECNICO.value in t:
            return t.replace(UbicazioneStrumenti.TECNICO.value, "ASSEGNATO<br>AL TECNICO")
        return t

    def _get_link_html(self, name: str, is_storico: bool) -> str:
        """Ritorna l'HTML per il link al certificato."""
        link = self._get_certificate_link(name)
        if not link:
            return f"&raquo; {name}" if is_storico else name

        color = "#64748b" if is_storico else "#2563eb"
        prefix = "&raquo; " if is_storico else ""
        return f"{prefix}<a href='{link}' style='color: {color}; text-decoration: underline;'>{name}</a>"

    def _get_html_styles(self) -> str:
        """Ritorna il blocco CSS per l'HTML del PDF."""
        return """<html><head><style>
        body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 7pt; color: #1e293b; margin: 10px; }
        h1 { color: #1e3a8a; font-size: 3pt; font-weight: bold; margin: 5px 0; }
        .timestamp { text-align: right; color: #64748b; font-size: 7pt; margin-bottom: 5px; }
        table { border-collapse: collapse; width: 100%; }
        th { background-color: #f8fafc; font-weight: bold; padding: 4px 3px; border-bottom: 1.5pt solid #cbd5e1; text-align: left; font-size: 6pt; }
        td { padding: 4px 3px; font-size: 6pt; vertical-align: middle; }
        .historical-row td { color: #64748b; }
        .parent-yes td { background-color: #dcfce7; border-top: 1pt solid #94a3b8; font-weight: bold; }
        .parent-no td { background-color: #fee2e2; border-top: 1pt solid #94a3b8; font-weight: bold; }
        .parent-warning td { background-color: #fef3c7; border-top: 1pt solid #94a3b8; font-weight: bold; }
        .parent-nd td { background-color: #f1f5f9; border-top: 1pt solid #94a3b8; font-weight: bold; }
        .col-stato { font-weight: bold; }
        .summary-table { border: 0.5pt solid #cbd5e1; background-color: #f8fafc; font-size: 5pt; }
        .summary-title { font-weight: bold; border-bottom: 0.5pt solid #cbd5e1; display: block; }
        .text-center { text-align: center; }
        </style></head><body>"""

    def _get_summary_html(self, s: dict[str, Any]) -> str:
        """Ritorna l'HTML del sommario statistiche."""
        now = datetime.now().strftime("%d/%m/%Y alle %H:%M:%S")
        meta = f"Generato il: {now} dal software Syncrojob v{__version__}"
        title = "Lista Strumenti Campione Secondari<br>assegnati al cantiere ISAB SUD"

        picco_html = ""
        if s.get("picco_imminente"):
            p = s["picco_imminente"]
            picco_html = f"<div style='margin-top:5px; color:#b91c1c; font-size:4.5pt;'>⚠️ <b>Picco tarature:</b><br>{p['inizio']} - {p['fine']} ({p['count']})</div>"

        return f"""
        <div class='timestamp'>{meta}</div>
        <table style="border:none; margin-bottom:8px;"><tr>
            <td style="border:none; width:40%;"><h1 style="font-size:4.5pt;">{title}</h1></td>
            <td style="border:none; width:60%;">
                <table class="summary-table"><tr>
                    <td style="width:25%; border-right:0.5pt solid #cbd5e1;"><div class="summary-title">STATO CERTIFICATI</div>
                        <span style="color:#15803d;">●</span> Attivi: <b>{s["attivi"]}</b><br>
                        <span style="color:#d97706;">●</span> In Scadenza: <b>{s["in_scadenza"]}</b><br>
                        <span style="color:#b91c1c;">●</span> Scaduti: <b>{s["scaduti"]}</b>
                    </td>
                    <td style="width:40%; border-right:0.5pt solid #cbd5e1;"><div class="summary-title">UBICAZIONE</div>
                        🏢 {UbicazioneStrumenti.UFFICIO_STRU.value}: <b>{s["ufficio_stru"]}</b><br>
                        📋 {UbicazioneStrumenti.UFFICIO_CC.value}: <b>{s["ufficio_cc"]}</b><br>
                        🛠️ {UbicazioneStrumenti.OFFICINA.value}: <b>{s["officina"]}</b>
                    </td>
                    <td style="width:35%; text-align:center;">
                        <b>Prossime tarature:</b><br>30gg: <b>{s["prossime_tarature"]["30"]}</b> | 60gg: <b>{s["prossime_tarature"]["60"]}</b><br>
                        Totale Strumenti: <span style="font-size:9pt; font-weight:bold;">{s["totale"]}</span>
                        {picco_html}
                    </td>
                </tr></table>
            </td>
        </tr></table>"""

    def _get_table_header_html(self) -> str:
        """Ritorna l'intestazione della tabella certificati."""
        return """<table width="100%"><thead><tr>
            <th width="6%">ID-COEMI</th><th width="6%">Certificato</th><th width="10%">Modello</th>
            <th width="8%">Costruttore</th><th width="8%">Matricola</th><th width="8%">Range</th>
            <th width="4%">Err %</th><th width="7%">Emissione</th><th width="7%">Scadenza</th>
            <th width="8%">Stato</th><th width="10%">Ubicazione</th><th width="18%">Annotazioni</th>
        </tr></thead><tbody>"""
