"""SyncroJob - Pydantic Configuration Model.

Definisce lo schema formale e fortemente tipizzato delle configurazioni di SyncroJob.
Integra pydantic-settings per la validazione automatica a runtime, l'override
nativo da variabili d'ambiente (12-Factor App) e la documentazione semantica per l'IA.
"""

from typing import Any, Final

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.paths import CONFIG_FILE


class RoiWeightsModel(BaseModel):
    """Modello per la definizione dei pesi del ROI relativi alle singole automazioni."""

    scarico_ts: float = Field(alias="Scarico TS", default=5.0)
    carico_ts: float = Field(alias="Carico TS", default=8.0)
    dettagli_oda: float = Field(alias="Dettagli ODA", default=3.0)
    prenota_bp: float = Field(alias="Prenota BP", default=10.0)
    scarico_pdl: float = Field(alias="Scarico PDL", default=12.0)
    ricerca_pdl: float = Field(alias="Ricerca PDL", default=2.0)
    sincronizzazione: float = Field(alias="Sincronizzazione", default=1.0)
    export_excel: float = Field(alias="Export Excel", default=5.0)


class SyncroJobSettings(BaseSettings):
    """Schema di configurazione centralizzato e tipizzato per SyncroJob.

    Supporta il caricamento da file JSON e l'override tramite variabili d'ambiente
    con prefisso 'SYNCROJOB_'.
    """

    model_config = SettingsConfigDict(
        env_prefix="SYNCROJOB_",
        json_file=str(CONFIG_FILE),
        json_file_encoding="utf-8",
        extra="ignore",
    )

    # Account e Portali
    accounts: list[dict[str, Any]] = Field(default=[], description="Elenco account Portale Fornitori")
    safework_accounts: list[dict[str, Any]] = Field(default=[], description="Elenco account SafeWork")
    contracts: list[str] = Field(default=[], description="Contratti attivi")
    default_contract: str = Field(default="", description="Contratto di default")

    # Browser ed Automazione
    automation_engine: str = Field(
        default="selenium", description="Motore di automazione (selenium|playwright)"
    )
    browser_headless: bool = Field(default=False, description="Esecuzione del browser in modalità nascosta")
    browser_timeout: int = Field(default=300, description="Timeout del browser in secondi")
    download_path: str = Field(default="", description="Percorso di scarico per i file timesheet ed Excel")

    # Stato del Lavoro
    fornitori: list[str] = Field(default=[], description="Elenco dei fornitori attivi")
    last_ts_date: str = Field(default="01.01.2026", description="Data dell'ultimo timesheet scaricato")
    last_ts_fornitore: str = Field(default="", description="Fornitore dell'ultimo timesheet scaricato")

    # Contabilità Strumentale
    contabilita_file_path: str = Field(default="", description="Percorso del file Excel di contabilità")
    enable_auto_update_contabilita: bool = Field(
        default=True, description="Aggiornamento automatico della contabilità"
    )
    certificati_campione_path: str = Field(default="", description="Percorso cartella certificati campione")
    master_preventivi_path: str = Field(default="", description="Percorso file master dei preventivi")
    base_network_path_preventivi: str = Field(default="", description="Percorso di rete preventivi")

    # Preventivi
    preventivi_tcl: list[str] = Field(default=[], description="Elenco tecnici TCL autorizzati")
    preventivi_stati: list[str] = Field(default=[], description="Stati ammessi per i preventivi")
    reparti: list[str] = Field(
        default=["STRUMENTALE", "ELETTRICO", "CANTIERE", "ANALISI"], description="Reparti operativi"
    )
    cantieri: list[str] = Field(default=[], description="Elenco dei cantieri attivi")

    # UI & Widget
    quick_actions: list[str] = Field(
        default=["nav_scarico_ts", "cmd_sync", "cmd_open_folder"], description="Azioni rapide in dashboard"
    )
    roi_weights: dict[str, float] = Field(default={}, description="Pesi di calcolo ROI per ciascun bot")

    # Autopilot Certificati
    certificati_autopilot_enabled: bool = Field(
        default=False, description="Autopilota invio certificati attivo"
    )
    certificati_autopilot_time: str = Field(default="08:30", description="Orario giornaliero autopilot")
    certificati_autopilot_interval_days: int = Field(default=1, description="Intervallo di giorni autopilot")

    # Varie
    weather_show_details: bool = Field(default=False, description="Dettagli meteo avanzati in dashboard")


# Istanza Singleton pre-caricata in memoria a runtime (thread-safe, performante e AI-First)
settings: Final[SyncroJobSettings] = SyncroJobSettings()


def get_typed_settings() -> SyncroJobSettings:
    """Restituisce l'istanza Singleton pre-caricata delle impostazioni.

    Garantisce retrocompatibilità totale con i moduli esistenti ottimizzando
    istantaneamente le performance di I/O (caricamento singolo).

    Returns:
        SyncroJobSettings: Istanza fortemente tipizzata e validata delle impostazioni.
    """
    return settings
