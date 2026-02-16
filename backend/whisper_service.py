"""
Whisper Service for Reuters Caption Generator
Handles audio transcription using OpenAI's Whisper model
"""

import os
import tempfile
import logging
from pathlib import Path
import whisper
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Get Whisper model size from environment variables
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

# Initialize Whisper model (lazy loading - will only load when first used)
_model = None


def get_model():
    """
    Lazy-load the Whisper model to avoid loading it on startup
    """
    global _model
    if _model is None:
        logger.info(f"Loading Whisper model: {WHISPER_MODEL}")
        _model = whisper.load_model(WHISPER_MODEL)
        logger.info("Whisper model loaded successfully")
    return _model


def transcribe_audio(audio_file_path):
    """
    Transcribe audio file using Whisper
    
    Args:
        audio_file_path (str): Path to the audio file
        
    Returns:
        str: Transcribed text
    """
    try:
        logger.info(f"Transcribing audio file: {audio_file_path}")
        
        # Get the model
        model = get_model()
        
        # Transcribe the audio
        result = model.transcribe(audio_file_path)
        
        # Extract the transcribed text
        transcription = result["text"].strip()
        
        logger.info("Transcription completed successfully")
        return transcription
    
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        raise


def save_audio_file(audio_data, file_extension=".wav"):
    """
    Save audio data to a temporary file
    
    Args:
        audio_data: Audio data to save
        file_extension (str): File extension for the temporary file
        
    Returns:
        str: Path to the saved temporary file
    """
    try:
        # Create uploads directory if it doesn't exist
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)
        
        # Create a temporary file in the uploads directory
        temp_file = tempfile.NamedTemporaryFile(
            delete=False, 
            suffix=file_extension, 
            dir=uploads_dir
        )
        
        # Write audio data to the temporary file
        temp_file.write(audio_data)
        temp_file.close()
        
        logger.info(f"Audio saved to temporary file: {temp_file.name}")
        return temp_file.name
    
    except Exception as e:
        logger.error(f"Error saving audio file: {str(e)}")
        raise


def cleanup_audio_file(file_path):
    """
    Delete temporary audio file
    
    Args:
        file_path (str): Path to the audio file to delete
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted temporary audio file: {file_path}")
    except Exception as e:
        logger.error(f"Error deleting temporary audio file: {str(e)}")
