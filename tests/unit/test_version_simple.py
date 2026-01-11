import pytest
from src.core.version import __version__, __app_name__

def test_version_info():
    # Verifica che la versione sia una stringa valida
    assert isinstance(__version__, str)
    assert "." in __version__
    assert __app_name__ == "SyncroJob"