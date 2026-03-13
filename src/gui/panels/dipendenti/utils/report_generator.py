import logging
import operator
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from PyQt6.QtWidgets import QMessageBox

from src.core.database import db_manager
from src.core.report_history import ReportHistory
from src.gui.panels.dipendenti.utils.data_helpers import build_timbrature_maps
from src.gui.styles import COLORS
from src.gui.styles.constants import THRESHOLD_DAYS
from src.gui.widgets.toast import ToastManager

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Gestisce la generazione e l'invio dei report per l'anagrafica dipendenti."""

    @staticmethod
    def generate_email_report(parent_widget=None):
        """Genera email report professionale coordinando raccolta dati, generazione HTML/Excel e invio."""
        try:
            # 1. Raccolta e classificazione dati
            report_data = ReportGenerator._gather_report_data()
            if not report_data["warning_list"] and not report_data["expired_list"]:
                if parent_widget:
                    QMessageBox.information(
                        parent_widget,
                        "Nessun dipendente",
                        "Ottimo! Non ci sono dipendenti in scadenza o scaduti.",
                    )
                return

            # 2. Generazione HTML
            body_html = ReportGenerator._build_report_html(report_data)

            # 3. Generazione Excel
            excel_path = ReportGenerator._create_report_excel(
                report_data["warning_list"], report_data["expired_list"]
            )

            # 4. Invio Email
            ReportGenerator._send_report_email(body_html, excel_path, report_data)

        except Exception as e:
            logger.error(f"Errore generazione email report: {e}")
            if parent_widget:
                QMessageBox.critical(parent_widget, "Errore", f"Impossibile generare il report:\n{e}")

    @staticmethod
    def _gather_report_data():
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
        last_by_cf, last_by_name, normalize = build_timbrature_maps(accessi)

        warning_list = []
        expired_list = []

        for dip in dipendenti:
            id_ris, cog, nom, cf, badge, _ = dip
            cf_norm = normalize(cf or "")
            name_key = (normalize(cog or ""), normalize(nom or ""))

            diff_days = last_by_cf.get(cf_norm) or last_by_name.get(name_key)
            if diff_days is None:
                continue

            last_access_date = datetime.now() - timedelta(days=diff_days)
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

        # Ordinamento per urgenza
        warning_list.sort(key=operator.itemgetter("giorni"), reverse=True)
        expired_list.sort(key=operator.itemgetter("giorni"), reverse=True)

        return {
            "warning_list": warning_list,
            "expired_list": expired_list,
            "total_monitored": len(dipendenti),
        }

    @staticmethod
    def _build_report_html(data):
        """Costruisce il template HTML per l'email."""
        from src.core.version import __version__

        current_date = datetime.now().strftime("%d/%m/%Y %H:%M")
        font_family = "'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif"
        header_color = COLORS["primary_dark"]
        border_color = COLORS["border_light"]

        # Executive Summary Logic
        urgenti = len([d for d in data["expired_list"] if d["giorni"] > 60])
        tot_attenzione = len(data["warning_list"]) + len(data["expired_list"])

        if urgenti > 0:
            sum_text = f"<strong>ATTENZIONE:</strong> {urgenti} dipendenti richiedono azione <strong>IMMEDIATA</strong> (oltre {THRESHOLD_DAYS['critical']} giorni). Totale da gestire: {tot_attenzione}."
            sum_color, sum_icon = COLORS["error_red"], "⚠️"
        elif len(data["expired_list"]) > 0:
            sum_text = f"<strong>{len(data['expired_list'])}</strong> dipendenti scaduti e <strong>{len(data['warning_list'])}</strong> in scadenza richiedono attenzione."
            sum_color, sum_icon = COLORS["warning_orange"], "🚨"
        else:
            sum_text = f"<strong>{len(data['warning_list'])}</strong> dipendenti in scadenza da monitorare nei prossimi giorni."
            sum_color, sum_icon = COLORS["primary_dark"], "ℹ️"

        # Trend calculation
        trend_html = ""
        trend = ReportHistory.calculate_trend(len(data["warning_list"]), len(data["expired_list"]))
        if trend:
            parts = []
            for k, label in (
                ("warning_diff", "in scadenza"),
                ("expired_diff", "scaduti"),
            ):
                diff = trend[k]
                if diff > 0:
                    parts.append(f'<span style="color: {COLORS["error_red"]};">+{diff} {label}</span>')
                elif diff < 0:
                    parts.append(f'<span style="color: {COLORS["success_dark"]};">{diff} {label}</span>')
            if parts:
                trend_html = f'<p style="margin: 8px 0 0 0; padding: 10px 12px; background-color: {COLORS["bg_light"]}; border-radius: 4px; font-size: 12px; color: {COLORS["text_muted"]};">📊 <strong>Trend:</strong> {" | ".join(parts)} rispetto al {trend["last_date"]}</p>'

        # Main Template
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: {font_family}; margin: 0; padding: 0; color: {COLORS["text_dark"]}; background-color: {COLORS["bg_light"]}; }}
                .container {{ width: auto; max-width: 1500px; margin: 0 auto; background-color: {COLORS["bg_white"]}; }}
                .summary-table {{ width: auto; min-width: 480px; border-collapse: separate; border-spacing: 8px; margin: 16px auto; }}
                .card {{ background-color: {COLORS["bg_white"]}; padding: 14px 20px; border: 1px solid {border_color}; border-radius: 6px; text-align: center; width: 160px; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }}
                .card-number {{ font-size: 24px; font-weight: 700; display: block; margin-bottom: 4px; letter-spacing: -0.5px; }}
                .card-label {{ font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; color: {COLORS["text_muted"]}; font-weight: 600; }}
                .data-table {{ width: auto; border-collapse: collapse; margin: 0 0 20px 0; background-color: white; border: 1px solid {border_color}; }}
                .data-table th {{ background-color: {COLORS["table_info_bg"]}; text-align: left; padding: 5px 10px; border: 1px solid {COLORS["border_light"]}; font-size: 12px; color: {COLORS["primary_dark"]}; text-transform: uppercase; font-weight: 600; letter-spacing: 0.3px; }}
                .data-table td {{ padding: 5px 12px; border: 1px solid {border_color}; font-size: 13px; vertical-align: middle; color: {COLORS["text_dark"]}; }}
            </style>
        </head>
        <body style="background-color: {COLORS["bg_light"]}; margin: 0; padding: 20px 0;">
            <div class="container" style="border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08);">
                <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: {COLORS["primary_dark"]};">
                    <tr><td style="padding: 20px 24px; text-align: center;">
                        <h2 style="margin: 0; font-weight: 700; font-size: 20px; color: {COLORS["bg_white"]};">Report Monitoraggio Accessi in ISAB</h2>
                        <p style="margin: 8px 0 0 0; font-size: 13px; color: {COLORS["table_info_bg"]};">Generato il {current_date} da SyncroJob v{__version__}</p>
                    </td></tr>
                </table>
                <div style="padding: 16px 20px; background-color: {COLORS["bg_white"]};">
                    <table class="summary-table" style="margin: 0 auto;">
                        <tr>
                            <td><div class="card" style="border-left: 3px solid {header_color}; text-align: left;"><span class="card-number">{data["total_monitored"]}</span><span class="card-label">Monitorati</span></div></td>
                            <td><div class="card" style="border-left: 3px solid {COLORS["warning_orange"]}; text-align: left;"><span class="card-number">{len(data["warning_list"])}</span><span class="card-label">In Scadenza</span></div></td>
                            <td><div class="card" style="border-left: 3px solid {COLORS["error_red"]}; text-align: left;"><span class="card-number">{len(data["expired_list"])}</span><span class="card-label">Scaduti</span></div></td>
                        </tr>
                    </table>
                </div>
                <div style="padding: 0 20px 20px 20px; background-color: {COLORS["bg_white"]};">
                    <p style="margin: 0 0 8px 0; padding: 12px; background-color: {COLORS["bg_light"]}; border-radius: 6px; color: {sum_color}; font-size: 13px; border-left: 3px solid {sum_color}; font-weight: 500;">
                        {sum_icon} {sum_text}</p>
                    {trend_html}
        """

        if data["warning_list"]:
            html += f'<h3 style="color: {COLORS["warning_orange"]}; margin: 16px 0 12px 0; padding-left: 12px; border-left: 4px solid {COLORS["warning_orange"]}; font-size: 15px;">⚠️ In Scadenza ({THRESHOLD_DAYS["warning"] + 1}-{THRESHOLD_DAYS["expired"]} gg)</h3>'
            html += ReportGenerator._build_html_table(data["warning_list"], COLORS["warning_orange"])

        if data["expired_list"]:
            html += f'<h3 style="color: {COLORS["error_red"]}; margin: 16px 0 12px 0; padding-left: 12px; border-left: 4px solid {COLORS["error_red"]}; font-size: 15px;">🚫 Scaduti (&gt; {THRESHOLD_DAYS["expired"]} gg)</h3>'
            html += ReportGenerator._build_html_table(data["expired_list"], COLORS["error_red"])

        html += "</div></div></body></html>"
        return html

    @staticmethod
    def _build_html_table(items, color, rows_per_col=10):
        """Crea tabelle HTML multi-colonna."""
        chunks = [items[i : i + rows_per_col] for i in range(0, len(items), rows_per_col)]
        html = '<table cellpadding="0" cellspacing="0" border="0"><tr>'
        for col_idx, chunk in enumerate(chunks[:4]):
            if col_idx > 0:
                html += '<td style="width: 15px;"></td>'
            html += '<td style="vertical-align: top;"><table class="data-table"><thead><tr><th>Dipendente</th><th>Badge</th><th>Ultimo Accesso</th><th style="text-align: center;">Gg</th></tr></thead><tbody>'
            for idx, dip in enumerate(chunk):
                row_bg = COLORS["bg_white"] if idx % 2 == 0 else COLORS["bg_light"]
                html += f'<tr style="background-color: {row_bg};"><td>{dip["cognome"]} {dip["nome"]}</td><td>{dip["badge"]}</td><td>{dip["data"]}</td><td style="text-align: center; color: {color}; font-weight: 600;">{dip["giorni"]}</td></tr>'
            html += "</tbody></table></td>"
        html += "</tr></table>"
        return html

    @staticmethod
    def _create_report_excel(warning_list, expired_list):
        """Crea il file Excel temporaneo con i dati del report."""
        excel_data: list[dict[str, Any]] = []
        for items, label in ((warning_list, "In Scadenza"), (expired_list, "Scaduto")):
            excel_data.extend(
                {
                    "Cognome": dip["cognome"],
                    "Nome": dip["nome"],
                    "Badge": dip["badge"],
                    "Ultimo Accesso": dip["data"],
                    "Giorni": dip["giorni"],
                    "Stato": label,
                }
                for dip in items
            )

        if not excel_data:
            return None

        import pandas as pd

        df_report = pd.DataFrame(excel_data)
        path = (
            Path(os.environ["TEMP"]) / f"report Accessi ISAB {datetime.now().strftime('%d-%m-%Y_%H-%M')}.xlsx"
        )
        df_report.to_excel(path, index=False, sheet_name="Dipendenti")
        return path

    @staticmethod
    def _send_report_email(body_html, excel_path, data):
        """Gestisce l'invio fisico dell'email tramite Outlook o Browser."""
        subject = f"Report Monitoraggio Accessi in ISAB - {datetime.now().strftime('%d/%m/%Y')}"

        if os.name == "nt":
            try:
                import pythoncom
                import win32com.client

                # Inizializza COM per il thread corrente (essenziale in app compilate)
                pythoncom.CoInitialize()

                try:
                    # Usa Dispatch dinamico (più sicuro per app compilate/PyInstaller)
                    # Evita EnsureDispatch che tenta di scrivere nella cache (spesso read-only o mancante)
                    outlook = win32com.client.Dispatch("Outlook.Application")

                    from src.core.constants import Emails

                    mail = outlook.CreateItem(0)
                    mail.To = Emails.ACCESSI_TO
                    mail.CC = Emails.ACCESSI_CC
                    mail.Subject = subject
                    mail.HTMLBody = body_html
                    if excel_path and excel_path.exists():
                        mail.Attachments.Add(str(excel_path))
                    mail.Display()

                    ReportHistory.save_report(data["warning_list"], data["expired_list"])
                    ToastManager.instance().show(
                        "Report generato in Outlook con allegato Excel",
                        "success",
                        duration=3000,
                    )
                    return

                except Exception as e:
                    logger.error(f"Outlook automation error: {e}", exc_info=True)
                    # Non fare raise qui, lascia che scenda al fallback

            except Exception as e:
                logger.warning(f"Outlook integration failed (module import or init): {e}")

        # Fallback Browser / Sistema
        from PyQt6.QtCore import QUrl
        from PyQt6.QtGui import QDesktopServices

        tmp_path = Path(os.environ["TEMP"]) / f"report_isab_{datetime.now().strftime('%H%M%S')}.html"
        try:
            tmp_path.write_text(body_html, encoding="utf-8")
            # Usa QDesktopServices per aprire il file con l'app predefinita del sistema
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(tmp_path)))

            ReportHistory.save_report(data["warning_list"], data["expired_list"])
            ToastManager.instance().show(
                "Outlook non disponibile: aperto anteprima report",
                "warning",
                duration=4000,
            )
        except Exception as e:
            logger.error(f"Errore fallback report: {e}")
            ToastManager.instance().show("Impossibile aprire il report", "error")
