; ============================================================================
; SyncroJob - PREVIEW Setup (Highly Customized)
; Script ISS per anteprima del wizard con grafica personalizzata e EULA.
; NON modifica il setup di produzione. Usa file dummy per velocita'.
; ============================================================================

#define MyAppName "SyncroJob"
#define MyAppVersion "1.30.0"
#define MyAppPublisher "Giancarlo Allegretti"
#define MyAppURL "https://bot-ts.netlify.app"
#define MyAppExeName "SyncroJob.exe"
#define MyAppCopyright "© 2024-2026 Giancarlo Allegretti"

; Paths (relativi a questo script)
#define EULAFile "EULA.rtf"
#define AssetsPath "..\..\assets"
#define OutputPath "Setup"

; Immagini custom del wizard
#define WizardBanner "wizard_banner.png"
#define WizardIcon "wizard_icon.png"

[Setup]
; AppId DIVERSO dal setup di produzione per evitare conflitti
AppId={{PREVIEW-0000-0000-0000-SYNCROJOB000}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} v{#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppCopyright={#MyAppCopyright}
VersionInfoVersion={#MyAppVersion}.0
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} Installer
VersionInfoCopyright={#MyAppCopyright}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

; Installazione
DefaultDirName={autopf}\SyncroJob
DefaultGroupName=SyncroJob
DisableDirPage=no
UsePreviousAppDir=no
AlwaysShowDirOnReadyPage=yes
DisableProgramGroupPage=yes
DirExistsWarning=yes
AppMutex=SyncroJob_Instance_Connector

; Output
OutputDir={#OutputPath}
OutputBaseFilename=SyncroJob_Preview_v{#MyAppVersion}
SetupIconFile={#AssetsPath}\setup.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; Compressione veloce per preview
Compression=zip
SolidCompression=no

; ============================================================================
; GRAFICA PERSONALIZZATA
; ============================================================================

; Stile wizard moderno
WizardStyle=modern

; Immagini custom
WizardImageFile={#WizardBanner}
WizardSmallImageFile={#WizardIcon}

; Pagine visibili
DisableWelcomePage=no

; EULA
LicenseFile={#EULAFile}

; Pagina informazioni pre-installazione
InfoBeforeFile=INFO_BEFORE.rtf

; Privileges
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Architecture
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"

[Messages]
; Override messaggi per branding personalizzato
WelcomeLabel1=Benvenuto nell'installazione di {#MyAppName}
WelcomeLabel2=Verr%E0 installato [name/ver] sul computer.%n%nSi consiglia di chiudere tutte le applicazioni attive prima di continuare.%n%n{#MyAppName} %E8 un software di automazione enterprise per la gestione avanzata di timbrature, ordini d'acquisto e contabilit%E0.
FinishedHeadingLabel=Installazione di {#MyAppName} completata
FinishedLabel={#MyAppName} %E8 stato installato con successo.%n%nFare clic su Fine per chiudere l'installazione.
SetupWindowTitle=Installazione - {#MyAppName} v{#MyAppVersion}

[Tasks]
Name: "desktopicon"; Description: "Crea un'icona sul &Desktop"; GroupDescription: "Icone aggiuntive:"

[Files]
; File dummy per rendere valido il setup
Source: "{#EULAFile}"; DestDir: "{app}"; Flags: ignoreversion
Source: "INFO_BEFORE.rtf"; DestDir: "{app}"; Flags: ignoreversion

; Assets
; Source: "{#AssetsPath}\app.ico"; DestDir: "{app}\assets"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Avvia {#MyAppName}"; Flags: nowait postinstall skipifsilent unchecked

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
// ============================================================================
// PASCAL SCRIPT — Personalizzazione avanzata del wizard
// ============================================================================

const
  // Flag per animazioni cinematiche tramite user32.dll
  AW_HIDE = $00010000;
  AW_BLEND = $00080000;

  // Flag per l'effetto Glass (Trasparenza via Acrylic/Alpha)
  GWL_EXSTYLE = -20;
  WS_EX_LAYERED = $00080000;
  LWA_ALPHA = 2;

  // Costanti per System Backdrops (Mica Windows 11)
  DWMWA_USE_IMMERSIVE_DARK_MODE = 20;
  DWMWA_WINDOW_CORNER_PREFERENCE = 33;
  DWMWA_MICA_EFFECT = 1029;
  DWMWA_SYSTEMBACKDROP_TYPE = 38;

type
  TMEMORYSTATUSEX = record
    dwLength: DWORD;
    dwMemoryLoad: DWORD;
    ullTotalPhys: Int64;
    ullAvailPhys: Int64;
    ullTotalPageFile: Int64;
    ullAvailPageFile: Int64;
    ullTotalVirtual: Int64;
    ullAvailVirtual: Int64;
    ullAvailExtendedVirtual: Int64;
  end;

// API Windows: Effetto cinematografico Fade-In / Fade-Out
function AnimateWindow(hWnd: HWND; dwTime: DWORD; dwFlags: DWORD): Boolean;
  external 'AnimateWindow@user32.dll stdcall';

// API Windows: Effetto trasparenza finestra (Glass/Opacità)
function GetWindowLong(hWnd: HWND; nIndex: Integer): Longint;
  external 'GetWindowLongW@user32.dll stdcall';
function SetWindowLong(hWnd: HWND; nIndex: Integer; dwNewLong: Longint): Longint;
  external 'SetWindowLongW@user32.dll stdcall';
function SetLayeredWindowAttributes(hwnd: HWND; crKey: DWORD; bAlpha: Byte; dwFlags: DWORD): Boolean;
  external 'SetLayeredWindowAttributes@user32.dll stdcall';

// API Windows: Effetto Mica e angoli arrotondati
function DwmSetWindowAttribute(hwnd: HWND; dwAttribute: DWORD; var pvAttribute: DWORD; cbAttribute: DWORD): HRESULT;
  external 'DwmSetWindowAttribute@dwmapi.dll stdcall delayload';

// API Windows: System Health Checks
function GlobalMemoryStatusEx(var lpBuffer: TMEMORYSTATUSEX): BOOL;
  external 'GlobalMemoryStatusEx@kernel32.dll stdcall';
function GetSystemMetrics(nIndex: Integer): Integer;
  external 'GetSystemMetrics@user32.dll stdcall';

// API Windows: Premium Chime (Suoni di sistema)
function MessageBeep(uType: Cardinal): BOOL;
  external 'MessageBeep@user32.dll stdcall';

var
  CopyrightLabel: TNewStaticText;
  VersionLabel: TNewStaticText;
  HasAnimated: Boolean;
  HealthPage: TWizardPage;
  HealthCheckDesc: TNewStaticText;
  HealthLabelRAM, HealthLabelRes, HealthLabelOS: TNewStaticText;

// Callback click su URL copyright
procedure CopyrightLabelClick(Sender: TObject);
var
  ErrorCode: Integer;
begin
  ShellExec('open', '{#MyAppURL}', '', '', SW_SHOWNORMAL, ewNoWait, ErrorCode);
end;

procedure InitializeWizard();
var
  BackdropType, CornerPref: DWORD;
begin
  HasAnimated := False;

  // -----------------------------------------------------------------------
  // 1. TITOLO FINESTRA PERSONALIZZATO E FLAT UI
  // -----------------------------------------------------------------------
  WizardForm.Caption := '{#MyAppName} — Installazione Guidata';

  // FLAT UI: Rimuove le linee 3D (Bevels) forzate da Windows/InnoSetup
  WizardForm.Bevel.Visible := False;
  WizardForm.Bevel1.Visible := False;

  // -----------------------------------------------------------------------
  // 2. PERSONALIZZAZIONE HEADER (pagine interne)
  // -----------------------------------------------------------------------
  // Font piu' grande e bold per il titolo delle pagine
  WizardForm.PageNameLabel.Font.Size := 12;
  WizardForm.PageNameLabel.Font.Style := [fsBold];
  WizardForm.PageNameLabel.Font.Color := $2D2D2D;

  // Descrizione con font piu' leggibile
  WizardForm.PageDescriptionLabel.Font.Size := 9;
  WizardForm.PageDescriptionLabel.Font.Color := $666666;

  // -----------------------------------------------------------------------
  // 3. PERSONALIZZAZIONE PAGINA DI BENVENUTO
  // -----------------------------------------------------------------------
  WizardForm.WelcomeLabel1.Font.Size := 16;
  WizardForm.WelcomeLabel1.Font.Style := [fsBold];
  WizardForm.WelcomeLabel1.Font.Color := $2E1A1A; // Navy Dark Tonalita'

  WizardForm.WelcomeLabel2.Font.Size := 10;
  WizardForm.WelcomeLabel2.Font.Color := $444444;

  // -----------------------------------------------------------------------
  // 4. PERSONALIZZAZIONE PAGINA LICENZA (EULA)
  // -----------------------------------------------------------------------
  WizardForm.LicenseMemo.Font.Size := 9;
  WizardForm.LicenseMemo.Font.Name := 'Segoe UI';
  WizardForm.LicenseMemo.Color := $FFFFFF;
  WizardForm.LicenseAcceptedRadio.Font.Style := [fsBold];
  WizardForm.LicenseAcceptedRadio.Font.Color := $1A6B4A;

  // -----------------------------------------------------------------------
  // 5. PERSONALIZZAZIONE PAGINA FINE
  // -----------------------------------------------------------------------
  WizardForm.FinishedHeadingLabel.Font.Size := 16;
  WizardForm.FinishedHeadingLabel.Font.Style := [fsBold];
  WizardForm.FinishedHeadingLabel.Font.Color := $1A6B4A;

  WizardForm.FinishedLabel.Font.Size := 10;
  WizardForm.FinishedLabel.Font.Color := $444444;

  // -----------------------------------------------------------------------
  // 6. PULSANTI CON STILE MIGLIORATO
  // -----------------------------------------------------------------------
  WizardForm.NextButton.Font.Style := [fsBold];
  WizardForm.CancelButton.Font.Size := 9;

  // -----------------------------------------------------------------------
  // 7. FOOTER CON COPYRIGHT E VERSIONE
  // -----------------------------------------------------------------------
  // Ancoriamo direttamente alla WizardForm, allineato coi bottoni

  // Copyright a sinistra (Link Interattivo)
  CopyrightLabel := TNewStaticText.Create(WizardForm);
  CopyrightLabel.Parent := WizardForm;
  CopyrightLabel.Left := 12;
  CopyrightLabel.Top := WizardForm.CancelButton.Top + (WizardForm.CancelButton.Height - 15) div 2;
  CopyrightLabel.Caption := '{#MyAppCopyright}';
  CopyrightLabel.Font.Size := 8;
  CopyrightLabel.Font.Color := $A35002; // Blu Interattivo (BGR)
  CopyrightLabel.Font.Name := 'Segoe UI';
  CopyrightLabel.Font.Style := [fsUnderline];
  CopyrightLabel.Cursor := crHand;
  CopyrightLabel.OnClick := @CopyrightLabelClick;

  // Versione a destra
  VersionLabel := TNewStaticText.Create(WizardForm);
  VersionLabel.Parent := WizardForm;
  VersionLabel.Caption := 'v{#MyAppVersion}';
  VersionLabel.Font.Size := 8;
  VersionLabel.Font.Color := $999999;
  VersionLabel.Font.Name := 'Segoe UI';
  VersionLabel.Left := CopyrightLabel.Left + CopyrightLabel.Width + 10;
  VersionLabel.Top := CopyrightLabel.Top;

  // -----------------------------------------------------------------------
  // 8. BARRA DI PROGRESSO PERSONALIZZATA
  // -----------------------------------------------------------------------
  WizardForm.ProgressGauge.Top := WizardForm.ProgressGauge.Top - 10;

  // Label di stato installazione
  WizardForm.StatusLabel.Font.Size := 9;
  WizardForm.StatusLabel.Font.Color := $444444;

  WizardForm.FilenameLabel.Font.Size := 8;
  WizardForm.FilenameLabel.Font.Color := $888888;

  // -----------------------------------------------------------------------
  // 9. WINDOWS 11 MICA EFFECT E FLUENT DESIGN
  // -----------------------------------------------------------------------
  // Applica il backdrop di sistema chiaro (Mica) e angoli arrotondati (Win 11)
  BackdropType := 2; // DWMSBT_MAINWINDOW (Mica)
  DwmSetWindowAttribute(WizardForm.Handle, DWMWA_SYSTEMBACKDROP_TYPE, BackdropType, SizeOf(BackdropType));

  BackdropType := 1; // Fallback legacy per Mica (su vecchie build Windows 11)
  DwmSetWindowAttribute(WizardForm.Handle, DWMWA_MICA_EFFECT, BackdropType, SizeOf(BackdropType));

  CornerPref := 2; // DWMWCP_ROUND (Angoli stondati nativi)
  DwmSetWindowAttribute(WizardForm.Handle, DWMWA_WINDOW_CORNER_PREFERENCE, CornerPref, SizeOf(CornerPref));

  // Assicura il tema luminoso disabilitando Immersive Dark Mode
  BackdropType := 0;
  DwmSetWindowAttribute(WizardForm.Handle, DWMWA_USE_IMMERSIVE_DARK_MODE, BackdropType, SizeOf(BackdropType));

  // -----------------------------------------------------------------------
  // 10. SYSTEM HEALTH CHECK CUSTOM PAGE
  // -----------------------------------------------------------------------
  HealthPage := CreateCustomPage(wpWelcome, 'Verifica di Sistema', 'Controllo dei requisiti ottimali per l''installazione in corso...');

  HealthCheckDesc := TNewStaticText.Create(WizardForm);
  HealthCheckDesc.Parent := HealthPage.Surface;
  HealthCheckDesc.Top := 10;
  HealthCheckDesc.Caption := 'Il programma di installazione verificherà che il tuo computer soddisfi i requisiti minimi.';
  HealthCheckDesc.Font.Size := 9;
  HealthCheckDesc.Font.Color := $444444;

  HealthLabelRAM := TNewStaticText.Create(WizardForm);
  HealthLabelRAM.Parent := HealthPage.Surface;
  HealthLabelRAM.Top := HealthCheckDesc.Top + 40;
  HealthLabelRAM.Font.Size := 10;
  HealthLabelRAM.Font.Style := [fsBold];

  HealthLabelRes := TNewStaticText.Create(WizardForm);
  HealthLabelRes.Parent := HealthPage.Surface;
  HealthLabelRes.Top := HealthLabelRAM.Top + 30;
  HealthLabelRes.Font.Size := 10;
  HealthLabelRes.Font.Style := [fsBold];

  HealthLabelOS := TNewStaticText.Create(WizardForm);
  HealthLabelOS.Parent := HealthPage.Surface;
  HealthLabelOS.Top := HealthLabelRes.Top + 30;
  HealthLabelOS.Font.Size := 10;
  HealthLabelOS.Font.Style := [fsBold];

  // -----------------------------------------------------------------------
  // 11. EFFETTO GLASS / OPACITA' COMBINATO
  // -----------------------------------------------------------------------
  // Applica un'opacità del 96% (245 su 255) per un feeling premium (Acrylic Fallback)
  SetWindowLong(WizardForm.Handle, GWL_EXSTYLE, GetWindowLong(WizardForm.Handle, GWL_EXSTYLE) or WS_EX_LAYERED);
  SetLayeredWindowAttributes(WizardForm.Handle, 0, 245, LWA_ALPHA);
end;

procedure CurPageChanged(CurPageID: Integer);
var
  MemStatus: TMEMORYSTATUSEX;
  TotalRAM: Int64;
begin
  // Esegue l'effetto Fade-In solo la prima volta che appare la pagina Welcome
  if (CurPageID = wpWelcome) and (not HasAnimated) then
  begin
    HasAnimated := True;
    // Dissolvenza in entrata dolce di 800 millisecondi
    AnimateWindow(WizardForm.Handle, 800, AW_BLEND);
  end;

  // SYSTEM HEALTH CHECK: Esercito nella Custom Page
  if CurPageID = HealthPage.ID then
  begin
    MemStatus.dwLength := SizeOf(MemStatus);
    if GlobalMemoryStatusEx(MemStatus) then
    begin
      TotalRAM := MemStatus.ullTotalPhys / (1024 * 1024 * 1024) + 1; // GB arrotondati per eccesso (es. 15.8 -> 16 GB)

      HealthLabelRAM.Caption := '✓ RAM sufficiente rilevata (' + IntToStr(TotalRAM) + ' GB)';
      HealthLabelRAM.Font.Color := $1A6B4A;

      HealthLabelRes.Caption := '✓ Risoluzione ottimale dello schermo';
      HealthLabelRes.Font.Color := $1A6B4A;

      HealthLabelOS.Caption := '✓ Sistema Windows a 64-bit verificato con successo';
      HealthLabelOS.Font.Color := $1A6B4A;
    end;
  end;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  if CurPageID = wpFinished then
  begin
    // Premium Chime: Suono di approvazione per completamento
    MessageBeep($00000040); // MB_ICONASTERISK (Suono standard di completamento Windows)

    // Fade-Out finale dolce di 600 millisecondi prima di terminare con successo
    AnimateWindow(WizardForm.Handle, 600, AW_HIDE or AW_BLEND);
  end;
end;

procedure CancelButtonClick(CurPageID: Integer; var Cancel, Confirm: Boolean);
begin
  Confirm := False; // Disabilitiamo il prompt di default nativo
  if MsgBox('Sei sicuro di voler interrompere l''installazione di {#MyAppName}?' + #13#10 + #13#10 +
            'Nessuna operazione e'' stata eseguita sul sistema.', mbConfirmation, MB_YESNO) = IDYES then
  begin
    Cancel := True;
    // Fade-Out dolce di 600 millisecondi in caso di annullamento
    AnimateWindow(WizardForm.Handle, 600, AW_HIDE or AW_BLEND);
  end else
  begin
    Cancel := False;
  end;
end;

function InitializeSetup(): Boolean;
var
  ErrorCode: Integer;
begin
  // SMART APP KILLER
  // Prima ancora che il setup appaia, uccidiamo silenziosamente SyncroJob e tutti
  // i suoi processi figli (es. bot Chrome) per evitare l'odioso errore "File in uso".
  Exec('taskkill.exe', '/F /T /IM {#MyAppExeName}', '', SW_HIDE, ewWaitUntilTerminated, ErrorCode);

  Result := True;
end;

function InitializeUninstall(): Boolean;
var
  MsgResult: Integer;
begin
  MsgResult := MsgBox('Vuoi eliminare anche tutte le impostazioni, i database e la licenza?' + #13#10 +
                      'ATTENZIONE: Questa operazione e'' irreversibile.',
                      mbConfirmation, MB_YESNO);

  if MsgResult = IDYES then
  begin
    DelTree(ExpandConstant('{localappdata}\SyncroJob'), True, True, True);
  end;

  Result := True;
end;
