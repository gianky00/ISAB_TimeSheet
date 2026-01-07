import win32print
import subprocess

def debug_printer():
    try:
        printer_name = win32print.GetDefaultPrinter()
        print(f"DEBUG INFO FOR: {printer_name}")
        
        # 1. Check Driver Settings (Win32 API)
        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            info = win32print.GetPrinter(hPrinter, 2)
            devmode = info["pDevMode"]
            # 1=Simplex, 2=Vertical(Duplex), 3=Horizontal(Duplex)
            modes = {1: "Simplex", 2: "Duplex Vertical", 3: "Duplex Horizontal"}
            print(f"API Current Mode: {devmode.Duplex} ({modes.get(devmode.Duplex, 'Unknown')})")
        finally:
            win32print.ClosePrinter(hPrinter)

        # 2. Check PowerShell Configuration
        print("\nPowerShell Config:")
        cmd = f"Get-PrintConfiguration -PrinterName '{printer_name}' | Format-List *Duplex*"
        res = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
        print(res.stdout)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_printer()
