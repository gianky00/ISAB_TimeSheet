"""
Bot TS - License Generator (Admin Tool)
Genera file di licenza per i client.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
import os
import shutil
import json
import hashlib
import sys
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Add project root to sys.path to allow importing src modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, project_root)

from src.core.secrets_manager import SecretsManager

# Carica variabili d'ambiente
load_dotenv()

def get_signing_key():
    """Recupera la chiave di firma/cifratura in modo sicuro."""
    # 1. Environment Variable
    env_key = os.getenv("LICENSE_SECRET_KEY")
    if env_key:
        return env_key.encode()

    # 2. SecretsManager (se configurato localmente per admin)
    try:
        return SecretsManager.get_license_key()
    except Exception:
        pass

    return b""


def _calculate_sha256(filepath):
    """Calcola l'hash SHA256 di un file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


class LicenseAdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bot TS - Gestore Licenze (Admin)")
        self.root.geometry("650x550")
        self.root.resizable(False, False)
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"))
        
        # Header
        header_frame = ttk.Frame(root)
        header_frame.pack(fill="x", pady=15)
        ttk.Label(
            header_frame, 
            text="🔑 Generatore Licenza Bot TS", 
            style="Header.TLabel"
        ).pack()
        
        # Main container
        frm = ttk.LabelFrame(root, text="Dati Cliente", padding=20)
        frm.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Hardware ID
        ttk.Label(frm, text="Hardware ID (Seriale Disco):").pack(anchor="w")
        
        hw_frame = ttk.Frame(frm)
        hw_frame.pack(fill="x", pady=5)
        
        self.ent_disk = ttk.Entry(hw_frame, width=50)
        self.ent_disk.pack(side="left", fill="x", expand=True)
        
        ttk.Button(hw_frame, text="📋 Incolla", command=self.paste_disk, width=10).pack(side="right", padx=(5, 0))
        
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
            date_frame, text="1 Anno", width=8,
            command=lambda: self.set_expiry_days(365)
        ).pack(side="left", padx=(10, 2))
        
        ttk.Button(
            date_frame, text="6 Mesi", width=8,
            command=lambda: self.set_expiry_days(180)
        ).pack(side="left", padx=2)
        
        ttk.Button(
            date_frame, text="3 Mesi", width=8,
            command=lambda: self.set_expiry_days(90)
        ).pack(side="left", padx=2)
        
        ttk.Button(
            date_frame, text="1 Mese", width=8,
            command=lambda: self.set_expiry_days(30)
        ).pack(side="left", padx=2)
        
        # Default: 1 anno
        self.set_expiry_days(365)
        
        # Info box
        info_frame = ttk.LabelFrame(frm, text="ℹ️ Info", padding=10)
        info_frame.pack(fill="x", pady=(20, 0))
        
        info_text = (
            "I file generati saranno:\n"
            "• config.dat - Dati licenza cifrati\n"
            "• manifest.json - Checksum integrità\n\n"
            "Caricare su: github.com/gianky00/intelleo-licenses/tree/main/licenses/{HW_ID}/"
        )
        ttk.Label(info_frame, text=info_text, justify="left").pack(anchor="w")
        
        # Generate button
        self.btn_gen = ttk.Button(
            root, 
            text="🔐 GENERA FILE LICENZA", 
            command=self.generate,
            style="Accent.TButton"
        )
        self.btn_gen.pack(fill="x", padx=20, pady=20, ipady=12)
    
    def paste_disk(self):
        """Incolla dagli appunti."""
        try:
            self.ent_disk.delete(0, tk.END)
            self.ent_disk.insert(0, self.root.clipboard_get().strip())
        except:
            pass
    
    def set_expiry_days(self, days):
        """Imposta la data di scadenza."""
        expiry = (date.today() + timedelta(days=days)).strftime("%Y-%m-%d")
        self.ent_date.delete(0, tk.END)
        self.ent_date.insert(0, expiry)
    
    def generate(self):
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
        
        license_key = get_signing_key()
        if not license_key:
             messagebox.showerror("Errore Crittografia", "Chiave segreta LICENSE_SECRET_KEY non trovata!\nImposta la variabile d'ambiente o il .env.")
             return

        # Pulisci nome per cartella
        folder_name = "".join(
            c for c in client_name 
            if c.isalnum() or c in (' ', '_', '-')
        ).strip().replace(' ', '_')
        
        # Paths
        base_output = os.path.dirname(os.path.abspath(__file__))
        client_dir = os.path.join(base_output, folder_name)
        target_dir = os.path.join(client_dir, "Licenza")
        
        try:
            # Crea/pulisci cartella
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            os.makedirs(target_dir)
            
            # Formatta data
            try:
                expiry_obj = date.fromisoformat(expiry)
                expiry_str = expiry_obj.strftime('%d/%m/%Y')
            except ValueError:
                expiry_str = expiry
            
            gen_date_str = date.today().strftime('%d/%m/%Y')
            
            # Payload licenza
            payload = {
                "Hardware ID": disk_serial.strip().rstrip('.'),
                "Scadenza Licenza": expiry_str,
                "Generato il": gen_date_str,
                "Cliente": client_name,
                "Applicazione": "Bot TS"
            }
            
            # Cifra payload
            json_payload = json.dumps(payload, indent=2).encode('utf-8')
            cipher = Fernet(license_key)
            encrypted_data = cipher.encrypt(json_payload)
            
            # Scrivi config.dat
            config_path = os.path.join(target_dir, "config.dat")
            with open(config_path, "wb") as f:
                f.write(encrypted_data)
            
            # Genera manifest
            manifest = {
                "config.dat": _calculate_sha256(config_path),
                "generated": gen_date_str,
                "client": client_name
            }
            
            manifest_path = os.path.join(target_dir, "manifest.json")
            with open(manifest_path, "w") as f:
                json.dump(manifest, f, indent=4)
            
            # Messaggio successo
            msg = (
                f"✅ Licenza GENERATA con successo!\n\n"
                f"📋 Cliente: {client_name}\n"
                f"🔧 Hardware ID: {disk_serial[:30]}...\n"
                f"📅 Scadenza: {expiry_str}\n\n"
                f"📁 File salvati in:\n{target_dir}\n\n"
                f"⬆️ Caricare su GitHub:\n"
                f"gianky00/intelleo-licenses/tree/main/licenses/{disk_serial.strip().rstrip('.')}/"
            )
            
            messagebox.showinfo("Successo", msg)
            
            # Apri cartella (Windows)
            if os.name == 'nt':
                os.startfile(target_dir)
        
        except Exception as e:
            messagebox.showerror("Errore", f"Generazione fallita:\n{str(e)}")


def main():
    root = tk.Tk()
    app = LicenseAdminApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
