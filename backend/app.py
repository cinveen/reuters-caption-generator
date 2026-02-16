"""
Reuters Photo Caption Generator
Flask application for transcribing audio and generating Reuters-style captions
"""

import os
import logging
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Import services
import whisper_service
import claude_service

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Flask configuration
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Create uploads directory if it doesn't exist
UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

# Initialize Flask app
app = Flask(__name__, static_folder="../frontend/public")
CORS(app)  # Enable CORS for all routes
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max upload size

# Allowed audio file extensions
ALLOWED_EXTENSIONS = {"wav", "mp3", "ogg", "m4a", "flac"}


def allowed_file(filename):
    """Check if the file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """Serve the frontend index.html file"""
    return send_from_directory("../frontend/public", "index.html")


@app.route("/<path:filename>")
def serve_static(filename):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory("../frontend/public", filename)


@app.route("/api/health")
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok"})


@app.route("/api/transcribe", methods=["POST"])
def transcribe_audio():
    """
    Endpoint to transcribe audio using Whisper
    
    Expects:
        - audio_file: Audio file in the request
        
    Returns:
        - JSON with transcription text
    """
    try:
        # Check if the post request has the file part
        if "audio_file" not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        file = request.files["audio_file"]
        
        # Check if the file is empty
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        
        # Check if the file extension is allowed
        if not allowed_file(file.filename):
            return jsonify({"error": f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"}), 400
        
        # Save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        
        # Transcribe the audio
        transcription = whisper_service.transcribe_audio(file_path)
        
        # Clean up the file
        whisper_service.cleanup_audio_file(file_path)
        
        return jsonify({"transcription": transcription})
    
    except Exception as e:
        logger.error(f"Error in transcribe_audio: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/generate-caption", methods=["POST"])
def generate_caption():
    """
    Endpoint to generate a Reuters-style caption using Claude
    
    Expects:
        - JSON with transcription text
        
    Returns:
        - JSON with formatted caption, missing information, and follow-up questions
    """
    try:
        # Get the transcription from the request
        data = request.json
        
        if not data or "transcription" not in data:
            return jsonify({"error": "No transcription provided"}), 400
        
        transcription = data["transcription"]
        
        # Generate the caption
        caption_data = claude_service.generate_caption(transcription)
        
        return jsonify(caption_data)
    
    except Exception as e:
        logger.error(f"Error in generate_caption: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/upload-audio", methods=["POST"])
def upload_audio():
    """
    Endpoint to handle audio blob uploads from the browser
    
    Expects:
        - audio_blob: Audio blob data in the request
        
    Returns:
        - JSON with transcription text
    """
    try:
        # Check if the post request has the file part
        if "audio_blob" not in request.files:
            return jsonify({"error": "No audio blob provided"}), 400
        
        file = request.files["audio_blob"]
        
        # Save the audio blob to a temporary file
        temp_file_path = whisper_service.save_audio_file(file.read())
        
        # Transcribe the audio
        transcription = whisper_service.transcribe_audio(temp_file_path)
        
        # Clean up the temporary file
        whisper_service.cleanup_audio_file(temp_file_path)
        
        return jsonify({"transcription": transcription})
    
    except Exception as e:
        logger.error(f"Error in upload_audio: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    logger.info(f"Starting Reuters Caption Generator on port {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
