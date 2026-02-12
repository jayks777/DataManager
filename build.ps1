$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

$python = Join-Path $root ".venv\Scripts\python.exe"

& $python -m pip install --upgrade pip
& $python -m pip install -r requirements.txt
& $python -m pip install pyinstaller

$iconCandidates = @(
    "datamanager_app\\assets\\icons\\app.ico",
    "assets\\icons\\app.ico"
)
$iconPath = $iconCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

$args = @("--onefile", "--noconsole", "--name", "DataManager")
if ($iconPath) {
    $args += @("--icon", $iconPath)
}
$assetsIconsDir = "datamanager_app\\assets\\icons"
if (Test-Path $assetsIconsDir) {
    $args += @("--add-data", "$assetsIconsDir;datamanager_app/assets/icons")
}

& $python -m PyInstaller @args datamanager.py

Write-Host "Build concluido: dist\DataManager.exe"
