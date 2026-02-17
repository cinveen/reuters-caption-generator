@echo off
REM Reuters Caption Generator - Setup Script for Windows
REM Run this once to install everything needed

echo ================================================
echo Reuters Caption Generator - Setup
echo ================================================
echo.
echo This will install all required dependencies.
echo It may take 5-10 minutes...
echo.

REM Check if Python 3 is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3 is not installed!
    echo.
    echo Please install Python 3 from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Change to parent directory (where backend folder is)
cd ..

REM Install Python dependencies
echo Installing Python packages...
echo This may take a few minutes...
echo.
pip install -r backend\requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo.
    pause
    exit /b 1
)

echo.
echo Python packages installed successfully
echo.

REM Download Whisper large model
echo Downloading Whisper large model (1.5 GB)...
echo This is a one-time download and may take 5-10 minutes...
echo.
python -c "import whisper; print('Downloading...'); model = whisper.load_model('large'); print('Whisper model downloaded!')"

if errorlevel 1 (
    echo.
    echo Warning: Whisper model download failed
    echo It will try to download automatically when you first use the app.
    echo.
)

echo.
echo ================================================
echo Setup Complete!
echo ================================================
echo.
echo You can now run 'start.bat' to launch the app.
echo.
pause
