#!/bin/bash
# Change to parent directory (where launcher.py is)
cd "$(dirname "$0")/.."

# Kill any existing Flask servers to prevent conflicts
lsof -ti:8000 | xargs kill -9 2>/dev/null

echo "🚀 Starting Reuters Caption Generator..."
echo ""
echo "App window will open shortly..."
echo "When you close the app window, this Terminal will close automatically."
echo ""

# Start the app with pywebview
# When you close the app window, everything stops cleanly!
python3 launcher.py

# When window closes, we get here
echo ""
echo "✅ App closed successfully."
exit
