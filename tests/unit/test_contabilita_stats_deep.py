from pathlib import Path

from src.application.services.contabilita.stats_service import ContabilitaStats


class TestContabilitaStatsDeep:
    def test_get_year_stats_calculations(self, mocker):
        """Verifica i calcoli di base: somme, conteggi e stati."""
        # Mock dei dati restituiti dalle query
        # Mapping Contabilita (data_by_year):
        # 0:data_prev, 1:mese, 2:n_prev, 3:totale_prev, 4:attivita, 5:tcl, 6:odc, 7:stato,
        # 8:tipologia, 9:ore_sp, 10:resa, 11:note, 12:path, 13:file
        mock_data = [
            (
                "01/01",
                "Gen",
                "P1",
                "1.000,00",
                "Attivita A",
                "T1",
                "O1",
                "COMPLETATO",
                "T",
                "8,0",
                "1",
                "N",
                "P",
                "F",
            ),
            (
                "02/01",
                "Gen",
                "P2",
                "500,50",
                "Attivita B",
                "T1",
                "O2",
                "IN CORSO",
                "T",
                "4,5",
                "1",
                "N",
                "P",
                "F",
            ),
            (
                "03/01",
                "Gen",
                "TOTALE",
                "1.500,50",
                "IGNORE",
                "T1",
                "O3",
                "DONE",
                "T",
                "12,5",
                "1",
                "N",
                "P",
                "F",
            ),  # Deve essere ignorata
        ]

        mocker.patch(
            "src.application.services.contabilita_queries.ContabilitaQueries.get_data_by_year",
            return_value=mock_data,
        )
        mocker.patch(
            "src.application.services.contabilita_queries.ContabilitaQueries.get_giornaliere_by_year",
            return_value=[],
        )

        stats = ContabilitaStats.get_year_stats(Path("fake.db"), 2024)

        assert stats["total_prev"] == 1500.50
        assert stats["total_ore"] == 12.5
        assert stats["count_total"] == 2
        assert stats["status_counts"]["COMPLETATO"] == 1
        assert stats["status_counts"]["IN CORSO"] == 1

    def test_get_year_stats_top_commesse(self, mocker):
        """Verifica l'ordinamento e il limite delle top commesse."""
        mock_data = [
            (
                "D",
                "M",
                f"P{i}",
                f"{i * 100}",
                f"Att {i}",
                "T",
                "O",
                "S",
                "T",
                "0",
                "R",
                "N",
                "P",
                "F",
            )
            for i in range(1, 10)  # 9 commesse da 100 a 900
        ]
        mocker.patch(
            "src.application.services.contabilita_queries.ContabilitaQueries.get_data_by_year",
            return_value=mock_data,
        )
        mocker.patch(
            "src.application.services.contabilita_queries.ContabilitaQueries.get_giornaliere_by_year",
            return_value=[],
        )

        stats = ContabilitaStats.get_year_stats(Path("fake.db"), 2024)

        top = stats["top_commesse"]
        assert len(top) == 5
        assert top[0][0] == "Att 9"  # Il valore più alto (900)
        assert top[0][1] == 900.0

    def test_get_year_stats_dirette_indirette(self, mocker):
        """Verifica la distinzione tra ore dirette e indirette nelle giornaliere."""
        # Mapping Giornaliere (giornaliere_by_year):
        # 0:data, 1:personale, 2:tcl, 3:descrizione, 4:n_prev, 5:odc, 6:pdl, 7:inizio, 8:fine, 9:ore, 10:nome_file
        mock_giornaliere = [
            (
                "D1",
                "U1",
                "T1",
                "Desc",
                "P123",
                "",
                "PDL",
                "08",
                "17",
                "9,0",
                "F1",
            ),  # DIRETTA (ha n_prev)
            (
                "D2",
                "U1",
                "T1",
                "Desc",
                "",
                "ODC456",
                "PDL",
                "08",
                "17",
                "4,5",
                "F1",
            ),  # DIRETTA (ha odc)
            (
                "D3",
                "U1",
                "T1",
                "Indiretta",
                "",
                "",
                "",
                "08",
                "17",
                "2,0",
                "F1",
            ),  # INDIRETTA (vuote)
            (
                "D4",
                "U1",
                "T1",
                "Desc",
                "NaN",
                "nan",
                "",
                "08",
                "17",
                "1,0",
                "F1",
            ),  # INDIRETTA (NaN stringhe)
        ]

        mocker.patch(
            "src.application.services.contabilita_queries.ContabilitaQueries.get_data_by_year",
            return_value=[],
        )
        mocker.patch(
            "src.application.services.contabilita_queries.ContabilitaQueries.get_giornaliere_by_year",
            return_value=mock_giornaliere,
        )

        stats = ContabilitaStats.get_year_stats(Path("fake.db"), 2024)

        assert stats["ore_dirette"] == 13.5  # 9 + 4.5
        assert stats["ore_indirette"] == 3.0  # 2 + 1
