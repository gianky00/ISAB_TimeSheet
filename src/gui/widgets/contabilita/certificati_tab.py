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

        self.show_excluded_check = StandardCheckBox("Mostra esclusi")
        self.show_excluded_check.stateChanged.connect(self._on_show_excluded_changed)

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
            toolbar.addWidget(btn_collapse)
            toolbar.addSpacing(20)
            toolbar.addWidget(self.show_excluded_check)
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
        """Gestisce il cambiamento della checkbox 'Mostra esclusi'."""
        self._show_excluded = state in (Qt.CheckState.Checked.value, 2)
        self._apply_exclusion_visibility()

    def _apply_exclusion_visibility(self) -> None:
        """Applica la visibilità agli strumenti esclusi in base allo stato del filtro."""
        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            if not parent:
                continue
            matricola = self.engine.parse_parent_label(parent.text(0))["matricola"]
            is_excluded = matricola in self.engine._exclusions
            parent.setHidden(is_excluded and not self._show_excluded)

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
        """Popola l'albero delegando i calcoli all'engine."""
        data = ContabilitaManager.get_certificati_campione_data()
        self.tree.clear()
        self.tree.setSortingEnabled(False)

        # Raggruppa per matricola
        matricola_groups = defaultdict(list)
        for r in data:
            matricola = r[self.tree.IDX_MATRICOLA] or "N/D"
            matricola_groups[matricola].append(r)

        groups_with_priority = []
        for matricola, certificates in matricola_groups.items():
            # Ordina per emissione (più recente in alto)
            def parse_date(c: Any) -> datetime:
                d = c[self.tree.IDX_EMISSIONE] or ""
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
            days, icon = self.engine.calculate_days_and_status(latest[self.tree.IDX_SCADENZA])

            groups_with_priority.append(
                {
                    "matricola": matricola,
                    "costruttore": latest[self.tree.IDX_COSTRUTTORE] or "N/D",
                    "modello": latest[self.tree.IDX_MODELLO] or "N/D",
                    "range_strumento": latest[self.tree.IDX_RANGE] or "",
                    "certificates": certs_sorted,
                    "days": days,
                    "icon": icon,
                    "priority": days if days is not None else 9999,
                }
            )

        groups_with_priority.sort(key=operator.itemgetter("priority"))

        for g in groups_with_priority:
            is_excluded = g["matricola"] in self.engine._exclusions
            days_val: int | None = g["days"]  # type: ignore
            days_text = self.engine.format_days_text_short(days_val)

            modello_str: str = g["modello"]  # type: ignore
            is_digital = "MANOMETRO DIGITALE" in modello_str.upper()
            range_part = f"  •  {g['range_strumento']}" if is_digital and g["range_strumento"] else ""
            excluded_marker = "  [ESCLUSO]" if is_excluded else ""

            label = f"{g['matricola']}  •  {g['costruttore']}  •  {g['modello']}{range_part}  •  {days_text}{excluded_marker}"
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
                # La tupla ha 13 elementi dal DB in ordine:
                # 0: id_coemi, 1: certificato, 2: modello, 3: costruttore, 4: matricola
                # 5: range, 6: errore_max, 7: emissione, 8: scadenza, 9: stato
                # 10: annotazioni, 11: ubicazione, 12: id

                # Format errore_max (index 6)
                err_val = cert[6]
                err_formatted = self.engine.format_errore_max(err_val) if err_val is not None else ""

                row_data = [
                    str(cert[0] if cert[0] is not None else ""),  # 0. ID
                    str(cert[1] if cert[1] is not None else ""),  # 1. Certificato
                    str(cert[2] if cert[2] is not None else ""),  # 2. Modello
                    str(cert[3] if cert[3] is not None else ""),  # 3. Costruttore
                    str(cert[4] if cert[4] is not None else ""),  # 4. Matricola
                    str(cert[5] if cert[5] is not None else ""),  # 5. Range Strumento
                    err_formatted,                                # 6. Err %
                    str(cert[7] if cert[7] is not None else ""),  # 7. Emissione
                    str(cert[8] if cert[8] is not None else ""),  # 8. Scadenza
                    str(cert[9] if cert[9] is not None else ""),  # 9. Stato
                    str(cert[11] if len(cert) > 11 and cert[11] is not None else ""), # 10. Ubicazione
                    str(cert[10] if len(cert) > 10 and cert[10] is not None else "")  # 11. Annotazioni
                ]

                row = SortableTreeWidgetItem(parent_item, row_data)

                # Salviamo l'ID nel ruolo user per poterlo aggiornare
                record_id = cert[12] if len(cert) > 12 else None
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
        count = len(self.engine._exclusions)
        self.excluded_count_label.setText(f"({count} esclusi)" if count > 0 else "")

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
            parent_visible = False
            for j in range(parent.childCount()):
                child = parent.child(j)
                if not child:
                    continue
                match = any(query in child.text(c).lower() for c in range(self.tree.columnCount()))
                child.setHidden(not match)
                if match:
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
            is_excluded = matricola in self.engine._exclusions
            action_text = "✅ Includi nel monitoraggio" if is_excluded else "🚫 Escludi dal monitoraggio"
            action = QAction(action_text, self)
            action.triggered.connect(lambda: self._toggle_exclusion(matricola))
            menu.addAction(action)
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
        self.engine.save_exclusions(self.engine._exclusions)
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

            # Recuperiamo l'ID-COEMI dal certificato corrente (primo figlio)
            id_coemi = ""
            if parent.childCount() > 0:
                child = parent.child(0)
                if child:
                    id_coemi = child.text(self.tree.IDX_ID)

            certs_data.append(
                {
                    "matricola": meta["matricola"],
                    "costruttore": meta["costruttore"],
                    "modello": meta["modello"],
                    "range": meta["range"],
                    "id_coemi": id_coemi,
                    "days": user_data.get("days") if user_data else None,
                }
            )

        certs_data.sort(key=lambda x: x["days"] if x["days"] is not None else 9999)
        ScadenzeAnalysisDialog(certs_data, self._show_excluded, self).exec()

    def _export_pdf(self) -> None:
        """Esporta la lista dei certificati in un PDF formattato professionalmente."""
        # Creiamo un modulo separato o usiamo una classe dedicata all'esportazione per mantenere SRP
        from src.gui.widgets.contabilita.certificati.pdf_exporter import CertificatiPdfExporter

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Esporta Certificati in PDF",
            f"Certificati_Campione_{datetime.now().strftime('%Y%m%d')}.pdf",
            "PDF Files (*.pdf)",
        )

        if not file_path:
            return

        exporter = CertificatiPdfExporter(
            self.tree, self._show_excluded, include_history=self.include_history_check.isChecked()
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
