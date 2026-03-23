from contextlib import suppress
from datetime import UTC, datetime
from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem


class SortableTableWidgetItem(QTableWidgetItem):
    """
    QTableWidgetItem personalizzato che gestisce correttamente l'ordinamento
    per numeri (int, float) e date (formati comuni), con fallback alfabetico.
    """

    def __init__(self, value: Any, alignment: Qt.AlignmentFlag | None = None) -> None:  # noqa: ANN401
        """
        Inizializza l'item.
        :param value: Il valore (str, int, float, datetime, o None).
        :param alignment: Opzionale, allineamento Qt (es. Qt.AlignmentFlag.AlignRight).
        """
        display_text = str(value) if value is not None else ""
        super().__init__(display_text)
        self.raw_value = value

        if alignment:
            self.setTextAlignment(alignment)

    def __lt__(self, other: Any) -> bool:  # noqa: ANN401, PLR0911
        """Override dell'operatore < per ordinamento personalizzato."""
        if not isinstance(other, QTableWidgetItem):
            return super().__lt__(other)

        val1 = self.text().strip()
        val2 = other.text().strip()

        # 1. Gestione celle vuote (vanno sempre in fondo o in cima a seconda dell'ordinamento,
        # ma qui implementiamo logica standard: vuoto < pieno)
        if not val1 and not val2:
            return False
        if not val1:
            return True
        if val2 == "":
            return False

        # 2. Tentativo Numerico
        with suppress(ValueError):
            n1 = self._parse_number(val1)
            n2 = self._parse_number(val2)
            return n1 < n2

        # 3. Tentativo Data
        with suppress(ValueError):
            d1 = self._parse_date(val1)
            d2 = self._parse_date(val2)
            return d1 < d2

        # 4. Fallback Stringa (Lexicographical)
        return val1.lower() < val2.lower()

    def _parse_number(self, text: str) -> float:
        """Tenta di convertire testo in float gestendo formati IT/US."""
        # Rimuovi simboli valuta
        text = text.replace("€", "").replace("$", "").strip()

        if "," in text and "." in text:
            # Assume formato 1.234,56 -> 1234.56
            if text.find(".") < text.find(","):
                text = text.replace(".", "").replace(",", ".")
            else:
                # Assume formato 1,234.56 -> 1234.56
                text = text.replace(",", "")
        elif "," in text:
            # Assume 12,5 -> 12.5 (decimale IT)
            text = text.replace(",", ".")

        return float(text)

    def _parse_date(self, text: str) -> datetime:
        """Tenta di convertire testo in datetime."""
        formats = [
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%d/%m/%Y %H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
        ]
        for fmt in formats:
            with suppress(ValueError):
                # Gestisce anche date parziali troncando il testo se necessario?
                # Meglio match esatto per evitare falsi positivi
                return datetime.strptime(text, fmt).replace(tzinfo=UTC)
        raise ValueError("Not a date")  # noqa: TRY003
