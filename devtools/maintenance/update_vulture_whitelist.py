import re


def main() -> None:
    try:
        with open("tests/vulture_raw.txt", encoding="utf-8") as f:
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
        with open("devtools/devtools/config/vulture_whitelist.py", "a", encoding="utf-8") as f:
            f.write("\n# Auto-generated whitelists from framework utilities\n")
            f.writelines(f"{name}\n" for name in sorted(names))
        print(f"Aggiunti {len(names)} elementi alla whitelist.")
    else:
        print("Nessun elemento da aggiungere.")


if __name__ == "__main__":
    main()
