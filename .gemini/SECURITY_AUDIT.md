# SyncroJob - Security Audit & Vulnerability Report

Questo documento riassume le criticità rilevate e gli standard di sicurezza da mantenere.

## 🚨 Vulnerabilità Note (SAST Audit)

### 1. Esposizione GitHub PAT
- **Rischio**: Token GitHub ricostruito da lista statica in `license_updater.py`.
- **Azione**: Migrare a un sistema di backend intermediario per non esporre il token nel client.

### 2. Grace Period Manipulation
- **Rischio**: `GRACE_PERIOD_KEY` hardcoded.
- **Azione**: Spostare la validazione della data di scadenza lato server.

### 3. SQL Injection (Bandit B608)
- **Rischio**: Uso di f-strings in `src/core/database/pdl_queries.py` e migrazioni.
- **Standard**: Usare sempre query parametrizzate (`cursor.execute("SELECT... WHERE id=?", (val,))`).

---

## 🛡️ Standard di Sicurezza Enterprise

### 1. Gestione Credenziali
*   **MAI** salvare password in chiaro.
*   Usare `SecretsManager` per l'integrazione con il keyring di sistema.
*   Configurazioni sensibili (`.env`) devono essere nel `.gitignore`.

### 2. Sanitizzazione UI
*   Evitare `RichText` in dialoghi che mostrano input esterni non filtrati per prevenire UI Injection.

### 3. Integrità Dati
*   Utilizzare checksum per validare i file scaricati dai bot prima del processamento.
