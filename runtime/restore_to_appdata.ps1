# Ripristina lo snapshot runtime/ in %LOCALAPPDATA%\SyncroJob
# Eseguire dopo git clone su un PC nuovo, prima di avviare SyncroJob.

$ErrorActionPreference = "Stop"

$source = $PSScriptRoot
$destination = Join-Path $env:LOCALAPPDATA "SyncroJob"

Write-Host "Ripristino SyncroJob runtime"
Write-Host "  da: $source"
Write-Host "  a:  $destination"

New-Item -ItemType Directory -Path $destination -Force | Out-Null

Get-ChildItem -LiteralPath $source -Force | Where-Object {
    $_.Name -ne "restore_to_appdata.ps1"
} | ForEach-Object {
    $target = Join-Path $destination $_.Name
    Copy-Item -LiteralPath $_.FullName -Destination $target -Recurse -Force
    Write-Host "  copiato $($_.Name)"
}

Write-Host "Ripristino completato."
Write-Host "Sul PC nuovo genera una licenza con devtools\gui\Crea Licenze\avvia_license_gui.bat"
