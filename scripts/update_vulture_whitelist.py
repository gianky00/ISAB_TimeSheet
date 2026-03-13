import re
import sys

def main():
    try:
        with open("tests/vulture_raw.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("File non trovato")
        return

    names = set()
    for line in lines:
        # Cerca pattern come: unused method 'nome_metodo' o unused attribute 'nome_attr'
        match = re.search(r"unused \w+ '([^']+)'", line)
        if match:
            names.add(match.group(1))

    if names:
        with open("config/vulture_whitelist.py", "a", encoding="utf-8") as f:
            f.write("\n# Auto-generated whitelists from framework utilities\n")
            for name in sorted(names):
                f.write(f"{name}\n")
        print(f"Aggiunti {len(names)} elementi alla whitelist.")
    else:
        print("Nessun elemento da aggiungere.")

if __name__ == "__main__":
    main()
