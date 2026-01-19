"""
SyncroJob - Log Humanizer
Converte messaggi di log tecnici in frasi umane e colloquiali.
"""

import random
from datetime import datetime


def friendly_time_delta(dt):
    """Restituisce una stringa amichevole per il delta temporale (es. '5 min fa')."""
    now = datetime.now()
    diff = now - dt

    if diff.days > 0:
        return dt.strftime("%d/%m")

    seconds = diff.total_seconds()
    if seconds < 60:
        return "Adesso"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} min fa"
    else:
        hours = int(seconds / 3600)
        return f"{hours}h fa"


class SmartLogTranslator:
    """Traduce i log tecnici in frasi 'umane'."""

    # Dizionario di template per categoria
    TEMPLATES = {
        "start": [
            "Si parte! Avvio i motori...",
            "Ciao! Iniziamo subito a lavorare.",
            "Bot pronto. Andiamo!",
            "Iniziamo l'automazione.",
        ],
        "login": [
            "Sto effettuando l'accesso al portale...",
            "Inserisco le credenziali...",
            "Busso alla porta di ISAB...",
            "Apro le porte del sistema.",
        ],
        "search": [
            "Cerco i dati richiesti...",
            "Mi metto alla ricerca...",
            "Analizzo il database...",
            "Vediamo cosa trovo...",
        ],
        "download": [
            "Scarico i file...",
            "Salvo tutto sul disco...",
            "Pacchetto in arrivo...",
            "Recupero i documenti.",
        ],
        "success": [
            "Fatto! Tutto perfetto.",
            "Missione compiuta!",
            "Ottimo lavoro, ho finito.",
            "Completato con successo.",
        ],
        "error": [
            "Oops, qualcosa è andato storto.",
            "Ho incontrato un ostacolo.",
            "C'è un problema tecnico.",
            "Ahi, errore imprevisto.",
        ],
        "wait": [
            "Attendo un attimo...",
            "Pausa caffè virtuale...",
            "Dammi un secondo...",
            "Aspetto che il sito risponda...",
        ],
    }

    @staticmethod
    def humanize(message: str) -> tuple[str, str, str]:
        """Analizza il messaggio tecnico e restituisce (human_msg, tech_msg, category)."""
        category = SmartLogTranslator._detect_category(message)

        if category in SmartLogTranslator.TEMPLATES:
            human_msg = random.choice(SmartLogTranslator.TEMPLATES[category])
        else:
            human_msg = message

        tech_msg = SmartLogTranslator._inject_tags(message, category)
        return human_msg, tech_msg, category

    @staticmethod
    def _detect_category(message: str) -> str:
        """Determina la categoria del messaggio basandosi sulle keyword."""
        lower_msg = message.lower()
        mappings = {
            "error": ["errore", "fallit", "exception", "eccezion", "✗"],
            "start": ["avvio", "start"],
            "login": ["login", "accesso", "connessione"],
            "search": ["cerca", "trovat", "analizz"],
            "download": ["scaric", "salvat", "export"],
            "success": ["successo", "completat", "✓"],
            "wait": ["attes", "wait"],
        }

        for cat, keywords in mappings.items():
            if any(kw in lower_msg for kw in keywords):
                return cat
            # Check case-sensitive icons for success/error
            if cat in ["error", "success"] and any(
                kw in message for kw in ["✗", "✓"] if kw in keywords
            ):
                return cat
        return "info"

    @staticmethod
    def _inject_tags(message: str, category: str) -> str:
        """Inietta tag tecnici per suggerire azioni alla UI."""
        lower_msg = message.lower()
        if "credenziali" in lower_msg or (category == "error" and "login" in lower_msg):
            return f"{message} [FIXIT:ACCOUNT]"
        return message
