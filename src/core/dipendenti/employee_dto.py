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

    @property
    def full_name(self) -> str:
        """Restituisce il nome completo formattato."""
        cog = f"[ATTENZIONE] {self.cognome}" if self.cf_warning else self.cognome
        return f"{cog} {self.nome}"

    def to_table_row(self) -> list[str | int | None]:
        """Restituisce i campiu'per la riga della tabella anagrafica."""
        return [
            self.inactivation_days_left,
            self.id_risorsa,
            f"[ATTENZIONE] {self.cognome}" if self.cf_warning else self.cognome,
            self.nome,
            self.codice_fiscale or "-",
            self.badge or "-",
            self.data_assunzione or "-",
            self.data_nascita or "-",
            "",  # created_at (placeholder if needed)
            self.cognome,  # Original cognome for sorting/logic
        ]

    def get_metadata(self) -> dict[str, str | bool]:
        """Restituisce i metadati per il TableModel (UserRole)."""
        return {"id_risorsa": self.id_risorsa, "is_monitored": self.monitoraggio_attivo}
