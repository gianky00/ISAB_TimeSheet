from typing import Callable, Dict, List, Optional, Tuple

from src.core.importers.attivita import AttivitaImporter
from src.core.importers.base import BaseImporter
from src.core.importers.certificati import CertificatiImporter
from src.core.importers.contabilita import ContabilitaImporter
from src.core.importers.giornaliere import GiornaliereImporter
from src.core.importers.scarico_ore import ScaricoOreImporter
from src.core.importers.storico_oda import StoricoOdaImporter


class ExcelImporter:
    """
    Facade per l'importazione di dati da file Excel.
    Delega ai moduli specifici in src/core/importers/.
    Mantiene la compatibilità con il codice esistente.
    """

    # --- Contabilità ---
    COLUMNS_MAPPING = ContabilitaImporter.COLUMNS_MAPPING

    @staticmethod
    def import_contabilita_dati(
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, list, list]:
        return ContabilitaImporter.import_contabilita_dati(file_path, progress_callback)

    # --- Giornaliere ---
    GIORNALIERE_MAPPING = GiornaliereImporter.GIORNALIERE_MAPPING

    @staticmethod
    def import_giornaliere(
        root_path: str,
        lookup_map: Dict,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, List[Tuple], List[int]]:
        return GiornaliereImporter.import_giornaliere(
            root_path, lookup_map, progress_callback
        )

    # --- Attività Programmate ---
    ATTIVITA_PROGRAMMATE_MAPPING = AttivitaImporter.ATTIVITA_PROGRAMMATE_MAPPING
    ATTIVITA_PROGRAMMATE_COLS = AttivitaImporter.ATTIVITA_PROGRAMMATE_COLS

    @staticmethod
    def import_attivita_programmate(
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, List[Tuple]]:
        return AttivitaImporter.import_attivita_programmate(file_path, progress_callback)

    # --- Scarico Ore ---
    SCARICO_ORE_COLS = ScaricoOreImporter.SCARICO_ORE_COLS

    @staticmethod
    def import_scarico_ore(
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, List[Tuple]]:
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
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, List[Tuple]]:
        return CertificatiImporter.import_certificati_campione(file_path, progress_callback)

    # --- Storico OdA ---
    STORICO_ODA_MAPPING = StoricoOdaImporter.STORICO_ODA_MAPPING
    STORICO_ODA_COLS = StoricoOdaImporter.STORICO_ODA_COLS

    @staticmethod
    def import_storico_oda(
        file_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> Tuple[bool, str, List[Tuple]]:
        return StoricoOdaImporter.import_storico_oda(file_path, progress_callback)

    # --- Helpers Vari ---
    @staticmethod
    def scan_workload(file_path: str, giornaliere_path: str) -> Tuple[int, int]:
        sheets = ContabilitaImporter.scan_sheets(file_path)
        files = GiornaliereImporter.scan_files(giornaliere_path)
        return sheets, files
