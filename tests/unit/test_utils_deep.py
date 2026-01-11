import pytest
from src.utils.security import password_manager, PasswordManager
from src.utils.document_processor import DocumentProcessor
from pathlib import Path
from unittest.mock import patch, MagicMock

class TestUtilsDeep:
    def test_password_manager_encryption(self):
        original = "Secret123!"
        encrypted = password_manager.encrypt(original)
        assert encrypted.startswith("ENC:v2:")
        decrypted = password_manager.decrypt(encrypted)
        assert decrypted == original

    def test_document_processor_text_extraction(self, tmp_path):
        pdf_path = tmp_path / "test.pdf"
        pdf_path.touch()
        
        # We need to mock fitz.open and its return object
        mock_doc = MagicMock()
        mock_page = MagicMock()
        mock_doc.__len__.return_value = 1
        mock_doc.__getitem__.return_value = mock_page
        mock_page.get_text.return_value = "Contenuto PDF"
        
        with patch("src.utils.document_processor.fitz.open", return_value=mock_doc):
            text = DocumentProcessor.extract_text(pdf_path)
            assert text == "Contenuto PDF"

    def test_password_manager_singleton(self):
        pm1 = PasswordManager()
        pm2 = PasswordManager()
        assert pm1 is pm2
