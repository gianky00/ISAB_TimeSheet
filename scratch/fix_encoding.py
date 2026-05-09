import os
import re

REPLACEMENTS = {
    "a'": "à",
    "e'": "è",
    "i'": "ì",
    "o'": "ò",
    "u'": "ù",
    "E'": "È",
    "A'": "À",
}

# Regex to match any of the keys followed by word boundary or space/punctuation
# to avoid catching things like "variable_a'1" if they existed (unlikely in Py)
PATTERN = re.compile("|".join(re.escape(k) for k in REPLACEMENTS))


def fix_file(filepath):
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        new_content = PATTERN.sub(lambda m: REPLACEMENTS[m.group(0)], content)

        if content != new_content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
    return False


def main():
    base_dir = r"c:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\src"
    count = 0
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):
                if fix_file(os.path.join(root, file)):
                    count += 1
                    print(f"Fixed: {file}")

    # Also check main.py
    if fix_file(r"c:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\main.py"):
        count += 1
        print("Fixed: main.py")

    print(f"\nTotal files fixed: {count}")


if __name__ == "__main__":
    main()
