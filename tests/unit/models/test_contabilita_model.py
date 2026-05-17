from src.models.contabilita import (
    AttivitaProgrammataRecord,
    CertificatoCampioneRecord,
    ContabilitaRecord,
    GiornalieraRecord,
)


class TestContabilitaModels:
    def test_contabilita_record_creation(self):
        """Testa la creazione del modello ContabilitaRecord."""
        record = ContabilitaRecord(
            id=1,
            data_prev="2026-05-17",
            mese="Maggio",
            n_prev="PREV-001",
            totale_prev=1500.50,
            attivita="Manutenzione",
            tcl="TCL-A",
            odc="ODC-123",
            stato_attivita="Aperto",
            tipologia="Straordinaria",
            ore_sp=8.5,
            resa="100%",
            annotazioni="Nessuna nota",
            indirizzo_consuntivo="/path/to/file",
            nome_file="preventivo.pdf",
            year=2026,
        )

        assert record.id == 1
        assert record.totale_prev == 1500.50
        assert record.ore_sp == 8.5
        assert record.year == 2026

    def test_giornaliera_record_creation(self):
        """Testa la creazione del modello GiornalieraRecord."""
        record = GiornalieraRecord(
            id=2,
            data="2026-05-17",
            personale="Mario Rossi",
            tcl="TCL-B",
            descrizione="Lavoro in quota",
            n_prev="PREV-002",
            odc="ODC-456",
            pdl="123456/C",
            inizio="08:00",
            fine="17:00",
            ore=8.0,
            nome_file="giornaliera.xls",
            year=2026,
        )

        assert record.id == 2
        assert record.personale == "Mario Rossi"
        assert record.ore == 8.0
        assert record.year == 2026

    def test_attivita_programmata_record_creation(self):
        """Testa la creazione del modello AttivitaProgrammataRecord."""
        record = AttivitaProgrammataRecord(
            id=3,
            n_prev="PREV-003",
            odc="ODC-789",
            descrizione="Installazione quadro",
            data_inizio="2026-05-18",
            data_fine="2026-05-20",
            stato="Pianificata",
        )

        assert record.id == 3
        assert record.n_prev == "PREV-003"
        assert record.stato == "Pianificata"

    def test_certificato_campione_record_creation(self):
        """Testa la creazione del modello CertificatoCampioneRecord."""
        record = CertificatoCampioneRecord(
            id=4,
            id_coemi="C-001",
            certificato="CERT-999",
            modello="MOD-X",
            costruttore="Fluke",
            matricola="SN-12345",
            range_strumento="0-100V",
            errore_max="0.1%",
            emissione="2025-05-17",
            scadenza="2026-05-17",
            stato="Valido",
            annotazioni="Tutto ok",
            ubicazione="Laboratorio",
        )

        assert record.id == 4
        assert record.id_coemi == "C-001"
        assert record.costruttore == "Fluke"
        assert record.stato == "Valido"

    def test_certificato_campione_record_defaults(self):
        """Testa i default del modello CertificatoCampioneRecord."""
        record = CertificatoCampioneRecord(
            id_coemi="C-002",
            certificato="CERT-888",
            modello="MOD-Y",
            costruttore="Testo",
            matricola="SN-67890",
            range_strumento="0-10A",
            errore_max="0.5%",
            emissione="2025-05-17",
            scadenza="2026-05-17",
            stato="Valido",
        )
        assert record.id is None
        assert record.annotazioni is None
        assert record.ubicazione is None
