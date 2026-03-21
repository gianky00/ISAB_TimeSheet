"""
SyncroJob - ODA Adapter
Adapter per convertire i dati ODA in oggetti QStandardItem per la GUI.
Isola le dipendenze PyQt dal CORE.
"""

from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QStandardItem

from src.gui.formatters import format_currency_smart


class ODAAdapter:
    """Gestisce la creazione degli item per il modello della vista ODA."""

    @staticmethod
    def create_root_row(data: dict[str, Any]) -> list[QStandardItem]:
        """Crea la riga genitore (OdA) per il modello."""
        items = [
            QStandardItem(str(data["data"])),
            QStandardItem(str(data["oda"])),
            QStandardItem(""),  # Pos (vuota per il root)
            QStandardItem(str(data["creatore"])),
            QStandardItem(str(data["descrizione"])),
            QStandardItem(format_currency_smart(data["valore_totale"])),
            QStandardItem(str(data["stato"])),
            QStandardItem(str(data["rilascio"])),
        ]
        # Alleghiamo i dati grezzi al primo item
        items[0].setData(data["raw_first"], Qt.ItemDataRole.UserRole)
        return items

    @staticmethod
    def create_child_row(pos_row: tuple[Any, ...]) -> list[QStandardItem]:
        """Crea la riga figlia (Posizione)."""
        val_pos_riga = f"{pos_row[3]}/{pos_row[27]}" if str(pos_row[27]) != "0" else str(pos_row[3])

        # Accorpamento Quantità + Unità Misura + Prezzo
        qta_val = pos_row[28]
        uom_val = pos_row[29]
        prezzo_str = format_currency_smart(pos_row[30])
        val_tecnico = f"{qta_val} {uom_val} - {prezzo_str}"

        items = [
            QStandardItem(str(pos_row[31])),  # Col 0: Testo Breve
            QStandardItem(""),  # Col 1
            QStandardItem(val_pos_riga),  # Col 2
            QStandardItem(val_tecnico),  # Col 3
            QStandardItem(""),  # Col 4
            QStandardItem(""),  # Col 5
            QStandardItem(""),  # Col 6
            QStandardItem(""),  # Col 7
        ]

        items[0].setData(pos_row, Qt.ItemDataRole.UserRole)

        # Styling blu scuro
        blue_color = QColor("#003366")
        for it in items:
            it.setForeground(blue_color)

        return items
