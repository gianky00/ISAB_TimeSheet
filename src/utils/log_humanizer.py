"""
SyncroJob - Log Humanizer
Converte messaggi di log tecnici in frasi pulite e professionali.
Rimosso il sistema casuale per garantire coerenza e precisione.
"""

from datetime import UTC, datetime
from typing import ClassVar


def friendly_time_delta(dt: datetime) -> str:
    """Restituisce una stringa amichevole per il delta temporale (es. '5 min fa')."""
    if dt.tzinfo is None:
        dt = dt.astimezone()
    now = datetime.now(UTC).astimezone()
    diff = now - dt

    if diff.days > 0:
        return dt.strftime("%d/%m")

    seconds = diff.total_seconds()
    seconds_in_minute = 60
    seconds_in_hour = 3600

    if seconds < seconds_in_minute:
        return "Adesso"
    if seconds < seconds_in_hour:
        minutes = int(seconds / seconds_in_minute)
        return f"{minutes} min fa"
    hours = int(seconds / seconds_in_hour)
    return f"{hours}h fa"


class SmartLogTranslator:
    """Traduce i log tecnici in frasi pulite e categorizzate per la UI."""

    # Mappatura diretta per messaggi comuni (per garantire coerenza)
    FIXED_MAPPING: ClassVar[dict[str, str]] = {
        "avvio automazione": "[AVVIO] Avvio automazione in corso...",
        "inizializzazione browser": "🌐 Inizializzazione browser...",
        "inserimento credenziali": "🔐 Inserimento credenziali...",
        "attendo un attimo": "[ATTESA] Attesa operativa...",
        "aspetto che il sito risponda": "[ATTESA] In attesa di risposta dal server...",
        "spinner scomparso": "[OK] Caricamento completato.",
        "dashboard raggiunta correttamente": "[OK] Accesso al sistema completato.",
        "recupero i documenti": "[FILE] Recupero documenti in corso...",
        "mi metto alla ricerca": "[CERCA] Ricerca in corso...",
        "analizzo il database": "[CERCA] Analisi dati in corso...",
        "scarico i file": "[DOWNLOAD] Scarico file in corso...",
        "missione compiuta": "[INFO] Missione completata con successo!",
        "completato con successo": "[OK] Operazione conclusa.",
        "fatto! tutto perfetto": "[OK] Operazione conclusa.",
        "errore critico": "[ERRORE] Errore critico rilevato!",
    }

    @staticmethod
    def humanize(message: str) -> tuple[str, str, str]:
        """Analizza il messaggio tecnico e restituisce (human_msg, tech_msg, category)."""
        category = SmartLogTranslator._detect_category(message)

        # Se il messaggio ha già un'icona o un prefisso speciale, lo teniamo così come è
        # (es. "[CLICK] Click su", "[FILE] Verifica")
        if any(
            message.startswith(icon)
            for icon in (
                "[CLICK]",
                "[FILE]",
                "[CERCA]",
                "[ATTESA]",
                "[OK]",
                "[ERRORE]",
                "[ATTENZIONE]",
                "[AVVIO]",
                "[INFO]",
                "[DOWNLOAD]",
                "[LINK]",
                "[INPUT]",
                "[SYNC]",
                "[INFO]",
            )
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
        category = "info"

        # Priorità a categorie specifiche di business
        if any(kw in lower_msg for kw in ("scaric", "download", "[download]")):
            category = "download"
        elif any(
            kw in lower_msg
            for kw in (
                "errore",
                "fallit",
                "falliment",
                "fail",
                "exception",
                "eccezion",
                "critico",
                "[errore]",
            )
        ):
            category = "error"
        elif any(kw in lower_msg for kw in ("successo", "completat", "compiut", "fatto", "[ok]", "[info]")):
            category = "success"
        elif any(kw in lower_msg for kw in ("click", "premuto", "selezion", "[click]")):
            category = "action"
        elif any(kw in lower_msg for kw in ("ricerca", "cerca", "[cerca]")):
            category = "search"
        elif any(
            kw in lower_msg for kw in ("attesa", "attendi", "aspetto", "polling", "caricamento", "[attesa]")
        ):
            category = "wait"

        return category
