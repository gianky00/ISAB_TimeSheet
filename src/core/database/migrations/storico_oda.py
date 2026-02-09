import sqlite3


def mig_storico_oda_v1(conn: sqlite3.Connection) -> None:
    """Schema Iniziale Storico OdA (v1)"""
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS storico_oda (
            oda TEXT,
            pos_oda TEXT,
            num_riga TEXT,
            org_acq TEXT,
            data_oda TEXT,
            stato TEXT,
            cat_contab TEXT,
            descrizione TEXT,
            qta REAL,
            uom TEXT,
            data_consegna TEXT,
            valore_netto_pos REAL,
            valore_residuo REAL,
            valore_netto_oda REAL,
            divisione TEXT,
            destinatario TEXT,
            nome_destinatario TEXT,
            codice_fornitore TEXT,
            descrizione_fornitore TEXT,
            emittente_fattura TEXT,
            desc_emittente_fattura TEXT,
            contract_card TEXT,
            contratto TEXT,
            posizione_contratto TEXT,
            gruppo_acquisti TEXT,
            indicatore_rilascio TEXT,
            stato_rilascio TEXT,
            attivita TEXT,
            quantita REAL,
            unita_mis TEXT,
            prezzo_lordo REAL,
            testo_breve TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (oda, pos_oda, num_riga)
        )
    """
    )
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_oda_data_oda ON storico_oda(data_oda)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_oda_fornitore ON storico_oda(codice_fornitore)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_oda_contratto ON storico_oda(contratto)")


def mig_storico_oda_v2(conn: sqlite3.Connection) -> None:
    """Fix tipi colonne per evitare overflow (v2)"""
    # Poiché SQLite non supporta ALTER COLUMN facilmente, e i dati sono corrotti/cache,
    # ricreiamo la tabella.
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS storico_oda")
    mig_storico_oda_v1(conn)
