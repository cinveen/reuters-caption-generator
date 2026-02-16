#!/bin/bash

echo "Stopping Reuters Caption Generator..."

# Kill all Python processes running the app
lsof -ti:8000 | xargs kill -9 2>/dev/null

# Also kill any launcher.py or app.py processes
pkill -f "python.*launcher.py" 2>/dev/null
pkill -f "python.*app.py" 2>/dev/null

# Wait a moment
sleep 1

# Check if anything is still running
if lsof -ti:8000 > /dev/null 2>&1; then
    echo "❌ Failed to stop server (port 8000 still in use)"
    echo "You may need to restart your computer."
else
    echo "✅ Reuters Caption Generator stopped successfully!"
fi

# Keep window open for 2 seconds so user sees the message
sleep 2

# Close this Terminal window
osascript -e 'tell application "Terminal" to close first window' > /dev/null 2>&1 &

exit
