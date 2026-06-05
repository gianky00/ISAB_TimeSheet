from unittest.mock import MagicMock, patch

import pytest

from src.application.services.database.repositories.oda_repository import OdaRepository
from src.application.services.oda.oda_controller import ODAController
from src.domain import OdaRecord


class TestOdaArchitecture:
    @pytest.fixture
    def mock_db_manager(self):
        mock = MagicMock()
        mock.DB_STORICO_ODA.exists.return_value = True
        return mock

    def test_repository_get_all(self, mock_db_manager):
        repo = OdaRepository(db_manager_instance=mock_db_manager)

        # Mocking sqlite3 connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db_manager.get_connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock row that matches OdaRecord fields
        mock_row = {
            "org_acq": "ORG1",
            "data_oda": "2024-05-13",
            "oda": "12345",
            "pos_oda": "10",
            "stato": "APERTO",
            "cat_contab": "CAT1",
            "descrizione": "DESC",
            "qta": 1.0,
            "uom": "PZ",
            "data_consegna": "2024-06-13",
            "valore_netto_pos": 100.0,
            "valore_residuo": 50.0,
            "valore_netto_oda": 1000.0,
            "divisione": "DIV1",
            "destinatario": "DEST1",
            "nome_destinatario": "NAME1",
            "codice_fornitore": "FORN1",
            "descrizione_fornitore": "FORN_DESC",
            "emittente_fattura": "EMI1",
            "desc_emittente_fattura": "EMI_DESC",
            "contract_card": "CC1",
            "contratto": "CON1",
            "posizione_contratto": "1",
            "gruppo_acquisti": "GRP1",
            "indicatore_rilascio": "X",
            "stato_rilascio": "OK",
            "attivita": "ACT1",
            "num_riga": "1",
            "quantita": 1.0,
            "unita_mis": "PZ",
            "prezzo_lordo": 100.0,
            "testo_breve": "SHORT",
            "id": 1,
        }

        mock_cursor.fetchall.return_value = [mock_row]

        records = repo.get_all(as_objects=True)
        assert len(records) == 1
        assert isinstance(records[0], OdaRecord)
        assert records[0].oda == "12345"

    def test_controller_grouping(self, mock_db_manager):
        with patch(
            "src.application.services.database.repositories.oda_repository.OdaRepository.get_all"
        ) as mock_get_all:
            record = OdaRecord(
                org_acq="ORG1",
                data_oda="2024-05-13",
                oda="12345",
                pos_oda="10",
                stato="APERTO",
                cat_contab="CAT1",
                descrizione="DESC",
                qta=1.0,
                uom="PZ",
                data_consegna="2024-06-13",
                valore_netto_pos=100.0,
                valore_residuo=50.0,
                valore_netto_oda=1000.0,
                divisione="DIV1",
                destinatario="DEST1",
                nome_destinatario="NAME1",
                codice_fornitore="FORN1",
                descrizione_fornitore="FORN_DESC",
                emittente_fattura="EMI1",
                desc_emittente_fattura="EMI_DESC",
                contract_card="CC1",
                contratto="CON1",
                posizione_contratto="1",
                gruppo_acquisti="GRP1",
                indicatore_rilascio="X",
                stato_rilascio="OK",
                attivita="ACT1",
                num_riga="1",
                quantita=1.0,
                unita_mis="PZ",
                prezzo_lordo=100.0,
                testo_breve="SHORT",
                id=1,
            )
            mock_get_all.return_value = [record]

            controller = ODAController()
            grouped = controller.get_grouped_data()

            assert len(grouped) == 1
            assert grouped[0]["oda"] == "12345"
            assert grouped[0]["valore_totale"] == 1000.0
