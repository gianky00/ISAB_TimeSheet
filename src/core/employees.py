import csv
import logging
import sqlite3
from pathlib import Path
from typing import Any

from src.core.database import db_manager

logger = logging.getLogger(__name__)


class EmployeeManager:
    """
    Gestisce la logica di business per i dipendenti, facendo da interfaccia
    tra la GUI/Bot e il Database SQLite.
    Sostituisce la gestione diretta dei file CSV.
    """

    def __init__(self) -> None:
        self.db = db_manager

    def get_all_employees(self, active_only: bool = True) -> list[dict[str, Any]]:
        """Restituisce tutti i dipendenti dal database come lista di dizionari."""
        # Selezioniamo colonne esplicite per sicurezza
        query = "SELECT id_risorsa, cognome, nome, badge, codice_fiscale, data_assunzione, monitoraggio_attivo FROM dipendenti"

        try:
            # Verifica se la colonna monitoraggio_attivo esiste provando una select limitata
            # Se fallisce, fallback su query senza filtro
            rows = []
            try:
                final_query = query
                if active_only:
                    final_query += " WHERE monitoraggio_attivo = 1"
                final_query += " ORDER BY cognome, nome"
                rows = self.db.execute_query(self.db.DB_DIPENDENTI, final_query)
            except sqlite3.OperationalError:
                # Fallback per schema vecchio
                query_fallback = "SELECT id_risorsa, cognome, nome, badge, codice_fiscale, data_assunzione FROM dipendenti ORDER BY cognome, nome"
                rows = self.db.execute_query(self.db.DB_DIPENDENTI, query_fallback)

            # Conversione Tupla -> Dict
            employees = []
            for row in rows:
                # Gestiamo il caso in cui la query fallback ha meno colonne
                has_monitoraggio = len(row) >= 7  # noqa: PLR2004

                emp = {
                    "id_risorsa": row[0],
                    "cognome": row[1],
                    "nome": row[2],
                    "badge": row[3],
                    "codice_fiscale": row[4],
                    "data_assunzione": row[5],
                    "monitoraggio_attivo": row[6] if has_monitoraggio else 1,
                }
                employees.append(emp)

            return employees  # noqa: TRY300

        except Exception as e:
            logger.error(f"Errore recupero dipendenti: {e}")  # noqa: TRY400
            return []

    def get_employee_by_badge(self, badge: str) -> sqlite3.Row | None:
        """Cerca un dipendente per numero di badge."""
        query = "SELECT * FROM dipendenti WHERE badge = ?"
        results = self.db.execute_query(self.db.DB_DIPENDENTI, query, (badge,))
        return results[0] if results else None

    def add_employee(self, employee_data: dict[str, Any]) -> bool:
        """
        Aggiunge un nuovo dipendente.
        employee_data deve contenere: nome, cognome, badge, ecc.
        """
        query = """
            INSERT INTO dipendenti (
                id_risorsa, cognome, nome, data_nascita,
                codice_fiscale, badge, data_assunzione, monitoraggio_attivo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            employee_data.get("id_risorsa"),  # Può essere None (autoincrement) o specifico
            employee_data["cognome"].upper(),
            employee_data["nome"].upper(),
            employee_data.get("data_nascita"),
            employee_data.get("codice_fiscale", "").upper(),
            employee_data.get("badge"),
            employee_data.get("data_assunzione"),
            1,  # Default attivo
        )

        try:
            self.db.execute_query(self.db.DB_DIPENDENTI, query, params)
            logger.info(f"Dipendente {employee_data['cognome']} aggiunto con successo.")
            return True  # noqa: TRY300
        except sqlite3.IntegrityError as e:
            logger.error(f"Errore inserimento dipendente: {e}")  # noqa: TRY400
            return False

    def update_employee(self, id_risorsa: int, data: dict[str, Any]) -> bool:
        """Aggiorna i dati di un dipendente esistente."""
        # Costruiamo la query dinamicamente in base ai campi forniti
        fields = []
        values = []
        for key, value in data.items():
            fields.append(f"{key} = ?")
            values.append(value)

        values.append(id_risorsa)  # Per le WHERE

        query = f"UPDATE dipendenti SET {', '.join(fields)} WHERE id_risorsa = ?"  # nosec B608

        try:
            self.db.execute_query(self.db.DB_DIPENDENTI, query, tuple(values))
            logger.info(f"Dipendente ID {id_risorsa} aggiornato.")
            return True  # noqa: TRY300
        except Exception as e:
            logger.error(f"Errore aggiornamento dipendente: {e}")  # noqa: TRY400
            return False

    def import_from_csv(self, csv_path: str) -> int:
        """
        Importa/Sincronizza i dipendenti dal vecchio CSV al DB.
        Ritorna il numero di record importati.
        """
        path = Path(csv_path)
        if not path.exists():
            logger.error(f"File CSV non trovato: {csv_path}")
            return 0

        import time  # noqa: PLC0415

        from src.core.sync_tracker import SyncTracker  # noqa: PLC0415

        start_time = time.time()
        added_count = 0
        updated_count = 0
        count = 0

        try:
            with path.open("r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f, delimiter=";")

                # Normalizziamo i nomi delle colonne rimuovendo spazi extra
                if reader.fieldnames:
                    reader.fieldnames = [name.strip() for name in reader.fieldnames]

                for row in reader:
                    # Mappatura CSV -> DB
                    id_val = row.get("id_risorsa") or row.get("ID")
                    id_risorsa = int(id_val) if id_val and str(id_val).isdigit() else None

                    data = {
                        "id_risorsa": id_risorsa,
                        "cognome": row.get("Cognome", ""),
                        "nome": row.get("Nome", ""),
                        "data_nascita": row.get("Data_nascita", ""),
                        "codice_fiscale": row.get("Codice_fiscale", ""),
                        "badge": row.get("Badge", ""),
                        "data_assunzione": row.get("Data_assunzione", ""),
                    }

                    # Controlla se esiste già (per badge o ID)
                    existing = None
                    if id_risorsa:
                        existing = self.db.execute_query(
                            self.db.DB_DIPENDENTI,
                            "SELECT id_risorsa FROM dipendenti WHERE id_risorsa = ?",
                            (id_risorsa,),
                        )

                    if existing and id_risorsa is not None:
                        self.update_employee(id_risorsa, data)
                        updated_count += 1
                    else:
                        self.add_employee(data)
                        added_count += 1

                    count += 1

            duration = time.time() - start_time
            # Consideriamo "Added" i nuovi, e Removed 0.
            # (In futuro si potrebbe calcolare removed se il CSV fosse l'unica fonte di verità)
            SyncTracker.update_status("dipendenti", added_count, 0, duration)

            logger.info(f"Importazione completata: {count} dipendenti processati ({added_count} nuovi).")
            return count  # noqa: TRY300

        except Exception as e:
            logger.error(f"Errore durante l'importazione CSV: {e}")  # noqa: TRY400
            raise


# Istanza globale
employee_manager = EmployeeManager()
