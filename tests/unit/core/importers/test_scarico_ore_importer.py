import io
import zipfile
from unittest.mock import MagicMock, patch

from src.core.importers.scarico_ore import ScaricoOreImporter


class TestScaricoOreImporter:
    def test_scan_scarico_ore_rows_not_exists(self):
        assert ScaricoOreImporter.scan_scarico_ore_rows("/non/existent.xlsx") == 0

    def test_scan_scarico_ore_rows_success(self, fs):
        # Creiamo un file .xlsx finto (ZIP)
        xlsx_path = "/test.xlsx"
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as z:
            # Structure required by scan_scarico_ore_rows
            xml = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet><dimension ref="A1:K100"/></worksheet>'
            z.writestr("xl/worksheets/sheet1.xml", xml)

        fs.create_file(xlsx_path, contents=buffer.getvalue())

        assert ScaricoOreImporter.scan_scarico_ore_rows(xlsx_path) == 100

    @patch("src.core.importers.scarico_ore.Pipeline")
    def test_import_scarico_ore_success(self, mock_pipeline, fs):
        fs.create_file("/test.xlsx")

        mock_p = MagicMock()
        mock_p.run.return_value = {
            "success": True,
            "message": "OK",
            "rows": [("2023-01-01", "P1", "P2", "123", "10", "08:00", "17:00", 8.0, "D", "NO", "C1", "{}")],
        }
        mock_pipeline.return_value = mock_p

        success, msg, rows = ScaricoOreImporter.import_scarico_ore("/test.xlsx")

        assert success is True
        assert len(rows) == 1
        assert "OK" in msg

    @patch("src.core.importers.scarico_ore.Pipeline")
    def test_import_scarico_ore_failure(self, mock_pipeline, fs):
        fs.create_file("/test.xlsx")
        mock_p = MagicMock()
        mock_p.run.return_value = {"success": False, "message": "Pipeline Crash"}
        mock_pipeline.return_value = mock_p

        success, msg, _rows = ScaricoOreImporter.import_scarico_ore("/test.xlsx")
        assert success is False
        assert msg == "Pipeline Crash"

    @patch("src.core.importers.scarico_ore.msoffcrypto")
    def test_scan_scarico_ore_rows_encrypted(self, mock_crypto, fs):
        xlsx_path = "/test_enc.xlsx"
        fs.create_file(xlsx_path, contents=b"encrypted content")

        # Simula msoffcrypto
        mock_file = MagicMock()
        mock_crypto.OfficeFile.return_value = mock_file

        # Setup decrypted buffer (valid ZIP)
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as z:
            z.writestr("xl/worksheets/sheet1.xml", b'<dimension ref="A1:K50"/>')

        def mock_decrypt(out_buf):
            out_buf.write(buffer.getvalue())

        mock_file.decrypt.side_effect = mock_decrypt

        # Forza errore nel primo scan zip (file criptato non è un zip valido)
        # scan_scarico_ore_rows proverà il fallback crypto

        with patch(
            "src.core.importers.scarico_ore.zipfile.ZipFile", side_effect=[zipfile.BadZipFile(), MagicMock()]
        ):
            # No, la logica interna chiama _scan_zip(path) poi fallback
            # Forziamo BadZipFile nel primo blocco
            pass

        # Proviamo direttamente
