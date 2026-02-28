"""
SyncroJob - ODA Controller
Logica di business per il caricamento, raggruppamento e processing degli Ordini di Acquisto.
"""

import logging
from collections import defaultdict
from typing import Any

from PyQt6.QtGui import QFont, QStandardItem

from src.core.oda_manager import OdaManager
from src.gui.formatters import format_currency_smart

logger = logging.getLogger(__name__)


class ODAController:
    """Controller per gestire la gerarchia e il processing dei dati OdA."""

    @staticmethod
    def get_grouped_data(search_text: str = "") -> list[dict[str, Any]]:
        """Recupera i dati dal DB e li raggruppa per numero OdA."""
        raw_data = OdaManager.get_all_oda(search_text)

        # Raggruppamento per numero OdA
        grouped = defaultdict(list)
        for r in raw_data:
            oda_num = str(r[2])  # Colonna 2: Numero OdA
            grouped[oda_num].append(r)

        # Trasformazione in lista strutturata per la UI
        structured = []
        for oda_num, positions in grouped.items():
            first = positions[0]
            # Calcolo totale OdA (somma dei valori netti delle posizioni)
            total_value = sum(float(p[12]) if p[12] else 0.0 for p in positions)

            structured.append(
                {
                    "oda": oda_num,
                    "data": first[1],
                    "creatore": first[14],
                    "descrizione": first[6],
                    "valore_totale": total_value,
                    "stato": first[4],
                    "rilascio": first[24],
                    "positions": positions,
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
        # Styling grassetto per il root
        font = QFont()
        font.setBold(True)
        for it in items:
            it.setFont(font)
        return items

    @staticmethod
    def create_child_item(pos_row: tuple[Any, ...]) -> list[QStandardItem]:
        """Crea la riga figlia (Posizione) per il modello."""
        return [
            QStandardItem(""),  # Data (vuota)
            QStandardItem(""),  # OdA (vuota)
            QStandardItem(str(pos_row[3])),  # Pos OdA
            QStandardItem(""),  # Creato da (vuota)
            QStandardItem(str(pos_row[6])),  # Descrizione
            QStandardItem(format_currency_smart(pos_row[10])),  # Valore Netto Pos
            QStandardItem(str(pos_row[4])),  # Stato
            QStandardItem(""),  # Rilascio (vuota)
        ]
