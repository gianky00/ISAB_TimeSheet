# ruff: noqa: E402
import json
import os
import shutil
import sys
import time
import tkinter as tk
from datetime import datetime
from tkinter import scrolledtext, ttk

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Setup path per import interni
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core import config_manager
from src.core.constants import URLs

# --- CONFIGURAZIONE ---
ADMIN_DIR = os.path.dirname(os.path.abspath(__file__))
INSPECTOR_DIR = os.path.join(ADMIN_DIR, "log_inspector")
MANIFEST_FILE = os.path.join(INSPECTOR_DIR, "workflow_manifest.json")

URL_MAP = {
    "Portale Fornitori": URLs.ISAB_PORTAL,
    "Safework": "https://safework.isab.com/",
    "Google (Test)": "https://www.google.com",
}


class BotArchitect:
    """
    Automated inspector tool for capturing web application states and DOM structures.
    Used for creating datasets for AI training or debugging Selenium workflows.
    """

    def __init__(self):
        self.driver = None
        self.config = config_manager.load_config()
        self.state_counter = 0
        self.action_counter = 0
        self.last_state_folder = "Nessuno"
        self.workflow = []
        self.prepare_environment()

    def prepare_environment(self):
        """Prepara la cartella log_inspector pulendo sessioni precedenti."""
        if os.path.exists(INSPECTOR_DIR):
            shutil.rmtree(INSPECTOR_DIR)
        os.makedirs(INSPECTOR_DIR)
        self.log_to_console(
            "🚀 ISPETTORE PRONTO. Cartella log_inspector inizializzata."
        )

    def log_to_console(self, text):
        """Logs message to console with timestamp."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {text}")

    def get_user_choice(self):
        """Launches a Tkinter GUI to select the target portal and configuration."""
        root = tk.Tk()
        # ... (tkinter code unchanged)
        root.title("Universal Inspector - Setup")
        root.geometry("600x500")
        root.attributes("-topmost", True)

        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # --- TAB 1: SETUP ---
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text=" ⚙️ Setup ")

        ttk.Label(
            config_frame, text="Inizia Sessione di Analisi", font=("Arial", 12, "bold")
        ).pack(pady=20)

        selected_url = tk.StringVar()
        ttk.Label(config_frame, text="Seleziona Portale Target:").pack(pady=5)
        combo = ttk.Combobox(
            config_frame, textvariable=selected_url, state="readonly", width=40
        )
        combo["values"] = list(URL_MAP.keys())
        combo.current(0)
        combo.pack(pady=5)

        ttk.Label(
            config_frame, text="Output: admin/log_inspector/", foreground="blue"
        ).pack(pady=10)

        def on_confirm():
            root.quit()
            root.destroy()

        ttk.Button(config_frame, text="🚀 AVVIA ISPEZIONE", command=on_confirm).pack(
            side="bottom", pady=30
        )

        # --- TAB 2: GUIDA ---
        guide_frame = ttk.Frame(notebook)
        notebook.add(guide_frame, text=" 📖 Guida ")

        guide_text = scrolledtext.ScrolledText(
            guide_frame, wrap=tk.WORD, font=("Consolas", 10)
        )
        guide_text.pack(expand=True, fill="both", padx=5, pady=5)

        instructions = """
=== GUIDA ALL'USO DELL'ISPETTORE ===

1. LOG_INSPECTOR
   Tutti i dati vengono salvati in admin/log_inspector/.
   La cartella viene pulita ad ogni nuovo avvio dello script.

2. COMANDI IN CONSOLE
   Mentre navighi nel browser, usa questi comandi nel terminale:

   A) 's [Nome]' -> SNAPSHOT DI STATO
      Esegui questo comando ogni volta che cambi pagina o apri un popup.
      Esempio: > s Pagina_Ricerca
      Salva: Screenshot, HTML e Mappa JSON in una sottocartella dedicata.

   B) 'Azione' -> REGISTRA AZIONE
      Se stai compilando campi sulla stessa pagina, scrivi cosa fai.
      Esempio: > Inserisco codice 5000123
      Registra l'azione nel manifest senza creare nuovi file pesanti.

   C) 'q' -> ESCI E SALVA
      Conclude la sessione di lavoro.

3. SOTTOCARTELLE
   Per ogni snapshot 's', verrà creata una cartella debug_N_Nome
   contenente screenshot e dati tecnici per l'IA.
"""
        guide_text.insert(tk.INSERT, instructions)
        guide_text.configure(state="disabled")

        root.mainloop()
        return selected_url.get(), URL_MAP.get(selected_url.get())

    def init_driver(self):
        """Initializes the Chrome WebDriver with anti-detection options."""
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=chrome_options)

    def auto_login(self, portal_name, url):
        """Performs automatic login to the selected portal using credentials from config."""
        self.driver.get(url)
        accounts = (
            self.config.get("accounts", [])
            if portal_name != "Safework"
            else self.config.get("safework_accounts", [])
        )
        acc = next(
            (a for a in accounts if a.get("default")), accounts[0] if accounts else None
        )
        if not acc:
            return
        u, p = acc.get("username"), acc.get("password")
        try:
            if portal_name == "Safework":
                WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[@class='ms-choice']")
                    )
                ).click()
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//span[normalize-space()='ISAB Sud']")
                    )
                ).click()
                self.driver.find_element(By.ID, "inpUtente").send_keys(u)
                self.driver.find_element(By.ID, "inpPassword").send_keys(p)
                self.driver.find_element(By.ID, "btnLogin").click()
            else:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.NAME, "Username"))
                ).send_keys(u)
                self.driver.find_element(By.NAME, "Password").send_keys(p)
                btn = self.driver.find_element(By.XPATH, "//span[text()='Accedi']")
                self.driver.execute_script("arguments[0].click();", btn)
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[text()='Si']"))
                    ).click()
                except Exception:
                    pass
            self.log_to_console(f"✅ Login automatico: {u}")
        except Exception:
            pass

    def capture_state(self, state_name):
        """
        Captures the current browser state (Screenshot, DOM, JSON mapping).
        Creates a new directory in log_inspector for the snapshot.
        """
        self.state_counter += 1
        folder_name = f"debug_{self.state_counter}_{state_name.replace(' ', '_')}"
        state_path = os.path.join(INSPECTOR_DIR, folder_name)
        os.makedirs(state_path)

        self.log_to_console(f"📸 SNAPSHOT {self.state_counter}: {state_name}")
        self.driver.save_screenshot(os.path.join(state_path, "view.png"))
        with open(
            os.path.join(state_path, "structure.html"), "w", encoding="utf-8"
        ) as f:
            f.write(self.driver.page_source)

        elements = self.driver.execute_script(self._get_ultimate_scanner_js())
        with open(os.path.join(state_path, "mapping.json"), "w", encoding="utf-8") as f:
            json.dump(
                {
                    "context": state_name,
                    "url": self.driver.current_url,
                    "elements": elements,
                },
                f,
                indent=4,
            )

        self.last_state_folder = folder_name
        self._record_entry("STATE_CHANGE", state_name, folder_name)

    def record_action(self, action_desc):
        """Records a user action (text description) into the workflow manifest."""
        self.action_counter += 1
        self.log_to_console(f"📝 AZIONE {self.action_counter}: {action_desc}")
        self._record_entry("ACTION", action_desc, self.last_state_folder)

    def _record_entry(self, entry_type, description, ref_state):
        """Helper to append an entry to the workflow JSON list."""
        self.workflow.append(
            {
                "order": len(self.workflow) + 1,
                "type": entry_type,
                "description": description,
                "reference_state": ref_state,
                "url": self.driver.current_url,
                "timestamp": datetime.now().isoformat(),
            }
        )
        with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
            json.dump(self.workflow, f, indent=4)

    def _get_ultimate_scanner_js(self):
        """Returns the JS code for deep DOM scanning and element extraction."""
        return r"""
            function scan(root = document, framePath = "root") {
                let results = [];
                const selectors = "input, button, textarea, select, a, iframe, [role='button'], .x-btn, .x-action-col-icon, svg, [onclick]";
                function getMeta(el) {
                    const rect = el.getBoundingClientRect();
                    function getXPath(element) {
                        if (element.id && !element.id.includes('ext-')) return 'id("' + element.id + '")';
                        if (element === document.body) return 'body';
                        var ix = 0; var siblings = element.parentNode.childNodes;
                        for (var i = 0; i < siblings.length; i++) {
                            var sibling = siblings[i];
                            if (sibling === element) return getXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
                            if (sibling.nodeType === 1 && sibling.tagName === element.tagName) ix++;
                        }
                    }
                    return {
                        tag: el.tagName.toLowerCase(), name: el.getAttribute('name'), id: el.id,
                        data_id: el.getAttribute('data-componentid'), qtip: el.getAttribute('data-qtip'),
                        text: el.innerText.trim().substring(0, 100), value: el.value,
                        visible: !!(el.offsetWidth || el.offsetHeight), xpath: getXPath(el),
                        frame: framePath, row_ctx: (el.closest('tr') || el.closest('.x-grid-row') || {innerText: ""}).innerText.split('\n').join(' ').substring(0, 150),
                        rect: {x: rect.left, y: rect.top, w: rect.width, h: rect.height}
                    };
                }
                root.querySelectorAll(selectors).forEach(el => {
                    if (el.offsetWidth > 0 || el.offsetHeight > 0) results.push(getMeta(el));
                    if (el.shadowRoot) results = results.concat(scan(el.shadowRoot, framePath + " > shadow"));
                });
                return results;
            }
            return scan();
        """

    def run(self):
        """
        Main execution loop.
        Initializes driver, performs login, and enters interactive command loop.
        """
        name, url = self.get_user_choice()
        self.init_driver()
        self.auto_login(name, url)

        print("\n" + "═" * 60)
        print(" 🕵️  UNIVERSAL INSPECTOR - ACTIVE")
        print(f" 📂  DESTINAZIONE: {INSPECTOR_DIR}")
        print("─" * 60)
        print(" Comandi:")
        print("  's Nome' -> Snapshot STATO (Nuova Vista)")
        print("  'Testo'  -> Descrivi AZIONE (es. Clicco Cerca)")
        print("  'q'      -> Fine Sessione")
        print("═" * 60 + "\n")

        try:
            time.sleep(2)
            self.capture_state("Landing_Page")
            while True:
                cmd = input(f"[{self.last_state_folder}] > ").strip()
                if cmd.lower() == "q":
                    break
                if cmd.lower().startswith("s "):
                    self.capture_state(cmd[2:].strip())
                else:
                    self.record_action(cmd)
            self.log_to_console(f"✅ SESSIONE COMPLETATA. Cartella: {INSPECTOR_DIR}")
        except KeyboardInterrupt:
            pass
        finally:
            if self.driver:
                self.driver.quit()


if __name__ == "__main__":
    BotArchitect().run()
