from pathlib import Path
from unittest.mock import patch

import pytest

from src.application.services.contabilita_queries import ContabilitaQueries


class TestContabilitaQueries:
    @pytest.fixture(autouse=True)
    def mock_repo(self):
        with patch.object(ContabilitaQueries, "_repo") as mock:
            self.repo = mock
            yield mock

    def test_get_available_years(self):
        self.repo.get_available_years.return_value = [2023]
        assert ContabilitaQueries.get_available_years(Path("db.sqlite")) == [2023]

    def test_get_data_by_year(self):
        self.repo.get_data_by_year.return_value = [("row",)]
        res = ContabilitaQueries.get_data_by_year(Path("db.sqlite"), 2023)
        assert res == [("row",)]
        self.repo.get_data_by_year.assert_called_with(2023, as_objects=False)

    def test_get_giornaliere_by_year(self):
        self.repo.get_giornaliere_by_year.return_value = []
        ContabilitaQueries.get_giornaliere_by_year(Path("db.sqlite"), 2023)
        assert self.repo.get_giornaliere_by_year.called

    def test_get_attivita_programmate_data(self):
        ContabilitaQueries.get_attivita_programmate_data(Path("db.sqlite"))
        assert self.repo.get_attivita_programmate.called

    def test_get_certificati_campione_data(self):
        ContabilitaQueries.get_certificati_campione_data(Path("db.sqlite"))
        assert self.repo.get_certificati_campione.called

    def test_get_scarico_ore_data(self):
        ContabilitaQueries.get_scarico_ore_data(Path("db.sqlite"))
        assert self.repo.get_scarico_ore.called
