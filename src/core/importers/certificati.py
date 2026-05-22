"""Modulo Certificati."""

import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any, ClassVar

from src.core.importers.base import BaseImporter
from src.core.processing.base import Pipeline
from src.core.processing.certificati.steps import (
    FormatCertificatiStep,
    NormalizeCertificatiStep,
    ReadCertificatiExcelStep,
)

logger = logging.getLogger(__name__)


class CertificatiImporter(BaseImporter):
    """Importer per i Certificati Campione tramite Pipeline."""

    CERTIFICATI_CAMPIONE_MAPPING: ClassVar[dict[str, str]] = (
        NormalizeCertificatiStep.CERTIFICATI_CAMPIONE_MAPPING
    )
    CERTIFICATI_CAMPIONE_COLS: ClassVar[list[str]] = NormalizeCertificatiStep.CERTIFICATI_CAMPIONE_COLS

    @classmethod
    def import_certificati_campione(
        cls,
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, list[tuple[Any, ...]]]:
        """Importa il file Certificati Campione tramite Pipeline."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File non trovato: {file_path}", []

        try:
            logger.info(f"Avvio lettura Excel certificati via Pipeline: {file_path}")

            pipeline = Pipeline()
            pipeline.add_step(ReadCertificatiExcelStep())
            pipeline.add_step(NormalizeCertificatiStep())
            pipeline.add_step(FormatCertificatiStep())

            context = {"file_path": str(path)}
            result = pipeline.run(context)

            success = result.get("success", False)
            message = result.get("message", "Errore sconosciuto")
            rows = result.get("rows", [])

        except Exception as e:
            return False, f"Errore importazione Certificati: {e}", []
        else:
            return success, message, rows
