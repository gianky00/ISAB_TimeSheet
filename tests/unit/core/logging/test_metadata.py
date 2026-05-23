import os
from unittest.mock import MagicMock, patch

import pytest

from src.core.logging.metadata import MetadataEnricher, enrich_entry, get_enricher


class TestMetadataEnricher:
    @pytest.fixture(autouse=True)
    def reset_enricher(self):
        MetadataEnricher._instance = None
        MetadataEnricher._cache = None
        self.enricher = MetadataEnricher()

    def test_static_metadata_keys(self):
        meta = self.enricher.get_static_metadata()
        assert "app_name" in meta
        assert "app_version" in meta
        assert "environment" in meta
        assert "platform" in meta
        assert "user" in meta

    def test_detect_environment_test(self):
        # In questo ambiente (pytest), deve ritornare "test"
        assert self.enricher._detect_environment() == "test"

    @patch.dict(os.environ, {"SYNCROJOB_ENV": "production"})
    def test_detect_environment_override(self):
        # Forziamo ricalcolo cache resetando l'istanza
        MetadataEnricher._instance = None
        MetadataEnricher._cache = None
        enricher = MetadataEnricher()
        assert enricher._detect_environment() == "production"

    def test_dynamic_metadata(self):
        dyn = self.enricher.get_dynamic_metadata()
        assert "process_id" in dyn
        assert "working_directory" in dyn
        assert dyn["process_id"] == os.getpid()

    def test_enrich_log_entry(self):
        entry = {"message": "Test"}
        enriched = self.enricher.enrich_log_entry(entry)

        assert "metadata" in enriched
        assert enriched["metadata"]["app_name"] == "SyncroJob"
        assert "process_id" in enriched["metadata"]

    def test_enrich_log_entry_no_overwrite(self):
        # Non deve sovrascrivere valori già presenti
        entry = {"metadata": {"app_name": "CustomApp", "process_id": 999}}
        enriched = self.enricher.enrich_log_entry(entry)

        assert enriched["metadata"]["app_name"] == "CustomApp"
        assert enriched["metadata"]["process_id"] == 999

    def test_singleton(self):
        e1 = get_enricher()
        e2 = MetadataEnricher()
        assert e1 is e2

    def test_enrich_entry_helper(self):
        with patch("src.core.logging.metadata.get_enricher") as mock_get:
            mock_inst = MagicMock()
            mock_get.return_value = mock_inst

            enrich_entry({"m": 1})
            assert mock_inst.enrich_log_entry.called
