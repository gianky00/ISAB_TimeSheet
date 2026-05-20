from src.models.oda import OdaRecord


class TestOdaModels:
    def test_oda_record_creation(self):
        """Testa la creazione di base del modello OdaRecord."""
        record = OdaRecord(
            id=1,
            org_acq="ORG-1",
            data_oda="2026-05-17",
            oda="ODA-12345",
            pos_oda="10",
            stato="Attivo",
            cat_contab="K",
            descrizione="Fornitura materiale",
            qta=100.5,
            uom="PZ",
            data_consegna="2026-06-01",
            valore_netto_pos=1500.0,
            valore_residuo=500.0,
            valore_netto_oda=15000.0,
            divisione="DIV-A",
            destinatario="Magazzino",
            nome_destinatario="Mario Rossi",
            codice_fornitore="F-001",
            descrizione_fornitore="Fornitore Test SPA",
            emittente_fattura="E-001",
            desc_emittente_fattura="Emittente Test SRL",
            contract_card="CC-999",
            contratto="CON-2026",
            posizione_contratto="20",
            gruppo_acquisti="G-1",
            indicatore_rilascio="R",
            stato_rilascio="Rilasciato",
            attivita="Attività Test",
            num_riga="1",
            quantita=50.0,
            unita_mis="PZ",
            prezzo_lordo=2000.0,
            testo_breve="Note brevi",
        )

        assert record.id == 1
        assert record.oda == "ODA-12345"
        assert record.qta == 100.5
        assert record.valore_netto_pos == 1500.0
        assert record.codice_fornitore == "F-001"

    def test_oda_record_default_id(self):
        """Testa la creazione di OdaRecord senza specificare l'id (default None)."""
        record = OdaRecord(
            org_acq="ORG-1",
            data_oda="2026-05-17",
            oda="ODA-12345",
            pos_oda="10",
            stato="Attivo",
            cat_contab="K",
            descrizione="Desc",
            qta=1.0,
            uom="PZ",
            data_consegna="2026-06-01",
            valore_netto_pos=10.0,
            valore_residuo=10.0,
            valore_netto_oda=100.0,
            divisione="DIV-A",
            destinatario="Magazzino",
            nome_destinatario="Nome",
            codice_fornitore="F",
            descrizione_fornitore="DescF",
            emittente_fattura="E",
            desc_emittente_fattura="DescE",
            contract_card="CC",
            contratto="C",
            posizione_contratto="1",
            gruppo_acquisti="G",
            indicatore_rilascio="R",
            stato_rilascio="S",
            attivita="A",
            num_riga="1",
            quantita=1.0,
            unita_mis="PZ",
            prezzo_lordo=10.0,
            testo_breve="T",
        )

        assert record.id is None
        assert record.oda == "ODA-12345"
