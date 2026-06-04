"""SyncroJob - Timesheet Processing Logic (VBA Replacement).

Replica fedelmente la logica VBA "ProcessTimesheetFiles" per elaborazione, pulizia e rinomina.
"""

from contextlib import suppress
from pathlib import Path

from src.application.services.processing.timesheet.pipeline import TimesheetProcessingPipeline
from src.infrastructure.utils.secure_logger import get_secure_logger

logger = get_secure_logger("TimesheetProcessor")


class TimesheetProcessor:
    """Classe per elaborare i file timesheet delegando alla Pipeline."""

    @staticmethod
    def process_and_move(file_path: Path, dest_dir: Path) -> tuple[bool, str]:
        """Elabora il file Excel utilizzando la pipeline e lo salva nella destinazione."""
        if not file_path.exists():
            return False, f"File sorgente non trovato: {file_path}"

        try:
            # Inizializzazione Pipeline (Pattern SRP)
            pipeline = TimesheetProcessingPipeline()

            # Esecuzione della Pipeline
            context = pipeline.execute(file_path, dest_dir)

            if context.get("is_empty", False):
                return False, "EMPTY: Nessun dato registrato nel Timesheet per l'ODC inserito."

            dest_path = context.get("dest_path")
            if not dest_path:
                return False, "Errore durante il salvataggio del file."

            # Pulizia file sorgente
            TimesheetProcessor._cleanup_source(file_path, dest_path)
        except Exception as e:
            logger.exception(f"Errore elaborazione {file_path.name}")
            return False, str(e)
        else:
            return True, f"Salvato in: {dest_path.name}"

    @staticmethod
    def _cleanup_source(src: Path, dest: Path) -> None:
        """Rimuove il file sorgente se diverso dalla destinazione."""
        with suppress(Exception):
            if src.resolve() != dest.resolve():
                src.unlink()

    @staticmethod
    def _clean_pos_value(val: str | None) -> str:
        """Alias per retrocompatibilità con i test."""
        from src.application.services.processing.timesheet.steps import ExtractMetadataStep  # noqa: PLC0415

        return ExtractMetadataStep()._clean_pos_value(val)
