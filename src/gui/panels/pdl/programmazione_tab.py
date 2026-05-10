# mypy: disable-error-code="no-untyped-def, no-untyped-call, arg-type, attr-defined, misc, no-redef"
"""
SyncroJob - PDL Programmazione Tab (Refactored)
Scheda coordinata per il monitoraggio della programmazione settimanale SafeWork.
"""

import logging
from datetime import UTC, datetime
from typing import Any

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.bots.base.selenium_bot_config import SeleniumBotConfig
from src.bots.safework.programmazione.bot import SafeWorkProgrammazioneBot
from src.core import config_manager
from src.core.constants import Icons
from src.core.database.pdl_queries import PDLQueries
from src.core.pdl.period_manager import PDLPeriodManager
from src.gui.controllers.bot_worker import BotWorker
from src.gui.styles import COLORS
from src.gui.widgets import MultiSelectFilter, TimelineWidget
from src.gui.widgets.core_widgets import FilterComboBox, StandardGroupBox
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.pdl.status_bar_widget import ProgrammingStatusWidget
from src.gui.widgets.pdl.table_widget import ProgrammazioneTableWidget
from src.gui.widgets.toast import ToastManager
from src.utils.helpers import get_asset_path

logger = logging.getLogger(__name__)


class ProgrammazioneTab(QWidget):
    """Orchestratore della programmazione settimanale PDL."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.worker: BotWorker | None = None
        self.last_results: list[dict[str, Any]] = []
        self.tables: list[ProgrammazioneTableWidget] = []
        self._setup_ui()
        self._load_requesters()
        self._load_persisted_data()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # --- TOOLBAR ---
        top_bar = QHBoxLayout()
        filter_area = QVBoxLayout()

        start_date, end_date, _ = PDLPeriodManager.get_week_range()
        self.week_label = QLabel(f"Monitoraggio Settimana: <b>{start_date} - {end_date}</b>")
        self.week_label.setStyleSheet(f"font-size: 13px; color: {COLORS['text_dark']};")
        filter_area.addWidget(self.week_label)

        controls = QHBoxLayout()
        controls.setSpacing(20)

        # Import Controls
        self.week_selector = FilterComboBox()
        self.week_selector.addItems(["Settimana Corrente", "Settimana Prossima"])
        self.week_selector.setFixedWidth(160)
        self.week_selector.currentIndexChanged.connect(self._on_week_changed)
        controls.addWidget(self.week_selector)

        self.req_filter = MultiSelectFilter("Richiedenti", "Seleziona Bot...")
        self.req_filter.setFixedWidth(220)
        self.req_filter.changed.connect(
            lambda s: config_manager.set_config_value("selected_programming_requesters", s)
        )
        controls.addWidget(self.req_filter)

        # View Filters
        self.view_filter = MultiSelectFilter("Mostra", "Filtra Risultati...")
        self.view_filter.setFixedWidth(200)
        self.view_filter.changed.connect(lambda _: self._apply_filters())
        controls.addWidget(self.view_filter)

        self.day_selector = FilterComboBox()
        self.day_selector.addItems(
            [
                "Settimana Intera",
                "Oggi",
                "Luned ",
                "Marted ",
                "Mercoled ",
                "Gioved ",
                "Venerd ",
                "Sabato",
                "Domenica",
            ]
        )
        self.day_selector.setFixedWidth(130)
        self.day_selector.currentTextChanged.connect(lambda _: self._apply_filters())
        controls.addWidget(self.day_selector)

        self.group_selector = FilterComboBox()
        self.group_selector.addItems(["Tabella Unica", "Area", "Richiedente"])
        self.group_selector.setFixedWidth(140)
        self.group_selector.currentTextChanged.connect(self._on_group_mode_changed)
        controls.addWidget(self.group_selector)

        filter_area.addLayout(controls)
        top_bar.addLayout(filter_area)
        top_bar.addStretch()

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

        self.log_widget = TimelineWidget()
        self.log_widget.setFixedHeight(180)
        self.log_widget.setVisible(False)
        layout.addWidget(self.log_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.tables_container = QWidget()
        self.tables_layout = QVBoxLayout(self.tables_container)
        self.tables_layout.addStretch()
        self.scroll_area.setWidget(self.tables_container)
        layout.addWidget(self.scroll_area)

    def _load_requesters(self) -> None:
        try:
            reqs = PDLQueries.get_unique_requesters()
            self.req_filter.set_items(reqs)
            saved = config_manager.get_config_value("selected_programming_requesters", [])
            self.req_filter.set_selected(saved)
        except Exception as e:
            logger.exception("Errore richiedenti", exc_info=e)

    def _on_week_changed(self, idx: int) -> None:
        config_manager.set_config_value("programming_selected_week", idx)
        s, e, _ = PDLPeriodManager.get_week_range(idx)
        self.week_label.setText(f"Monitoraggio Settimana: <b>{s} - {e}</b>")
        self._load_persisted_data()

    def _load_persisted_data(self) -> None:
        s, e, _ = PDLPeriodManager.get_week_range(self.week_selector.currentIndex())
        self.last_results = PDLQueries.get_programming_results_by_week(s, e)
        self._update_tables()

    def _on_group_mode_changed(self, mode: str) -> None:
        config_manager.set_config_value("programming_group_mode", mode)
        self._update_tables()

    def _update_tables(self) -> None:
        while self.tables_layout.count() > 1:
            item = self.tables_layout.takeAt(0)
            if item and (w := item.widget()):
                w.deleteLater()
        self.tables.clear()

        if not self.last_results:
            self.view_filter.set_items([])
            return

        self.view_filter.set_items(sorted({r["richiedente"] for r in self.last_results}))
        mode = self.group_selector.currentText()

        grouped = {"Globale": self.last_results} if mode == "Tabella Unica" else {}
        if mode != "Tabella Unica":
            key = "area" if mode == "Area" else "richiedente"
            for r in self.last_results:
                val = r.get(key) or "N/D"
                if val not in grouped:
                    grouped[val] = []
                grouped[val].append(r)

        _, _, start_dt = PDLPeriodManager.get_week_range(self.week_selector.currentIndex())
        headers = PDLPeriodManager.get_table_headers(start_dt)
        today_idx = datetime.now(UTC).astimezone().weekday() if self.week_selector.currentIndex() == 0 else -1

        for name, res in sorted(grouped.items()):
            box = StandardGroupBox(name)
            box_lay = QVBoxLayout(box)
            table = ProgrammazioneTableWidget()
            table.setHorizontalHeaderLabels(headers)
            table.populate_results(res, today_idx)
            table.selection_changed_custom.connect(self._deselect_others)
            table.row_expanded.connect(lambda: QTimer.singleShot(50, self._refresh_heights))

            self.tables.append(table)
            box_lay.addWidget(table)
            self.tables_layout.insertWidget(self.tables_layout.count() - 1, box)

        self._apply_filters()
        self.btn_email.setEnabled(len(self.last_results) > 0)

    def _deselect_others(self) -> None:
        sender = self.sender()
        for t in self.tables:
            if t is not sender:
                t.clearSelection()

    def _apply_filters(self) -> None:
        selected_reqs = self.view_filter.selected
        day_choice = self.day_selector.currentText()
        target_day = {
            "Luned ": 0,
            "Marted ": 1,
            "Mercoled ": 2,
            "Gioved ": 3,
            "Venerd ": 4,
            "Sabato": 5,
            "Domenica": 6,
            "Oggi": datetime.now(UTC).astimezone().weekday(),
        }.get(day_choice, -1)

        for table in self.tables:
            for i in range(7):
                table.setColumnHidden(5 + i, target_day not in (-1, i))
            for row in range(table.rowCount()):
                it = table.item(row, 0)
                req = it.text() if it else ""
                visible = not selected_reqs or req in selected_reqs
                if target_day != -1:
                    w = table.cellWidget(row, 5 + target_day)
                    if isinstance(w, ProgrammingStatusWidget):
                        visible = visible and (w.tcl or w.tgo)
                table.setRowHidden(row, not visible)
        self._refresh_heights()

    def _refresh_heights(self) -> None:
        for table in self.tables:
            h = 25
            for r in range(table.rowCount()):
                if not table.isRowHidden(r):
                    h += table.rowHeight(r)
            box = table.parentWidget()
            if isinstance(box, StandardGroupBox):
                box.setVisible(h > 25)  # noqa: PLR2004
            table.setMinimumHeight(h + 20 if h > 25 else 0)  # noqa: PLR2004
            table.setMaximumHeight(h + 20 if h > 25 else 0)  # noqa: PLR2004

    def _on_run_clicked(self) -> None:
        """Avvia il controllo programmazione tramite bot SafeWork."""
        # 1. Recuperòcredenziali
        username, password, account_type = self.get_safework_credentials()
        if not username or not password:
            ToastManager.instance().show("Configura le credenziali SafeWork nelle Impostazioni.", "warning")
            return

        # 2. Parametri Bot
        requesters = self.req_filter.selected
        if not requesters:
            ToastManager.instance().show("Seleziona almeno un richiedente dal filtro.", "info")
            return

        start_date, end_date, _ = PDLPeriodManager.get_week_range(self.week_selector.currentIndex())

        # 3. Istanza Bot
        config = config_manager.load_config()
        bot_config = SeleniumBotConfig(
            username=username,
            password=password,
            headless=config.get("browser_headless", False),
            timeout=config.get("browser_timeout", 30),
            download_path=config_manager.get_download_path(),
        )
        bot = SafeWorkProgrammazioneBot(config=bot_config, account_type=account_type)

        # 4. Worker
        bot_data = {
            "requesters": requesters,
            "date_start": start_date,
            "date_end": end_date,
        }

        self.worker = BotWorker(bot, data=[bot_data])
        self.worker.log_signal.connect(self._on_log)
        self.worker.finished_signal.connect(self._on_worker_finished)

        # UI Update
        self.btn_run.setEnabled(False)
        self.log_widget.setVisible(True)
        self.log_widget.clear()
        self.log_widget.append(
            f"Avvio controllo programmazione per la settimana {start_date} - {end_date}..."
        )

        self.worker.start()

    def get_safework_credentials(self) -> tuple[str, str, str]:
        """Recupera le credenziali SafeWork predefinite."""
        accounts = config_manager.load_config().get("safework_accounts", [])
        if not accounts:
            return "", "", "Esecutore"
        default_acc = next((a for a in accounts if a.get("default")), accounts[0])
        return (
            default_acc.get("username", ""),
            default_acc.get("password", ""),
            default_acc.get("type", "Esecutore"),
        )

    def _on_worker_finished(self, success: bool) -> None:
        """Gestisce il completamento del bot worker."""
        self.btn_run.setEnabled(True)
        if success and self.worker:
            results = getattr(self.worker.bot, "results", [])
            start_date, end_date, _ = PDLPeriodManager.get_week_range(self.week_selector.currentIndex())
            PDLQueries.save_programming_results(results, start_date, end_date)
            self.log_widget.append(
                f"✅ Controllo completato. Trovati {len(results)} PDL aggiornati.", "SUCCESS"
            )
            self._load_persisted_data()
        else:
            self.log_widget.append("❌ Errore durante il controllo della programmazione.", "ERROR")

        if self.worker:
            self.worker.deleteLater()
            self.worker = None

    def _on_log(self, message: str) -> None:
        """Aggiunge un messaggio al widget dei log."""
        self.log_widget.append(message)

    def _on_email_clicked(self) -> None:
        """Gestione invio report via email (Placeholder)."""
        ToastManager.instance().show("Funzionalità Report Outlook in fase di implementazione.", "info")
