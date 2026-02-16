#!/usr/bin/env python3
"""
Reuters Photo Caption Generator - Mac App Launcher
Starts the Flask server and opens a native Mac window
"""

import os
import sys
import threading
import time
import logging
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

import webview
from werkzeug.serving import make_server


def start_flask_server():
    """Start the Flask server in a separate thread"""
    # Change to backend directory for proper paths
    os.chdir(backend_path)

    # Import Flask app
    from app import app, PORT, logger

    logger.info(f"Starting Flask server on port {PORT}")

    # Create server
    server = make_server("127.0.0.1", PORT, app, threaded=True)

    # Store server in thread so we can shut it down later
    threading.current_thread().server = server

    # Start serving
    server.serve_forever()


def main():
    """Main function to launch the app"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Start Flask in a background thread (NOT daemon so it keeps process alive)
    flask_thread = threading.Thread(target=start_flask_server, daemon=False)
    flask_thread.start()

    # Wait a moment for Flask to start
    time.sleep(3)

    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    url = f"http://127.0.0.1:{port}"

    logger.info(f"Opening Reuters Caption Generator at {url}")

    # Open in default browser (supports microphone access)
    import webbrowser
    webbrowser.open(url)

    logger.info("Application opened in browser - server running")

    # Keep server running forever
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Application closed")


if __name__ == "__main__":
    main()
