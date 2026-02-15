import os
import sys
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import QObject, Qt, QUrl
from PyQt6.QtGui import QDesktopServices, QKeySequence, QShortcut

from src.core.config_manager import get_data_path, get_logs_path
from src.core.constants import Icons
from src.gui.controllers.command_registry import CommandNode
from src.gui.dialogs.bug_report_dialog import BugReportDialog
from src.gui.dialogs.command_palette import CommandPaletteDialog


class MenuBarComponent(QObject):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.command_palette = None
        self._last_palette_toggle: float = 0
        self._bug_dialog = None
        self._setup_shortcuts()

    def open_bug_report_dialog(self):
        """Apre il dialogo per la segnalazione di bug."""
        try:
            self._bug_dialog = BugReportDialog(self.main_window)
            self._bug_dialog.show()
        except Exception as e:
            print(f"Error opening bug report dialog: {e}")
            if hasattr(self.main_window, "show_toast"):
                self.main_window.show_toast(f"Errore apertura segnalazione: {e}", "error")

    def _setup_shortcuts(self):
        # Shortcut per Command Palette (Spotlight)
        self.shortcut_palette = QShortcut(QKeySequence("Ctrl+K"), self.main_window)
        self.shortcut_palette.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_palette.activated.connect(self.open_command_palette)

        # Fallback Shortcut (Ctrl+Shift+P) per conflitti
        self.shortcut_palette_sec = QShortcut(QKeySequence("Ctrl+Shift+P"), self.main_window)
        self.shortcut_palette_sec.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_palette_sec.activated.connect(self.open_command_palette)

        # Fallback Shortcut (F1)
        self.shortcut_palette_f1 = QShortcut(QKeySequence("F1"), self.main_window)
        self.shortcut_palette_f1.setContext(Qt.ShortcutContext.ApplicationShortcut)
        self.shortcut_palette_f1.activated.connect(self.open_command_palette)

    def open_command_palette(self):
        """Apre o chiude la Command Palette (Spotlight) con animazione e debouncing."""
        now = datetime.now().timestamp() * 1000
        if (now - self._last_palette_toggle) < 300:
            return
        self._last_palette_toggle = now

        if self.command_palette is None:
            self._init_palette()

        if self.command_palette and self.command_palette.isVisible():
            self.command_palette.hide_animated()
        elif self.command_palette:
            self.command_palette.show_animated()
            # Optional: Toast per confermare l'apertura se in debug mode, ma meglio evitare spam

    def _init_palette(self):
        try:
            root_nodes = self._build_menu_tree()
            self.command_palette = CommandPaletteDialog(self.main_window, root_nodes)
        except Exception as e:
            import traceback

            print(f"CRITICAL ERROR initializing Command Palette: {e}")
            traceback.print_exc()
            if hasattr(self.main_window, "show_toast"):
                self.main_window.show_toast(f"Error opening palette: {e}")

    def _build_menu_tree(self):
        # Helper helpers
        def restart_app():
            from PyQt6.QtWidgets import QApplication

            QApplication.quit()
            os.execl(sys.executable, sys.executable, *sys.argv)  # noqa: S606

        def open_folder_path(path):
            if Path(path).exists():
                QDesktopServices.openUrl(QUrl.fromLocalFile(path))

        mw = self.main_window

        # We assume mw has methods like _navigate_to, _run_timbrature_bot etc.
        # This preserves the Facade pattern for now.

        # 1. ESEGUI (Execution Flow)
        menu_run = CommandNode(
            "Esegui...",
            "Avvia bot e task automatici",
            Icons.PLAY,
            children=[
                # --- Timbrature ---
                CommandNode(
                    "Scarica Timbrature",
                    "Portale Fornitori: Presenze",
                    Icons.CLOCK,
                    children=[
                        CommandNode(
                            "Oggi",
                            "Scarica solo oggi",
                            Icons.CALENDAR,
                            action=lambda: mw._run_timbrature_bot("oggi"),
                        ),
                        CommandNode(
                            "Ieri",
                            "Scarica giornata di ieri",
                            Icons.CLOCK,
                            action=lambda: mw._run_timbrature_bot("ieri"),
                        ),
                        CommandNode(
                            "Mese Corrente",
                            "Dal 1° del mese ad oggi",
                            Icons.CALENDAR,
                            action=lambda: mw._run_timbrature_bot("mese"),
                        ),
                    ],
                ),
                # --- Scarico TS ---
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
                            on_input_complete=mw._on_scarico_ts_input,
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
                # --- Other commands (simplified for brevity, keeping critical ones) ---
                CommandNode(
                    "Dettagli OdA",
                    "Portale Fornitori: Dettagli Ordini",
                    Icons.LIST,
                    input_prompts=["Inserisci Numero OdA"],
                    on_input_complete=mw._on_dettagli_oda_input,
                ),
                CommandNode(
                    "Prenota BP",
                    "Portale Fornitori: Prenotazione Badge",
                    Icons.TICKET,
                    input_prompts=["Inserisci Numero BP"],
                    on_input_complete=mw._on_prenota_bp_input,
                ),
                CommandNode(
                    "Carico TS",
                    "Portale Fornitori: Upload Timesheets",
                    Icons.UPLOAD,
                    action=mw._run_carico_ts,
                ),
                CommandNode(
                    "Scarico PDL",
                    "SafeWork: Download Permessi",
                    Icons.SHIELD,
                    input_prompts=["Inserisci Numero PDL"],
                    on_input_complete=mw._on_pdl_input,
                ),
                CommandNode(
                    "Sincronizza DataEase",
                    "Scarico ore e quadrature",
                    Icons.DATABASE,
                    action=mw._run_sync_dataease,
                ),
                CommandNode(
                    "Sincronizza Strumentale",
                    "Aggiorna Contabilità e OdA",
                    Icons.FOLDER,
                    action=mw._run_sync_strumentale,
                ),
            ],
        )

        from src.gui.main_window.page_index import PageIndex  # We will create this

        # 2. GO (Navigation Flow)
        menu_go = CommandNode(
            "Vai a...",
            "Navigazione rapida pannelli",
            Icons.GLOBE,
            children=[
                CommandNode(
                    "Dashboard",
                    "KPI e Stato",
                    Icons.ACTIVITY,
                    action=lambda: mw._navigate_to(PageIndex.DASHBOARD),
                ),
                CommandNode(
                    "Notifiche & Audit",
                    "Log sistema",
                    Icons.BELL,
                    action=lambda: mw._navigate_to(PageIndex.NOTIFICATIONS),
                ),
                CommandNode(
                    "Timbrature",
                    "Gestione Presenze",
                    Icons.CLOCK,
                    action=lambda: mw._navigate_to(PageIndex.TIMBRATURE),
                ),
                CommandNode(
                    "Strumentale",
                    "Contabilità & OdA",
                    Icons.FOLDER,
                    action=lambda: mw._navigate_to(PageIndex.STRUMENTALE),
                ),
                CommandNode(
                    "DataEase",
                    "Importazione Dati",
                    Icons.DATABASE,
                    action=lambda: mw._navigate_to(PageIndex.DATAEASE),
                ),  # Added
                CommandNode(
                    "Dipendenti",
                    "Anagrafica Risorse",
                    Icons.USERS,
                    action=lambda: mw._navigate_to(PageIndex.DIPENDENTI),
                ),
                CommandNode(
                    "Storico OdA",
                    "Database Ordini",
                    Icons.ARCHIVE,
                    action=lambda: mw._navigate_to(PageIndex.STORICO_ODA),
                ),
                CommandNode(
                    "Impostazioni",
                    "Configurazione",
                    Icons.SETTINGS_DARK,
                    action=lambda: mw._navigate_to(PageIndex.SETTINGS),
                ),
                CommandNode(
                    "Automazioni",
                    "Scheduler",
                    Icons.SMART_TOY,
                    action=lambda: mw._navigate_to(PageIndex.AUTOMAZIONI),
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
                        CommandNode(
                            "Riavvia Applicazione",
                            "Soft Reboot",
                            Icons.REFRESH,
                            action=restart_app,
                        ),
                        CommandNode(
                            "Toggle Stats",
                            "Mostra telemetria",
                            Icons.TERMINAL,
                            action=mw._toggle_footer_stats,
                            close_on_execute=False,
                        ),
                        CommandNode(
                            "Aggiorna Dati (F5)",
                            "Refresh view",
                            Icons.REFRESH,
                            action=mw._handle_f5,
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
                    action=lambda: mw._navigate_to(PageIndex.HELP),
                ),
                CommandNode(
                    "Segnala Bug",
                    "Invia Report con Outlook",
                    Icons.ALERT_TRIANGLE,
                    action=self.open_bug_report_dialog,
                ),
            ],
        )

        return [
            menu_run,
            menu_go,
            menu_help,
            # Shortcuts
            CommandNode(
                "Vai a Timbrature",
                "Nav",
                Icons.CLOCK,
                shortcut="Alt+2",
                action=lambda: mw._navigate_to(PageIndex.TIMBRATURE),
            ),
            CommandNode(
                "Vai a Strumentale",
                "Nav",
                Icons.FOLDER,
                shortcut="Alt+3",
                action=lambda: mw._navigate_to(PageIndex.STRUMENTALE),
            ),
            CommandNode(
                "Vai a DataEase",
                "Nav",
                Icons.DATABASE,
                shortcut="Alt+4",
                action=lambda: mw._navigate_to(PageIndex.DATAEASE),
            ),
            menu_set,
            CommandNode(
                "Esci",
                "Chiudi applicazione",
                Icons.LOG_OUT,
                action=mw._quit_application,
            ),
        ]
