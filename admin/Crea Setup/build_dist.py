"""
Bot TS - Build & Distribution Script
Compila l'applicazione con PyInstaller, crea l'installer con Inno Setup,
e opzionalmente deploya su Netlify.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys

# Add admin folder to path to import analyzer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analyze_dependencies import get_all_imports  # noqa: E402

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
DIST_DIR = os.path.join(ROOT_DIR, "dist")
BUILD_DIR = os.path.join(ROOT_DIR, "build")
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
NETLIFY_SITE_ID = "2b481f10-fbd1-44d4-81ed-1a15b15c315b"  # Updated with correct API ID


def log(message):
    """Log message to console and file."""
    print(message)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(str(message) + "\n")
    except Exception:
        pass


def run_command(cmd, cwd=None, shell=False, check=True):
    """Run command and log output."""
    if cwd is None:
        cwd = ROOT_DIR

    cmd_str = " ".join(cmd) if isinstance(cmd, list) else cmd
    log(f"\n[EXEC] {cmd_str}")

    try:
        # Open file in append mode to redirect stdout
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            # We want to stream to console AND file.
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

            for line in process.stdout:
                sys.stdout.write(line)
                f.write(line)
                f.flush()

            return_code = process.wait()

            if check and return_code != 0:
                log(f"[ERROR] Command failed with return code {return_code}")
                sys.exit(1)
            return return_code

    except Exception as e:
        log(f"[EXCEPTION] {e}")
        if check:
            sys.exit(1)
        return 1


def get_version():
    """Read version from version.py"""
    version_file = os.path.join(ROOT_DIR, "src", "core", "version.py")
    try:
        with open(version_file, "r") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split('"')[1]
    except Exception:
        pass
    return "0.0.0"


def clean_build():
    """Remove previous build artifacts."""
    log("[BUILD] Cleaning previous builds...")
    for folder in [DIST_DIR, BUILD_DIR]:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
                log(f"  Removed: {folder}")
            except Exception as e:
                log(f"  Error removing {folder}: {e}")


def run_pyarmor():
    """Obfuscate scripts using PyArmor."""
    log("[BUILD] Running PyArmor obfuscation...")

    if not os.path.exists(OBF_DIR):
        os.makedirs(OBF_DIR)

    # PyArmor gen command
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

    # Use shell=True specifically for Windows if pyarmor is a bat/cmd shim
    run_command(cmd, cwd=ROOT_DIR, shell=(os.name == "nt"))
    log("[BUILD] PyArmor obfuscation completed.")


def run_pyinstaller(obfuscated=False):
    """Build executable with PyInstaller."""
    log(f"[BUILD] Running PyInstaller (Obfuscated: {obfuscated})...")

    # Determine paths based on obfuscation
    if obfuscated:
        script_path = os.path.join(OBF_DIR, "main.py")
        src_path = os.path.join(OBF_DIR, "src")
        # Validate existence
        if not os.path.exists(script_path):
            log(f"[ERROR] Obfuscated script not found: {script_path}")
            sys.exit(1)
    else:
        script_path = MAIN_SCRIPT
        src_path = os.path.join(ROOT_DIR, "src")

    # PyInstaller command
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
        # Add data files
        "--add-data",
        f"{src_path};src",
        "--add-data",
        f"{os.path.join(ROOT_DIR, 'assets')};assets",
    ]

    # Add icon if exists
    if os.path.exists(ICON_PATH):
        cmd.extend(["--icon", ICON_PATH])

    # --- AUTOMATIC DEPENDENCY ANALYSIS ---
    log("[BUILD] Analyzing source code for dependencies...")

    # Capture analyzer output to log as well?
    # Since get_all_imports prints to stdout, we might want to capture it.
    # But for now let's just run it. The user will see output in console.
    # To properly log it we'd need to redirect stdout during this call.
    # We will trust the console output for this part or wrap it later if needed.

    try:
        detected_imports = get_all_imports(MAIN_SCRIPT, os.path.join(ROOT_DIR, "src"))
        log(f"[BUILD] Detected {len(detected_imports)} hidden imports.")
    except Exception as e:
        log(f"[ERROR] Dependency analysis failed: {e}")
        detected_imports = []

    # FIX: Filter out internal/redundant modules that cause "Hidden import not found" errors
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

    # FIX: Exclude unnecessary Qt modules to reduce size and warnings
    qt_excludes = [
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

    # Collect all submodules for complex packages
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

    # Force collect all data for critical packages
    force_collect = [
        "pandera",
        "telegram",
        "markdown",
        "matplotlib",
        "cryptography",
    ]
    for pkg in force_collect:
        cmd.extend(["--collect-all", pkg])

    # Main script
    cmd.append(script_path)

    # Run PyInstaller
    run_command(cmd, cwd=ROOT_DIR)
    log("[BUILD] PyInstaller completed successfully.")


def run_inno_setup():
    """Build installer with Inno Setup."""
    log("[BUILD] Running Inno Setup...")

    # Find Inno Setup compiler
    inno_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
    ]

    iscc = None
    for path in inno_paths:
        if os.path.exists(path):
            iscc = path
            break

    if not iscc:
        log("[WARNING] Inno Setup not found. Skipping installer creation.")
        return False

    # Create output directory
    if not os.path.exists(SETUP_OUTPUT_DIR):
        os.makedirs(SETUP_OUTPUT_DIR)

    # Get version for Inno Setup
    version = get_version()
    log(f"[BUILD] Building installer for version: {version}")

    # Run ISCC
    cmd = [iscc, f"/DMyAppVersion={version}", ISS_SCRIPT]

    # Inno Setup might not print much to stdout/stderr in a way that is useful to capture line-by-line
    # but we will try.
    run_command(cmd, cwd=SCRIPT_DIR)

    log("[BUILD] Installer created successfully.")
    return True


def create_version_json():
    """Create version.json for update checking."""
    log("[BUILD] Creating version.json...")

    version = get_version()

    # Create netlify directory
    netlify_dir = os.path.join(SETUP_OUTPUT_DIR, "netlify")
    if not os.path.exists(netlify_dir):
        os.makedirs(netlify_dir)

    version_json = {
        "version": version,
        "url": f"https://syncrojob.netlify.app/SyncroJob_Setup_{version}.exe",
    }

    # Write version.json
    json_path = os.path.join(netlify_dir, "version.json")
    with open(json_path, "w") as f:
        json.dump(version_json, f, indent=2)

    # Copy installer to netlify folder
    version = get_version()
    installer_name = f"SyncroJob_Setup_{version}.exe"
    src_installer = os.path.join(SETUP_OUTPUT_DIR, installer_name)

    if os.path.exists(src_installer):
        shutil.copy2(src_installer, os.path.join(netlify_dir, installer_name))
        log("  Copied installer to netlify folder")

    # Create professional index.html
    index_html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SyncroJob - Download</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }}
        .container {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            text-align: center;
            max-width: 500px;
            width: 90%;
        }}
        h1 {{
            margin-bottom: 0.5rem;
            font-size: 2.5rem;
        }}
        p {{
            font-size: 1.1rem;
            opacity: 0.9;
            margin-bottom: 2rem;
        }}
        .btn {{
            display: inline-block;
            background: #fff;
            color: #764ba2;
            padding: 15px 30px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: bold;
            font-size: 1.2rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            background: #f8f9fa;
        }}
        .version {{
            margin-top: 1.5rem;
            font-size: 0.9rem;
            opacity: 0.7;
        }}
        .loader {{
            border: 3px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top: 3px solid #fff;
            width: 20px;
            height: 20px;
            -webkit-animation: spin 1s linear infinite; /* Safari */
            animation: spin 1s linear infinite;
            display: inline-block;
            margin-right: 10px;
            vertical-align: middle;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
    <meta http-equiv="refresh" content="2; url={installer_name}">
</head>
<body>
    <div class="container">
        <h1>🚀 SyncroJob</h1>
        <p>Il download inizierà automaticamente tra pochi secondi...</p>

        <a href="{installer_name}" class="btn">
            Scarica manualmente
        </a>

        <div class="version">
            <div class="loader"></div>
            Versione {version}
        </div>
    </div>
</body>
</html>
"""
    with open(os.path.join(netlify_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    log(f"[BUILD] version.json created: v{version}")
    return netlify_dir


def deploy_netlify(netlify_dir):
    """Deploy to Netlify."""
    log("[BUILD] Deploying to Netlify...")

    # Check if netlify CLI is available
    try:
        subprocess.run(["netlify", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        log("[WARNING] Netlify CLI not found. Install with: npm install -g netlify-cli")
        return False

    # Deploy
    cmd = [
        "netlify",
        "deploy",
        "--prod",
        "--dir",
        netlify_dir,
        "--site",
        NETLIFY_SITE_ID,
    ]

    run_command(cmd)
    log("[BUILD] Deployed to Netlify successfully.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Bot TS Build Script")
    parser.add_argument(
        "--no-deploy", action="store_true", help="Skip Netlify deployment"
    )
    parser.add_argument("--skip-installer", action="store_true", help="Skip Inno Setup")
    # PyArmor is now mandatory/standard. Added a skip flag only for debugging if absolutely needed,
    # but the default flow involves obfuscation.
    parser.add_argument(
        "--debug-no-obfuscate",
        action="store_true",
        help="DEBUG ONLY: Skip PyArmor (Not for production)",
    )
    args = parser.parse_args()

    # Clear log file
    if os.path.exists(LOG_FILE):
        try:
            os.remove(LOG_FILE)
        except OSError:
            pass

    log("=" * 60)
    log(f"  SYNCROJOB BUILD SCRIPT - v{get_version()}")
    log("=" * 60)

    # Step 1: Clean
    clean_build()

    # Step 2: Obfuscation (Standard/Mandatory)
    is_obfuscated = True
    if args.debug_no_obfuscate:
        log(
            "[WARNING] SKIPPING OBFUSCATION (Debug Mode). This build is NOT for distribution."
        )
        is_obfuscated = False
    else:
        run_pyarmor()

    # Step 3: PyInstaller
    run_pyinstaller(obfuscated=is_obfuscated)

    # Step 4: Inno Setup
    if not args.skip_installer:
        run_inno_setup()

    # Step 4: Create version.json
    netlify_dir = create_version_json()

    # Step 5: Deploy (optional)
    if not args.no_deploy:
        deploy_netlify(netlify_dir)
    else:
        log("[BUILD] Skipping Netlify deployment (--no-deploy)")

    log("=" * 60)
    log("  BUILD COMPLETED!")
    log("=" * 60)


if __name__ == "__main__":
    main()
