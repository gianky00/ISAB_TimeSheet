# 🧠 DEVTOOLS - AI ARCHITECT GUIDELINES

Sei all'interno di `devtools/`, l'arsenale per lo sviluppo, la CI/CD, la manutenzione e la build dell'applicazione.

## 🚨 REGOLE DEL LAYER (STRICT)
1. **ESECUZIONE INDIPENDENTE:** Ogni script in `devtools` deve essere pensato per poter essere eseguito da solo tramite CLI (es. `uv run python devtools/gui/release.py`). Usa blocchi `if __name__ == "__main__":` in fondo ai file.
2. **PATH RELATIVI AL PROGETTO:** Gli script non devono mai dipendere dalla current working directory (CWD) in modo ingenuo. Usa sempre `pathlib.Path(__file__).parent` per risolvere percorsi assoluti in modo dinamico e sicuro, partendo sempre dalla ROOT del progetto.
3. **PULIZIA:** Gli script di build o manutenzione NON devono inquinare la ROOT (`ISAB_TimeSheet/`). File temporanei, report, log ed eseguibili intermedi devono essere generati dentro `.cache/`, `scratch/`, `build/` o `dist/`.
4. **INTEGRAZIONE CONTINUA:** Prevedi sempre flag CLI non-interattivi (es. `--no-confirm`, `--ci`) in modo che gli script possano girare senza bloccare l'esecuzione in GitHub Actions.
5. **LOGGING:** Dato che questi script girano da terminale, produci output visivi chiari per lo sviluppatore o per i log CI, usando colori base, prefissi chiari (`[INFO]`, `[ERROR]`) o sfruttando `loguru`.
