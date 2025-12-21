import unittest
import sys
import os

# Ensure src can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    from src.utils.helpers import sanitize_filename
except ImportError:
    # Allow test file to exist before implementation for TDD, 
    # but it will fail if run.
    pass

class TestFilenameSanitization(unittest.TestCase):
    def test_path_traversal_attempts(self):
        """Verify that directory traversal sequences are neutralized."""
        unsafe_input = "../../evil.xlsx"
        safe_output = sanitize_filename(unsafe_input)
        
        print(f"Sanitized '{unsafe_input}' -> '{safe_output}'")
        
        self.assertNotIn("..", safe_output)
        self.assertNotIn("/", safe_output)
        self.assertNotIn("\\", safe_output)
        
        # Ensure it resolves to a safe filename
        self.assertNotEqual(safe_output, "")

    def test_valid_inputs_preserved(self):
        """Verify that standard inputs remain unchanged."""
        inputs = ["8500123", "10", "ODA_2024-01-01"]
        for inp in inputs:
            self.assertEqual(sanitize_filename(inp), inp)

    def test_special_chars_handled(self):
        """Verify that forbidden characters are replaced."""
        unsafe = "Oda:123/456*?"
        safe = sanitize_filename(unsafe)
        
        for char in [':', '/', '*', '?']:
            self.assertNotIn(char, safe)
            
    def test_null_bytes(self):
        """Verify null bytes are removed (C-string termination attacks)."""
        unsafe = "file.txt\0.exe"
        safe = sanitize_filename(unsafe)
        self.assertNotIn("\0", safe)

if __name__ == '__main__':
    unittest.main()
