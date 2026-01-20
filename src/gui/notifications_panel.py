"""
SyncroJob - Notifications Panel
Pannello per la visualizzazione delle notifiche e Audit Log Dashboard.
"""

import json
from datetime import datetime

from PyQt6.QtCore import QDate, Qt, QTimer
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTableView,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.core.audit_manager import AuditManager
from src.core.constants import Icons
from src.core.notification_manager import NotificationManager
from src.gui.models.audit_model import AuditTableModel
from src.gui.widgets.calendar_date_edit import CalendarDateEdit
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.notification_item import NotificationItem
from src.utils.helpers import get_asset_path, get_colored_icon


class AuditDetailDialog(QDialog):
    """Dialog per visualizzare i dettagli completi di un log."""

    def __init__(self, log_data, parent=None):
        super().__init__(parent)
        self.log_data = log_data  # Save for copy
        self.setWindowTitle("Dettagli Audit Log")
        self.setMinimumSize(700, 600)
        self._setup_ui(log_data)

    def _setup_ui(self, data):
        layout = QVBoxLayout(self)

        # Header Info
        ts = data.get("timestamp", "-")
        try:
            dt = datetime.fromisoformat(ts)
            ts = dt.strftime("%d/%m/%Y %H:%M:%S")
        except ValueError:
            pass

        dur_ms = data.get("duration_ms", 0) or 0
        dur_str = f"{dur_ms}ms" if dur_ms < 1000 else f"{dur_ms/1000:.2f}s"

        err_code = data.get("error_code") or "Nessuno"
        module = data.get("module") or "Generico"

        info_text = f"""
        <table style="font-size: 14px; margin-bottom: 10px;" cellspacing="5">
            <tr><td><b>Data:</b></td><td>{ts}</td><td><b>Modulo:</b></td><td>{module}</td></tr>
            <tr><td><b>Utente:</b></td><td>{data.get('user_id', '-')}</td><td><b>Durata:</b></td><td>{dur_str}</td></tr>
            <tr><td><b>Azione:</b></td><td>{data.get('action', '-')}</td><td><b>Cod. Errore:</b></td><td>{err_code}</td></tr>
            <tr><td><b>Entità:</b></td><td>{data.get('entity', '-')}</td><td><b>Stato:</b></td><td>{data.get('status', '-')}</td></tr>
        </table>
        """
        lbl = QLabel(info_text)
        lbl.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(lbl)

        # JSON Viewer
        layout.addWidget(QLabel("<b>Dettagli Tecnici (JSON):</b>"))

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet(
            "font-family: Consolas, monospace; font-size: 13px; background-color: #f8f9fa;"
        )

        try:
            params_str = data.get("params", "{}")
            if isinstance(params_str, str):
                params_json = json.loads(params_str)
            else:
                params_json = params_str

            pretty_json = json.dumps(params_json, indent=4, ensure_ascii=False)
            self.text_edit.setText(pretty_json)
        except (json.JSONDecodeError, TypeError):
            self.text_edit.setText(str(data.get("params", "-")))

        layout.addWidget(self.text_edit)

        # Buttons Bar
        btn_layout = QHBoxLayout()

        # Copia JSON
        btn_copy = QPushButton("Copia JSON")
        btn_copy.setIcon(get_colored_icon(get_asset_path(Icons.FILE_TEXT), "#000000"))
        btn_copy.clicked.connect(self._copy_to_clipboard)
        btn_copy.setStyleSheet(
            """
            QPushButton {
                background-color: #e9ecef; border: 1px solid #ced4da;
                padding: 8px 15px; border-radius: 4px; font-weight: 600;
            }
            QPushButton:hover { background-color: #dee2e6; }
        """
        )
        btn_layout.addWidget(btn_copy)

        btn_layout.addStretch()

        # Chiudi
        btn_close = QPushButton("Chiudi")
        btn_close.clicked.connect(self.accept)
        btn_close.setStyleSheet(
            """
            QPushButton {
                background-color: #6c757d; color: white; border: none;
                padding: 8px 15px; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #5c636a; }
        """
        )
        btn_layout.addWidget(btn_close)

        layout.addLayout(btn_layout)

    def _copy_to_clipboard(self):
        cb = QGuiApplication.clipboard()
        cb.setText(self.text_edit.toPlainText())
        QMessageBox.information(self, "Copiato", "Dettagli copiati negli appunti!")


class AuditLogWidget(QWidget):
    """
    Dashboard avanzata per l'Audit Log V2.
    """

    PAGE_SIZE = 50

    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = AuditManager.instance()
        self.current_page = 0
        self.total_logs = 0

        # Timer per Live View
        self.live_timer = QTimer()
        self.live_timer.setInterval(5000)
        self.live_timer.timeout.connect(self._on_live_refresh)

        self._setup_ui()
        self._load_categories()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(10)

        # --- TOP BAR ---
        top_bar = QHBoxLayout()
        info_lbl = QLabel("Dashboard Operazioni")
        info_lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #212529;")
        top_bar.addWidget(info_lbl)

        self.integrity_icon = QLabel()
        self.integrity_icon.setFixedSize(18, 18)
        self.integrity_icon.setScaledContents(True)
        top_bar.addWidget(self.integrity_icon)

        self.integrity_lbl = QLabel("Verifica...")
        self.integrity_lbl.setStyleSheet(
            "color: #6c757d; font-size: 13px; font-weight: 600;"
        )
        top_bar.addWidget(self.integrity_lbl)

        top_bar.addStretch()

        self.live_check = QCheckBox("Live Mode")
        self.live_check.setToolTip("Aggiorna automaticamente ogni 5 secondi")
        self.live_check.stateChanged.connect(self._toggle_live_mode)
        top_bar.addWidget(self.live_check)
        layout.addLayout(top_bar)

        # --- FILTER BAR ---
        filter_frame = QFrame()
        filter_frame.setStyleSheet(
            "background-color: #f8f9fa; border-radius: 6px; border: 1px solid #dee2e6;"
        )
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(10, 10, 10, 10)
        filter_layout.setSpacing(10)

        # Date Range
        self.date_from = CalendarDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-7))
        self.date_from.setDisplayFormat("dd/MM/yyyy")
        self.date_from.setMinimumWidth(160)
        self.date_from.setMaximumWidth(200)

        self.date_to = CalendarDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setDisplayFormat("dd/MM/yyyy")
        self.date_to.setMinimumWidth(160)
        self.date_to.setMaximumWidth(200)

        filter_layout.addWidget(QLabel("Dal:"))
        filter_layout.addWidget(self.date_from)
        filter_layout.addWidget(QLabel("Al:"))
        filter_layout.addWidget(self.date_to)

        # Categoria
        self.cat_combo = QComboBox()
        self.cat_combo.addItem("Tutte")
        self.cat_combo.setFixedWidth(150)
        filter_layout.addWidget(self.cat_combo)

        # Livello
        self.level_combo = QComboBox()
        self.level_combo.addItems(
            ["Tutti", "Info (Low)", "Warning (Med)", "Error (High)"]
        )
        self.level_combo.setFixedWidth(130)
        filter_layout.addWidget(self.level_combo)

        # Search
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Cerca nei log...")
        self.search_edit.setStyleSheet(
            "border: 1px solid #ced4da; border-radius: 4px; padding: 4px;"
        )
        filter_layout.addWidget(self.search_edit)

        # Btn Applica
        apply_btn = QPushButton("Filtra")
        apply_btn.setIcon(get_colored_icon(get_asset_path(Icons.SEARCH), "#ffffff"))
        apply_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #0d6efd; color: white; border: none;
                border-radius: 4px; padding: 6px 12px; font-weight: bold;
            }
            QPushButton:hover { background-color: #0b5ed7; }
        """
        )
        apply_btn.clicked.connect(lambda: self.refresh(reset_page=True))
        filter_layout.addWidget(apply_btn)

        layout.addWidget(filter_frame)

        # --- DATA GRID ---
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_view.verticalHeader().setVisible(False)
        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )
        self.table_view.horizontalHeader().setStretchLastSection(True)
        self.table_view.setStyleSheet(
            """
            QTableView {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                background-color: white;
                gridline-color: #f1f3f5;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 8px;
                border: none;
                font-weight: bold;
                color: #495057;
            }
        """
        )

        self.model = AuditTableModel([])
        self.table_view.setModel(self.model)
        self.table_view.doubleClicked.connect(self._on_row_double_click)
        layout.addWidget(self.table_view)

        # --- PAGINATION ---
        pag_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Precedente")
        self.prev_btn.setEnabled(False)
        self.prev_btn.clicked.connect(self._prev_page)

        self.page_lbl = QLabel("Pagina 1")
        self.page_lbl.setStyleSheet("font-weight: bold;")

        self.next_btn = QPushButton("Successiva")
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self._next_page)

        pag_layout.addWidget(self.prev_btn)
        pag_layout.addStretch()
        pag_layout.addWidget(self.page_lbl)
        pag_layout.addStretch()
        pag_layout.addWidget(self.next_btn)
        layout.addLayout(pag_layout)

    def _load_categories(self):
        cats = self.manager.get_categories()
        self.cat_combo.addItems(cats)

    def _toggle_live_mode(self, state):
        if state == Qt.CheckState.Checked.value:
            self.refresh(reset_page=True)
            self.live_timer.start()
            self.date_from.setEnabled(False)
            self.date_to.setEnabled(False)
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
        else:
            self.live_timer.stop()
            self.date_from.setEnabled(True)
            self.date_to.setEnabled(True)
            self.refresh()

    def _on_live_refresh(self):
        self.refresh(reset_page=True)

    def refresh(self, reset_page=False):
        if reset_page:
            self.current_page = 0

        start = self.date_from.date().toPyDate()
        end = self.date_to.date().toPyDate()
        start_dt = datetime.combine(start, datetime.min.time())
        end_dt = datetime.combine(end, datetime.max.time())

        cat = self.cat_combo.currentText()
        lvl_idx = self.level_combo.currentIndex()
        levels = None
        if lvl_idx == 1:
            levels = ["low"]
        elif lvl_idx == 2:
            levels = ["medium"]
        elif lvl_idx == 3:
            levels = ["high"]

        search = self.search_edit.text().strip()

        logs, total = self.manager.get_filtered_logs(
            start_date=start_dt,
            end_date=end_dt,
            category=cat,
            levels=levels,
            search_text=search,
            limit=self.PAGE_SIZE,
            offset=self.current_page * self.PAGE_SIZE,
        )

        self.total_logs = total
        self.model.update_data(logs)

        # Smart Resize
        self.table_view.resizeColumnsToContents()
        for i in range(self.model.columnCount() - 1):
            w = self.table_view.columnWidth(i)
            # Aumentiamo il buffer per leggibilità
            self.table_view.setColumnWidth(i, int(w * 1.15) + 15)

        self.table_view.horizontalHeader().setSectionResizeMode(
            self.model.columnCount() - 1, QHeaderView.ResizeMode.Stretch
        )

        self._update_pagination_ui()
        if self.current_page == 0:
            self._check_integrity()

    def _update_pagination_ui(self):
        total_pages = (self.total_logs + self.PAGE_SIZE - 1) // self.PAGE_SIZE
        if total_pages < 1:
            total_pages = 1
        disp = self.current_page + 1
        self.page_lbl.setText(
            f"Pagina {disp} di {total_pages} (Tot: {self.total_logs})"
        )
        self.prev_btn.setEnabled(self.current_page > 0)
        self.next_btn.setEnabled(disp < total_pages)

    def _next_page(self):
        self.current_page += 1
        self.refresh()

    def _prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.refresh()

    def _check_integrity(self):
        valid = self.manager.verify_integrity()
        if valid:
            self.integrity_icon.setPixmap(
                get_colored_icon(get_asset_path(Icons.SHIELD), "#198754").pixmap(18, 18)
            )
            self.integrity_lbl.setText("Integro")
            self.integrity_lbl.setStyleSheet("color: #198754; font-weight: bold;")
        else:
            self.integrity_icon.setPixmap(
                get_colored_icon(
                    get_asset_path(Icons.ALERT_TRIANGLE), "#dc3545"
                ).pixmap(18, 18)
            )
            # Fallimento atteso per vecchi record dopo update schema
            self.integrity_lbl.setText("Legacy/Manomesso")
            self.integrity_lbl.setStyleSheet("color: #dc3545; font-weight: bold;")

    def _on_row_double_click(self, index):
        log = self.model.get_log_at(index.row())
        if log:
            AuditDetailDialog(log, self).exec()


class NotificationsPanel(QWidget):
    """Pannello principale delle notifiche con schede Audit."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_filter = "all"
        self.manager = NotificationManager.instance()
        self._setup_ui()
        self.manager.notifications_updated.connect(self.refresh_notifications)
        self.refresh_notifications()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        self.tabs = QTabWidget()
        self.tabs.setProperty("class", "Level2Tabs")
        main_layout.addWidget(self.tabs)

        # Tab Notifiche
        self.notif_tab = QWidget()
        nl = QVBoxLayout(self.notif_tab)
        nl.setContentsMargins(0, 10, 0, 0)

        tb = QHBoxLayout()
        self.btn_all = QPushButton("Tutti")
        self.btn_all.setCheckable(True)
        self.btn_all.setChecked(True)
        self.btn_all.clicked.connect(lambda: self._set_filter("all"))
        self._style_filter_btn(self.btn_all)
        tb.addWidget(self.btn_all)

        self.btn_unread = QPushButton("Da leggere")
        self.btn_unread.setCheckable(True)
        self.btn_unread.clicked.connect(lambda: self._set_filter("unread"))
        self._style_filter_btn(self.btn_unread)
        tb.addWidget(self.btn_unread)

        self.btn_errors = QPushButton("Solo Errori")
        self.btn_errors.setCheckable(True)
        self.btn_errors.clicked.connect(lambda: self._set_filter("errors"))
        self._style_filter_btn(self.btn_errors)
        tb.addWidget(self.btn_errors)

        tb.addStretch()

        mark_read = ModernButton(
            "Segna letti",
            variant=ModernButton.Variant.GHOST,
            size=ModernButton.Size.SMALL,
        )
        mark_read.setMinimumWidth(120)
        mark_read.setFixedHeight(40)
        mark_read.clicked.connect(self.manager.mark_all_as_read)
        tb.addWidget(mark_read)

        clear = ModernButton(
            "Svuota", variant=ModernButton.Variant.DANGER, size=ModernButton.Size.SMALL
        )
        clear.setMinimumWidth(120)
        clear.setFixedHeight(40)
        clear.clicked.connect(self._clear_notifications)
        tb.addWidget(clear)
        nl.addLayout(tb)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.addStretch()
        self.scroll.setWidget(self.scroll_content)
        nl.addWidget(self.scroll)

        self.tabs.addTab(
            self.notif_tab,
            get_colored_icon(get_asset_path(Icons.BELL), "#546E7A"),
            "Notifiche",
        )

        # Tab Audit
        self.audit_tab = AuditLogWidget()
        self.tabs.addTab(
            self.audit_tab,
            get_colored_icon(get_asset_path(Icons.SHIELD), "#546E7A"),
            "Audit",
        )
        self.tabs.currentChanged.connect(self._on_tab_changed)

    def _on_tab_changed(self, index):
        if self.tabs.tabText(index) == "Audit":
            self.audit_tab.refresh()

    def _style_filter_btn(self, btn):
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(45)
        btn.setMinimumWidth(150)
        btn.setStyleSheet(
            """
            QPushButton {
                background-color: white; border: 1px solid #ced4da;
                border-radius: 22px; color: #495057; font-weight: bold;
                font-size: 14px; padding: 0 15px;
            }
            QPushButton:checked {
                background-color: #0d6efd; color: white; border: 1px solid #0d6efd;
            }
            QPushButton:hover:!checked { background-color: #e9ecef; }
        """
        )

    def _set_filter(self, mode):
        self.current_filter = mode
        self.btn_all.setChecked(mode == "all")
        self.btn_unread.setChecked(mode == "unread")
        self.btn_errors.setChecked(mode == "errors")
        self.refresh_notifications()

    def _clear_notifications(self):
        if (
            QMessageBox.question(self, "Conferma", "Vuoi svuotare i messaggi?")
            == QMessageBox.StandardButton.Yes
        ):
            self.manager.clear_all()

    def refresh_notifications(self):
        while self.scroll_layout.count() > 1:
            w = self.scroll_layout.takeAt(0).widget()
            if w:
                w.deleteLater()

        unread = self.current_filter == "unread"
        notifs = self.manager.get_notifications(unread)
        if self.current_filter == "errors":
            notifs = [n for n in notifs if n.get("level") == "error"]

        if not notifs:
            lbl = QLabel("Nessuna notifica")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: #adb5bd; font-size: 16px; margin-top: 50px;")
            self.scroll_layout.insertWidget(0, lbl)
        else:
            for n in notifs:
                self.scroll_layout.insertWidget(
                    self.scroll_layout.count() - 1, NotificationItem(n)
                )
