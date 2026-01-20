"""
SyncroJob - Architecture Generator
Genera il diagramma dell'architettura dell'applicazione.
Richiede Graphviz installato nel sistema (https://graphviz.org/download/).
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
from diagrams.generic.database import SQL
from diagrams.generic.device import Tablet
from diagrams.generic.network import Firewall
from diagrams.onprem.client import User
from diagrams.programming.language import Python

# Percorso di output
OUTPUT_DIR = Path(__file__).parent / "assets"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = "architecture"

# Cambia directory di lavoro per salvare l'output correttamente
os.chdir(OUTPUT_DIR)

graph_attr = {"fontsize": "20", "bgcolor": "transparent"}

with Diagram(
    "SyncroJob Enterprise Architecture",
    show=False,
    filename=OUTPUT_FILE,
    direction="TB",
    graph_attr=graph_attr,
):
    user = User("Operatore COEMI")

    with Cluster("SyncroJob Application (PyQt6)"):
        with Cluster("Core Engine"):
            core = Python("Core Logic")
            db = SQL("Local Cache\n(Audit / Data)")
            config = Python("Config Manager")

        with Cluster("GUI Panels"):
            gui = Tablet("Main Window")
            notif = Python("Notifications")
            audit_ui = Python("Audit Dashboard")

        with Cluster("Automation Bots (Selenium)"):
            scheduler = Python("Autopilot\nScheduler")
            isab_bot = Python("ISAB Portal Bot")
            safework_bot = Python("SafeWork Bot")

    with Cluster("External Systems"):
        isab_ext = Firewall("ISAB Supplier\nPortal")
        safework_ext = Firewall("SafeWork\nPortal")

    # Connections
    user >> Edge(label="Interazione UI", color="blue") >> gui
    gui >> core
    core >> db
    core >> config

    gui >> scheduler
    scheduler >> isab_bot
    scheduler >> safework_bot

    isab_bot >> Edge(label="Automation", color="red", style="dashed") >> isab_ext
    (
        safework_bot
        >> Edge(label="Automation", color="red", style="dashed")
        >> safework_ext
    )

    isab_bot >> Edge(label="Data Sync", color="green") >> db
    safework_bot >> Edge(label="Data Sync", color="green") >> db

print(f"✅ Architettura generata in: {OUTPUT_DIR / OUTPUT_FILE}.png")
