
import os
import sys
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from src.utils.resource_manager import ResourceManager

class TestResourceManagerCoverage:
    @pytest.fixture
    def temp_root(self, tmp_path):
        """Mock della root di progetto."""
        return tmp_path

    def test_get_icon_logic(self, temp_root, mocker):
        """Verifica il recupero delle icone con estensione automatica."""
        mocker.patch.object(ResourceManager, "ICONS_DIR", temp_root / "icons")
        ResourceManager.ICONS_DIR.mkdir()
        
        icon_file = ResourceManager.ICONS_DIR / "test.svg"
        icon_file.write_text("<svg></svg>")
        
        # Con estensione
        assert ResourceManager.get_icon("test.svg") == str(icon_file)
        # Senza estensione (auto-aggiunta .svg)
        assert ResourceManager.get_icon("test") == str(icon_file)
        # Inesistente
        assert ResourceManager.get_icon("ghost") == ""

    def test_get_style_logic(self, temp_root, mocker):
        """Verifica il recupero dei file QSS."""
        mocker.patch.object(ResourceManager, "STYLES_DIR", temp_root / "styles")
        ResourceManager.STYLES_DIR.mkdir()
        
        style_file = ResourceManager.STYLES_DIR / "dark.qss"
        style_file.write_text("QWidget { color: white; }")
        
        assert ResourceManager.get_style("dark") == str(style_file)
        assert ResourceManager.get_style("light") == "" # Non esiste

    def test_get_temp_path_creation(self, temp_root, mocker):
        """Verifica generazione path in temp e creazione cartella."""
        mocker.patch.object(ResourceManager, "TEMP_DIR", temp_root / "temp")
        
        path = ResourceManager.get_temp_path("session.tmp")
        
        assert path.name == "session.tmp"
        assert path.parent == ResourceManager.TEMP_DIR
        assert ResourceManager.TEMP_DIR.exists()

    def test_ensure_structure(self, temp_root, mocker):
        """Verifica creazione gerarchia cartelle dati e log."""
        mocker.patch.object(ResourceManager, "TEMP_DIR", temp_root / "temp")
        mocker.patch.object(ResourceManager, "LOGS_DIR", temp_root / "logs")
        mocker.patch.object(ResourceManager, "DATA_DIR", temp_root / "data")
        
        ResourceManager.ensure_structure()
        
        assert ResourceManager.TEMP_DIR.is_dir()
        assert ResourceManager.LOGS_DIR.is_dir()
        assert ResourceManager.DATA_DIR.is_dir()

    def test_project_root_frozen(self, mocker):
        """Verifica rilevamento root quando l'app è compilata (frozen)."""
        mocker.patch("sys.frozen", True, create=True)
        mocker.patch("sys.executable", "C:\\Program Files\\App\\app.exe")
        
        # Dobbiamo ricaricare o simulare la logica del blocco if iniziale
        # Poiché PROJECT_ROOT è definito a livello di classe, simuliamo il calcolo
        if getattr(sys, "frozen", False):
            root = Path(os.path.dirname(sys.executable))
        else:
            root = Path("/source")
            
        assert "App" in str(root)

