"""
Tabella dati con sorting, filtering e row styling, basata su ExcelTableWidget.
Fornisce un'interfaccia ad alto livello con ricerca e pulsante di aggiornamento.
"""

from typing import Any, ClassVar

from src.gui.widgets.core_widgets import (PrimaryButton, SecondaryButton, DangerButton, GhostButton, IconButton, SearchInput, StandardInput, StandardTextEdit, FilterComboBox, StandardCheckBox, StandardSpinBox, StandardTable, StandardListWidget, StandardTreeWidget, StandardGroupBox, StandardProgressBar)
from PyQt6.QtCore import (  # type: ignore[attr-defined]
    QEasingCurve,
    QModelIndex,
    QPropertyAnimation,
    Qt,
    pyqtProperty,
    pyqtSignal,
)
from PyQt6.QtGui import QBrush, QColor, QPainter, QPen
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.constants import Icons
from src.gui.styles import COLORS
from src.gui.widgets.sortable_table_item import SortableTableWidgetItem
from src.utils.helpers import get_asset_path, get_colored_icon

from ..design.colors import get_palette
from ..design.spacing import Spacing

# Use explicit import from new modular widget to avoid circular dependency
from .excel_table import ExcelTableWidget


class HoverPulseFrame(QFrame):
    """
    Frame personalizzato che fa pulsare il bordo inferiore al passaggio del mouse.
    Migliora il feedback visivo dell'interfaccia.
    """

    def __init__(self, accent_color: str | None = None, parent=None):
        """
        Inizializza il frame con il colore di accento specificato.

        Args:
            accent_color: Colore del bordo pulsante.
            parent: Widget genitore.
        """
        super().__init__(parent)
        self._accent_color = QColor(accent_color or COLORS["text_dark"])
        self._pulse_val = 1.0

        self._anim = QPropertyAnimation(self, b"pulse_value")
        self._anim.setDuration(1500)
        self._anim.setStartValue(0.4)
        self._anim.setEndValue(1.0)
        self._anim.setLoopCount(-1)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutSine)

    @pyqtProperty(float)
    def pulse_value(self) -> float:
        """Restituisce il valore corrente della pulsazione."""
        return self._pulse_val

    @pulse_value.setter  # type: ignore[no-redef]
    def pulse_value(self, v: float):
        """Imposta il valore della pulsazione e aggiorna il widget."""
        self._pulse_val = v
        self.update()

    def enterEvent(self, event):
        """Avvia l'animazione di pulsazione all'ingresso del mouse."""
        self._anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Ferma l'animazione di pulsazione all'uscita del mouse."""
        self._anim.stop()
        self.pulse_value = 1.0  # type: ignore[method-assign]
        super().leaveEvent(event)

    def paintEvent(self, event):
        """Disegna il bordo inferiore pulsante."""
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        alpha = int(100 + (self._pulse_val * 155))
        pen = QPen(
            QColor(self._accent_color.red(), self._accent_color.green(), self._accent_color.blue(), alpha)
        )
        pen.setWidth(3)
        painter.setPen(pen)

        rect = self.rect()
        painter.drawLine(12, rect.height() - 2, rect.width() - 12, rect.height() - 2)


class DataTable(QWidget):
    """
    Tabella dati con funzionalità avanzate (search, refresh) che wrappa ExcelTableWidget.
    Supporta il filtraggio in tempo reale e la colorazione semantica delle righe.
    """

    rowDoubleClicked = pyqtSignal(int, dict)  # row_index, row_data
    """Segnale emesso al doppio click su una riga."""

    # Status colors
    STATUS_COLORS: ClassVar[dict[str, str]] = {
        "completato": COLORS["table_success_bg"],  # Green
        "errore": COLORS["table_error_bg"],  # Red
        "in_corso": COLORS["table_warning_bg"],  # Yellow
        "pending": COLORS["table_info_bg"],  # Blue
        "da_processare": COLORS["bg_white"],  # White
    }

    def __init__(self, columns: list[dict[str, Any]], parent: QWidget | None = None) -> None:
        """
        Inizializza la DataTable con le colonne specificate.

        Args:
            columns: Lista di dict con keys: 'name', 'key', 'width', 'editable'.
            parent: Widget genitore.
        """
        super().__init__(parent)
        self._columns = columns
        self._data: list[dict[str, Any]] = []
        self._palette = get_palette()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configura il layout, la toolbar di ricerca e la card contenente la tabella."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(Spacing.xs)

        # Toolbar
        toolbar = QHBoxLayout()

        # Search
        self._search_input = SearchInput()
        self._search_input.setPlaceholderText("Cerca...")
        self._search_input.setClearButtonEnabled(True)
        self._search_input.textChanged.connect(self._filter_rows)
        # Apply modern style
        self._search_input.setStyleSheet(
            f"""
            QLineEdit {{
                border: 1px solid {self._palette.border};
                border-radius: 6px;
                padding: 6px 10px;
                background: {self._palette.surface};
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['text_dark']};
            }}
        """
        )
        toolbar.addWidget(self._search_input, 1)

        # Actions
        self._refresh_btn = PrimaryButton(" Aggiorna")
        self._refresh_btn.setIcon(get_colored_icon(get_asset_path(Icons.REFRESH), COLORS["text_dark"]))
        self._refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._refresh_btn.clicked.connect(self.refresh)
        self._refresh_btn.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self._palette.surface};
                border: 1px solid {self._palette.border};
                border-radius: 6px;
                padding: 6px 12px;
                color: {self._palette.on_surface};
            }}
            QPushButton:hover {{
                background-color: {self._palette.hover};
            }}
        """
        )
        toolbar.addWidget(self._refresh_btn)

        layout.addLayout(toolbar)

        # --- CONTAINER PRINCIPALE (Card con ombra e accento scuro pulsante) ---
        self.container = HoverPulseFrame(COLORS["text_dark"])
        self.container.setObjectName("tableContainer")
        self.container.setStyleSheet(f"""
            QFrame#tableContainer {{
                background-color: {COLORS['bg_white']};
                border: 1px solid {COLORS['border_light']};
                /* border-bottom rimosso perché gestito da HoverPulseFrame */
                border-radius: 12px;
            }}
            QTableWidget {{
                background-color: transparent;
                border: none;
                gridline-color: {COLORS['bg_alt']};
                selection-background-color: {COLORS['table_selection_bg']};
                selection-color: {COLORS['text_dark']};
                outline: none;
            }}
            QHeaderView::section {{
                background-color: {COLORS['bg_light']};
                color: {COLORS['text_dark']};
                padding: 10px;
                font-weight: bold;
                border: none;
                border-bottom: 1px solid {COLORS['border_light']};
            }}
        """)

        # Shadow Effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.container.setGraphicsEffect(shadow)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(5, 5, 5, 5)

        self._table = ExcelTableWidget()
        self._table.setColumnCount(len(self._columns))
        self._table.setHorizontalHeaderLabels([str(c["name"]) for c in self._columns])
        # ExcelTableWidget handles SelectionBehavior and SelectionMode already
        self._table.setAlternatingRowColors(True)
        self._table.setSortingEnabled(True)
        self._table.doubleClicked.connect(self._on_double_click)

        # Header sizing
        header = self._table.horizontalHeader()
        if header is not None:
            header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        for i, col in enumerate(self._columns):
            if "width" in col:
                self._table.setColumnWidth(i, int(col["width"]))
            elif header is not None:
                header.setSectionResizeMode(i, QHeaderView.ResizeMode.Interactive)

        container_layout.addWidget(self._table)
        layout.addWidget(self.container)

    def _apply_table_style(self) -> None:
        """Applica stili specifici alla tabella (opzionale, gestito principalmente da QSS)."""

    def setData(self, data: list[dict[str, Any]]) -> None:
        """
        Popola la tabella con i dati forniti.

        Args:
            data: Lista di dizionari contenenti i dati delle righe.
        """
        self._data = data
        self._populate_table(data)

    def _populate_table(self, data: list[dict[str, Any]]) -> None:
        """Riempie fisicamente il widget QTableWidget con i dati."""
        self._table.setSortingEnabled(False)  # Optimization
        self._table.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            # Determina colore riga basato su stato
            status = str(row_data.get("stato", "")).lower()
            row_color = self._get_row_color(status)

            for col_idx, col in enumerate(self._columns):
                key = col.get("key", str(col["name"]).lower())
                value = str(row_data.get(key, ""))

                item = SortableTableWidgetItem(value)

                # Editabilità
                if not col.get("editable", True):
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                # Colore sfondo
                if row_color:
                    item.setBackground(QBrush(QColor(row_color)))
                    item.setForeground(QBrush(QColor("black")))  # Force contrast

                self._table.setItem(row_idx, col_idx, item)

        self._table.setSortingEnabled(True)

    def _get_row_color(self, status: str) -> str | None:
        """Restituisce il codice colore esadecimale per uno stato specifico."""
        if status in self.STATUS_COLORS:
            return self.STATUS_COLORS[status]
        # Check prefix
        for key, color in self.STATUS_COLORS.items():
            if status.startswith(key):
                return color
        return None

    def _filter_rows(self, text: str) -> None:
        """
        Filtra le righe della tabella in base al testo di ricerca (case-insensitive).

        Args:
            text: Testo da cercare in tutte le colonne.
        """
        text = text.lower()
        for row in range(self._table.rowCount()):
            match = False
            for col in range(self._table.columnCount()):
                item = self._table.item(row, col)
                if item and text in item.text().lower():
                    match = True
                    break
            self._table.setRowHidden(row, not match)

    def _on_double_click(self, index: QModelIndex) -> None:
        """
        Gestisce l'evento di doppio click emettendo il segnale rowDoubleClicked.

        Args:
            index: Indice del modello dell'elemento cliccato.
        """
        row = index.row()
        if 0 <= row < len(self._data):
            self.rowDoubleClicked.emit(row, self._data[row])

    def getSelectedRows(self) -> list[dict[str, Any]]:
        """
        Restituisce i dati di tutte le righe attualmente selezionate.

        Returns:
            list: Lista di dizionari rappresentanti le righe selezionate.
        """
        rows = {item.row() for item in self._table.selectedItems()}

        selected_data = []
        for r in rows:
            row_dict: dict[str, Any] = {}
            for c, col in enumerate(self._columns):
                item = self._table.item(r, c)
                key = col.get("key", str(col["name"]).lower())
                row_dict[key] = item.text() if item else ""
            selected_data.append(row_dict)

        return selected_data

    def refresh(self) -> None:
        """Metodo per ricaricare i dati. Da connettere esternamente."""

    def get_table_widget(self) -> ExcelTableWidget:
        """
        Restituisce il widget QTableWidget interno.

        Returns:
            ExcelTableWidget: Il widget della tabella.
        """
        return self._table
