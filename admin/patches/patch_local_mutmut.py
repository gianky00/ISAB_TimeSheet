import os
from pathlib import Path

def patch_mutmut():
    venv_path = Path(".venv/Lib/site-packages/mutmut/__main__.py")
    if not venv_path.exists():
        print("Venv mutmut not found.")
        return

    content = venv_path.read_text(encoding="utf-8")
    
    # Protegge l'import di resource usando stringhe raw per sicurezza
    old_line = "import resource"
    new_line = "try:\n    import resource\nexcept ImportError:\n    resource = None"
    
    if old_line in content:
        new_content = content.replace(old_line, new_line)
        venv_path.write_text(new_content, encoding="utf-8")
        print("Successfully patched mutmut for Windows.")
    else:
        print("Mutmut already patched or import not found.")

if __name__ == "__main__":
    patch_mutmut()