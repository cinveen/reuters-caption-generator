#!/usr/bin/env python3
"""
Quick test: Can we record audio natively on macOS?
"""

import sounddevice as sd
import soundfile as sf
import numpy as np

print("🎤 Native Audio Recording Test")
print("=" * 50)

# Check available audio devices
print("\nAvailable audio devices:")
print(sd.query_devices())

# Recording parameters
duration = 3  # seconds
sample_rate = 44100  # Hz
output_file = "test_recording.wav"

print(f"\n🔴 Recording for {duration} seconds...")
print("Say something!")

try:
    # Record audio
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='float32'
    )

    # Wait for recording to finish
    sd.wait()

    print("✅ Recording complete!")

    # Save to file
    sf.write(output_file, recording, sample_rate)
    print(f"💾 Saved to: {output_file}")

    # Test transcription with Whisper
    print("\n🔄 Testing Whisper transcription...")
    import sys
    sys.path.insert(0, 'backend')
    from whisper_service import transcribe_audio

    transcription = transcribe_audio(output_file)
    print(f"\n📝 Transcription: {transcription}")

    print("\n✅ SUCCESS! Native recording works!")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nThis might be a permissions issue.")
    print("Check: System Preferences → Security & Privacy → Microphone")
