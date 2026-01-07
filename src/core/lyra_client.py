"""
Lyra AI Client
Gestisce l'interazione con l'intelligenza artificiale (Google Gemini).
"""
import requests
import sqlite3
import json
from pathlib import Path
from src.core.contabilita_manager import ContabilitaManager
from src.core.config_manager import CONFIG_DIR
from src.core.audit_manager import AuditManager

class LyraClient:
    """Client per interagire con l'API di Google Gemini (Lyra)."""

    def __init__(self, api_key: str, model_name: str = None):
        if not api_key:
            raise ValueError("API Key for Gemini is required.")
        self._api_key = api_key
        
        # Carica modello preferito esclusivamente da config se non specificato
        from src.core import config_manager
        config = config_manager.load_config()
        self.model = model_name or config.get("ai_model", "gemini-1.5-pro")
        
        # Nessun fallback: usa solo il modello scelto
        self.models = [self.model]

        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.url = f"{self.base_url}/{self.model}:generateContent?key={self._api_key}"

        self.context_prompt = """
        Sei Lyra, un motore di estrazione dati ultra-professionale basato su Gemini.
        La tua missione è la digitalizzazione integrale dei Rapportini Giornalieri ISAB.

        REGOLE MANDATORIE PER ESTRAZIONE (PDF/IMMAGINI):
        1. SOLO LA TABELLA: Se l'utente chiede di estrarre o analizzare un documento, restituisci ESCLUSIVAMENTE la tabella Markdown. 
        2. NO INTRODUZIONE: Non scrivere mai "Ecco i dati", "Analisi completata" o titoli. Inizia direttamente con la riga intestazione | SC | TS | ...
        3. NO CONCLUSIONE: Non aggiungere commenti, sintesi o segnalazione anomalie a meno che non venga chiesto esplicitamente.
        4. COMPLETEZZA TOTALE: Estrai OGNI singola riga. Se nel foglio vedi 6 persone o 6 righe di attività, DEVI riportare 6 righe. Non saltare nessuno.
        5. PRECISIONE CHIRURGICA:
           - Colonne: SC, TS, FG, PE, Personale, Descrizione Attività, TCL, ODC, N° PDL, Inizio, Fine, Ore.
           - Mantieni i nomi e i codici (es. 5400 canone) esattamente come scritti.

        Per domande non legate ai documenti, rispondi in modo tecnico e conciso.
        """

    def list_models(self) -> list[str]:
        """Recupera la lista di modelli che supportano 'generateContent'."""
        try:
            url = f"{self.base_url}?key={self._api_key}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                models = response.json().get("models", [])
                # Filtra per i modelli che sono effettivamente utilizzabili per la chat/analisi
                compatible_models = [
                    m.get("name").replace("models/", "") 
                    for m in models 
                    if "generateContent" in m.get("supportedGenerationMethods", [])
                ]
                return compatible_models
            return []
        except Exception:
            return []


    def _get_system_context(self) -> str:
        """Raccoglie i dati dai database locali per il contesto AI."""
        context = []

        # --- 1. Contabilità Strumentale ---
        try:
            years = ContabilitaManager.get_available_years()
            if years:
                latest_year = max(years)
                stats = ContabilitaManager.get_year_stats(latest_year)

                # Calcoli derivati
                margine = stats['total_prev'] - (stats['total_ore'] * 30.0) # Costo std 30
                marginalita = (margine / stats['total_prev'] * 100) if stats['total_prev'] > 0 else 0

                context.append(f"=== REPORT CONTABILITÀ ({latest_year}) ===")
                context.append(f"- Valore Totale Preventivato: € {stats['total_prev']:,.2f}")
                context.append(f"- Ore Spese Totali: {stats['total_ore']:,.1f} h")
                context.append(f"- Margine Operativo Stimato (vs Costo €30/h): € {margine:,.2f} ({marginalita:.1f}%)")
                context.append(f"- Totale Commesse: {stats['count_total']}")

                context.append("- Stato Avanzamento:")
                for status, count in stats.get('status_counts', {}).items():
                    if count > 0:
                        context.append(f"  • {status}: {count}")

                context.append("- Top 5 Commesse (per Valore):")
                for name, val in stats.get('top_commesse', []):
                    # Tronca nomi troppo lunghi
                    short_name = (name[:35] + '..') if len(name) > 35 else name
                    context.append(f"  • {short_name}: € {val:,.0f}")
            else:
                context.append("=== CONTABILITÀ ===\nNessun dato disponibile.")
        except Exception as e:
            context.append(f"Errore lettura Contabilità: {e}")

        # --- 2. Timbrature ---
        try:
            db_path = CONFIG_DIR / "data" / "timbrature_Isab.db"
            if db_path.exists():
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()

                # Totali
                cursor.execute("SELECT COUNT(*) FROM timbrature")
                total_count = cursor.fetchone()[0]

                # Ultime attività
                cursor.execute("SELECT data, nome, cognome, ingresso, uscita FROM timbrature ORDER BY data DESC, ingresso DESC LIMIT 5")
                last_entries = cursor.fetchall()

                # Anomalie (es. Uscita mancante negli ultimi 30gg)
                # Semplice check: se uscita è vuota o null e data < oggi
                cursor.execute("SELECT COUNT(*) FROM timbrature WHERE (uscita IS NULL OR uscita = '') AND data < date('now')")
                missing_out = cursor.fetchone()[0]

                conn.close()

                context.append(f"\n=== REPORT TIMBRATURE ===")
                context.append(f"- Record Totali: {total_count}")
                if missing_out > 0:
                    context.append(f"- ⚠️ ATTENZIONE: Rilevate {missing_out} timbrature con uscita mancante (anomalie).")
                else:
                    context.append("- Nessuna anomalia (uscite mancanti) rilevata.")

                context.append("- Ultime 5 Attività Registrate:")
                for entry in last_entries:
                    d, n, c, i, u = entry
                    u_str = u if u else "---"
                    context.append(f"  • {d}: {n} {c} ({i} -> {u_str})")
            else:
                context.append("\n=== TIMBRATURE ===\nDatabase non trovato.")
        except Exception as e:
            context.append(f"Errore lettura Timbrature: {e}")

        return "\n".join(context)

    def ask(self, question: str, extra_context: str = "", images: list = None) -> str:
        """Invia una domanda a Gemini con il contesto ed eventuali immagini."""
        try:
            system_data = self._get_system_context()

            ctx = ""
            if extra_context:
                ctx = f"\n\n[CONTESTO SPECIFICO FORNITO DALL'UTENTE (ANALIZZA QUESTO RECORD)]:\n{extra_context}\n"

            full_prompt = f"{self.context_prompt}\n{system_data}{ctx}\n\nUtente: {question}\nLyra:"

            # Costruzione parti del messaggio
            parts = [{"text": full_prompt}]
            
            if images:
                for img_b64 in images:
                    parts.append({
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": img_b64
                        }
                    })

            payload = {
                "contents": [{
                    "parts": parts
                }]
            }

            headers = {'Content-Type': 'application/json'}

            # Nessun loop di retry: usa solo il modello impostato
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self._api_key}"

            try:
                response = requests.post(url, json=payload, headers=headers, timeout=60)

                if response.status_code == 200:
                    result = response.json()
                    
                    # Audit Token Usage
                    usage = result.get('usageMetadata', {})
                    if usage:
                        AuditManager().log_action(
                            "Consumo Token AI", 
                            category="lyra", 
                            entity=self.model,
                            params={
                                "prompt": usage.get("promptTokenCount", 0),
                                "response": usage.get("candidatesTokenCount", 0),
                                "total": usage.get("totalTokenCount", 0)
                            }
                        )

                    try:
                        return result['candidates'][0]['content']['parts'][0]['text']
                    except (KeyError, IndexError):
                        return f"Errore elaborazione risposta AI: {json.dumps(result)}"
                else:
                    return f"Errore API {self.model} (Status {response.status_code}): {response.text}"

            except Exception as e:
                return f"Errore connessione AI ({self.model}): {str(e)}"

        except Exception as e:
            return f"Si è verificato un errore critico: {str(e)}"

    def analyze_media(self, media_bytes: bytes, prompt: str, mime_type: str = "image/png") -> str:
        """Invia un file multimediale (audio/immagine) a Gemini per analisi."""
        import base64
        media_b64 = base64.b64encode(media_bytes).decode('utf-8')
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": media_b64
                        }
                    }
                ]
            }]
        }
        
        headers = {'Content-Type': 'application/json'}
        
        # Usa il modello scelto dall'utente
        model = self.model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self._api_key}"
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                result = response.json()
                # Audit usage
                usage = result.get('usageMetadata', {})
                if usage:
                    AuditManager().log_action("Consumo Token Media AI", category="lyra", entity=model, params=usage)
                
                return result['candidates'][0]['content']['parts'][0]['text']
            return f"Errore API Media: {response.status_code}"
        except Exception as e:
            return f"Errore analisi media: {e}"
