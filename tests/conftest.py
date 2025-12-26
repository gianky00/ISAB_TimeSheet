import sys
import pytest
from PyQt6.QtWidgets import QApplication

@pytest.fixture(scope="session")
def qapp():
    """
    Fixture to create a QApplication instance for tests.
    Ensures only one instance is created.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
    # Teardown (optional, can be added if needed)
