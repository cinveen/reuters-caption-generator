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


class API:
    """API class to expose Python functions to JavaScript"""

    def start_recording(self):
        """Start native audio recording"""
        try:
            from audio_recorder import start_recording
            logger = logging.getLogger(__name__)
            logger.info("API: start_recording called")
            success = start_recording()
            return {"success": success}
        except Exception as e:
            logging.error(f"API: start_recording error: {e}")
            return {"success": False, "error": str(e)}

    def stop_recording(self):
        """Stop recording and return transcription"""
        try:
            from audio_recorder import stop_recording
            from whisper_service import transcribe_audio, cleanup_audio_file

            logger = logging.getLogger(__name__)
            logger.info("API: stop_recording called")

            # Stop recording and get file path
            file_path = stop_recording()

            if not file_path:
                return {"success": False, "error": "Recording failed"}

            # Transcribe the audio
            transcription = transcribe_audio(file_path)

            # Clean up the file
            cleanup_audio_file(file_path)

            logger.info(f"API: transcription complete: {transcription}")
            return {"success": True, "transcription": transcription}

        except Exception as e:
            logging.error(f"API: stop_recording error: {e}")
            return {"success": False, "error": str(e)}

    def is_recording(self):
        """Check if currently recording"""
        try:
            from audio_recorder import is_recording
            return {"recording": is_recording()}
        except Exception as e:
            return {"recording": False, "error": str(e)}


class FlaskServer:
    """Flask server wrapper that can be cleanly shut down"""
    def __init__(self):
        self.server = None
        self.thread = None

    def start(self):
        """Start the Flask server in a separate thread"""
        # Change to backend directory for proper paths
        os.chdir(backend_path)

        # Import Flask app
        from app import app, PORT, logger

        logger.info(f"Starting Flask server on port {PORT}")

        # Create server
        self.server = make_server("127.0.0.1", PORT, app, threaded=True)

        # Start serving in a daemon thread so it doesn't block shutdown
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

        logger.info("Flask server started")

    def stop(self):
        """Stop the Flask server"""
        if self.server:
            logging.getLogger(__name__).info("Shutting down Flask server...")
            self.server.shutdown()
            logging.getLogger(__name__).info("Flask server stopped")

# Global server instance
flask_server = FlaskServer()


def on_closing():
    """Called when the window is closing - cleanup here"""
    logger = logging.getLogger(__name__)
    logger.info("Window closing - cleaning up...")

    # Stop the Flask server
    flask_server.stop()

    logger.info("Cleanup complete")


def main():
    """Main function to launch the app"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    # Start Flask server
    flask_server.start()

    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    url = f"http://127.0.0.1:{port}"

    # Wait for Flask to be ready
    logger.info("Waiting for Flask server to be ready...")
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            import urllib.request
            urllib.request.urlopen(f"{url}/api/health", timeout=1)
            logger.info("Flask server is ready!")
            break
        except Exception:
            if attempt < max_attempts - 1:
                time.sleep(0.5)
            else:
                logger.error("Flask server failed to start!")
                return

    logger.info(f"Opening Reuters Caption Generator at {url}")

    # Create API instance
    api = API()

    # Create pywebview window with Python API bridge
    window = webview.create_window(
        title="Reuters Photo Caption Generator",
        url=url,
        width=1200,
        height=800,
        resizable=True,
        min_size=(800, 600),
        js_api=api  # This exposes Python functions to JavaScript!
    )

    # Register the closing event handler
    window.events.closing += on_closing

    logger.info("Starting pywebview window...")

    # Start the GUI (this blocks until window is closed)
    webview.start()

    logger.info("Application shut down successfully")


if __name__ == "__main__":
    main()
