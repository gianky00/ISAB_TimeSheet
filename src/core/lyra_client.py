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

class LyraClient:
    def __init__(self):
        # Obfuscated API Key (Reconstructed at runtime)
        self._k_parts = [65, 73, 122, 97, 83, 121, 66, 83, 84, 66, 100, 95, 112, 87, 113, 111, 86, 49, 73, 106, 75, 83, 49, 88, 120, 48, 81, 119, 112, 75, 69, 68, 119, 54, 66, 70, 121, 98, 85]
        self._api_key = "".join([chr(c) for c in self._k_parts])

        # Models to try in order of preference (Fallback strategy)
        self.models = [
            "models/gemini-2.0-flash",
            "models/gemini-2.0-flash-lite-preview-02-05",
            "models/gemini-flash-latest"
        ]

        self.context_prompt = (
            "Sei Lyra, un'esperta contabile executive per 'Bot TS'. "
            "NON presentarti mai (es. 'Sono Lyra', 'Ciao'). Vai dritta al punto con i dati. "
            "Usa SEMPRE tabelle Markdown (| Colonna 1 | Colonna 2 |) per presentare liste, numeri o confronti. "
            "Formatta i numeri in italiano (es. € 1.234,56). "
            "Rispondi in modo analitico, evidenziando proattivamente anomalie (es. margini negativi). "
            "DATI SISTEMA AGGIORNATI:\n"
        )

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

    def ask(self, question: str, extra_context: str = "") -> str:
        """Invia una domanda a Gemini con il contesto."""
        try:
            system_data = self._get_system_context()

            ctx = ""
            if extra_context:
                ctx = f"\n\n[CONTESTO SPECIFICO FORNITO DALL'UTENTE (ANALIZZA QUESTO RECORD)]:\n{extra_context}\n"

            full_prompt = f"{self.context_prompt}\n{system_data}{ctx}\n\nUtente: {question}\nLyra:"

            payload = {
                "contents": [{
                    "parts": [{"text": full_prompt}]
                }]
            }

            headers = {'Content-Type': 'application/json'}

            last_error = ""

            # Retry loop with different models
            for model in self.models:
                url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={self._api_key}"

                try:
                    response = requests.post(url, json=payload, headers=headers)

                    if response.status_code == 200:
                        result = response.json()
                        try:
                            return result['candidates'][0]['content']['parts'][0]['text']
                        except (KeyError, IndexError):
                            return "Non sono riuscita a elaborare la risposta. Riprova."
                    elif response.status_code == 429:
                        last_error = f"Quota esaurita per {model} (429)."
                        continue # Try next model
                    else:
                        last_error = f"Errore API {model} ({response.status_code}): {response.text}"
                        continue

                except Exception as e:
                    last_error = f"Errore connessione: {e}"
                    continue

            return f"Tutti i modelli AI hanno fallito. Ultimo errore: {last_error}"

        except Exception as e:
            return f"Si è verificato un errore critico: {e}"
