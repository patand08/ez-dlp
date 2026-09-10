@echo off
cd /d "%~dp0"
echo Creating EZ-DLP.exe and a Desktop shortcut.
echo Leave this window open. The first time can take a minute.
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build.ps1"
set ERR=%errorlevel%

echo.
if exist "%~dp0EZ-DLP.exe" (
  echo Done. Look on your Desktop for an icon named EZ-DLP and double-click it.
) else (
  echo It did not finish.
  echo Install Python first: https://www.python.org/downloads/
  echo On the installer, check  Add python.exe to PATH
  if not %ERR%==0 echo Error code: %ERR%
)
echo.
pause
