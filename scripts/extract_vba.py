import os

from oletools.olevba import VBA_Parser  # type: ignore


def extract_vba_no_excel(file_path: str, output_md: str) -> None:
    if not os.path.exists(file_path):
        print(f"File non trovato: {file_path}")
        return

    try:
        parser = VBA_Parser(file_path)
        if not parser.detect_vba_macros():
            print("Nessuna macro rilevata nel file.")
            return

        with open(output_md, "w", encoding="utf-8") as f:
            f.write(f"# Knowledge Base VBA: {os.path.basename(file_path)}\n\n")
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
    target = r"C:\Users\Coemi\Desktop\SCRIPT\ISAB_TimeSheet\master_consuntivo_Automatico.xlsm"
    output = r"docs/VBA_KNOW_HOW.md"
    os.makedirs("docs", exist_ok=True)
    extract_vba_no_excel(target, output)
