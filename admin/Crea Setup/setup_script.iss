; Bot TS - Inno Setup Script
; Installer configuration for Bot TS application

#define MyAppName "Bot TS"
#define MyAppPublisher "Giancarlo Allegretti"
#define MyAppURL "https://bot-ts.netlify.app"
#define MyAppExeName "BotTS.exe"

; Read version from version.py (manually update or use preprocessor)
#define MyAppVersion "1.0.0"

; Paths (relative to this script location)
#define SourcePath "..\..\dist\BotTS"
#define OutputPath "Setup"
#define AssetsPath "..\..\assets"

[Setup]
; Application identification
AppId={{8E5F9A2C-7B4D-4E6F-A123-9D8C7E6F5A4B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation paths
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output configuration
OutputDir={#OutputPath}
OutputBaseFilename=BotTS_Setup_{#MyAppVersion}
SetupIconFile={#AssetsPath}\setup.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; Compression
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes

; UI Settings
WizardStyle=modern
WizardSizePercent=110
DisableWelcomePage=no

; Privileges (per-user installation by default)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Misc
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Main application files
Source: "{#SourcePath}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Icon file
Source: "{#AssetsPath}\app.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\app.ico"

; Desktop (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\app.ico"; Tasks: desktopicon

[Run]
; Launch after install (optional)
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up application data on uninstall (optional - commented out to preserve user data)
; Type: filesandordirs; Name: "{localappdata}\Programs\Bot TS"

[Code]
// Custom code for installation logic

function InitializeSetup(): Boolean;
begin
  Result := True;
  // Add any pre-installation checks here
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Post-installation actions
    // e.g., create license directory
    ForceDirectories(ExpandConstant('{localappdata}\Programs\Bot TS\Licenza'));
  end;
end;

function InitializeUninstall(): Boolean;
var
  MsgResult: Integer;
begin
  // Ask about keeping configuration
  MsgResult := MsgBox('Vuoi mantenere le impostazioni e la licenza per un''eventuale reinstallazione?', 
                      mbConfirmation, MB_YESNO);
  
  if MsgResult = IDNO then
  begin
    // User chose to delete everything
    DelTree(ExpandConstant('{localappdata}\Programs\Bot TS'), True, True, True);
  end;
  
  Result := True;
end;
