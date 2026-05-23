import logging

import pytest

from src.utils.secure_logger import SensitiveDataFilter, get_secure_logger


class TestSecureLogger:
    @pytest.fixture
    def data_filter(self):
        return SensitiveDataFilter()

    def test_filter_password(self, data_filter):
        record = logging.LogRecord(
            "test", logging.INFO, "path", 10, "User login with password=secret123", None, None
        )
        data_filter.filter(record)
        assert "password=***MASKED***" in record.msg

    def test_filter_cf(self, data_filter):
        record = logging.LogRecord("test", logging.INFO, "path", 10, "Found CF RSSMRA80A01H501Z", None, None)
        data_filter.filter(record)
        assert "***CF_MASKED***" in record.msg

    def test_filter_email(self, data_filter):
        record = logging.LogRecord(
            "test", logging.INFO, "path", 10, "Contact me at mario@example.com", None, None
        )
        data_filter.filter(record)
        assert "***EMAIL_MASKED***" in record.msg

    def test_filter_args(self, data_filter):
        # Test mascheramento negli argomenti del log
        record = logging.LogRecord(
            "test", logging.INFO, "path", 10, "User %s has pwd %s", ("mario", "secret"), None
        )
        # Nota: La logica attuale di _mask_value cerca i pattern anche negli argomenti
        # Ma "secret" da solo non triggera il pattern r'(token|api_key|apikey|secret)["\s:=]+...'
        # se non c'è il prefisso.

        record.args = ("mario", "password:my_pwd")
        data_filter.filter(record)
        assert record.args[1] == "password=***MASKED***"

    def test_get_secure_logger(self):
        logger = get_secure_logger("SecureTest")
        assert any(isinstance(f, SensitiveDataFilter) for f in logger.filters)

        # Seconda chiamata non deve aggiungere duplicati
        logger2 = get_secure_logger("SecureTest")
        filters = [f for f in logger2.filters if isinstance(f, SensitiveDataFilter)]
        assert len(filters) == 1
