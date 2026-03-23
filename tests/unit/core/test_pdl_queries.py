import sqlite3
from unittest.mock import MagicMock, patch

import pytest

from src.core.database.pdl_queries import PDLQueries


class TestPDLQueries:
    @pytest.fixture
    def mock_db(self):
        with patch("src.core.database.pdl_queries.db_manager") as mock:
            mock.DB_PDL = "mock_pdl.db"
            # Mock context manager for get_connection
            mock_conn = MagicMock()
            mock.get_connection.return_value.__enter__.return_value = mock_conn
            mock.conn = mock_conn  # Shortcut
            yield mock

    def test_get_unique_requesters_normalization(self, mock_db):
        """Verifica la normalizzazione dei nomi dei richiedenti."""
        mock_db.execute_query.return_value = [
            ("  MARIO   ROSSI  ",),
            ("luigi verdi",),
            ("ISAB s.r.l.",),
            (None,),
            ("",),
        ]

        results = PDLQueries.get_unique_requesters()

        # "  MARIO   ROSSI  " -> "Mario Rossi"
        # "luigi verdi" -> "Luigi Verdi"
        # "ISAB s.r.l." -> "Isab S.R.L." (title case behavior)
        assert "Mario Rossi" in results
        assert "Luigi Verdi" in results
        assert "Isab S.R.L." in results
        assert len(results) == 3
        assert results == sorted(results)

    def test_save_programming_results_empty(self, mock_db):
        """Verifica la cancellazione se i risultati sono vuoti."""
        success = PDLQueries.save_programming_results([], "01/01/2024", "07/01/2024")
        assert success is True
        # Deve chiamare DELETE
        args = mock_db.execute_query.call_args
        assert "DELETE FROM pdl_programmazione" in args[0][1]
        assert args[0][2] == ("01/01/2024", "07/01/2024")

    def test_save_programming_results_success(self, mock_db):
        """Verifica l'inserimento corretto dei dati di programmazione."""
        results = [
            {
                "richiedente": "R1",
                "pdl": "P1",
                "area": "A1",
                "unita": "U1",
                "descrizione": "D1",
                "programmazione": [{"tcl": True, "tgo": False}] * 7,
            }
        ]

        success = PDLQueries.save_programming_results(results, "01/01", "07/01")
        assert success is True

        # Verifica DELETE iniziale
        assert mock_db.execute_query.called
        # Verifica executemany
        assert mock_db.conn.executemany.called
        insert_args = mock_db.conn.executemany.call_args
        batch = insert_args[0][1]
        assert len(batch) == 1
        # 19 colonne base + 2 date = 21 (il codice estende TCL/TGO per 7 giorni = 14 + 5 base = 19)
        assert len(batch[0]) == 21

    def test_get_programming_results_by_week(self, mock_db):
        """Verifica il recupero dei dati settimanali mappati in dizionari."""
        mock_cursor = mock_db.conn.cursor.return_value
        # Simula Row object (comportamento dict-like)
        mock_row = {
            "richiedente": "R1",
            "n_pdl": "P1",
            "area": "A1",
            "unita": "U1",
            "descrizione": "D1",
            "ultimo_aggiornamento": "2024",
            "lun_tcl": 1,
            "lun_tgo": 0,
            "mar_tcl": 1,
            "mar_tgo": 1,
            "mer_tcl": 0,
            "mer_tgo": 0,
            "gio_tcl": 0,
            "gio_tgo": 0,
            "ven_tcl": 0,
            "ven_tgo": 0,
            "sab_tcl": 0,
            "sab_tgo": 0,
            "dom_tcl": 0,
            "dom_tgo": 0,
        }
        mock_cursor.fetchall.return_value = [mock_row]

        results = PDLQueries.get_programming_results_by_week("start", "end")

        assert len(results) == 1
        assert results[0]["richiedente"] == "R1"
        assert results[0]["programmazione"][0]["tcl"] is True
        assert results[0]["programmazione"][1]["tgo"] is True  # Mar TGO = 1

    def test_get_pdl_interventions_db_missing(self, tmp_path):
        """Verifica che torni lista vuota se il DB esterno non esiste."""
        with patch("src.core.config_manager.load_config") as mock_cfg:
            mock_cfg.return_value = {"activity_db_path": str(tmp_path / "non_existent.db")}
            res = PDLQueries.get_pdl_interventions("P123")
            assert res == []

    def test_get_pdl_interventions_success(self, tmp_path):
        """Verifica la query UNION su DB esterno."""
        db_file = tmp_path / "ext.db"
        with sqlite3.connect(db_file) as conn:
            conn.execute(
                "CREATE TABLE report_interventi (pdl TEXT, data_riferimento_attivita TEXT, nome_tecnico TEXT, testo_report TEXT)"
            )
            conn.execute(
                "CREATE TABLE report_da_validare (pdl TEXT, data_riferimento_attivita TEXT, nome_tecnico TEXT, testo_report TEXT)"
            )
            conn.execute(
                "CREATE TABLE relazioni (pdl TEXT, data_intervento TEXT, nome_compilatore TEXT, cognome_compilatore TEXT, corpo_relazione TEXT)"
            )

            conn.execute("INSERT INTO report_interventi VALUES ('P1', '2024-01-01', 'T1', 'DESC')")

        with patch("src.core.config_manager.load_config") as mock_cfg:
            mock_cfg.return_value = {"activity_db_path": str(db_file)}
            res = PDLQueries.get_pdl_interventions("P1")

            assert len(res) == 1
            assert res[0]["fonte"] == "Report (Validato)"
            assert res[0]["tecnico"] == "T1"
