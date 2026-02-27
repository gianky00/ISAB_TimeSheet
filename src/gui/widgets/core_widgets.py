"""
Core Widgets - UI Kit Standard components for SyncroJob Enterprise.

Questo modulo definisce wrapper stilizzati per i widget PyQt6 di base,
garantendo coerenza visiva nell'intera applicazione.
"""

from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QWidget,
)

from src.gui.design.colors import get_palette
from src.gui.widgets.modern_button import ModernButton


class PrimaryButton(ModernButton):
    """Pulsante primario con stile accent."""

    def __init__(self, text: str = "", icon: Optional[str] = None, parent: Optional[QWidget] = None):
        super().__init__(text=text, variant=ModernButton.Variant.PRIMARY, icon=icon, parent=parent)


class SecondaryButton(ModernButton):
    """Pulsante secondario con stile neutro."""

    def __init__(self, text: str = "", icon: Optional[str] = None, parent: Optional[QWidget] = None):
        super().__init__(text=text, variant=ModernButton.Variant.SECONDARY, icon=icon, parent=parent)


class DangerButton(ModernButton):
    """Pulsante rosso per azioni distruttive."""

    def __init__(self, text: str = "", icon: Optional[str] = None, parent: Optional[QWidget] = None):
        super().__init__(text=text, variant=ModernButton.Variant.DANGER, icon=icon, parent=parent)


class GhostButton(ModernButton):
    """Pulsante trasparente con bordo."""

    def __init__(self, text: str = "", icon: Optional[str] = None, parent: Optional[QWidget] = None):
        super().__init__(text=text, variant=ModernButton.Variant.GHOST, icon=icon, parent=parent)


class SearchInput(QLineEdit):
    """QLineEdit stilizzato per campi di ricerca, con placeholder e clear button."""

    def __init__(self, placeholder: str = "Cerca...", parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setClearButtonEnabled(True)
        self._apply_style()

    def _apply_style(self) -> None:
        palette = get_palette()
        self.setStyleSheet(f"""
            QLineEdit {{
                padding: 8px 12px;
                border: 1px solid {palette.border};
                border-radius: 6px;
                background-color: {palette.surface};
                color: {palette.on_surface};
            }}
            QLineEdit:focus {{
                border: 1px solid {palette.primary};
            }}
        """)


class FilterComboBox(QComboBox):
    """QComboBox stilizzata per filtri e selettori."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._apply_style()

    def _apply_style(self) -> None:
        palette = get_palette()
        self.setStyleSheet(f"""
            QComboBox {{
                padding: 6px 12px;
                border: 1px solid {palette.border};
                border-radius: 6px;
                background-color: {palette.surface};
                color: {palette.on_surface};
            }}
            QComboBox:focus {{
                border: 1px solid {palette.primary};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
        """)


class StandardTable(QTableWidget):
    """QTableWidget con stile enterprise, righe alternate e selezione per riga."""

    def __init__(self, rows: int = 0, columns: int = 0, parent: Optional[QWidget] = None):
        super().__init__(rows, columns, parent)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._apply_style()

    def _apply_style(self) -> None:
        palette = get_palette()
        self.setStyleSheet(f"""
            QTableWidget {{
                border: 1px solid {palette.border};
                border-radius: 8px;
                background-color: {palette.surface};
                alternate-background-color: rgba(0, 0, 0, 0.02);
                selection-background-color: {palette.primary};
                selection-color: {palette.on_primary};
                gridline-color: {palette.border};
            }}
            QHeaderView::section {{
                background-color: {palette.background};
                color: {palette.on_surface};
                padding: 8px;
                border: none;
                border-bottom: 2px solid {palette.border};
                font-weight: bold;
            }}
            QTableWidget::item {{
                padding: 4px;
            }}
        """)


class StandardCheckBox(QCheckBox):
    """QCheckBox stilizzata con indicatore personalizzato."""

    def __init__(self, text: str = "", parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self._apply_style()

    def _apply_style(self) -> None:
        palette = get_palette()
        self.setStyleSheet(f"""
            QCheckBox {{
                color: {palette.on_background};
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid {palette.border};
                background-color: {palette.surface};
            }}
            QCheckBox::indicator:checked {{
                background-color: {palette.primary};
                border: 2px solid {palette.primary};
            }}
        """)


class StandardSpinBox(QSpinBox):
    """QSpinBox stilizzato con bordi coerenti."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._apply_style()

    def _apply_style(self) -> None:
        palette = get_palette()
        self.setStyleSheet(f"""
            QSpinBox {{
                padding: 6px 12px;
                border: 1px solid {palette.border};
                border-radius: 6px;
                background-color: {palette.surface};
                color: {palette.on_surface};
            }}
            QSpinBox:focus {{
                border: 1px solid {palette.primary};
            }}
        """)
