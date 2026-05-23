import logging

from src.utils.secure_logger import SensitiveDataFilter, get_secure_logger


class TestSecureLogger:
    def test_sensitive_data_filter_msg_masking(self):
        filter_obj = SensitiveDataFilter()

        # Test Password
        record = logging.LogRecord("test", logging.INFO, "path", 1, "User password: mysecret123", None, None)
        filter_obj.filter(record)
        assert "***MASKED***" in record.msg
        assert "mysecret123" not in record.msg

        # Test CF
        record = logging.LogRecord("test", logging.INFO, "path", 1, "CF: RSSMRA80A01H501Z", None, None)
        filter_obj.filter(record)
        assert "***CF_MASKED***" in record.msg

        # Test Email
        record = logging.LogRecord(
            "test", logging.INFO, "path", 1, "Contact me at mario.rossi@example.com", None, None
        )
        filter_obj.filter(record)
        assert "***EMAIL_MASKED***" in record.msg

    def test_sensitive_data_filter_args_masking(self):
        filter_obj = SensitiveDataFilter()

        # Test Args
        record = logging.LogRecord(
            "test", logging.INFO, "path", 1, "Login with %s", ("my_token_abc123",), None
        )
        # In LogRecord, args is a tuple.
        # But wait, SensitiveDataFilter handles tokens specifically
        record.msg = "token: %s"
        record.args = ("abc-123-token",)

        filter_obj.filter(record)
        # Note: the filter in _mask_value uses the same PATTERNS.
        # For tokens it replaces with \1=***MASKED***.
        # But "abc-123-token" alone might not match the token pattern which expects "token:" prefix.
        # Let's check the pattern: re.compile(r'(token|api_key|...)["\s:=]+["\']?[\w-]+["\']?')

        # If I pass a full string as arg:
        record.args = ("token=abc-123",)
        filter_obj.filter(record)
        assert "token=***MASKED***" in record.args[0]

    def test_get_secure_logger(self):
        logger = get_secure_logger("secure_test")
        assert any(isinstance(f, SensitiveDataFilter) for f in logger.filters)

        # Re-getting should not add another filter
        count = len(logger.filters)
        logger2 = get_secure_logger("secure_test")
        assert len(logger2.filters) == count
