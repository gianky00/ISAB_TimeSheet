import warnings
from collections.abc import Callable
from pathlib import Path
from typing import Any, ClassVar

import pandas as pd

from src.core.importers.base import BaseImporter


class StoricoOdaImporter(BaseImporter):
    """Importer per lo Storico OdA."""

    STORICO_ODA_MAPPING: ClassVar[dict[str, str]] = {
        "Org. Acq.": "org_acq",
        "Data OdA": "data_oda",
        "OdA": "oda",
        "Pos OdA": "pos_oda",
        "Stato": "stato",
        "Cat. Contab.": "cat_contab",
        "Descrizione": "descrizione",
        "Qta": "qta",
        "UOM": "uom",
        "Data Consegna": "data_consegna",
        "Valore Netto Pos. ODA": "valore_netto_pos",
        "Valore Residuo ODA": "valore_residuo",
        "Valore Netto ODA": "valore_netto_oda",
        "Divisione": "divisione",
        "Destinatario": "destinatario",
        "Nome Destinatario": "nome_destinatario",
        "Codice Fornitore": "codice_fornitore",
        "Descrizione Fornitore": "descrizione_fornitore",
        "Emittente Fattura": "emittente_fattura",
        "Descrizione Emittente Fattura": "desc_emittente_fattura",
        "Contract Card": "contract_card",
        "Contratto": "contratto",
        "Posizione Contratto": "posizione_contratto",
        "Gruppo Acquisti": "gruppo_acquisti",
        "Indicatore Rilascio": "indicatore_rilascio",
        "Stato Rilascio": "stato_rilascio",
        "Attività": "attivita",
        "Num riga": "num_riga",
        "Quantit ": "quantita",
        "Unità di Mis": "unita_mis",
        "Prezzo lordo": "prezzo_lordo",
        "Testo breve": "testo_breve",
    }

    STORICO_ODA_COLS: ClassVar[list[str]] = list(STORICO_ODA_MAPPING.values())

    @classmethod
    def import_storico_oda(
        cls,
        file_path: str,
        progress_callback: Callable[[int, int], None] | None = None,
    ) -> tuple[bool, str, list[tuple[Any, ...]]]:
        """Importa il file Storico OdA."""
        path = Path(file_path)
        if not path.exists():
            return False, f"File non trovato: {file_path}", []

        try:
            # 1. Lettura Excel
            df = cls._read_storico_oda_excel(path)
            if df.empty:
                return False, "Foglio vuoto.", []

            # 2. Mappatura Colonne
            rename_map = cls._map_storico_oda_columns(df)
            if not rename_map:
                return False, "Nessuna colonna riconosciuta.", []

            df.rename(columns=rename_map, inplace=True)
            df = df.loc[:, ~df.columns.duplicated()]

            # 3. Normalizzazione e Pulizia
            df = cls._normalize_storico_oda_df(df)
            cls._clean_storico_oda_data(df)

            # 4. Conversione in tuple
            data = [tuple(x) for x in df.to_numpy()]
            return True, f"Trovate {len(data)} righe.", data

        except Exception as e:
            return False, f"Errore importazione Storico OdA: {e}", []

    @classmethod
    def _read_storico_oda_excel(cls, path: Path) -> pd.DataFrame:
        """Legge il file excel tentando diversi fogli."""
        pd_obj = cls._get_pd()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                return pd_obj.read_excel(path, sheet_name="Formato PF")  # type: ignore[no-any-return]
            except ValueError:
                return pd_obj.read_excel(path, sheet_name=0)  # type: ignore[no-any-return]

    @classmethod
    def _map_storico_oda_columns(cls, df: pd.DataFrame) -> dict[str, str]:
        """Mappa le colonne dell'Excel a quelle del DB con precisione."""
        df.columns = df.columns.astype(str).str.strip()

        rename_map = {
            excel_col: db_col
            for excel_col, db_col in cls.STORICO_ODA_MAPPING.items()
            if excel_col in df.columns
        }

        # 2. Second Pass: Case-insensitive fallback (Strict name)
        for excel_col, db_col in cls.STORICO_ODA_MAPPING.items():
            if excel_col not in rename_map:
                for col in df.columns:
                    if col.lower() == excel_col.lower():
                        rename_map[col] = db_col
                        break

        return rename_map

    @classmethod
    def _normalize_storico_oda_df(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Assicura l'ordine esatto delle colonne richiesto dal DB."""
        return df.reindex(columns=cls.STORICO_ODA_COLS).fillna("")

    @classmethod
    def _clean_storico_oda_data(cls, df: pd.DataFrame) -> None:
        """Pulisce date, numeri e ID."""
        pd_obj = cls._get_pd()

        # Date
        for date_col in ("data_oda", "data_consegna"):
            df[date_col] = (
                pd_obj.to_datetime(df[date_col], errors="coerce").dt.strftime("%Y-%m-%d").fillna("")
            )

        # Numeri
        num_cols = [
            "qta",
            "valore_netto_pos",
            "valore_residuo",
            "valore_netto_oda",
            "quantita",
            "prezzo_lordo",
        ]
        for num_col in num_cols:
            df[num_col] = df[num_col].apply(cls._clean_euro_num)

        # IDs
        id_cols = [
            "oda",
            "pos_oda",
            "num_riga",
            "divisione",
            "destinatario",
            "contratto",
            "posizione_contratto",
        ]
        for str_col in id_cols:
            df[str_col] = df[str_col].fillna(0).astype(str).str.replace(r"\.0$", "", regex=True).str.strip()

        # Altre stringhe
        for col in df.columns:
            if col not in (*num_cols, "data_oda", "data_consegna", *id_cols):
                df[col] = df[col].fillna("").astype(str).str.strip()

    @staticmethod
    def _clean_euro_num(x: Any) -> float:
        """Helper for European numbers (1.234,56 -> 1234.56).

        Always returns float to match SQLite REAL column behavior (5.0 -> '5.0').
        """
        if pd.isna(x) or str(x).strip() == "":
            return 0.0
        if isinstance(x, (int, float)):
            return float(x)

        s = str(x).strip()
        if "." in s and "," in s:
            s = s.replace(".", "").replace(",", ".")
        elif "," in s:
            s = s.replace(",", ".")

        try:
            return float(s)
        except ValueError:
            return 0.0
