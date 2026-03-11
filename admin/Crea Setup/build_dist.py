"""
Bot TS - Build & Distribution Script
Compila l'applicazione con PyInstaller, crea l'installer con Inno Setup,
e deploya su Netlify tramite API (ZIP deploy).
"""

import argparse
import contextlib
import glob
import json
import logging
import os
import shutil
import subprocess
import sys
import time
import zipfile

# Add admin folder to path to import analyzer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from analyze_dependencies import get_all_imports

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
DIST_DIR = os.path.join(SCRIPT_DIR, "dist")
BUILD_DIR = os.path.join(SCRIPT_DIR, "build")
OBF_DIR = os.path.join(BUILD_DIR, "obf")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
SETUP_OUTPUT_DIR = os.path.join(SCRIPT_DIR, "Setup")

# Log File
LOG_FILE = os.path.join(ROOT_DIR, "build_log.txt")

# Application info
APP_NAME = "SyncroJob"
APP_EXE_NAME = "SyncroJob"
MAIN_SCRIPT = os.path.join(ROOT_DIR, "main.py")
ICON_PATH = os.path.join(ASSETS_DIR, "app.ico")
ISS_SCRIPT = os.path.join(SCRIPT_DIR, "setup_script.iss")

# Netlify config
NETLIFY_SITE_ID = "2b481f10-fbd1-44d4-81ed-1a15b15c315b"

# Setup Logging
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

def log_and_print(message, level="INFO"):
    """Logga su file e stampa a video."""
    print(message)
    sys.stdout.flush()
    if level == "INFO":
        logger.info(message)
    elif level == "ERROR":
        logger.error(message)
    elif level == "WARNING":
        logger.warning(message)


def run_command(cmd, cwd=None, shell=False, check=True):
    """Run command and log output."""
    if cwd is None:
        cwd = ROOT_DIR

    # On Windows, always use shell=True for script commands
    if os.name == "nt":
        shell = True

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
    log_and_print(f"\n[EXEC] {cmd_str}")

    try:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        for line in iter(process.stdout.readline, ""):
            if line:
                sys.stdout.write(line)
                sys.stdout.flush()
                logger.info(f"[CMD] {line.strip()}")

        return_code = process.wait()

        if check and return_code != 0:
            log_and_print(f"[ERROR] Command failed with return code {return_code}", "ERROR")
            sys.exit(1)
        return return_code

    except Exception as e:
        log_and_print(f"[EXCEPTION] {e}", "ERROR")
        if check:
            sys.exit(1)
        return 1


def get_version():
    """Read version from version.py"""
    version_file = os.path.join(ROOT_DIR, "src", "core", "version.py")
    try:
        with open(version_file, encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split('"')[1]
    except Exception as e:
        log_and_print(f"Warning: Build distribution process error: {e}", "WARNING")
    return "0.0.0"


def clean_build():
    """Remove previous build artifacts."""
    log_and_print("[BUILD] Cleaning previous builds...")
    for folder in [DIST_DIR, BUILD_DIR]:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                log_and_print(f"  Removed: {folder}")
            except Exception as e:
                log_and_print(f"  Error removing {folder}: {e}", "ERROR")


def ensure_drivers():
    """Ensure chromedriver is present and up-to-date in drivers folder."""
    log_and_print("[BUILD] Ensuring drivers are present and aligned...")
    drivers_dir = os.path.join(ROOT_DIR, "drivers")
    if not os.path.exists(drivers_dir):
        os.makedirs(drivers_dir)

    # Crea un file sentinel per assicurare che PyInstaller includa sempre la cartella
    with open(os.path.join(drivers_dir, ".exists"), "w") as f:
        f.write("Sentinel file for PyInstaller")

    # Use webdriver-manager to get the latest driver
    try:
        from webdriver_manager.chrome import ChromeDriverManager

        log_and_print("  Checking for latest ChromeDriver...")
        driver_path = ChromeDriverManager().install()

        if not os.path.isfile(driver_path) or not driver_path.lower().endswith(".exe"):
            search_path = os.path.dirname(driver_path) if os.path.isfile(driver_path) else driver_path
            potential_exes = glob.glob(os.path.join(search_path, "**/chromedriver.exe"), recursive=True)
            if potential_exes:
                driver_path = potential_exes[0]
            else:
                raise FileNotFoundError(f"Chromedriver.exe not found in {search_path}")

        dest_path = os.path.join(drivers_dir, "chromedriver.exe")
        shutil.copy2(driver_path, dest_path)
        log_and_print(f"  [SUCCESS] Driver aligned: {dest_path}")

    except Exception as e:
        log_and_print(f"  [WARNING] Could not automatically update driver: {e}", "WARNING")
        if os.path.exists(os.path.join(drivers_dir, "chromedriver.exe")):
            log_and_print("  [INFO] Using existing driver as fallback.")
        else:
            log_and_print("  [CRITICAL ERROR] Driver missing and auto-download failed! Build aborted.", "ERROR")
            sys.exit(1)


def run_pyarmor():
    """Obfuscate scripts using PyArmor."""
    log_and_print("[BUILD] Running PyArmor obfuscation...")

    if not os.path.exists(OBF_DIR):
        os.makedirs(OBF_DIR)

    cmd = [
        sys.executable,
        "-m",
        "pyarmor.cli",
        "gen",
        "--output",
        OBF_DIR,
        "--recursive",
        os.path.join(ROOT_DIR, "src"),
        MAIN_SCRIPT,
    ]

    run_command(cmd, cwd=ROOT_DIR)
    log_and_print("[BUILD] PyArmor obfuscation completed.")


def run_pyinstaller(obfuscated=False):
    """Build executable with PyInstaller."""
    log_and_print(f"[BUILD] Running PyInstaller (Obfuscated: {obfuscated})...")

    if obfuscated:
        script_path = os.path.join(OBF_DIR, "main.py")
        src_path = os.path.join(OBF_DIR, "src")
        if not os.path.exists(script_path):
            log_and_print(f"[ERROR] Obfuscated script not found: {script_path}", "ERROR")
            sys.exit(1)
    else:
        script_path = MAIN_SCRIPT
        src_path = os.path.join(ROOT_DIR, "src")

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
        DIST_DIR,
        "--workpath",
        BUILD_DIR,
        "--add-data",
        f"{src_path};src",
        "--add-data",
        f"{os.path.join(ROOT_DIR, 'assets')};assets",
        "--add-data",
        f"{os.path.join(ROOT_DIR, 'drivers')};drivers",
    ]

    if os.path.exists(ICON_PATH):
        cmd.extend(["--icon", ICON_PATH])

    log_and_print("[BUILD] Analyzing source code for dependencies...")

    try:
        detected_imports = get_all_imports(MAIN_SCRIPT, os.path.join(ROOT_DIR, "src"))
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

    # CRITICAL: Force include standard library handlers often missed in frozen environments
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

    complex_packages = [
        "selenium",
        "webdriver_manager",
        "markdown",
        "matplotlib",
        "telegram",
        "pandera",
    ]
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
    ]
    for pkg in force_collect:
        cmd.extend(["--collect-all", pkg])

    cmd.append(script_path)
    run_command(cmd, cwd=ROOT_DIR)
    log_and_print("[BUILD] PyInstaller completed successfully.")


def run_inno_setup():
    """Build installer with Inno Setup."""
    log_and_print("[BUILD] Running Inno Setup...")

    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    ]

    iscc = None
    for path in inno_paths:
        if os.path.exists(path):
            iscc = path
            break

    if not iscc:
        log_and_print("[WARNING] Inno Setup not found. Skipping installer creation.", "WARNING")
        return False

    if not os.path.exists(SETUP_OUTPUT_DIR):
        os.makedirs(SETUP_OUTPUT_DIR)

    version = get_version()
    log_and_print(f"[BUILD] Building installer for version: {version}")

    cmd = [iscc, f"/DMyAppVersion={version}", ISS_SCRIPT]
    run_command(cmd, cwd=SCRIPT_DIR)

    log_and_print("[BUILD] Installer created successfully.")
    return True


def get_netlify_token():
    """Returns the obfuscated Netlify API token."""
    # Obfuscated token parts
    p1 = "nfp_VJbSMoKXxms3"
    p2 = "Xa8gdQkKKedPC6"
    p3 = "EnHQZL9687"
    return p1 + p2 + p3


def generate_index_html(deploy_dir, setup_filename, version_str):
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
        body {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .card {{
            border: none;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            max-width: 500px;
            width: 90%;
        }}
        .card-header {{
            background-color: white;
            border-bottom: none;
            padding-top: 30px;
            border-radius: 15px 15px 0 0 !important;
        }}
        .app-icon {{
            font-size: 4rem;
            color: #764ba2;
        }}
        .btn-download {{
            padding: 15px 30px;
            font-size: 1.2rem;
            font-weight: 600;
            border-radius: 50px;
            box-shadow: 0 4px 6px rgba(118, 75, 162, 0.3);
            transition: all 0.3s ease;
            background-color: #667eea;
            border-color: #667eea;
            color: white;
        }}
        .btn-download:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(118, 75, 162, 0.4);
            background-color: #764ba2;
            border-color: #764ba2;
            color: white;
        }}
        .features-list {{
            text-align: left;
            margin: 20px 0;
            color: #6c757d;
        }}
        .features-list li {{
            margin-bottom: 8px;
        }}
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

            <a href="{setup_filename}" class="btn btn-download w-100 my-3">
                <i class="bi bi-windows me-2"></i> Scarica per Windows
            </a>

            <div class="mt-4 pt-3 border-top">
                <div class="row text-muted small">
                    <div class="col-6 text-start">
                        Versione: <span class="fw-bold text-dark">v{version_str}</span>
                    </div>
                    <div class="col-6 text-end">
                        Data: {time.strftime("%d/%m/%Y")}
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script>
        setTimeout(function() {{
            window.location.href = "{setup_filename}";
        }}, 2000);
    </script>
</body>
</html>"""

    with open(os.path.join(deploy_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    log_and_print("Generated index.html")


def prepare_and_deploy_netlify(setup_dir, setup_filename):
    """
    Creates a deploy folder with version.json, index.html, and the setup file,
    then uploads to Netlify via API (ZIP deploy).
    """
    deploy_dir = os.path.join(DIST_DIR, "deploy")
    if os.path.exists(deploy_dir):
        shutil.rmtree(deploy_dir)
    os.makedirs(deploy_dir)

    # 1. Copy Setup File
    src_setup = os.path.join(setup_dir, setup_filename)
    dst_setup = os.path.join(deploy_dir, setup_filename)
    shutil.copy(src_setup, dst_setup)
    log_and_print(f"Copied setup to: {deploy_dir}")

    # 2. Generate version.json
    version_str = get_version()
    # Costruiamo l'URL in base al nome dell'installer come nel file originale
    download_url = f"https://projectjob-bot.netlify.app/{setup_filename}"

    version_data = {"version": version_str, "url": download_url}

    with open(os.path.join(deploy_dir, "version.json"), "w", encoding="utf-8") as f:
        json.dump(version_data, f, indent=4)
    log_and_print(f"Generated version.json (v{version_str})")

    # 3. Generate Landing Page
    generate_index_html(deploy_dir, setup_filename, version_str)

    # 4. Generate netlify.toml to skip post-processing
    netlify_toml = """[build]
  publish = "."

[build.processing]
  skip_processing = true

[build.processing.html]
  pretty_urls = false

[build.processing.images]
  compress = false

[build.processing.js]
  bundle = false
  minify = false

[build.processing.css]
  bundle = false
  minify = false
"""
    with open(os.path.join(deploy_dir, "netlify.toml"), "w", encoding="utf-8") as f:
        f.write(netlify_toml)
    log_and_print("Generated netlify.toml (skip processing enabled)")

    # 5. Netlify Credentials & Upload
    auth_token = get_netlify_token()
    site_id = NETLIFY_SITE_ID

    log_and_print(f"Ready to deploy to Site ID: {site_id}")
    log_and_print("Starting automatic upload to Netlify via ZIP deploy...")

    zip_path = os.path.join(DIST_DIR, "deploy.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, deploy_dir)
                zipf.write(file_path, arcname)
                log_and_print(f"  + Added to zip: {arcname}")

    if os.path.exists(zip_path):
        size_mb = os.path.getsize(zip_path) / (1024 * 1024)
        log_and_print(f"Zip created successfully. Size: {size_mb:.2f} MB")

    try:
        with open(zip_path, "rb") as f:
            data = f.read()

        url = f"https://api.netlify.com/api/v1/sites/{site_id}/deploys"
        headers = {"Content-Type": "application/zip", "Authorization": f"Bearer {auth_token}"}

        response = requests.post(url, headers=headers, data=data, timeout=600)

        if response.status_code == 200:
            log_and_print("-" * 40)
            log_and_print("DEPLOY SUCCESSFUL!", "INFO")
            log_and_print(f"Live URL: {response.json().get('url')}")
            log_and_print(f"Admin Console: {response.json().get('admin_url')}")
            log_and_print("-" * 40)
            return True
        log_and_print(f"Upload Failed: {response.status_code} - {response.text}", "ERROR")
        return False

    except Exception as e:
        log_and_print(f"Error during Netlify upload: {e}", "ERROR")
        return False
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Bot TS Build Script")
    parser.add_argument("--no-deploy", action="store_true", help="Skip Netlify deployment")
    parser.add_argument("--skip-installer", action="store_true", help="Skip Inno Setup")
    parser.add_argument(
        "--debug-no-obfuscate",
        action="store_true",
        help="DEBUG ONLY: Skip PyArmor",
    )
    args = parser.parse_args()

    if os.path.exists(LOG_FILE):
        with contextlib.suppress(OSError):
            os.remove(LOG_FILE)

    log_and_print("=" * 60)
    log_and_print(f"  SYNCROJOB BUILD SCRIPT - v{get_version()}")
    log_and_print("=" * 60)

    ensure_drivers()
    clean_build()

    is_obfuscated = not args.debug_no_obfuscate
    if is_obfuscated:
        run_pyarmor()
    else:
        log_and_print("[WARNING] SKIPPING OBFUSCATION.", "WARNING")

    run_pyinstaller(obfuscated=is_obfuscated)

    setup_filename = None
    if not args.skip_installer:
        run_inno_setup()
        version = get_version()
        setup_filename = f"SyncroJob_Setup_{version}.exe"

    if setup_filename and os.path.exists(os.path.join(SETUP_OUTPUT_DIR, setup_filename)) and not args.no_deploy:
        deploy_success = prepare_and_deploy_netlify(SETUP_OUTPUT_DIR, setup_filename)
        if deploy_success:
            log_and_print("=" * 60)
            log_and_print("BUILD AND PACKAGING COMPLETE SUCCESS!")
            log_and_print("=" * 60)
        else:
            log_and_print("=" * 60)
            log_and_print("BUILD SUCCESSFUL BUT DEPLOY FAILED!")
            log_and_print("=" * 60)
            sys.exit(1)
    elif args.no_deploy:
        log_and_print("[BUILD] Skipping Netlify deployment (--no-deploy)")
        log_and_print("=" * 60)
        log_and_print("BUILD COMPLETED (NO DEPLOY)!")
        log_and_print("=" * 60)
    else:
        log_and_print("[WARNING] Installer missing, skipping deploy.", "WARNING")


if __name__ == "__main__":
    main()
