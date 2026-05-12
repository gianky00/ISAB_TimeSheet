"""
Filtri per sicurezza e privacy.
"""

import re
from collections.abc import Sequence
from re import Pattern
from typing import Any, ClassVar


class SensitiveDataFilter:
    """
    Filtro per mascherare dati sensibili nei log.

    Identifica e maschera:
    - Password, token, API keys
    - Codici fiscali italiani
    - Numeri carte di credito
    - Email addresses
    - Numeri telefono
    - IBAN
    """

    PATTERNS: ClassVar[list[tuple[Pattern[str], str]]] = [
        # Password in vari formati
        (
            re.compile(r'(password|passwd|pwd)["\s:=]+["\']?[\w@#$%^&*!]+["\']?', re.IGNORECASE),
            r"\1=***MASKED***",
        ),
        # Token/API keys
        (
            re.compile(
                r'(token|api_key|apikey|secret|auth)["\s:=]+["\']?[\w\-._]+["\']?',
                re.IGNORECASE,
            ),
            r"\1=***MASKED***",
        ),
        # Codici fiscali italiani
        (
            re.compile(r"\b[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]\b"),
            "***CF_MASKED***",
        ),
        # Numeri di carta di credito (4 gruppi di 4 cifre)
        (
            re.compile(r"\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b"),
            "***CARD_MASKED***",
        ),
        # Email addresses
        (
            re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Z|a-z]{2,}\b"),
            "***EMAIL_MASKED***",
        ),
        # Numeri telefono italiani
        (
            re.compile(r"\b(\+39[\s\-]?)?[0-9]{2,4}[\s\-]?[0-9]{6,8}\b"),
            "***PHONE_MASKED***",
        ),
        # IBAN
        (
            re.compile(r"\b[A-Z]{2}[0-9]{2}[A-Z0-9]{10,30}\b"),
            "***IBAN_MASKED***",
        ),
    ]

    SENSITIVE_KEYS: ClassVar[set[str]] = {
        "password",
        "passwd",
        "pwd",
        "token",
        "api_key",
        "apikey",
        "secret",
        "auth",
        "authorization",
        "credential",
        "private_key",
        "session_key",
    }

    @classmethod
    def mask_string(cls, text: str) -> str:
        """
        Maschera dati sensibili in una stringa.

        Args:
          text: Stringa da processare

        Returns:
          Stringa con dati sensibili mascherati
        """

        masked = text
        for pattern, replacement in cls.PATTERNS:
            masked = pattern.sub(replacement, masked)

        return masked

    @classmethod
    def mask_dict(cls, data: dict[str, Any]) -> dict[str, Any]:
        """
        Maschera dati sensibili in un dizionario (ricorsivo).

        Args:
          data: Dizionario da processare

        Returns:
          Nuovo dizionario con dati sensibili mascherati
        """

        masked: dict[str, Any] = {}
        for key, value in data.items():
            # Se la chiave  sensibile, maschera il valore
            if any(sensitive_key in key.lower() for sensitive_key in cls.SENSITIVE_KEYS):
                masked[key] = "***MASKED***"
            # Altrimenti processa il valore ricorsivamente
            elif isinstance(value, dict):
                masked[key] = cls.mask_dict(value)
            elif isinstance(value, str):
                masked[key] = cls.mask_string(value)
            elif isinstance(value, (list, tuple)):
                masked[key] = cls.mask_list(value)
            else:
                masked[key] = value

        return masked

    @classmethod
    def mask_list(cls, data: Sequence[Any]) -> list[Any]:
        """
        Maschera dati sensibili in una lista (ricorsivo).

        Args:
          data: Lista da processare

        Returns:
          Nuova lista con dati sensibili mascherati
        """

        masked: list[Any] = []
        for item in data:
            if isinstance(item, dict):
                masked.append(cls.mask_dict(item))
            elif isinstance(item, str):
                masked.append(cls.mask_string(item))
            elif isinstance(item, (list, tuple)):
                masked.append(cls.mask_list(item))
            else:
                masked.append(item)

        return masked

    @classmethod
    def mask(cls, data: Any) -> Any:
        """
        Maschera dati sensibili in qualsiasi tipo di dato.

        Args:
          data: Dato da processare (str, dict, list, o altro)

        Returns:
          Dato con informazioni sensibili mascherate
        """
        if isinstance(data, str):
            return cls.mask_string(data)
        if isinstance(data, dict):
            return cls.mask_dict(data)
        if isinstance(data, (list, tuple)):
            return cls.mask_list(data)
        return data


class SamplingFilter:
    """
    Filtro per sampling dei log (riduce volume).

    Utile per log ad alto volume (es: ogni riga processata).
    """

    def __init__(self, sample_rate: float = 1.0) -> None:
        """
        Inizializza filter.

        Args:
          sample_rate: Percentuale di log da mantenere (0.0-1.0)
                1.0 = 100% (tutti), 0.01 = 1%
        """
        self.sample_rate = max(0.0, min(1.0, sample_rate))
        self._counter = 0

    def should_log(self) -> bool:
        """
        Determina se il log corrente dovrebbe essere scritto.

        Returns:
          True se il log deve essere scritto, False altrimenti
        """
        if self.sample_rate >= 1.0:
            return True

        if self.sample_rate <= 0.0:
            return False

        # Sampling deterministico: 1 ogni N
        self._counter += 1
        threshold = int(1.0 / self.sample_rate)
        return (self._counter % threshold) == 0
