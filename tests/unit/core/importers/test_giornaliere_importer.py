from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.core.importers.giornaliere import GiornaliereImporter


class TestGiornaliereImporter:
    @pytest.fixture
    def mock_fs(self, fs):
        root = Path("/giornaliere")
        fs.create_dir(str(root))
        # Cartella 2025 (valida)
        y2025 = root / "Giornaliere 2025"
        fs.create_dir(str(y2025))
        fs.create_file(str(y2025 / "test1.xlsx"))
        # Cartella 2024 (troppo vecchia)
        y2024 = root / "Giornaliere 2024"
        fs.create_dir(str(y2024))
        fs.create_file(str(y2024 / "old.xlsx"))
        return root

    def test_scan_files(self, mock_fs):
        count = GiornaliereImporter.scan_files(str(mock_fs))
        # Deve trovare solo il file in 2025
        assert count == 1

    @patch("src.core.importers.giornaliere.ProcessPoolExecutor")
    def test_import_giornaliere_orchestration(self, mock_executor, mock_fs):
        mock_instance = mock_executor.return_value.__enter__.return_value
        # Simula risultato di _process_single_giornaliera
        mock_instance.map.return_value = [(2025, [(2025, "row")], None)]

        lookup = {"desc": "1"}
        success, _msg, rows, years = GiornaliereImporter.import_giornaliere(str(mock_fs), lookup)

        assert success is True
        assert 2025 in years
        assert len(rows) == 1

    @patch("src.core.importers.giornaliere.Pipeline")
    @patch("src.core.importers.giornaliere.BaseImporter._decrypt_if_encrypted")
    def test_process_single_giornaliera_success(self, mock_decrypt, mock_pipeline, fs):
        file_path = Path("test.xlsx")
        fs.create_file(str(file_path))
        mock_decrypt.return_value = (MagicMock(), False)

        # Setup mock pipeline
        mock_p = MagicMock()
        mock_p.run.return_value = {"success": True, "rows": [(2025, "R1")]}
        mock_pipeline.return_value = mock_p

        res = GiornaliereImporter._process_single_giornaliera((2025, file_path, {}))

        assert res[0] == 2025
        assert len(res[1]) == 1
        assert res[2] is None

    @patch("src.core.importers.giornaliere.Pipeline")
    def test_process_single_giornaliera_failure(self, mock_pipeline, fs):
        file_path = Path("test.xlsx")
        fs.create_file(str(file_path))

        mock_p = MagicMock()
        mock_p.run.return_value = {"success": False, "message": "Read Error"}
        mock_pipeline.return_value = mock_p

        res = GiornaliereImporter._process_single_giornaliera((2025, file_path, {}))
        assert res[1] == []
        assert res[2] == "Read Error"

    def test_collect_giornaliere_tasks(self, mock_fs):
        tasks = GiornaliereImporter._collect_giornaliere_tasks(mock_fs, {})
        assert len(tasks) == 1
        assert tasks[0][0] == 2025
        assert "test1.xlsx" in str(tasks[0][1])
