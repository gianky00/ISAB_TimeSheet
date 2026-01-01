import pytest
import datetime
from src.utils.helpers import sanitize_filename, format_timestamp, truncate_string, get_years_list
from src.utils.parsing import parse_currency
from src.utils.validators import InputValidator

class TestUtilsHelpers:
    
    def test_sanitize_filename(self):
        assert sanitize_filename("normal_file.txt") == "normal_file.txt"
        assert sanitize_filename("File Con Spazi.pdf") == "File Con Spazi.pdf"
        # The sanitizer replaces backslashes with underscores and collapses dots
        # Input: "..\\../traversal.txt" -> ".._../traversal.txt" -> cleaning -> "_._traversal.txt" or similar
        # Let's check it doesn't contain traversal characters
        sanitized = sanitize_filename("..\\../traversal.txt")
        assert ".." not in sanitized
        assert "\\" not in sanitized
        assert "/" not in sanitized
        
        assert sanitize_filename("invalid|chars<>?*.txt") == "invalid_chars_.txt"
        assert sanitize_filename(None) == "unnamed_file"
        assert sanitize_filename("") == "unnamed_file"
        # Test cleaning multiple dots
        assert sanitize_filename("file...txt") == "file.txt"

    def test_format_timestamp(self):
        dt = datetime.datetime(2023, 1, 1, 12, 30, 0)
        assert format_timestamp(dt) == "01/01/2023 12:30:00"
        # Test current time (format structure check)
        now_str = format_timestamp()
        assert len(now_str) == 19
        assert "/" in now_str
        
    def test_truncate_string(self):
        s = "Questo è un testo molto lungo che deve essere troncato"
        assert truncate_string(s, 10, "...") == "Questo ..."
        assert truncate_string(s, 100) == s
        assert truncate_string(None) == ""
        
    def test_get_years_list(self):
        current_year = datetime.datetime.now().year
        years = get_years_list(-1, 1)
        assert len(years) == 3
        assert str(current_year) in years
        assert str(current_year - 1) in years
        assert str(current_year + 1) in years

class TestUtilsParsing:
    
    def test_parse_currency(self):
        # IT format
        assert parse_currency("1.234,56") == 1234.56
        assert parse_currency("1234,56") == 1234.56
        assert parse_currency("50,00") == 50.0
        
        # US/Std format
        assert parse_currency("1,234.56") == 1234.56
        assert parse_currency("1234.56") == 1234.56
        
        # Currency symbol
        assert parse_currency("€ 1.000,00") == 1000.0
        
        # Edge cases
        assert parse_currency(None) == 0.0
        assert parse_currency("") == 0.0
        assert parse_currency(100) == 100.0
        
        # Ambiguous but robust check
        # "1.000" -> 1000.0 or 1.0? 
        # The parser logic says: len(parts[1]) == 3 (000), so it's ambiguous.
        # But `float("1.000")` is 1.0. Let's see behavior.
        # Our implementation usually treats it as float if simple casting works.
        assert parse_currency("1.000") == 1.0 

class TestUtilsValidators:
    
    def test_validate_oda(self):
        assert InputValidator.validate_oda("12345ABC").valid is True
        assert InputValidator.validate_oda("").valid is False
        assert InputValidator.validate_oda("A"*21).valid is False
        assert InputValidator.validate_oda("Invalid-Char!").valid is False
        
    def test_validate_cf_checksum(self):
        # Real CF example (RSSMRA80A01H501U - Mario Rossi generated)
        valid_cf = "RSSMRA80A01H501U" 
        assert InputValidator.validate_codice_fiscale(valid_cf).valid is True
        
        # Invalid Length
        assert InputValidator.validate_codice_fiscale("RSSMRA80A01H501").valid is False
        
        # Invalid Checksum (Last char U -> Z)
        invalid_cf = "RSSMRA80A01H501Z"
        assert InputValidator.validate_codice_fiscale(invalid_cf).valid is False
        
    def test_validate_date_it(self):
        assert InputValidator.validate_date_italian("01.01.2023").valid is True
        assert InputValidator.validate_date_italian("31/12/2023").valid is True # Auto-fix /
        assert InputValidator.validate_date_italian("32.01.2023").valid is False # Not valid date
        assert InputValidator.validate_date_italian("2023.01.01").valid is False # Wrong format
