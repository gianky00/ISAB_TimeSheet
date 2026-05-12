"""
SyncroJob - Certificati Tree Widget
Componente specializzato per la visualizzazione gerarchica dei certificati campione.
"""

from typing import ClassVar

from PySide6.QtCore import QAbstractItemModel, QModelIndex, QPersistentModelIndex, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QIcon
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QHeaderView,
    QLineEdit,
    QStyledItemDelegate,
    QTreeWidgetItem,
    QWidget,
)

from src.core.constants import Icons, UbicazioneStrumenti
from src.gui.styles import COLORS
from src.gui.widgets.contabilita.helpers import SortableTreeWidgetItem
from src.gui.widgets.core_widgets import StandardTreeWidget
from src.utils.helpers import get_asset_path


class UbicazioneDelegate(QStyledItemDelegate):
    """Delegate per la selezione dell'ubicazione tramite ComboBox."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.items = [
            UbicazioneStrumenti.ASSENTE.value,
            UbicazioneStrumenti.UFFICIO_STRU.value,
            UbicazioneStrumenti.UFFICIO_CC.value,
            UbicazioneStrumenti.OFFICINA.value,
            UbicazioneStrumenti.SEDE.value,
            UbicazioneStrumenti.TECNICO.value,
        ]

    def createEditor(
        self, parent: QWidget, option: object, index: QModelIndex | QPersistentModelIndex
    ) -> QWidget:
        """Crea l'editor per la colonna Ubicazione."""
        editor = QComboBox(parent)
        editor.addItems(self.items)
        # Seleziona l'elemento corrente se valido
        current_text = index.data(Qt.ItemDataRole.EditRole)
        if current_text in self.items:
            editor.setCurrentText(current_text)
        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex | QPersistentModelIndex) -> None:
        """Popola l'editor con i dati correnti."""
        value = index.data(Qt.ItemDataRole.EditRole)
        if isinstance(editor, QComboBox):
            idx = editor.findText(value)
            if idx >= 0:
                editor.setCurrentIndex(idx)

    def setModelData(
        self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex | QPersistentModelIndex
    ) -> None:
        """Salva i dati dall'editor al modello."""
        if isinstance(editor, QComboBox):
            value = editor.currentText()
            model.setData(index, value, Qt.ItemDataRole.EditRole)


class AnnotazioniDelegate(QStyledItemDelegate):
    """Delegate per l'inserimento testo libero nelle annotazioni."""

    def createEditor(
        self, parent: QWidget, option: object, index: QModelIndex | QPersistentModelIndex
    ) -> QWidget:
        """Crea l'editor per la colonna Annotazioni."""
        return QLineEdit(parent)

    def setEditorData(self, editor: QWidget, index: QModelIndex | QPersistentModelIndex) -> None:
        """Popola l'editor con i dati correnti."""
        value = index.data(Qt.ItemDataRole.EditRole)
        if isinstance(editor, QLineEdit):
            editor.setText(value)

    def setModelData(
        self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex | QPersistentModelIndex
    ) -> None:
        """Salva i dati dall'editor al modello."""
        if isinstance(editor, QLineEdit):
            value = editor.text()
            model.setData(index, value, Qt.ItemDataRole.EditRole)


class CertificatiTreeWidget(StandardTreeWidget):
    """Tree Widget specializzato per la gestione dei certificati."""

    item_edited_custom = Signal(object, str, str)  # (item, col_name, new_value)

    HEADERS: ClassVar[list[str]] = [
        "ID-STRUMENTO",
        "Certificato",
        "Modello /\nTipo",
        "Costruttore",
        "Matricola",
        "Range\nStrumento",
        "Err %",
        "Emissione",
        "Scadenza",
        "Stato",
        "Ubicazione",
        "Annotazioni",
    ]

    (
        IDX_ID_STRUMENTO,
        IDX_CERTIFICATO,
        IDX_MODELLO,
        IDX_COSTRUTTORE,
        IDX_MATRICOLA,
        IDX_RANGE,
        IDX_ERRORE,
        IDX_EMISSIONE,
        IDX_SCADENZA,
        IDX_STATO,
        IDX_UBICAZIONE,
        IDX_ANNOTAZIONI,
    ) = range(12)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()
        self.itemChanged.connect(self._on_item_changed)

    def _setup_ui(self) -> None:
        self.setHeaderLabels(self.HEADERS)
        self.setWordWrap(True)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        # Abilitiamo l'edit on double click, ma poi gestiremo i flag nei singoli item
        self.setEditTriggers(
            QAbstractItemView.EditTrigger.DoubleClicked | QAbstractItemView.EditTrigger.EditKeyPressed
        )
        self.setAnimated(True)

        # Applica i delegate
        self.setItemDelegateForColumn(self.IDX_UBICAZIONE, UbicazioneDelegate(self))
        self.setItemDelegateForColumn(self.IDX_ANNOTAZIONI, AnnotazioniDelegate(self))

        h = self.header()
        if h:
            for col in range(12):
                h.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
            h.setStretchLastSection(True)

        self.setStyleSheet(f"""
      QTreeWidget {{
        border: 1px solid {COLORS["border_light"]};
        border-radius: 8px;
        background-color: {COLORS["bg_white"]};
        outline: none;
      }}
      QTreeWidget::item {{
        padding: 8px 4px;
        border-bottom: 1px solid {COLORS["bg_alt"]};
      }}
      QTreeWidget::item:hover {{ background-color: {COLORS["bg_light"]}; }}
      QTreeWidget::item:selected {{
        background-color: {COLORS["bg_info_pastel"]};
        color: {COLORS["primary_dark"]};
      }}
      QHeaderView::section {{
        background-color: {COLORS["bg_light"]};
        padding: 10px 8px;
        border: none;
        border-bottom: 2px solid {COLORS["border_light"]};
        border-right: 1px solid {COLORS["border_light"]};
        font-weight: bold;
        color: {COLORS["text_muted"]};
      }}
    """)

    def apply_current_certificate_styling(
        self, item: SortableTreeWidgetItem, days_to_expiry: int | None, status_dot_icon: str
    ) -> None:
        """Applica lo styling specifico per il certificato più recente."""
        if days_to_expiry is None:
            status_text, bg_color, text_color = (
                "N/D (Senza Scadenza)",
                COLORS["bg_alt"],
                COLORS["text_light"],
            )
        elif days_to_expiry == -9999:
            status_text, bg_color, text_color = (
                "GUASTO",
                COLORS["bg_error_pastel"],
                COLORS["error_red"],
            )
        elif days_to_expiry < 0:
            status_text, bg_color, text_color = (
                f"Scaduto da {abs(days_to_expiry)} giorni",
                COLORS["bg_error_pastel"],
                COLORS["error_red"],
            )
        elif 0 <= days_to_expiry <= 15:
            status_text, bg_color, text_color = (
                f"Scade tra {days_to_expiry} giorni",
                COLORS["bg_warning_pastel"],
                COLORS["warning_orange"],
            )
        elif 16 <= days_to_expiry <= 30:
            status_text, bg_color, text_color = (
                f"Scade tra {days_to_expiry} giorni",
                COLORS["bg_attention_pastel"],
                COLORS["warning_yellow"],
            )
        else:
            status_text, bg_color, text_color = (
                f"Attivo ({days_to_expiry} giorni rimanenti)",
                COLORS["bg_success_pastel"],
                COLORS["success_dark"],
            )

        for col in range(self.columnCount()):
            item.setBackground(col, QBrush(QColor(bg_color)))

        item.setIcon(self.IDX_STATO, QIcon(get_asset_path(status_dot_icon)))
        item.setText(self.IDX_STATO, status_text)
        item.setForeground(self.IDX_STATO, QBrush(QColor(text_color)))

        font = item.font(self.IDX_STATO)
        font.setBold(True)
        item.setFont(self.IDX_STATO, font)

    def apply_historical_certificate_styling(self, item: SortableTreeWidgetItem) -> None:
        """Applica lo styling per i certificati storici."""
        bg_color = QColor(COLORS["bg_alt"])
        for col in range(self.columnCount()):
            item.setBackground(col, QBrush(bg_color))

        item.setIcon(self.IDX_STATO, QIcon(get_asset_path(Icons.STATUS_DOT_GRAY)))
        item.setText(self.IDX_STATO, "STORICO")
        item.setForeground(self.IDX_STATO, QBrush(QColor(COLORS["text_light"])))
        item.setToolTip(self.IDX_STATO, "Certificato storico - Esiste un certificato più recente")

    def _on_item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        """Gestisce il cambiamento di valore in una cella."""
        if column == self.IDX_ANNOTAZIONI:
            self.item_edited_custom.emit(item, "annotazioni", item.text(column))
        elif column == self.IDX_UBICAZIONE:
            self.item_edited_custom.emit(item, "ubicazione", item.text(column))
