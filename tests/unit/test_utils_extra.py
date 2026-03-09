import logging
import pytest
from src.utils.log_humanizer import SmartLogTranslator
from src.utils.secure_logger import SensitiveDataFilter, get_secure_logger

def test_log_humanizer_categories():
    """Verifica che tutte le categorie restituiscano stringhe non vuote."""
    # In V9.0 usiamo categorie reali: download, error, success, action, search, wait
    messages = ["scarico", "errore", "successo", "click", "ricerca", "attesa"]
    for m in messages:
        h, _, _ = SmartLogTranslator.humanize(m)
        assert isinstance(h, str)
        assert len(h) > 0

def test_log_humanizer_unknown_category():
    """Verifica fallback su categoria sconosciuta (info)."""
    h, _, c = SmartLogTranslator.humanize("Messaggio generico")
    assert c == "info"
    assert h == "Messaggio generico"

def test_log_humanizer_deterministic_choice():
    """Verifica che la scelta sia deterministica in V9.0 (niente varianti casuali)."""
    results = {SmartLogTranslator.humanize("errore")[0] for _ in range(50)}
    # In V9.0 c'è solo 1 variante per messaggio
    assert len(results) == 1

def test_secure_logger_masking_via_filter():
    """Verifica mascheramento dati sensibili tramite filtro."""
    filt = SensitiveDataFilter()

    # Test Codice Fiscale
    msg = "Il CF è RSSMRA80A01L219Z"
    record = logging.LogRecord("name", logging.INFO, "path", 10, msg, None, None)
    filt.filter(record)
    assert "RSSMRA80A01L219Z" not in record.msg
    assert "***CF_MASKED***" in record.msg

    # Test Password
    msg2 = "L'utente ha password segreta123"
    record2 = logging.LogRecord("name", logging.INFO, "path", 10, msg2, None, None)
    filt.filter(record2)
    assert "segreta123" not in record2.msg
    assert "password=***MASKED***" in record2.msg

def test_get_secure_logger():
    """Verifica inizializzazione e recupero logger sicuro."""
    logger = get_secure_logger("TestLogger")
    assert logger is not None
    assert any(isinstance(f, SensitiveDataFilter) for f in logger.filters)
