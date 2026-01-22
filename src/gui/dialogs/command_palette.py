from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem,
    QLabel, QGraphicsDropShadowEffect, QWidget, QHBoxLayout, QFrame,
    QApplication, QScrollBar
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QColor, QFont, QIcon, QPainter
from src.core.constants import Icons
from src.utils.helpers import get_colored_icon, get_asset_path

class CommandPaletteDialog(QDialog):
    """
    Dialogo 'Quick Open' stile VSCode.
    - Frameless
    - Centered Top
    - Input Field styled
    - List styled with icons and shortcuts
    """
    
    def __init__(self, parent=None, commands=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(700, 500)  # Slightly larger
        
        self.commands = commands or []
        
        self._setup_ui()
        self._populate_list(self.commands)
        self.search_bar.setFocus()

    def _setup_ui(self):
        # Container Principale (Shadowed)
        self.container = QWidget(self)
        self.container.setGeometry(10, 10, 680, 480)
        
        # VSCode Style Colors
        bg_color = "#1e1e1e"  # Darker background
        input_bg = "#3c3c3c"
        text_color = "#cccccc"
        sel_bg = "#04395e"    # Deep blue selection
        sel_text = "#ffffff"
        border_color = "#454545"

        # MAIN CONTAINER STYLE - Scoped carefully
        self.container.setObjectName("MainContainer")
        self.container.setStyleSheet(f"""
            QWidget#MainContainer {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 6px;
                color: {text_color};
            }}
            QLabel {{
                border: none;
                background: transparent;
            }}
        """)
        
        # Shadow Effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.container.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Search Bar Area ---
        search_container = QWidget()
        search_container.setStyleSheet(f"""
            background-color: {input_bg}; 
            border-top-left-radius: 6px; 
            border-top-right-radius: 6px; 
            padding: 5px;
            border-bottom: 1px solid {border_color};
        """)
        search_layout = QVBoxLayout(search_container)
        search_layout.setContentsMargins(8, 8, 8, 5)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("> Type a command...")
        self.search_bar.setStyleSheet(f"""
            QLineEdit {{
                background-color: #3c3c3c;
                color: {text_color};
                border: 1px solid transparent;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                padding: 4px;
            }}
            QLineEdit:focus {{
                border: 1px solid #007fd4; /* VSCode focus blue */
                background-color: #252526;
            }}
        """)
        self.search_bar.textChanged.connect(self._filter_list)
        self.search_bar.installEventFilter(self)
        
        search_layout.addWidget(self.search_bar)
        layout.addWidget(search_container)

        # --- List Widget ---
        self.list_widget = QListWidget()
        self.list_widget.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.list_widget.setStyleSheet(f"""
            QListWidget {{
                background-color: {bg_color};
                border: none;
                border-bottom-left-radius: 6px;
                border-bottom-right-radius: 6px;
                outline: none;
            }}
            QListWidget::item {{
                padding: 0px;
                border: none;
                color: {text_color};
            }}
            QListWidget::item:selected {{
                background-color: {sel_bg};
                color: {sel_text};
                border: none;
            }}
            QListWidget::item:hover {{
                background-color: #2a2d2e;
            }}
            
            /* Scrollbar Styling */
            QScrollBar:vertical {{
                border: none;
                background: {bg_color};
                width: 10px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: #424242;
                min-height: 20px;
                border-radius: 5px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: #4f4f4f;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        self.list_widget.itemActivated.connect(self._execute_selected)
        self.list_widget.clicked.connect(self._execute_selected)
        layout.addWidget(self.list_widget)

    def eventFilter(self, obj, event):
        if obj == self.search_bar and event.type() == event.Type.KeyPress:
            key = event.key()
            if key == Qt.Key.Key_Down:
                idx = self.list_widget.currentRow()
                if idx < self.list_widget.count() - 1:
                    self.list_widget.setCurrentRow(idx + 1)
                return True
            elif key == Qt.Key.Key_Up:
                idx = self.list_widget.currentRow()
                if idx > 0:
                    self.list_widget.setCurrentRow(idx - 1)
                return True
            elif key == Qt.Key.Key_Return or key == Qt.Key.Key_Enter:
                self._execute_selected()
                return True
            elif key == Qt.Key.Key_Escape:
                self.reject()
                return True
        return super().eventFilter(obj, event)

    def _populate_list(self, items):
        self.list_widget.clear()
        for cmd in items:
            self._add_item(cmd)
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def _add_item(self, cmd):
        # Widget contenitore per l'item
        item = QListWidgetItem(self.list_widget)
        item.setSizeHint(QSize(0, 50)) 
        
        widget = QWidget()
        widget.setStyleSheet("background: transparent; border: none;") # CRUCIAL: No border on container
        h_layout = QHBoxLayout(widget)
        h_layout.setContentsMargins(10, 5, 10, 5)
        h_layout.setSpacing(15)
        
        # Icon
        icon_lbl = QLabel()
        icon_lbl.setFixedSize(20, 20)
        if cmd.get('icon'):
            pm = get_colored_icon(get_asset_path(cmd['icon']), "#cccccc").pixmap(20, 20)
            icon_lbl.setPixmap(pm)
        h_layout.addWidget(icon_lbl)
        
        # Text Stack
        txt_layout = QVBoxLayout()
        txt_layout.setSpacing(2)
        txt_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        lbl_main = QLabel(cmd['label'])
        lbl_main.setStyleSheet("font-size: 14px; font-weight: bold; color: #e1e1e1; border: none;")
        txt_layout.addWidget(lbl_main)
        
        if cmd.get('desc'):
            lbl_desc = QLabel(cmd['desc'])
            lbl_desc.setStyleSheet("font-size: 12px; color: #858585; border: none;")
            txt_layout.addWidget(lbl_desc)
            
        h_layout.addLayout(txt_layout)
        h_layout.addStretch()
        
        # Shortcut Label
        if cmd.get('shortcut'):
            sc_lbl = QLabel(cmd['shortcut'])
            sc_lbl.setStyleSheet("color: #858585; font-size: 12px; font-family: monospace; border: none;")
            h_layout.addWidget(sc_lbl)

        # Set widget
        item.setData(Qt.ItemDataRole.UserRole, cmd)
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)

    def _filter_list(self, text):
        search = text.lower()
        self.list_widget.clear()
        
        # Filter logic: Title or Description contains text
        filtered = [c for c in self.commands if search in c['label'].lower() or search in c.get('desc', '').lower()]
        
        # Limit results for performance if list is huge (e.g. 100)
        for cmd in filtered:
            self._add_item(cmd)
            
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def _execute_selected(self):
        item = self.list_widget.currentItem()
        if not item: return
        cmd = item.data(Qt.ItemDataRole.UserRole)
        if cmd and cmd.get('action'):
            self.accept()
            QTimer.singleShot(50, cmd['action'])