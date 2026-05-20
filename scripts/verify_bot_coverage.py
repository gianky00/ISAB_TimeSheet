import sys
from pathlib import Path

import coverage
import pytest


def run_coverage_for_bot(test_file: Path, source_file: Path, bot_name: str) -> float:
    print("\n" + "=" * 50)
    print(f"ANALISI COVERAGE PER: {bot_name}")
    print("=" * 50)

    # Configuriamo coverage per il file sorgente specifico
    cov = coverage.Coverage(source=[str(source_file)], branch=True)
    cov.erase()
    cov.start()

    # Esegue pytest
    pytest.main([str(test_file), "-q", "--no-header", "--no-summary"])

    cov.stop()
    cov.save()

    # Mostra report testuale delle righe mancanti
    print(f"\nReport dettagliato per {source_file}:")
    cov.report(show_missing=True)

    # Restituisce la percentuale per controllo finale
    return float(cov.report())


if __name__ == "__main__":
    root = Path.cwd()
    sys.path.insert(0, str(root))

    bots = [
        ("tests/unit/test_safework_pdl_bot_comprehensive.py", "src/bots/safework/pdl/bot.py", "SafeWork PDL"),
        (
            "tests/unit/test_dettagli_oda_comprehensive.py",
            "src/bots/portale_fornitori/dettagli_oda/bot.py",
            "Dettagli OdA",
        ),
        (
            "tests/unit/test_scarico_ts_comprehensive.py",
            "src/bots/portale_fornitori/scarico_ts/bot.py",
            "Scarico TS",
        ),
    ]

    results = [run_coverage_for_bot(root / t, root / s, n) for t, s, n in bots]

    print("\n" + "=" * 50)
    print("RIEPILOGO FINALE COVERAGE BOT")
    print("=" * 50)
    for i, res in enumerate(results):
        print(f"{bots[i][2]}: {res:.2f}%")
