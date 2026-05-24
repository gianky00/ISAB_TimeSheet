import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from src.gui.cleanup_final import main, process_file, remove_orphan_imports


def test_remove_orphan_imports_used():
    content = """from PySide6.QtWidgets import QPushButton, QLabel

btn = QPushButton()
"""
    assert "QPushButton" in remove_orphan_imports(content)


def test_remove_orphan_imports_unused():
    content = """from PySide6.QtWidgets import QPushButton, QLabel

lbl = QLabel()
"""
    result = remove_orphan_imports(content)
    assert "QPushButton" not in result
    assert "QLabel" in result


def test_process_file_no_changes():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".py") as f:
        content = "x = 1\n"
        f.write(content)
        f_path = f.name

    try:
        process_file(f_path)
        assert Path(f_path).read_text() == content
    finally:
        os.unlink(f_path)


def test_process_file_with_changes():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".py") as f:
        content = """from PySide6.QtWidgets import QPushButton, QLabel
import core_widgets
lbl = QLabel()
"""
        f.write(content)
        f_path = f.name

    try:
        process_file(f_path)
        new_content = Path(f_path).read_text()
        assert "QPushButton" not in new_content
    finally:
        os.unlink(f_path)


def test_process_file_syntax_error():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".py") as f:
        # Invalid python code after removal might cause syntax error,
        # but the test is easier if we just mock ast.parse to raise SyntaxError
        content = """from PySide6.QtWidgets import QPushButton, QLabel
import core_widgets
lbl = QLabel()
"""
        f.write(content)
        f_path = f.name

    try:
        with patch("ast.parse", side_effect=SyntaxError("mock error")):
            process_file(f_path)
            # Should rollback, content unchanged
            assert Path(f_path).read_text() == content
    finally:
        os.unlink(f_path)


def test_main(mocker):
    mocker.patch("os.walk", return_value=[("/mock/dir", [], ["test1.py", "core_widgets.py"])])
    mock_process = mocker.patch("src.gui.cleanup_final.process_file")

    main()

    # core_widgets.py is in SKIP_FILES
    mock_process.assert_called_once_with(os.path.join("/mock/dir", "test1.py"))
