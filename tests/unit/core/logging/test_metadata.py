import os
from unittest.mock import patch

import pytest

from src.core.logging.metadata import MetadataEnricher, enrich_entry, get_enricher


class TestMetadataEnricher:
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        # Ripristino lo stato globale
        MetadataEnricher._instance = None
        MetadataEnricher._cache = None
        # Remove unused global declaration
        import src.core.logging.metadata as md

        md._enricher = None

    def test_singleton(self):
        e1 = MetadataEnricher()
        e2 = MetadataEnricher()
        assert e1 is e2

    def test_get_enricher_helper(self):
        e1 = get_enricher()
        e2 = get_enricher()
        assert e1 is e2
        assert isinstance(e1, MetadataEnricher)

    def test_build_static_metadata(self):
        enricher = MetadataEnricher()
        static = enricher.get_static_metadata()

        assert "app_name" in static
        assert static["app_name"] == "SyncroJob"
        assert "app_version" in static
        assert "environment" in static
        assert "hostname" in static
        assert "platform" in static
        assert "user" in static

    @patch("src.core.logging.metadata.socket.gethostname", side_effect=Exception("Net Error"))
    @patch("src.core.logging.metadata.os.getlogin", side_effect=Exception("User Error"))
    def test_build_static_metadata_errors(self, mock_getlogin, mock_hostname):
        with patch.dict(os.environ, {"USERNAME": "test_user"}):
            enricher = MetadataEnricher()
            static = enricher.get_static_metadata()

            assert static["hostname"] == "unknown"
            assert static["user"] == "test_user"

    def test_detect_environment_env_vars(self):
        enricher = MetadataEnricher()

        with patch.dict(os.environ, {"SYNCROJOB_ENV": "dev"}):
            assert enricher._detect_environment() == "development"

        with patch.dict(os.environ, {"SYNCROJOB_ENV": "prod"}):
            assert enricher._detect_environment() == "production"

        with patch.dict(os.environ, {"SYNCROJOB_ENV": "test"}):
            assert enricher._detect_environment() == "test"

    @patch("src.core.logging.metadata.sys")
    def test_detect_environment_frozen(self, mock_sys):
        # Simula assenza env vars
        with patch.dict(os.environ, clear=True):
            mock_sys.modules = {}  # No pytest
            mock_sys.executable = "python.exe"
            mock_sys.frozen = True  # Simula PyInstaller

            enricher = MetadataEnricher()
            assert enricher._detect_environment() == "production"

    def test_get_dynamic_metadata(self):
        enricher = MetadataEnricher()
        dynamic = enricher.get_dynamic_metadata()

        assert "process_id" in dynamic
        assert "parent_process_id" in dynamic
        assert "working_directory" in dynamic

    @patch("src.core.logging.metadata.Path.cwd", side_effect=Exception("CWD Error"))
    def test_get_dynamic_metadata_error(self, mock_cwd):
        enricher = MetadataEnricher()
        dynamic = enricher.get_dynamic_metadata()
        assert dynamic["working_directory"] == "unknown"

    def test_get_full_metadata(self):
        enricher = MetadataEnricher()
        full = enricher.get_full_metadata()

        assert "app_name" in full
        assert "process_id" in full

    def test_enrich_log_entry(self):
        enricher = MetadataEnricher()
        entry = {"message": "Test"}

        enriched = enricher.enrich_log_entry(entry)

        assert "metadata" in enriched
        assert "app_name" in enriched["metadata"]
        assert "process_id" in enriched["metadata"]

    def test_enrich_entry_helper(self):
        entry = {"message": "Hello"}
        res = enrich_entry(entry)
        assert "metadata" in res
        assert "app_name" in res["metadata"]
