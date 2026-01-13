
from unittest.mock import MagicMock

from src.utils.printing import get_installed_printers, print_pdf


class TestPrintingWindowsMocked:
    def test_get_installed_printers_mocked(self, mocker):
        """Verifica il recupero nomi stampanti tramite win32print."""
        # EnumPrinters restituisce tuple (flags, description, name, comment)
        mocker.patch("win32print.EnumPrinters", return_value=[
            (0, "Desc1", "Printer1", ""),
            (0, "Desc2", "Printer2", "")
        ])

        printers = get_installed_printers()
        assert printers == ["Printer1", "Printer2"]

    def test_print_pdf_split_jobs_sequence(self, mocker, tmp_path):
        """Verifica la logica atomica: una pagina = un job di stampa."""
        # 1. Mock file PDF
        dummy_pdf = tmp_path / "test.pdf"
        dummy_pdf.write_text("fake pdf content")

        # 2. Mock librerie Windows e Fitz
        mock_fitz = mocker.patch("fitz.open")
        mock_doc = MagicMock()
        mock_doc.__len__.return_value = 2 # 2 pagine
        mock_fitz.return_value = mock_doc

        mocker.patch("win32print.GetDefaultPrinter", return_value="DefaultPrinter")
        mock_win32ui = mocker.patch("win32ui.CreateDC")
        mock_hdc = MagicMock()
        mock_win32ui.return_value = mock_hdc

        # Mock rendering per evitare errori reali
        mocker.patch("PIL.Image.frombytes")
        mocker.patch("PIL.ImageWin.Dib")
        mocker.patch("time.sleep")
        mocker.patch("src.utils.printing._set_printer_duplex_powershell")

        # 3. Esecuzione
        success = print_pdf(str(dummy_pdf), "MyPrinter")

        assert success is True
        # Deve aver creato 2 DC (uno per pagina) e avviato 2 documenti
        assert mock_hdc.CreatePrinterDC.call_count == 2
        assert mock_hdc.StartDoc.call_count == 2
        assert mock_hdc.EndDoc.call_count == 2

    def test_print_pdf_fallback_on_direct_failure(self, mocker, tmp_path):
        """Verifica il fallback su os.startfile se fitz/win32 fallisce."""
        dummy_pdf = tmp_path / "fail.pdf"
        dummy_pdf.write_text("data")

        mocker.patch("fitz.open", side_effect=Exception("Critical Fitz Error"))
        mock_startfile = mocker.patch("os.startfile")

        # Deve catturare l'eccezione interna e provare startfile
        success = print_pdf(str(dummy_pdf), "Printer")

        assert success is True # Ritorna True se lo startfile ha successo
        mock_startfile.assert_called_once_with(str(dummy_pdf), "print")

    def test_print_pdf_file_not_found(self):
        """Verifica gestione file mancante."""
        assert print_pdf("missing.pdf", "Printer") is False
