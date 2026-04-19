from pathlib import Path

from oletools.olevba import VBA_Parser  # type: ignore


def extract_vba_no_excel(file_path: str, output_md: str) -> None:
    p_file = Path(file_path)
    if not p_file.exists():
        print(f"File non trovato: {file_path}")
        return

    try:
        parser = VBA_Parser(file_path)
        if not parser.detect_vba_macros():
            print("Nessuna macro rilevata nel file.")
            return

        p_out = Path(output_md)
        with p_out.open("w", encoding="utf-8") as f:
            f.write(f"# Knowledge Base VBA: {p_file.name}\n\n")
            f.write(
                "Questo file contiene il codice estratto senza l'uso di Excel (bypassando gli errori UI).\n\n"
            )

            for _, stream_path, vba_filename, vba_code in parser.extract_macros():
                f.write(f"## Componente: {vba_filename}\n")
                f.write(f"Stream: {stream_path}\n\n")

                if vba_code:
                    f.write("```vba\n")
                    f.write(vba_code)
                    f.write("\n```\n\n")
                else:
                    f.write("*Codice vuoto.*\n\n")

        print(f"Estrazione completata con successo in {output_md}")

    except Exception as e:
        print(f"Errore durante l'analisi OLE: {e}")


if __name__ == "__main__":
    target = "data/master_consuntivo_Automatico.xlsm"
    output = r"docs/VBA_KNOW_HOW.md"
    Path("docs").mkdir(parents=True, exist_ok=True)
    extract_vba_no_excel(target, output)
