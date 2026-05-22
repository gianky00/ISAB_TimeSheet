"""SyncroJob - Contabilità Panel.

Pannello centrale per la visualizzazione e l'analisi della Contabilità Strumentale.
Integra reportistica annuale, dati giornalieri, attività programmate e certificati campione.
Include un motore di ricerca unificato e l'accesso al pannello di analisi KPI.
"""

from __future__ import annotations

import logging
import warnings
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from PySide6.QtGui import QShowEvent

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.constants import Icons
from src.core.contabilita_manager import ContabilitaManager
from src.core.contabilita_worker import ContabilitaWorker
from src.gui.components.animated_tab_widget import AnimatedTabWidget
from src.gui.controllers.contabilita_controller import ContabilitaController
from src.gui.dialogs.confirmation_dialog import ConfirmationDialog
from src.gui.panels.contabilita_kpi import ContabilitaKPIPanel
from src.gui.styles import COLORS, LABEL_MUTED, LINEEDIT_STYLE
from src.gui.widgets.contabilita.attivita_tab import AttivitaProgrammateTab
from src.gui.widgets.contabilita.certificati_tab import CertificatiCampioneTab
from src.gui.widgets.contabilita.giornaliere_tab import GiornaliereYearTab
from src.gui.widgets.contabilita.stats_helper import ContabilitaStatsHelper
from src.gui.widgets.contabilita.year_tab import ContabilitaYearTab
from src.gui.widgets.core_widgets import (
    SearchInput,
)
from src.gui.widgets.modern_button import ModernButton
from src.gui.widgets.modern_card import ModernCard
from src.utils.helpers import get_asset_path, get_colored_icon

logger = logging.getLogger(__name__)


class ContabilitaPanel(QWidget):
    """Pannello principale dell'interfaccia di contabilità.

    Organizza i dati complessi in tab logici e fornisce strumenti per:
    - Ricerca rapida tra migliaia di record.
    - Calcolo dinamico dei totali ore su selezione utente.
    - Sincronizzazione background con file Excel esterni.
    - Visualizzazione grafica dei KPI.

    Inizializza il pannello e avvia il caricamento lazy dei dati.

    Args:
      parent: Widget genitore opzionale.

    Attributes:
        SECONDS_IN_MINUTE: Final[int: Segnale o attributo della classe.
    """

    SECONDS_IN_MINUTE: Final[int] = 60

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.controller = ContabilitaController(self)
        self.status_labels: list[QLabel] = []
        self.update_buttons: list[ModernButton] = []

        # UI Elements
        self.toolbar_card: ModernCard
        self.selection_count_label: QLabel
        self.selection_sum_label: QLabel
        self.search_input: SearchInput
        self.status_lbl: QLabel
        self.update_btn: ModernButton
        self.main_tabs: AnimatedTabWidget
        self.year_tabs_widget: AnimatedTabWidget
        self.giornaliere_tabs_widget: AnimatedTabWidget
        self.attivita_widget: AttivitaProgrammateTab
        self.certificati_widget: CertificatiCampioneTab
        self.kpi_panel: ContabilitaKPIPanel
        self.worker: ContabilitaWorker | None = None

        self._first_refresh_done = False
        self._setup_ui()
        self._connect_controller()

    def _connect_controller(self) -> None:
        """Collega i segnali del controller alla UI."""
        self.controller.status_updated.connect(self.status_lbl.setText)
        self.controller.import_finished.connect(self._on_import_finished_from_controller)
        self.controller.data_refreshed.connect(self.refresh_tabs)

    def _on_import_finished_from_controller(self, success: bool, message: str) -> None:
        """Gestisce la fine dell'importazione dal controller."""
        if not success:
            logger.error(f"Importazione fallita dal controller: {message}")

    def showEvent(self, event: QShowEvent) -> None:
        """Esegue il primo refresh solo quando il pannello diventa visibile."""
        super().showEvent(event)
        if not self._first_refresh_done:
            self._first_refresh_done = True
            QTimer.singleShot(100, self._safe_refresh_tabs)

    def set_current_tab(self, index: int | None = None) -> None:
        """Cambia il tab visualizzato in base all'indice."""
        if index is not None and 0 <= index < self.main_tabs.count():
            self.main_tabs.setCurrentIndex(index)

    def _safe_refresh_tabs(self) -> None:
        """Tenta il caricamento dei tab gestendo eventuali errori critici del DB."""
        try:
            self.refresh_tabs()
        except Exception:
            logger.exception("Error refreshing tabs for ContabilitaPanel")

    def _setup_ui(self) -> None:
        """Costruisce l'architettura dei tab e la toolbar unificata."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        self._setup_toolbar(layout)
        self._setup_tabs(layout)

    def _setup_toolbar(self, parent_layout: QVBoxLayout) -> None:
        """Configura la barra degli strumenti superiore."""
        self.toolbar_card = ModernCard(elevation=10)
        self.toolbar_card.setObjectName("filterBar")

        toolbar_layout = QHBoxLayout(self.toolbar_card)
        toolbar_layout.setContentsMargins(15, 10, 15, 10)
        toolbar_layout.setSpacing(15)

        # Sezione Statistiche Rapide
        self._setup_stats_section(toolbar_layout)

        # Divisore
        v_line = QFrame()
        v_line.setFrameShape(QFrame.Shape.VLine)
        v_line.setFrameShadow(QFrame.Shadow.Plain)
        v_line.setStyleSheet(f"color: {COLORS['border_light']};")
        toolbar_layout.addWidget(v_line)

        # Sezione Ricerca
        self._setup_search_section(toolbar_layout)

        toolbar_layout.addStretch()

        # Info & Actions
        self._setup_actions_section(toolbar_layout)

        parent_layout.addWidget(self.toolbar_card)

    def _setup_stats_section(self, layout: QHBoxLayout) -> None:
        """Configura la sezione statistiche della toolbar."""
        stats_h = QHBoxLayout()
        stats_h.setSpacing(20)

        rows_v = QVBoxLayout()
        rows_v.setSpacing(4)
        lbl_rows = QLabel("RIGHE SELEZIONATE")
        lbl_rows.setStyleSheet(LABEL_MUTED)
        self.selection_count_label = QLabel("0")
        self.selection_count_label.setStyleSheet(
            f"color: {COLORS['text_dark']}; font-weight: 700; font-size: 14px;"
        )
        rows_v.addWidget(lbl_rows)
        rows_v.addWidget(self.selection_count_label)
        stats_h.addLayout(rows_v)

        hours_v = QVBoxLayout()
        hours_v.setSpacing(4)
        lbl_hours = QLabel("TOTALE ORE")
        lbl_hours.setStyleSheet(LABEL_MUTED)
        self.selection_sum_label = QLabel("0")
        self.selection_sum_label.setStyleSheet(
            f"color: {COLORS['teal_accent']}; font-weight: 800; font-size: 14px;"
        )
        hours_v.addWidget(lbl_hours)
        hours_v.addWidget(self.selection_sum_label)
        stats_h.addLayout(hours_v)

        layout.addLayout(stats_h)

    def _setup_search_section(self, layout: QHBoxLayout) -> None:
        """Configura la sezione di ricerca della toolbar."""
        search_v = QVBoxLayout()
        search_v.setSpacing(4)
        lbl_search = QLabel("CERCA NEI DATI")
        lbl_search.setStyleSheet(LABEL_MUTED)
        self.search_input = SearchInput()
        self.search_input.setPlaceholderText("Cerca ovunque...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setMinimumWidth(300)
        self.search_input.setStyleSheet(LINEEDIT_STYLE)
        self.search_input.textChanged.connect(self.controller.handle_search)
        search_v.addWidget(lbl_search)
        search_v.addWidget(self.search_input)
        layout.addLayout(search_v)

    def _setup_actions_section(self, layout: QHBoxLayout) -> None:
        """Configura la sezione azioni della toolbar."""
        info_v = QVBoxLayout()
        info_v.setSpacing(4)
        info_v.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.status_lbl = QLabel("Pronto")
        self.status_lbl.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 10px;")
        self.status_lbl.setTextFormat(Qt.TextFormat.RichText)

        self.update_btn = ModernButton(
            "AGGIORNA DATABASE",
            variant=ModernButton.Variant.PRIMARY,
            size=ModernButton.Size.SMALL,
            icon=get_asset_path(Icons.REFRESH),
        )
        self.update_btn.clicked.connect(self.controller.start_import_process)

        btn_h = QHBoxLayout()
        btn_h.setSpacing(5)
        btn_h.addWidget(self.update_btn)

        info_v.addWidget(self.status_lbl)
        info_v.addLayout(btn_h)
        layout.addLayout(info_v)

    def _setup_tabs(self, parent_layout: QVBoxLayout) -> None:
        """Inizializza i tab principali dell'interfaccia."""
        self.main_tabs = AnimatedTabWidget()
        self.main_tabs.currentChanged.connect(self._on_main_tab_changed)

        self._add_preventivi_tabs()
        self._add_giornaliere_tabs()
        self._add_programmate_tabs()
        self._add_certificati_tabs()
        self._add_kpi_tabs()

        parent_layout.addWidget(self.main_tabs)

    def _add_preventivi_tabs(self) -> None:
        """Aggiunge i tab dei preventivi annuali."""
        self.year_tabs_widget = AnimatedTabWidget()
        self.year_tabs_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.year_tabs_widget.currentChanged.connect(self._on_tab_changed)
        self.main_tabs.addTab(
            self.year_tabs_widget,
            get_colored_icon(get_asset_path(Icons.FOLDER), COLORS["text_muted"]),
            "Preventivi",
        )

    def _add_giornaliere_tabs(self) -> None:
        """Aggiunge i tab delle giornaliere annuali."""
        self.giornaliere_tabs_widget = AnimatedTabWidget()
        self.giornaliere_tabs_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.giornaliere_tabs_widget.currentChanged.connect(self._on_tab_changed)
        self.main_tabs.addTab(
            self.giornaliere_tabs_widget,
            get_colored_icon(get_asset_path(Icons.FOLDER), COLORS["text_muted"]),
            "Giornaliere",
        )

    def _add_programmate_tabs(self) -> None:
        """Aggiunge il tab delle attività programmate."""
        self.attivita_widget = AttivitaProgrammateTab()
        self.main_tabs.addTab(
            self.attivita_widget,
            get_colored_icon(get_asset_path(Icons.CALENDAR), COLORS["text_muted"]),
            "Attività Programmate",
        )

    def _add_certificati_tabs(self) -> None:
        """Aggiunge il tab dei certificati campione."""
        self.certificati_widget = CertificatiCampioneTab()
        self.main_tabs.addTab(
            self.certificati_widget,
            get_colored_icon(get_asset_path(Icons.FILE_TEXT), COLORS["text_muted"]),
            "Certificati Campione",
        )

    def _add_kpi_tabs(self) -> None:
        """Aggiunge il tab dell'analisi KPI."""
        self.kpi_panel = ContabilitaKPIPanel()
        self.main_tabs.addTab(
            self.kpi_panel,
            get_colored_icon(get_asset_path(Icons.BAR_CHART), COLORS["text_muted"]),
            "Analisi KPI",
        )

    def _on_search_changed(self, text: str) -> None:
        """Inoltra la stringa di ricerca al widget o al tab attualmente attivo."""
        current_widget = self.main_tabs.currentWidget()
        if isinstance(current_widget, (QTabWidget, AnimatedTabWidget)):
            current_widget = current_widget.currentWidget()
        if current_widget and hasattr(current_widget, "filter_data") and callable(current_widget.filter_data):
            current_widget.filter_data(text)

    def _on_main_tab_changed(self, index: int) -> None:
        """Nasconde o mostra gli strumenti di ricerca in base al tab selezionato."""
        tab_text = self.main_tabs.tabText(index)
        is_kpi = "Analisi KPI" in tab_text
        self.toolbar_card.setVisible(not is_kpi)

        if not is_kpi:
            self._connect_selection_signal()
            text = self.search_input.text()
            if text:
                self._on_search_changed(text)
            self.search_input.setFocus()

    def refresh_tabs(self, auto_email: bool = False) -> None:
        """Interroga il database per gli anni disponibili e aggiorna i tab degli anni.

        Sincronizza inoltre i dati per le attività e i certificati.
        """
        years = ContabilitaManager.get_available_years()
        if not years:
            for tw in (self.year_tabs_widget, self.giornaliere_tabs_widget):
                tw.clear()
                tw.addTab(QLabel("Nessun dato disponibile."), "Info")
            return

        self._sync_tab_widget(self.year_tabs_widget, years, ContabilitaYearTab)
        self._sync_tab_widget(self.giornaliere_tabs_widget, years, GiornaliereYearTab)
        self._connect_selection_signal()

        if hasattr(self.kpi_panel, "refresh_years") and callable(self.kpi_panel.refresh_years):
            self.kpi_panel.refresh_years()

        if hasattr(self.attivita_widget, "refresh_data") and callable(self.attivita_widget.refresh_data):
            self.attivita_widget.refresh_data()

        if hasattr(self.certificati_widget, "refresh_data") and callable(
            self.certificati_widget.refresh_data
        ):
            self.certificati_widget.refresh_data()

            # Se richiesto e siamo nel tab certificati, lancia email
            if auto_email and self.main_tabs.currentIndex() == 3:
                from PySide6.QtCore import QTimer

                QTimer.singleShot(1000, self.certificati_widget._run_analysis_and_send_email)

        # Riapplica il filtro di ricerca se presente
        search_text = self.search_input.text()
        if search_text:
            self._on_search_changed(search_text)

    def _sync_tab_widget(
        self, tab_widget: AnimatedTabWidget, target_years: list[int], tab_class: Any
    ) -> None:
        """Aggiorna i tab di un AnimatedTabWidget senza distruggere i widget esistenti per gli stessi anni."""
        existing_years = {}
        for i in range(tab_widget.count()):
            with suppress(ValueError):
                existing_years[int(tab_widget.tabText(i))] = i

        for year in list(existing_years.keys()):
            if year not in target_years:
                tab_widget.removeTab(existing_years[year])
                self._sync_tab_widget(tab_widget, target_years, tab_class)
                return

        for year in target_years:
            if year in existing_years:
                widget = tab_widget.widget(existing_years[year])
                if widget and hasattr(widget, "refresh_data") and callable(widget.refresh_data):
                    widget.refresh_data()
            else:
                tab_widget.addTab(tab_class(year), str(year))

    def set_search_query(self, query: str) -> None:
        """Programma l'input di ricerca esternamente (es. da Quick Actions)."""
        self.search_input.setText(query)
        self.search_input.setFocus()
        self.search_input.selectAll()

    def _on_tab_changed(self, index: int) -> None:
        """Gestisce il cambio dell'anno all'interno di una categoria contabile."""
        self._connect_selection_signal()
        text = self.search_input.text()
        if text:
            self._on_search_changed(text)

    def _connect_selection_signal(self) -> None:
        """Collega dinamicamente i segnali di selezione della tabella attiva per aggiornare i totali ore."""
        curr = self.main_tabs.currentWidget()
        target = curr.currentWidget() if isinstance(curr, (QTabWidget, AnimatedTabWidget)) else curr

        if target:
            # Silenziamo il RuntimeWarning se il segnale non è connesso
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                if hasattr(target, "table"):
                    table: Any = target.table
                    if model := table.selectionModel():
                        with suppress(TypeError, RuntimeError):
                            model.selectionChanged.disconnect()
                        model.selectionChanged.connect(lambda s, d: self._update_selection_total(table))
                elif hasattr(target, "tree"):
                    tree: Any = target.tree
                    with suppress(TypeError, RuntimeError):
                        tree.itemSelectionChanged.disconnect()
                    tree.itemSelectionChanged.connect(lambda: self._update_selection_total(tree))

    def _update_selection_total(self, widget: QWidget) -> None:
        """Aggiorna le label statistiche basandosi sulla selezione corrente."""
        count, hours = ContabilitaStatsHelper.calculate_selection_stats(widget)
        self.selection_count_label.setText(str(count))
        self.selection_sum_label.setText(hours)

    def start_import_process(self) -> None:
        """Avvia il worker asincrono per l'importazione dei file Excel definiti nei path configurati."""
        config = config_manager.load_config()
        path = config.get("contabilita_file_path", "")
        if not path or not Path(path).exists():
            self.status_lbl.setText("File non trovato.")
            return

        self.update_btn.setDisabled(True)
        self.status_lbl.setText("Aggiornamento...")

        self.worker = ContabilitaWorker(
            "",  # Svuotiamo il path principale per non aggiornare Preventivi/Giornaliere
            "",
            "",
            config.get("certificati_campione_path", ""),
        )
        self.worker.finished_signal.connect(self._on_import_finished)
        self.worker.progress_signal.connect(self.status_lbl.setText)
        self.worker.start()

    def _on_import_finished(self, success: bool, msg: str, added: int, removed: int, duration: float) -> None:
        """Gestisce il completamento dell'importazione aggiornando lo stato e rinfrescando i dati."""
        if success:
            timestamp = datetime.now(UTC).astimezone().strftime("%d/%m/%Y %H:%M")
            added_str = f"<font color='{COLORS['success_dark']}'><b>+{added}</b></font>"
            removed_str = f"<font color='{COLORS['error_red']}'><b>-{removed}</b></font>"

            if duration < self.SECONDS_IN_MINUTE:
                time_str = f"{duration:.1f}s"
            else:
                time_str = (
                    f"{int(duration // self.SECONDS_IN_MINUTE)}m {int(duration % self.SECONDS_IN_MINUTE)}s"
                )

            final_status = f"{timestamp} {added_str} {removed_str} (Tempo: {time_str})"
            self._last_status_html = final_status
            self.status_lbl.setText(final_status)
            self.refresh_tabs(auto_email=True)
        else:
            self.status_lbl.setText("Errore")
            ConfirmationDialog.show_error(self, "Errore", msg)
        self.worker = None
        self.update_btn.setDisabled(False)
