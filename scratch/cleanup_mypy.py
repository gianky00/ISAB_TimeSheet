"""Script di utilità per rimuovere forzatamente le soppressioni MyPy dai file sorgente."""

import os
import re


def cleanup_mypy_suppressions(directory: str) -> None:
    """
    Scansiona ricorsivamente una directory e rimuove i commenti 'disable-error-code' di MyPy.

    Args:
      directory: Il percorso della cartella da pulire.
    """
    pattern = re.compile(r"^# mypy: disable-error-code=.*$\n?", re.MULTILINE)

    for root, _dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, encoding="utf-8") as f:
                    content = f.read()

                new_content = pattern.sub("", content)

                if new_content != content:
                    print(f"Cleaned {path}")
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(new_content)


if __name__ == "__main__":
    cleanup_mypy_suppressions("src")
