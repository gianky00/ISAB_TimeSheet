"""
SyncroJob - Notifications Panel
Pannello per la visualizzazione delle notifiche.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.core.audit_manager import AuditManager
from src.core.notification_manager import NotificationManager
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.notification_item import NotificationItem


# Force file update - Refreshed
class AuditLogWidget(QWidget):
    """Widget avanzato per l'Audit Log con validazione integrità."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = AuditManager()
        self._setup_ui()
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(15)

        # Toolbar
        toolbar = QHBoxLayout()

        info_lbl = QLabel("Registro Operazioni (Audit Trail)")
        info_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #212529;")
        toolbar.addWidget(info_lbl)

        self.integrity_lbl = QLabel("🛡️ Verifica in corso...")
        self.integrity_lbl.setStyleSheet("color: #6c757d; font-size: 13px; font-weight: bold;")
        toolbar.addWidget(self.integrity_lbl)

        toolbar.addStretch()

        # Retention Info
        retention_lbl = QLabel("Policy: 90 Giorni")
        retention_lbl.setStyleSheet("color: #adb5bd; font-size: 12px; margin-right: 10px;")
        toolbar.addWidget(retention_lbl)

        refresh_btn = QPushButton("🔄 Aggiorna e Valida")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #0b5ed7; }
        """
        )
        refresh_btn.clicked.connect(self.refresh)
        toolbar.addWidget(refresh_btn)

        layout.addLayout(toolbar)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Data/Ora", "Utente", "Operazione", "Entità", "Parametri", "Esito"]
        )

        self.table.setStyleSheet(
            """
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
                gridline-color: #f8f9fa;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 12px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
                color: #495057;
            }
        """
        )

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Timestamp
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # User
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Action
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Entity
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Params
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Status

        layout.addWidget(self.table)

    def refresh(self):
        """Ricarica i log e applica colori basati sulla severità."""
        self._update_integrity_ui(self.manager.verify_integrity())

        logs = self.manager.get_logs(limit=200)
        self.table.setRowCount(0)
        self._populate_table(logs)

    def _update_integrity_ui(self, is_valid: bool):
        if is_valid:
            self.integrity_lbl.setText("✅ Database Integro (Certificato)")
            self.integrity_lbl.setStyleSheet("color: #198754; font-size: 13px; font-weight: bold;")
        else:
            self.integrity_lbl.setText("⚠️ MANOMISSIONE RILEVATA!")
            self.integrity_lbl.setStyleSheet("color: #dc3545; font-size: 13px; font-weight: bold;")

    def _populate_table(self, logs):
        for log in logs:
            row = self.table.rowCount()
            self.table.insertRow(row)

            items = self._create_row_items(log)
            self._apply_row_styles(items, log)

            for col, item in enumerate(items):
                self.table.setItem(row, col, item)

    def _create_row_items(self, log) -> list[QTableWidgetItem]:
        def clean(v):
            s = str(v).strip()
            return "-" if not v or s.lower() == "none" or s == "" else s

        ts = self._format_log_timestamp(log.get("timestamp"))
        params = clean(log.get("params")) if log.get("params") != "{}" else "-"

        return [
            QTableWidgetItem(ts),
            QTableWidgetItem(clean(log.get("user_id"))),
            QTableWidgetItem(clean(log.get("action"))),
            QTableWidgetItem(clean(log.get("entity"))),
            QTableWidgetItem(params),
            QTableWidgetItem(clean(log.get("status")).upper()),
        ]

    def _format_log_timestamp(self, ts_raw) -> str:
        try:
            from datetime import datetime

            dt = datetime.fromisoformat(ts_raw)
            return dt.strftime("%d/%m/%y %H:%M")
        except Exception:
            return str(ts_raw) if ts_raw else "-"

    def _apply_row_styles(self, items, log):
        sev = str(log.get("severity", "")).lower()
        status = str(log.get("status", "")).lower()

        # 1. Background (Severity)
        bg = QColor("#fff5f5") if sev == "high" else QColor("#fff9f0") if sev == "medium" else None
        if bg:
            for it in items:
                it.setBackground(bg)

        # 2. Action Font (Bold)
        items[2].setFont(QFont("Arial", 9, QFont.Weight.Bold))

        # 3. Status Color (Foreground)
        if status == "error" or sev == "high":
            items[5].setForeground(QColor("#dc3545"))
        elif status == "warning" or sev == "medium":
            items[5].setForeground(QColor("#fd7e14"))
        else:
            items[5].setForeground(QColor("#198754"))
        items[5].setTextAlignment(Qt.AlignmentFlag.AlignCenter)


class NotificationsPanel(QWidget):
    """Pannello principale delle notifiche con schede Audit."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_filter = "all"  # 'all', 'unread', 'errors'
        self.manager = NotificationManager.instance()

        self._setup_ui()

        # Connect signals
        self.manager.notifications_updated.connect(self.refresh_notifications)

        self.refresh_notifications()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header Area
        header_layout = QHBoxLayout()
        title = QLabel("🔔 Centro Notifiche & Audit")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #212529;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        main_layout.addLayout(header_layout)

        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(
            """
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                padding: 10px 25px;
                margin-right: 2px;
                color: #495057;
                font-weight: bold;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
                color: #0d6efd;
            }
        """
        )
        main_layout.addWidget(self.tabs)

        # --- TAB 1: MESSAGGI ---
        self.notif_tab = QWidget()
        notif_layout = QVBoxLayout(self.notif_tab)
        notif_layout.setContentsMargins(15, 15, 15, 15)

        # Toolbar Notifiche
        notif_toolbar = QHBoxLayout()
        self.btn_all = QPushButton("Tutti")
        self.btn_all.setCheckable(True)
        self.btn_all.setChecked(True)
        self.btn_all.clicked.connect(lambda: self._set_filter("all"))
        self._style_filter_btn(self.btn_all)
        notif_toolbar.addWidget(self.btn_all)

        self.btn_unread = QPushButton("Da leggere")
        self.btn_unread.setCheckable(True)
        self.btn_unread.clicked.connect(lambda: self._set_filter("unread"))
        self._style_filter_btn(self.btn_unread)
        notif_toolbar.addWidget(self.btn_unread)

        self.btn_errors = QPushButton("Solo Errori")
        self.btn_errors.setCheckable(True)
        self.btn_errors.clicked.connect(lambda: self._set_filter("errors"))
        self._style_filter_btn(self.btn_errors)
        notif_toolbar.addWidget(self.btn_errors)

        notif_toolbar.addStretch()

        mark_read_btn = ModernButton(
            "Segna letti",
            variant=ModernButton.Variant.GHOST,
            size=ModernButton.Size.SMALL,
        )
        mark_read_btn.setMinimumWidth(120)
        mark_read_btn.setFixedHeight(40)
        mark_read_btn.clicked.connect(self._mark_all_read)
        notif_toolbar.addWidget(mark_read_btn)

        clear_btn = ModernButton("Svuota", variant=ModernButton.Variant.DANGER, size=ModernButton.Size.SMALL)
        clear_btn.setMinimumWidth(120)
        clear_btn.setFixedHeight(40)
        clear_btn.setToolTip("Elimina definitivamente i messaggi (l'audit rimarrà intatto)")
        clear_btn.clicked.connect(self._clear_notifications)
        notif_toolbar.addWidget(clear_btn)

        notif_layout.addLayout(notif_toolbar)

        # Scroll Area Notifiche
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.addStretch()
        self.scroll.setWidget(self.scroll_content)
        notif_layout.addWidget(self.scroll)

        self.tabs.addTab(self.notif_tab, "Messaggi Operativi")

        # --- TAB 2: AUDIT ---
        self.audit_tab = AuditLogWidget()
        self.tabs.addTab(self.audit_tab, "Registro Attività (Audit)")

        # Refresh audit when tab selected
        self.tabs.currentChanged.connect(self._on_tab_changed)

    def _on_tab_changed(self, index):
        if self.tabs.tabText(index) == "Registro Attività (Audit)":
            self.audit_tab.refresh()

    def _clear_notifications(self):
        """Elimina tutte le notifiche utente."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Conferma")
        msg_box.setText("Vuoi svuotare i messaggi? L'Audit Log non verrà toccato.")
        msg_box.setIcon(QMessageBox.Icon.Question)

        # Pulsanti Custom
        yes_btn = msg_box.addButton("Sì", QMessageBox.ButtonRole.YesRole)
        msg_box.addButton("No", QMessageBox.ButtonRole.NoRole)

        # Stile leggibile
        msg_box.setStyleSheet(
            """
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: #212529;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 15px;
                font-weight: bold;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
            QPushButton[text="No"] {
                background-color: #6c757d;
            }
            QPushButton[text="No"]:hover {
                background-color: #5c636a;
            }
        """
        )

        msg_box.exec()

        if msg_box.clickedButton() == yes_btn:
            self.manager.clear_all()

    def _style_filter_btn(self, btn):
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(45)
        btn.setMinimumWidth(150)
        btn.setStyleSheet(
            """
            QPushButton {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 22px;
                color: #495057;
                font-weight: bold;
                font-size: 14px;
                padding: 0 15px;
            }
            QPushButton:checked {
                background-color: #0d6efd;
                color: white;
                border: 1px solid #0d6efd;
            }
            QPushButton:hover:!checked {
                background-color: #e9ecef;
            }
        """
        )

    def _set_filter(self, mode):
        self.current_filter = mode
        self.btn_all.setChecked(mode == "all")
        self.btn_unread.setChecked(mode == "unread")
        self.btn_errors.setChecked(mode == "errors")
        self.refresh_notifications()

    def _mark_all_read(self):
        self.manager.mark_all_as_read()

    def refresh_notifications(self):
        """Ricarica la lista notifiche."""
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        is_unread_mode = self.current_filter == "unread"
        notifications = self.manager.get_notifications(is_unread_mode)

        if self.current_filter == "errors":
            notifications = [n for n in notifications if n.get("level") == "error"]

        if not notifications:
            empty_lbl = QLabel("Nessuna notifica")
            empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_lbl.setStyleSheet("color: #adb5bd; font-size: 16px; margin-top: 50px;")
            self.scroll_layout.insertWidget(0, empty_lbl)
        else:
            for n in notifications:
                item = NotificationItem(n)
                self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, item)
