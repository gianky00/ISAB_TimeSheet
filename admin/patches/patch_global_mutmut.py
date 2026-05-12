from pathlib import Path

import mutmut


def patch_global_mutmut() -> None:
    p = Path(mutmut.__file__).parent / "__main__.py"
    if not p.exists():
        print("Global mutmut not found.")
        return

    content = p.read_text(encoding="utf-8")

    # 1. Protegge resource
    old_res = "import resource"
    new_res = "try:\n    import resource\nexcept ImportError:\n    resource = None"

    # 2. Rimuove fork (non supportato su Windows)
    old_fork = "set_start_method('fork')"
    new_fork = "# set_start_method('fork')"

    if old_res in content:
        content = content.replace(old_res, new_res)

    if old_fork in content:
        content = content.replace(old_fork, new_fork)

    p.write_text(content, encoding="utf-8")
    print(f"Successfully patched global mutmut at: {p}")


if __name__ == "__main__":
    patch_global_mutmut()
