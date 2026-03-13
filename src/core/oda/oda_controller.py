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
        """Crea la riga figlia (Posizione) ultra-snella: Qta, UoM e Prezzo accorpati."""
        # Indici definiti in OdaManager.get_all_oda:
        # 31:testo_breve, 3:pos_oda, 27:num_riga, 28:quantita, 29:unita_mis, 30:prezzo_lordo

        val_pos_riga = f"{pos_row[3]}/{pos_row[27]}" if str(pos_row[27]) != "0" else str(pos_row[3])

        # Accorpamento Quantità + Unità Misura + Prezzo con €
        qta_val = pos_row[28]
        uom_val = pos_row[29]
        prezzo_str = format_currency_smart(pos_row[30])
        val_tecnico = f"{qta_val} {uom_val} - {prezzo_str}"

        items = [
            QStandardItem(str(pos_row[31])),  # Col 0: Testo Breve (per merge Col 0-1)
            QStandardItem(""),  # Col 1: Vuota (coperta dal merge)
            QStandardItem(val_pos_riga),  # Col 2: Pos / Riga
            QStandardItem(val_tecnico),  # Col 3: Qta/UoM e Prezzo (vicini)
            QStandardItem(""),  # Col 4: Descrizione (Svuotata)
            QStandardItem(""),  # Col 5: Valore Netto (Svuotata)
            QStandardItem(""),  # Col 6: Stato (Rimosso come richiesto)
            QStandardItem(""),  # Col 7: Prezzo (Spostato in Col 3)
        ]

        # Alleghiamo i dati grezzi della posizione al primo item per il dettaglio laterale
        items[0].setData(pos_row, Qt.ItemDataRole.UserRole)

        # Styling blu scuro per distinguere i figli
        from PyQt6.QtGui import QColor

        for it in items:
            it.setForeground(QColor("#003366"))

        return items
