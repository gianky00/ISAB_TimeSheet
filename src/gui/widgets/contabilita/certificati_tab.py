"""SyncroJob - Certificati Campione Tab (Refactored).

Gestore dell'interfaccia per il monitoraggio dei certificati campione.
Coordina l'uso del CertificatiEngine e del CertificatiTreeWidget.
"""

from contextlib import suppress
from datetime import datetime
from typing import Any

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QAction, QBrush, QColor, QIcon
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMenu,
    QMessageBox,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.core.config_manager import get_config_value, set_config_value
from src.core.constants import Icons, UbicazioneStrumenti
from src.core.contabilita.certificati_engine import CertificatiEngine
from src.core.contabilita_manager import ContabilitaManager
from src.core.notification_manager import NotificationManager
from src.gui.dialogs.certificati_analysis_dialog import ScadenzeAnalysisDialog
from src.gui.styles import COLORS
from src.gui.widgets.contabilita.helpers import SortableTreeWidgetItem
from src.gui.widgets.core_widgets import PrimaryButton
from src.gui.workers.certificati_worker import CertificatiWorker
from src.gui.workers.pdf_export_worker import PDFExportWorker
from src.utils.helpers import get_asset_path, safe_open

from .certificati.tree_widget import CertificatiTreeWidget


class CertificatiCampioneTab(QWidget):
    """Tab per Certificati Campione (Tree View) - Versione Modularizzata."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Inizializza il tab dei certificati caricano i filtri persistenti.

        Args:
            parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self.engine = CertificatiEngine()

        # Caricamento Filtri Persistenti
        self._show_excluded = get_config_value("cert_filter_mon", False)
        self._show_print_excluded = get_config_value("cert_filter_print", False)
        self._only_excluded = get_config_value("cert_filter_only_ex", False)
        self._hide_absent = get_config_value("cert_filter_hide_absent", False)
        self._include_history = get_config_value("cert_filter_history", True)

        self.worker: CertificatiWorker | None = None
        self._pdf_worker: PDFExportWorker | None = None
        self._pending_expanded_ids: list[str] = []

        self._setup_ui()
        self._load_data()

    def _setup_ui(self) -> None:
        """Configura il layout, la toolbar e l'albero dei certificati."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Configurazione Componenti
        layout.addLayout(self._setup_toolbar())

        # Tree Widget
        self.tree = CertificatiTreeWidget()
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)
        self.tree.itemExpanded.connect(self._on_item_expanded)
        self.tree.itemCollapsed.connect(self._on_item_collapsed)
        self.tree.item_edited_custom.connect(self._on_item_edited)
        layout.addWidget(self.tree)

    def _setup_toolbar(self) -> QHBoxLayout:
        """Configura la toolbar superiore con azioni, ricerca e menu Mostra/Escludi."""
        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        # Azioni Rapide (Espandi/Comprimi)
        toolbar.addWidget(self._create_toolbar_btn("", Icons.MAXIMIZE, self._expand_all, "Espandi Tutto"))
        toolbar.addWidget(self._create_toolbar_btn("", Icons.MINIMIZE, self._collapse_all, "Comprimi Tutto"))
        toolbar.addSpacing(10)

        # Campo di Ricerca Moderno
        from src.gui.widgets.core_widgets import SearchInput

        self.search_input = SearchInput("Cerca per ID COEMI, Matricola, Modello...")
        self.search_input.setFixedWidth(350)
        self.search_input.textChanged.connect(lambda _: self._apply_filters())
        toolbar.addWidget(self.search_input)

        # Menu Mostra/Escludi (Professionale)
        self.btn_view_options = PrimaryButton("Mostra/Escludi")
        self.btn_view_options.setIcon(QIcon(get_asset_path(Icons.EYE)))
        self.btn_view_options.setMenu(self._create_view_menu())
        toolbar.addWidget(self.btn_view_options)

        self.excluded_count_label = QLabel("")
        self.excluded_count_label.setStyleSheet(
            f"color: {COLORS['text_light']}; font-size: 11px; font-style: italic; margin-left: 5px;"
        )
        toolbar.addWidget(self.excluded_count_label)

        toolbar.addStretch()

        self.btn_export_pdf = PrimaryButton("Esporta PDF")
        self.btn_export_pdf.setIcon(QIcon(get_asset_path(Icons.FILE_TEXT)))
        self.btn_export_pdf.clicked.connect(self._export_pdf)

        self.btn_analyze = PrimaryButton("Analizza Scadenze")
        self.btn_analyze.setIcon(QIcon(get_asset_path(Icons.BAR_CHART)))
        self.btn_analyze.clicked.connect(self._run_analysis)

        toolbar.addWidget(self.btn_export_pdf)
        toolbar.addWidget(self.btn_analyze)
        return toolbar

    def _create_view_menu(self) -> QMenu:
        """Crea il menu a discesa per i filtri di visualizzazione."""
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{ background-color: {COLORS["bg_white"]}; border: 1px solid {COLORS["border_medium"]}; padding: 5px; }}
            QMenu::item {{ padding: 6px 30px 6px 30px; color: {COLORS["text_dark"]}; }}
            QMenu::item:selected {{ background-color: {COLORS["bg_hover"]}; color: {COLORS["primary_dark"]}; }}
            QMenu::separator {{ height: 1px; background: {COLORS["border_light"]}; margin: 5px 10px; }}
        """)

        # Azioni Checkable
        self.act_mon = QAction("Monitoraggio (Esclusi)", self)
        self.act_mon.setCheckable(True)
        self.act_mon.setChecked(self._show_excluded)
        self.act_mon.triggered.connect(self._on_view_action_toggled)

        self.act_print = QAction("Stampa (Esclusi)", self)
        self.act_print.setCheckable(True)
        self.act_print.setChecked(self._show_print_excluded)
        self.act_print.triggered.connect(self._on_view_action_toggled)

        self.act_absent = QAction("Strumenti ASSENTI", self)
        self.act_absent.setCheckable(True)
        self.act_absent.setChecked(not self._hide_absent)
        self.act_absent.triggered.connect(self._on_view_action_toggled)

        self.act_history = QAction("Includi Storico", self)
        self.act_history.setCheckable(True)
        self.act_history.setChecked(self._include_history)
        self.act_history.triggered.connect(self._on_view_action_toggled)

        self.act_only_ex = QAction("Solo Esclusi", self)
        self.act_only_ex.setCheckable(True)
        self.act_only_ex.setChecked(self._only_excluded)
        self.act_only_ex.triggered.connect(self._on_only_excluded_toggled)

        menu.addAction(self.act_mon)
        menu.addAction(self.act_print)
        menu.addAction(self.act_absent)
        menu.addSeparator()
        menu.addAction(self.act_only_ex)
        menu.addAction(self.act_history)
        return menu

    def _on_view_action_toggled(self) -> None:
        """Sincronizza lo stato dai parametri del menu, salva su disco e riapplica i filtri."""
        self._show_excluded = self.act_mon.isChecked()
        self._show_print_excluded = self.act_print.isChecked()
        self._hide_absent = not self.act_absent.isChecked()
        self._include_history = self.act_history.isChecked()

        # Salvataggio Persistente
        set_config_value("cert_filter_mon", self._show_excluded)
        set_config_value("cert_filter_print", self._show_print_excluded)
        set_config_value("cert_filter_hide_absent", self._hide_absent)
        set_config_value("cert_filter_history", self._include_history)

        self._apply_filters()

    def _on_only_excluded_toggled(self, checked: bool) -> None:
        """Gestisce la logica specifica per il filtro 'Solo Esclusì e salva lo stato."""
        self._only_excluded = checked
        if checked:
            # Se vogliamo vedere SOLO gli esclusi, abilitiamo per coerenza la loro visualizzazione
            self.act_mon.setChecked(True)
            self.act_print.setChecked(True)
            self._show_excluded = True
            self._show_print_excluded = True

        set_config_value("cert_filter_only_ex", checked)
        self._apply_filters()

    def _create_toolbar_btn(
        self, text: str, icon_enum: str, callback: Any, tooltip: str = ""
    ) -> PrimaryButton:
        """Helper per creare pulsanti della toolbar con stile coerente."""
        btn = PrimaryButton(text)
        btn.setIcon(QIcon(get_asset_path(icon_enum)))
        btn.clicked.connect(callback)
        btn.setToolTip(tooltip)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                padding: 6px; background-color: {COLORS["bg_alt"]};
                border: 1px solid {COLORS["border_medium"]}; border-radius: 6px;
                min-width: 32px;
            }}
            QPushButton:hover {{ background-color: {COLORS["bg_hover"]}; border-color: {COLORS["primary_dark"]}; }}
        """)

        return btn

    def _expand_all(self) -> None:
        """Espande tutti i rami dell'albero."""
        self.tree.expandAll()

    def _collapse_all(self) -> None:
        """Contrae tutti i rami dell'albero."""
        self.tree.collapseAll()

    def _apply_filters(self) -> None:
        """Applica tutti i filtri (ricerca, esclusioni, assenti, storico) in un unico ciclo."""
        query = self.search_input.text().lower().strip()

        for i in range(self.tree.topLevelItemCount()):
            if parent := self.tree.topLevelItem(i):
                self._filter_parent_item(parent, query)

        self._update_excluded_count_label()

    def _filter_parent_item(self, parent: QTreeWidgetItem, query: str) -> None:
        """Determina e applica la visibilità per un singolo elemento padre."""
        # 1. Recupero stati base
        is_any_ex = self._is_any_excluded(parent)
        is_absent = self._is_instrument_absent(parent)

        # 2. Calcolo Visibilità Primaria (Padre)
        visible = self._calculate_parent_visibility(parent, is_any_ex, is_absent)

        # 3. Gestione Figli (Storico) e Ricerca
        found_in_child = self._filter_child_items(parent, query)

        # 4. Verifica Finale con Ricerca
        if visible and query:
            # Match su label padre o su qualsiasi dato nei figli
            visible = (query in parent.text(0).lower()) or found_in_child

        parent.setHidden(not visible)

    def _is_any_excluded(self, parent: QTreeWidgetItem) -> bool:
        """Verifica se lo strumento è escluso (monitoraggio o stampa)."""
        matricola = self.engine.parse_parent_label(parent.text(0))["matricola"]
        return matricola in self.engine._exclusions or matricola in self.engine._print_exclusions

    def _is_instrument_absent(self, parent: QTreeWidgetItem) -> bool:
        """Verifica se lo strumento è marcato come ASSENTE."""
        if parent.childCount() > 0 and (first_child := parent.child(0)):
            child_loc = first_child.text(self.tree.IDX_UBICAZIONE).upper()
            return UbicazioneStrumenti.ASSENTE.value in child_loc
        return False

    def _calculate_parent_visibility(self, parent: QTreeWidgetItem, is_any_ex: bool, is_absent: bool) -> bool:
        """Determina la visibilità dell'item padre basandosi sui filtri di stato."""
        if self._only_excluded:
            return is_any_ex

        # Esclusione basata sui singoli flag di monitoraggio/stampa
        matricola = self.engine.parse_parent_label(parent.text(0))["matricola"]
        if (matricola in self.engine._exclusions and not self._show_excluded) or (
            matricola in self.engine._print_exclusions and not self._show_print_excluded
        ):
            return False

        return not (self._hide_absent and is_absent)

    def _filter_child_items(self, parent: QTreeWidgetItem, query: str) -> bool:
        """Filtra i figli (storico) e verifica se la query match almeno uno di essi."""
        found_in_visible_child = False
        for j in range(parent.childCount()):
            if child := parent.child(j):
                is_allowed = (j == 0) or self._include_history
                child.setHidden(not is_allowed)

                if (
                    is_allowed
                    and query
                    and not found_in_visible_child
                    and any(query in child.text(c).lower() for c in range(self.tree.columnCount()))
                ):
                    found_in_visible_child = True
        return found_in_visible_child

    def refresh_data(self) -> None:
        """Ricarica i dati dal database e aggiorna la vista preservando lo stato."""
        # Ricarica esclusioni dal disco per sicurezza
        self.engine.load_exclusions()

        # Salva stato espansione
        self._pending_expanded_ids = []
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            if item and item.isExpanded():
                with suppress(Exception):
                    # Usiamo l'ID COEMI per ripristinare l'espansione
                    meta = self.engine.parse_parent_label(item.text(0))
                    if id_coemi := meta.get("id_coemi"):
                        self._pending_expanded_ids.append(id_coemi)

        self._load_data()

    def _load_data(self) -> None:
        """Popola l'albero raggruppando i certificati per ID COEMI (Asincrono)."""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()

        # Feedback visivo caricamento (opzionale)
        self.tree.setUpdatesEnabled(False)

        self.worker = CertificatiWorker(self.engine)
        self.worker.finished_signal.connect(self._on_data_ready)
        self.worker.error_signal.connect(lambda msg: print(f"Errore caricamento certificati: {msg}"))
        self.worker.start()

    def _on_data_ready(self, prioritized_groups: list[dict[str, Any]]) -> None:
        """Callback eseguita al termine del worker per popolare la UI."""
        self.tree.clear()
        self.tree.setSortingEnabled(False)

        # Popolamento Tree
        self._populate_tree(prioritized_groups)

        self.tree.collapseAll()

        # Ripristina stato espansione salvato
        if self._pending_expanded_ids:
            for i in range(self.tree.topLevelItemCount()):
                item = self.tree.topLevelItem(i)
                if item:
                    with suppress(Exception):
                        meta = self.engine.parse_parent_label(item.text(0))
                        if meta.get("id_coemi") in self._pending_expanded_ids:
                            item.setExpanded(True)
            self._pending_expanded_ids = []

        self._apply_filters()
        self._update_excluded_count_label()
        self.tree.setUpdatesEnabled(True)

    def _populate_tree(self, groups: list[dict[str, Any]]) -> None:
        """Crea gli elementi nell'albero per ogni gruppo di certificati."""
        for g in groups:
            parent_item = self._create_parent_item(g)
            self._add_child_items(parent_item, g)

    def _create_parent_item(self, g: dict[str, Any]) -> SortableTreeWidgetItem:
        """Crea e configura l'elemento padre nell'albero."""
        is_excluded = g["matricola"] in self.engine._exclusions
        is_print_excluded = g["matricola"] in self.engine._print_exclusions
        days_val: int | None = g["days"]
        days_text = self.engine.format_days_text_short(days_val)

        # Recupero numero certificato più recente (il primo della lista ordinata dall'engine)
        from src.core.contabilita_queries import ContabilitaQueries

        latest_cert_num = ""
        if g.get("certificates"):
            latest_cert_num = self.engine.get_col_safe(
                g["certificates"][0], ContabilitaQueries.CERT_IDX_CERTIFICATO
            )

        is_digital = "MANOMETRO DIGITALE" in str(g["modello"]).upper()
        range_part = f"  •  {g['range_strumento']}" if is_digital and g["range_strumento"] else ""
        ex_marker = "  [ESCLUSO]" if is_excluded else ""
        pr_marker = "  [NON STAMPARE]" if is_print_excluded else ""

        id_part = f"{g['id_coemi']}  •  " if g["id_coemi"] else ""
        cert_part = f"{latest_cert_num} " if latest_cert_num else ""
        label = (
            f"{id_part}{g['costruttore']}  •  {g['modello']}{range_part}  •  {g['matricola']}  •  "
            f"{cert_part}{days_text}{ex_marker}{pr_marker}"
        )

        parent_item = SortableTreeWidgetItem(self.tree, [label])
        parent_item.setFirstColumnSpanned(True)

        status_icon: str = Icons.STATUS_DOT_GRAY if is_excluded else g["icon"]
        parent_item.setIcon(0, QIcon(get_asset_path(status_icon)))
        parent_item.setData(0, Qt.ItemDataRole.UserRole, {"days": days_val, "matricola": g["matricola"]})

        if is_excluded:
            font = parent_item.font(0)
            font.setStrikeOut(True)
            parent_item.setFont(0, font)
            parent_item.setForeground(0, QBrush(QColor(COLORS["text_light"])))

        return parent_item

    def _add_child_items(self, parent: SortableTreeWidgetItem, g: dict[str, Any]) -> None:
        """Aggiunge i certificati (corrente e storico) come figli dell'item padre."""
        from src.core.contabilita_queries import ContabilitaQueries

        for i, cert in enumerate(g["certificates"]):
            err_val = (
                cert[ContabilitaQueries.CERT_IDX_ERRORE]
                if len(cert) > ContabilitaQueries.CERT_IDX_ERRORE
                else None
            )
            err_formatted = self.engine.format_errore_max(err_val) if err_val is not None else ""

            row_data = [
                self.engine.get_col_safe(cert, ContabilitaQueries.CERT_IDX_ID_STRUMENTO),
                self.engine.get_col_safe(cert, ContabilitaQueries.CERT_IDX_CERTIFICATO),
                self.engine.get_col_safe(cert, ContabilitaQueries.CERT_IDX_MODELLO),
                self.engine.get_col_safe(cert, ContabilitaQueries.CERT_IDX_COSTRUTTORE),
                self.engine.get_col_safe(cert, ContabilitaQueries.CERT_IDX_MATRICOLA),
                self.engine.get_col_safe(cert, ContabilitaQueries.CERT_IDX_RANGE),
                err_formatted,
                self.engine.get_col_safe(cert, ContabilitaQueries.CERT_IDX_EMISSIONE),
                self.engine.get_col_safe(cert, ContabilitaQueries.CERT_IDX_SCADENZA),
                self.engine.get_col_safe(cert, ContabilitaQueries.CERT_IDX_STATO),
                self._get_ubicazione_safe(cert),
                self.engine.get_col_safe(cert, ContabilitaQueries.CERT_IDX_ANNOTAZIONI),
            ]

            row = SortableTreeWidgetItem(parent, row_data)
            record_id = (
                cert[ContabilitaQueries.CERT_IDX_ID] if len(cert) > ContabilitaQueries.CERT_IDX_ID else None
            )
            row.setData(0, Qt.ItemDataRole.UserRole, record_id)
            row.setFlags(row.flags() | Qt.ItemFlag.ItemIsEditable)

            if i == 0:
                self.tree.apply_current_certificate_styling(row, g["days"], g["icon"])
            else:
                self.tree.apply_historical_certificate_styling(row)

    def _get_ubicazione_safe(self, cert: tuple[Any, ...]) -> str:
        """Ritorna l'ubicazione con fallback su ASSENTE."""
        from src.core.contabilita_queries import ContabilitaQueries

        idx = ContabilitaQueries.CERT_IDX_UBICAZIONE
        val = cert[idx] if len(cert) > idx else None
        return str(val) if val not in (None, "") else "ASSENTE"

    def _on_item_edited(self, item: QTreeWidgetItem, col_name: str, new_value: str) -> None:
        """Salva nel database quando un utente modifica Annotazioni o Ubicazione."""
        record_id = item.data(0, Qt.ItemDataRole.UserRole)
        if not record_id:
            return

        if col_name == "ubicazione":
            # Propaghiamo l'ubicazione a tutti i certificati dello stesso strumento (ID COEMI)
            id_coemi = item.text(self.tree.IDX_ID_STRUMENTO)
            if ContabilitaManager.update_certificati_ubicazione_by_id_coemi(id_coemi, new_value):
                # Aggiorniamo visivamente tutti i fratelli se necessario (o ricarichiamo i dati)
                self._update_ui_after_ubicazione_change(item, new_value)
        else:
            # Annotazioni rimangono specifiche del singolo certificato
            ContabilitaManager.update_certificato_field(record_id, col_name, new_value)

    def _update_ui_after_ubicazione_change(self, edited_item: QTreeWidgetItem, new_value: str) -> None:
        """Aggiorna visivamente l'ubicazione per tutti i certificati dello stesso gruppo."""
        if parent := edited_item.parent():
            for i in range(parent.childCount()):
                child = parent.child(i)
                if child:
                    child.setText(self.tree.IDX_UBICAZIONE, new_value)

    def _update_excluded_count_label(self) -> None:
        """Aggiorna il contatore degli strumenti esclusi nella toolbar."""
        mon_count = len(self.engine._exclusions)
        print_count = len(self.engine._print_exclusions)

        parts = []
        if mon_count > 0:
            parts.append(f"{mon_count} monitoraggio")
        if print_count > 0:
            parts.append(f"{print_count} stampa")

        text = f"({', '.join(parts)} esclusi)" if parts else ""
        self.excluded_count_label.setText(text)

    def _on_item_expanded(self, item: QTreeWidgetItem) -> None:
        """Evidenzia in grassetto l'intestazione quando viene espansa."""
        if item.parent() is None:
            font = item.font(0)
            font.setBold(True)
            item.setFont(0, font)

    def _on_item_collapsed(self, item: QTreeWidgetItem) -> None:
        """Rimuove il grassetto dall'intestazione quando viene contratta."""
        if item.parent() is None:
            font = item.font(0)
            font.setBold(False)
            item.setFont(0, font)

    def _show_context_menu(self, pos: QPoint) -> None:
        """Mostra il menu contestuale per includere/escludere o visualizzare certificati."""
        item = self.tree.itemAt(pos)
        if not item:
            return

        menu = QMenu(self)
        if item.parent() is None:
            self._add_parent_context_actions(menu, item)
        else:
            self._add_child_context_actions(menu, item)

        if viewport := self.tree.viewport():
            menu.exec(viewport.mapToGlobal(pos))

    def _add_parent_context_actions(self, menu: QMenu, item: QTreeWidgetItem) -> None:
        """Aggiunge le azioni specifiche per l'item padre (strumento)."""
        matricola = self.engine.parse_parent_label(item.text(0))["matricola"]

        # Monitoraggio
        is_ex = matricola in self.engine._exclusions
        mon_act = QAction("Includi nel monitoraggio" if is_ex else "Escludi dal monitoraggio", self)
        mon_act.setIcon(QIcon(get_asset_path(Icons.CHECK_CIRCLE if is_ex else Icons.X_CIRCLE)))
        mon_act.triggered.connect(lambda: self._toggle_exclusion(matricola))
        menu.addAction(mon_act)

        # Stampa
        is_pr_ex = matricola in self.engine._print_exclusions
        print_act = QAction("Includi nella stampa" if is_pr_ex else "Escludi dalla stampa", self)
        print_act.setIcon(QIcon(get_asset_path(Icons.FILE_TEXT if is_pr_ex else Icons.ALERT)))
        print_act.triggered.connect(lambda: self._toggle_print_exclusion(matricola))
        menu.addAction(print_act)

        menu.addSeparator()
        self._add_expansion_action(menu, item)

    def _add_child_context_actions(self, menu: QMenu, item: QTreeWidgetItem) -> None:
        """Aggiunge le azioni per il singolo certificato (figlio)."""
        if cert_num := item.text(self.tree.IDX_CERTIFICATO):
            open_act = QAction("Apri Certificato", self)
            open_act.setIcon(QIcon(get_asset_path(Icons.FILE_TEXT)))
            open_act.triggered.connect(lambda: self._open_certificate(cert_num))
            menu.addAction(open_act)

        menu.addSeparator()
        edit_anno = QAction("Modifica Annotazioni", self)
        edit_anno.setIcon(QIcon(get_asset_path(Icons.LIST)))
        edit_anno.triggered.connect(lambda: self.tree.editItem(item, self.tree.IDX_ANNOTAZIONI))
        menu.addAction(edit_anno)

        edit_ubic = QAction("Modifica Ubicazione", self)
        edit_ubic.setIcon(QIcon(get_asset_path(Icons.PDL)))
        edit_ubic.triggered.connect(lambda: self.tree.editItem(item, self.tree.IDX_UBICAZIONE))
        menu.addAction(edit_ubic)

    def _add_expansion_action(self, menu: QMenu, item: QTreeWidgetItem) -> None:
        """Aggiunge azione espandi/comprimi al menu."""
        toggle_expand = QAction("Comprimi" if item.isExpanded() else "Expand", self)
        toggle_expand.setIcon(QIcon(get_asset_path(Icons.MINIMIZE if item.isExpanded() else Icons.MAXIMIZE)))
        toggle_expand.triggered.connect(
            lambda: self.tree.collapseItem(item) if item.isExpanded() else self.tree.expandItem(item)
        )
        menu.addAction(toggle_expand)

    def _toggle_exclusion(self, matricola: str) -> None:
        """Inverte lo stato di esclusione di una matricola."""
        if matricola in self.engine._exclusions:
            self.engine._exclusions.discard(matricola)
        else:
            self.engine._exclusions.add(matricola)
        self.engine.save_exclusions(exclusions=self.engine._exclusions)
        self._load_data()

    def _toggle_print_exclusion(self, matricola: str) -> None:
        """Inverte lo stato di esclusione dalla stampa di una matricola."""
        if matricola in self.engine._print_exclusions:
            self.engine._print_exclusions.discard(matricola)
        else:
            self.engine._print_exclusions.add(matricola)
        self.engine.save_exclusions(print_exclusions=self.engine._print_exclusions)
        self._load_data()

    def _open_certificate(self, cert_number: str) -> None:
        """Tenta di aprire il file PDF del certificato specificato in modo sicuro."""
        if path := self.engine.find_certificate_path(cert_number):
            safe_open(path)
        else:
            QMessageBox.warning(self, "Non trovato", f"Impossibile trovare il certificato '{cert_number}'")

    def _collect_analysis_data(self) -> list[dict[str, Any]]:
        """Raccoglie i dati degli strumenti per l'analisi, escludendo gli item non validi."""
        certs_data = []
        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            if not parent:
                continue
            meta = self.engine.parse_parent_label(parent.text(0))

            # Se il filtro "Mostra esclusi" è disattivato, saltiamo gli esclusi
            is_excluded = meta.get("matricola", "") in self.engine._exclusions
            if is_excluded and not self._show_excluded:
                continue

            user_data = parent.data(0, Qt.ItemDataRole.UserRole)
            id_coemi = meta.get("id_coemi", "")
            matricola = meta.get("matricola", "")
            costruttore = meta.get("costruttore", "N/D")
            modello = meta.get("modello", "N/D")
            range_val = meta.get("range", "")
            ubicazione = "ASSENTE"

            if parent.childCount() > 0:
                child = parent.child(0)
                if child:
                    id_coemi = child.text(self.tree.IDX_ID_STRUMENTO)
                    matricola = child.text(self.tree.IDX_MATRICOLA)
                    costruttore = child.text(self.tree.IDX_COSTRUTTORE)
                    modello = child.text(self.tree.IDX_MODELLO)
                    range_val = child.text(self.tree.IDX_RANGE)
                    ubicazione = child.text(self.tree.IDX_UBICAZIONE)

            certs_data.append(
                {
                    "matricola": matricola,
                    "costruttore": costruttore,
                    "modello": modello,
                    "range": range_val,
                    "id_strumento": id_coemi,
                    "ubicazione": ubicazione,
                    "days": user_data.get("days") if user_data else None,
                }
            )
        return certs_data

    def _run_analysis(self) -> None:
        """Avvia l'algoritmo di analisi predittiva delle scadenze."""
        certs_data = self._collect_analysis_data()
        certs_data.sort(key=lambda x: x["days"] if x["days"] is not None else 9999)
        ScadenzeAnalysisDialog(certs_data, self._show_excluded, self, self.tree, self.engine).exec()

    def _run_analysis_and_send_email(self) -> None:
        """Esegue l'analisi e invia direttamente l'email (utilizzato dopo aggiornamento DB)."""
        certs_data = self._collect_analysis_data()
        certs_data.sort(key=lambda x: x["days"] if x["days"] is not None else 9999)

        # Creiamo il dialogo ma invece di mostrarlo invochiamo direttamente l'email
        dialog = ScadenzeAnalysisDialog(certs_data, self._show_excluded, self, self.tree, self.engine)
        dialog._send_email()

    def _export_pdf(self) -> None:
        """Esporta la lista dei certificati in un PDF formattato professionalmente (Asincrono)."""
        from src.gui.widgets.contabilita.certificati.pdf_exporter import (
            CertificatiPdfExporter,
        )

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Esporta Certificati in PDF",
            f"Report Certificati Campione Secondari ISAB SUD al {datetime.now().strftime('%d-%m-%Y')}.pdf",
            "PDF Files (*.pdf)",
        )

        if not file_path:
            return

        if hasattr(self, "_pdf_worker") and self._pdf_worker and self._pdf_worker.isRunning():
            return

        NotificationManager.instance().add_notification(
            title="PDF", message="Generazione PDF in corso...", level="info", show_toast=True
        )

        exporter = CertificatiPdfExporter(
            self.tree,
            show_excluded=self._show_excluded,
            include_history=self._include_history,
            print_exclusions=self.engine._print_exclusions,
        )

        self._pdf_worker = PDFExportWorker(exporter, file_path)
        self._pdf_worker.finished_signal.connect(self._on_pdf_export_finished)
        self._pdf_worker.start()

    def _on_pdf_export_finished(self, success: bool, message: str) -> None:
        """Callback al termine della generazione PDF."""
        if success:
            NotificationManager.instance().add_notification(
                title="Esportazione completata",
                message="Il report PDF è stato generato con successo.",
                level="success",
                show_toast=True,
            )
        else:
            NotificationManager.instance().add_notification(
                title="Errore esportazione", message=message, level="error", show_toast=True
            )
