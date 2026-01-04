import pytest
import logging
from src.utils.log_humanizer import SmartLogTranslator
from src.utils.secure_logger import SensitiveDataFilter, get_secure_logger

def test_log_humanizer_categories():
    translator = SmartLogTranslator()
    
    # Test mapping categories
    _, _, cat = translator.humanize("Avvio il lavoro")
    assert cat == "start"
    
    _, _, cat = translator.humanize("Effettuo login")
    assert cat == "login"
    
    _, _, cat = translator.humanize("Cerca nel database")
    assert cat == "search"
    
    _, _, cat = translator.humanize("Scarico il file")
    assert cat == "download"
    
    _, _, cat = translator.humanize("Operazione completata con successo")
    assert cat == "success"
    
    _, _, cat = translator.humanize("Si è verificato un errore")
    assert cat == "error"
    
    _, _, cat = translator.humanize("In attesa di risposta")
    assert cat == "wait"

def test_log_humanizer_random_choice():
    translator = SmartLogTranslator()
    msg1, _, _ = translator.humanize("start")
    msg2, _, _ = translator.humanize("start")
    # Non è garantito che siano diversi, ma possiamo testare che siano nei template
    assert msg1 in SmartLogTranslator.TEMPLATES["start"]
    assert msg2 in SmartLogTranslator.TEMPLATES["start"]

def test_log_humanizer_fixit_tag():
    translator = SmartLogTranslator()
    _, tech_msg, _ = translator.humanize("Errore nelle credenziali di login")
    assert "[FIXIT:ACCOUNT]" in tech_msg

def test_secure_logger_masking():
    logger_filter = SensitiveDataFilter()
    
    # Test password masking
    record = logging.LogRecord("test", logging.INFO, "path", 1, "My password: SuperSecret123", None, None)
    logger_filter.filter(record)
    assert "***MASKED***" in record.msg
    assert "SuperSecret123" not in record.msg

    # Test token masking
    record = logging.LogRecord("test", logging.INFO, "path", 1, "token: abc-123-def", None, None)
    logger_filter.filter(record)
    assert "token=***MASKED***" in record.msg
    assert "abc-123-def" not in record.msg

    # Test CF masking
    record = logging.LogRecord("test", logging.INFO, "path", 1, "Il codice fiscale è RSSMRA80A01H501W", None, None)
    logger_filter.filter(record)
    assert "***CF_MASKED***" in record.msg
    assert "RSSMRA80A01H501W" not in record.msg

    # Test Credit Card masking
    record = logging.LogRecord("test", logging.INFO, "path", 1, "Pagamento con 1234-5678-9012-3456", None, None)
    logger_filter.filter(record)
    assert "***CARD_MASKED***" in record.msg
    assert "1234-5678-9012-3456" not in record.msg

def test_get_secure_logger():
    logger = get_secure_logger("test_secure")
    assert any(isinstance(f, SensitiveDataFilter) for f in logger.filters)
    
    # Verify singleton-like filter addition
    initial_filter_count = len(logger.filters)
    logger = get_secure_logger("test_secure")
    assert len(logger.filters) == initial_filter_count
