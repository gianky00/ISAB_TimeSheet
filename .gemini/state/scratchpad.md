# 🧠 AI Session Scratchpad
*Questo file è la memoria a breve termine dell'Intelligenza Artificiale.*
*Git lo ignorerà grazie al `.gitignore`, quindi non esiterà mai su GitHub.*

## 📋 Task Correnti
- [x] Correggere exit code del test runner custom.
- [x] Sistemare la logica del CI context generator.
- [x] Configurare file di Overrides locali (`gemini.toml`).
- [ ] Attendere prossime direttive dell'Architetto Umano.

## 📝 Appunti Architetturali Recenti
- È stato deciso di mantenere il test runner modulare custom.
- La CI pipeline fallirà se c'è un exit code 1 da `run_robust_test`.
- MyPy e Ruff sono stati spostati anche nel `pre-commit` locale.
