"""
Tests for SafeWorkPDLSearchBot database import logic.
"""

from unittest.mock import MagicMock

import pandas as pd
import pytest

from src.bots.safework.pdl.search_bot import SafeWorkPDLSearchBot


class TestSafeWorkPDLSearchBotImport:
    @pytest.fixture
    def bot(self, tmp_path):
        bot = SafeWorkPDLSearchBot("user", "pass", download_path=str(tmp_path))
        bot.log = MagicMock()
        return bot

    def test_import_to_db_mapping(self, bot, tmp_path, mocker):
        """Verifica che il mapping delle colonne Excel -> DB sia corretto."""
        excel_path = tmp_path / "RicercaPDL.xlsx"

        # Crea DataFrame con nomi colonne SafeWork (italiano)
        df_source = pd.DataFrame(
            {
                "N° PDL": ["566360/C"],
                "AREA": ["ISAB SUD"],
                "UNITÀ": ["U100"],
                "STATO": ["CHIUSO"],
                "ORDINE": ["12345"],
            }
        )
        # Forza tipi stringa per evitare problemi di asserzione
        df_source = df_source.astype(str)
        df_source.to_excel(excel_path, index=False)

        # Mock DB connection
        mock_conn = MagicMock()
        mocker.patch("src.core.database.db_manager.get_connection", return_value=mock_conn)
        mocker.patch("src.core.sync_tracker.SyncTracker.update_status")

        bot._import_to_db(str(excel_path))

        args, _kwargs = mock_conn.__enter__.return_value.executemany.call_args
        query = args[0]
        data = args[1]

        assert "INSERT OR REPLACE INTO pdl" in query
        assert "n_pdl" in query
        assert "unita" in query

        row = data[0]
        assert str(row[0]) == "566360/C"
        assert str(row[2]) == "ISAB SUD"
        assert str(row[3]) == "U100"
        assert str(row[7]) == "CHIUSO"

    def test_import_to_db_missing_columns_resilience(self, bot, tmp_path, mocker):
        """Verifica che l'import non fallisca se mancano alcune colonne nell'Excel."""
        excel_path = tmp_path / "Ricerca_Minima.xlsx"
        # Solo PdL
        df_source = pd.DataFrame({"N° PDL": ["111222"]})
        df_source = df_source.astype(str)
        df_source.to_excel(excel_path, index=False)

        mock_conn = MagicMock()
        mocker.patch("src.core.database.db_manager.get_connection", return_value=mock_conn)
        mocker.patch("src.core.sync_tracker.SyncTracker.update_status")

        bot._import_to_db(str(excel_path))

        assert mock_conn.__enter__.return_value.executemany.called
        data = mock_conn.__enter__.return_value.executemany.call_args[0][1]
        assert str(data[0][0]) == "111222"
        assert data[0][3] == ""

    def test_run_site_loop(self, bot, mocker):
        """Verifica che il bot iteri su tutti i siti se selezionato 'Seleziona tutto'."""
        mocker.patch.object(bot, "_naviga_a_ricerca", return_value=True)
        # Importante: inizializziamo ricerca_pdl_page perché run la usa
        bot.ricerca_pdl_page = MagicMock()
        bot.ricerca_pdl_page.seleziona_sito_e_cerca.return_value = True

        # Patch methods that would require real driver interaction
        mocker.patch.object(bot, "_attendi_scomparsa_overlay")
        mocker.patch.object(bot, "_esegui_export", return_value=None)
        mocker.patch.object(bot, "_check_stop")

        bot.driver = MagicMock()
        bot.wait = MagicMock()

        data = [{"site_selection": "Seleziona tutto"}]
        bot.run(data)

        # Deve aver chiamato seleziona_sito_e_cerca per IGCC, ISAB Nord, ISAB Sud
        assert bot.ricerca_pdl_page.seleziona_sito_e_cerca.call_count == 3
        calls = [c.args[0] for c in bot.ricerca_pdl_page.seleziona_sito_e_cerca.call_args_list]
        assert "IGCC" in calls
        assert "ISAB Nord" in calls
        assert "ISAB Sud" in calls
