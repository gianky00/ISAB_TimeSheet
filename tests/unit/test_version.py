import re

from src.core import version


def test_version_format():
    """Verifica formato versione Semantic Versioning like."""
    assert isinstance(version.__version__, str)
    # Formato X.Y.Z
    assert re.match(r"^\d+\.\d+\.\d+$", version.__version__)


def test_app_constants():
    """Verifica costanti applicazione."""
    assert version.__app_name__ == "SyncroJob"
    assert version.APP_NAME == "SyncroJob"
    assert version.UPDATE_URL.startswith("https://")
    assert "version.json" in version.UPDATE_URL
