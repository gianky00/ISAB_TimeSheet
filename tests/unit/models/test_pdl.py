from src.models.pdl import PdlProgrammazioneRecord, PdlRecord


class TestPdlModels:
    def test_pdl_record_creation(self):
        """Testa la creazione di base del modello PdlRecord."""
        record = PdlRecord(
            id=1,
            n_pdl="123456/C",
            data_creazione="2026-05-17",
            area="Area A",
            unita="Unita 1",
            ditta="Coemi",
            descrizione_lavoro="Manutenzione ordinaria",
            tipologia="Elettrico",
            stato="Aperto",
            apparecchiatura="APP-001",
            richiedente="Mario Rossi",
            data_richiesta="2026-05-16",
            emittente="Luigi Bianchi",
            data_emissione="2026-05-16 10:00",
            aprente="Giovanni Verdi",
            data_apertura="2026-05-17 08:00",
            priorita="Alta",
            contratto="C-2026-01",
            ordine="ODA-001",
            sito="ISAB Sud",
            importato_il="2026-05-17 08:30",
        )

        assert record.id == 1
        assert record.n_pdl == "123456/C"
        assert record.area == "Area A"
        assert record.ditta == "Coemi"
        assert record.stato == "Aperto"

    def test_pdl_programmazione_record_creation(self):
        """Testa la creazione di base del modello PdlProgrammazioneRecord."""
        record = PdlProgrammazioneRecord(
            id=None,
            richiedente="Mario Rossi",
            n_pdl="123456/C",
            area="Area B",
            unita="Unita 2",
            descrizione="Manutenzione straordinaria",
            lun_tcl=True,
            lun_tgo=False,
            mar_tcl=True,
            mar_tgo=False,
            mer_tcl=True,
            mer_tgo=False,
            gio_tcl=True,
            gio_tgo=False,
            ven_tcl=True,
            ven_tgo=True,
            sab_tcl=False,
            sab_tgo=False,
            dom_tcl=False,
            dom_tgo=False,
            settimana_start="2026-05-18",
            settimana_end="2026-05-24",
            ultimo_aggiornamento="2026-05-17",
        )

        assert record.id is None
        assert record.n_pdl == "123456/C"
        assert record.lun_tcl is True
        assert record.sab_tgo is False
        assert record.settimana_start == "2026-05-18"
        assert record.ultimo_aggiornamento == "2026-05-17"

    def test_pdl_programmazione_record_default_args(self):
        """Testa il valore di default per l'ultimo argomento in PdlProgrammazioneRecord."""
        record = PdlProgrammazioneRecord(
            id=1,
            richiedente="Mario Rossi",
            n_pdl="123456/C",
            area="Area B",
            unita="Unita 2",
            descrizione="Manutenzione straordinaria",
            lun_tcl=False,
            lun_tgo=False,
            mar_tcl=False,
            mar_tgo=False,
            mer_tcl=False,
            mer_tgo=False,
            gio_tcl=False,
            gio_tgo=False,
            ven_tcl=False,
            ven_tgo=False,
            sab_tcl=False,
            sab_tgo=False,
            dom_tcl=False,
            dom_tgo=False,
            settimana_start="2026-05-18",
            settimana_end="2026-05-24",
        )

        assert record.ultimo_aggiornamento is None
