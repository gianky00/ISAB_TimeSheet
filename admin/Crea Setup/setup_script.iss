; Bot TS - Inno Setup Script
; Installer configuration for SyncroJob application

#define MyAppName "SyncroJob"
#define MyAppPublisher "Giancarlo Allegretti"
#define MyAppURL "https://bot-ts.netlify.app"
#define MyAppExeName "SyncroJob.exe"

; Read version from version.py (manually update or use preprocessor)
#ifndef MyAppVersion
  #define MyAppVersion "1.0.0"
#endif

; Paths (relative to this script location)
#define SourcePath "..\..\dist\SyncroJob"
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
DefaultDirName={autopf}\SyncroJob
DefaultGroupName=SyncroJob
DisableProgramGroupPage=yes

; Output configuration
OutputDir={#OutputPath}
OutputBaseFilename=SyncroJob_Setup_{#MyAppVersion}
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

[Files]
; Main application files
Source: "{#SourcePath}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Icon file
Source: "{#AssetsPath}\app.ico"; DestDir: "{app}"; Flags: ignoreversion

; Copy all assets (icons, styles, etc.)
Source: "{#AssetsPath}\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Start Menu
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\app.ico"

; Desktop (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\app.ico"; Tasks: desktopicon

[Run]
; Launch after install (optional)
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Non eliminiamo nulla automaticamente per preservare i dati tra versioni.

[Code]
// Custom code for installation logic

function InitializeSetup(): Boolean;
begin
  Result := True;
end;

function InitializeUninstall(): Boolean;
var
  MsgResult: Integer;
begin
  // Chiedi all'utente se vuole pulire TUTTO (Config, Database, Licenza)
  MsgResult := MsgBox('Vuoi eliminare anche tutte le impostazioni, i database e la licenza?' + #13#10 + 
                      'ATTENZIONE: Questa operazione è irreversibile.', 
                      mbConfirmation, MB_YESNO);
  
  if MsgResult = IDYES then
  begin
    // Elimina la cartella in Local (SyncroJob) per coerenza con il codice Python
    DelTree(ExpandConstant('{localappdata}\SyncroJob'), True, True, True);
  end;
  
  Result := True;
end;
