#!/bin/bash

# Reuters Caption Generator - Setup Script
# Run this once to install everything needed

# Change to parent directory (where backend/ folder is)
cd "$(dirname "$0")/.."

echo "================================================"
echo "Reuters Caption Generator - Setup"
echo "================================================"
echo ""
echo "This will install all required dependencies."
echo "It may take 5-10 minutes..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed!"
    echo ""
    echo "Please install Python 3 from: https://www.python.org/downloads/"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Install Python dependencies
echo "📦 Installing Python packages..."
echo "This may take a few minutes..."
echo ""
pip3 install -r backend/requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ ERROR: Failed to install dependencies"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo ""
echo "✅ Python packages installed successfully"
echo ""

# Download Whisper large model
echo "📥 Downloading Whisper large model (1.5 GB)..."
echo "This is a one-time download and may take 5-10 minutes..."
echo ""
python3 -c "import whisper; print('Downloading...'); model = whisper.load_model('large'); print('✅ Whisper model downloaded!')"

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Warning: Whisper model download failed"
    echo "It will try to download automatically when you first use the app."
    echo ""
fi

echo ""
echo "================================================"
echo "✅ Setup Complete!"
echo "================================================"
echo ""
echo "You can now run 'start.command' to launch the app."
echo ""
read -p "Press Enter to close this window..."
