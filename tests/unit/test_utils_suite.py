import datetime
import logging
import sys
from unittest.mock import patch

from src.utils.helpers import (
    format_timestamp,
    get_app_icon_path,
    get_months_list,
    get_years_list,
    is_windows,
    open_folder,
    safe_str,
    sanitize_filename,
    setup_logging,
    truncate_string,
)
from src.utils.parsing import parse_currency
from src.utils.validators import InputValidator


class TestUtilsHelpers:
    def test_sanitize_filename(self):
        assert sanitize_filename("normal_file.txt") == "normal_file.txt"
        assert sanitize_filename("File Con Spazi.pdf") == "File Con Spazi.pdf"
        sanitized = sanitize_filename("..\\../traversal.txt")
        assert ".." not in sanitized
        assert "\\" not in sanitized
        assert "/" not in sanitized
        assert sanitize_filename("invalid|chars<>?*.txt") == "invalid_chars_.txt"
        assert sanitize_filename(None) == "unnamed_file"
        assert sanitize_filename("") == "unnamed_file"
        assert sanitize_filename("file...txt") == "file.txt"
        assert sanitize_filename("   space_at_ends.txt   ") == "space_at_ends.txt"

    def test_get_app_icon_path(self):
        with (
            patch("src.utils.helpers.Path.exists", return_value=True),
            patch("sys.frozen", False, create=True),
        ):
            path = get_app_icon_path()
            assert path is not None
            assert "assets" in path
            assert "app.ico" in path

        with patch("src.utils.helpers.Path.exists", return_value=False):
            assert get_app_icon_path() is None

    def test_setup_logging(self):
        # Test basic setup
        logger = setup_logging("TestLogger")
        assert logger.name == "TestLogger"
        assert logger.level == logging.INFO
        assert len(logger.handlers) >= 1

        # Test with file handler
        with patch("logging.FileHandler") as mock_handler:
            setup_logging("FileLogger", log_file="test.log")
            mock_handler.assert_called_with("test.log", encoding="utf-8")

    def test_format_timestamp(self):
        dt = datetime.datetime(2023, 1, 1, 12, 30, 0)
        assert format_timestamp(dt) == "01/01/2023 12:30:00"
        now_str = format_timestamp()
        assert len(now_str) == 19  # noqa: PLR2004

    def test_get_months_list(self):
        months = get_months_list()
        assert len(months) == 12  # noqa: PLR2004
        assert months[0] == "Gennaio"

    def test_get_years_list(self):
        current_year = datetime.datetime.now().year
        years = get_years_list(-1, 1)
        assert len(years) == 3  # noqa: PLR2004
        assert str(current_year) in years

    def test_is_windows(self):
        expected = sys.platform.startswith("win")
        assert is_windows() == expected

    def test_open_folder(self):
        with patch("os.path.exists", return_value=False):
            assert open_folder("/invalid/path") is False

        with patch("os.path.exists", return_value=True):
            if sys.platform.startswith("win"):
                with patch("os.startfile") as mock_start:
                    assert open_folder("C:\\") is True
                    mock_start.assert_called()
            else:
                with patch("subprocess.run") as mock_run:
                    assert open_folder("/tmp") is True
                    mock_run.assert_called()

    def test_safe_str(self):
        assert safe_str(None) == ""
        assert safe_str(None, default="N/A") == "N/A"
        assert safe_str(123) == "123"
        assert safe_str("test") == "test"

    def test_truncate_string(self):
        s = "Hello World"
        assert truncate_string(s, 5, "...") == "He..."
        assert truncate_string(s, 20) == s
        assert truncate_string(None) == ""
        assert truncate_string("", 5) == ""


class TestUtilsParsing:
    def test_parse_currency(self):
        assert parse_currency("1.234,56") == 1234.56  # noqa: PLR2004
        assert parse_currency("1234,56") == 1234.56  # noqa: PLR2004
        assert parse_currency("€ 50,00") == 50.0  # noqa: PLR2004
        assert parse_currency("1,234.56") == 1234.56  # noqa: PLR2004
        assert parse_currency(None) == 0.0
        assert parse_currency("") == 0.0
        assert parse_currency("abc") == 0.0  # Error case
        # Printable chars only - In formato IT 1.000 è mille
        assert parse_currency("€ 1.000\u200b") == 1000.0  # noqa: PLR2004


class TestUtilsValidators:
    def test_validate_oda(self):
        assert InputValidator.validate_oda("12345ABC").valid is True
        assert InputValidator.validate_oda("").valid is False
        assert InputValidator.validate_oda("A" * 21).valid is False

    def test_validate_codice_fiscale(self):
        valid_cf = "RSSMRA80A01H501U"
        assert InputValidator.validate_codice_fiscale(valid_cf).valid is True
        assert InputValidator.validate_codice_fiscale("INVALID").valid is False
        assert InputValidator.validate_codice_fiscale("RSSMRA80A01H501Z").valid is False

    def test_validate_date_it(self):
        assert InputValidator.validate_date_italian("01.01.2023").valid is True
        assert InputValidator.validate_date_italian("32.01.2023").valid is False
        assert InputValidator.validate_date_italian("").valid is False

    def test_sanitize_sql_string(self):
        assert InputValidator.sanitize_sql_string("test\x00data") == "testdata"
        assert InputValidator.sanitize_sql_string(None) == ""
