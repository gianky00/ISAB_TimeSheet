"""
Lyra AI Client
Gestisce l'interazione con l'intelligenza artificiale (Google Gemini).
"""
import requests
import sqlite3
import json
from pathlib import Path
from src.core.contabilita_manager import ContabilitaManager

class LyraClient:
    def __init__(self):
        # Obfuscated API Key (Reconstructed at runtime)
        self._k_parts = [65, 73, 122, 97, 83, 121, 66, 83, 84, 66, 100, 95, 112, 87, 113, 111, 86, 49, 73, 106, 75, 83, 49, 88, 120, 48, 81, 119, 112, 75, 69, 68, 119, 54, 66, 70, 121, 98, 85]
        self._api_key = "".join([chr(c) for c in self._k_parts])
        self._url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self._api_key}"

        self.context_prompt = (
            "Sei Lyra, un'esperta contabile e assistente virtuale per l'applicazione 'Bot TS'. "
            "Il tuo obiettivo è analizzare i dati aziendali e fornire insight utili. "
            "Rispondi sempre in italiano, in modo professionale ma amichevole. "
            "Sii concisa."
            "Ecco i dati attuali del sistema (aggiornati in tempo reale):\n"
        )

    def _get_system_context(self) -> str:
        """Raccoglie i dati dai database locali."""
        context = []

        # 1. Contabilità
        try:
            years = ContabilitaManager.get_available_years()
            if years:
                latest_year = max(years)
                data = ContabilitaManager.get_data_by_year(latest_year)
                # Calcolo sommario veloce
                tot_prev = 0.0
                for row in data:
                    try:
                        # Colonna 3 è Totale Prev
                        if len(row) > 3 and row[3]:
                            val = float(str(row[3]).replace('.','').replace(',','.').replace('€','').strip())
                            tot_prev += val
                    except: pass

                context.append(f"- Contabilità {latest_year}: {len(data)} commesse registrate. Valore Totale Preventivato: € {tot_prev:,.2f}.")
            else:
                context.append("- Contabilità: Nessun dato disponibile.")
        except Exception as e:
            context.append(f"- Errore lettura Contabilità: {e}")

        # 2. Timbrature
        try:
            db_path = Path("data/timbrature_Isab.db")
            if db_path.exists():
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*), MAX(data) FROM timbrature")
                res = cursor.fetchone()
                if res:
                    count, last_date = res
                    context.append(f"- Timbrature: {count} record totali nel database. Ultima timbratura registrata il: {last_date}.")
                conn.close()
            else:
                context.append("- Timbrature: Database non trovato.")
        except Exception as e:
            context.append(f"- Errore lettura Timbrature: {e}")

        return "\n".join(context)

    def ask(self, question: str) -> str:
        """Invia una domanda a Gemini con il contesto."""
        try:
            system_data = self._get_system_context()
            full_prompt = f"{self.context_prompt}\n{system_data}\n\nUtente: {question}\nLyra:"

            payload = {
                "contents": [{
                    "parts": [{"text": full_prompt}]
                }]
            }

            headers = {'Content-Type': 'application/json'}
            response = requests.post(self._url, json=payload, headers=headers)

            if response.status_code == 200:
                result = response.json()
                try:
                    return result['candidates'][0]['content']['parts'][0]['text']
                except (KeyError, IndexError):
                    return "Non sono riuscita a elaborare la risposta. Riprova."
            else:
                return f"Errore API ({response.status_code}): {response.text}"

        except Exception as e:
            return f"Si è verificato un errore critico: {e}"
