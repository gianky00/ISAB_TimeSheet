"""
SyncroJob - ODA Controller
Logica di business per il caricamento, raggruppamento e processing degli Ordini di Acquisto.
Refactored V9.3: Fixed column alignment for ChildDescriptionDelegate.
"""

import logging
from collections import defaultdict
from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItem

from src.core.oda_manager import OdaManager
from src.gui.formatters import format_currency_smart, format_date_it

logger = logging.getLogger(__name__)


class ODAController:
    """Controller per gestire la gerarchia e il processing dei dati OdA."""

    @staticmethod
    def get_grouped_data(search_text: str = "") -> list[dict[str, Any]]:
        """Recupera i dati dal DB e li raggruppa per numero OdA."""
        raw_data = OdaManager.get_all_oda(search_text)

        # Raggruppamento per numero OdA (indice 2)
        grouped = defaultdict(list)
        for r in raw_data:
            oda_num = str(r[2])
            grouped[oda_num].append(r)

        # Trasformazione in lista strutturata per la UI
        structured = []
        for oda_num, positions in grouped.items():
            first = positions[0]
            # Valore Netto ODA (indice 12) è già il totale dell'intero ordine
            total_value = float(first[12]) if first[12] else 0.0

            structured.append(
                {
                    "oda": oda_num,
                    "data": format_date_it(first[1]),  # Data OdA (indice 1)
                    "creatore": first[15],  # Nome Destinatario (indice 15)
                    "descrizione": first[6],  # Descrizione (indice 6)
                    "valore_totale": total_value,
                    "stato": first[4],  # Stato (indice 4)
                    "rilascio": first[24],  # Indicatore Rilascio (indice 24)
                    "positions": positions,
                    "raw_first": first,
                }
            )
        return structured

    @staticmethod
    def create_root_item(data: dict[str, Any]) -> list[QStandardItem]:
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
    def create_child_item(pos_row: tuple[Any, ...]) -> list[QStandardItem]:
        """Crea la riga figlia (Posizione) per il modello."""
        # Nota: La colonna 0 contiene il Testo Breve (indice 31) che verrà unito alla colonna 1 dal delegate
        items = [
            QStandardItem(str(pos_row[31])),  # Testo Breve (per merge Col 0-1)
            QStandardItem(""),  # Vuota (coperta dal merge)
            QStandardItem(str(pos_row[3])),  # Pos OdA (indice 3)
            QStandardItem(""),  # Creato da (vuota)
            QStandardItem(str(pos_row[6])),  # Descrizione (indice 6)
            QStandardItem(format_currency_smart(pos_row[10])),  # Valore Netto Pos (indice 10)
            QStandardItem(str(pos_row[4])),  # Stato (indice 4)
            QStandardItem(""),  # Rilascio (vuota)
        ]
        # Alleghiamo i dati grezzi della posizione al primo item
        items[0].setData(pos_row, Qt.ItemDataRole.UserRole)
        return items
