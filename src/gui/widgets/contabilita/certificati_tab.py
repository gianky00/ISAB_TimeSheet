import os
import subprocess
import tempfile

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QHeaderView,
    QMenu,
    QMessageBox,
    QPushButton,
    QTreeWidget,
    QVBoxLayout,
    QWidget,
)

from src.core import config_manager
from src.core.contabilita_manager import ContabilitaManager
from src.gui.widgets.contabilita.helpers import SortableTreeWidgetItem


class CertificatiCampioneTab(QWidget):
    """Tab per Certificati Campione (Tree View)."""

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
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(self.HEADERS)
        self.tree.setWordWrap(True)
        self.tree.setAlternatingRowColors(True)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tree.setStyleSheet("""
            QTreeWidget { background-color: white; color: black; font-size: 13px; border: 1px solid #dee2e6; }
            QTreeWidget::item { color: black; padding: 4px; }
            QTreeWidget::item:selected { background-color: #0d6efd; color: white; }
            QTreeWidget::item:focus { background-color: #0d6efd; color: white; }
            QHeaderView::section { background-color: #E1F5FE; color: #333333; padding: 10px 5px; border: none; border-right: 1px solid #B3E5FC; border-bottom: 3px solid #81D4FA; font-weight: bold; text-transform: uppercase; font-size: 11px; }
        """)
        h = self.tree.header()
        h.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.tree.setColumnWidth(0, 200)
        self.tree.setColumnWidth(1, 120)
        self.tree.setColumnWidth(2, 120)
        self.tree.setColumnWidth(3, 120)
        self.tree.setColumnWidth(4, 80)
        self.tree.setColumnWidth(5, 140)
        self.tree.setColumnWidth(6, 120)
        self.tree.setColumnWidth(7, 120)
        self.tree.setColumnWidth(8, 100)
        h.setSectionResizeMode(9, QHeaderView.ResizeMode.Stretch)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)

        toolbar = QHBoxLayout()
        for text, func in [
            ("Espandi Tutto", self.tree.expandAll),
            ("Comprimi Tutto", self.tree.collapseAll),
        ]:
            btn = QPushButton(text)
            btn.clicked.connect(func)
            toolbar.addWidget(btn)
        toolbar.addStretch()
        self.btn_analyze = QPushButton("📊 Analizza")
        self.btn_analyze.clicked.connect(self._run_analysis)
        toolbar.addWidget(self.btn_analyze)
        layout.addLayout(toolbar)
        layout.addWidget(self.tree)

    def refresh_data(self):
        self._load_data()

    def _load_data(self):
        data = ContabilitaManager.get_certificati_campione_data()
        self.tree.clear()
        self.tree.setSortingEnabled(False)
        groups = {}
        for r in data:
            costruttore = r[self.IDX_COSTRUTTORE] or "Altro"
            if costruttore not in groups:
                groups[costruttore] = SortableTreeWidgetItem(self.tree, [costruttore])
                groups[costruttore].setFirstColumnSpanned(True)
            row_item = SortableTreeWidgetItem(
                groups[costruttore], [str(x) if x is not None else "" for x in r]
            )
            status = r[self.IDX_STATO]
            if status == "SCADUTO":
                row_item.setBackground(self.IDX_STATO, Qt.GlobalColor.red)
            elif status == "IN SCADENZA":
                row_item.setBackground(self.IDX_STATO, Qt.GlobalColor.yellow)
        self.tree.setSortingEnabled(True)
        self.tree.sortByColumn(self.IDX_SCADENZA, Qt.SortOrder.AscendingOrder)

    def filter_data(self, text):
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
        if not item or item.parent() is None:
            return
        menu = QMenu(self)
        menu.addAction(QAction("✨ Analizza con Lyra", self)).triggered.connect(
            lambda: self._analyze_item(item)
        )
        menu.exec(self.tree.viewport().mapToGlobal(pos))

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

            subprocess.Popen(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", tmp_path],
                shell=True,
            )
        except Exception as e:
            QMessageBox.critical(self, "Errore", f"Impossibile avviare l'analisi:\n{e}")
