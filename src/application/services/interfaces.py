#!/usr/bin/env python
"""SyncroJob - AI-First Architectural Interfaces and Protocols.

Questo modulo definisce i contratti formali e fortemente tipizzati (typing.Protocol)
delle principali componenti dell'applicazione (Bot, Importer, Services).
Queste interfacce consentono un disaccoppiamento ottimale, abilitano il mocking
nativo per i test e forniscono un contesto logico immediato e privo di allucinazioni
per le IA nella programmazione del codice.
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class BotProtocol(Protocol):
    """Contratto formale rigido per tutti i Bot di automazione del portale.

    Ogni bot implementato nel sistema (Selenium o Playwright) deve conformarsi
    a questa interfaccia per garantire la compatibilità con il motore di esecuzione
    e la GUI asincrona.
    """

    def run(self, *args: Any, **kwargs: Any) -> bool:
        """Avvia la procedura di automazione del bot.

        Args:
            *args (Any): Argomenti posizionali flessibili per l'inizializzazione del bot.
            **kwargs (Any): Argomenti nominali flessibili per l'inizializzazione del bot.

        Returns:
            bool: True se l'esecuzione è completata con successo, False altrimenti.
        """
        ...

    def force_stop(self) -> None:
        """Arresta immediatamente ed in modo sicuro l'esecuzione del bot."""
        ...

    def cleanup(self) -> None:
        """Pulisce le risorse occupate dal bot (chiusura driver, file temporanei)."""
        ...


@runtime_checkable
class DataImporterProtocol(Protocol):
    """Contratto formale per tutti gli importatori di dati (Excel, CSV, PDF, Web).

    Ogni importatore nel sistema si occupa di tradurre un preciso tracciato record
    di input in structures dati tipizzate (Modelli o DTO).
    """

    def import_file(self, file_path: str, *args: Any, **kwargs: Any) -> Any:
        """Importa e processa un file di dati dal percorso specificato.

        Args:
            file_path (str): Il percorso assoluto del file da importare.
            *args (Any): Argomenti posizionali aggiuntivi per il parsing.
            **kwargs (Any): Argomenti nominali aggiuntivi per il parsing.

        Returns:
            Any: I dati importati e normalizzati (lista di record o DTO).
        """
        ...
