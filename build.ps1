$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$assets = Join-Path $PSScriptRoot "assets"
$ico = Join-Path $assets "icon.ico"
if (-not (Test-Path $ico)) {
    throw "Missing icon: $ico"
}

python -m pip install -r requirements.txt
python -m PyInstaller `
    --noconfirm --clean --windowed --onefile `
    --name "EZ-DLP" `
    --icon $ico `
    --add-data "$assets;assets" `
    --distpath $PSScriptRoot `
    --workpath (Join-Path $PSScriptRoot "build") `
    --specpath (Join-Path $PSScriptRoot "build") `
    (Join-Path $PSScriptRoot "app.py")

if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

if (Test-Path ".\EZ-DLP.exe") {
    & "$PSScriptRoot\create-shortcut.ps1"
    Write-Host ""
    Write-Host "Done. Click the EZ-DLP desktop shortcut (or EZ-DLP.exe in this folder)."
}
