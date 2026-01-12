import subprocess
import sys
import time
from pathlib import Path

def main():
    """
    Esegue i test Pytest file per file in processi separati.
    Questo previene che memory leaks o GDI handle exhaustion in un test
    facciano crashare l'intera suite.
    """
    # 1. Trova tutti i file di test
    root_dir = Path(__file__).parent.parent
    tests_dir = root_dir / "tests"
    
    test_files = sorted(list(tests_dir.rglob("test_*.py")))
    
    # Filtra eventuali file in cartelle cache o non pertinenti
    test_files = [f for f in test_files if "__pycache__" not in str(f)]

    total_files = len(test_files)
    print(f"--- Trovati {total_files} file di test. Avvio isolamento per file ---\n")

    failed_files = []
    start_time = time.time()

    # 2. Esegui ogni file in un subprocess
    for index, test_file in enumerate(test_files, 1):
        rel_path = test_file.relative_to(root_dir)
        print(f"[{index}/{total_files}] Esecuzione: {rel_path} ... ", end="", flush=True)
        
        file_start = time.time()
        
        # Comando: python -m pytest <file>
        cmd = [sys.executable, "-m", "pytest", str(test_file), "--no-header", "--quiet"]
        
        # Esegui e cattura l'output
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=root_dir
        )
        
        duration = time.time() - file_start
        
        if result.returncode == 0:
            print(f"PASS ({duration:.2f}s)")
        else:
            print(f"FAIL ({duration:.2f}s)")
            failed_files.append((rel_path, result.stdout, result.stderr))

    total_duration = time.time() - start_time
    print("\n" + "="*60)
    print(f"ESECUZIONE TERMINATA in {total_duration:.2f}s")
    print("="*60)

    # 3. Report Finale
    if not failed_files:
        print("\nSUCCESS: Tutti i file di test sono passati!")
        sys.exit(0)
    else:
        print(f"\nERROR: {len(failed_files)} file hanno fallito:\n")
        for path, out, err in failed_files:
            print(f"--- Errore in: {path} ---")
            print(out if out else "Nessun output su stdout")
            print(err if err else "")
            print("-" * 40)
        sys.exit(1)

if __name__ == "__main__":
    main()