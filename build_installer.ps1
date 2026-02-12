$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

# Build the exe first
& .\build.ps1

# Run Inno Setup
if (-not (Get-Command iscc.exe -ErrorAction SilentlyContinue)) {
    throw "Inno Setup nao encontrado. Instale o Inno Setup e adicione iscc.exe ao PATH."
}

& iscc ".\installer\DataManager.iss"

Write-Host "Installer gerado em: installer\\output\\DataManagerSetup.exe"
