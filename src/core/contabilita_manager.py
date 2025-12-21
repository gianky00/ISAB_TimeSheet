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
                warnings.simplefilter("ignore")

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

                        # 1. Rimuovi righe completamente vuote
                        df.dropna(how='all', inplace=True)
                        if df.empty:
                            continue

                        # 2. Aggiungi colonna anno
                        df['year'] = year

                        # 3. Gestione Mapping e Colonne mancanti
                        # Mappa le colonne presenti nel DF ai nomi DB
                        rename_map = {k: v for k, v in cls.COLUMNS_MAPPING.items() if k in df.columns}
                        df.rename(columns=rename_map, inplace=True)

                        # Aggiungi le colonne DB mancanti come stringhe vuote
                        for db_col in cls.COLUMNS_MAPPING.values():
                            if db_col not in df.columns:
                                df[db_col] = ""

                        # 4. Seleziona e ordina le colonne per l'inserimento
                        target_columns = ['year'] + list(cls.COLUMNS_MAPPING.values())
                        df = df[target_columns]

                        # 5. Pulizia dati e conversione stringhe
                        # fillna("") converte NaN in stringa vuota
                        df = df.fillna("")
                        
                        # Converti colonne tranne 'year' in stringa
                        cols_to_str = [c for c in df.columns if c != 'year']
                        df[cols_to_str] = df[cols_to_str].astype(str)

                        # Transazione per anno: Cancella vecchi dati dell'anno e inserisci nuovi
                        cursor.execute("DELETE FROM contabilita WHERE year = ?", (year,))

                        # Prepara query inserimento
                        placeholders = ', '.join(['?'] * len(target_columns))
                        query = f"INSERT INTO contabilita ({', '.join(target_columns)}) VALUES ({placeholders})"

                        # Prepara lista di tuple (molto più veloce del loop manuale)
                        values = list(df.itertuples(index=False, name=None))

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

    @classmethod
    def get_year_stats(cls, year: int) -> Dict:
        """Calcola statistiche avanzate per l'anno specificato."""
        data = cls.get_data_by_year(year)
        if not data:
            return {}

        stats = {
            "total_prev": 0.0,
            "total_ore": 0.0,
            "count_total": len(data),
            "status_counts": {},
            "top_commesse": []
        }

        commesse = []

        for row in data:
            # row indexes based on get_data_by_year cols:
            # 0: data_prev, 1: mese, 2: n_prev, 3: totale_prev, 4: attivita,
            # 5: tcl, 6: odc, 7: stato, 8: tipologia, 9: ore_sp, 10: resa...

            # Parse Totale Prev
            try:
                t_str = str(row[3]).replace('.','').replace(',','.').replace('€','').strip()
                val_prev = float(t_str) if t_str else 0.0
            except: val_prev = 0.0

            # Parse Ore Sp
            try:
                o_str = str(row[9]).replace(',','.').strip()
                val_ore = float(o_str) if o_str else 0.0
            except: val_ore = 0.0

            stats["total_prev"] += val_prev
            stats["total_ore"] += val_ore

            # Status Count
            status = str(row[7]).strip().upper()
            if status:
                stats["status_counts"][status] = stats["status_counts"].get(status, 0) + 1

            # For Top Commesse
            if val_prev > 0:
                attivita = str(row[4]).strip() or "N/D"
                commesse.append((attivita, val_prev))

        # Top 5 Commesse
        commesse.sort(key=lambda x: x[1], reverse=True)
        stats["top_commesse"] = commesse[:5]

        return stats
