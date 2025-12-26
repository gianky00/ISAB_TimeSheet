"""
Framework di validazione input centralizzato.
"""
import re
from typing import Optional
from dataclasses import dataclass

@dataclass
class ValidationResult:
    valid: bool
    error: Optional[str] = None
    sanitized_value: Optional[str] = None

class InputValidator:
    """Validatore centralizzato per tutti gli input utente."""

    # Pattern comuni
    PATTERNS = {
        'oda_number': r'^[A-Za-z0-9]{1,20}$',
        'codice_fiscale': r'^[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]$',
        'date_it': r'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d$',
        'time': r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$',
        'username': r'^[a-zA-Z0-9_]{3,50}$',
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    }

    @classmethod
    def validate_oda(cls, value: str) -> ValidationResult:
        """Valida numero OdA."""
        if not value:
            return ValidationResult(False, "Numero OdA obbligatorio")

        sanitized = value.strip().upper()

        if len(sanitized) > 20:
            return ValidationResult(False, "Numero OdA troppo lungo (max 20 caratteri)")

        if not re.match(cls.PATTERNS['oda_number'], sanitized):
            return ValidationResult(False, "Numero OdA contiene caratteri non validi")

        return ValidationResult(True, sanitized_value=sanitized)

    @classmethod
    def validate_codice_fiscale(cls, value: str) -> ValidationResult:
        """Valida codice fiscale italiano."""
        if not value:
            return ValidationResult(False, "Codice Fiscale obbligatorio")

        sanitized = value.strip().upper()

        if len(sanitized) != 16:
            return ValidationResult(False, "Codice Fiscale deve essere di 16 caratteri")

        if not re.match(cls.PATTERNS['codice_fiscale'], sanitized):
            return ValidationResult(False, "Formato Codice Fiscale non valido")

        # Validazione checksum (carattere di controllo)
        if not cls._validate_cf_checksum(sanitized):
            return ValidationResult(False, "Checksum Codice Fiscale non valido")

        return ValidationResult(True, sanitized_value=sanitized)

    @staticmethod
    def _validate_cf_checksum(cf: str) -> bool:
        """Verifica il carattere di controllo del CF."""
        # Implementazione algoritmo di controllo
        odd_map = {
            '0': 1, '1': 0, '2': 5, '3': 7, '4': 9, '5': 13, '6': 15, '7': 17, '8': 19, '9': 21,
            'A': 1, 'B': 0, 'C': 5, 'D': 7, 'E': 9, 'F': 13, 'G': 15, 'H': 17, 'I': 19, 'J': 21,
            'K': 2, 'L': 4, 'M': 18, 'N': 20, 'O': 11, 'P': 3, 'Q': 6, 'R': 8, 'S': 12, 'T': 14,
            'U': 16, 'V': 10, 'W': 22, 'X': 25, 'Y': 24, 'Z': 23
        }
        even_map = {
            '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
            'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
            'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19,
            'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25
        }

        total = 0
        for i, char in enumerate(cf[:15]):
            if i % 2 == 0:  # Posizione dispari (1-indexed)
                total += odd_map.get(char, 0)
            else:  # Posizione pari
                total += even_map.get(char, 0)

        expected = chr(65 + (total % 26))
        return cf[15] == expected

    @classmethod
    def validate_date_italian(cls, value: str) -> ValidationResult:
        """Valida data in formato italiano (GG.MM.AAAA)."""
        if not value:
            return ValidationResult(False, "Data obbligatoria")

        sanitized = value.strip().replace('/', '.')

        if not re.match(cls.PATTERNS['date_it'], sanitized):
            return ValidationResult(False, "Formato data non valido (usa GG.MM.AAAA)")

        # Verifica data valida
        try:
            from datetime import datetime
            datetime.strptime(sanitized, '%d.%m.%Y')
        except ValueError:
            return ValidationResult(False, "Data non esistente")

        return ValidationResult(True, sanitized_value=sanitized)

    @classmethod
    def sanitize_sql_string(cls, value: str) -> str:
        """Sanitizza stringa per uso in SQL (anche se usiamo parametri)."""
        if not value:
            return ""
        # Rimuovi caratteri di controllo
        return ''.join(c for c in value if c.isprintable())
