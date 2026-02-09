from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

from src.gui.widgets.animated_progress_bar import AnimatedProgressBar


class FooterRightWidget(QWidget):
    """Parte destra del footer: contiene Progress Bar e Status Cards Bot."""

    def __init__(
        self, status_portale: QWidget, status_safework: QWidget, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 15, 0)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.progress_bar = AnimatedProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("0%")
        self.progress_label.setStyleSheet(
            "color: #000000; font-family: 'Consolas', monospace; font-weight: bold; font-size: 13px;"
        )
        self.progress_label.setVisible(False)
        layout.addWidget(self.progress_label)

        self.status_portale = status_portale
        self.status_safework = status_safework
        layout.addWidget(status_portale)
        layout.addWidget(status_safework)

    def set_global_progress(self, value: int) -> None:
        value = max(0, min(value, 100))
        self.progress_bar.setValue(value)
        self.progress_label.setText(f"{value}%")

    def show_loading(self) -> None:
        self.progress_bar.setVisible(True)
        self.progress_label.setVisible(True)
        self.status_portale.setVisible(False)
        self.status_safework.setVisible(False)

    def show_operational(self) -> None:
        self.progress_bar.setVisible(False)
        self.progress_label.setVisible(False)
        self.status_portale.setVisible(True)
        self.status_safework.setVisible(True)
