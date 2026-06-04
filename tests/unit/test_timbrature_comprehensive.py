import sqlite3
from unittest.mock import MagicMock, patch

import pandas as pd

from src.infrastructure.bots.portale_fornitori.timbrature.bot import TimbratureBot


class TestTimbratureBotComprehensive:
    def test_init_and_properties(self):
        bot = TimbratureBot("u", "p")
        assert bot.username == "u"
        assert bot.name == "timbrature"

    @patch("src.infrastructure.bots.portale_fornitori.timbrature.bot.TimbraturePage")
    @patch("src.infrastructure.bots.portale_fornitori.timbrature.bot.TimbratureStorage")
    def test_run_success(self, mock_storage_class, mock_page_class):
        bot = TimbratureBot("u", "p")
        bot.driver = MagicMock()
        mock_page = mock_page_class.return_value
        mock_page.navigate_to_timbrature.return_value = True
        mock_page.download_timbrature.return_value = "file.xlsx"
        mock_storage = mock_storage_class.return_value
        mock_storage.import_excel.return_value = True

        with patch("src.infrastructure.bots.portale_fornitori.timbrature.bot.Path") as mock_path:
            mock_path.return_value.name = "file.xlsx"
            res = bot.run([])
            assert res is True


class TestTimbratureStorageComprehensive:
    def test_import_excel_data_flow(self, tmp_path, mocker):
        from src.infrastructure.bots.portale_fornitori.timbrature.storage import TimbratureStorage

        db = tmp_path / "test_import_final_round20.db"

        # 1. Creazione fisica dello schema COMPLETO
        with sqlite3.connect(db) as conn:
            conn.execute("""
                CREATE TABLE timbrature (
                    id_dipendente TEXT, data TEXT, ingresso TEXT, uscita TEXT,
                    fornitore TEXT, codice_rilpres TEXT, numero_badge TEXT,
                    nome TEXT, cognome TEXT, codice_fiscale TEXT,
                    codice_qualifica TEXT, specializzazione TEXT,
                    societa_ospitante TEXT, data_ins TEXT, presenza_ts TEXT,
                    sito_timbratura TEXT
                )
            """)
            conn.commit()

        storage = TimbratureStorage(db)

        # 2. Mocking pandas per evitare I/O reale
        mock_df = pd.DataFrame([{"Data Timbratura": "2024-01-01", "Cognome Risorsa": "Rossi"}])
        mocker.patch("src.infrastructure.bots.portale_fornitori.timbrature.storage.pd.read_excel", return_value=mock_df)

        # Mocking db_manager per la connessione
        mocker.patch(
            "src.infrastructure.bots.portale_fornitori.timbrature.storage.db_manager.get_connection",
            side_effect=lambda p, **kw: sqlite3.connect(p),
        )

        # Mocking l'importatore di basso livello (non usato se process_excel_row è reale)
        # Ma storage.import_excel chiama ScaricoOreImporter.import_scarico_ore? No, lo fa il BOT.
        # Storage.import_excel legge direttamente via pandas in V9.4

        res = storage.import_excel("any.xlsx")
        assert res is True
