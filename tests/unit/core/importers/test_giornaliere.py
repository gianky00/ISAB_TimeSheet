from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.application.services.importers.giornaliere import GiornaliereImporter


class TestGiornaliereImporter:
    @patch("src.application.services.importers.giornaliere.Path")
    def test_scan_files_no_path(self, mock_path):
        """Testa scan_files con path nullo o inesistente."""
        assert GiornaliereImporter.scan_files(None) == 0

        mock_instance = mock_path.return_value
        mock_instance.exists.return_value = False
        assert GiornaliereImporter.scan_files("/invalid/path") == 0

    @patch("src.application.services.importers.giornaliere.Path")
    def test_scan_files_valid_structure(self, mock_path):
        """Testa scan_files con una struttura di cartelle valida."""
        mock_root = MagicMock()
        mock_path.return_value = mock_root
        mock_root.exists.return_value = True

        # Mock cartelle: una valida, una vecchia, una futura, un file
        mock_folder_2025 = MagicMock()
        mock_folder_2025.is_dir.return_value = True
        mock_folder_2025.name = "Giornaliere 2025"
        mock_folder_2025.glob.return_value = [Path("file1.xlsx"), Path("file2.xls")]

        mock_folder_old = MagicMock()
        mock_folder_old.is_dir.return_value = True
        mock_folder_old.name = "Giornaliere 2020"  # < MIN_IMPORT_YEAR (2025)

        mock_folder_future = MagicMock()
        mock_folder_future.is_dir.return_value = True
        mock_folder_future.name = f"Giornaliere {datetime.now(UTC).year + 1}"

        mock_file = MagicMock()
        mock_file.is_dir.return_value = False

        mock_root.iterdir.return_value = [mock_folder_2025, mock_folder_old, mock_folder_future, mock_file]

        count = GiornaliereImporter.scan_files("/fake/path")
        assert count == 2

    @patch("src.application.services.importers.giornaliere.Path")
    def test_import_giornaliere_not_found(self, mock_path):
        """Testa import_giornaliere con directory non trovata."""
        mock_root = MagicMock()
        mock_path.return_value = mock_root
        mock_root.exists.return_value = False

        success, msg, _rows, _years = GiornaliereImporter.import_giornaliere("/fake", {})
        assert success is False
        assert "non trovata" in msg

    @patch("src.application.services.importers.giornaliere.GiornaliereImporter._run_parallel_import")
    @patch("src.application.services.importers.giornaliere.Path")
    def test_import_giornaliere_empty(self, mock_path, mock_run_parallel):
        """Testa import_giornaliere quando non ci sono task."""
        mock_root = MagicMock()
        mock_path.return_value = mock_root
        mock_root.exists.return_value = True
        mock_root.iterdir.return_value = []

        success, msg, rows, years = GiornaliereImporter.import_giornaliere("/fake", {})
        assert success is True
        assert "Nessuna nuova giornaliera" in msg
        assert rows == []
        assert years == []

    @patch("src.application.services.processing.giornaliere.steps.NormalizeGiornalieraStep")
    def test_normalize_giornaliera_columns_alias(self, mock_step_class):
        """Testa l'alias per la normalizzazione colonne."""
        import pandas as pd

        mock_step = mock_step_class.return_value
        df = pd.DataFrame({"A": [1]})

        res = GiornaliereImporter._normalize_giornaliera_columns(df)
        assert mock_step.execute.called
        assert isinstance(res, pd.DataFrame)

    @patch("src.application.services.importers.giornaliere.Path")
    def test_collect_giornaliere_tasks(self, mock_path):
        """Testa la raccolta dei task di importazione."""
        mock_root = MagicMock()
        mock_path.return_value = mock_root

        mock_folder = MagicMock()
        mock_folder.is_dir.return_value = True
        mock_folder.name = "Giornaliere 2025"
        mock_file = MagicMock()
        mock_file.name = "test.xlsx"
        mock_folder.glob.return_value = [mock_file]

        mock_root.iterdir.return_value = [mock_folder]

        tasks = GiornaliereImporter._collect_giornaliere_tasks(mock_root, {"k": "v"})
        assert len(tasks) == 1
        assert tasks[0][0] == 2025
        assert tasks[0][1] == mock_file
        assert tasks[0][2] == {"k": "v"}
