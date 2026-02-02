from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from src.core import auth_monitor
from src.core.auth_monitor import _build_access_maps, _normalize


class TestAuthMonitorRobust:
    def test_normalize(self):
        """Test normalizzazione stringhe."""
        assert _normalize("  Rossi  ") == "ROSSI"
        assert _normalize("De  Luca") == "DE LUCA"
        assert _normalize(None) == "NONE"

    def test_build_access_maps_formats(self):
        """Test parsing formati data diversi."""
        # Setup dati: (Cognome, Nome, CF, Data)
        raw = [
            ("ROSSI", "MARIO", "CF1", "2024-01-01"),
            ("BIANCHI", "LUIGI", "CF2", "01/01/2024 08:30:00"), # con orario
            ("VERDI", "ANNA", "CF3", "invalid-date"), # Data rotta
        ]
        
        # Mock datetime.now -> 2024-01-10 (9 giorni dopo)
        mock_now = datetime(2024, 1, 10)
        
        with patch("src.core.auth_monitor.datetime") as mock_dt:
            mock_dt.now.return_value = mock_now
            mock_dt.strptime.side_effect = datetime.strptime # Usa reale per parsing
            
            last_by_cf, last_by_name = _build_access_maps(raw)
            
            assert "CF1" in last_by_cf
            assert last_by_cf["CF1"][0] == 9 # delta days
            
            assert "CF2" in last_by_cf
            assert last_by_cf["CF2"][0] == 9
            
            assert "CF3" not in last_by_cf

    def test_build_access_maps_priority(self):
        """Test priorità: data più recente vince."""
        raw = [
            ("ROSSI", "MARIO", "CF1", "2024-01-01"), # 9 giorni fa
            ("ROSSI", "MARIO", "CF1", "2024-01-05"), # 5 giorni fa (Vince)
        ]
        
        mock_now = datetime(2024, 1, 10)
        with patch("src.core.auth_monitor.datetime") as mock_dt:
            mock_dt.now.return_value = mock_now
            mock_dt.strptime.side_effect = datetime.strptime
            
            last_by_cf, _ = _build_access_maps(raw)
            
            assert last_by_cf["CF1"][0] == 5 # 5 giorni (il più recente)

    @patch("src.core.database.db_manager.execute_query")
    def test_check_expiring_authorizations_logic(self, mock_query):
        """Test logica business (soglie e fallback)."""
        # 1. Dipendenti
        # A: OK (10 giorni)
        # B: IN SCADENZA (25 giorni)
        # C: SCADUTA (40 giorni)
        # D: Nessun accesso
        # E: Senza CF, match per nome (35 giorni) -> SCADUTA
        dipendenti = [
            ("A", "A", "CF_A"),
            ("B", "B", "CF_B"),
            ("C", "C", "CF_C"),
            ("D", "D", "CF_D"),
            ("E", "E", ""),
        ]
        
        # 2. Accessi
        # Mock Now: 2024-02-01
        # A: 2024-01-22 (Delta 10)
        # B: 2024-01-07 (Delta 25)
        # C: 2023-12-23 (Delta 40)
        # E: 2023-12-28 (Delta 35)
        accessi = [
            ("A", "A", "CF_A", "2024-01-22"),
            ("B", "B", "CF_B", "2024-01-07"),
            ("C", "C", "CF_C", "2023-12-23"),
            ("E", "E", "", "2023-12-28"),
        ]
        
        # Configura mock per restituire prima dipendenti poi accessi
        mock_query.side_effect = [dipendenti, accessi]
        
        mock_now = datetime(2024, 2, 1)
        with patch("src.core.auth_monitor.datetime") as mock_dt:
            mock_dt.now.return_value = mock_now
            mock_dt.strptime.side_effect = datetime.strptime
            
            results = auth_monitor.check_expiring_isab_authorizations()
            
            # Analisi risultati
            res_map = {r["cognome"]: r for r in results}
            
            assert "A" not in res_map # OK
            assert "D" not in res_map # No data
            
            assert "B" in res_map
            assert res_map["B"]["stato"] == "IN SCADENZA"
            assert res_map["B"]["giorni_trascorsi"] == 25
            
            assert "C" in res_map
            assert res_map["C"]["stato"] == "SCADUTA"
            assert res_map["C"]["giorni_trascorsi"] == 40
            
            assert "E" in res_map
            assert res_map["E"]["stato"] == "SCADUTA"
            assert res_map["E"]["cf_mancante"] is True

    @patch("src.core.database.db_manager.execute_query")
    def test_check_expiring_authorizations_error(self, mock_query):
        """Test gestione errore DB."""
        mock_query.side_effect = Exception("DB Error")
        
        res = auth_monitor.check_expiring_isab_authorizations()
        assert res == []