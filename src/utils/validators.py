"""
SyncroJob - Input Validators
Framework di validazione centralizzato per garantire l'integrità dei dati inseriti dall'utente.
Include controlli per OdA, PDL, Codici Fiscali e date.
"""

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import ClassVar


@dataclass
class ValidationResult:
    """
    Rappresenta l'esito di un'operazione di validazione.

    Attributes:
      valid: True se il valore  conforme al pattern richiesto.
      error: Messaggio descrittivo in caso di errore.
      sanitized_value: Il valore normalizzato e pronto per l'uso (es. maiuscolo, senza spazi).
    """

    valid: bool
    error: str | None = None
    sanitized_value: str | None = None


class InputValidator:
    """
    Validatore centralizzato per tutti gli input utente.
    Contiene pattern regex standard e logica di validazione complessa (es. checksum CF).
    """

    # Costanti di validazione
    PDL_DIGITS_ONLY = 6
    PDL_SUFFIX_THRESHOLD = 400000
    ODA_MAX_LENGTH = 20
    CF_LENGTH = 16

    # Pattern comuni
    PATTERNS: ClassVar[dict[str, str]] = {
        "oda_number": r"^[A-Za-z0-9]{1,20}$",
        "pdl_number": r"^[0-9]{6}/[CS]$",
        "codice_fiscale": r"^[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]$",
        "date_it": r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d$",
        "time": r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$",
        "username": r"^[a-zA-Z0-9_]{3,50}$",
        "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    }

    @classmethod
    def validate_pdl(cls, value: str) -> ValidationResult:
        """
        Valida numero PDL (6 cifre + /C o /S).
        Se vengono fornite solo 6 cifre, aggiunge automaticamente il suffisso in base al numero.

        Args:
          value: Il numero PDL grezzo.

        Returns:
          ValidationResult: L'esito della validazione con il valore eventualmente corretto.
        """
        if not value:
            return ValidationResult(False, "Numero PDL obbligatorio")

        # Sanitizzazione: maiuscolo e rimuovi spazi
        sanitized = value.strip().upper().replace(" ", "")

        # Intelligenza PDL: se sono solo 6 cifre, aggiungi suffisso automatico
        if sanitized.isdigit() and len(sanitized) == cls.PDL_DIGITS_ONLY:
            num = int(sanitized)
            suffix = "/S" if num < cls.PDL_SUFFIX_THRESHOLD else "/C"
            sanitized = f"{sanitized}{suffix}"

        if not re.match(cls.PATTERNS["pdl_number"], sanitized):
            return ValidationResult(
                False,
                f"PDL '{value}' non valido. Formato richiesto: 123456/C o 123456/S (o solo 6 cifre)",
            )

        return ValidationResult(True, sanitized_value=sanitized)

    @classmethod
    def validate_oda(cls, value: str) -> ValidationResult:
        """
        Valida la correttezza formale di un numero di Ordine d'Acquisto.

        Args:
          value: Numero OdA inserito.

        Returns:
          ValidationResult: Esito della validazione.
        """
        if not value:
            return ValidationResult(False, "Numero OdA obbligatorio")

        sanitized = value.strip().upper()

        if len(sanitized) > cls.ODA_MAX_LENGTH:
            return ValidationResult(False, f"Numero OdA troppo lungo (max {cls.ODA_MAX_LENGTH} caratteri)")

        if not re.match(cls.PATTERNS["oda_number"], sanitized):
            return ValidationResult(False, "Numero OdA contiene caratteri non validi")

        return ValidationResult(True, sanitized_value=sanitized)

    @classmethod
    def validate_codice_fiscale(cls, value: str) -> ValidationResult:
        """
        Valida un Codice Fiscale italiano controllando formato e carattere di controllo.

        Args:
          value: CF da validare.

        Returns:
          ValidationResult: Esito con errore descrittivo se non valido.
        """
        if not value:
            return ValidationResult(False, "Codice Fiscale obbligatorio")

        sanitized = value.strip().upper()

        if len(sanitized) != cls.CF_LENGTH:
            return ValidationResult(False, f"Codice Fiscale deve essere di {cls.CF_LENGTH} caratteri")

        if not re.match(cls.PATTERNS["codice_fiscale"], sanitized):
            return ValidationResult(False, "Formato Codice Fiscale non valido")

        # Validazione checksum (carattere di controllo)
        if not cls._validate_cf_checksum(sanitized):
            return ValidationResult(False, "Checksum Codice Fiscale non valido")

        return ValidationResult(True, sanitized_value=sanitized)

    @staticmethod
    def _validate_cf_checksum(cf: str) -> bool:
        """
        Implementa l'algoritmo di calcolo del carattere di controllo per il Codice Fiscale.

        Args:
          cf: Il codice fiscale completo (16 caratteri).

        Returns:
          bool: True se l'ultimo carattere coincide con il checksum calcolato sui primi 15.
        """
        odd_map = {
            "0": 1,
            "1": 0,
            "2": 5,
            "3": 7,
            "4": 9,
            "5": 13,
            "6": 15,
            "7": 17,
            "8": 19,
            "9": 21,
            "A": 1,
            "B": 0,
            "C": 5,
            "D": 7,
            "E": 9,
            "F": 13,
            "G": 15,
            "H": 17,
            "I": 19,
            "J": 21,
            "K": 2,
            "L": 4,
            "M": 18,
            "N": 20,
            "O": 11,
            "P": 3,
            "Q": 6,
            "R": 8,
            "S": 12,
            "T": 14,
            "U": 16,
            "V": 10,
            "W": 22,
            "X": 25,
            "Y": 24,
            "Z": 23,
        }
        even_map = {
            "0": 0,
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "A": 0,
            "B": 1,
            "C": 2,
            "D": 3,
            "E": 4,
            "F": 5,
            "G": 6,
            "H": 7,
            "I": 8,
            "J": 9,
            "K": 10,
            "L": 11,
            "M": 12,
            "N": 13,
            "O": 14,
            "P": 15,
            "Q": 16,
            "R": 17,
            "S": 18,
            "T": 19,
            "U": 20,
            "V": 21,
            "W": 22,
            "X": 23,
            "Y": 24,
            "Z": 25,
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
        """
        Valida una data in formato italiano (GG.MM.AAAA).

        Args:
          value: La data inserita.

        Returns:
          ValidationResult: Esito con valore sanitizzato (sostituisce / con .).
        """
        if not value:
            return ValidationResult(False, "Data obbligatoria")

        sanitized = value.strip().replace("/", ".")

        if not re.match(cls.PATTERNS["date_it"], sanitized):
            return ValidationResult(False, "Formato data non valido (usa GG.MM.AAAA)")

        # Verifica data valida
        try:
            datetime.strptime(sanitized, "%d.%m.%Y").replace(tzinfo=UTC)
        except ValueError:
            return ValidationResult(False, "Data non esistente")

        return ValidationResult(True, sanitized_value=sanitized)

    @classmethod
    def sanitize_sql_string(cls, value: str) -> str:
        """
        Rimuove caratteri non stampabili per prevenire errori in query SQL.

        Args:
          value: Stringa da pulire.

        Returns:
          str: Stringa contenente solo caratteri stampabili e spazi bianchi base.
        """
        if not value:
            return ""
        # Rimuovi caratteri di controllo, ma mantieni formattazione base
        return "".join(c for c in value if c.isprintable() or c in ("\n", "\r", "\t"))
