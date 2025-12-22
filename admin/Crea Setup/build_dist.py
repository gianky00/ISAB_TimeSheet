"""
Bot TS - Build & Distribution Script
Compila l'applicazione con PyInstaller, crea l'installer con Inno Setup,
e opzionalmente deploya su Netlify.
"""
import os
import sys
import shutil
import subprocess
import json
import argparse

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
DIST_DIR = os.path.join(ROOT_DIR, "dist")
BUILD_DIR = os.path.join(ROOT_DIR, "build")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
SETUP_OUTPUT_DIR = os.path.join(SCRIPT_DIR, "Setup")

# Application info
APP_NAME = "Bot TS"
APP_EXE_NAME = "BotTS"
MAIN_SCRIPT = os.path.join(ROOT_DIR, "main.py")
ICON_PATH = os.path.join(ASSETS_DIR, "app.ico")
ISS_SCRIPT = os.path.join(SCRIPT_DIR, "setup_script.iss")

# Netlify config
NETLIFY_SITE_ID = "bot-ts"  # Update with actual site ID


def get_version():
    """Read version from version.py"""
    version_file = os.path.join(ROOT_DIR, "src", "core", "version.py")
    with open(version_file, "r") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split('"')[1]
    return "0.0.0"


def clean_build():
    """Remove previous build artifacts."""
    print("[BUILD] Cleaning previous builds...")
    for folder in [DIST_DIR, BUILD_DIR]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  Removed: {folder}")


def run_pyinstaller():
    """Build executable with PyInstaller."""
    print("[BUILD] Running PyInstaller...")
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", APP_EXE_NAME,
        "--onedir",
        "--windowed",
        "--noconfirm",
        "--clean",
        # Add data files
        "--add-data", f"{os.path.join(ROOT_DIR, 'src')};src",
    ]
    
    # Add icon if exists
    if os.path.exists(ICON_PATH):
        cmd.extend(["--icon", ICON_PATH])
    
    # Hidden imports for PyQt6 and selenium
    hidden_imports = [
        "PyQt6.QtWidgets",
        "PyQt6.QtCore",
        "PyQt6.QtGui",
        "selenium.webdriver",
        "selenium.webdriver.chrome.service",
        "selenium.webdriver.chrome.options",
        "webdriver_manager.chrome",
        "cryptography.fernet",
        "packaging.version",
        "platformdirs",
    ]
    
    for imp in hidden_imports:
        cmd.extend(["--hidden-import", imp])
    
    # Collect all submodules
    cmd.extend(["--collect-submodules", "selenium"])
    cmd.extend(["--collect-submodules", "webdriver_manager"])
    
    # Main script
    cmd.append(MAIN_SCRIPT)
    
    # Run PyInstaller
    result = subprocess.run(cmd, cwd=ROOT_DIR)
    
    if result.returncode != 0:
        print("[ERROR] PyInstaller failed!")
        sys.exit(1)
    
    print("[BUILD] PyInstaller completed successfully.")


def run_inno_setup():
    """Build installer with Inno Setup."""
    print("[BUILD] Running Inno Setup...")
    
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
        print("[WARNING] Inno Setup not found. Skipping installer creation.")
        return False
    
    # Create output directory
    if not os.path.exists(SETUP_OUTPUT_DIR):
        os.makedirs(SETUP_OUTPUT_DIR)
    
    # Get version for Inno Setup
    version = get_version()
    print(f"[BUILD] Building installer for version: {version}")

    # Run ISCC
    cmd = [iscc, f"/DMyAppVersion={version}", ISS_SCRIPT]
    result = subprocess.run(cmd, cwd=SCRIPT_DIR)
    
    if result.returncode != 0:
        print("[ERROR] Inno Setup failed!")
        return False
    
    print("[BUILD] Installer created successfully.")
    return True


def create_version_json():
    """Create version.json for update checking."""
    print("[BUILD] Creating version.json...")
    
    version = get_version()
    
    # Create netlify directory
    netlify_dir = os.path.join(SETUP_OUTPUT_DIR, "netlify")
    if not os.path.exists(netlify_dir):
        os.makedirs(netlify_dir)
    
    version_json = {
        "version": version,
        "url": f"https://bot-ts.netlify.app/BotTS_Setup_{version}.exe"
    }
    
    # Write version.json
    json_path = os.path.join(netlify_dir, "version.json")
    with open(json_path, "w") as f:
        json.dump(version_json, f, indent=2)
    
    # Copy installer to netlify folder
    version = get_version()
    installer_name = f"BotTS_Setup_{version}.exe"
    src_installer = os.path.join(SETUP_OUTPUT_DIR, installer_name)
    
    if os.path.exists(src_installer):
        shutil.copy2(src_installer, os.path.join(netlify_dir, installer_name))
        print(f"  Copied installer to netlify folder")
    
    # Create professional index.html
    index_html = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot TS - Download</title>
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
        <h1>🤖 Bot TS</h1>
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
    
    print(f"[BUILD] version.json created: v{version}")
    return netlify_dir


def deploy_netlify(netlify_dir):
    """Deploy to Netlify."""
    print("[BUILD] Deploying to Netlify...")
    
    # Check if netlify CLI is available
    try:
        subprocess.run(["netlify", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[WARNING] Netlify CLI not found. Install with: npm install -g netlify-cli")
        return False
    
    # Deploy
    cmd = [
        "netlify", "deploy",
        "--prod",
        "--dir", netlify_dir,
        "--site", NETLIFY_SITE_ID
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode != 0:
        print("[ERROR] Netlify deploy failed!")
        return False
    
    print("[BUILD] Deployed to Netlify successfully.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Bot TS Build Script")
    parser.add_argument("--no-deploy", action="store_true", help="Skip Netlify deployment")
    parser.add_argument("--skip-installer", action="store_true", help="Skip Inno Setup")
    args = parser.parse_args()
    
    print("=" * 60)
    print(f"  BOT TS BUILD SCRIPT - v{get_version()}")
    print("=" * 60)
    
    # Step 1: Clean
    clean_build()
    
    # Step 2: PyInstaller
    run_pyinstaller()
    
    # Step 3: Inno Setup
    if not args.skip_installer:
        run_inno_setup()
    
    # Step 4: Create version.json
    netlify_dir = create_version_json()
    
    # Step 5: Deploy (optional)
    if not args.no_deploy:
        deploy_netlify(netlify_dir)
    else:
        print("[BUILD] Skipping Netlify deployment (--no-deploy)")
    
    print("=" * 60)
    print("  BUILD COMPLETED!")
    print("=" * 60)


if __name__ == "__main__":
    main()
