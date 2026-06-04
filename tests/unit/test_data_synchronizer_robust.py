import pytest

from src.application.services.exceptions import ValidationError
from src.application.services.sync.base import BaseSyncEngine


class TestDataSynchronizerRobust:
    def test_validate_identifier(self):
        # Test valid identifiers
        assert BaseSyncEngine._validate_identifier("table_name") == "table_name"
        assert BaseSyncEngine._validate_identifier("col1") == "col1"

        # Test invalid identifiers
        with pytest.raises(ValidationError):
            BaseSyncEngine._validate_identifier("table name")
        with pytest.raises(ValidationError):
            BaseSyncEngine._validate_identifier("table; DROP")
        with pytest.raises(ValidationError):
            BaseSyncEngine._validate_identifier("col-1")

    def test_clean_value(self):
        assert BaseSyncEngine._clean_value(None) == ""
        assert BaseSyncEngine._clean_value(10) == "10"
        assert BaseSyncEngine._clean_value("  text  ") == "text"
