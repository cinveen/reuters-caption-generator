@echo off
REM Reuters Caption Generator - Windows Launcher
REM Double-click this to start the app

REM Change to parent directory (where launcher.py is)
cd ..

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

REM Launch the app
echo Starting Reuters Caption Generator...
python launcher.py

REM If the script exits, keep window open
if errorlevel 1 (
    echo.
    echo Error: App failed to start
    echo Make sure you ran setup.bat first
    pause
)
