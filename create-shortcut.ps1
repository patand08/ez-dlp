$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$here = $PSScriptRoot
$desktop = [Environment]::GetFolderPath("Desktop")
$ico = Join-Path $here "assets\icon.ico"
$exe = Join-Path $here "EZ-DLP.exe"
$pythonw = (Get-Command pythonw -ErrorAction SilentlyContinue).Source

if (-not (Test-Path $ico)) {
    throw "Missing icon: $ico"
}

$shell = New-Object -ComObject WScript.Shell

function New-EzdlpShortcut([string]$Path) {
    if (Test-Path $Path) {
        Remove-Item -Force $Path
    }
    $lnk = $shell.CreateShortcut($Path)
    $lnk.WorkingDirectory = $here
    $lnk.WindowStyle = 1
    $lnk.Description = "EZ-DLP - download MP4 and MP3"
    # Windows does not use SVG on .exe/.lnk. The .ico is rasterized from assets/icon.svg.
    $lnk.IconLocation = "$ico,0"
    if (Test-Path $exe) {
        $lnk.TargetPath = $exe
        $lnk.Arguments = ""
    } elseif ($pythonw) {
        $lnk.TargetPath = $pythonw
        $lnk.Arguments = "`"$here\app.py`""
    } else {
        throw "Neither EZ-DLP.exe nor pythonw was found."
    }
    $lnk.Save()
}

New-EzdlpShortcut (Join-Path $here "EZ-DLP.lnk")
New-EzdlpShortcut (Join-Path $desktop "EZ-DLP.lnk")

Write-Host "Shortcut created on the desktop and in this folder: EZ-DLP.lnk"
Write-Host "Icon: $ico"
