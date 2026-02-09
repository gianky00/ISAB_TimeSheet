from collections.abc import Callable
from typing import Any, Optional

from src.core.importers.attivita import AttivitaImporter
from src.core.importers.certificati import CertificatiImporter
from src.core.importers.contabilita import ContabilitaImporter
from src.core.importers.giornaliere import GiornaliereImporter
from src.core.importers.scarico_ore import ScaricoOreImporter
from src.core.importers.storico_oda import StoricoOdaImporter


class ExcelImporter:
    """
    Facade per l'importazione di dati da file Excel.
    Delega ai moduli specifici in src/core/importers/.
    Mantiene la compatibilitÃ  con il codice esistente.
    """

    # --- ContabilitÃ  ---
    COLUMNS_MAPPING = ContabilitaImporter.COLUMNS_MAPPING

    @staticmethod
    def import_contabilita_dati(
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, list[tuple[Any, ...]], list[int]]:
        """
        Importa i dati di contabilitÃ  dal file specificato.

        Returns:
            Tuple: (success, message, data_rows, years_found)
        """
        return ContabilitaImporter.import_contabilita_dati(file_path, progress_callback)

    # --- Giornaliere ---
    GIORNALIERE_MAPPING = GiornaliereImporter.GIORNALIERE_MAPPING

    @staticmethod
    def import_giornaliere(
        root_path: str,
        lookup_map: dict[str, str],
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, list[tuple[Any, ...]], list[int]]:
        """
        Importa le giornaliere ricorsivamente dalla root path.

        Returns:
            Tuple: (success, message, rows, years_cleared)
        """
        return GiornaliereImporter.import_giornaliere(root_path, lookup_map, progress_callback)

    # --- AttivitÃ  Programmate ---
    ATTIVITA_PROGRAMMATE_MAPPING = AttivitaImporter.ATTIVITA_PROGRAMMATE_MAPPING
    ATTIVITA_PROGRAMMATE_COLS = AttivitaImporter.ATTIVITA_PROGRAMMATE_COLS

    @staticmethod
    def import_attivita_programmate(
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, list[tuple[Any, ...]]]:
        """Importa la programmazione attivitÃ ."""
        return AttivitaImporter.import_attivita_programmate(file_path, progress_callback)

    # --- Scarico Ore ---
    SCARICO_ORE_COLS = ScaricoOreImporter.SCARICO_ORE_COLS

    @staticmethod
    def import_scarico_ore(
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, list[tuple[Any, ...]]]:
        """Importa il file di scarico ore massivo."""
        return ScaricoOreImporter.import_scarico_ore(file_path, progress_callback)

    @staticmethod
    def scan_scarico_ore_rows(file_path: str) -> int:
        return ScaricoOreImporter.scan_scarico_ore_rows(file_path)

    # --- Certificati ---
    CERTIFICATI_CAMPIONE_MAPPING = CertificatiImporter.CERTIFICATI_CAMPIONE_MAPPING
    CERTIFICATI_CAMPIONE_COLS = CertificatiImporter.CERTIFICATI_CAMPIONE_COLS

    @staticmethod
    def import_certificati_campione(
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, list[tuple[Any, ...]]]:
        return CertificatiImporter.import_certificati_campione(file_path, progress_callback)

    # --- Storico OdA ---
    STORICO_ODA_MAPPING = StoricoOdaImporter.STORICO_ODA_MAPPING
    STORICO_ODA_COLS = StoricoOdaImporter.STORICO_ODA_COLS

    @staticmethod
    def import_storico_oda(
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, list[tuple[Any, ...]]]:
        return StoricoOdaImporter.import_storico_oda(file_path, progress_callback)

    # --- Helpers Vari ---
    @staticmethod
    def scan_workload(file_path: str, giornaliere_path: str) -> tuple[int, int]:
        sheets = ContabilitaImporter.scan_sheets(file_path)
        files = GiornaliereImporter.scan_files(giornaliere_path)
        return sheets, files
