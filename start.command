#!/bin/bash
cd "$(dirname "$0")"

# Kill any existing Flask servers to prevent conflicts
lsof -ti:8000 | xargs kill -9 2>/dev/null

# Start the app in background
python3 launcher.py > /dev/null 2>&1 &

# Wait for server to start
sleep 3

# Close this Terminal window
osascript -e 'tell application "Terminal" to close first window' &

exit
