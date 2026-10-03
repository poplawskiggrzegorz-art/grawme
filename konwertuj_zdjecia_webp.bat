@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
    echo Python nie jest zainstalowany. Pobierz go z https://www.python.org/downloads/windows/
    pause
    exit /b 1
)

py -3 -m pip install -r requirements.txt
if errorlevel 1 (
    echo Nie udalo sie zainstalowac wymaganych bibliotek.
    pause
    exit /b 1
)

py -3 convert_to_webp.py %*
pause
