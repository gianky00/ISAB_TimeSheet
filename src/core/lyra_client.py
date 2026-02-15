"""
Lyra AI Client
Gestisce l'interazione con l'intelligenza artificiale (Google Gemini o Ollama locale).
"""

import sqlite3
from typing import Any

import requests

from src.core import config_manager
from src.core.audit_manager import AuditManager
from src.core.config_manager import CONFIG_DIR
from src.core.contabilita_manager import ContabilitaManager


class LyraClient:
    """Client per interagire con l'AI (Gemini o Ollama)."""

    def __init__(
        self,
        api_key: str | None = None,
        model_name: str | None = None,
        provider: str | None = None,
        ollama_url: str | None = None,
    ):
        config = config_manager.load_config()
        self.provider = provider or config.get("ai_provider", "gemini")
        self._api_key = api_key

        # Validazione minima per Gemini
        if self.provider == "gemini" and not self._api_key:
            # Non solleviamo errore qui per permettere il listing se la chiave verrà passata dopo
            pass

        self.model = model_name or config.get("ai_model", "gemini-1.5-pro")
        self.ollama_url = ollama_url or config.get("ollama_url", "http://localhost:11434")

        # Prompt di sistema unificato
        self.context_prompt = """
        Sei Lyra, un motore di estrazione dati ultra-professionale.
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
        """Recupera la lista di modelli disponibili dal provider corrente."""
        if self.provider == "ollama":
            return self._list_ollama_models()
        return self._list_gemini_models()

    def _list_gemini_models(self) -> list[str]:
        """Recupera la lista di modelli Gemini."""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self._api_key}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                models = response.json().get("models", [])
                compatible_models = [
                    m.get("name").replace("models/", "")
                    for m in models
                    if "generateContent" in m.get("supportedGenerationMethods", [])
                ]
                return compatible_models
            return []
        except Exception:
            return []

    def _list_ollama_models(self) -> list[str]:
        """Recupera la lista di modelli installati su Ollama."""
        try:
            url = f"{self.ollama_url}/api/tags"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                models_data = response.json().get("models", [])
                return [m.get("name") for m in models_data]
            return []
        except Exception:
            return []

    def _get_system_context(self) -> str:
        """Raccoglie i dati dai database locali per il contesto AI."""
        context = [self._get_contabilita_context(), self._get_timbrature_context()]
        return "\n".join(context)

    def _get_contabilita_context(self) -> str:
        """Raccoglie dati contabilità per il contesto AI."""
        try:
            years = ContabilitaManager.get_available_years()
            if not years:
                return "=== CONTABILITÀ ===\nNessun dato disponibile."

            latest_year = max(years)
            stats = ContabilitaManager.get_year_stats(latest_year)
            margine = stats["total_prev"] - (stats["total_ore"] * 30.0)
            marginalita = (margine / stats["total_prev"] * 100) if stats["total_prev"] > 0 else 0

            lines = [
                f"=== REPORT CONTABILITÀ ({latest_year}) ===",
                f"- Valore Totale Preventivato: € {stats['total_prev']:,.2f}",
                f"- Ore Spese Totali: {stats['total_ore']:,.1f} h",
                f"- Margine Operativo Stimato (vs Costo €30/h): € {margine:,.2f} ({marginalita:.1f}%)",
                f"- Totale Commesse: {stats['count_total']}",
                "- Stato Avanzamento:",
            ]
            for status, count in stats.get("status_counts", {}).items():
                if count > 0:
                    lines.append(f"  • {status}: {count}")

            lines.append("- Top 5 Commesse (per Valore):")
            for name, val in stats.get("top_commesse", []):
                short_name = (name[:35] + "..") if len(name) > 35 else name
                lines.append(f"  • {short_name}: € {val:,.0f}")
            return "\n".join(lines)
        except Exception as e:
            return f"Errore lettura Contabilità: {e}"

    def _get_timbrature_context(self) -> str:
        """Raccoglie dati timbrature per il contesto AI."""
        try:
            db_path = CONFIG_DIR / "data" / "timbrature_Isab.db"
            if not db_path.exists():
                return "\n=== TIMBRATURE ===\nDatabase non trovato."

            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM timbrature")
                total_count = cursor.fetchone()[0]
                cursor.execute(
                    "SELECT data, nome, cognome, ingresso, uscita FROM timbrature ORDER BY data DESC, ingresso DESC LIMIT 5"
                )
                last_entries = cursor.fetchall()
                cursor.execute(
                    "SELECT COUNT(*) FROM timbrature WHERE (uscita IS NULL OR uscita = '') AND data < date('now')"
                )
                missing_out = cursor.fetchone()[0]

            lines = ["\n=== REPORT TIMBRATURE ===", f"- Record Totali: {total_count}"]
            if missing_out > 0:
                lines.append(f"- ⚠️ ATTENZIONE: Rilevate {missing_out} timbrature con uscita mancante.")
            else:
                lines.append("- Nessuna anomalia (uscite mancanti) rilevata.")

            lines.append("- Ultime 5 Attività Registrate:")
            for entry in last_entries:
                d, n, c, i, u = entry
                initials = f"{n[0]}. {c[0]}." if n and c else "N.D."
                lines.append(f"  • {d}: {initials} ({i} -> {u or '---'})")
            return "\n".join(lines)
        except Exception as e:
            return f"Errore lettura Timbrature: {e}"

    def ask(
        self,
        question: str,
        extra_context: str = "",
        images: list[Any] | None = None,
    ) -> str:
        """Invia una domanda al provider scelto."""
        if self.provider == "ollama":
            return self._ask_ollama(question, extra_context, images)
        return self._ask_gemini(question, extra_context, images)

    def _ask_gemini(
        self,
        question: str,
        extra_context: str = "",
        images: list[Any] | None = None,
    ) -> str:
        """Invia una domanda a Google Gemini."""
        try:
            system_data = self._get_system_context()
            ctx = (
                f"\n\n[CONTESTO SPECIFICO FORNITO DALL'UTENTE (ANALIZZA QUESTO RECORD)]:\n{extra_context}\n"
                if extra_context
                else ""
            )
            full_prompt = f"{self.context_prompt}\n{system_data}{ctx}\n\nUtente: {question}\nLyra:"

            parts: list[dict[str, Any]] = [{"text": full_prompt}]
            if images:
                parts.extend(
                    {"inline_data": {"mime_type": "image/png", "data": img_b64}} for img_b64 in images
                )

            payload = {"contents": [{"parts": parts}]}
            headers = {"Content-Type": "application/json"}
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self._api_key}"

            response = requests.post(url, json=payload, headers=headers, timeout=60)
            if response.status_code == 200:
                result = response.json()
                usage = result.get("usageMetadata", {})
                if usage:
                    AuditManager.instance().log_action(
                        "Consumo Token AI",
                        category="lyra",
                        entity=f"gemini:{self.model}",
                        params=usage,
                    )
                return str(result["candidates"][0]["content"]["parts"][0]["text"])
            return f"Errore API Gemini (Status {response.status_code}): {response.text}"
        except Exception as e:
            return f"Errore connessione Gemini ({self.model}): {e}"

    def _ask_ollama(
        self,
        question: str,
        extra_context: str = "",
        images: list[Any] | None = None,
    ) -> str:
        """Invia una domanda a Ollama locale usando l'endpoint chat."""
        try:
            system_data = self._get_system_context()
            ctx = (
                f"\n\n[CONTESTO SPECIFICO FORNITO DALL'UTENTE (ANALIZZA QUESTO RECORD)]:\n{extra_context}\n"
                if extra_context
                else ""
            )

            messages = [
                {"role": "system", "content": self.context_prompt},
                {"role": "system", "content": f"Dati di sistema attuali:\n{system_data}"},
            ]

            if ctx:
                messages.append({"role": "system", "content": ctx})

            user_msg = {"role": "user", "content": question}
            if images:
                user_msg["images"] = images

            messages.append(user_msg)

            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {"num_ctx": 4096},
            }

            url = f"{self.ollama_url}/api/chat"
            response = requests.post(url, json=payload, timeout=120)

            if response.status_code == 200:
                result = response.json()
                AuditManager.instance().log_action(
                    "Interazione AI Locale",
                    category="lyra",
                    entity=f"ollama:{self.model}",
                    params={"prompt_len": len(question)},
                )
                return str(result.get("message", {}).get("content", ""))

            # Gestione errori strutturata
            error_msg = f"Errore Ollama (Status {response.status_code})"
            try:
                error_json = response.json()
                if "error" in error_json:
                    error_msg += f": {error_json['error']}"
            except Exception:
                error_msg += f": {response.text[:200]}"
            return error_msg

        except requests.exceptions.ConnectionError:
            return f"Impossibile connettersi a Ollama su {self.ollama_url}. Assicurati che il servizio sia attivo."
        except Exception as e:
            return f"Errore connessione Ollama ({self.model}): {e}"

    def analyze_media(
        self,
        media_bytes: bytes,
        prompt: str,
        mime_type: str = "image/png",
    ) -> str:
        """Analisi media (principalmente via Gemini, Ollama supporta solo immagini)."""
        if self.provider == "ollama":
            import base64

            media_b64 = base64.b64encode(media_bytes).decode("utf-8")
            return self._ask_ollama(prompt, images=[media_b64])

        # Fallback Gemini
        import base64

        media_b64 = base64.b64encode(media_bytes).decode("utf-8")
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {"inline_data": {"mime_type": mime_type, "data": media_b64}},
                    ]
                }
            ]
        }
        headers = {"Content-Type": "application/json"}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self._api_key}"

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                return str(response.json()["candidates"][0]["content"]["parts"][0]["text"])
            return f"Errore API Media: {response.status_code}"
        except Exception as e:
            return f"Errore analisi media: {e}"
