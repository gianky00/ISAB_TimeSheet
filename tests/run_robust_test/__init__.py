"""Package per l'esecuzione robusta e modulare dei test.

Questo package fornisce un orchestratore avanzato (UltraRunner) capace di
gestire esecuzioni parallele, recupero sequenziale dei test falliti,
fingerprinting degli errori e output strutturato per agenti IA.
"""

from __future__ import annotations

from .models import AIReport, FailureDetail, TestResult
from .utils import ROOT_DIR

__all__ = ["ROOT_DIR", "AIReport", "FailureDetail", "TestResult"]
