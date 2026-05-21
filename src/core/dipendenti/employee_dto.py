"""
SyncroJob - Employee DTO
Oggetti di trasporto dati per il modulo Dipendenti.
Garantisce l'incapsulamento e previene la data leakage verso la GUI.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EmployeeDTO:
    """Rappresenta un dipendente con i relativi metadati di monitoraggio."""

    id_risorsa: str
    cognome: str
    nome: str
    data_nascita: str | None = None
    badge: str | None = None
    data_assunzione: str | None = None
    codice_fiscale: str | None = None
    monitoraggio_attivo: bool = True

    # Campi calcolati per la UI
    inactivation_days_left: int | None = None
    cf_warning: bool = False
    last_access_isab: str | None = None

    @property
    def full_name(self) -> str:
        """Restituisce il nome completo formattato."""
        cog = f"⚠️ {self.cognome}" if self.cf_warning else self.cognome
        return f"{cog} {self.nome}"

    def to_table_row(self) -> list[str | int | None]:
        """Restituisce i campiùper la riga della tabella anagrafica."""
        return [
            self.inactivation_days_left,  # 0
            self.id_risorsa,  # 1
            f"⚠️ {self.cognome}" if self.cf_warning else self.cognome,  # 2
            self.nome,  # 3
            self.codice_fiscale or "-",  # 4
            self.badge or "-",  # 5
            self.data_assunzione or "-",  # 6
            self.last_access_isab or "Mai effettuato",  # 7
            self.data_nascita or "-",  # 8
            "",  # 9: data_import placeholder
            self.cognome,  # 10: Original cognome for sorting
        ]

    def get_metadata(self) -> dict[str, str | bool]:
        """Restituisce i metadati per il TableModel (UserRole)."""
        return {"id_risorsa": self.id_risorsa, "is_monitored": self.monitoraggio_attivo}
