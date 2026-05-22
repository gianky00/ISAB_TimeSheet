"""Zip Compressor.

Gestisce la compressione fisica in formato ZIP e l'estrazione sicura per i file di backup.
"""

import os
import zipfile
from pathlib import Path
from typing import ClassVar

from src.core.logging import get_logger

logger = get_logger("ZipCompressor")


class ZipCompressor:
    """Gestore di basso livello per le operazioni di compressione ed estrazione ZIP."""

    # Cartelle da escludere dal backup
    EXCLUDE_DIRS: ClassVar[list[str]] = ["chrome_profile", "logs", "cache"]

    # Estensioni file critici da includere
    INCLUDE_EXT: ClassVar[list[str]] = [".db", ".json", ".dat"]

    @staticmethod
    def compress_directory(source_dir: Path, target_zip: Path) -> int:
        """Comprime i file validi presenti nella directory sorgente all'interno dello zip di destinazione.

        Args:
            source_dir: Percorso sorgente da comprimere.
            target_zip: Percorso del file ZIP da creare.

        Returns:
            Il numero di file scritti con successo nell'archivio.
        """
        file_count = 0
        with zipfile.ZipFile(target_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                # Filtra le directory escluse in-place per os.walk
                dirs[:] = [d for d in dirs if d not in ZipCompressor.EXCLUDE_DIRS]

                for file in files:
                    file_path = Path(root) / file
                    if file_path.suffix in ZipCompressor.INCLUDE_EXT:
                        arcname = file_path.relative_to(source_dir)
                        zipf.write(file_path, arcname)
                        file_count += 1
        return file_count

    @staticmethod
    def extract_archive(zip_path: Path, target_dir: Path) -> None:
        """Esegue l'estrazione sicura di un archivio ZIP all'interno della cartella di destinazione.

        Args:
            zip_path: Percorso del file ZIP da estrarre.
            target_dir: Percorso di destinazione per l'estrazione.
        """
        if not zipfile.is_zipfile(zip_path):
            raise ValueError("File non valido o corrotto.")

        with zipfile.ZipFile(zip_path, "r") as zipf:
            zipf.extractall(target_dir)
