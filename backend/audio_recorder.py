"""
Native Audio Recorder for Reuters Caption Generator
Handles microphone recording directly via Python (no browser API needed)
"""

import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import logging
from pathlib import Path
import threading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class AudioRecorder:
    """Handles native audio recording"""

    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.is_recording = False
        self.recording_data = []
        self.stream = None

    def start_recording(self):
        """Start recording from the default microphone"""
        if self.is_recording:
            logger.warning("Already recording")
            return False

        try:
            logger.info("Starting native audio recording")
            self.recording_data = []
            self.is_recording = True

            # Start recording with a callback that continuously captures audio
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32',
                callback=self._audio_callback
            )
            self.stream.start()

            logger.info("Recording started successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            self.is_recording = False
            return False

    def _audio_callback(self, indata, frames, time_info, status):
        """Callback for continuous audio capture"""
        if status:
            logger.warning(f"Audio callback status: {status}")

        if self.is_recording:
            # Append audio data to our buffer
            self.recording_data.append(indata.copy())

    def stop_recording(self):
        """Stop recording and save to a temporary file"""
        if not self.is_recording:
            logger.warning("Not currently recording")
            return None

        try:
            logger.info("Stopping recording")
            self.is_recording = False

            # Stop the stream
            if self.stream:
                self.stream.stop()
                self.stream.close()
                self.stream = None

            # Concatenate all recorded chunks
            if not self.recording_data:
                logger.error("No audio data recorded")
                return None

            recording = np.concatenate(self.recording_data, axis=0)

            # Create temporary file in uploads directory
            uploads_dir = Path("uploads")
            uploads_dir.mkdir(exist_ok=True)

            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix='.wav',
                dir=uploads_dir
            )
            temp_file.close()

            # Save audio to file
            sf.write(temp_file.name, recording, self.sample_rate)

            logger.info(f"Recording saved to: {temp_file.name}")
            return temp_file.name

        except Exception as e:
            logger.error(f"Failed to stop recording: {e}")
            return None


# Global recorder instance
_recorder = None


def get_recorder():
    """Get or create the global recorder instance"""
    global _recorder
    if _recorder is None:
        _recorder = AudioRecorder()
    return _recorder


def start_recording():
    """Start recording audio"""
    recorder = get_recorder()
    return recorder.start_recording()


def stop_recording():
    """Stop recording and return the file path"""
    recorder = get_recorder()
    return recorder.stop_recording()


def is_recording():
    """Check if currently recording"""
    recorder = get_recorder()
    return recorder.is_recording
