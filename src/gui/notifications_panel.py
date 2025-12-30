"""
Bot TS - Notifications Panel
Pannello per la visualizzazione delle notifiche.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPalette

from src.core.notification_manager import NotificationManager
from src.gui.widgets.modern_button import ModernButton

class NotificationItem(QFrame):
    """Card per singola notifica."""
    
    def __init__(self, notification, parent=None):
        super().__init__(parent)
        self.notification = notification
        self.notification_id = notification['id']
        
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self._setup_ui()
        self._update_style()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(5)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Icon/Indicator
        self.indicator = QLabel("●")
        self.indicator.setStyleSheet(self._get_indicator_color())
        header_layout.addWidget(self.indicator)
        
        # Title
        title_lbl = QLabel(self.notification['title'])
        title_lbl.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(title_lbl)
        
        header_layout.addStretch()
        
        # Time
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(self.notification['timestamp'])
            time_str = dt.strftime("%d/%m %H:%M")
        except:
            time_str = ""
            
        time_lbl = QLabel(time_str)
        time_lbl.setStyleSheet("color: #6c757d; font-size: 12px;")
        header_layout.addWidget(time_lbl)
        
        layout.addLayout(header_layout)
        
        # Message
        msg_lbl = QLabel(self.notification['message'])
        msg_lbl.setWordWrap(True)
        msg_lbl.setStyleSheet("color: #495057; margin-top: 5px;")
        layout.addWidget(msg_lbl)
        
        # Actions (only if unread)
        if not self.notification['read']:
            action_layout = QHBoxLayout()
            action_layout.addStretch()
            
            mark_read_btn = QPushButton("Segna come letta")
            mark_read_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            mark_read_btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    color: #0d6efd;
                    font-weight: bold;
                }
                QPushButton:hover {
                    text-decoration: underline;
                }
            """)
            mark_read_btn.clicked.connect(self._mark_as_read)
            action_layout.addWidget(mark_read_btn)
            
            layout.addLayout(action_layout)
            
    def _get_indicator_color(self):
        level = self.notification.get('level', 'info')
        colors = {
            'info': '#0d6efd',
            'success': '#198754',
            'warning': '#ffc107',
            'error': '#dc3545'
        }
        color = colors.get(level, '#0d6efd')
        return f"color: {color}; font-size: 16px;"

    def _update_style(self):
        if self.notification['read']:
            self.setStyleSheet("""
                NotificationItem {
                    background-color: white;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                }
            """)
            self.indicator.setVisible(False)
        else:
            self.setStyleSheet("""
                NotificationItem {
                    background-color: #f8f9fa;
                    border: 1px solid #ced4da;
                    border-left: 4px solid #0d6efd;
                    border-radius: 8px;
                }
            """)

    def _mark_as_read(self):
        NotificationManager.instance().mark_as_read(self.notification_id)


class NotificationsPanel(QWidget):
    """Pannello principale delle notifiche."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_unread = False
        
        self._setup_ui()
        
        # Connect signals
        self.manager = NotificationManager.instance()
        self.manager.notifications_updated.connect(self.refresh)
        
        self.refresh()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header Area
        header = QHBoxLayout()
        
        title = QLabel("🔔 Centro Notifiche")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #212529;")
        header.addWidget(title)
        
        header.addStretch()
        
        # Filter Buttons
        self.btn_all = QPushButton("Tutte")
        self.btn_all.setCheckable(True)
        self.btn_all.setChecked(True)
        self.btn_all.clicked.connect(lambda: self._set_filter(False))
        self._style_filter_btn(self.btn_all)
        header.addWidget(self.btn_all)
        
        self.btn_unread = QPushButton("Non lette")
        self.btn_unread.setCheckable(True)
        self.btn_unread.clicked.connect(lambda: self._set_filter(True))
        self._style_filter_btn(self.btn_unread)
        header.addWidget(self.btn_unread)
        
        header.addSpacing(20)
        
        # Clear Button
        clear_btn = ModernButton("Segna tutto come letto", variant=ModernButton.Variant.GHOST, size=ModernButton.Size.SMALL)
        clear_btn.clicked.connect(self._mark_all_read)
        header.addWidget(clear_btn)
        
        layout.addLayout(header)
        
        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.addStretch() # Push items to top
        
        self.scroll.setWidget(self.scroll_content)
        layout.addWidget(self.scroll)

    def _style_filter_btn(self, btn):
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(35)
        btn.setMinimumWidth(80)
        btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 17px;
                color: #495057;
                font-weight: 500;
            }
            QPushButton:checked {
                background-color: #0d6efd;
                color: white;
                border: 1px solid #0d6efd;
            }
            QPushButton:hover:!checked {
                background-color: #e9ecef;
            }
        """)

    def _set_filter(self, unread_only):
        self.filter_unread = unread_only
        
        # Update buttons state
        self.btn_all.setChecked(not unread_only)
        self.btn_unread.setChecked(unread_only)
        
        self.refresh()

    def _mark_all_read(self):
        self.manager.mark_all_as_read()

    def refresh(self):
        """Ricarica la lista notifiche."""
        # Clear existing items (except the stretch at the end)
        while self.scroll_layout.count() > 1:
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        notifications = self.manager.get_notifications(self.filter_unread)
        
        if not notifications:
            # Empty State
            empty_lbl = QLabel("Nessuna notifica da mostrare")
            empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_lbl.setStyleSheet("color: #adb5bd; font-size: 16px; margin-top: 50px;")
            self.scroll_layout.insertWidget(0, empty_lbl)
        else:
            for n in notifications:
                item = NotificationItem(n)
                self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, item)

