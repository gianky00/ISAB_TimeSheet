from dataclasses import dataclass


@dataclass
class EmployeeRecord:
    """Modello per un record di Anagrafica Dipendenti."""
    id_risorsa: int | None
    cognome: str
    nome: str
    badge: str
    codice_fiscale: str
    data_assunzione: str | None
    monitoraggio_attivo: int = 1
    data_nascita: str | None = None

    @property
    def full_name(self) -> str:
        """Restituisce il nome completo."""
        return f"{self.cognome} {self.nome}".strip()
