"""Unit tests for ZipCompressor."""

import zipfile
from pathlib import Path

import pytest

from src.core.backup.zip_compressor import ZipCompressor


def test_compress_directory_excludes_correctly(tmp_path: Path) -> None:
    """Verifica che la compressione includa solo estensioni valide ed escluda cartelle vietate."""
    # Setup cartella sorgente
    source = tmp_path / "source"
    source.mkdir()

    # Creazione file inclusi
    (source / "db.db").write_text("sqlite db content")
    (source / "config.json").write_text('{"key": "value"}')
    (source / "data.dat").write_text("binary data")

    # Creazione file con estensione esclusa
    (source / "readme.txt").write_text("should be ignored")

    # Creazione cartella esclusa
    logs_dir = source / "logs"
    logs_dir.mkdir()
    (logs_dir / "app.db").write_text("should not be included because it is inside logs")

    # Target zip
    target_zip = tmp_path / "backup.zip"

    # Esegui compressione
    count = ZipCompressor.compress_directory(source, target_zip)

    assert count == 3
    assert target_zip.exists()
    assert zipfile.is_zipfile(target_zip)

    # Verifica contenuto dello zip
    with zipfile.ZipFile(target_zip, "r") as z:
        files = z.namelist()
        assert "db.db" in files
        assert "config.json" in files
        assert "data.dat" in files
        assert "readme.txt" not in files
        assert "logs/app.db" not in files


def test_extract_archive_success(tmp_path: Path) -> None:
    """Verifica il ripristino/estrazione di uno zip valido."""
    # Crea zip fake
    zip_path = tmp_path / "test.zip"
    with zipfile.ZipFile(zip_path, "w") as z:
        z.writestr("test_file.db", "restored content")

    dest_dir = tmp_path / "dest"
    dest_dir.mkdir()

    ZipCompressor.extract_archive(zip_path, dest_dir)

    extracted_file = dest_dir / "test_file.db"
    assert extracted_file.exists()
    assert extracted_file.read_text() == "restored content"


def test_extract_archive_invalid_raises_error(tmp_path: Path) -> None:
    """Verifica che l'estrazione di un archivio non valido sollevi ValueError."""
    bad_zip = tmp_path / "bad.zip"
    bad_zip.write_text("not a zip file content")

    dest_dir = tmp_path / "dest"
    dest_dir.mkdir()

    with pytest.raises(ValueError, match="File non valido o corrotto"):
        ZipCompressor.extract_archive(bad_zip, dest_dir)
