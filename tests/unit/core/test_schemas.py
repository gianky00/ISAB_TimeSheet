import pandas as pd
import pandera as pa
import pytest

from src.application.services.schemas import validate_contabilita, validate_dipendenti, validate_giornaliere


class TestSchemas:
    def test_validate_dipendenti_success(self):
        df = pd.DataFrame(
            {
                "id_risorsa": [1, "2"],  # "2" should be coerced to int
                "Cognome": ["Rossi", "Verdi"],
                "Nome": ["Mario", "Luigi"],
                "Data_nascita": ["1980-01-01", "1990-05-23"],
                "Badge": [123, 456],
                "Data_assunzione": ["2010-01-01", "2020-01-01"],
            }
        )

        valid_df = validate_dipendenti(df)
        assert valid_df["id_risorsa"].dtype == "int64"
        assert len(valid_df) == 2

    def test_validate_dipendenti_failure(self):
        # Manca colonna obbligatoria
        df = pd.DataFrame({"id_risorsa": [1]})
        with pytest.raises(pa.errors.SchemaErrors):
            validate_dipendenti(df)

    def test_validate_giornaliere_success(self):
        df = pd.DataFrame(
            {
                "data": ["2023-01-01"],
                "personale": ["P1"],
                "descrizione": ["Lavoro"],
                "tcl": ["S"],
                "odc": ["23/123"],
                "pdl": ["12345/S"],
                "inizio": ["08:00"],
                "fine": ["17:00"],
                "ore": ["8.5"],  # String float -> float
                "n_prev": ["PREV1"],
            }
        )

        valid_df = validate_giornaliere(df)
        assert valid_df["ore"].iloc[0] == 8.5
        assert isinstance(valid_df["data"].iloc[0], pd.Timestamp)

    def test_validate_contabilita_success(self):
        df = pd.DataFrame(
            {
                "data_prev": ["2023-05-23"],
                "mese": ["Maggio"],
                "n_prev": ["123"],
                "totale_prev": [1000.0],
                "attivita": ["A1"],
                "tcl": ["T1"],
                "odc": ["O1"],
                "stato_attivita": ["S1"],
                "tipologia": ["T1"],
                "ore_sp": [10.0],
                "resa": ["100%"],
                "annotazioni": ["Nota"],
                "indirizzo_consuntivo": ["/path"],
                "nome_file": ["file.xlsx"],
            }
        )

        valid_df = validate_contabilita(df)
        assert len(valid_df) == 1
        assert valid_df["totale_prev"].iloc[0] == 1000.0

    def test_headers_only_validation(self):
        # Valida solo i nomi delle colonne, ignorando i dati
        df = pd.DataFrame(
            columns=["id_risorsa", "Cognome", "Nome", "Data_nascita", "Badge", "Data_assunzione"]
        )
        valid_df = validate_dipendenti(df, headers_only=True)
        assert len(valid_df) == 0
        assert list(valid_df.columns) == list(df.columns)
