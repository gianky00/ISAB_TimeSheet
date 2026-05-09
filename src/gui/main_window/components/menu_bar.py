# mypy: disable-error-code="no-untyped-def, no-untyped-call, arg-type, attr-defined, misc, no-redef"
"""
SyncroJob - Menu Bar Component
Componente responsabile della gestione delle scorciatoie globali e della Command Palette.
Implementa il sistema di navigazione gerarchica 'Spotlight' per l'accesso rapido a tutte le funzioni.
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Qt, QUrl
from PySide6.QtGui import QDesktopServices, QKeySequence, QShortcut

from src.core.constants import Icons
from src.core.paths import get_data_path, get_logs_path
from src.gui.controllers.command_registry import CommandNode
from src.gui.dialogs.bug_report_dialog import BugReportDialog
from src.gui.dialogs.command_palette import CommandPaletteDialog

if TYPE_CHECKING:
    from src.gui.main_window.main import MainWindow


class MenuBarComponent(QObject):
    """
    Gestisce l'interazione con i comandi globali tramite tastiera e interfaccia Spotlight.
    Coordina l'inizializzazione della Command Palette e la costruzione dell'albero dei comandi.
    """

    def __init__(self, main_window: MainWindow) -> None:
        """
        Inizializza il componente menu e registra le scorciatoie.

        Args:
          main_window: Riferimento alla MainWindow dell'applicazione.
        """
        super().__init__(main_window)
        self.main_window = main_window
        self.command_palette: CommandPaletteDialog | None = None
        self._last_palette_toggle: float = 0
        self._bug_dialog: BugReportDialog | None = None

        # Shortcuts
        self.shortcut_palette: QShortcut
        self.shortcut_palette_sec: QShortcut
        self.shortcut_palette_f1: QShortcut

        self._setup_shortcuts()

    def open_bug_report_dialog(self) -> None:
        """Visualizza il dialogo avanzato per la segnalazione di problemi tecnici."""
        try:
            self._bug_dialog = BugReportDialog(self.main_window)
            self._bug_dialog.show()
        except Exception as e:
            print(f"Error opening bug report dialog: {e}")
            if hasattr(self.main_window, "show_toast"):
                self.main_window.show_toast(f"Errore apertura segnalazione: {e}", "error")

    def _setup_shortcuts(self) -> None:
        """Configura le scorciatoie da tastiera (Ctrl+K, F1, Ctrl+Shift+P) per la Command Palette."""
        self.shortcut_palette = QShortcut(QKeySequence("Ctrl+K"), self.main_window)
        self.shortcut_palette.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_palette.activated.connect(self.open_command_palette)

        self.shortcut_palette_sec = QShortcut(QKeySequence("Ctrl+Shift+P"), self.main_window)
        self.shortcut_palette_sec.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_palette_sec.activated.connect(self.open_command_palette)

        self.shortcut_palette_f1 = QShortcut(QKeySequence("F1"), self.main_window)
        self.shortcut_palette_f1.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_palette_f1.activated.connect(self.open_command_palette)

    def open_command_palette(self) -> None:
        """Apre o chiude la Command Palette con effetto a tendina e controllo anti-rimbalzo."""
        now = datetime.now(UTC).timestamp() * 1000
        if (now - self._last_palette_toggle) < 300:  # noqa: PLR2004
            return
        self._last_palette_toggle = now

        if self.command_palette is None:
            self._init_palette()

        if self.command_palette and self.command_palette.isVisible():
            self.command_palette.hide_animated()
        elif self.command_palette:
            self.command_palette.show_animated()

    def _init_palette(self) -> None:
        """Inizializza l'istanza del dialogo Command Palette costruendo l'albero dei comandi."""
        try:
            root_nodes = self._build_menu_tree()
            if not root_nodes:
                if hasattr(self.main_window, "show_toast"):
                    self.main_window.show_toast("Errore: l'albero dei comandi  vuoto", "error")
                return

            self.command_palette = CommandPaletteDialog(self.main_window, root_nodes)
        except Exception as e:
            import traceback  # noqa: PLC0415

            print(f"Error initializing palette: {e}")
            traceback.print_exc()

            # Feedback visivo critico per l'utente
            if hasattr(self.main_window, "show_toast"):
                self.main_window.show_toast(f"Errore critico Palette: {e}", "error")

            # Reset per riprovare al prossimo clic
            self.command_palette = None

    def _build_menu_tree(self) -> list[CommandNode]:
        """
        Costruisce dinamicamente la struttura gerarchica dei comandi disponibili nell'applicazione.
        Definisce azioni per esecuzione bot, navigazione pagine e manutenzione sistema.

        Returns:
          list[CommandNode]: Lista dei nodi comando radice.
        """

        def restart_app() -> None:
            import subprocess  # noqa: PLC0415

            from PySide6.QtWidgets import QApplication  # noqa: PLC0415

            QApplication.quit()
            subprocess.Popen([sys.executable, *sys.argv])
            sys.exit()

        def open_folder_path(path: str | Path) -> None:
            if Path(path).exists():
                QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

        mw = self.main_window
        wc = mw.workflow_controller

        # 1. ESEGUI (Execution Flow)
        menu_run = CommandNode(
            "Esegui...",
            "Avvia bot e task automatici",
            Icons.PLAY,
            children=[
                CommandNode(
                    "Scarica Timbrature",
                    "Portale Fornitori: Presenze",
                    Icons.CLOCK,
                    children=[
                        CommandNode(
                            "Oggi",
                            "Scarica solo oggi",
                            Icons.CALENDAR,
                            action=lambda: wc.run_timbrature_bot("oggi"),
                        ),
                        CommandNode(
                            "Ieri",
                            "Scarica giornata di ieri",
                            Icons.CLOCK,
                            action=lambda: wc.run_timbrature_bot("ieri"),
                        ),
                        CommandNode(
                            "Mese Corrente",
                            "Dal 1  del mese ad oggi",
                            Icons.CALENDAR,
                            action=lambda: wc.run_timbrature_bot("mese"),
                        ),
                    ],
                ),
                CommandNode(
                    "Scarico TS",
                    "Portale Fornitori: Download Timesheets",
                    Icons.DOWNLOAD,
                    children=[
                        CommandNode(
                            "Scarica singola OdA",
                            "Inserisci numero OdA manualmente",
                            Icons.EDIT,
                            input_prompts=["Inserisci Numero OdA"],
                            on_input_complete=wc.handle_scarico_ts_input,
                        ),
                        CommandNode(
                            "Esegui lista pannello",
                            "Processa le righe salvate nel pannello",
                            Icons.PLAY,
                            action=lambda: (
                                mw.scarico_panel.run_externally({}) if hasattr(mw, "scarico_panel") else None
                            ),
                        ),
                    ],
                ),
                CommandNode(
                    "Dettagli OdA",
                    "Portale Fornitori",
                    Icons.LIST,
                    input_prompts=["Inserisci Numero OdA"],
                    on_input_complete=wc.handle_dettagli_oda_input,
                ),
                CommandNode(
                    "Prenota BP",
                    "Portale Fornitori",
                    Icons.TICKET,
                    input_prompts=["Inserisci Numero BP"],
                    on_input_complete=wc.handle_prenota_bp_input,
                ),
                CommandNode("Carico TS", "Portale Fornitori", Icons.UPLOAD, action=wc.run_carico_ts),
                CommandNode(
                    "Scarico PDL",
                    "SafeWork",
                    Icons.SHIELD,
                    input_prompts=["Inserisci Numero PDL"],
                    on_input_complete=wc.handle_pdl_input,
                ),
            ],
        )

        from src.gui.main_window.page_index import PageIndex  # noqa: PLC0415

        # 2. GO (Navigation Flow)
        menu_go = CommandNode(
            "Vai a...",
            "Navigazione rapida pannelli",
            Icons.GLOBE,
            children=[
                CommandNode(
                    "Dashboard",
                    "KPiu'e Stato",
                    Icons.ACTIVITY,
                    action=lambda: mw.navigation_controller.navigate_to(PageIndex.DASHBOARD),
                ),
                CommandNode(
                    "Notifiche & Audit",
                    "Log sistema",
                    Icons.BELL,
                    action=lambda: mw.navigation_controller.navigate_to(PageIndex.NOTIFICATIONS),
                ),
                CommandNode(
                    "Timbrature",
                    "Gestione Presenze",
                    Icons.CLOCK,
                    action=lambda: mw.navigation_controller.navigate_to(PageIndex.TIMBRATURE),
                ),
                CommandNode(
                    "Strumentale",
                    "Contabilit  & OdA",
                    Icons.FOLDER,
                    action=lambda: mw.navigation_controller.navigate_to(PageIndex.STRUMENTALE),
                ),
                CommandNode(
                    "DataEase",
                    "Importazione Dati",
                    Icons.DATABASE,
                    action=lambda: mw.navigation_controller.navigate_to(PageIndex.DATAEASE),
                ),
                CommandNode(
                    "Dipendenti",
                    "Anagrafica Risorse",
                    Icons.USERS,
                    action=lambda: mw.navigation_controller.navigate_to(PageIndex.DIPENDENTI),
                ),
                CommandNode(
                    "Storico OdA",
                    "Database Ordini",
                    Icons.ARCHIVE,
                    action=lambda: mw.navigation_controller.navigate_to(PageIndex.STORICO_ODA),
                ),
                CommandNode(
                    "Impostazioni",
                    "Configurazione",
                    Icons.SETTINGS_DARK,
                    action=lambda: mw.navigation_controller.navigate_to(PageIndex.SETTINGS),
                ),
                CommandNode(
                    "Automazioni",
                    "Scheduler",
                    Icons.SMART_TOY,
                    action=lambda: mw.navigation_controller.navigate_to(PageIndex.AUTOMAZIONI),
                ),
            ],
        )

        # 3. SET (Settings)
        menu_set = CommandNode(
            "Sistema...",
            "Strumenti tecnici e opzioni",
            Icons.TERMINAL,
            children=[
                CommandNode(
                    "Cartelle",
                    children=[
                        CommandNode(
                            "Dati Applicazione",
                            "Apri cartella config",
                            Icons.FOLDER_OPEN,
                            action=lambda: open_folder_path(get_data_path()),
                        ),
                        CommandNode(
                            "Log Files",
                            "Apri cartella log",
                            Icons.FILE_TEXT,
                            action=lambda: open_folder_path(get_logs_path()),
                        ),
                    ],
                ),
                CommandNode(
                    "Manutenzione",
                    children=[
                        CommandNode("Riavvia Applicazione", "Soft Reboot", Icons.REFRESH, action=restart_app),
                        CommandNode(
                            "Toggle Stats",
                            "Mostra telemetria",
                            Icons.TERMINAL,
                            action=mw.status_bar_component._toggle_footer_stats,
                            close_on_execute=False,
                        ),
                        CommandNode(
                            "Aggiorna Dati (F5)",
                            "Refresh view",
                            Icons.REFRESH,
                            action=mw.app_event_handler.handle_f5,
                        ),
                    ],
                ),
            ],
        )

        menu_help = CommandNode(
            "Help...",
            "Supporto",
            Icons.HELP,
            children=[
                CommandNode(
                    "Guida utente",
                    "Manuale operativo",
                    Icons.HELP,
                    action=lambda: mw.navigation_controller.navigate_to(PageIndex.HELP),
                ),
                CommandNode(
                    "Segnala Bug",
                    "Invia Report con Outlook",
                    Icons.ALERT_TRIANGLE,
                    action=self.open_bug_report_dialog,
                ),
            ],
        )

        try:
            return [
                menu_run,
                menu_go,
                menu_help,
                CommandNode(
                    "Vai a Timbrature",
                    "Nav",
                    Icons.CLOCK,
                    shortcut="Alt+2",
                    action=lambda: mw.navigation_controller.navigate_to(PageIndex.TIMBRATURE),
                ),
                CommandNode(
                    "Vai a Strumentale",
                    "Nav",
                    Icons.FOLDER,
                    shortcut="Alt+3",
                    action=lambda: mw.navigation_controller.navigate_to(PageIndex.STRUMENTALE),
                ),
                CommandNode(
                    "Vai a DataEase",
                    "Nav",
                    Icons.DATABASE,
                    shortcut="Alt+4",
                    action=lambda: mw.navigation_controller.navigate_to(PageIndex.DATAEASE),
                ),
                menu_set,
                CommandNode(
                    "Esci", "Chiudi applicazione", Icons.LOG_OUT, action=mw.app_event_handler.quit_application
                ),
            ]
        except Exception as e:
            print(f"Error building menu tree: {e}")
            return []
