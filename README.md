# Reuters Photo Caption Generator

A native desktop application designed for Reuters photographers to generate properly formatted photo captions through voice input. Features a simplified wizard interface with full Thomson Reuters branding, powered by OpenAI Whisper Large for transcription and Claude Sonnet 4.5 for intelligent caption generation.

## Overview

Built specifically for photographers who need fast, accurate caption generation in the field. The app uses a native window (no browser required) with a step-by-step wizard design that guides users through recording, generation, and refinement without overwhelming them with technical details.

## Key Features

### Native Desktop Application
- **No browser required**: Runs in a native window using pywebview
- **Clean lifecycle**: Close window = everything shuts down automatically
- **Python audio recording**: Native microphone access via sounddevice
- **Cross-platform**: Works on macOS, Windows, and Linux

### Simplified Wizard Interface
- **One step at a time**: Progressive disclosure design shows only what's relevant
- **Voice-first workflow**: Record descriptions naturally without typing
- **Iterative refinement**: Add details in multiple rounds, building on previous context
- **Clean, minimal UI**: No clutter, no boxes-within-boxes - just the next action

### AI-Powered Intelligence
- **Whisper Large**: Most accurate transcription model, excellent for accents (~1.5GB)
- **Claude Sonnet 4.5**: Reuters-style formatting with comprehensive style guide
- **Smart detection**: Identifies missing information automatically
- **Plain text output**: No markdown artifacts, ready to copy-paste

### Thomson Reuters Branding
- **Official logo**: Sticky header with TR branding
- **Clario font family**: Professional Reuters typography
- **Brand colors**: TR Orange (#D64000), Racing Green (#123015)
- **Random backgrounds**: 9 professional Reuters photos rotate on each launch
- **Mobile responsive**: Clean, modern design

### Comprehensive Reuters Style Guide
- **Detailed requirements**: Core principles, caption structure, writing style
- **Real examples**: Multiple Reuters caption examples with proper formatting
- **Forbidden phrases**: Explicit guidance on avoiding "is seen", "poses", etc.
- **Special situations**: Conflict coverage, third-party images, controlled access

## User Experience Flow

```
1. RECORD & GENERATE
   ↓ Click "Start Recording" button
   ↓ Speak your description
   ↓ Click "Stop Recording"
   ↓ Auto-generates caption immediately (no preview step!)

2. REVIEW & COPY
   ↓ Your caption appears with Copy button
   ↓ Missing info shown as friendly questions (if any)
   ↓ Click "Copy Caption" (done!)

3. REFINE (optional, inline, repeatable)
   ↓ Click "Record Additional Details" to record more
   ↓ OR click "Or Type Here" to reveal text box
   ↓ Auto-updates caption on stop (or click Update after typing)
   ↓ Everything stays on same page - no navigation needed!
```

**Key improvements:**
- ⚡ Faster workflow - no preview step, auto-generates
- 📋 Copy button right below caption
- ❓ Missing info phrased as friendly questions
- 🎤 Inline recording/typing - no page switching
- 🔄 Smart loading messages ("Generating..." vs "Updating...")

## Project Structure

```
reuters-caption-generator/
├── backend/
│   ├── app.py              # Flask application
│   ├── whisper_service.py  # Whisper Large transcription
│   ├── claude_service.py   # Claude/LiteLLM integration
│   ├── audio_recorder.py   # Native audio recording
│   ├── requirements.txt    # Python dependencies
│   └── .env                # Environment configuration (API keys)
│
├── frontend/
│   └── public/
│       ├── index.html      # Simplified wizard UI
│       ├── style.css       # TR branding & styling
│       ├── script.js       # State management & API calls
│       ├── images/
│       │   ├── tr_pri_logo_rgb_color.png
│       │   └── backgrounds/  # 9 Reuters background photos
│       ├── fonts/          # Clario font family
│       └── favicon.ico     # Thomson Reuters favicon
│
├── setup-mac/              # macOS setup and launcher
│   ├── setup.command       # One-time setup (double-click)
│   ├── start.command       # App launcher (double-click)
│   └── SETUP_INSTRUCTIONS_MAC.md
│
├── setup-windows/          # Windows setup and launcher
│   ├── setup.bat           # One-time setup (double-click)
│   ├── start.bat           # App launcher (double-click)
│   └── SETUP_INSTRUCTIONS_WINDOWS.md
│
├── launcher.py             # Python launcher with pywebview
├── setup.py                # py2app config (for future Electron packaging)
├── START_HERE.md           # First file users see
├── HOW_TO_SHARE.md         # Guide for sharing with colleagues
└── README.md               # This file
```

## Quick Start

### For End Users (Photographers)

1. **Extract the folder** you received
2. **Open `START_HERE.md`** and follow the instructions for your OS
3. **macOS users**: Go to `setup-mac/` folder
4. **Windows users**: Go to `setup-windows/` folder
5. **Double-click setup** script (one-time, 5-10 minutes)
6. **Double-click start** script to use the app!

### For Developers

See the **Installation** section below.

## Prerequisites

- **Python 3.8+** (tested on 3.9+)
- **pip** (Python package manager)
- **~2GB disk space** (for Whisper Large model and dependencies)

## Installation (For Developers)

### Quick Setup (Recommended)

**macOS:**
```bash
cd setup-mac
bash setup.command
```

**Windows:**
```bash
cd setup-windows
setup.bat
```

This installs all dependencies and downloads the Whisper Large model.

### Manual Installation

1. **Install Python dependencies:**
```bash
pip install -r backend/requirements.txt
```

2. **Download Whisper Large model:**
```bash
python -c "import whisper; whisper.load_model('large')"
```

3. **Configure API access:**

Create `backend/.env`:
```
LITELLM_API_KEY=your_api_key_here
LITELLM_API_URL=https://litellm.int.thomsonreuters.com
WHISPER_MODEL=large
PORT=8000
LOG_LEVEL=INFO
```

**Note:** You must have access to Thomson Reuters internal LiteLLM instance.

## Running the Application

### Easy Launch

**macOS:**
```bash
# From setup-mac/ folder
./start.command
```

**Windows:**
```bash
# From setup-windows/ folder
start.bat
```

A native window opens with the app. Close the window to shut everything down.

### Manual Launch

```bash
python launcher.py
```

## Usage Guide

### For Photographers

**Step 1: Record & Auto-Generate**
- Click the large "Start Recording" button
- Speak naturally about your photo:
  - Who is in the photo (names, titles)
  - What is happening (action, scene)
  - Where it was taken (specific location, city, country)
  - When it was taken (date, time context)
  - Why it's newsworthy (context, significance)
- Click "Stop Recording" when finished
- **Caption generates automatically** - no extra clicks!

**Step 2: Review & Copy**
- Your formatted caption appears immediately
- Copy button right below caption
- Missing information shown as friendly questions (if any)
- Click "Copy Caption" to copy to clipboard
- Done! Or continue to step 3 to refine...

**Step 3: Refine (Optional, Inline, Repeatable)**
- **Record more:** Click "Record Additional Details" → record → auto-updates
- **OR Type:** Click "Or Type Here" → text box appears → type → click "Update Caption"
- Everything happens on the same page - no navigation!
- New caption builds on ALL previous information
- Repeat as many times as needed

### Best Practices

**Speak clearly and include:**
- Full names with correct spelling
- Specific dates (not "yesterday" but "February 16, 2026")
- Exact locations (not "downtown" but "Times Square, New York")
- Context that makes it newsworthy
- Credit line photographer name

**Recording tips:**
- Minimize background noise
- Speak at normal pace
- Pause briefly between different pieces of information
- Use "Add Missing Info" for corrections

## Technical Architecture

### Native App Stack
- **pywebview**: Native window wrapper (no browser)
- **Python audio recording**: sounddevice library for microphone access
- **Flask**: Backend API server
- **JavaScript bridge**: Communication between Python and JavaScript

### AI Models
- **Whisper Large** (~1.5GB): Most accurate transcription, cached at `~/.cache/whisper/`
- **Claude Sonnet 4.5**: Reuters caption generation via LiteLLM

### Frontend
- **Vanilla JavaScript**: No framework overhead
- **State machine**: Clean step management
- **Toast notifications**: Non-intrusive feedback
- **Responsive CSS**: Works on all screen sizes

### Backend
- **Flask**: Lightweight Python web framework
- **Native audio recording**: Direct microphone access
- **Whisper service**: Local transcription
- **Claude service**: Reuters-style formatting with comprehensive prompt

### API Flow
```
Native Window → Python Audio Recording → WAV file
    ↓
Whisper Large → Transcription
    ↓
Claude Sonnet 4.5 (via LiteLLM) → Formatted Caption
```

### Context Chaining
The app builds context across iterations:
```
Round 1: "Original recording"
         ↓ + details A
Round 2: "Original recording + Additional details: A"
         ↓ + details B
Round 3: "Original recording + Additional details: A + B"
```

## Sharing with Colleagues

See `HOW_TO_SHARE.md` for detailed instructions.

**Quick summary:**
1. Zip the entire folder
2. Send to colleague
3. They follow `START_HERE.md` instructions
4. API credentials automatically included (in `backend/.env`)

## Background Photos

The app features 9 rotating Reuters photos as backgrounds:
- Rugby match
- Arctic scene
- German carnival
- Lunar New Year celebrations (Indonesia, Russia, Thailand)
- Olympics (ski jumping, snowboard)
- Gaza coverage

To add more:
1. Add JPG files to `frontend/public/images/backgrounds/`
2. Update `backgroundImages` array in `frontend/public/script.js`

## Troubleshooting

### Setup Issues
- **"Python not found"**: Install Python 3 from python.org
- **Setup fails**: Make sure you have internet connection for downloads
- **Permission denied (Mac)**: Right-click script → Open → Open anyway

### App Issues
- **Window doesn't open**: Check that setup completed successfully
- **Microphone not working**: Grant microphone permissions in system settings
- **Transcription slow**: Normal for Whisper Large (~2-3 seconds per 10s audio)
- **Caption generation fails**: Check VPN connection to LiteLLM

### Common Fixes
- **Port conflict**: Close window and reopen (auto-kills old servers)
- **Whisper model missing**: Run setup script again
- **API errors**: Verify `.env` file has correct credentials

## Browser Compatibility (Dev Mode)

If running Flask directly (not via launcher):
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## Development Notes

### Key Files to Modify

**Change Reuters prompt:**
- Edit `backend/claude_service.py` → `REUTERS_PROMPT_TEMPLATE`

**Change Whisper model:**
- Edit `backend/whisper_service.py` → `WHISPER_MODEL` (or set in `.env`)

**Change UI:**
- `frontend/public/index.html` - Structure
- `frontend/public/style.css` - Styling
- `frontend/public/script.js` - Behavior

**Add background photos:**
- Add to `frontend/public/images/backgrounds/`
- Update `backgroundImages` array in `script.js`

### Model Options

Whisper models available (change in `.env`):
- `tiny` (~39MB) - Fastest, least accurate
- `base` (~74MB) - Fast, good accuracy
- `small` (~244MB) - Medium speed, better accuracy
- `medium` (~769MB) - Slower, great accuracy
- **`large` (~1.5GB)** - Slowest, best accuracy (current)

## Future Enhancements

Potential improvements:
- Electron packaging for true standalone .app
- Keyboard shortcuts
- Caption history/templates
- Multi-language support
- Batch processing
- Export to various formats

## Credits & Acknowledgments

- **OpenAI Whisper Large** - Industry-leading audio transcription
- **Anthropic Claude Sonnet 4.5** - Intelligent caption generation
- **Thomson Reuters** - Brand guidelines and caption standards
- **LiteLLM** - Unified API management
- **pywebview** - Native window wrapper

## Support

For issues, questions, or feature requests, contact the development team.

---

**Built for Reuters photographers** 📸
