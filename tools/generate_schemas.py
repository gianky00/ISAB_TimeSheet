#!/usr/bin/env python
"""Script per generare automaticamente i JSON Schema delle configurazioni Pydantic.

Questo script esporta lo schema JSON della configurazione centralizzata di SyncroJob,
consentendo a IDE ed assistenti IA di validare e autocompilare i file di configurazione.
"""

import json
import os
import sys

# Aggiungiamo la root del progetto al path per consentire gli import di src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.config.settings import SyncroJobSettings


def main() -> None:
    """Genera ed esporta lo schema JSON delle impostazioni di SyncroJob."""
    print("Generazione JSON Schema per SyncroJobSettings...")

    # Cartella di output
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../docs/schemas"))
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "config.schema.json")

    try:
        # Pydantic v2 utilizza model_json_schema()
        schema = SyncroJobSettings.model_json_schema()

        # Scrittura dello schema in formato indentato ed ordinato
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(schema, f, indent=4, ensure_ascii=False)

        print(f"ECCELLENTE! Schema esportato con successo in: {output_file}")
        sys.exit(0)
    except Exception as e:
        print(f"Errore durante la generazione dello schema: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
