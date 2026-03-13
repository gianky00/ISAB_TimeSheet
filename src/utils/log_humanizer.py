"""
SyncroJob - Log Humanizer
Converte messaggi di log tecnici in frasi pulite e professionali.
Rimosso il sistema casuale per garantire coerenza e precisione.
"""

from datetime import datetime
from typing import ClassVar


def friendly_time_delta(dt: datetime) -> str:
    """Restituisce una stringa amichevole per il delta temporale (es. '5 min fa')."""
    now = datetime.now()
    diff = now - dt

    if diff.days > 0:
        return dt.strftime("%d/%m")

    seconds = diff.total_seconds()
    if seconds < 60:
        return "Adesso"
    if seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} min fa"
    hours = int(seconds / 3600)
    return f"{hours}h fa"


class SmartLogTranslator:
    """Traduce i log tecnici in frasi pulite e categorizzate per la UI."""

    # Mappatura diretta per messaggi comuni (per garantire coerenza)
    FIXED_MAPPING: ClassVar[dict[str, str]] = {
        "avvio automazione": "🚀 Avvio automazione in corso...",
        "inizializzazione browser": "🌐 Inizializzazione browser...",
        "inserimento credenziali": "🔐 Inserimento credenziali...",
        "attendo un attimo": "⏳ Attesa operativa...",
        "aspetto che il sito risponda": "⏳ In attesa di risposta dal server...",
        "spinner scomparso": "✅ Caricamento completato.",
        "dashboard raggiunta correttamente": "✅ Accesso al sistema completato.",
        "recupero i documenti": "📂 Recupero documenti in corso...",
        "mi metto alla ricerca": "🔍 Ricerca in corso...",
        "analizzo il database": "🔍 Analisi dati in corso...",
        "scarico i file": "⬇️ Scarico file in corso...",
        "missione compiuta": "✨ Missione completata con successo!",
        "completato con successo": "✅ Operazione conclusa.",
        "fatto! tutto perfetto": "✅ Operazione conclusa.",
        "errore critico": "❌ Errore critico rilevato!",
    }

    @staticmethod
    def humanize(message: str) -> tuple[str, str, str]:
        """Analizza il messaggio tecnico e restituisce (human_msg, tech_msg, category)."""
        category = SmartLogTranslator._detect_category(message)

        # Se il messaggio ha già un'icona o un prefisso speciale, lo teniamo così come è
        # (es. "🖱️ Click su", "📂 Verifica")
        if any(
            message.startswith(icon)
            for icon in ("🖱️", "📂", "🔍", "⏳", "✅", "❌", "⚠️", "🚀", "✨", "⬇️", "🔗", "⌨️", "🔄", "ℹ️")
        ):
            human_msg = message
        else:
            # Altrimenti cerchiamo una mappatura fissa o puliamo il testo
            msg_lower = message.lower().strip().rstrip(".")
            human_msg = SmartLogTranslator.FIXED_MAPPING.get(msg_lower, message)

        return human_msg, message, category

    @staticmethod
    def _detect_category(message: str) -> str:
        """Determina la categoria del messaggio basandosi sulle keyword."""
        lower_msg = message.lower()

        # Priorità a categorie specifiche di business
        if any(kw in lower_msg for kw in ("scaric", "download", "⬇️")):
            return "download"

        if any(
            kw in lower_msg
            for kw in ("errore", "fallit", "falliment", "fail", "exception", "eccezion", "critico", "❌")
        ):
            return "error"

        if any(kw in lower_msg for kw in ("successo", "completat", "compiut", "fatto", "✅", "✨")):
            return "success"

        if any(kw in lower_msg for kw in ("click", "premuto", "selezion", "🖱️")):
            return "action"

        if any(kw in lower_msg for kw in ("ricerca", "cerca", "🔍")):
            return "search"

        # Categorie speciali per animazioni o colori
        if any(kw in lower_msg for kw in ("attesa", "attendi", "aspetto", "polling", "caricamento", "⏳")):
            return "wait"

        return "info"
