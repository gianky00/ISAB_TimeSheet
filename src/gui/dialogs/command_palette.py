from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem,
    QLabel, QGraphicsDropShadowEffect, QWidget, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QColor, QFont, QIcon
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
        self.setFixedSize(650, 450)
        
        self.commands = commands or []
        
        self._setup_ui()
        self._populate_list(self.commands)
        self.search_bar.setFocus()

    def _setup_ui(self):
        # Container Principale (Shadowed)
        self.container = QWidget(self)
        self.container.setGeometry(10, 10, 630, 430)
        
        # VSCode Style Colors (Dark/Light hybrid fit or strict VSCode Dark)
        # User said "stile perfetto vscode". Let's go with the classic Dark theme look 
        # as it's the most recognizable "VSCode Style", serving as a spotlight overlay.
        bg_color = "#252526"
        input_bg = "#3c3c3c"
        text_color = "#cccccc"
        sel_bg = "#094771" # VSCode selection blue
        sel_text = "#ffffff"
        border_color = "#454545"

        self.container.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 6px;
                color: {text_color};
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
        search_container.setStyleSheet(f"background-color: {input_bg}; border-top-left-radius: 6px; border-top-right-radius: 6px; padding: 5px;")
        search_layout = QVBoxLayout(search_container)
        search_layout.setContentsMargins(10, 10, 10, 5)
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("> Type a command...")
        self.search_bar.setStyleSheet(f"""
            QLineEdit {{
                background-color: #3c3c3c;
                color: {text_color};
                border: 1px solid #3c3c3c;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                padding: 4px;
            }}
            QLineEdit:focus {{
                border: 1px solid #007fd4; /* VSCode focus blue */
            }}
        """)
        self.search_bar.textChanged.connect(self._filter_list)
        self.search_bar.installEventFilter(self)
        
        search_layout.addWidget(self.search_bar)
        layout.addWidget(search_container)

        # --- List Widget ---
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet(f"""
            QListWidget {{
                background-color: {bg_color};
                border: none;
                border-top: 1px solid {border_color};
                outline: none;
            }}
            QListWidget::item {{
                padding: 5px 10px;
                height: 30px;
                color: {text_color};
            }}
            QListWidget::item:selected {{
                background-color: {sel_bg};
                color: {sel_text};
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
        # Creiamo un widget custom per l'item per avere layout icona - testo - shortcut
        item = QListWidgetItem(self.list_widget)
        item.setSizeHint(QSize(0, 42)) # Altezza fissa
        
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        h_layout = QHBoxLayout(widget)
        h_layout.setContentsMargins(5, 0, 5, 0)
        h_layout.setSpacing(10)
        
        # Icon (White/Grey for dark theme)
        icon_lbl = QLabel()
        if cmd.get('icon'):
            pm = get_colored_icon(get_asset_path(cmd['icon']), "#cccccc").pixmap(16, 16)
            icon_lbl.setPixmap(pm)
        h_layout.addWidget(icon_lbl)
        
        # Text Stack (Label + Desc) -> In VSCode usually side by side or just Label
        # We will do: Label ....... Desc/Shortcut
        
        txt_layout = QVBoxLayout()
        txt_layout.setSpacing(2)
        txt_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        lbl_main = QLabel(cmd['label'])
        lbl_main.setStyleSheet("font-size: 13px; font-weight: bold; color: #cccccc;")
        txt_layout.addWidget(lbl_main)
        
        if cmd.get('desc'):
            lbl_desc = QLabel(cmd['desc'])
            lbl_desc.setStyleSheet("font-size: 11px; color: #858585;")
            txt_layout.addWidget(lbl_desc)
            
        h_layout.addLayout(txt_layout)
        h_layout.addStretch()
        
        # Shortcut (fake styling)
        if cmd.get('shortcut'):
            sc_lbl = QLabel(cmd['shortcut'])
            sc_lbl.setStyleSheet("color: #858585; font-size: 12px;")
            h_layout.addWidget(sc_lbl)

        # Set widget
        item.setData(Qt.ItemDataRole.UserRole, cmd)
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)

    def _filter_list(self, text):
        search = text.lower()
        self.list_widget.clear()
        # Non-Strict Filter
        filtered = [c for c in self.commands if search in c['label'].lower() or search in c.get('desc', '').lower()]
        
        for cmd in filtered[:15]:
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
