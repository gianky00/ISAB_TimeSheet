# 🧠 INFRASTRUCTURE LAYER - AI ARCHITECT GUIDELINES

Sei all'interno di `src/infrastructure/`, il braccio operativo che parla con il mondo esterno (Database, Rete, API, Browser Automation).

## 🚨 REGOLE DEL LAYER (STRICT)
1. **DIPENDENZA VERSO L'INTERNO:** Questo layer implementa i `Protocol` definiti in `src/domain`. Nessun altro layer deve dipendere dalle implementazioni specifiche scritte qui.
2. **BOTS E AUTOMAZIONE WEB (`infrastructure/bots`):**
   - **Zero Hardcoding:** Timeout, URL e credenziali devono provenire dall'Application Layer o dalle configurazioni.
   - **Sicurezza:** NON LOGGARE MAI password, token o dati PII estratti dalle pagine. Usa log oscurati.
   - **Resilienza:** Ogni interazione di rete o del browser deve avere retry (es. `Tenacity`) e fallback chiari.
3. **DATABASE (`infrastructure/database`):**
   - Parametrizza sempre le query SQL per prevenire injection (`?` o `:name`).
   - Usa rigorosamente i context manager (`with conn:`) per evitare lock del database SQLite.
4. **RETE E API (`infrastructure/api` o `network`):**
   - Applica sempre un Timeout globale alle chiamate HTTP.
   - Gestisci i Rate-Limit usando ritardi esponenziali.
