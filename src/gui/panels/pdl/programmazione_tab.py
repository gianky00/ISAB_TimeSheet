"""
SyncroJob - PDL Programmazione Tab
Scheda per il monitoraggio della programmazione settimanale SafeWork.
"""

import logging
from datetime import datetime, timedelta
from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
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
        """Carica l'ultimo controllo salvato dal database."""
        self.last_results = PDLQueries.get_last_programming_results()
        if self.last_results:
            self._update_table(self.last_results)
            self.btn_email.setEnabled(True)
            self._on_log("ℹ️ Caricati risultati dell'ultimo controllo salvato.")

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
        self.week_label.setStyleSheet("font-size: 13px;")
        filter_area.addWidget(self.week_label)

        # Nuovo Selettore Richiedenti
        self.req_filter = MultiSelectFilter("Richiedenti", "Seleziona Richiedenti...")
        self.req_filter.setFixedWidth(300)
        # Carica selezione salvata
        saved_reqs = config_manager.get_config_value("selected_programming_requesters", [])
        self.req_filter.set_selected(saved_reqs)
        self.req_filter.changed.connect(self._on_requesters_changed)

        filter_area.addWidget(self.req_filter)
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
        self.results_table.setColumnCount(10)  # Richiedente, PDL, Descrizione, 7 Giorni
        self.results_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e9ecef;
                border-radius: 8px;
                gridline-color: #f8f9fa;
                background-color: white;
            }
            QTableWidget::item { padding: 5px; }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
                color: #495057;
            }
        """)

        # Calcolo date per Header
        today = datetime.now()
        current_weekday = today.weekday()  # 0 = Lun
        start_dt = today - timedelta(days=current_weekday)
        d = [(start_dt + timedelta(days=i)).strftime("%d/%m") for i in range(7)]

        headers = [
            "Richiedente",
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
        self.results_table.setHorizontalHeaderLabels(headers)
        self.results_table.setAlternatingRowColors(True)

        if v_header := self.results_table.verticalHeader():
            v_header.setVisible(False)
            v_header.setDefaultSectionSize(40)

        if h_header := self.results_table.horizontalHeader():
            h_header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            h_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
            h_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            h_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

            for i in range(3, 10):
                h_header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
                self.results_table.setColumnWidth(i, 85)

                # Evidenzia giorno corrente
                if i - 3 == current_weekday:
                    headers[i] = f"➤ {headers[i]}"
                    self.results_table.setHorizontalHeaderLabels(headers)

        layout.addWidget(self.results_table)

    def _get_current_week_range(self) -> tuple[str, str]:
        today = datetime.now()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return start.strftime("%d/%m/%Y"), end.strftime("%d/%m/%Y")

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

        start_date, end_date = self._get_current_week_range()
        bot = create_bot(
            "programmazione_pdl",
            username=account["username"],
            password=account["password"],
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=str(config_manager.CONFIG_DIR / "temp"),
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
            if self.last_results:
                PDLQueries.save_programming_results(self.last_results)
            self._update_table(self.last_results)
            self.btn_email.setEnabled(len(self.last_results) > 0)
            msg = (
                f"Completato! Trovati {len(self.last_results)} PDL."
                if self.last_results
                else "Nessun dato trovato."
            )
            ToastManager.instance().show(msg, "success" if self.last_results else "info")
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
            self.results_table.setItem(row_idx, 1, QTableWidgetItem(res["pdl"]))
            self.results_table.setItem(row_idx, 2, QTableWidgetItem(res.get("descrizione", "")))

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

                self.results_table.setCellWidget(row_idx, 3 + i, cell_widget)

    def _on_email_clicked(self):
        if not self.last_results:
            return
        try:
            import win32com.client

            outlook = win32com.client.Dispatch("Outlook.Application")
            mail = outlook.CreateItem(0)
            start_date, end_date = self._get_current_week_range()
            mail.Subject = f"Monitoraggio Programmazione Settimanale {start_date} - {end_date}"

            unique_reqs = {r["richiedente"] for r in self.last_results}
            recipients = []
            for r in unique_reqs:
                if r and len(r.split()) >= 2:
                    parts = r.split()
                    # Fallback logic per email richiedente
                    recipients.append(f"{parts[1][0].lower()}.{parts[0].lower()}@isab.com")

            mail.To = "; ".join(recipients)
            mail.CC = "francesco.millo@coemi.it; ciro.scaravelli@coemi.it"

            html = "<h2 style='color: #0d6efd; font-family: Segoe UI, sans-serif;'>Report Programmazione Settimanale</h2>"
            html += (
                f"<p style='font-family: Segoe UI, sans-serif;'>Periodo: <b>{start_date} - {end_date}</b></p>"
            )
            html += "<table border='1' style='border-collapse: collapse; font-family: Segoe UI, sans-serif; width: 100%; font-size: 13px;'>"
            html += "<tr style='background-color: #f8f9fa;'><th>Richiedente</th><th>PdL</th><th>Descrizione</th><th>Lun</th><th>Mar</th><th>Mer</th><th>Gio</th><th>Ven</th><th>Sab</th><th>Dom</th></tr>"

            for res in self.last_results:
                html += f"<tr><td style='padding: 5px;'>{res['richiedente']}</td>"
                html += f"<td style='padding: 5px; text-align: center;'><b>{res['pdl']}</b></td>"
                html += f"<td style='padding: 5px;'>{res.get('descrizione', '')}</td>"
                for prog in res["programmazione"]:
                    tcl_val = prog["tcl"]
                    tgo_val = prog["tgo"]
                    tcl_html = f"<span style='color:{'#2E7D32' if tcl_val else '#C62828'}; font-weight: bold;'>TCL</span>"
                    tgo_html = f"<span style='color:{'#2E7D32' if tgo_val else '#C62828'}; font-weight: bold;'>TGO</span>"
                    html += f"<td align='center' style='padding: 5px; background-color: {'#e8f5e9' if (tcl_val or tgo_val) else 'transparent'};'>{tcl_html}/{tgo_html}</td>"
                html += "</tr>"

            html += "</table><p style='color: #6c757d; font-size: 11px; font-family: Segoe UI, sans-serif;'>Generato automaticamente da SyncroJob Enterprise</p>"
            mail.HTMLBody = html + mail.HTMLBody
            mail.Display()
            ToastManager.instance().show("Bozza Outlook creata!", "success")
        except Exception as e:
            ToastManager.instance().show(f"Errore Outlook: {e}", "error")
