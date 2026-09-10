@echo off
cd /d "%~dp0"

where pythonw >nul 2>&1
if %errorlevel%==0 (
  start "" pythonw "%~dp0app.py"
  exit /b 0
)

where python >nul 2>&1
if %errorlevel%==0 (
  python "%~dp0app.py"
  exit /b %errorlevel%
)

echo.
echo Python was not found.
echo.
echo 1. Open https://www.python.org/downloads/
echo 2. Run the installer.
echo 3. Check the box  Add python.exe to PATH
echo 4. Click Install Now, then double-click this file again.
echo.
pause
