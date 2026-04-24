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

from src.core.constants import Icons
from src.core.contabilita.certificati_engine import CertificatiEngine
from src.core.contabilita_manager import ContabilitaManager
from src.core.notification_manager import NotificationManager
from src.gui.dialogs.certificati_analysis_dialog import ScadenzeAnalysisDialog
from src.gui.styles import COLORS
from src.gui.widgets.contabilita.helpers import SortableTreeWidgetItem
from src.gui.widgets.core_widgets import PrimaryButton, StandardCheckBox
from src.utils.helpers import get_asset_path

from .certificati.tree_widget import CertificatiTreeWidget


class CertificatiCampioneTab(QWidget):
    """Tab per Certificati Campione (Tree View) - Versione Modularizzata."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """
        Inizializza il tab dei certificati.

        Args:
            parent: Widget genitore opzionale.
        """
        super().__init__(parent)
        self.engine = CertificatiEngine()
        self._show_excluded = False
        self._show_print_excluded = False
        self._only_excluded = False
        self._setup_ui()
        self._load_data()

    def _setup_ui(self) -> None:
        """Configura il layout, la toolbar e l'albero dei certificati."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)

        # Toolbar
        toolbar = QHBoxLayout()

        btn_expand = self._create_toolbar_btn("Espandi Tutto", Icons.FOLDER_OPEN, self._expand_all)
        btn_collapse = self._create_toolbar_btn("Comprimi Tutto", Icons.FOLDER, self._collapse_all)

        self.show_excluded_check = StandardCheckBox("Mostra esclusi monitoraggio")
        self.show_excluded_check.stateChanged.connect(self._on_show_excluded_changed)

        self.show_print_excluded_check = StandardCheckBox("Mostra esclusi stampa")
        self.show_print_excluded_check.stateChanged.connect(self._on_show_print_excluded_changed)

        self.only_excluded_check = StandardCheckBox("Solo esclusi")
        self.only_excluded_check.stateChanged.connect(self._on_only_excluded_changed)

        self.include_history_check = StandardCheckBox("Includi storico")
        self.include_history_check.setChecked(True)

        self.excluded_count_label = QLabel("")
        self.excluded_count_label.setStyleSheet(
            f"color: {COLORS['text_light']}; font-size: 12px; padding: 0 8px;"
        )

        self.btn_export_pdf = PrimaryButton("Esporta PDF")
        self.btn_export_pdf.setIcon(QIcon(get_asset_path(Icons.FILE_TEXT)))
        self.btn_export_pdf.clicked.connect(self._export_pdf)

        self.btn_analyze = PrimaryButton("Analizza Scadenze")
        self.btn_analyze.setIcon(QIcon(get_asset_path(Icons.BAR_CHART)))
        self.btn_analyze.clicked.connect(self._run_analysis)

        for w in (btn_expand, btn_collapse):
            toolbar.addWidget(w)
        toolbar.addSpacing(20)
        toolbar.addWidget(self.show_excluded_check)
        toolbar.addWidget(self.show_print_excluded_check)
        toolbar.addWidget(self.only_excluded_check)
        toolbar.addWidget(self.include_history_check)
        toolbar.addWidget(self.excluded_count_label)
        toolbar.addStretch()
        toolbar.addWidget(self.btn_export_pdf)
        toolbar.addWidget(self.btn_analyze)
        layout.addLayout(toolbar)

        # Tree Widget
        self.tree = CertificatiTreeWidget()
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)
        self.tree.itemExpanded.connect(self._on_item_expanded)
        self.tree.itemCollapsed.connect(self._on_item_collapsed)
        self.tree.itemEditedCustom.connect(self._on_item_edited)
        layout.addWidget(self.tree)

    def _create_toolbar_btn(self, text: str, icon_enum: str, callback: Any) -> PrimaryButton:
        """Helper per creare pulsanti della toolbar con stile coerente."""
        btn = PrimaryButton(text)
        btn.setIcon(QIcon(get_asset_path(icon_enum)))
        btn.clicked.connect(callback)
        btn.setStyleSheet(f"""
            QPushButton {{
                padding: 8px 16px; background-color: {COLORS["bg_alt"]};
                border: 1px solid {COLORS["border_medium"]}; border-radius: 6px;
                font-weight: 500; color: {COLORS["text_dark"]};
            }}
            QPushButton:hover {{ background-color: {COLORS["bg_hover"]}; }}
        """)
        return btn

    def _expand_all(self) -> None:
        """Espande tutti i rami dell'albero."""
        self.tree.expandAll()

    def _collapse_all(self) -> None:
        """Contrae tutti i rami dell'albero."""
        self.tree.collapseAll()

    def _on_show_excluded_changed(self, state: int) -> None:
        """Gestisce il cambiamento della checkbox 'Mostra esclusi monitoraggio'."""
        self._show_excluded = state in (Qt.CheckState.Checked.value, 2)
        self._apply_exclusion_visibility()

    def _on_show_print_excluded_changed(self, state: int) -> None:
        """Gestisce il cambiamento della checkbox 'Mostra esclusi stampa'."""
        self._show_print_excluded = state in (Qt.CheckState.Checked.value, 2)
        if self._show_print_excluded:
            self.only_excluded_check.setChecked(False)
        self._apply_exclusion_visibility()

    def _on_only_excluded_changed(self, state: int) -> None:
        """Gestisce il cambiamento della checkbox 'Solo esclusi'."""
        self._only_excluded = state in (Qt.CheckState.Checked.value, 2)
        if self._only_excluded:
            # Se vogliamo vedere SOLO gli esclusi, resettiamo gli altri filtri di "mostra" per coerenza
            self.show_excluded_check.setChecked(True)
            self.show_print_excluded_check.setChecked(True)
        self._apply_exclusion_visibility()

    def _apply_exclusion_visibility(self) -> None:
        """Applica la visibilità agli strumenti esclusi (monitoraggio/stampa) in base allo stato dei filtri."""
        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            if not parent:
                continue
            matricola = self.engine.parse_parent_label(parent.text(0))["matricola"]

            is_mon_excluded = matricola in self.engine._exclusions
            is_print_excluded = matricola in self.engine._print_exclusions
            is_any_excluded = is_mon_excluded or is_print_excluded

            if self._only_excluded:
                # Modalità "Solo esclusi": nascondi tutto ciò che NON è escluso
                parent.setHidden(not is_any_excluded)
            else:
                # Modalità standard: nascondi in base ai filtri di "mostra"
                hide_mon = is_mon_excluded and not self._show_excluded
                hide_print = is_print_excluded and not self._show_print_excluded
                parent.setHidden(hide_mon or hide_print)

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

    def _load_data(self) -> None:  # noqa: PLR0915
        """Popola l'albero raggruppando i certificati per ID-COEMI."""
        data = ContabilitaManager.get_certificati_campione_data()
        self.tree.clear()
        self.tree.setSortingEnabled(False)

        # Indici fissi del risultato DB (definiti in ContabilitaQueries)
        idx_id_coemi = 0
        idx_certificato = 1
        idx_modello = 2
        idx_costruttore = 3
        idx_matricola = 4
        idx_range = 5
        idx_errore = 6
        idx_emissione = 7
        idx_scadenza = 8
        idx_stato = 9
        idx_annotazioni = 10
        idx_ubicazione = 11
        idx_id = 12

        # Raggruppa per ID-COEMI (o Matricola/Certificato se manca)
        id_coemi_groups = defaultdict(list)
        for r in data:
            # Chiave di raggruppamento: ID-COEMI > Matricola > Certificato
            key = (
                str(r[idx_id_coemi]).strip()
                or str(r[idx_matricola]).strip()
                or str(r[idx_certificato]).strip()
                or "Sconosciuto"
            )
            id_coemi_groups[key].append(r)

        groups_with_priority = []
        for group_key, certificates in id_coemi_groups.items():
            # Ordina per emissione (più recente in alto)
            def parse_date(c: Any) -> datetime:
                # Guardia sulla lunghezza per evitare crash con dati mockati incompleti
                if len(c) <= idx_emissione:
                    return datetime.min.replace(tzinfo=UTC)
                    
                d = c[idx_emissione] or ""
                try:
                    return (
                        datetime.strptime(d, "%d/%m/%Y").replace(tzinfo=UTC)
                        if "/" in d
                        else datetime.min.replace(tzinfo=UTC)
                    )
                except Exception:
                    return datetime.min.replace(tzinfo=UTC)

            certs_sorted = sorted(certificates, key=parse_date, reverse=True)
            latest = certs_sorted[0]
            
            # Guardia sulla lunghezza per scadenza
            scadenza = latest[idx_scadenza] if len(latest) > idx_scadenza else ""
            days, icon = self.engine.calculate_days_and_status(scadenza)

            groups_with_priority.append(
                {
                    "group_key": group_key,
                    "id_coemi": (latest[idx_id_coemi] if len(latest) > idx_id_coemi else "") or "",
                    "matricola": (latest[idx_matricola] if len(latest) > idx_matricola else "") or "N/D",
                    "costruttore": (latest[idx_costruttore] if len(latest) > idx_costruttore else "") or "N/D",
                    "modello": (latest[idx_modello] if len(latest) > idx_modello else "") or "N/D",
                    "range_strumento": (latest[idx_range] if len(latest) > idx_range else "") or "",
                    "certificates": certs_sorted,
                    "days": days,
                    "icon": icon,
                    "priority": days if days is not None else 9999,
                }
            )

        groups_with_priority.sort(key=operator.itemgetter("priority"))

        for g in groups_with_priority:
            # Per l'esclusione usiamo la matricola o l'ID-COEMI?
            # Manteniamo la matricola per compatibilità con il file esclusioni
            is_excluded = g["matricola"] in self.engine._exclusions
            is_print_excluded = g["matricola"] in self.engine._print_exclusions
            days_val: int | None = g["days"]  # type: ignore
            days_text = self.engine.format_days_text_short(days_val)

            modello_str: str = g["modello"]  # type: ignore
            is_digital = "MANOMETRO DIGITALE" in modello_str.upper()
            range_part = f"  •  {g['range_strumento']}" if is_digital and g["range_strumento"] else ""
            excluded_marker = "  [ESCLUSO]" if is_excluded else ""
            print_excluded_marker = "  [NON STAMPARE]" if is_print_excluded else ""

            # Label Padre: ID-COEMI • Costruttore • Modello • Matricola • Stato
            id_part = f"{g['id_coemi']}  •  " if g["id_coemi"] else ""
            label = f"{id_part}{g['costruttore']}  •  {g['modello']}{range_part}  •  {g['matricola']}  •  {days_text}{excluded_marker}{print_excluded_marker}"
            parent_item = SortableTreeWidgetItem(self.tree, [label])
            parent_item.setFirstColumnSpanned(True)

            status_icon: str = Icons.STATUS_DOT_GRAY if is_excluded else g["icon"]  # type: ignore
            parent_item.setIcon(0, QIcon(get_asset_path(status_icon)))
            parent_item.setData(0, Qt.ItemDataRole.UserRole, {"days": days_val, "matricola": g["matricola"]})

            if is_excluded:
                font = parent_item.font(0)
                font.setStrikeOut(True)
                parent_item.setFont(0, font)
                parent_item.setForeground(0, QBrush(QColor(COLORS["text_light"])))

            cert_list: list[Any] = g["certificates"]  # type: ignore
            for i, cert in enumerate(cert_list):
                # Format errore_max (index 6)
                err_val = cert[idx_errore] if len(cert) > idx_errore else None
                err_formatted = self.engine.format_errore_max(err_val) if err_val is not None else ""

                def get_val(idx: int) -> str:
                    return str(cert[idx]) if len(cert) > idx and cert[idx] is not None else ""

                row_data = [
                    get_val(idx_id_coemi),  # 0. ID-COEMI
                    get_val(idx_certificato),  # 1. Certificato
                    get_val(idx_modello),  # 2. Modello
                    get_val(idx_costruttore),  # 3. Costruttore
                    get_val(idx_matricola),  # 4. Matricola
                    get_val(idx_range),  # 5. Range Strumento
                    err_formatted,  # 6. Err %
                    get_val(idx_emissione),  # 7. Emissione
                    get_val(idx_scadenza),  # 8. Scadenza
                    get_val(idx_stato),  # 9. Stato
                    str(
                        cert[idx_ubicazione] if len(cert) > idx_ubicazione and cert[idx_ubicazione] not in (None, "") else "ASSENTE"
                    ),  # 10. Ubicazione
                    get_val(idx_annotazioni),  # 11. Annotazioni
                ]

                row = SortableTreeWidgetItem(parent_item, row_data)

                # Salviamo l'ID nel ruolo user per poterlo aggiornare
                record_id = cert[idx_id] if len(cert) > idx_id else None
                row.setData(0, Qt.ItemDataRole.UserRole, record_id)

                # Permettiamo l'editing solo delle ultime due colonne
                flags = row.flags() | Qt.ItemFlag.ItemIsEditable
                row.setFlags(flags)

                if i == 0:
                    icon_val: str = g["icon"]  # type: ignore
                    self.tree.apply_current_certificate_styling(row, days_val, icon_val)
                else:
                    self.tree.apply_historical_certificate_styling(row)

        self.tree.collapseAll()
        self._apply_exclusion_visibility()
        self._update_excluded_count_label()

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

    def filter_data(self, text: str) -> None:
        """
        Filtra i certificati in base alla stringa di ricerca.

        Args:
            text: Testo da cercare in tutte le colonne.
        """
        query = text.lower()
        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            if not parent:
                continue

            # Controlliamo se la query è nel testo del PADRE (ID-COEMI, Matricola, etc.)
            parent_match = query in parent.text(0).lower()

            parent_visible = parent_match
            for j in range(parent.childCount()):
                child = parent.child(j)
                if not child:
                    continue

                # Se il padre non matcha, controlliamo i figli
                child_match = any(query in child.text(c).lower() for c in range(self.tree.columnCount()))

                # Se siamo in modalità ricerca, nascondiamo i figli che non matchano
                # A MENO CHE non abbia matchato il padre (in quel caso mostriamo tutto lo strumento)
                child.setHidden(not (parent_match or child_match))

                if child_match:
                    parent_visible = True

            parent.setHidden(not parent_visible)

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
            f"Certificati_Campione_{datetime.now().strftime('%Y%m%d')}.pdf",
            "PDF Files (*.pdf)",
        )

        if not file_path:
            return

        exporter = CertificatiPdfExporter(
            self.tree,
            self._show_excluded,
            include_history=self.include_history_check.isChecked(),
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
