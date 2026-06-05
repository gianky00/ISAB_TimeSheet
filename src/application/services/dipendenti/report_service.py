"""SyncroJob - Report Service.

Servizio CORE per la raccolta dati e generazione report (HTML/Excel).
Indipendente dalla GUI.
"""

import logging
import operator
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd

from src.application.services.constants import REPORT_COLORS as COLORS, THRESHOLD_DAYS
from src.application.services.database import db_manager
from src.application.services.dipendenti.data_helpers import build_timbrature_maps
from src.application.services.report_history import ReportHistory
from src.application.services.version import __version__

logger = logging.getLogger(__name__)


class ReportService:
    """Servizio per la logica di business dei report dipendenti."""

    @staticmethod
    def gather_report_data() -> dict[str, Any]:
        """Raccoglie i dati dei dipendenti e li divide in warning ed expired."""
        query = """
      SELECT id_risorsa, cognome, nome, codice_fiscale, badge, data_assunzione
      FROM dipendenti
      WHERE monitoraggio_attivo = 1 OR monitoraggio_attivo IS NULL
      ORDER BY cognome ASC, nome ASC
    """
        dipendenti = db_manager.execute_query(db_manager.DB_DIPENDENTI, query)

        query_timb = "SELECT cognome, nome, codice_fiscale, data FROM timbrature"
        accessi = db_manager.execute_query(db_manager.DB_TIMBRATURE, query_timb)

        # Nota: build_timbrature_maps  attualmente in gui/utils, andrebbe spostato in core.
        # Per ora lo importiamo mantenendo la funzionalità.
        last_by_cf, last_by_name, normalize = build_timbrature_maps(accessi)

        warning_list = []
        expired_list = []

        for dip in dipendenti:
            id_ris, cog, nom, cf, badge, _ = dip
            cf_norm = normalize(cf or "")
            name_key = (normalize(cog or ""), normalize(nom or ""))

            diff_days_tuple = last_by_cf.get(cf_norm) or last_by_name.get(name_key)
            if diff_days_tuple is None:
                continue

            diff_days, _ = diff_days_tuple
            last_access_date = datetime.now(UTC).astimezone() - timedelta(days=diff_days)
            item = {
                "id": id_ris,
                "cognome": cog,
                "nome": nom,
                "badge": badge or "-",
                "giorni": diff_days,
                "data": last_access_date.strftime("%d/%m/%Y"),
            }

            if THRESHOLD_DAYS["warning"] < diff_days <= THRESHOLD_DAYS["expired"]:
                warning_list.append(item)
            elif diff_days > THRESHOLD_DAYS["expired"]:
                expired_list.append(item)

        warning_list.sort(key=operator.itemgetter("giorni"), reverse=True)
        expired_list.sort(key=operator.itemgetter("giorni"), reverse=True)

        return {
            "warning_list": warning_list,
            "expired_list": expired_list,
            "total_monitored": len(dipendenti),
        }

    @staticmethod
    def _build_summary_section(data: dict[str, Any]) -> tuple[str, str, str]:
        urgenti = len([d for d in data["expired_list"] if d["giorni"] > 60])  # noqa: PLR2004
        tot_attenzione = len(data["warning_list"]) + len(data["expired_list"])

        if urgenti > 0:
            sum_text = f"<strong>ATTENZIONE:</strong> {urgenti} dipendenti richiedono azione <strong>IMMEDIATA</strong> (oltre {THRESHOLD_DAYS['critical']} giorni). Totale da gestire: {tot_attenzione}."
            sum_color, sum_icon = COLORS["error_red"], "⚠️"
        elif len(data["expired_list"]) > 0:
            sum_text = f"<strong>{len(data['expired_list'])}</strong> dipendenti scaduti e <strong>{len(data['warning_list'])}</strong> in scadenza richiedono attenzione."
            sum_color, sum_icon = COLORS["warning_orange"], "  "
        else:
            sum_text = f"<strong>{len(data['warning_list'])}</strong> dipendenti in scadenza da monitorare nei prossimi giorni."
            sum_color, sum_icon = COLORS["primary_dark"], "ℹ️"
        return sum_text, sum_color, sum_icon

    @staticmethod
    def _build_trend_html(data: dict[str, Any]) -> str:
        trend = ReportHistory.calculate_trend(len(data["warning_list"]), len(data["expired_list"]))
        if not trend:
            return ""
        parts = []
        for k, label in (("warning_diff", "in scadenza"), ("expired_diff", "scaduti")):
            diff = trend[k]
            if diff > 0:
                parts.append(f'<span style="color: {COLORS["error_red"]};">+{diff} {label}</span>')
            elif diff < 0:
                parts.append(f'<span style="color: {COLORS["success_dark"]};">{diff} {label}</span>')
        if parts:
            return f'<p style="margin: 8px 0 0 0; padding: 10px 12px; background-color: {COLORS["bg_light"]}; border-radius: 4px; font-size: 12px; color: {COLORS["text_muted"]};">   <strong>Trend:</strong> {" | ".join(parts)} rispetto al {trend["last_date"]}</p>'
        return ""

    @staticmethod
    def build_report_html(data: dict[str, Any]) -> str:
        """Costruisce il template HTML per l'email."""
        current_date = datetime.now(UTC).astimezone().strftime("%d/%m/%Y %H:%M")
        font_family = "'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif"
        header_color = COLORS["primary_dark"]
        border_color = COLORS.get("border_gray", "#dee2e6")

        sum_text, sum_color, sum_icon = ReportService._build_summary_section(data)
        trend_html = ReportService._build_trend_html(data)

        html = f"""
    <html><head><style>
      body {{ font-family: {font_family}; margin: 0; padding: 0; color: #333333; background-color: {COLORS["bg_light"]}; }}
      .container {{ width: auto; max-width: 1500px; margin: 0 auto; background-color: #ffffff; }}
      .summary-table {{ width: auto; min-width: 480px; border-collapse: separate; border-spacing: 8px; margin: 16px auto; }}
      .card {{ background-color: #ffffff; padding: 14px 20px; border: 1px solid {border_color}; border-radius: 6px; text-align: center; width: 160px; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }}
      .card-number {{ font-size: 24px; font-weight: 700; display: block; margin-bottom: 4px; letter-spacing: -0.5px; }}
      .card-label {{ font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; color: {COLORS["text_muted"]}; font-weight: 600; }}
      .data-table {{ width: auto; border-collapse: collapse; margin: 0 0 20px 0; background-color: white; border: 1px solid {border_color}; }}
      .data-table th {{ background-color: #f0f4f8; text-align: left; padding: 5px 10px; border: 1px solid {border_color}; font-size: 12px; color: {COLORS["primary_dark"]}; text-transform: uppercase; font-weight: 600; letter-spacing: 0.3px; }}
      .data-table td {{ padding: 5px 12px; border: 1px solid {border_color}; font-size: 13px; vertical-align: middle; color: #333333; }}
    </style></head>
    <body style="background-color: {COLORS["bg_light"]}; margin: 0; padding: 20px 0;">
      <div class="container" style="border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: {COLORS["primary_dark"]};">
          <tr><td style="padding: 20px 24px; text-align: center;">
            <h2 style="margin: 0; font-weight: 700; font-size: 20px; color: #ffffff;">Report Monitoraggio Accessi in ISAB</h2>
            <p style="margin: 8px 0 0 0; font-size: 13px; color: #f0f4f8;">Generato il {current_date} da SyncroJob v{__version__}</p>
          </td></tr>
        </table>
        <div style="padding: 16px 20px; background-color: #ffffff;">
          <table class="summary-table" style="margin: 0 auto;">
            <tr>
              <td><div class="card" style="border-left: 3px solid {header_color}; text-align: left;"><span class="card-number">{data["total_monitored"]}</span><span class="card-label">Monitorati</span></div></td>
              <td><div class="card" style="border-left: 3px solid {COLORS["warning_orange"]}; text-align: left;"><span class="card-number">{len(data["warning_list"])}</span><span class="card-label">In Scadenza</span></div></td>
              <td><div class="card" style="border-left: 3px solid {COLORS["error_red"]}; text-align: left;"><span class="card-number">{len(data["expired_list"])}</span><span class="card-label">Scaduti</span></div></td>
            </tr>
          </table>
        </div>
        <div style="padding: 0 20px 20px 20px; background-color: #ffffff;">
          <p style="margin: 0 0 8px 0; padding: 12px; background-color: {COLORS["bg_light"]}; border-radius: 6px; color: {sum_color}; font-size: 13px; border-left: 3px solid {sum_color}; font-weight: 500;">
            {sum_icon} {sum_text}</p>
          {trend_html}
    """

        if data["warning_list"]:
            html += f'<h3 style="color: {COLORS["warning_orange"]}; margin: 16px 0 12px 0; padding-left: 12px; border-left: 4px solid {COLORS["warning_orange"]}; font-size: 15px;">⚠️ In Scadenza ({THRESHOLD_DAYS["warning"] + 1}-{THRESHOLD_DAYS["expired"]} gg)</h3>'
            html += ReportService._build_html_table(data["warning_list"], COLORS["warning_orange"])

        if data["expired_list"]:
            html += f'<h3 style="color: {COLORS["error_red"]}; margin: 16px 0 12px 0; padding-left: 12px; border-left: 4px solid {COLORS["error_red"]}; font-size: 15px;">   Scaduti (&gt; {THRESHOLD_DAYS["expired"]} gg)</h3>'
            html += ReportService._build_html_table(data["expired_list"], COLORS["error_red"])

        html += "</div></div></body></html>"
        return html

    @staticmethod
    def _build_html_table(items: list[dict[str, Any]], color: str, rows_per_col: int = 10) -> str:
        """Crea tabelle HTML multi-colonna."""
        chunks = [items[i : i + rows_per_col] for i in range(0, len(items), rows_per_col)]
        html = '<table cellpadding="0" cellspacing="0" border="0"><tr>'
        for col_idx, chunk in enumerate(chunks[:4]):
            if col_idx > 0:
                html += '<td style="width: 15px;"></td>'
            html += '<td style="vertical-align: top;"><table class="data-table"><thead><tr><th>Dipendente</th><th>Badge</th><th>Ultimo Accesso</th><th style="text-align: center;">Gg</th></tr></thead><tbody>'
            for idx, dip in enumerate(chunk):
                row_bg = "#ffffff" if idx % 2 == 0 else COLORS["bg_light"]
                html += f'<tr style="background-color: {row_bg};"><td>{dip["cognome"]} {dip["nome"]}</td><td>{dip["badge"]}</td><td>{dip["data"]}</td><td style="text-align: center; color: {color}; font-weight: 600;">{dip["giorni"]}</td></tr>'
            html += "</tbody></table></td>"
        html += "</tr></table>"
        return html

    @staticmethod
    def create_report_excel(
        warning_list: list[dict[str, Any]], expired_list: list[dict[str, Any]]
    ) -> Path | None:
        """Crea il file Excel temporaneo."""
        excel_data = []
        for items, label in ((warning_list, "In Scadenza"), (expired_list, "Scaduto")):
            for dip in items:
                excel_data.append(  # noqa: PERF401
                    {
                        "Cognome": dip["cognome"],
                        "Nome": dip["nome"],
                        "Badge": dip["badge"],
                        "Ultimo Accesso": dip["data"],
                        "Giorni": dip["giorni"],
                        "Stato": label,
                    }
                )

        if not excel_data:
            return None

        df_report = pd.DataFrame(excel_data)
        path = (
            Path(os.environ["TEMP"])
            / f"report Accessi ISAB {datetime.now(UTC).astimezone().strftime('%d-%m-%Y_%H-%M')}.xlsx"
        )
        df_report.to_excel(path, index=False, sheet_name="Dipendenti")
        return path
