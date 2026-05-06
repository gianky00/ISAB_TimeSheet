"""
Bot TS - Build & Distribution Script
Compila l'applicazione con PyInstaller, crea l'installer con Inno Setup,
e deploya su Netlify tramite API (ZIP deploy).
"""

import argparse
import contextlib
import json
import logging
import os
import shutil
import subprocess
import sys
import time
import zipfile
from pathlib import Path

# Add admin folder to path to import analyzer
sys.path.append(str(Path(__file__).resolve().parent.parent))
import requests
from analyze_dependencies import get_all_imports  # type: ignore

# Paths
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
DIST_DIR = SCRIPT_DIR / "dist"
BUILD_DIR = SCRIPT_DIR / "build"
OBF_DIR = BUILD_DIR / "obf"
ASSETS_DIR = ROOT_DIR / "assets"
SETUP_OUTPUT_DIR = SCRIPT_DIR / "Setup"

# Add ROOT_DIR to sys.path to allow importing src
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Log File
LOG_FILE = ROOT_DIR / "build_log.txt"

# Application info
APP_NAME = "SyncroJob"
APP_EXE_NAME = "SyncroJob"
MAIN_SCRIPT = ROOT_DIR / "main.py"
ICON_PATH = ASSETS_DIR / "app.ico"
ISS_SCRIPT = SCRIPT_DIR / "setup_script.iss"

# Netlify config
NETLIFY_SITE_ID = "2b481f10-fbd1-44d4-81ed-1a15b15c315b"

# Setup Logging
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)


def log_and_print(message, level="INFO"):  # noqa: ANN001, ANN201
    """Logga su file e stampa a video."""
    print(message)
    sys.stdout.flush()
    if level == "INFO":
        logger.info(message)
    elif level == "ERROR":
        logger.error(message)
    elif level == "WARNING":
        logger.warning(message)


def run_command(cmd, cwd=None, shell=False, check=True, input_str=None):  # noqa: ANN001, ANN201
    """Run command and log output. Supports sending input to stdin."""
    if cwd is None:
        cwd = ROOT_DIR

    if os.name == "nt":
        shell = True

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
    log_and_print(f"\n[EXEC] {cmd_str}")

    # Costanti per Windows
    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NO_WINDOW

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            shell=shell,
            stdin=subprocess.PIPE if input_str else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            creationflags=creationflags,
        )

        if input_str and process.stdin:
            log_and_print(f"[INPUT] Sending: {input_str.strip()}")
            process.stdin.write(input_str)
            process.stdin.flush()
            process.stdin.close()

        if process.stdout:
            for line in iter(process.stdout.readline, ""):
                if line:
                    # Clear spinner line before printing actual output
                    sys.stdout.write("\r" + " " * 20 + "\r")
                    sys.stdout.write(line)
                    sys.stdout.flush()
                    logger.info(f"[CMD] {line.strip()}")

        return_code = process.wait()

        if check and return_code != 0:
            log_and_print(f"[ERROR] Command failed with return code {return_code}", "ERROR")
            sys.exit(1)
        return return_code  # noqa: TRY300

    except Exception as e:
        log_and_print(f"[EXCEPTION] {e}", "ERROR")
        if check:
            sys.exit(1)
        return 1


def get_version():  # noqa: ANN201
    """Read version from version.py"""
    version_file = ROOT_DIR / "src" / "core" / "version.py"
    try:
        with version_file.open(encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split('"')[1]
    except Exception as e:
        log_and_print(f"Warning: Build distribution process error: {e}", "WARNING")
    return "0.0.0"


def clean_build():  # noqa: ANN201
    """Remove previous build artifacts."""
    log_and_print("[BUILD] Cleaning previous builds...")
    for folder in (DIST_DIR, BUILD_DIR):
        if folder.exists():
            try:
                shutil.rmtree(folder)
                log_and_print(f"  Removed: {folder}")
            except Exception as e:
                log_and_print(f"  Error removing {folder}: {e}", "ERROR")


def _ensure_selenium_driver(drivers_dir: Path) -> None:
    """Scarica e allinea il ChromeDriver per Selenium."""
    (drivers_dir / ".exists").write_text("Sentinel file for PyInstaller")
    try:
        from webdriver_manager.chrome import ChromeDriverManager  # noqa: PLC0415

        log_and_print("  Checking for latest ChromeDriver...")
        driver_path_str = ChromeDriverManager().install()
        driver_path = Path(driver_path_str)
        if not driver_path.is_file() or driver_path.suffix.lower() != ".exe":
            search_path = driver_path.parent if driver_path.is_file() else driver_path
            potential_exes = list(search_path.rglob("chromedriver.exe"))
            if potential_exes:
                driver_path = potential_exes[0]
            else:
                raise FileNotFoundError(f"Chromedriver.exe not found in {search_path}")  # noqa: TRY003, TRY301
        dest_path = drivers_dir / "chromedriver.exe"
        shutil.copy2(driver_path, dest_path)
        log_and_print(f"  [SUCCESS] ChromeDriver aligned: {dest_path}")
    except Exception as e:
        log_and_print(f"  [WARNING] Could not update ChromeDriver: {e}", "WARNING")


def _ensure_playwright_browsers(drivers_dir: Path):  # noqa: ANN201
    """Sincronizza i binari di Playwright (Chromium, Headless Shell, FFmpeg)."""
    pw_source_dir = Path(os.environ["LOCALAPPDATA"]) / "ms-playwright"
    pw_dest_dir = drivers_dir / "ms-playwright"

    try:
        if not pw_source_dir.exists():
            log_and_print(f"  [WARNING] Playwright source dir not found: {pw_source_dir}", "WARNING")
            return

        log_and_print(f"  Syncing Playwright browsers from {pw_source_dir}...")

        # Pattern di binari da includere (Chromium standard, Headless Shell e FFmpeg per codec)
        browser_patterns = ["chromium-*", "chromium_headless_shell-*", "ffmpeg-*"]
        found_any = False

        for pattern in browser_patterns:
            for src_dir in pw_source_dir.glob(pattern):
                target_pw_dir = pw_dest_dir / src_dir.name

                if not target_pw_dir.exists():
                    log_and_print(
                        f"  Copying {src_dir.name} to drivers folder (this may take a while)..."
                    )
                    shutil.copytree(src_dir, target_pw_dir, dirs_exist_ok=True)
                    log_and_print(f"  [SUCCESS] Playwright {src_dir.name} aligned.")
                else:
                    log_and_print(f"  [INFO] Playwright {src_dir.name} already present.")
                found_any = True

        if found_any:
            # File sentinel per confermare a runtime l'integrità
            (pw_dest_dir / "bundled.txt").write_text(
                f"Last sync: {time.ctime()}\nPatterns: {', '.join(browser_patterns)}"
            )
        else:
            log_and_print("  [WARNING] No Playwright browsers found in source!", "WARNING")

    except Exception as e:
        log_and_print(f"  [ERROR] Playwright browser sync failed: {e}", "ERROR")
        if not pw_dest_dir.exists():
            log_and_print("  [CRITICAL] Playwright browsers missing for build!", "ERROR")


def ensure_drivers():  # noqa: ANN201
    """Ensure chromedriver and Playwright browsers are present and aligned."""
    log_and_print("[BUILD] Ensuring drivers and Playwright browsers are present...")
    drivers_dir = ROOT_DIR / "drivers"
    drivers_dir.mkdir(parents=True, exist_ok=True)

    _ensure_selenium_driver(drivers_dir)
    _ensure_playwright_browsers(drivers_dir)

def run_pyarmor():  # noqa: ANN201
    """Obfuscate scripts using PyArmor."""
    log_and_print("[BUILD] Running PyArmor obfuscation...")

    OBF_DIR.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "pyarmor.cli",
        "gen",
        "--output",
        str(OBF_DIR),
        "--recursive",
        str(ROOT_DIR / "src"),
        str(MAIN_SCRIPT),
    ]

    # Invia 'c' (continue) per gestire il prompt della licenza di PyArmor 9 in ambienti non interattivi
    run_command(cmd, cwd=ROOT_DIR, input_str="c\n")
    log_and_print("[BUILD] PyArmor obfuscation completed.")


def run_pyinstaller(obfuscated=False):  # noqa: ANN001, ANN201
    """Build executable with PyInstaller."""
    log_and_print(f"[BUILD] Running PyInstaller (Obfuscated: {obfuscated})...")

    if obfuscated:
        script_path = OBF_DIR / "main.py"
        src_path = OBF_DIR / "src"
        if not script_path.exists():
            log_and_print(f"[ERROR] Obfuscated script not found: {script_path}", "ERROR")
            sys.exit(1)
    else:
        script_path = MAIN_SCRIPT
        src_path = ROOT_DIR / "src"

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name",
        APP_EXE_NAME,
        "--onedir",
        "--windowed",
        "--noconfirm",
        "--clean",
        "--distpath",
        str(DIST_DIR),
        "--workpath",
        str(BUILD_DIR),
        "--add-data",
        f"{src_path};src",
        "--add-data",
        f"{ROOT_DIR / 'assets'};assets",
        "--add-data",
        f"{ROOT_DIR / 'drivers'};drivers",
    ]

    if ICON_PATH.exists():
        cmd.extend(["--icon", str(ICON_PATH)])

    log_and_print("[BUILD] Analyzing source code for dependencies...")

    try:
        detected_imports = get_all_imports(str(MAIN_SCRIPT), str(ROOT_DIR / "src"))
        log_and_print(f"[BUILD] Detected {len(detected_imports)} hidden imports.")
    except Exception as e:
        log_and_print(f"[ERROR] Dependency analysis failed: {e}", "ERROR")
        detected_imports = []

    ignored_imports = [
        "bot",
        "locators",
        "pages",
        "modern_button",
        "timeline_widget",
        "toast",
        "status_card",
        "status_indicator",
        "helpers",
        "info_widgets",
        "data_table",
        "excel_table",
        "version",
        "constants",
    ]
    detected_imports = [imp for imp in detected_imports if imp not in ignored_imports]

    for imp in detected_imports:
        cmd.extend(["--hidden-import", imp])

    # CRITICAL: Force include standard library handlers
    force_hidden_imports = [
        "win32con",
        "win32print",
        "win32ui",
        "logging.handlers",
        "win32com",
        "win32com.client",
        "pythoncom",
    ]
    for mod in force_hidden_imports:
        cmd.extend(["--hidden-import", mod])

    qt_excludes = [
        "shapely",
        "PyQt6.QtBluetooth",
        "PyQt6.QtNfc",
        "PyQt6.Qt3DCore",
        "PyQt6.Qt3DRender",
        "PyQt6.Qt3DInput",
        "PyQt6.Qt3DLogic",
        "PyQt6.Qt3DExtras",
        "PyQt6.QtSpatialAudio",
        "PyQt6.QtSensors",
        "PyQt6.QtQuick3D",
        "PyQt6.QtMultimedia",
        "PyQt6.QtQml",
        "PyQt6.QtQuick",
    ]
    for exc in qt_excludes:
        cmd.extend(["--exclude-module", exc])

    complex_packages = ["selenium", "webdriver_manager", "markdown", "matplotlib", "telegram", "pandera"]
    for pkg in complex_packages:
        cmd.extend(["--collect-submodules", pkg])

    force_collect = [
        "pandas",
        "numpy",
        "pandera",
        "telegram",
        "markdown",
        "matplotlib",
        "cryptography",
        "jaraco.text",
        "keyring",
        "pymupdf",
        "fitz",
        "lxml",
        "openpyxl",
        "PIL",
        "playwright",
    ]
    for pkg in force_collect:
        cmd.extend(["--collect-all", pkg])

    cmd.append(str(script_path))
    run_command(cmd, cwd=ROOT_DIR)
    log_and_print("[BUILD] PyInstaller completed successfully.")


def run_nuitka(obfuscated=False):  # noqa: ANN001, ANN201
    """Build executable with Nuitka."""
    log_and_print(f"[BUILD] Running Nuitka (Obfuscated: {obfuscated})...")

    if obfuscated:
        script_path = OBF_DIR / "main.py"
        if not script_path.exists():
            log_and_print(f"[ERROR] Obfuscated script not found: {script_path}", "ERROR")
            sys.exit(1)
    else:
        script_path = MAIN_SCRIPT

    cmd = [
        sys.executable,
        "-m",
        "nuitka",
        "--standalone",
        "--show-progress",
        "--show-scons",
        "--verbose",
        "--enable-plugin=pyqt6",
        "--enable-plugin=matplotlib",
        "--windows-disable-console",
        "--follow-imports",
        "--assume-yes-for-downloads",
        "--lto=no",
        "--jobs=1",
        "--low-memory",
        f"--windows-product-version={get_version()}",
        f"--windows-file-version={get_version()}",
        "--python-flag=-O",
        "--output-dir=" + str(DIST_DIR),
        "--include-data-dir=" + str(ROOT_DIR / "assets") + "=assets",
        "--include-data-dir=" + str(ROOT_DIR / "drivers") + "=drivers",
    ]

    if ICON_PATH.exists():
        cmd.append(f"--windows-icon-from-ico={ICON_PATH}")

    # Nuitka handles hidden imports differently.
    force_include_mods = [
        "win32con",
        "win32print",
        "win32ui",
        "logging.handlers",
        "win32com",
        "win32com.client",
        "pythoncom",
        "jaraco.text",
        "keyring.backends",
    ]
    cmd.extend([f"--include-module={mod}" for mod in force_include_mods])

    force_include_pkgs = [
        "pandas",
        "numpy",
        "pandera",
        "telegram",
        "markdown",
        "matplotlib",
        "cryptography",
        "keyring",
        "pymupdf",
        "fitz",
        "openpyxl",
        "PIL",
        "selenium",
        "webdriver_manager",
        "playwright",
    ]
    cmd.extend([f"--include-package={pkg}" for pkg in force_include_pkgs])

    cmd.append(str(script_path))
    run_command(cmd, cwd=ROOT_DIR)

    # Nuitka puts the output in <output-dir>/<script-name>.dist
    # We need to move/align it to match DIST_DIR structure expected by Inno Setup
    nuitka_dist = DIST_DIR / (script_path.stem + ".dist")
    target_dist = DIST_DIR / APP_EXE_NAME

    if nuitka_dist.exists():
        if target_dist.exists():
            shutil.rmtree(target_dist)
        shutil.move(str(nuitka_dist), str(target_dist))
        log_and_print(f"[BUILD] Nuitka build moved to {target_dist}")

    log_and_print("[BUILD] Nuitka completed successfully.")


def run_inno_setup():  # noqa: ANN201
    """Build installer with Inno Setup."""
    log_and_print("[BUILD] Running Inno Setup...")

    # Tenta di trovare ISCC nel PATH o in percorsi comuni
    iscc = shutil.which("iscc")
    if not iscc:
        inno_paths = [
            Path(r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"),
            Path(r"C:\Program Files\Inno Setup 6\ISCC.exe"),
        ]
        iscc = next((str(p) for p in inno_paths if p.exists()), None)

    if not iscc:
        log_and_print("[WARNING] Inno Setup (ISCC.exe) not found. Skipping installer creation.", "WARNING")
        return False

    SETUP_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    version = get_version()
    log_and_print(f"[BUILD] Building installer for version: {version}")

    cmd = [str(iscc), f"/DMyAppVersion={version}", str(ISS_SCRIPT)]
    run_command(cmd, cwd=SCRIPT_DIR)

    log_and_print("[BUILD] Installer created successfully.")
    return True


def get_netlify_token():  # noqa: ANN201
    """Returns the obfuscated Netlify API token."""
    return "nfp_VJbSMoKXxms3" + "Xa8gdQkKKedPC6" + "EnHQZL9687"


def generate_index_html(deploy_dir: Path, setup_filename: str, version_str: str):  # noqa: ANN201
    """Generates a professional index.html download page."""
    html_content = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Download {APP_NAME}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
    <style>
        body {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 100vh; display: flex; align-items: center; justify-content: center; }}
        .card {{ border: none; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); max-width: 500px; width: 90%; }}
        .card-header {{ background-color: white; border-bottom: none; padding-top: 30px; border-radius: 15px 15px 0 0 !important; }}
        .app-icon {{ font-size: 4rem; color: #764ba2; }}
        .btn-download {{ padding: 15px 30px; font-size: 1.2rem; font-weight: 600; border-radius: 50px; box-shadow: 0 4px 6px rgba(118, 75, 162, 0.3); transition: all 0.3s ease; background-color: #667eea; border-color: #667eea; color: white; }}
        .btn-download:hover {{ transform: translateY(-2px); box-shadow: 0 6px 12px rgba(118, 75, 162, 0.4); background-color: #764ba2; border-color: #764ba2; color: white; }}
        .features-list {{ text-align: left; margin: 20px 0; color: #6c757d; }}
        .features-list li {{ margin-bottom: 8px; }}
    </style>
</head>
<body>
    <div class="card text-center p-4">
        <div class="card-header">
            <i class="bi bi-robot app-icon"></i>
            <h2 class="mt-3 fw-bold" style="color: #764ba2;">{APP_NAME}</h2>
            <p class="text-muted">Automazione e Gestione Avanzata</p>
        </div>
        <div class="card-body">
            <ul class="list-unstyled features-list mx-auto" style="max-width: 300px;">
                <li><i class="bi bi-check-circle-fill text-success me-2"></i>Scarico Ore Automatico</li>
                <li><i class="bi bi-check-circle-fill text-success me-2"></i>Integrazione Safework</li>
                <li><i class="bi bi-check-circle-fill text-success me-2"></i>Dashboard Intelligente</li>
            </ul>
            <a href="{setup_filename}" class="btn btn-download w-100 my-3"><i class="bi bi-windows me-2"></i> Scarica per Windows</a>
            <div class="mt-4 pt-3 border-top">
                <div class="row text-muted small">
                    <div class="col-6 text-start">Versione: <span class="fw-bold text-dark">v{version_str}</span></div>
                    <div class="col-6 text-end">Data: {time.strftime("%d/%m/%Y")}</div>
                </div>
            </div>
        </div>
    </div>
    <script>setTimeout(function() {{ window.location.href = "{setup_filename}"; }}, 2000);</script>
</body>
</html>"""
    (deploy_dir / "index.html").write_text(html_content, encoding="utf-8")
    log_and_print("Generated index.html")


def prepare_and_deploy_netlify(setup_dir: Path, setup_filename: str):  # noqa: ANN201
    """Creates deploy folder and uploads to Netlify."""
    deploy_dir = DIST_DIR / "deploy"
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir(parents=True)

    # 1. Copy Setup File
    shutil.copy2(setup_dir / setup_filename, deploy_dir / setup_filename)
    log_and_print(f"Copied setup to: {deploy_dir}")

    # 2. Generate version.json
    version_str = get_version()
    download_url = f"https://projectjob-bot.netlify.app/{setup_filename}"
    version_data = {"version": version_str, "url": download_url}
    (deploy_dir / "version.json").write_text(json.dumps(version_data, indent=4), encoding="utf-8")
    log_and_print(f"Generated version.json (v{version_str})")

    # 3. Generate Landing Page
    generate_index_html(deploy_dir, setup_filename, version_str)

    # 4. Generate netlify.toml
    netlify_toml = '[build]\n  publish = "."\n\n[build.processing]\n  skip_processing = true'
    (deploy_dir / "netlify.toml").write_text(netlify_toml, encoding="utf-8")

    # 5. ZIP and Upload
    log_and_print("Starting Netlify ZIP deploy...")
    zip_path = DIST_DIR / "deploy.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in deploy_dir.rglob("*"):
            if file.is_file():
                zipf.write(file, file.relative_to(deploy_dir))

    if zip_path.exists():
        log_and_print(f"Zip created: {zip_path.stat().st_size / 1024 / 1024:.2f} MB")

    try:
        data = zip_path.read_bytes()
        url = f"https://api.netlify.com/api/v1/sites/{NETLIFY_SITE_ID}/deploys"
        headers = {"Content-Type": "application/zip", "Authorization": f"Bearer {get_netlify_token()}"}
        response = requests.post(url, headers=headers, data=data, timeout=600)

        if response.status_code == 200:  # noqa: PLR2004
            log_and_print("DEPLOY SUCCESSFUL!")
            log_and_print(f"Live URL: {response.json().get('url')}")
            return True
        log_and_print(f"Upload Failed: {response.status_code} - {response.text}", "ERROR")
        return False  # noqa: TRY300
    except Exception as e:
        log_and_print(f"Error during upload: {e}", "ERROR")
        return False
    finally:
        if zip_path.exists():
            zip_path.unlink()


def deploy_to_network_share(setup_dir: Path, setup_filename: str):  # noqa: ANN201
    """Deploys to local network share with auto-archiving."""
    try:
        from src.core import version as v_mod  # noqa: PLC0415

        net_path_str = getattr(v_mod, "NETWORK_UPDATE_PATH", None)
        if not net_path_str:
            log_and_print("[WARNING] NETWORK_UPDATE_PATH not defined. Skipping.", "WARNING")
            return False

        net_path = Path(net_path_str)
        log_and_print(f"[DEPLOY] Starting network deploy to: {net_path}")

        archive_path = net_path / "archive"
        archive_path.mkdir(parents=True, exist_ok=True)

        # 1. Archivia i setup precedenti
        for existing_file in net_path.glob("SyncroJob_Setup_*.exe"):
            if existing_file.name != setup_filename:
                dst_old = archive_path / existing_file.name
                try:
                    if dst_old.exists():
                        dst_old.unlink()
                    shutil.move(str(existing_file), str(dst_old))
                    log_and_print(f"  Archived: {existing_file.name}")
                except Exception as e:
                    log_and_print(f"  [WARNING] Could not archive {existing_file.name}: {e}", "WARNING")

        # 2. Copia il nuovo Setup File
        shutil.copy2(setup_dir / setup_filename, net_path / setup_filename)
        log_and_print(f"  Copying latest setup: {setup_filename}")

        # 3. Update version.json
        version_str = get_version()
        version_data = {
            "version": version_str,
            "url": setup_filename,
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "notes": "Latest stable release",
        }
        (net_path / "version.json").write_text(json.dumps(version_data, indent=4), encoding="utf-8")
        log_and_print(f"  [SUCCESS] Network deploy complete (v{version_str}).")
        return True  # noqa: TRY300
    except Exception as e:
        log_and_print(f"[ERROR] Network deploy failed: {e}", "ERROR")
        return False


def main() -> None:  # noqa: PLR0912
    parser = argparse.ArgumentParser(description="Bot TS Build Script")
    parser.add_argument("--use-nuitka", action="store_true", help="Use Nuitka instead of PyInstaller")
    parser.add_argument("--no-deploy", action="store_true", help="Skip Netlify")
    parser.add_argument("--no-network", action="store_true", help="Skip Network")
    parser.add_argument("--skip-installer", action="store_true", help="Skip Inno")
    parser.add_argument("--debug-no-obfuscate", action="store_true", help="Skip PyArmor")
    args = parser.parse_args()

    if LOG_FILE.exists():
        with contextlib.suppress(OSError):
            LOG_FILE.unlink()

    log_and_print("=" * 60)
    log_and_print(f"  SYNCROJOB BUILD SCRIPT - v{get_version()}")
    if args.use_nuitka:
        log_and_print("  COMPILER: NUITKA")
    else:
        log_and_print("  COMPILER: PYINSTALLER")
    log_and_print("=" * 60)

    ensure_drivers()
    clean_build()

    is_obfuscated = not args.debug_no_obfuscate
    if is_obfuscated:
        run_pyarmor()

    if args.use_nuitka:
        run_nuitka(obfuscated=is_obfuscated)
    else:
        run_pyinstaller(obfuscated=is_obfuscated)

    setup_filename = None
    if not args.skip_installer:
        run_inno_setup()
        setup_filename = f"SyncroJob_Setup_{get_version()}.exe"

    if setup_filename and (SETUP_OUTPUT_DIR / setup_filename).exists():
        if not args.no_network:
            deploy_to_network_share(SETUP_OUTPUT_DIR, setup_filename)
        if not args.no_deploy:
            if prepare_and_deploy_netlify(SETUP_OUTPUT_DIR, setup_filename):
                log_and_print("=" * 60 + "\nBUILD AND PACKAGING COMPLETE SUCCESS!\n" + "=" * 60)
            else:
                log_and_print("=" * 60 + "\nBUILD SUCCESSFUL BUT DEPLOY FAILED!\n" + "=" * 60)
                sys.exit(1)
    elif args.no_deploy:
        log_and_print("BUILD COMPLETED (NO DEPLOY)!")
    else:
        log_and_print("[WARNING] Installer missing, skipping deploy.", "WARNING")


if __name__ == "__main__":
    main()
