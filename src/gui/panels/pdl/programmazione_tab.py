"""
SyncroJob - PDL Programmazione Tab
Scheda per il monitoraggio della programmazione settimanale SafeWork.
"""

import logging
from datetime import datetime, timedelta
from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QIcon
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.bots import create_bot
from src.core import config_manager
from src.core.constants import Icons
from src.core.database.pdl_queries import PDLQueries
from src.gui.panels.base import BotWorker
from src.gui.widgets import MultiSelectFilter, TimelineWidget
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path

logger = logging.getLogger(__name__)


class ProgrammazioneTab(QWidget):
    """Sottoscheda per il controllo della programmazione settimanale con vista PDL aggregata."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.worker: BotWorker | None = None
        self.last_results: list[dict[str, Any]] = []
        self.requesters: list[str] = []
        self._setup_ui()
        self._load_requesters()
        # Carica dati persistenti
        self._load_persisted_data()

    def _load_persisted_data(self):
        """Carica dati per la settimana selezionata."""
        try:
            start_date, end_date, _ = self._get_selected_week_range()
            self.last_results = PDLQueries.get_programming_results_by_week(start_date, end_date)

            self._update_table(self.last_results)
            self.btn_email.setEnabled(len(self.last_results) > 0)

            if self.last_results:
                self._on_log(
                    f"ℹ️ Caricati {len(self.last_results)} risultati per la settimana {start_date} - {end_date}."
                )
            else:
                self._on_log(f"ℹ️ Nessun dato salvato per la settimana {start_date} - {end_date}.")
        except Exception as e:
            logger.error(f"Errore caricamento dati: {e}")
            self._on_log(f"⚠️ Errore caricamento dati: {e}")

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # --- BARRA SUPERIORE MODERNA ---
        top_bar = QHBoxLayout()

        # Area Filtri
        filter_area = QVBoxLayout()

        # Info Settimana
        start_date, end_date = self._get_current_week_range()
        self.week_label = QLabel(
            f"<span style='color: #6c757d;'>Monitoraggio Settimana:</span> "
            f"<b style='color: #212529;'>{start_date} - {end_date}</b>"
        )
        self.week_label.setStyleSheet("font-size: 13px; margin-bottom: 5px;")
        filter_area.addWidget(self.week_label)

        # Controlli in linea (Settimana + Richiedenti)
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)

        # Selettore Settimana
        self.week_selector = QComboBox()
        self.week_selector.addItems(["Settimana Corrente", "Settimana Prossima"])
        self.week_selector.setFixedWidth(200)
        self.week_selector.currentIndexChanged.connect(self._update_ui_dates)
        controls_layout.addWidget(self.week_selector)

        # Nuovo Selettore Richiedenti
        self.req_filter = MultiSelectFilter("Richiedenti", "Seleziona Richiedenti...")
        self.req_filter.setFixedWidth(300)
        # Carica selezione salvata
        saved_reqs = config_manager.get_config_value("selected_programming_requesters", [])
        self.req_filter.set_selected(saved_reqs)
        self.req_filter.changed.connect(self._on_requesters_changed)
        controls_layout.addWidget(self.req_filter)

        controls_layout.addStretch()
        filter_area.addLayout(controls_layout)

        top_bar.addLayout(filter_area)

        top_bar.addStretch()

        # Azioni
        self.btn_run = ModernButton(
            "Esegui Controllo", variant=ModernButton.Variant.PRIMARY, icon=get_asset_path(Icons.PLAY)
        )
        self.btn_email = ModernButton(
            "Report Outlook", variant=ModernButton.Variant.GHOST, icon=get_asset_path(Icons.SEND)
        )
        self.btn_email.setEnabled(False)
        self.btn_run.clicked.connect(self._on_run_clicked)
        self.btn_email.clicked.connect(self._on_email_clicked)

        top_bar.addWidget(self.btn_email)
        top_bar.addWidget(self.btn_run)

        layout.addLayout(top_bar)

        # --- LOG (Dinamico) ---
        self.log_widget = TimelineWidget()
        self.log_widget.setFixedHeight(180)
        self.log_widget.setVisible(False)
        layout.addWidget(self.log_widget)

        # --- TABELLA AGGREGATA ---
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(11)  # Richiedente, Area, PDL, Descrizione, 7 Giorni
        self.results_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e9ecef;
                border-radius: 8px;
                gridline-color: #f8f9fa;
                background-color: white;
            }
            QTableWidget::item { padding: 5px; }
        """)

        # Calcolo date per Header (Iniziale)
        self._update_ui_dates()
        self.results_table.setAlternatingRowColors(True)

        if v_header := self.results_table.verticalHeader():
            v_header.setVisible(False)
            v_header.setDefaultSectionSize(40)

        if h_header := self.results_table.horizontalHeader():
            h_header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            h_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Richiedente
            h_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Area
            h_header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # PDL
            h_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Descrizione

            for i in range(4, 11):
                h_header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
                self.results_table.setColumnWidth(i, 85)

        layout.addWidget(self.results_table)

    def _get_selected_week_range(self) -> tuple[str, str, datetime]:
        """Restituisce start_str, end_str e start_dt in base alla selezione."""
        today = datetime.now()
        current_weekday = today.weekday()
        start_current = today - timedelta(days=current_weekday)

        # 0 = Current, 1 = Next
        offset = self.week_selector.currentIndex() if hasattr(self, "week_selector") else 0

        start_target = start_current + timedelta(weeks=offset)
        end_target = start_target + timedelta(days=6)

        return start_target.strftime("%d/%m/%Y"), end_target.strftime("%d/%m/%Y"), start_target

    def _get_current_week_range(self) -> tuple[str, str]:
        # Mantenuto per compatibilità o uso interno iniziale
        s, e, _ = self._get_selected_week_range()
        return s, e

    def _update_ui_dates(self):
        """Aggiorna label, header tabella e carcia i dati per la settimana selezionata."""
        start_str, end_str, start_dt = self._get_selected_week_range()

        # Update Label
        if hasattr(self, "week_label"):
            self.week_label.setText(
                f"<span style='color: #6c757d;'>Monitoraggio Settimana:</span> "
                f"<b style='color: #212529;'>{start_str} - {end_str}</b>"
            )

        # Update Table Headers
        d = [(start_dt + timedelta(days=i)).strftime("%d/%m") for i in range(7)]
        headers = [
            "Richiedente",
            "Area",
            "N° PDL",
            "Descrizione",
            f"LUN {d[0]}",
            f"MAR {d[1]}",
            f"MER {d[2]}",
            f"GIO {d[3]}",
            f"VEN {d[4]}",
            f"SAB {d[5]}",
            f"DOM {d[6]}",
        ]

        # Evidenzia giorno corrente con stile moderno (Background + Colore)
        is_current_week = getattr(self, "week_selector", None) and self.week_selector.currentIndex() == 0
        current_weekday = datetime.now().weekday()

        if hasattr(self, "results_table"):
            self.results_table.setHorizontalHeaderLabels(headers)

            # Applica stili agli header
            for i in range(4, 11):
                item = self.results_table.horizontalHeaderItem(i)
                if not item:
                    continue

                is_today = is_current_week and (i - 4 == current_weekday)

                if is_today:
                    # Giorno Corrente: Azzurro chiaro sfondo, Blu scuro testo e indicatore testuale
                    item.setBackground(QColor("#e7f1ff"))
                    item.setForeground(QColor("#0d6efd"))

                    # Aggiungiamo un pallino visibile nel testo dell'header
                    header_text = headers[i]
                    if " ●" not in header_text:
                        item.setText(f"{header_text} ●")

                    font = QFont()
                    font.setBold(True)
                    font.setPointSize(11)  # Più grande per visibilità
                    item.setFont(font)
                    item.setToolTip("Oggi")
                else:
                    # Reset (usa defaults o null per ereditare stylesheet)
                    item.setBackground(QColor("#f8f9fa"))
                    item.setForeground(QColor("#495057"))
                    item.setText(headers[i])
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.setToolTip("")

        # Ricarica i dati per la nuova settimana
        self._load_persisted_data()

    def _load_requesters(self):
        try:
            self.requesters = PDLQueries.get_unique_requesters()
            self.req_filter.set_items(self.requesters)
        except Exception as e:
            logger.error(f"Errore caricamento richiedenti: {e}")

    def _on_requesters_changed(self, selected: list[str]):
        """Salva i richiedenti selezionati nella configurazione."""
        config_manager.set_config_value("selected_programming_requesters", selected)

    def _on_log(self, message: str):
        """Aggiunge un messaggio alla console di log."""
        if hasattr(self, "log_widget"):
            self.log_widget.append(message)

    def _on_run_clicked(self):
        selected_reqs = self.req_filter.selected

        if not selected_reqs:
            ToastManager.instance().show("Seleziona almeno un richiedente.", "warning")
            return

        config = config_manager.load_config()
        safework_accounts = config.get("safework_accounts", [])
        account = None
        if safework_accounts:
            account = next((a for a in safework_accounts if a.get("default")), safework_accounts[0])

        if not account:
            ToastManager.instance().show("Credenziali SafeWork non configurate.", "error")
            return

        start_date, end_date, _ = self._get_selected_week_range()

        # Assicura che la cartella temp esista
        temp_dir = config_manager.CONFIG_DIR / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)

        bot = create_bot(
            "programmazione_pdl",
            username=account["username"],
            password=account["password"],
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=str(temp_dir),
        )

        if not bot:
            return

        self.btn_run.setEnabled(False)
        self.btn_email.setEnabled(False)
        self.results_table.setRowCount(0)
        self.log_widget.clear()
        self.log_widget.setVisible(True)
        self.log_widget.timeline.set_mood("running")

        self.worker = BotWorker(
            bot, [{"requesters": selected_reqs, "date_start": start_date, "date_end": end_date}]
        )
        self.worker.log_signal.connect(self._on_log)
        self.worker.finished_signal.connect(self._on_bot_finished)
        self.worker.start()
        ToastManager.instance().show("Avvio monitoraggio SafeWork...", "info")

    def _on_bot_finished(self, success: bool):
        self.btn_run.setEnabled(True)
        self.log_widget.timeline.set_mood("idle")
        if success and self.worker:
            self.log_widget.setVisible(False)
            self.last_results = getattr(self.worker.bot, "results", [])

            start_date, end_date, _ = self._get_selected_week_range()
            if self.last_results:
                PDLQueries.save_programming_results(self.last_results, start_date, end_date)

            self._update_table(self.last_results)
            self.btn_email.setEnabled(len(self.last_results) > 0)
            msg = (
                f"Completato! Trovati {len(self.last_results)} PDL."
                if self.last_results
                else "Nessun dato trovato."
            )
            ToastManager.instance().show(msg, "success" if self.last_results else "info")

            # Refresh logs per confermare salvataggio
            self._on_log(f"✅ Dati salvati per la settimana {start_date} - {end_date}")
        else:
            ToastManager.instance().show("Errore durante il controllo SafeWork.", "error")

    def _update_table(self, results: list[dict[str, Any]]):
        self.results_table.setRowCount(0)
        icon_tcl_on = QIcon(get_asset_path(Icons.FLAG_TCL_ON))
        icon_tcl_off = QIcon(get_asset_path(Icons.FLAG_TCL_OFF))
        icon_tgo_on = QIcon(get_asset_path(Icons.FLAG_TGO_ON))
        icon_tgo_off = QIcon(get_asset_path(Icons.FLAG_TGO_OFF))

        today_idx = datetime.now().weekday()

        for row_idx, res in enumerate(results):
            self.results_table.insertRow(row_idx)
            self.results_table.setItem(row_idx, 0, QTableWidgetItem(res["richiedente"]))
            self.results_table.setItem(row_idx, 1, QTableWidgetItem(res.get("area", "")))
            self.results_table.setItem(row_idx, 2, QTableWidgetItem(res["pdl"]))
            self.results_table.setItem(row_idx, 3, QTableWidgetItem(res.get("descrizione", "")))

            for i, prog in enumerate(res["programmazione"]):
                cell_widget = QWidget()
                cell_layout = QHBoxLayout(cell_widget)
                cell_layout.setContentsMargins(4, 2, 4, 2)
                cell_layout.setSpacing(6)
                cell_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # TCL
                lbl_tcl = QLabel()
                lbl_tcl.setPixmap((icon_tcl_on if prog["tcl"] else icon_tcl_off).pixmap(32, 18))
                lbl_tcl.setToolTip(f"TCL: {'Programmato' if prog['tcl'] else 'Assente'}")
                cell_layout.addWidget(lbl_tcl)

                # TGO
                lbl_tgo = QLabel()
                lbl_tgo.setPixmap((icon_tgo_on if prog["tgo"] else icon_tgo_off).pixmap(32, 18))
                lbl_tgo.setToolTip(f"TGO: {'Programmato' if prog['tgo'] else 'Assente'}")
                cell_layout.addWidget(lbl_tgo)

                # Evidenzia giorno oggi
                if i == today_idx:
                    cell_widget.setStyleSheet("background-color: rgba(13, 110, 253, 0.05);")

                self.results_table.setCellWidget(row_idx, 4 + i, cell_widget)

    def _on_email_clicked(self):
        if not self.last_results:
            return
        try:
            import win32com.client  # type: ignore

            outlook = win32com.client.Dispatch("Outlook.Application")
            mail = outlook.CreateItem(0)
            start_date, end_date, start_dt = self._get_selected_week_range()

            # Calcolo numero settimana
            week_num = start_dt.isocalendar()[1]
            mail.Subject = f"Programmazione Settimanale - Settimana {week_num} ({start_date} - {end_date})"

            unique_reqs = {r["richiedente"] for r in self.last_results}
            recipients = []
            for r in unique_reqs:
                if r and len(r.split()) >= 2:
                    parts = r.split()
                    # Destinatari: rimuovi punti (fcaldarella invece di f.caldarella)
                    email_prefix = f"{parts[1][0].lower()}{parts[0].lower()}"
                    recipients.append(f"{email_prefix}@isab.com")

            mail.To = "; ".join(recipients)
            mail.CC = "francesco.millo@coemi.it; ciro.scaravelli@coemi.it"

            # Check se siamo nella settimana corrente per evidenziazione oggi
            is_current_week = getattr(self, "week_selector", None) and self.week_selector.currentIndex() == 0
            today_idx = datetime.now().weekday() if is_current_week else -1

            # Template HTML Moderno e Professionale (Larghezza Dinamica)
            html = """
            <div style='font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif; color: #212529; padding: 20px; line-height: 1.5;'>
                <h2 style='color: #0d6efd; border-bottom: 2px solid #e9ecef; padding-bottom: 15px; font-size: 24px; margin-top: 0;'>
                    Programmazione Settimanale
                </h2>
                <p style='font-size: 16px; margin-bottom: 20px;'>
                    Periodo: <span style='color: #0d6efd; font-weight: bold;'>{start_date} - {end_date}</span>
                    <span style='color: #6c757d; margin-left: 10px;'>(Settimana {week_num})</span>
                </p>

                <table style='border-collapse: collapse; min-width: 600px; width: auto; font-size: 14px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #dee2e6;'>
                    <thead>
                        <tr style='background-color: #f8f9fa; color: #495057; text-align: left;'>
                            <th style='padding: 12px 15px; border: 1px solid #dee2e6;'>Richiedente</th>
                            <th style='padding: 12px 15px; border: 1px solid #dee2e6;'>Area</th>
                            <th style='padding: 12px 15px; border: 1px solid #dee2e6; text-align: center;'>PdL</th>
                            <th style='padding: 12px 15px; border: 1px solid #dee2e6;'>Descrizione</th>
                            {headers_html}
                        </tr>
                    </thead>
                    <tbody>
            """

            day_names = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
            headers_html = ""
            for i, day in enumerate(day_names):
                style = "padding: 12px 10px; border: 1px solid #dee2e6; text-align: center; min-width: 65px;"
                if i == today_idx:
                    style += " background-color: #e7f1ff; color: #0d6efd; font-weight: bold; border-bottom: 3px solid #0d6efd;"
                    day += " ●"
                headers_html += f"<th style='{style}'>{day}</th>"

            html = html.format(
                start_date=start_date, end_date=end_date, week_num=week_num, headers_html=headers_html
            )

            for res in self.last_results:
                html += "<tr>"
                html += f"<td style='padding: 12px 15px; border: 1px solid #dee2e6; white-space: nowrap;'>{res['richiedente']}</td>"
                html += f"<td style='padding: 12px 15px; border: 1px solid #dee2e6; color: #495057;'>{res.get('area', '')}</td>"
                html += f"<td style='padding: 12px; border: 1px solid #dee2e6; text-align: center;'><b>{res['pdl']}</b></td>"
                html += f"<td style='padding: 12px 15px; border: 1px solid #dee2e6; color: #495057;'>{res.get('descrizione', '')}</td>"

                for i, prog in enumerate(res["programmazione"]):
                    tcl_val = prog["tcl"]
                    tgo_val = prog["tgo"]

                    bg_color = "#ffffff"
                    if tcl_val or tgo_val:
                        bg_color = "#f8fff9"  # Verde chiarissimo attività

                    if i == today_idx:
                        bg_color = "#f0f7ff"  # Azzurro oggi

                    tcl_style = f"color: {'#198754' if tcl_val else '#dc3545'}; font-weight: {'bold' if tcl_val else 'normal'};"
                    tgo_style = f"color: {'#198754' if tgo_val else '#dc3545'}; font-weight: {'bold' if tgo_val else 'normal'};"

                    html += f"<td align='center' style='padding: 10px; border: 1px solid #dee2e6; background-color: {bg_color}; font-size: 13px;'>"
                    html += f"<span style='{tcl_style}'>TCL</span><br><span style='{tgo_style}'>TGO</span>"
                    html += "</td>"
                html += "</tr>"

            html += """
                    </tbody>
                </table>
            </div>
            """

            mail.HTMLBody = html + mail.HTMLBody
            mail.Display()
            ToastManager.instance().show("Bozza Outlook creata!", "success")
        except Exception as e:
            ToastManager.instance().show(f"Errore Outlook: {e}", "error")
