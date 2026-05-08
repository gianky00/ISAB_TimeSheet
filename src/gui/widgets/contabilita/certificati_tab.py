"""
SyncroJob - Certificati Campione Tab (Refactored)
Gestore dell'interfaccia per il monitoraggio dei certificati campione.
Coordina l'uso del CertificatiEngine e del CertificatiTreeWidget.
"""

import operator
import os
from collections import defaultdict
from contextlib import suppress
from datetime import UTC, datetime
from typing import Any

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QAction, QBrush, QColor, QIcon
from PyQt6.QtWidgets import (
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
from src.utils.helpers import get_asset_path

from .certificati.tree_widget import CertificatiTreeWidget


class CertificatiCampioneTab(QWidget):
    """Tab per Certificati Campione (Tree View) - Versione Modularizzata."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il tab dei certificati caricano i filtri persistenti.

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
        self.tree.itemEditedCustom.connect(self._on_item_edited)
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
        from src.gui.widgets.core_widgets import SearchInput  # noqa: PLC0415

        self.search_input = SearchInput("Cerca per Matricola, Modello o ID...")
        self.search_input.setFixedWidth(350)
        self.search_input.textChanged.connect(self._apply_filters)
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
        """Gestisce la logica specifica per il filtro 'Solo Esclusi' e salva lo stato."""
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
            parent = self.tree.topLevelItem(i)
            if not parent:
                continue

            # 1. Recupero stati base
            is_any_ex = self._is_any_excluded(parent)
            is_absent = self._is_instrument_absent(parent)

            # 2. Calcolo Visibilità Primaria (Padre)
            visible = self._calculate_parent_visibility(parent, is_any_ex, is_absent)

            # 3. Gestione Figli (Storico) e Ricerca
            found_in_child = self._filter_child_items(parent, query)

            # 4. Verifica Finale con Ricerca
            if visible and query:
                visible = (query in parent.text(0).lower()) or found_in_child

            parent.setHidden(not visible)

        self._update_excluded_count_label()

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

    def _calculate_parent_visibility(
        self, parent: QTreeWidgetItem, is_any_ex: bool, is_absent: bool
    ) -> bool:
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
        expanded_matricole = []
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            if item and item.isExpanded():
                with suppress(Exception):
                    matricola = self.engine.parse_parent_label(item.text(0))["matricola"]
                    expanded_matricole.append(matricola)

        self._load_data()

        # Ripristina stato espansione
        if expanded_matricole:
            for i in range(self.tree.topLevelItemCount()):
                item = self.tree.topLevelItem(i)
                if item:
                    with suppress(Exception):
                        matricola = self.engine.parse_parent_label(item.text(0))["matricola"]
                        if matricola in expanded_matricole:
                            item.setExpanded(True)

    def _load_data(self) -> None:
        """Popola l'albero raggruppando i certificati per ID-COEMI."""
        data = ContabilitaManager.get_certificati_campione_data()
        self.tree.clear()
        self.tree.setSortingEnabled(False)

        # 1. Raggruppamento dati
        id_coemi_groups = self._group_data_by_id_coemi(data)

        # 2. Preparazione gruppi con metadati e priorità
        groups_with_priority = self._prepare_groups_with_priority(id_coemi_groups)
        groups_with_priority.sort(key=operator.itemgetter("priority"))

        # 3. Popolamento Tree
        for g in groups_with_priority:
            parent_item = self._create_parent_item(g)
            self._add_child_items(parent_item, g)

        self.tree.collapseAll()
        self._apply_filters()
        self._update_excluded_count_label()

    def _group_data_by_id_coemi(self, data: list[tuple[Any, ...]]) -> dict[str, list[tuple[Any, ...]]]:
        """Raggruppa le righe del DB per ID-COEMI o fallback (Matricola/Certificato)."""
        from src.core.contabilita_queries import ContabilitaQueries  # noqa: PLC0415

        idx_id_coemi = ContabilitaQueries.CERT_IDX_ID_COEMI
        idx_matricola = ContabilitaQueries.CERT_IDX_MATRICOLA
        idx_certificato = ContabilitaQueries.CERT_IDX_CERTIFICATO

        groups = defaultdict(list)
        for r in data:
            key = (
                str(r[idx_id_coemi]).strip()
                or str(r[idx_matricola]).strip()
                or str(r[idx_certificato]).strip()
                or "Sconosciuto"
            )
            groups[key].append(r)
        return groups

    def _prepare_groups_with_priority(self, groups: dict[str, list[tuple[Any, ...]]]) -> list[dict[str, Any]]:
        """Calcola stati e priorità per ogni gruppo di certificati."""
        from src.core.contabilita_queries import ContabilitaQueries  # noqa: PLC0415

        processed_groups = []
        for group_key, certificates in groups.items():
            certs_sorted = sorted(certificates, key=self._parse_emission_date, reverse=True)
            latest = certs_sorted[0]

            scadenza = (
                latest[ContabilitaQueries.CERT_IDX_SCADENZA]
                if len(latest) > ContabilitaQueries.CERT_IDX_SCADENZA
                else ""
            )
            days, icon = self.engine.calculate_days_and_status(scadenza)

            processed_groups.append(
                {
                    "group_key": group_key,
                    "id_coemi": self._get_col_safe(latest, ContabilitaQueries.CERT_IDX_ID_COEMI),
                    "matricola": self._get_col_safe(latest, ContabilitaQueries.CERT_IDX_MATRICOLA) or "N/D",
                    "costruttore": self._get_col_safe(latest, ContabilitaQueries.CERT_IDX_COSTRUTTORE)
                    or "N/D",
                    "modello": self._get_col_safe(latest, ContabilitaQueries.CERT_IDX_MODELLO) or "N/D",
                    "range_strumento": self._get_col_safe(latest, ContabilitaQueries.CERT_IDX_RANGE),
                    "certificates": certs_sorted,
                    "days": days,
                    "icon": icon,
                    "priority": days if days is not None else 9999,
                }
            )
        return processed_groups

    def _parse_emission_date(self, row: tuple[Any, ...]) -> datetime:
        """Helper per il parsing sicuro della data di emissione per l'ordinamento."""
        from src.core.contabilita_queries import ContabilitaQueries  # noqa: PLC0415

        idx = ContabilitaQueries.CERT_IDX_EMISSIONE
        if len(row) <= idx:
            return datetime.min.replace(tzinfo=UTC)

        d = row[idx] or ""
        try:
            return (
                datetime.strptime(d, "%d/%m/%Y").replace(tzinfo=UTC)
                if "/" in d
                else datetime.min.replace(tzinfo=UTC)
            )
        except Exception:
            return datetime.min.replace(tzinfo=UTC)

    def _get_col_safe(self, row: tuple[Any, ...], idx: int) -> str:
        """Ritorna il valore della colonna in modo sicuro."""
        return str(row[idx]).strip() if len(row) > idx and row[idx] is not None else ""

    def _create_parent_item(self, g: dict[str, Any]) -> SortableTreeWidgetItem:
        """Crea e configura l'elemento padre nell'albero."""
        is_excluded = g["matricola"] in self.engine._exclusions
        is_print_excluded = g["matricola"] in self.engine._print_exclusions
        days_val: int | None = g["days"]
        days_text = self.engine.format_days_text_short(days_val)

        is_digital = "MANOMETRO DIGITALE" in str(g["modello"]).upper()
        range_part = f"  •  {g['range_strumento']}" if is_digital and g["range_strumento"] else ""
        ex_marker = "  [ESCLUSO]" if is_excluded else ""
        pr_marker = "  [NON STAMPARE]" if is_print_excluded else ""

        id_part = f"{g['id_coemi']}  •  " if g["id_coemi"] else ""
        label = f"{id_part}{g['costruttore']}  •  {g['modello']}{range_part}  •  {g['matricola']}  •  {days_text}{ex_marker}{pr_marker}"

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
        from src.core.contabilita_queries import ContabilitaQueries  # noqa: PLC0415

        for i, cert in enumerate(g["certificates"]):
            err_val = (
                cert[ContabilitaQueries.CERT_IDX_ERRORE]
                if len(cert) > ContabilitaQueries.CERT_IDX_ERRORE
                else None
            )
            err_formatted = self.engine.format_errore_max(err_val) if err_val is not None else ""

            row_data = [
                self._get_col_safe(cert, ContabilitaQueries.CERT_IDX_ID_COEMI),
                self._get_col_safe(cert, ContabilitaQueries.CERT_IDX_CERTIFICATO),
                self._get_col_safe(cert, ContabilitaQueries.CERT_IDX_MODELLO),
                self._get_col_safe(cert, ContabilitaQueries.CERT_IDX_COSTRUTTORE),
                self._get_col_safe(cert, ContabilitaQueries.CERT_IDX_MATRICOLA),
                self._get_col_safe(cert, ContabilitaQueries.CERT_IDX_RANGE),
                err_formatted,
                self._get_col_safe(cert, ContabilitaQueries.CERT_IDX_EMISSIONE),
                self._get_col_safe(cert, ContabilitaQueries.CERT_IDX_SCADENZA),
                self._get_col_safe(cert, ContabilitaQueries.CERT_IDX_STATO),
                self._get_ubicazione_safe(cert),
                self._get_col_safe(cert, ContabilitaQueries.CERT_IDX_ANNOTAZIONI),
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
        from src.core.contabilita_queries import ContabilitaQueries  # noqa: PLC0415

        idx = ContabilitaQueries.CERT_IDX_UBICAZIONE
        val = cert[idx] if len(cert) > idx else None
        return str(val) if val not in (None, "") else "ASSENTE"

    def _on_item_edited(self, item: QTreeWidgetItem, col_name: str, new_value: str) -> None:
        """Salva nel database quando un utente modifica Annotazioni o Ubicazione."""
        record_id = item.data(0, Qt.ItemDataRole.UserRole)
        if record_id:
            ContabilitaManager.update_certificato_field(record_id, col_name, new_value)

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
        is_parent = item.parent() is None

        if is_parent:
            matricola = self.engine.parse_parent_label(item.text(0))["matricola"]

            # Monitoraggio
            is_excluded = matricola in self.engine._exclusions
            mon_text = "[OK] Includi nel monitoraggio" if is_excluded else "🚫 Escludi dal monitoraggio"
            mon_act = QAction(mon_text, self)
            mon_act.triggered.connect(lambda: self._toggle_exclusion(matricola))
            menu.addAction(mon_act)

            # Stampa
            is_print_excluded = matricola in self.engine._print_exclusions
            print_text = "🖨️ Includi nella stampa" if is_print_excluded else "🚫 Escludi dalla stampa"
            print_act = QAction(print_text, self)
            print_act.triggered.connect(lambda: self._toggle_print_exclusion(matricola))
            menu.addAction(print_act)

            menu.addSeparator()
            toggle_expand = QAction("Comprimi" if item.isExpanded() else "Espandi", self)
            toggle_expand.triggered.connect(
                lambda: self.tree.collapseItem(item) if item.isExpanded() else self.tree.expandItem(item)
            )
            menu.addAction(toggle_expand)
        else:
            # Opzioni per il singolo certificato (Figlio)
            cert_number = item.text(self.tree.IDX_CERTIFICATO)
            if cert_number:
                open_act = QAction("📄 Apri Certificato", self)
                open_act.triggered.connect(lambda: self._open_certificate(cert_number))
                menu.addAction(open_act)

            menu.addSeparator()

            edit_anno_act = QAction("📝 Modifica Annotazioni", self)
            edit_anno_act.triggered.connect(lambda: self.tree.editItem(item, self.tree.IDX_ANNOTAZIONI))
            menu.addAction(edit_anno_act)

            edit_ubic_act = QAction("📍 Modifica Ubicazione", self)
            edit_ubic_act.triggered.connect(lambda: self.tree.editItem(item, self.tree.IDX_UBICAZIONE))
            menu.addAction(edit_ubic_act)

        if viewport := self.tree.viewport():
            menu.exec(viewport.mapToGlobal(pos))

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
        """Tenta di aprire il file PDF del certificato specificato."""
        path = self.engine.find_certificate_path(cert_number)
        if path:
            os.startfile(path)  # noqa: S606
        else:
            QMessageBox.warning(self, "Non trovato", f"Impossibile trovare il certificato '{cert_number}'")

    def _run_analysis(self) -> None:
        """Avvia l'algoritmo di analisi predittiva delle scadenze."""
        certs_data = []
        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            if not parent:
                continue
            meta = self.engine.parse_parent_label(parent.text(0))

            # Se il filtro "Mostra esclusi" è disattivato, saltiamo gli esclusi
            is_excluded = meta["matricola"] in self.engine._exclusions
            if is_excluded and not self._show_excluded:
                continue

            user_data = parent.data(0, Qt.ItemDataRole.UserRole)

            # Recuperiamo i dati reali dalle colonne del primo figlio
            id_coemi = ""
            matricola = ""
            costruttore = meta["costruttore"]
            modello = meta["modello"]
            range_val = meta["range"]

            if parent.childCount() > 0:
                child = parent.child(0)
                if child:
                    id_coemi = child.text(self.tree.IDX_ID_COEMI)
                    matricola = child.text(self.tree.IDX_MATRICOLA)
                    costruttore = child.text(self.tree.IDX_COSTRUTTORE)
                    modello = child.text(self.tree.IDX_MODELLO)
                    range_val = child.text(self.tree.IDX_RANGE)

            certs_data.append(
                {
                    "matricola": matricola,
                    "costruttore": costruttore,
                    "modello": modello,
                    "range": range_val,
                    "id_coemi": id_coemi,
                    "days": user_data.get("days") if user_data else None,
                }
            )

        certs_data.sort(key=lambda x: x["days"] if x["days"] is not None else 9999)
        ScadenzeAnalysisDialog(certs_data, self._show_excluded, self).exec()

    def _export_pdf(self) -> None:
        """Esporta la lista dei certificati in un PDF formattato professionalmente."""
        # Creiamo un modulo separato o usiamo una classe dedicata all'esportazione per mantenere SRP
        from src.gui.widgets.contabilita.certificati.pdf_exporter import (  # noqa: PLC0415
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

        exporter = CertificatiPdfExporter(
            self.tree,
            self._show_excluded,
            include_history=self._include_history,
            print_exclusions=self.engine._print_exclusions,
        )
        success, message = exporter.export(file_path)

        if success:
            NotificationManager.instance().add_notification(
                title="Esportazione completata",
                message=f"PDF generato con successo: {os.path.basename(file_path)}",
                level="success",
                show_toast=True,
            )
        else:
            NotificationManager.instance().add_notification(
                title="Errore esportazione", message=message, level="error", show_toast=True
            )
