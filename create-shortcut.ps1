$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$here = $PSScriptRoot
$desktop = [Environment]::GetFolderPath("Desktop")
$ico = Join-Path $here "assets\icon.ico"
$exe = Join-Path $here "EZ-DLP.exe"
$pythonw = (Get-Command pythonw -ErrorAction SilentlyContinue).Source

$shell = New-Object -ComObject WScript.Shell

function New-EzdlpShortcut([string]$Path) {
    $lnk = $shell.CreateShortcut($Path)
    $lnk.WorkingDirectory = $here
    $lnk.WindowStyle = 1
    $lnk.Description = "EZ-DLP - download MP4 and MP3"
    if (Test-Path $exe) {
        $lnk.TargetPath = $exe
        $lnk.Arguments = ""
        $lnk.IconLocation = "$exe,0"
    } elseif ($pythonw) {
        $lnk.TargetPath = $pythonw
        $lnk.Arguments = "`"$here\app.py`""
        if (Test-Path $ico) {
            $lnk.IconLocation = "$ico,0"
        }
    } else {
        throw "Neither EZ-DLP.exe nor pythonw was found."
    }
    $lnk.Save()
}

New-EzdlpShortcut (Join-Path $here "EZ-DLP.lnk")
New-EzdlpShortcut (Join-Path $desktop "EZ-DLP.lnk")

Write-Host "Shortcut created on the desktop and in this folder: EZ-DLP.lnk"
