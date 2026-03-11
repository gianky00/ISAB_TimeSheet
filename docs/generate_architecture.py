"""
SyncroJob - Architecture Generator (V2.2 - High Resolution & Clean Layout)
Genera il diagramma dell'architettura enterprise in alta risoluzione (300 DPI).
"""

import os
import sys
from pathlib import Path

# Aggiunge Graphviz al PATH se su Windows
if sys.platform == "win32":
    graphviz_path = r"C:\Program Files\Graphviz\bin"
    if graphviz_path not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + graphviz_path

from diagrams import Cluster, Diagram, Edge
from diagrams.generic.compute import Rack
from diagrams.generic.database import SQL
from diagrams.generic.device import Tablet
from diagrams.generic.network import Firewall
from diagrams.generic.storage import Storage
from diagrams.onprem.client import User
from diagrams.programming.language import Python
from diagrams.saas.chat import Telegram

# Percorso di output
OUTPUT_DIR = Path(__file__).parent / "assets"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = "architecture"

# Cambia directory di lavoro
os.chdir(OUTPUT_DIR)

# Attributi Graphviz per Alta Risoluzione e Spaziamento
graph_attr = {
    "fontsize": "32",
    "bgcolor": "white",
    "fontname": "Verdana Bold",
    "pad": "2.0",
    "nodesep": "1.8",  # Distanza orizzontale tra i nodi
    "ranksep": "2.5",  # Distanza verticale tra i livelli
    "dpi": "300",  # Alta risoluzione
    "splines": "curved",  # Linee curve eleganti
    "concentrate": "true",  # Unisce linee sovrapposte
    "compound": "true",
}

node_attr = {
    "fontsize": "14",
    "fontname": "Verdana",
}

with Diagram(
    "SyncroJob Enterprise Architecture v1.29",
    show=False,
    filename=OUTPUT_FILE,
    direction="TB",
    graph_attr=graph_attr,
    node_attr=node_attr,
):
    user = User("Operatore COEMI")
    tg_ext = Telegram("Telegram App")
    excel_legacy = Storage("Legacy Excel\n(.xlsm / .xlsx)")

    with Cluster("SyncroJob Enterprise Ecosystem"):
        with Cluster("GUI Application (PyQt6)"):
            gui = Tablet("Main Dashboard")
            gui_components = [Python("KPI & Stats"), Python("Lyra AI Panel"), Python("Consuntivi View")]
            notif = Python("Toast Notifications")

        with Cluster("Core Engine & Services"):
            core = Python("Core Logic")
            security = Rack("SecretsManager\n(Keyring)")
            excel_eng = Python("Excel Engine")
            sync_tracker = Python("SyncTracker")
            health = Python("Backup & Telemetry")

        with Cluster("Communication & Intelligence"):
            tg_bridge = Python("Telegram Bridge")
            lyra_client = Python("Lyra AI Client")

        with Cluster("Automation Engine (Selenium)"):
            autopilot = Python("Autopilot\nScheduler")
            isab_bots = Python("ISAB Bots\n(TS/ODA)")
            safework_bots = Python("SafeWork Bots\n(PDL)")

        with Cluster("Persistence Layer"):
            db_main = SQL("Main Data (SQLite)")
            db_audit = SQL("Audit (History)")

        reports = Storage("Output Reports\n(Excel / PDF)")

    with Cluster("External Infrastructure"):
        isab_ext = Firewall("ISAB Portal")
        safework_ext = Firewall("SafeWork Portal")
        ai_service = Rack("AI Services")

    # Connections
    user >> Edge(label="User Interaction", color="blue", penwidth="2.0") >> gui
    gui >> core

    # Core Data Flow
    core >> excel_eng
    excel_eng << Edge(label="Import", color="orange", style="dashed") << excel_legacy
    excel_eng >> Edge(label="Export", color="orange") >> reports

    core >> db_main
    core >> db_audit
    core >> security
    core >> sync_tracker
    core >> health

    # Automation Flow
    gui >> autopilot
    autopilot >> isab_bots
    autopilot >> safework_bots

    isab_bots >> Edge(label="Sync", color="green", penwidth="1.5") >> db_main
    safework_bots >> Edge(label="Sync", color="green", penwidth="1.5") >> db_main

    isab_bots >> Edge(label="Bot Action", color="red", style="dashed") >> isab_ext
    safework_bots >> Edge(label="Bot Action", color="red", style="dashed") >> safework_ext

    # AI & Comms Flow
    lyra_client >> Edge(label="AI Sync", color="purple") >> ai_service
    lyra_client >> core

    tg_bridge >> Edge(label="Telegram Sync", color="cyan", penwidth="2.0") >> tg_ext
    tg_bridge >> core

print(f"✅ Architettura High-Res v1.29 generata in: {OUTPUT_DIR / OUTPUT_FILE}.png")
