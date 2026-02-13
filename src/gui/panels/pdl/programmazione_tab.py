"""
SyncroJob - PDL Programmazione Tab
Scheda per il monitoraggio della programmazione settimanale SafeWork.
"""

import logging
from datetime import datetime, timedelta
from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

from src.bots import create_bot
from src.core import config_manager
from src.core.constants import Icons
from src.core.database.pdl_queries import PDLQueries
from src.gui.panels.base import BotWorker
from src.gui.widgets import TimelineWidget
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class ProgrammazioneTab(QWidget):
    """Sottoscheda per il controllo della programmazione settimanale con vista PDL aggregata."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.last_results = []
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
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # --- BARRA SUPERIORE COMPATTA ---
        top_bar = QHBoxLayout()
        
        # 1. Settimana e Ricerca
        filter_box = QVBoxLayout()
        start_date, end_date = self._get_current_week_range()
        self.week_label = QLabel(f"<b>Settimana:</b> {start_date} - {end_date}")
        self.week_label.setStyleSheet("font-size: 11px; color: #666;")
        filter_box.addWidget(self.week_label)
        
        self.req_search = QLineEdit()
        self.req_search.setPlaceholderText("Filtra richiedenti...")
        self.req_search.setClearButtonEnabled(True)
        self.req_search.setFixedWidth(180)
        self.req_search.textChanged.connect(self._filter_requesters)
        filter_box.addWidget(self.req_search)
        top_bar.addLayout(filter_box)

        # 2. Lista Richiedenti (Molto compatta)
        self.req_list = QListWidget()
        self.req_list.setFixedHeight(60)
        self.req_list.setStyleSheet("border: 1px solid #DDD; border-radius: 4px; font-size: 11px;")
        top_bar.addWidget(self.req_list, 1)

        # 3. Azioni
        actions_layout = QHBoxLayout()
        self.btn_run = ModernButton("Controlla", variant=ModernButton.Variant.PRIMARY, icon=get_asset_path(Icons.PLAY))
        self.btn_email = ModernButton("Email", variant=ModernButton.Variant.SUCCESS, icon=get_asset_path(Icons.SEND))
        self.btn_email.setEnabled(False)
        self.btn_run.clicked.connect(self._on_run_clicked)
        self.btn_email.clicked.connect(self._on_email_clicked)
        actions_layout.addWidget(self.btn_run)
        actions_layout.addWidget(self.btn_email)
        top_bar.addLayout(actions_layout)
        
        layout.addLayout(top_bar)

        # --- LOG (Dinamico) ---
        self.log_widget = TimelineWidget()
        self.log_widget.setFixedHeight(150)
        self.log_widget.setVisible(False)
        layout.addWidget(self.log_widget)

        # --- TABELLA AGGREGATA ---
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(10) # Richiedente, PDL, Descrizione, 7 Giorni
        
        # Calcolo date per Header
        start_dt = datetime.now() - timedelta(days=datetime.now().weekday())
        d = [(start_dt + timedelta(days=i)).strftime("%d/%m") for i in range(7)]
        
        headers = [
            "Richiedente", "N° PDL", "Descrizione", 
            f"LUN {d[0]}", f"MAR {d[1]}", f"MER {d[2]}", 
            f"GIO {d[3]}", f"VEN {d[4]}", f"SAB {d[5]}", f"DOM {d[6]}"
        ]
        self.results_table.setHorizontalHeaderLabels(headers)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.verticalHeader().setDefaultSectionSize(35)
        
        h_header = self.results_table.horizontalHeader()
        h_header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        h_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        h_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        h_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        
        for i in range(3, 10): 
            h_header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)
            self.results_table.setColumnWidth(i, 85)
        
        layout.addWidget(self.results_table)

    def _filter_requesters(self, text):
        text = text.lower()
        for i in range(self.req_list.count()):
            item = self.req_list.item(i)
            item.setHidden(text not in item.text().lower())

    def _get_current_week_range(self) -> tuple[str, str]:
        today = datetime.now()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return start.strftime("%d/%m/%Y"), end.strftime("%d/%m/%Y")

    def _load_requesters(self):
        try:
            requesters = PDLQueries.get_unique_requesters()
            self.req_list.clear()
            for req in requesters:
                item = QListWidgetItem(req)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.req_list.addItem(item)
        except Exception as e:
            logger.error(f"Errore caricamento richiedenti: {e}")

    def _on_log(self, message: str):
        """Aggiunge un messaggio alla console di log."""
        if hasattr(self, "log_widget"):
            self.log_widget.append(message)

    def _on_run_clicked(self):
        selected_reqs = [self.req_list.item(i).text() for i in range(self.req_list.count()) if self.req_list.item(i).checkState() == Qt.CheckState.Checked]
        if not selected_reqs:
            QMessageBox.warning(self, "Attenzione", "Seleziona almeno un richiedente.")
            return

        config = config_manager.load_config()
        safework_accounts = config.get("safework_accounts", [])
        account = next((a for a in safework_accounts if a.get("default")), safework_accounts[0]) if safework_accounts else None

        if not account:
            QMessageBox.warning(self, "Attenzione", "Credenziali SafeWork non configurate.")
            return

        start_date, end_date = self._get_current_week_range()
        bot = create_bot("programmazione_pdl", username=account["username"], password=account["password"],
                         headless=config.get("browser_headless", False), timeout=config.get("browser_timeout", 30),
                         download_path=str(config_manager.CONFIG_DIR / "temp"))

        if not bot: return
        self.btn_run.setEnabled(False)
        self.btn_email.setEnabled(False)
        self.results_table.setRowCount(0)
        self.log_widget.clear()
        self.log_widget.setVisible(True)
        self.log_widget.timeline.set_mood("running")
        
        self.worker = BotWorker(bot, [{"requesters": selected_reqs, "date_start": start_date, "date_end": end_date}])
        self.worker.log_signal.connect(self._on_log)
        self.worker.finished_signal.connect(self._on_bot_finished)
        self.worker.start()
        ToastManager.instance().show("Avvio monitoraggio...", "info")

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
            msg = f"Completato! Trovati {len(self.last_results)} PDL." if self.last_results else "Nessun dato trovato."
            ToastManager.instance().show(msg, "success" if self.last_results else "info")
        else:
            ToastManager.instance().show("Errore controllo.", "error")

    def _update_table(self, results):
        self.results_table.setRowCount(0)
        icon_tcl_on = QIcon(get_asset_path(Icons.FLAG_TCL_ON))
        icon_tcl_off = QIcon(get_asset_path(Icons.FLAG_TCL_OFF))
        icon_tgo_on = QIcon(get_asset_path(Icons.FLAG_TGO_ON))
        icon_tgo_off = QIcon(get_asset_path(Icons.FLAG_TGO_OFF))
        
        for row_idx, res in enumerate(results):
            self.results_table.insertRow(row_idx)
            self.results_table.setItem(row_idx, 0, QTableWidgetItem(res["richiedente"]))
            self.results_table.setItem(row_idx, 1, QTableWidgetItem(res["pdl"]))
            self.results_table.setItem(row_idx, 2, QTableWidgetItem(res.get("descrizione", "")))
            
            for i, prog in enumerate(res["programmazione"]):
                cell_widget = QWidget()
                cell_layout = QHBoxLayout(cell_widget)
                cell_layout.setContentsMargins(2, 0, 2, 0)
                cell_layout.setSpacing(4)
                cell_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                lbl_tcl = QLabel()
                lbl_tcl.setPixmap((icon_tcl_on if prog["tcl"] else icon_tcl_off).pixmap(32, 18))
                cell_layout.addWidget(lbl_tcl)
                
                lbl_tgo = QLabel()
                lbl_tgo.setPixmap((icon_tgo_on if prog["tgo"] else icon_tgo_off).pixmap(32, 18))
                cell_layout.addWidget(lbl_tgo)
                
                self.results_table.setCellWidget(row_idx, 3 + i, cell_widget)

    def _idx_to_day(self, idx: int) -> str:
        return ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"][idx-1]

    def _on_email_clicked(self):
        if not self.last_results: return
        try:
            import win32com.client
            outlook = win32com.client.Dispatch("Outlook.Application")
            mail = outlook.CreateItem(0)
            start_date, end_date = self._get_current_week_range()
            mail.Subject = f"Monitoraggio Programmazione Settimanale {start_date} - {end_date}"
            
            unique_reqs = set(r['richiedente'] for r in self.last_results)
            recipients = [f"{r.split()[1][0].lower()}.{r.split()[0].lower()}@isab.com" for r in unique_reqs if len(r.split()) >= 2]
            
            mail.To = "; ".join(recipients)
            mail.CC = "francesco.millo@coemi.it; ciro.scaravelli@coemi.it"
            
            html = "<h3>Report Programmazione Settimanale SafeWork</h3>"
            html += "<table border='1' style='border-collapse: collapse; font-family: Calibri; width: 100%;'>"
            html += "<tr style='background-color: #f2f2f2;'><th>Richiedente</th><th>PdL</th><th>Descrizione</th><th>Lun</th><th>Mar</th><th>Mer</th><th>Gio</th><th>Ven</th><th>Sab</th><th>Dom</th></tr>"
            
            for res in self.last_results:
                html += f"<tr><td>{res['richiedente']}</td><td>{res['pdl']}</td><td>{res.get('descrizione', '')}</td>"
                for prog in res["programmazione"]:
                    tcl = "<b style='color:#2E7D32;'>TCL</b>" if prog["tcl"] else "<b style='color:#C62828;'>TCL</b>"
                    tgo = "<b style='color:#2E7D32;'>TGO</b>" if prog["tgo"] else "<b style='color:#C62828;'>TGO</b>"
                    html += f"<td align='center'>{tcl}/{tgo}</td>"
                html += "</tr>"
            
            html += "</table><p><small>Generato da SyncroJob Enterprise</small></p>"
            mail.HTMLBody = html + mail.HTMLBody
            mail.Display()
            ToastManager.instance().show("Bozza Outlook creata!", "success")
        except Exception as e:
            QMessageBox.critical(self, "Errore Outlook", f"Errore: {e}")
