"""
Bot TS - Log Humanizer
Converte messaggi di log tecnici in frasi umane e colloquiali.
"""
import random

class SmartLogTranslator:
    """Traduce i log tecnici in frasi 'umane'."""

    # Dizionario di template per categoria
    TEMPLATES = {
        "start": [
            "🚀 Si parte! Avvio i motori...",
            "👋 Ciao! Iniziamo subito a lavorare.",
            "🤖 Bot pronto. Andiamo!",
            "⚡ Iniziamo l'automazione."
        ],
        "login": [
            "🔐 Sto effettuando l'accesso al portale...",
            "👤 Inserisco le credenziali...",
            "🔑 Busso alla porta di ISAB...",
            "🚪 Apro le porte del sistema."
        ],
        "search": [
            "🔍 Cerco i dati richiesti...",
            "🕵️ Mi metto alla ricerca...",
            "🔎 Analizzo il database...",
            "🧐 Vediamo cosa trovo..."
        ],
        "download": [
            "📥 Scarico i file...",
            "💾 Salvo tutto sul disco...",
            "📦 Pacchetto in arrivo...",
            "📨 Recupero i documenti."
        ],
        "success": [
            "✅ Fatto! Tutto perfetto.",
            "🎉 Missione compiuta!",
            "✨ Ottimo lavoro, ho finito.",
            "🏆 Completato con successo."
        ],
        "error": [
            "❌ Oops, qualcosa è andato storto.",
            "⚠️ Ho incontrato un ostacolo.",
            "🚫 C'è un problema tecnico.",
            "🤕 Ahi, errore imprevisto."
        ],
        "wait": [
            "⏳ Attendo un attimo...",
            "☕ Pausa caffè virtuale...",
            "🕒 Dammi un secondo...",
            "✋ Aspetto che il sito risponda..."
        ]
    }

    @staticmethod
    def humanize(message: str) -> tuple[str, str, str]:
        """
        Analizza il messaggio tecnico e restituisce (human_msg, tech_msg, category).
        """
        lower_msg = message.lower()
        category = "info"
        human_msg = message # Default fall-back

        if "avvio" in lower_msg or "start" in lower_msg:
            category = "start"
        elif "login" in lower_msg or "accesso" in lower_msg or "connessione" in lower_msg:
            category = "login"
        elif "cerca" in lower_msg or "trovat" in lower_msg or "analizz" in lower_msg:
            category = "search"
        elif "scaric" in lower_msg or "salvat" in lower_msg or "export" in lower_msg:
            category = "download"
        elif "successo" in lower_msg or "completat" in lower_msg or "✓" in message:
            category = "success"
        elif "errore" in lower_msg or "fallit" in lower_msg or "exception" in lower_msg or "✗" in message:
            category = "error"
        elif "attes" in lower_msg or "wait" in lower_msg:
            category = "wait"

        if category in SmartLogTranslator.TEMPLATES:
            human_msg = random.choice(SmartLogTranslator.TEMPLATES[category])

        return human_msg, message, category
