import os
import re

# Map back the corrupted dictionary keys/string literals
# These happen when a string literal ended in a vowel and the closing quote was '
REPAIR_MAP = {
    "à]": "a']",
    "è]": "e']",
    "ì]": "i']",
    "ò]": "o']",
    "ù]": "u']",
    "È]": "E']",
    "à)": "a')",  # In case it was in a function call like func('area')
    "è)": "e')",
    "ì)": "i')",
    "ò)": "o')",
    "ù)": "u')",
    "È)": "E')",
    "à,": "a',",  # In case it was in a list/tuple
    "è,": "e',",
    "ì,": "i',",
    "ò,": "o',",
    "ù,": "u',",
    "È,": "E',",
}

PATTERN = re.compile("|".join(re.escape(k) for k in REPAIR_MAP))


def repair_file(filepath):
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        new_content = PATTERN.sub(lambda m: REPAIR_MAP[m.group(0)], content)

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
                if repair_file(os.path.join(root, file)):
                    count += 1
                    print(f"Repaired: {file}")

    # Also check main.py
    if repair_file(r"c:\Users\gianc\Desktop\SCRIPT\ISAB_TimeSheet\main.py"):
        count += 1
        print("Repaired: main.py")

    print(f"\nTotal files repaired: {count}")


if __name__ == "__main__":
    main()
