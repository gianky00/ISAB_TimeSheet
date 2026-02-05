import json
import os
import subprocess
import tempfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QBrush, QColor, QFont, QIcon
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMenu,
    QMessageBox,
    QPushButton,
    QTreeWidget,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.config_manager import CONFIG_DIR
from src.core.constants import Icons
from src.core.contabilita_manager import ContabilitaManager
from src.gui.widgets.contabilita.helpers import SortableTreeWidgetItem
from src.utils.helpers import get_asset_path


class CertificatiCampioneTab(QWidget):
    """Tab per Certificati Campione (Tree View)."""

    # File per memorizzare le esclusioni
    EXCLUSIONS_FILE = CONFIG_DIR / "data" / "certificati_exclusions.json"

    # Stile per elementi esclusi
    EXCLUDED_STYLE = """
        color: #9ca3af;
        text-decoration: line-through;
    """

    HEADERS = [
        "Modello /\nTipo",
        "Costruttore",
        "Matricola",
        "Range\nStrumento",
        "Errore\nmax %",
        "Certificato\nTaratura",
        "Scadenza\nCertificato",
        "Emissione\nCertificato",
        "ID-COEMI",
        "Stato\nCertificato",
    ]
    (
        IDX_MODELLO,
        IDX_COSTRUTTORE,
        IDX_MATRICOLA,
        IDX_RANGE,
        IDX_ERRORE,
        IDX_CERTIFICATO,
        IDX_SCADENZA,
        IDX_EMISSIONE,
        IDX_ID,
        IDX_STATO,
    ) = range(10)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._exclusions: set[str] = set()  # Set di matricole escluse
        self._show_excluded = False  # Flag per mostrare/nascondere esclusi
        self._load_exclusions()
        self._setup_ui()
        self._load_data()

    def _load_exclusions(self):
        """Carica le esclusioni dal file JSON."""
        try:
            if self.EXCLUSIONS_FILE.exists():
                with open(self.EXCLUSIONS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._exclusions = set(data.get("excluded_matricole", []))
        except Exception:
            self._exclusions = set()

    def _save_exclusions(self):
        """Salva le esclusioni nel file JSON."""
        try:
            # Assicura che la directory esista
            self.EXCLUSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(self.EXCLUSIONS_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    {"excluded_matricole": list(self._exclusions)},
                    f,
                    indent=2,
                    ensure_ascii=False,
                )
        except Exception as e:
            print(f"Errore salvataggio esclusioni: {e}")

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)

        # Tree widget configuration
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(self.HEADERS)
        self.tree.setWordWrap(True)
        self.tree.setAlternatingRowColors(True)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tree.setAnimated(True)  # Animazione per expand/collapse

        # Header configuration con larghezza dinamica per evitare troncamenti
        h = self.tree.header()
        # Imposta tutte le colonne a ResizeToContents per adattarsi al contenuto
        for col in range(10):
            h.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        # L'ultima colonna (Stato) può anche espandersi
        h.setStretchLastSection(True)

        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)

        # Stile personalizzato per il tree
        self.tree.setStyleSheet(
            """
            QTreeWidget {
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                background-color: white;
                outline: none;
            }
            QTreeWidget::item {
                padding: 8px 4px;
                border-bottom: 1px solid #f3f4f6;
            }
            QTreeWidget::item:hover {
                background-color: #f9fafb;
            }
            QTreeWidget::item:selected {
                background-color: #e0f2fe;
                color: #0c4a6e;
            }
            QHeaderView::section {
                background-color: #f8fafc;
                padding: 10px 8px;
                border: none;
                border-bottom: 2px solid #e2e8f0;
                border-right: 1px solid #e5e7eb;
                font-weight: bold;
                color: #475569;
            }
        """
        )

        # Toolbar con pulsanti migliorati
        toolbar = QHBoxLayout()

        # Gruppo espansione
        btn_expand = QPushButton("Espandi Tutto")
        btn_expand.setIcon(QIcon(get_asset_path(Icons.FOLDER_OPEN)))
        btn_expand.clicked.connect(self.tree.expandAll)
        btn_expand.setStyleSheet(
            """
            QPushButton {
                padding: 8px 16px;
                background-color: #f1f5f9;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                font-weight: 500;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
        """
        )

        btn_collapse = QPushButton("Comprimi Tutto")
        btn_collapse.setIcon(QIcon(get_asset_path(Icons.FOLDER)))
        btn_collapse.clicked.connect(self.tree.collapseAll)
        btn_collapse.setStyleSheet(
            """
            QPushButton {
                padding: 8px 16px;
                background-color: #f1f5f9;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                font-weight: 500;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
            }
        """
        )

        toolbar.addWidget(btn_expand)
        toolbar.addWidget(btn_collapse)
        toolbar.addSpacing(20)

        # Checkbox per mostrare esclusi
        self.show_excluded_check = QCheckBox("Mostra esclusi")
        self.show_excluded_check.setChecked(False)
        self.show_excluded_check.setStyleSheet(
            """
            QCheckBox {
                padding: 8px 12px;
                font-weight: 500;
                color: #64748b;
            }
            QCheckBox:hover {
                color: #334155;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #cbd5e1;
                border-radius: 4px;
                background: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #3b82f6;
                border-radius: 4px;
                background: #3b82f6;
            }
        """
        )
        self.show_excluded_check.stateChanged.connect(self._on_show_excluded_changed)
        toolbar.addWidget(self.show_excluded_check)

        # Label conteggio esclusi
        self.excluded_count_label = QLabel("")
        self.excluded_count_label.setStyleSheet(
            "color: #94a3b8; font-size: 12px; padding: 0 8px;"
        )
        toolbar.addWidget(self.excluded_count_label)

        toolbar.addStretch()

        # Pulsante analisi con stile migliorato
        self.btn_analyze = QPushButton("Analizza Scadenze")
        self.btn_analyze.setIcon(QIcon(get_asset_path(Icons.BAR_CHART)))
        self.btn_analyze.clicked.connect(self._run_analysis)
        self.btn_analyze.setStyleSheet(
            """
            QPushButton {
                padding: 8px 20px;
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """
        )
        toolbar.addWidget(self.btn_analyze)

        layout.addLayout(toolbar)
        layout.addWidget(self.tree)

    def _on_show_excluded_changed(self, state):
        """Gestisce il cambio di stato della checkbox 'Mostra esclusi'."""
        self._show_excluded = state == Qt.CheckState.Checked.value
        self._apply_exclusion_visibility()

    def _apply_exclusion_visibility(self):
        """Applica la visibilità agli elementi in base allo stato di esclusione."""
        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            matricola = self._extract_matricola_from_parent(parent)
            is_excluded = matricola in self._exclusions

            # Nascondi o mostra in base al flag
            if is_excluded and not self._show_excluded:
                parent.setHidden(True)
            else:
                parent.setHidden(False)

    def _extract_matricola_from_parent(self, parent_item) -> str:
        """Estrae la matricola dal testo del nodo padre."""
        # Il formato è: "matricola  •  costruttore  •  modello  •  days_text"
        text = parent_item.text(0)
        parts = text.split("  •  ")
        if parts:
            return parts[0].strip()
        return ""

    def _update_excluded_count_label(self):
        """Aggiorna la label con il conteggio degli esclusi."""
        count = len(self._exclusions)
        if count > 0:
            self.excluded_count_label.setText(f"({count} esclusi)")
        else:
            self.excluded_count_label.setText("")

    def refresh_data(self):
        """Ricarica i certificati dal database."""
        self._load_data()

    def _load_data(self):
        """Esegue la query e popola l'albero dei certificati raggruppati per matricola con logica intelligente."""
        data = ContabilitaManager.get_certificati_campione_data()
        self.tree.clear()
        self.tree.setSortingEnabled(False)

        # Step 1: Raggruppa per matricola
        matricola_groups = defaultdict(list)
        for r in data:
            matricola = r[self.IDX_MATRICOLA] or "N/D"
            matricola_groups[matricola].append(r)

        # Step 2: Crea una lista di gruppi con metadati per ordinamento
        groups_with_priority = []

        for matricola, certificates in matricola_groups.items():
            # Ordina per data di emissione (più recente in alto)
            def parse_date(cert):
                date_str = cert[self.IDX_EMISSIONE] or ""
                try:
                    if "/" in date_str:
                        return datetime.strptime(date_str, "%d/%m/%Y")
                    return datetime.min
                except Exception:
                    return datetime.min

            certificates_sorted = sorted(certificates, key=parse_date, reverse=True)

            # Step 3: Determina lo stato del certificato più recente (PRIMO della lista)
            latest_cert = certificates_sorted[0]
            modello = latest_cert[self.IDX_MODELLO] or "N/D"
            costruttore = latest_cert[self.IDX_COSTRUTTORE] or "N/D"
            range_strumento = latest_cert[self.IDX_RANGE] or ""

            # Calcola giorni alla scadenza per il certificato più recente
            days_to_expiry, status_dot_icon = self._calculate_days_and_status(
                latest_cert[self.IDX_SCADENZA]
            )

            # Aggiungi alla lista con priorità per ordinamento
            # Priorità: scaduti (negativo) < prossimi alla scadenza (0-15) < medi (16-30) < attivi (>30)
            priority = days_to_expiry if days_to_expiry is not None else 9999
            groups_with_priority.append(
                {
                    "matricola": matricola,
                    "costruttore": costruttore,
                    "modello": modello,
                    "range_strumento": range_strumento,
                    "certificates": certificates_sorted,
                    "days_to_expiry": days_to_expiry,
                    "status_dot_icon": status_dot_icon,
                    "priority": priority,
                }
            )

        # Step 4: Ordina i gruppi per priorità (scaduti prima)
        groups_with_priority.sort(key=lambda x: x["priority"])

        # Step 5: Crea i nodi padre e figli
        for group in groups_with_priority:
            matricola = group["matricola"]
            costruttore = group["costruttore"]
            modello = group["modello"]
            range_strumento = group["range_strumento"]
            certificates_sorted = group["certificates"]
            days_to_expiry = group["days_to_expiry"]
            status_dot_icon = group["status_dot_icon"]

            # Verifica se è escluso
            is_excluded = matricola in self._exclusions

            # Costruisci label padre con icone separator e info giorni
            # Punto 4: Mostra giorni anche quando compresso
            days_text = self._format_days_text_short(days_to_expiry)

            # Per MANOMETRO DIGITALE, aggiungi il range strumento prima dello stato
            is_manometro_digitale = "MANOMETRO DIGITALE" in modello.upper()
            range_part = f"  •  {range_strumento}" if is_manometro_digitale and range_strumento else ""

            # Aggiungi indicatore [ESCLUSO] se necessario
            excluded_marker = "  [ESCLUSO]" if is_excluded else ""
            parent_label = (
                f"{matricola}  •  {costruttore}  •  {modello}{range_part}  •  {days_text}{excluded_marker}"
            )
            parent_item = SortableTreeWidgetItem(self.tree, [parent_label])
            parent_item.setFirstColumnSpanned(True)

            # Pallino di stato sul padre (visibile anche quando compresso)
            # Se escluso, usa pallino grigio
            if is_excluded:
                parent_item.setIcon(0, QIcon(get_asset_path(Icons.STATUS_DOT_GRAY)))
            else:
                parent_item.setIcon(0, QIcon(get_asset_path(status_dot_icon)))

            # Punto 6: Grassetto solo se espanso (inizialmente no)
            # Salviamo lo stato per gestirlo dinamicamente
            parent_item.setData(
                0, Qt.ItemDataRole.UserRole, {"days": days_to_expiry, "matricola": matricola}
            )

            # Styling per elementi esclusi
            if is_excluded:
                font = parent_item.font(0)
                font.setStrikeOut(True)
                parent_item.setFont(0, font)
                parent_item.setForeground(0, QBrush(QColor("#9ca3af")))

            # Step 6: Aggiungi i certificati come figli
            for idx, cert in enumerate(certificates_sorted):
                row_item = SortableTreeWidgetItem(
                    parent_item, [str(x) if x is not None else "" for x in cert]
                )

                # LOGICA INTELLIGENTE:
                # - Il PRIMO certificato (idx == 0) è quello "attivo" con stato reale
                # - TUTTI gli altri (idx > 0) sono STORICO senza alert
                is_current = idx == 0

                if is_current:
                    # Certificato corrente: mostra stato reale con pallino
                    self._apply_current_certificate_styling(
                        row_item, cert, days_to_expiry, status_dot_icon
                    )
                else:
                    # Certificato storico: sempre grigio, nessun alert
                    self._apply_historical_certificate_styling(row_item, cert)

        self.tree.setSortingEnabled(False)  # Disabilita sorting per mantenere ordine
        # IMPORTANTE: Comprimi tutto di default (punto 5)
        self.tree.collapseAll()

        # Applica visibilità esclusioni
        self._apply_exclusion_visibility()
        self._update_excluded_count_label()

        # Connetti segnale per gestire grassetto dinamico (solo se non già connesso)
        try:
            self.tree.itemExpanded.disconnect(self._on_item_expanded)
            self.tree.itemCollapsed.disconnect(self._on_item_collapsed)
        except TypeError:
            pass  # Non era connesso
        self.tree.itemExpanded.connect(self._on_item_expanded)
        self.tree.itemCollapsed.connect(self._on_item_collapsed)

    def _calculate_days_and_status(self, scadenza_str):
        """
        Calcola i giorni alla scadenza e ritorna il pallino di stato appropriato.

        Returns:
            tuple: (giorni_alla_scadenza, icona_pallino)
        """
        try:
            if not scadenza_str or scadenza_str == "":
                return None, Icons.STATUS_DOT_GRAY

            # Parsing data italiana
            scadenza_date = datetime.strptime(scadenza_str, "%d/%m/%Y")
            today = datetime.now()
            delta = scadenza_date - today
            days = delta.days

            # Determina il pallino basato sui giorni
            if days < 0:
                # Scaduto
                return days, Icons.STATUS_DOT_RED
            elif 0 <= days <= 15:
                # Scadenza entro 15 giorni
                return days, Icons.STATUS_DOT_ORANGE
            elif 16 <= days <= 30:
                # Scadenza tra 16-30 giorni
                return days, Icons.STATUS_DOT_YELLOW
            else:
                # Attivo oltre 30 giorni
                return days, Icons.STATUS_DOT_GREEN

        except Exception:
            return None, Icons.STATUS_DOT_GRAY

    def _apply_current_certificate_styling(
        self, item, cert, days_to_expiry, status_dot_icon
    ):
        """Applica styling al certificato CORRENTE (più recente) con stato reale."""
        # Colori e stati basati sui giorni alla scadenza
        # AGGIORNATO: Colori più distintivi per migliore visibilità
        if days_to_expiry is None:
            status_text = "N/D"
            bg_color = QColor("#f3f4f6")
            text_color = QColor("#6b7280")
        elif days_to_expiry < 0:
            # ROSSO SCURO per scaduti
            status_text = f"Scaduto da {abs(days_to_expiry)} giorni"
            bg_color = QColor("#fee2e2")
            text_color = QColor("#dc2626")  # Rosso più scuro
        elif 0 <= days_to_expiry <= 15:
            # ARANCIONE SCURO per urgenza massima (0-15 giorni)
            status_text = f"Scade tra {days_to_expiry} giorni"
            bg_color = QColor("#fed7aa")
            text_color = QColor("#ea580c")  # Arancione scuro distintivo
        elif 16 <= days_to_expiry <= 30:
            # GIALLO CHIARO/BRILLANTE per attenzione (16-30 giorni)
            status_text = f"Scade tra {days_to_expiry} giorni"
            bg_color = QColor("#fef9c3")  # Giallo chiaro nel background
            text_color = QColor("#ca8a04")  # Giallo scuro nel testo per contrasto
        else:
            # VERDE per attivi (>30 giorni)
            status_text = f"Attivo ({days_to_expiry} giorni rimanenti)"
            bg_color = QColor("#d1fae5")
            text_color = QColor("#10b981")

        # Applica background
        for col in range(self.tree.columnCount()):
            item.setBackground(col, QBrush(bg_color))

        # Applica pallino e testo stato
        item.setIcon(self.IDX_STATO, QIcon(get_asset_path(status_dot_icon)))
        item.setText(self.IDX_STATO, status_text)
        item.setForeground(self.IDX_STATO, QBrush(text_color))

        # Punto 6: Font bold per certificato corrente (più recente)
        font = item.font(self.IDX_STATO)
        font.setBold(True)
        item.setFont(self.IDX_STATO, font)

    def _apply_historical_certificate_styling(self, item, cert):
        """Applica styling ai certificati STORICI (nessun alert)."""
        # Background grigio molto chiaro
        bg_color = QColor("#fafafa")
        for col in range(self.tree.columnCount()):
            item.setBackground(col, QBrush(bg_color))

        # Pallino grigio e testo STORICO
        item.setIcon(self.IDX_STATO, QIcon(get_asset_path(Icons.STATUS_DOT_GRAY)))
        item.setText(self.IDX_STATO, "STORICO")
        item.setForeground(self.IDX_STATO, QBrush(QColor("#9ca3af")))

        # Tooltip informativo
        tooltip = "Certificato storico - Esiste un certificato più recente per questa matricola"
        item.setToolTip(self.IDX_STATO, tooltip)

    def _format_days_text_short(self, days):
        """Formatta il testo dei giorni in versione breve per il nodo padre."""
        if days is None:
            return "N/D"
        elif days < 0:
            return f"🔴 Scaduto ({abs(days)}gg fa)"  # Rosso scuro
        elif 0 <= days <= 15:
            return f"🟠 Scade tra {days}gg"  # Arancione scuro (urgente)
        elif 16 <= days <= 30:
            return f"🟡 Scade tra {days}gg"  # Giallo chiaro (attenzione)
        else:
            return f"✅ Attivo ({days}gg rim.)"  # Verde

    def _on_item_expanded(self, item):
        """Gestisce l'evento di espansione: applica grassetto."""
        if item.parent() is None:  # Solo per nodi padre
            font = item.font(0)
            font.setBold(True)
            item.setFont(0, font)

    def _on_item_collapsed(self, item):
        """Gestisce l'evento di compressione: rimuove grassetto."""
        if item.parent() is None:  # Solo per nodi padre
            font = item.font(0)
            font.setBold(False)
            item.setFont(0, font)

    def filter_data(self, text):
        """Filtra l'albero dei certificati in base al testo di ricerca."""
        query = text.lower()
        for i in range(self.tree.topLevelItemCount()):
            parent = self.tree.topLevelItem(i)
            parent_visible = False
            for j in range(parent.childCount()):
                child = parent.child(j)
                match = any(
                    query in child.text(c).lower()
                    for c in range(self.tree.columnCount())
                )
                child.setHidden(not match)
                if match:
                    parent_visible = True
            parent.setHidden(not parent_visible)

    def _show_context_menu(self, pos):
        item = self.tree.itemAt(pos)
        if not item:
            return

        menu = QMenu(self)

        # Determina se è un nodo padre o figlio
        is_parent = item.parent() is None

        if is_parent:
            # Context menu per nodo PADRE (matricola)
            matricola = self._extract_matricola_from_parent(item)
            is_excluded = matricola in self._exclusions

            if is_excluded:
                # Opzione: Includi nel monitoraggio
                include_action = QAction("✅ Includi nel monitoraggio", self)
                include_action.triggered.connect(
                    lambda: self._include_matricola(matricola)
                )
                menu.addAction(include_action)
            else:
                # Opzione: Escludi dal monitoraggio
                exclude_action = QAction("🚫 Escludi dal monitoraggio", self)
                exclude_action.triggered.connect(
                    lambda: self._exclude_matricola(matricola)
                )
                menu.addAction(exclude_action)

            menu.addSeparator()

            # Espandi/Comprimi
            if item.isExpanded():
                collapse_action = QAction("Comprimi", self)
                collapse_action.triggered.connect(lambda: self.tree.collapseItem(item))
                menu.addAction(collapse_action)
            else:
                expand_action = QAction("Espandi", self)
                expand_action.triggered.connect(lambda: self.tree.expandItem(item))
                menu.addAction(expand_action)

        else:
            # Context menu per nodo FIGLIO (certificato)
            # Azione: Apri Certificato
            cert_number = item.text(self.IDX_CERTIFICATO)
            if cert_number:
                open_action = QAction("📄 Apri Certificato", self)
                open_action.triggered.connect(lambda: self._open_certificate(cert_number))
                menu.addAction(open_action)
                menu.addSeparator()

            # Azione: Analizza con Lyra
            lyra_action = QAction("🔍 Analizza con Lyra", self)
            lyra_action.triggered.connect(lambda: self._analyze_item(item))
            menu.addAction(lyra_action)

            menu.addSeparator()

            # Opzione esclusione anche dal figlio (usa la matricola del padre)
            parent_item = item.parent()
            if parent_item:
                matricola = self._extract_matricola_from_parent(parent_item)
                is_excluded = matricola in self._exclusions

                if is_excluded:
                    include_action = QAction("✅ Includi strumento nel monitoraggio", self)
                    include_action.triggered.connect(
                        lambda: self._include_matricola(matricola)
                    )
                    menu.addAction(include_action)
                else:
                    exclude_action = QAction("🚫 Escludi strumento dal monitoraggio", self)
                    exclude_action.triggered.connect(
                        lambda: self._exclude_matricola(matricola)
                    )
                    menu.addAction(exclude_action)

        menu.exec(self.tree.viewport().mapToGlobal(pos))

    def _exclude_matricola(self, matricola: str):
        """Esclude una matricola dal monitoraggio."""
        self._exclusions.add(matricola)
        self._save_exclusions()
        self._load_data()  # Ricarica per aggiornare lo styling

    def _include_matricola(self, matricola: str):
        """Include una matricola nel monitoraggio (rimuove esclusione)."""
        self._exclusions.discard(matricola)
        self._save_exclusions()
        self._load_data()  # Ricarica per aggiornare lo styling

    def _open_certificate(self, cert_number: str):
        """Apre il file PDF del certificato cercandolo ricorsivamente nella root configurata."""
        config = config_manager.load_config()
        cert_root = config.get("certificati_root_path", "")

        if not cert_root or not os.path.exists(cert_root):
            QMessageBox.warning(
                self,
                "Percorso non configurato",
                "Configura il percorso root dei certificati nelle impostazioni.\n"
                "Chiave: certificati_root_path",
            )
            return

        # Cerca il file PDF ricorsivamente
        # Il certificato "016-25" potrebbe essere in "2025/016-25.pdf" o simile
        search_patterns = [
            f"{cert_number}.pdf",
            f"{cert_number}.PDF",
            f"CERTIFICATO {cert_number}.pdf",
            f"certificato {cert_number}.pdf",
        ]

        found_path = None
        for root, dirs, files in os.walk(cert_root):
            for file in files:
                if any(file.lower() == pattern.lower() for pattern in search_patterns):
                    found_path = os.path.join(root, file)
                    break
                # Match parziale: il file contiene il numero certificato
                if cert_number.lower() in file.lower() and file.lower().endswith(".pdf"):
                    found_path = os.path.join(root, file)
                    break
            if found_path:
                break

        if found_path:
            os.startfile(found_path)
        else:
            QMessageBox.warning(
                self,
                "Certificato non trovato",
                f"Impossibile trovare il certificato '{cert_number}' in:\n{cert_root}",
            )

    def _analyze_item(self, item):
        from src.gui.main_window import MainWindow

        mw = self.window()
        if isinstance(mw, MainWindow):
            text = " | ".join(
                [
                    f"{self.HEADERS[c]}: {item.text(c)}"
                    for c in range(self.tree.columnCount())
                ]
            )
            mw.analyze_with_lyra(f"Certificato: {text}")

    def _run_analysis(self):
        # Esegue lo script PowerShell di analisi.
        config = config_manager.load_config()
        path = config.get("certificati_campione_path", "")
        if not path or not os.path.exists(path):
            QMessageBox.warning(
                self,
                "Attenzione",
                "File Certificati Campione non configurato o non trovato.",
            )
            return

        ps_script_template = r"""
# --- Parametri Iniziali ---
$Global:ExcelFilePath = "__FILE_PATH_PLACEHOLDER__"
$Global:SheetName = "strumenti campione ISAB SUD"
$startRow = 9
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type -ReferencedAssemblies System.Windows.Forms, System.Drawing -TypeDefinition @'
    using System;
    using System.Runtime.InteropServices;
    using System.Drawing;
    public class User32 {
        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool PrintWindow(IntPtr hwnd, IntPtr hdcBlt, uint nFlags);
    }
'@
function Show-CustomSummaryBox {
    param ($Title, $Scaduti, $Prossimi, $Oggi, $ExcelPath)
    $form = New-Object System.Windows.Forms.Form
    $form.Text = $Title; $form.Width = 1052; $form.Height = 600; $form.StartPosition = "CenterScreen"
    $rtb = New-Object System.Windows.Forms.RichTextBox
    $rtb.Dock = "Fill"; $rtb.ReadOnly = $true; $rtb.Font = New-Object System.Drawing.Font("Consolas", 10)
    $append = {
        param($Text, $Color = ([System.Drawing.Color]::Black), $Bold = $false)
        $rtb.SelectionStart = $rtb.TextLength
        $rtb.SelectionColor = $Color
        if ($Bold) {
            $fontStyle = [System.Drawing.FontStyle]::Bold
        } else {
            $fontStyle = [System.Drawing.FontStyle]::Regular
        }
        $rtb.SelectionFont = New-Object System.Drawing.Font($rtb.SelectionFont, $fontStyle)
        $rtb.AppendText("$Text`n")
    }
    $btnPanel = New-Object System.Windows.Forms.Panel; $btnPanel.Height = 50; $btnPanel.Dock = "Bottom"
    $closeBtn = New-Object System.Windows.Forms.Button; $closeBtn.Text = "Chiudi"; $closeBtn.Add_Click({ $form.Close() })
    $mailBtn = New-Object System.Windows.Forms.Button; $mailBtn.Text = "Invia Email"; $mailBtn.Width = 120
    $mailBtn.Add_Click({
        $bmp = New-Object System.Drawing.Bitmap($form.Width, $form.Height)
        $g = [System.Drawing.Graphics]::FromImage($bmp); $hdc = $g.GetHdc()
        [User32]::PrintWindow($form.Handle, $hdc, 0x2); $g.ReleaseHdc($hdc); $g.Dispose()
        $p = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), "cert_summary.png")
        $bmp.Save($p, [System.Drawing.Imaging.ImageFormat]::Png); $bmp.Dispose()
        $xl = New-Object -ComObject Excel.Application
        $wb = $xl.Workbooks.Open($ExcelPath)
        $xl.Run("'" + $($wb.Name) + "'!InviaEmailConScreenshotDaPS", $p)
        $wb.Close($false); $xl.Quit(); $form.Close()
    })
    $btnPanel.Controls.AddRange(@($mailBtn, $closeBtn))
    $form.Controls.AddRange(@($rtb, $btnPanel))
    &$append "RIEPILOGO SCADENZE (Analisi: $($Oggi.ToString('dd/MM/yyyy')))" ([System.Drawing.Color]::Black) $true
    if ($Scaduti.Count -gt 0) {
        &$append "--- SCADUTI ($($Scaduti.Count)) ---" ([System.Drawing.Color]::Red) $true
        foreach ($i in $Scaduti) { &$append "ID: $($i.ID) | $($i.Name) | Scad: $($i.Date.ToString('dd/MM/yyyy'))" ([System.Drawing.Color]::Red) }
    }
    if ($Prossimi.Count -gt 0) {
        &$append "--- IN SCADENZA ($($Prossimi.Count)) ---" ([System.Drawing.Color]::DarkOrange) $true
        foreach ($i in $Prossimi) { &$append "ID: $($i.ID) | $($i.Name) | Scad: $($i.Date.ToString('dd/MM/yyyy'))" ([System.Drawing.Color]::DarkOrange) }
    }
    $form.TopMost = $true; $null = $form.ShowDialog(); $form.Dispose()
}
try {
    $xl = New-Object -ComObject Excel.Application; $xl.Visible = $false
    $wb = $xl.Workbooks.Open($Global:ExcelFilePath); $ws = $wb.Sheets.Item($Global:SheetName)
    $last = $ws.Cells($ws.Rows.Count, "X").End(-4162).Row
    $list = New-Object System.Collections.ArrayList; $oggi = (Get-Date).Date
    for ($i = 9; $i -le $last; $i++) {
        if ($ws.Cells($i, "X").Value2 -eq "SI") {
            $null = $list.Add(([PSCustomObject]@{
                Name = $ws.Cells($i, "G").Value2; ID = $ws.Cells($i, "V").Value2
                Date = $oggi.AddDays([double]$ws.Cells($i, "W").Value2)
            }))
        }
    }
    $scad = $list | Where-Object {$_.Date -lt $oggi}
    $prox = $list | Where-Object {$_.Date -ge $oggi -and $_.Date -le $oggi.AddDays(3)}
    $wb.Close($false); $xl.Quit(); [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl)
    Show-CustomSummaryBox "Avviso Scadenze" $scad $prox $oggi $Global:ExcelFilePath
} catch { [System.Windows.Forms.MessageBox]::Show($_.Exception.Message) }
"""
        ps_script = ps_script_template.replace(
            "__FILE_PATH_PLACEHOLDER__", path.replace("\\", "\\\\")
        )
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".ps1", delete=False, encoding="utf-8"
            ) as tmp:
                tmp.write(ps_script)
                tmp_path = tmp.name

            CREATE_NO_WINDOW = 0x08000000
            subprocess.Popen(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", tmp_path],
                creationflags=CREATE_NO_WINDOW,
            )
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile avviare l'analisi:\n{e}")
