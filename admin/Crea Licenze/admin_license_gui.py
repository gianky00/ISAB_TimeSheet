"""
Bot TS - License Generator (Admin Tool)
Genera file di licenza per i client.
"""

import base64
import contextlib
import hashlib
import json
import shutil
import subprocess
import sys
import tkinter as tk
from datetime import date, timedelta
from pathlib import Path
from tkinter import messagebox, simpledialog, ttk

from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Add project root to sys.path to allow importing src modules
current_dir = Path(__file__).parent.resolve()
project_root = current_dir.parent.parent
sys.path.insert(0, str(project_root))

# Carica variabili d'ambiente
load_dotenv()

# Path per il file clienti
CLIENTS_FILE = current_dir / "clients.json"


def derive_license_key(hw_id: str) -> bytes:
    """
    Deriva la chiave di cifratura dall'Hardware ID utilizzando la stessa logica del client.
    Garantisce che la chiave sia esattamente 32 byte url-safe base64-encoded.
    """
    from cryptography.hazmat.primitives import hashes  # noqa: PLC0415
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC  # noqa: PLC0415

    # Pulisce l'Hardware ID (rimuove spazi e punti finali)
    clean_hwid = hw_id.strip().rstrip(".")
    if not clean_hwid:
        raise ValueError("Hardware ID vuoto")  # noqa: TRY003

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"SyncroJob_Grace_Salt_2026",
        iterations=480000,
    )
    # Deriva la chiave grezza (32 byte)
    raw_key = kdf.derive(clean_hwid.encode("utf-8"))

    # Converte in Base64 URL-safe (44 byte) come richiesto da Fernet
    return base64.urlsafe_b64encode(raw_key)


def _calculate_sha256(filepath):  # noqa: ANN001, ANN202
    """Calcola l'hash SHA256 di un file."""
    sha256_hash = hashlib.sha256()
    with Path(filepath).open("rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def load_clients():  # noqa: ANN201
    """Carica i clienti dal file JSON."""
    if CLIENTS_FILE.exists():
        with contextlib.suppress(Exception), CLIENTS_FILE.open(encoding="utf-8") as f:
            return json.load(f)
    # Default clients
    return {
        "PC_COEMI_GIGLIUTO": "0026_B768_5B05_C4F5",
        "PC_ALLEGRETTI_COEMI": "ACE4_2E00_951D_4DDA",
    }


def save_clients(clients):  # noqa: ANN001, ANN201
    """Salva i clienti nel file JSON."""
    with CLIENTS_FILE.open("w", encoding="utf-8") as f:
        json.dump(clients, f, indent=2, ensure_ascii=False)


class LicenseAdminApp:
    """Applicazione GUI per la generazione e gestione delle licenze software SyncroJob."""

    def __init__(self, root: tk.Tk):  # noqa: ANN204, PLR0915
        """Inizializza l'interfaccia grafica e carica il database clienti locale."""
        self.root = root
        self.root.title("SyncroJob - Gestore Licenze (Admin)")
        self.root.geometry("700x720")
        self.root.resizable(False, False)

        # Carica clienti
        self.clients = load_clients()

        # Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"))
        style.configure("Small.TButton", font=("Segoe UI", 9))

        # Header
        header_frame = ttk.Frame(root)
        header_frame.pack(fill="x", pady=15)
        ttk.Label(header_frame, text="🔑 Generatore Licenza SyncroJob", style="Header.TLabel").pack()

        # === Sezione Clienti Salvati ===
        clients_frame = ttk.LabelFrame(root, text="📋 Clienti Salvati", padding=10)
        clients_frame.pack(fill="x", padx=20, pady=5)

        # ComboBox clienti
        combo_frame = ttk.Frame(clients_frame)
        combo_frame.pack(fill="x", pady=5)

        ttk.Label(combo_frame, text="Seleziona Cliente:").pack(side="left")

        self.client_var = tk.StringVar()
        self.cmb_clients = ttk.Combobox(
            combo_frame,
            textvariable=self.client_var,
            values=list(self.clients.keys()),
            state="readonly",
            width=30,
        )
        self.cmb_clients.pack(side="left", padx=(10, 5))
        self.cmb_clients.bind("<<ComboboxSelected>>", self.on_client_selected)

        # Pulsanti gestione clienti
        ttk.Button(combo_frame, text="➕ Aggiungi", command=self.add_client, width=10).pack(
            side="left", padx=2
        )

        ttk.Button(combo_frame, text="✏️ Modifica", command=self.edit_client, width=10).pack(
            side="left", padx=2
        )

        ttk.Button(combo_frame, text="🗑️ Elimina", command=self.delete_client, width=10).pack(
            side="left", padx=2
        )

        # Main container
        frm = ttk.LabelFrame(root, text="Dati Licenza", padding=20)
        frm.pack(fill="both", expand=True, padx=20, pady=5)

        # Hardware ID
        ttk.Label(frm, text="Hardware ID (Seriale Disco):").pack(anchor="w")

        hw_frame = ttk.Frame(frm)
        hw_frame.pack(fill="x", pady=5)

        self.ent_disk = ttk.Entry(hw_frame, width=50)
        self.ent_disk.pack(side="left", fill="x", expand=True)

        ttk.Button(hw_frame, text="📋 Incolla", command=self.paste_disk, width=10).pack(
            side="right", padx=(5, 0)
        )

        # Nome Cliente
        ttk.Label(frm, text="Nome Cliente (riferimento):").pack(anchor="w", pady=(15, 0))
        self.ent_name = ttk.Entry(frm, width=60)
        self.ent_name.pack(fill="x", pady=5)

        # Scadenza
        ttk.Label(frm, text="Data Scadenza:").pack(anchor="w", pady=(15, 0))

        date_frame = ttk.Frame(frm)
        date_frame.pack(fill="x", pady=5)

        self.ent_date = ttk.Entry(date_frame, width=15)
        self.ent_date.pack(side="left")

        # Quick date buttons
        ttk.Button(
            date_frame,
            text="1 Anno",
            width=8,
            command=lambda: self.set_expiry_days(365),
        ).pack(side="left", padx=(10, 2))

        ttk.Button(
            date_frame,
            text="6 Mesi",
            width=8,
            command=lambda: self.set_expiry_days(180),
        ).pack(side="left", padx=2)

        ttk.Button(date_frame, text="3 Mesi", width=8, command=lambda: self.set_expiry_days(90)).pack(
            side="left", padx=2
        )

        ttk.Button(date_frame, text="1 Mese", width=8, command=lambda: self.set_expiry_days(30)).pack(
            side="left", padx=2
        )

        # Default: 1 mese
        self.set_expiry_days(30)

        # Checkbox per upload GitHub
        self.upload_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            frm,
            text="⬆️ Carica automaticamente su GitHub (intelleo-licenses)",
            variable=self.upload_var,
        ).pack(anchor="w", pady=(15, 0))

        # Info box
        info_frame = ttk.LabelFrame(frm, text="ℹ️ Info", padding=10)
        info_frame.pack(fill="x", pady=(15, 0))

        info_text = (
            "I file generati saranno:\n"
            "• config.dat - Dati licenza cifrati\n"
            "• manifest.json - Checksum integrità\n\n"
            "Repository: github.com/gianky00/intelleo-licenses/tree/main/licenses/{HW_ID}/"
        )
        ttk.Label(info_frame, text=info_text, justify="left").pack(anchor="w")

        # Generate button
        self.btn_gen = ttk.Button(
            root,
            text="🔐 GENERA FILE LICENZA",
            command=self.generate,
            style="Accent.TButton",
        )
        self.btn_gen.pack(fill="x", padx=20, pady=20, ipady=12)

    def refresh_clients_combo(self):  # noqa: ANN201
        """Aggiorna la ComboBox dei clienti."""
        self.cmb_clients["values"] = list(self.clients.keys())

    def on_client_selected(self, event=None):  # noqa: ANN001, ANN201
        """Callback quando viene selezionato un cliente."""
        client_name = self.client_var.get()
        if client_name and client_name in self.clients:
            hw_id = self.clients[client_name]
            self.ent_disk.delete(0, tk.END)
            self.ent_disk.insert(0, hw_id)
            self.ent_name.delete(0, tk.END)
            self.ent_name.insert(0, client_name)

    def add_client(self):  # noqa: ANN201
        """Aggiunge un nuovo cliente."""
        name = simpledialog.askstring("Nuovo Cliente", "Nome cliente:", parent=self.root)
        if not name:
            return

        hw_id = simpledialog.askstring("Nuovo Cliente", f"Hardware ID per '{name}':", parent=self.root)
        if not hw_id:
            return

        self.clients[name] = hw_id.strip()
        save_clients(self.clients)
        self.refresh_clients_combo()
        self.client_var.set(name)
        self.on_client_selected()
        messagebox.showinfo("Successo", f"Cliente '{name}' aggiunto!")

    def edit_client(self):  # noqa: ANN201
        """Modifica il cliente selezionato."""
        old_name = self.client_var.get()
        if not old_name:
            messagebox.showwarning("Attenzione", "Seleziona prima un cliente!")
            return

        new_name = simpledialog.askstring(
            "Modifica Cliente",
            "Nome cliente:",
            initialvalue=old_name,
            parent=self.root,
        )
        if not new_name:
            return

        new_hw_id = simpledialog.askstring(
            "Modifica Cliente",
            f"Hardware ID per '{new_name}':",
            initialvalue=self.clients.get(old_name, ""),
            parent=self.root,
        )
        if not new_hw_id:
            return

        # Rimuovi vecchio se nome cambiato
        if old_name != new_name and old_name in self.clients:
            del self.clients[old_name]

        self.clients[new_name] = new_hw_id.strip()
        save_clients(self.clients)
        self.refresh_clients_combo()
        self.client_var.set(new_name)
        self.on_client_selected()
        messagebox.showinfo("Successo", f"Cliente '{new_name}' modificato!")

    def delete_client(self):  # noqa: ANN201
        """Elimina il cliente selezionato."""
        name = self.client_var.get()
        if not name:
            messagebox.showwarning("Attenzione", "Seleziona prima un cliente!")
            return

        if messagebox.askyesno("Conferma", f"Eliminare il cliente '{name}'?", parent=self.root):
            del self.clients[name]
            save_clients(self.clients)
            self.refresh_clients_combo()
            self.client_var.set("")
            self.ent_disk.delete(0, tk.END)
            self.ent_name.delete(0, tk.END)
            messagebox.showinfo("Successo", f"Cliente '{name}' eliminato!")

    def paste_disk(self):  # noqa: ANN201
        """Incolla dagli appunti."""
        with contextlib.suppress(Exception):
            self.ent_disk.delete(0, tk.END)
            self.ent_disk.insert(0, self.root.clipboard_get().strip())

    def set_expiry_days(self, days):  # noqa: ANN001, ANN201
        """Imposta la data di scadenza."""
        expiry = (date.today() + timedelta(days=days)).strftime("%Y-%m-%d")
        self.ent_date.delete(0, tk.END)
        self.ent_date.insert(0, expiry)

    def _get_git_binary(self):  # noqa: ANN202
        """Trova il percorso dell'eseguibile git."""
        import shutil  # noqa: PLC0415

        git_path = shutil.which("git")
        if git_path:
            return git_path

        # Fallback per percorsi comuni se non è nel PATH
        common_paths = [
            r"C:\Program Files\Git\cmd\git.exe",
            r"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\CommonExtensions\Microsoft\TeamFoundation\Team Explorer\Git\cmd\git.exe",
            r"C:\Program Files\Git\bin\git.exe",
        ]
        for p in common_paths:
            if Path(p).exists():
                return p
        return "git"  # Speriamo nel meglio

    def upload_to_github(self, hw_id, target_dir):  # noqa: ANN001, ANN201
        """Carica i file su GitHub usando gh CLI."""
        try:
            # Trova l'eseguibile git
            git_bin = self._get_git_binary()

            # Path del repository locale (da clonare se non esiste)
            repo_name = "gianky00/intelleo-licenses"
            temp_repo_dir = current_dir / "_intelleo-licenses"

            # Clone o pull del repository
            if temp_repo_dir.exists():
                # Pull latest
                subprocess.run(
                    [git_bin, "-C", str(temp_repo_dir), "pull", "--rebase"],
                    check=True,
                    capture_output=True,
                )
            else:
                # Clone
                subprocess.run(
                    ["gh", "repo", "clone", repo_name, str(temp_repo_dir)],
                    check=True,
                    capture_output=True,
                )

            # Cartella destinazione nel repo
            license_dir = temp_repo_dir / "licenses" / hw_id
            license_dir.mkdir(parents=True, exist_ok=True)

            # Copia i file
            target_path = Path(target_dir)
            shutil.copy2(target_path / "config.dat", license_dir)
            shutil.copy2(target_path / "manifest.json", license_dir)

            # Git add, commit, push
            subprocess.run(
                [git_bin, "-C", str(temp_repo_dir), "add", "."],
                check=True,
                capture_output=True,
            )

            commit_msg = f"Update license for {hw_id}"
            subprocess.run(
                [git_bin, "-C", str(temp_repo_dir), "commit", "-m", commit_msg],
                check=True,
                capture_output=True,
            )

            subprocess.run(
                [git_bin, "-C", str(temp_repo_dir), "push"],
                check=True,
                capture_output=True,
            )

            return True, "Upload completato con successo!"  # noqa: TRY300

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            # Se "nothing to commit" non è un errore vero
            if "nothing to commit" in error_msg:
                return True, "File già aggiornati (nessuna modifica)"
            return False, f"Errore git: {error_msg}"
        except Exception as e:
            return False, f"Errore: {e!s}"

    def generate(self):  # noqa: ANN201, PLR0915
        """Genera i file di licenza."""
        disk_serial = self.ent_disk.get().strip()
        client_name = self.ent_name.get().strip()
        expiry = self.ent_date.get().strip()

        # Validazione
        if not disk_serial:
            messagebox.showerror("Errore", "Hardware ID è obbligatorio!")
            return

        if not client_name:
            client_name = disk_serial[:20]  # Fallback

        # Pulisci HW_ID (rimuovi punto finale se presente)
        hw_id = disk_serial.strip().rstrip(".")

        # --- NUOVA LOGICA: Derivazione Chiave specifica per questo HWID ---
        try:
            # Usa la funzione locale auto-contenuta
            license_key = derive_license_key(hw_id)
        except Exception as ke:
            messagebox.showerror("Errore Crittografia", f"Impossibile generare la chiave: {ke}")
            return
        # -----------------------------------------------------------------

        # Pulisci nome per cartella
        folder_name = (
            "".join(c for c in client_name if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
        )

        # Paths
        base_output = Path(__file__).parent.resolve()
        client_dir = base_output / folder_name
        target_dir = client_dir / "Licenza"

        try:
            # Crea/pulisci cartella
            if target_dir.exists():
                shutil.rmtree(target_dir)
            target_dir.mkdir(parents=True, exist_ok=True)

            # Formatta data
            try:
                expiry_obj = date.fromisoformat(expiry)
                expiry_str = expiry_obj.strftime("%d/%m/%Y")
            except ValueError:
                expiry_str = expiry

            gen_date_str = date.today().strftime("%d/%m/%Y")

            # Payload licenza
            payload = {
                "Hardware ID": hw_id,
                "Scadenza Licenza": expiry_str,
                "Generato il": gen_date_str,
                "Cliente": client_name,
                "Applicazione": "SyncroJob",
            }

            # Cifra payload
            json_payload = json.dumps(payload, indent=2).encode("utf-8")
            cipher = Fernet(license_key)
            encrypted_data = cipher.encrypt(json_payload)

            # Scrivi config.dat
            config_path = target_dir / "config.dat"
            config_path.write_bytes(encrypted_data)

            # Genera manifest
            manifest = {
                "config.dat": _calculate_sha256(config_path),
                "generated": gen_date_str,
                "client": client_name,
            }

            manifest_path = target_dir / "manifest.json"
            manifest_path.write_text(json.dumps(manifest, indent=4), encoding="utf-8")

            # Salva/aggiorna cliente nella memoria
            if client_name not in self.clients or self.clients.get(client_name) != hw_id:
                self.clients[client_name] = hw_id
                save_clients(self.clients)
                self.refresh_clients_combo()

            # Upload su GitHub se richiesto
            github_status = ""
            if self.upload_var.get():
                success, github_msg = self.upload_to_github(hw_id, target_dir)
                github_status = f"\n\n✅ GitHub: {github_msg}" if success else f"\n\n⚠️ GitHub: {github_msg}"

            # Messaggio successo
            msg = (
                f"✅ Licenza GENERATA con successo!\n\n"
                f"📋 Cliente: {client_name}\n"
                f"🔧 Hardware ID: {hw_id[:30]}...\n"
                f"📅 Scadenza: {expiry_str}\n\n"
                f"📁 File salvati in:\n{target_dir}"
                f"{github_status}"
            )

            messagebox.showinfo("Successo", msg)

            # Apri cartella (Windows)
            import os  # noqa: PLC0415

            if os.name == "nt":
                os.startfile(target_dir)  # noqa: S606

        except Exception as e:
            messagebox.showerror("Errore", f"Generazione fallita:\n{e!s}")


def main() -> None:
    """Entry point per l'applicazione di gestione licenze."""
    root = tk.Tk()
    _app = LicenseAdminApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
