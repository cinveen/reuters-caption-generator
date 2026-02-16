"""
py2app setup script for Reuters Photo Caption Generator
"""

from setuptools import setup

APP = ["launcher.py"]
DATA_FILES = [
    ("frontend/public", ["frontend/public/index.html", "frontend/public/script.js"]),
    ("backend", [
        "backend/app.py",
        "backend/claude_service.py",
        "backend/whisper_service.py",
        "backend/.env.example",
    ]),
]

OPTIONS = {
    "argv_emulation": False,
    "packages": [
        "flask",
        "flask_cors",
        "dotenv",
        "whisper",
        "torch",
        "litellm",
        "requests",
        "pydub",
        "speech_recognition",
        "werkzeug",
        "webview",
    ],
    "includes": [
        "app",
        "claude_service",
        "whisper_service",
    ],
    "excludes": [
        "tkinter",
        "matplotlib",
        "scipy",
    ],
    "iconfile": None,  # You can add an .icns file here later
    "plist": {
        "CFBundleName": "Reuters Caption Generator",
        "CFBundleDisplayName": "Reuters Caption Generator",
        "CFBundleIdentifier": "com.reuters.captiongenerator",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
        "NSHumanReadableCopyright": "© 2024 Reuters",
        "LSMinimumSystemVersion": "10.14",
        "NSMicrophoneUsageDescription": "This app needs access to your microphone to record audio for caption generation.",
    },
}

setup(
    name="Reuters Caption Generator",
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
