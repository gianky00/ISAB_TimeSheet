"""Modelli dati per il Robust Test Runner."""

from __future__ import annotations

import datetime
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class FailureDetail:
    """Dettaglio strutturato di un singolo test fallito, ottimizzato per IA.

    Attributes:
        node_id: Identificatore univoco del test (es: file.py::test_name).
        file: Percorso del file di test.
        test_name: Nome della funzione di test.
        error_type: Tipo di eccezione Python.
        error_message: Messaggio d'errore sintetico.
        traceback: Traceback completo del fallimento.
        category: Categoria semantica dell'errore.
        fingerprint: Hash univoco per raggruppare errori identici.
        repro_cmd: Comando CLI per riprodurre solo questo test.
    """

    node_id: str
    file: str
    test_name: str
    error_type: str
    error_message: str
    traceback: str
    category: str  # import_error, assertion, timeout, runtime, crash
    fingerprint: str = ""
    repro_cmd: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Converte l'oggetto in un dizionario standard."""
        return asdict(self)


@dataclass
class TestResult:
    """Risultato di un singolo file/NodeID test.

    Attributes:
        target: Bersaglio del test.
        success: True se il test è passato.
        duration: Tempo di esecuzione in secondi.
        passed: Numero di test superati nel target.
        failed: Numero di test falliti nel target.
        error_msg: Eventuale messaggio d'errore globale.
        full_output: Output completo (stdout+stderr).
        timestamp: Data e ora dell'esecuzione.
    """

    target: str
    success: bool
    duration: float
    passed: int = 0
    failed: int = 0
    error_msg: str | None = None
    full_output: str | None = None
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())


@dataclass
class AIReport:
    """Report strutturato completo per consumo IA.

    Attributes:
        success: Successo globale della suite.
        total_passed: Totale test superati.
        total_failed: Totale test falliti.
        duration: Durata totale dell'intera suite.
        strategy: Strategia usata (SEQUENZIALE/PARALLELO).
        total_files: Numero di file di test processati.
        failures: Lista di FailureDetail univoci.
        failure_clusters: Mappa di errori raggruppati per fingerprint.
        file_results: Risultati sintetici per ogni file.
        system_metadata: Informazioni sull'ambiente di sistema.
        timestamp: Data e ora del report.
    """

    success: bool
    total_passed: int
    total_failed: int
    duration: float
    strategy: str  # SEQUENZIALE | PARALLELO
    total_files: int
    failures: list[dict[str, Any]]
    failure_clusters: dict[str, list[str]]
    file_results: list[dict[str, Any]]
    system_metadata: dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Converte il report in un dizionario standard."""
        return asdict(self)
