from PyQt6.QtWidgets import QPushButton


class SidebarButton(QPushButton):
    """Pulsante personalizzato per la sidebar."""

    def __init__(self, text: str, icon: str = "", parent=None):
        super().__init__(parent)
        self.setText(f"{icon} {text}" if icon else text)
        self.setCheckable(True)
        self.setMinimumHeight(55)
        self.setMinimumWidth(180)
        self._original_text = f"{icon} {text}" if icon else text
        self._update_style()
        self.toggled.connect(self._update_style)

    def set_badge(self, count: int):
        """Imposta un badge di notifica."""
        if count > 0:
            self.setText(f"{self._original_text} 🔴 {count}")
        else:
            self.setText(self._original_text)

    def _update_style(self):
        """Aggiorna lo stile in base allo stato."""
        if self.isChecked():
            self.setStyleSheet(
                """
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.25);
                    color: #ffffff;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 8px;
                    padding: 12px 18px;
                    text-align: left;
                    font-weight: bold;
                    font-size: 16px;
                }
            """
            )
        else:
            self.setStyleSheet(
                """
                QPushButton {
                    background-color: transparent;
                    color: #ffffff;
                    border: 1px solid transparent;
                    border-radius: 8px;
                    padding: 12px 18px;
                    text-align: left;
                    font-size: 16px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.15);
                    color: white;
                }
            """
            )
