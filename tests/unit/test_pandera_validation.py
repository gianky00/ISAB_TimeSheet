import pandas as pd
import pytest
from rich.console import Console

from src.core.schemas import validate_dipendenti

console = Console()


def test_validate_real_anagrafica():
    """Testa la validazione sullo script reale anagrafica_dipendenti.csv."""
    path = "anagrafica_dipendenti.csv"
    try:
        # Caricamento con i parametri corretti identificati
        df = pd.read_csv(
            path,
            sep=";",
            dayfirst=True,
            parse_dates=["Data_nascita", "Data_assunzione"],
        )

        validated_df = validate_dipendenti(df)

        console.print(f"[green]✅ Validazione completata con successo per {len(validated_df)} righe.[/green]")
        assert not validated_df.empty

    except Exception as e:
        console.print(f"[red]❌ Errore durante la validazione:[/red] {str(e)}")
        pytest.fail(f"Validazione fallita: {e}")


if __name__ == "__main__":
    test_validate_real_anagrafica()
