"""
Bot TS - Contabilita Manager
Gestione dell'importazione e archiviazione dati della Contabilità Strumentale.
"""
import sqlite3
import pandas as pd
from pathlib import Path
import re
import logging
import warnings
from typing import List, Dict, Tuple, Optional

class ContabilitaManager:
    """Manager per la gestione del database e dell'importazione Excel."""

    DB_PATH = Path("data/contabilita.db")

    # Mapping colonne Excel -> DB
    # Nota: Le colonne Excel potrebbero avere nomi leggermente diversi o spazi,
    # ma useremo gli indici o cercheremo di normalizzare se possibile.
    # Qui assumiamo che i nomi nel file Excel siano esattamente quelli richiesti
    # o molto simili.
    COLUMNS_MAPPING = {
        'DATA PREV.': 'data_prev',
        'MESE': 'mese',
        'N°PREV.': 'n_prev',
        'TOTALE PREV.': 'totale_prev',
        "ATTIVITA'": 'attivita',
        'TCL': 'tcl',
        'ODC': 'odc',
        "STATO ATTIVITA'": 'stato_attivita',
        'TIPOLOGIA': 'tipologia',
        'ORE SP': 'ore_sp',
        'RESA': 'resa',
        'ANNOTAZIONI': 'annotazioni',
        'INDIRIZZO CONSUNTIVO': 'indirizzo_consuntivo',
        'NOME FILE': 'nome_file'
    }

    @classmethod
    def init_db(cls):
        """Inizializza il database creando la tabella se non esiste."""
        cls.DB_PATH.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()

        # Creazione tabella
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contabilita (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                data_prev TEXT,
                mese TEXT,
                n_prev TEXT,
                totale_prev TEXT,
                attivita TEXT,
                tcl TEXT,
                odc TEXT,
                stato_attivita TEXT,
                tipologia TEXT,
                ore_sp TEXT,
                resa TEXT,
                annotazioni TEXT,
                indirizzo_consuntivo TEXT,
                nome_file TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    @classmethod
    def import_data_from_excel(cls, file_path: str) -> Tuple[bool, str]:
        """
        Importa i dati dal file Excel specificato.

        Args:
            file_path: Percorso del file Excel.

        Returns:
            Tuple (Successo: bool, Messaggio: str)
        """
        path = Path(file_path)
        if not path.exists():
            return False, f"File non trovato: {file_path}"

        try:
            # Sopprimi i warning di openpyxl (es. Print area, Unknown extension)
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

                # Carica il file Excel (tutti i fogli)
                # engine='openpyxl' è standard per .xlsx/.xlsm
                xls = pd.ExcelFile(path, engine='openpyxl')

                imported_years = []

                conn = sqlite3.connect(cls.DB_PATH)
                cursor = conn.cursor()

                for sheet_name in xls.sheet_names:
                    # Controlla se il nome del foglio contiene un anno (4 cifre)
                    # Regex: cerca 4 cifre consecutive, es "2024", "Anno 2025"
                    match = re.search(r'(\d{4})', sheet_name)
                    if not match:
                        continue

                    year = int(match.group(1))

                    # Validazione base anno (es. tra 2000 e 2100 per evitare falsi positivi)
                    if not (2000 <= year <= 2100):
                        continue

                    try:
                        # Legge il foglio. Intestazioni alla riga 2 (index 1) -> header=1
                        df = pd.read_excel(xls, sheet_name=sheet_name, header=1)

                        # Rimuovi sistematicamente l'ultima riga (presunta riga totali del file Excel)
                        if not df.empty:
                            df = df.iloc[:-1]

                        # Normalizza i nomi delle colonne per il mapping
                        # Rimuove spazi extra e converte in upper per confronto
                        df.columns = [str(c).strip().upper() for c in df.columns]

                        # Filtra solo le colonne che ci interessano
                        # Costruiamo un DataFrame pulito da inserire
                        data_to_insert = []

                        for _, row in df.iterrows():
                            # Salta righe vuote (es. se data prev è vuota, spesso la riga è vuota)
                            # O se tutte sono NaN
                            if row.isna().all():
                                continue

                            record = {'year': year}

                            for excel_col, db_col in cls.COLUMNS_MAPPING.items():
                                # Cerca la colonna nel dataframe
                                if excel_col in df.columns:
                                    val = row[excel_col]
                                    # Converti in stringa gestendo i NaN
                                    if pd.isna(val):
                                        val = ""
                                    else:
                                        # Se è una data, formatta? Per ora stringa
                                        val = str(val)
                                    record[db_col] = val
                                else:
                                    record[db_col] = "" # Colonna mancante nel foglio

                            data_to_insert.append(record)

                        if not data_to_insert:
                            continue

                        # Transazione per anno: Cancella vecchi dati dell'anno e inserisci nuovi
                        cursor.execute("DELETE FROM contabilita WHERE year = ?", (year,))

                        # Prepara query inserimento
                        columns = ['year'] + list(cls.COLUMNS_MAPPING.values())
                        placeholders = ', '.join(['?'] * len(columns))
                        query = f"INSERT INTO contabilita ({', '.join(columns)}) VALUES ({placeholders})"

                        # Prepara lista di tuple
                        values = []
                        for item in data_to_insert:
                            row_vals = [item['year']]
                            for col in cls.COLUMNS_MAPPING.values():
                                row_vals.append(item.get(col, ""))
                            values.append(tuple(row_vals))

                        cursor.executemany(query, values)
                        imported_years.append(year)

                    except Exception as e:
                        print(f"Errore importazione foglio {sheet_name}: {e}")
                        continue

                conn.commit()
                conn.close()

                if not imported_years:
                    return False, "Nessun foglio valido (con anno) trovato o dati vuoti."

                return True, f"Importazione completata per gli anni: {sorted(imported_years)}"

        except Exception as e:
            return False, f"Errore generale importazione: {e}"

    @classmethod
    def get_available_years(cls) -> List[int]:
        """Restituisce la lista degli anni presenti nel DB."""
        if not cls.DB_PATH.exists():
            return []

        try:
            conn = sqlite3.connect(cls.DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT year FROM contabilita ORDER BY year DESC")
            years = [row[0] for row in cursor.fetchall()]
            conn.close()
            return years
        except:
            return []

    @classmethod
    def get_data_by_year(cls, year: int) -> List[Tuple]:
        """
        Restituisce i dati per un anno specifico.
        Ritorna lista di tuple ordinate per id.
        """
        if not cls.DB_PATH.exists():
            return []

        try:
            conn = sqlite3.connect(cls.DB_PATH)
            cursor = conn.cursor()
            # Seleziona colonne nell'ordine di visualizzazione + hidden
            # Ordine visualizzazione: 'DATA PREV.', 'MESE', 'N°PREV.', 'TOTALE PREV.', "ATTIVITA'",
            # 'TCL', 'ODC', "STATO ATTIVITA'", 'TIPOLOGIA', 'ORE SP', 'RESA', 'ANNOTAZIONI'
            # Hidden: 'INDIRIZZO CONSUNTIVO', 'NOME FILE'
            cols = [
                'data_prev', 'mese', 'n_prev', 'totale_prev', 'attivita', 'tcl', 'odc',
                'stato_attivita', 'tipologia', 'ore_sp', 'resa', 'annotazioni',
                'indirizzo_consuntivo', 'nome_file'
            ]
            query = f"SELECT {', '.join(cols)} FROM contabilita WHERE year = ? ORDER BY id"
            cursor.execute(query, (year,))
            rows = cursor.fetchall()
            conn.close()
            return rows
        except:
            return []
