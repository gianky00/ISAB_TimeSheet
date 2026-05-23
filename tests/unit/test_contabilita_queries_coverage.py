from pathlib import Path

import pytest

from src.core.contabilita_queries import ContabilitaQueries


class TestContabilitaQueriesCoverage:
    @pytest.fixture(autouse=True)
    def mock_repo(self, mocker):
        # Patch the class-level repository in ContabilitaQueries
        return mocker.patch("src.core.contabilita_queries.ContabilitaQueries._repo")

    def test_get_available_years_logic(self, mock_repo):
        mock_repo.get_available_years.return_value = [2024, 2025]
        years = ContabilitaQueries.get_available_years(Path("fake.db"))
        assert 2024 in years

    def test_get_available_years_empty_db(self, mock_repo):
        mock_repo.get_available_years.return_value = []
        years = ContabilitaQueries.get_available_years(Path("empty.db"))
        assert years == []

    def test_get_data_by_year_columns_alignment(self, mock_repo):
        mock_repo.get_data_by_year.return_value = [("C1", "R1", 2024, 100.0)]
        data = ContabilitaQueries.get_data_by_year(Path("fake.db"), 2024)
        assert len(data) == 1
        assert data[0][0] == "C1"
