#!/usr/bin/env python
"""Generatore dinamico del file .ai-context.json per SyncroJob.

Legge la versione corrente direttamente da ``src/application/services/version.py`` (via AST, senza
import del package completo) e costruisce un file ``.ai-context.json`` nella root del
progetto con il contesto architetturale completo dell'applicazione.

Questo file viene utilizzato dagli assistenti IA (Gemini, Copilot, ecc.) per:
- Comprendere la struttura del progetto in < 300 token.
- Evitare allucinazioni su nomi di tabelle, moduli e protocolli.
- Rispettare le regole architetturali codificate nelle direttive.

Il generatore è eseguito automaticamente ad ogni commit dal pre-commit hook
``generate-ai-context`` quando uno dei file chiave dell'architettura viene modificato.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

# ── Configurazione Percorsi ───────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent.parent
VERSION_FILE = ROOT / "src" / "application" / "services" / "version.py"
OUTPUT_FILE = ROOT / "docs" / "resources" / ".ai-context.json"


def _read_version_from_ast(path: Path) -> str:
    """Legge ``__version__`` da ``version.py`` tramite AST senza import del package.

    Args:
        path: Percorso assoluto al file ``version.py``.

    Returns:
        La stringa della versione (es. ``"1.49.0"``).

    Raises:
        RuntimeError: Se ``__version__`` non viene trovato nel file.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "__version__"
            and isinstance(node.value, ast.Constant)
        ):
            return str(node.value.value)
    msg = f"__version__ non trovato in {path}"
    raise RuntimeError(msg)


def _build_context(version: str) -> dict:  # type: ignore[type-arg]
    """Costruisce il dizionario completo del contesto IA.

    Args:
        version: La versione corrente dell'applicazione letta da ``version.py``.

    Returns:
        Dizionario strutturato pronto per la serializzazione JSON.
    """
    return {
        "$schema": "./docs/schemas/ai-context.schema.json",
        "$generated_by": "devtools/cli/generate_ai_context.py",
        "$note": "File generato automaticamente. NON modificare manualmente.",
        # ── Metadati del Progetto ─────────────────────────────────────────────
        "project": "SyncroJob Enterprise (ISAB_TimeSheet)",
        "version": version,
        "entry_point": "main.py",
        "python_version": ">=3.12,<3.13",
        "architectural_style": "Layered Architecture (Domain, Application, Infrastructure)",
        # ── Struttura Principale ──────────────────────────────────────────────
        "source_layout": {
            "src/domain/": "Business logic pura e modelli Pydantic",
            "src/application/services/": "Orchestrazione e servizi core (ex core/)",
            "src/infrastructure/": "Implementazioni tecniche (Bots, DB, Utils, Network)",
            "src/gui/": "Interfaccia PySide6 — NESSUNA logica di business",
            "src/api/": "Interfacce esterne e Bridge (Telegram)",
            "devtools/": "Toolchain di sviluppo (GUI, CLI, Maintenance)",
            "tests/": "Suite pytest (unit, gui, integration, slow)",
        },
        # ── Singleton e Contratti Formali ────────────────────────────────────
        "core_singletons": {
            "settings": "src/application/services/devtools/devtools/config/settings.py:settings  # SyncroJobSettings Pydantic",
        },
        "core_interfaces": {
            "BotProtocol": "src/application/services/interfaces.py",
            "DataImporterProtocol": "src/application/services/interfaces.py",
        },
        # ── Catalogo Bot ──────────────────────────────────────────────────────
        "bots": {
            "base_classes": {
                "SeleniumBaseBot": "src/infrastructure/bots/base/selenium_base_bot.py",
                "PlaywrightBaseBot": "src/infrastructure/bots/base/playwright_base_bot.py",
            },
            "portale_fornitori": {
                "CaricoTSBot": "src/infrastructure/bots/portale_fornitori/carico_ts/",
                "ScaricoTSBot": "src/infrastructure/bots/portale_fornitori/scarico_ts/",
                "DettagliOdABot": "src/infrastructure/bots/portale_fornitori/dettagli_oda/",
                "PrenotaBPBot": "src/infrastructure/bots/portale_fornitori/prenota_bp/",
                "TimbratureBot": "src/infrastructure/bots/portale_fornitori/timbrature/",
            },
            "safework": {
                "SafeWorkPDLSearchBot": "src/infrastructure/bots/safework/pdl/",
                "SafeWorkProgrammazioneBot": "src/infrastructure/bots/safework/programmazione/",
                "SafeWorkProgrammazioneSyncBot": "src/infrastructure/bots/safework/programmazione_sync/",
            },
            "rule": "Tutti i bot DEVONO conformarsi a BotProtocol (src/application/services/interfaces.py).",
        },
        # ── Database SQLite ───────────────────────────────────────────────────
        "databases": {
            "contabilita.db": {
                "purpose": "Strumentali, certificati e dati contabili ISAB",
                "key_tables": ["strumentali", "certificati_campione"],
            },
            "timbrature_Isab.db": {
                "purpose": "Timbrature giornaliere dei dipendenti scaricate dal portale",
                "key_tables": ["timbrature", "giornaliere"],
            },
            "pdl.db": {
                "purpose": "Piano di Lavoro (PDL) da SafeWork",
                "schema": "id INTEGER PRIMARY KEY, area TEXT, unita TEXT, codice_pdl TEXT, stato TEXT, data_assegnazione TEXT",
            },
            "storico_oda.db": {
                "purpose": "Ordini di Acquisto (OdA) scaricati dal portale fornitori",
                "schema": "id INTEGER PRIMARY KEY, fornitore TEXT, numero_oda TEXT, data_ordine TEXT, importo REAL, stato TEXT",
            },
            "anagrafica_dipendenti.db": {
                "purpose": "Anagrafica dipendenti e matricole",
                "schema": "id INTEGER PRIMARY KEY, matricola TEXT, nome TEXT, cognome TEXT, codice_fiscale TEXT, attivo INTEGER",
            },
            "scarico_ore.db": {
                "purpose": "Scarico ore da DataEase (sistema ERP)",
                "key_tables": ["ore_lavorate"],
            },
            "audit_log.db": {
                "purpose": "Log di audit delle operazioni critiche (immutabile)",
                "key_tables": ["audit_events"],
            },
        },
        # ── Gerarchia Eccezioni ───────────────────────────────────────────────
        "exception_hierarchy": {
            "SyncroJobError": {
                "module": "src/application/services/exceptions.py",
                "subclasses": {
                    "StartupError": "Errore durante l'avvio dell'applicazione",
                    "LicenseError": "Problemi relativi alla licenza",
                    "DatabaseError": "Errori nelle operazioni sul database",
                    "ConfigError": "Errori di configurazione o percorsi",
                    "ValidationError": "Errori di validazione dei dati",
                    "BotError": {
                        "desc": "Base per errori dei bot",
                        "subclasses": {
                            "BrowserInitError": "Fallimento inizializzazione browser",
                            "AutomationError": "Errore durante Selenium/Playwright",
                        },
                    },
                },
            }
        },
        # ── Standard UI ───────────────────────────────────────────────────────
        "ui_standards": {
            "buttons": "src/gui/widgets/modern_button.py:ModernButton  # SEMPRE questo, mai QPushButton nudo",
            "cards": "src/gui/widgets/modern_card.py:ModernCard",
            "dialogs_confirm": "src/gui/widgets/core_widgets.py:ConfirmationDialog  # SOSTITUISCE QMessageBox",
            "dialogs_input": "src/gui/widgets/core_widgets.py:StandardInputDialog  # SOSTITUISCE QInputDialog",
            "theme": "src/gui/styles/theme_manager.py:ThemeManager  # palette HSL dark/light coordinata",
            "toast": "src/gui/toast.py:ToastNotification",
        },
        # ── Comandi di Sviluppo ───────────────────────────────────────────────────
        "development_commands": {
            "run": "poetry run syncrojob",
            "lint": "poetry run ruff check --fix",
            "format": "poetry run ruff format",
            "type_check": "poetry run mypy --strict src/",
            "docstring_check": "poetry run interrogate src/",
            "complexity_check": "poetry run xenon src/ --max-absolute B --max-modules B --max-average A",
            "cohesion_check": "poetry run python devtools/maintenance/check_cohesion.py",
            "quality_check_all": "poetry run python devtools/maintenance/quality_check.py",
            "pre_commit": "poetry run pre-commit run --all-files",
            "generate_schemas": "poetry run python devtools/cli/generate_schemas.py",
            "generate_ai_context": "poetry run python devtools/cli/generate_ai_context.py",
            "generate_ci_context": "poetry run python devtools/cli/generate_ci_context.py",
            "generate_architecture": "poetry run python devtools/cli/generate_architecture.py",
            "tests": "python -m tests.run_robust_test",
            "tests_fast": "python -m tests.run_robust_test -m 'unit and not slow'",
            "tests_robust": "python -m tests.run_robust_test",
            "bump_version": "poetry run cz bump",
        },
        # ── Regole Anti-Breakage (MANDATORIE) ────────────────────────────────
        "anti_breakage_rules": [
            "SIGNAL SAFETY: Non rimuovere mai le `lambda` dalle connessioni dei segnali PySide6 (previene FURB111 ma rompe Qt).",
            "LOGGING: Usa esclusivamente `loguru`. Implementa `@logger.catch` su tutti gli entry point critici.",
            "SRP: Zero logica di business, query SQL o accesso al DB all'interno di src/gui/.",
            "SETTINGS: Usa sempre il Singleton `from src.application.services.config.settings import settings`. MAI istanziare SyncroJobSettings direttamente.",
            "DIALOGS: Usa ConfirmationDialog (non QMessageBox) e StandardInputDialog (non QInputDialog) ovunque.",
            "VERSIONING: La versione è gestita da commitizen. Esegui `cz bump`, non modificare manualmente pyproject.toml o version.py.",
            "TYPING: MyPy --strict. Zero `Any` non documentati. Usa `typing.Protocol` per i contratti tra moduli.",
            "ENCODING: UTF-8 obbligatorio su tutti i file aperti (open(..., encoding='utf-8')).",
        ],
        # ── Direttive di Qualità Statica ──────────────────────────────────────
        "quality_gates": {
            "ruff": "zero errori (linter + formatter)",
            "mypy": "--strict, zero errori",
            "interrogate": "copertura docstring >= 99%",
            "xenon": "Complessità CC massima B, media A",
            "cohesion": "LCOM < 40% per moduli core (vedi devtools/maintenance/check_cohesion.py)",
        },
        # ── Portali Esterni ───────────────────────────────────────────────────
        "external_portals": {
            "portale_fornitori": "https://portalefornitori.isab.com/Ui/",
            "safework": "https://safework.isab.com/",
            "update_url": "https://projectjob-bot.netlify.app/version.json",
        },
    }


def main() -> None:
    """Genera il file ``.ai-context.json`` nella root del progetto."""
    print("[INFO] Generazione .ai-context.json...")

    try:
        version = _read_version_from_ast(VERSION_FILE)
    except (OSError, RuntimeError) as e:
        print(f"[ERROR] Impossibile leggere la versione: {e}", file=sys.stderr)
        sys.exit(1)

    context = _build_context(version)

    try:
        OUTPUT_FILE.write_text(
            json.dumps(context, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"[OK] .ai-context.json aggiornato -> versione {version}")
        sys.exit(0)
    except OSError as e:
        print(f"[ERROR] Scrittura fallita: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
