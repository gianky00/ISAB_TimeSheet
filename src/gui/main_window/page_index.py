"""
SyncroJob - Page Index
Definizione degli indici numerici associati a ciascun pannello funzionale dell'applicazione.
Utilizzato dal NavigationController per la gestione del QStackedWidget della finestra principale.
"""

from enum import IntEnum


class PageIndex(IntEnum):
    """
    Enumerazione che mappa i nomi dei pannelli ai rispettivi indici nel container della GUI.
    Garantisce la coerenza nel routing tra i vari controller e i componenti dell'interfaccia.
    """

    DASHBOARD = 0
    """Dashboard principale con riepilogo e autopilot."""

    AUTOMAZIONI = 1
    """Pannello di controllo per l'avvio manuale dei bot."""

    RESERVED_AI = 2
    """Indice riservato (precedentemente Lyra)."""

    TIMBRATURE = 3
    """Gestione scarico timbrature portale fornitori."""

    STRUMENTALE = 4
    """Pannello contabilità strumentale e KPI."""

    DATAEASE = 5
    """Visualizzatore avanzato Scarico Ore Cantiere."""

    ANAGRAFICHE = 6
    """Gestione anagrafiche e directory aziendale."""

    SETTINGS = 7
    """Configurazione globale dell'applicazione."""

    HELP = 8
    """Manuale utente e documentazione integrata."""

    NOTIFICATIONS = 9
    """Centro notifiche e cronologia messaggi."""

    STORICO_ODA = 10
    """Consultazione e ricerca ordini di acquisto."""

    DIPENDENTI = 11
    """Gestione schede dipendenti e monitoraggio PDL."""

    CONSUNTIVO = 12
    """Generatore e gestore consuntivi automatizzato."""
