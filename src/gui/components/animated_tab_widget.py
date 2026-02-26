"""
SyncroJob - Animated Tab Widget
Componente universale con animazioni premium e supporto TabPosition.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QTabBar, QTabWidget, QVBoxLayout, QWidget

from src.gui.components.animated_stack import SlidingStackedWidget


class AnimatedTabWidget(QWidget):
    """
    Sostituto moderno di QTabWidget con transizioni Snapshot-Fade.
    Design pulito focalizzato sulla performance e fluidità.
    """

    currentChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        # Tab Bar personalizzata
        self.tab_bar = QTabBar()
        self.tab_bar.setDrawBase(False)
        self.tab_bar.setExpanding(False)
        self.tab_bar.setDocumentMode(True)
        self.tab_bar.setStyleSheet(self._get_default_style())
        self.tab_bar.currentChanged.connect(self._on_tab_bar_changed)

        # Stack animato
        self.stack = SlidingStackedWidget()
        self.stack.animation_finished.connect(lambda: self.setEnabled(True))

        # Default Position: North
        self._tab_position = QTabWidget.TabPosition.North
        self._layout.addWidget(self.tab_bar)
        self._layout.addWidget(self.stack)

    def setTabPosition(self, position: QTabWidget.TabPosition):
        """Cambia la posizione della barra dei tab (North o South)."""
        if position == self._tab_position:
            return
        
        self._tab_position = position
        self._layout.removeWidget(self.tab_bar)
        self._layout.removeWidget(self.stack)
        
        if position == QTabWidget.TabPosition.South:
            self._layout.addWidget(self.stack)
            self._layout.addWidget(self.tab_bar)
            self.tab_bar.setStyleSheet(self._get_south_style())
        else:
            self._layout.addWidget(self.tab_bar)
            self._layout.addWidget(self.stack)
            self.tab_bar.setStyleSheet(self._get_default_style())

    def addTab(self, widget: QWidget, *args):
        """Aggiunge una scheda allo stack e alla barra."""
        index = self.tab_bar.addTab(*args)
        self.stack.addWidget(widget)
        return index

    def _on_tab_bar_changed(self, index: int):
        """Innesca l'animazione di scorrimento Snapshot."""
        if index != self.stack.currentIndex():
            self.setEnabled(False)
            self.stack.slide_to_index(index)
            if not self.stack._is_animating:
                self.setEnabled(True)
            self.currentChanged.emit(index)

    # --- API Compatibility ---
    def currentIndex(self) -> int: return self.tab_bar.currentIndex()
    def currentWidget(self) -> QWidget: return self.stack.currentWidget()
    def setCurrentIndex(self, index: int):
        self.tab_bar.setCurrentIndex(index)
        self.stack.setCurrentIndex(index)
    def count(self) -> int: return self.tab_bar.count()
    def tabText(self, index: int) -> str: return self.tab_bar.tabText(index)
    def widget(self, index: int) -> QWidget: return self.stack.widget(index)
    def setTabText(self, index: int, text: str): self.tab_bar.setTabText(index, text)
    def tabBar(self) -> QTabBar: return self.tab_bar
    
    def clear(self):
        while self.tab_bar.count() > 0: self.tab_bar.removeTab(0)
        while self.stack.count() > 0:
            w = self.stack.widget(0)
            self.stack.removeWidget(w)
            w.deleteLater()

    def _get_default_style(self) -> str:
        return """
            QTabBar::tab {
                background: transparent; color: #78909C; padding: 12px 24px;
                font-weight: 600; font-size: 13px; border-bottom: 2px solid transparent;
            }
            QTabBar::tab:selected { color: #009688; border-bottom: 2px solid #009688; }
            QTabBar::tab:hover:!selected { color: #455A64; background: rgba(0, 0, 0, 0.03); }
        """

    def _get_south_style(self) -> str:
        return """
            QTabBar::tab {
                background: transparent; color: #78909C; padding: 8px 16px;
                font-weight: 600; font-size: 12px; border-top: 2px solid transparent;
            }
            QTabBar::tab:selected { color: #009688; border-top: 2px solid #009688; background: #FAFAFA; }
        """
