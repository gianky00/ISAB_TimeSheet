"""
Bot TS - Styles and Themes
Defines the visual styles for the application (Light/Dark mode).
"""

LIGHT_THEME = """
QMainWindow {
    background-color: #f5f5f5;
}
QWidget {
    font-family: "Segoe UI", sans-serif;
}
QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #1976D2;
}
QPushButton:pressed {
    background-color: #0D47A1;
}
QPushButton:disabled {
    background-color: #BDBDBD;
}
QTableWidget, QTableView {
    background-color: white;
    gridline-color: #E0E0E0;
    selection-background-color: #BBDEFB;
    selection-color: #000000;
    border: 1px solid #E0E0E0;
}
QTableWidget::item:selected, QTableView::item:selected {
    background-color: #BBDEFB;
    color: #212121;
}
QHeaderView::section {
    background-color: #E0E0E0;
    padding: 4px;
    border: 1px solid #BDBDBD;
    font-weight: bold;
}
QLineEdit, QDateEdit, QComboBox, QSpinBox, QTimeEdit, QListView {
    padding: 6px;
    border: 1px solid #BDBDBD;
    border-radius: 4px;
    background-color: white;
    color: black;
    selection-background-color: #2196F3;
    selection-color: white;
}
QComboBox QAbstractItemView {
    background-color: white;
    color: black;
    selection-background-color: #2196F3;
}
QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
    border: 2px solid #2196F3;
}
QLabel {
    color: #212121;
}
QGroupBox {
    border: 1px solid #BDBDBD;
    border-radius: 4px;
    margin-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}
QScrollBar:vertical {
    border: none;
    background: #F5F5F5;
    width: 12px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background: #BDBDBD;
    min-height: 20px;
    border-radius: 6px;
}
QScrollBar::handle:vertical:hover {
    background: #9E9E9E;
}
"""

DARK_THEME = """
QMainWindow, QWidget {
    background-color: #121212;
    color: #ffffff;
    font-family: "Segoe UI", sans-serif;
}
QPushButton {
    background-color: #0D47A1; /* Darker Blue */
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #1565C0;
}
QPushButton:pressed {
    background-color: #0D47A1;
}
QPushButton:disabled {
    background-color: #424242;
    color: #757575;
}
QTableWidget, QTableView {
    background-color: #1E1E1E;
    color: #ffffff;
    gridline-color: #424242;
    selection-background-color: #0D47A1;
    selection-color: #ffffff;
    border: 1px solid #424242;
}
QTableWidget::item:selected, QTableView::item:selected {
    background-color: #0D47A1;
}
QHeaderView::section {
    background-color: #333333;
    color: #ffffff;
    padding: 4px;
    border: 1px solid #424242;
    font-weight: bold;
}
QLineEdit, QDateEdit, QComboBox {
    padding: 6px;
    border: 1px solid #424242;
    border-radius: 4px;
    background-color: #333333;
    color: #ffffff;
    selection-background-color: #0D47A1;
}
QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
    border: 2px solid #2196F3;
}
QLabel {
    color: #ffffff;
}
QGroupBox {
    border: 1px solid #424242;
    border-radius: 4px;
    margin-top: 10px;
}
QGroupBox::title {
    color: #ffffff;
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}
QScrollBar:vertical {
    border: none;
    background: #121212;
    width: 12px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background: #424242;
    min-height: 20px;
    border-radius: 6px;
}
QScrollBar::handle:vertical:hover {
    background: #616161;
}
/* Ensure icons are visible (might need inversion or specific icons for dark mode) */
"""

def apply_theme(app, theme_name="light"):
    if theme_name.lower() == "dark":
        app.setStyleSheet(DARK_THEME)
    else:
        app.setStyleSheet(LIGHT_THEME)
