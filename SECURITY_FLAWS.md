# 🚨 Analisi Criticità di Sicurezza (SyncroJob)

Questo documento riassume le falle individuate durante l'audit SAST del sistema di licenze e automazione.

## 1. Esposizione Segreti (GitHub PAT)
- **File:** `src/core/license_updater.py`
- **Descrizione:** Il token GitHub per l'accesso al repository licenze è ricostruito da una lista di interi statica. È vulnerabile a decompilazione/reverse engineering.
- **Impatto:** Accesso totale al cloud delle licenze di tutti i clienti.

## 2. Chiave Cifratura Hardcoded (Grace Period)
- **File:** `src/core/license_updater.py`
- **Descrizione:** `GRACE_PERIOD_KEY` è cablata nel codice.
- **Impatto:** Un utente può manipolare il file `validity.token` locale per estendere infinitamente il periodo di grazia offline.

## 3. UI Injection (RichText Dialogs)
- **File:** `src/gui/dialogs/confirmation_dialog.py`
- **Descrizione:** Uso di `setTextFormat(Qt.TextFormat.RichText)` su messaggi non sanificati.
- **Impatto:** Possibilità di visualizzare contenuti ingannevoli o eseguire script (XSS) se l'errore proviene da una fonte esterna manipolata.

## 4. Stored XSS nei Log Bot
- **File:** `src/bots/base/base_bot.py`
- **Descrizione:** Salvataggio del `page_source` grezzo in file `.html` locali in caso di errore.
- **Impatto:** Se un sito web target è malevolo, può iniettare script che verranno eseguiti quando lo sviluppatore apre il file di log nel browser.
