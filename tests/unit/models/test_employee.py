from src.domain.employee import EmployeeRecord


class TestEmployeeModels:
    def test_employee_record_creation(self):
        """Testa la creazione e attributi di base di EmployeeRecord."""
        record = EmployeeRecord(
            cognome="Rossi",
            nome="Mario",
            badge="B-123",
            codice_fiscale="RSSMRA80A01H501U",
            data_assunzione="2020-01-01",
            id_risorsa=10,
            monitoraggio_attivo=1,
            data_nascita="1980-01-01",
        )

        assert record.cognome == "Rossi"
        assert record.nome == "Mario"
        assert record.badge == "B-123"
        assert record.id_risorsa == 10
        assert record.full_name == "Rossi Mario"

    def test_employee_record_defaults(self):
        """Testa la creazione di EmployeeRecord con i valori di default."""
        record = EmployeeRecord()

        assert record.cognome == ""
        assert record.nome == ""
        assert record.badge == ""
        assert record.codice_fiscale == ""
        assert record.data_assunzione is None
        assert record.id_risorsa is None
        assert record.monitoraggio_attivo == 1
        assert record.data_nascita is None
        assert record.full_name == ""

    def test_employee_record_partial_full_name(self):
        """Testa il property full_name quando manca nome o cognome."""
        record_only_cognome = EmployeeRecord(cognome="Rossi")
        assert record_only_cognome.full_name == "Rossi"

        record_only_nome = EmployeeRecord(nome="Mario")
        assert record_only_nome.full_name == "Mario"
