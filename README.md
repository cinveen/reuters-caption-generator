# Reuters Photo Caption Generator

A streamlined web application designed for Reuters photographers to generate properly formatted photo captions through voice input. Features a simplified wizard interface with full Thomson Reuters branding, powered by OpenAI Whisper for transcription and Claude Sonnet 4.5 for intelligent caption generation.

## Overview

Built specifically for photographers who need fast, accurate caption generation in the field. The app uses a step-by-step wizard design that guides users through recording, generation, and refinement without overwhelming them with technical details.

## Key Features

### Simplified Wizard Interface
- **One step at a time**: Progressive disclosure design shows only what's relevant
- **Voice-first workflow**: Record descriptions naturally without typing
- **Iterative refinement**: Add details in multiple rounds, building on previous context
- **Clean, minimal UI**: No clutter, no boxes-within-boxes - just the next action

### AI-Powered Intelligence
- **Whisper transcription**: Fast, accurate local transcription (no internet delays)
- **Claude Sonnet 4.5**: Reuters-style formatting with context awareness
- **Smart detection**: Identifies missing information automatically
- **Plain text output**: No markdown artifacts, ready to copy-paste

### Thomson Reuters Branding
- **Official logo**: Sticky header with TR branding
- **Clario font family**: Professional Reuters typography
- **Brand colors**: TR Orange (#D64000), Racing Green (#123015)
- **Consistent styling**: Clean white backgrounds with color accents
- **Mobile responsive**: Works seamlessly on phones and tablets

## User Experience Flow

```
1. RECORD
   ↓ Click big "Start Recording" button
   ↓ Speak your description
   ↓ Click "Stop"

2. GENERATE
   ↓ See preview of what was transcribed
   ↓ Click "Generate Reuters Caption"

3. REVIEW
   ↓ Your caption appears
   ↓ Missing info highlighted (if any)
   ↓ Click "Copy Caption" (done!) or "Add Missing Info"

4. REFINE (optional, repeatable)
   ↓ Record OR type additional details
   ↓ Click "Update Caption"
   ↓ Return to step 3 (builds on previous context)
```

## Project Structure

```
reuters-caption-generator/
├── backend/
│   ├── app.py              # Flask application with static file serving
│   ├── whisper_service.py  # Local Whisper transcription
│   ├── claude_service.py   # Claude/LiteLLM integration (Anthropic SDK)
│   ├── requirements.txt    # Python dependencies
│   ├── .env                # Environment configuration (API keys)
│   └── uploads/            # Temporary audio files (auto-created)
│
├── frontend/
│   └── public/
│       ├── index.html      # Simplified wizard UI
│       ├── style.css       # Thomson Reuters branding & styling
│       ├── script.js       # State management & API calls
│       ├── images/         # TR logos
│       ├── fonts/          # Clario font family
│       └── favicon.ico     # Thomson Reuters favicon
│
└── README.md               # This file
```

## Prerequisites

- **Python 3.8+** (tested on 3.9.6)
- **pip** (Python package manager)
- **FFmpeg** (required for Whisper audio processing)
- **Modern browser** (Chrome, Firefox, Edge, Safari)

## Installation

### 1. Install FFmpeg

FFmpeg is required for Whisper to process audio files.

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Windows (Chocolatey):**
```bash
choco install ffmpeg
```

Or download from [ffmpeg.org](https://ffmpeg.org/download.html)

### 2. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
pip install openai-whisper anthropic
```

**What gets installed:**
- Flask & Flask-CORS (web framework)
- OpenAI Whisper (audio transcription)
- PyTorch (~2GB, required by Whisper)
- Anthropic SDK (Claude API client)
- LiteLLM (API management)
- Supporting packages (numpy, etc.)

**Installation time:** 5-10 minutes (mostly PyTorch download)

### 3. Configure API Access

Create or update the `.env` file in the `backend/` directory:

```bash
cd backend
cp .env.example .env  # if .env doesn't exist
```

Edit `.env`:
```
LITELLM_API_KEY=your_api_key_here
LITELLM_API_URL=https://litellm.int.thomsonreuters.com
WHISPER_MODEL=base
PORT=8000
LOG_LEVEL=INFO
```

**Note:** You must have access to the Thomson Reuters internal LiteLLM instance and be on the appropriate VPN.

## Running the Application

### Start the Server

```bash
cd backend
python app.py
```

You should see:
```
Starting Reuters Caption Generator on port 8000
* Running on http://127.0.0.1:8000
```

### Access the Application

Open your browser to: **http://localhost:8000**

The Thomson Reuters-branded wizard interface will appear.

## Usage Guide

### For Photographers

**Step 1: Record Your Description**
- Click the large "Start Recording" button
- Speak naturally about your photo:
  - Who is in the photo (names, titles)
  - What is happening (action, scene)
  - Where it was taken (specific location, city, country)
  - When it was taken (date, time context)
  - Why it's newsworthy (context, significance)
- Click "Stop Recording" when finished
- Audio plays back automatically for verification

**Step 2: Generate Caption**
- Review the transcription preview (truncated)
- Click "Generate Reuters Caption"
- Claude analyzes the description and formats it

**Step 3: Review & Copy**
- Your formatted caption appears
- If information is missing, it's highlighted in an orange-bordered box
- Click "Copy Caption" to copy to clipboard
- Click "Start Over" to begin a new caption
- Or click "Add Missing Info" to refine...

**Step 4: Refine (Optional, Repeatable)**
- Choose to record OR type additional details
- Click "Record Details" for voice input, or just type in the box
- Click "Update Caption" to regenerate
- The new caption builds on ALL previous information
- Repeat as many times as needed until perfect

### Best Practices

**Speak clearly and include:**
- Full names with correct spelling (spell unusual names)
- Specific dates (not "yesterday" but "February 16, 2026")
- Exact locations (not "downtown" but "Times Square, New York")
- Context that makes it newsworthy
- Any relevant background information

**Recording tips:**
- Minimize background noise
- Speak at normal pace (not too fast)
- Pause briefly between different pieces of information
- Use the "Add Missing Info" feature for corrections

## Design Philosophy

### Why This UI?

This application was specifically designed for **photographers who hate tech and writing captions**. Every decision was made to reduce friction:

1. **No cognitive overload**: One clear action at a time
2. **No learning curve**: Obvious buttons, clear flow
3. **No technical jargon**: "Describe your photo" not "Audio input transcription"
4. **No visual clutter**: Clean white space, focused content
5. **No mistakes**: Smart detection of missing information

### Visual Design

- **Professional**: Thomson Reuters branding throughout
- **Accessible**: Large touch targets, high contrast, clear hierarchy
- **Responsive**: Works on desktop, tablet, and phone
- **Fast**: Smooth animations, instant feedback
- **Trustworthy**: Familiar Reuters visual language

## Technical Architecture

### Frontend
- **Vanilla JavaScript**: No framework overhead, fast and simple
- **Progressive enhancement**: Works without JavaScript for basic functionality
- **State machine**: Clean step management with `showStep()`
- **Toast notifications**: Non-intrusive feedback (no alerts)
- **Responsive CSS**: Mobile-first with breakpoints at 640px and 380px

### Backend
- **Flask**: Lightweight Python web framework
- **Whisper**: Local transcription (base model, ~1GB)
- **Claude via Anthropic SDK**: Custom base_url for LiteLLM
- **CORS enabled**: Supports local development
- **Static file serving**: Direct serving of frontend assets

### API Flow
```
Browser → Record Audio → Blob
    ↓
POST /api/upload-audio → Whisper Service → Transcription
    ↓
POST /api/generate-caption → Claude Service → Formatted Caption
```

### Context Chaining
The app intelligently builds context across iterations:
```
Round 1: "Original recording"
         ↓ + details A
Round 2: "Original recording + Additional details: A"
         ↓ + details B
Round 3: "Original recording + Additional details: A + B"
```

## Troubleshooting

### Microphone Issues
- **Browser permission denied**: Check browser settings
- **No audio detected**: Check system microphone settings
- **Recording doesn't start**: Try refreshing the page

### Transcription Issues
- **Inaccurate transcription**: Speak more clearly, reduce background noise
- **Wrong language detected**: Specify language in recording
- **Slow transcription**: Base model is ~1s per 10s of audio

### Caption Generation Issues
- **403 Forbidden**: Check API key, VPN connection
- **Slow generation**: LiteLLM instance may be under load
- **Markdown in output**: Refresh page and try again (prompt now prevents this)

### Styling Issues
- **Logo not loading**: Check `frontend/public/images/` directory
- **Fonts not loading**: Check `frontend/public/fonts/` directory
- **Colors wrong**: Hard refresh browser (Cmd+Shift+R / Ctrl+Shift+R)

## Browser Compatibility

- ✅ Chrome 90+ (recommended)
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ❌ Internet Explorer (not supported)

**Features requiring modern browser:**
- MediaRecorder API (audio recording)
- Fetch API (backend communication)
- CSS Grid & Flexbox (layout)
- CSS Custom Properties (theming)

## Development Notes

### Adding New Features

The wizard architecture makes it easy to add steps:

1. Add HTML section with `class="step"` and unique ID
2. Add step to `showStep()` navigation array
3. Add event listeners in `init()` function
4. Use existing button styles and layouts for consistency

### Modifying Branding

All brand colors and fonts are defined in CSS custom properties at the top of `style.css`. To rebrand:

1. Update `:root` variables (colors)
2. Update `@font-face` declarations (fonts)
3. Replace logo in `images/` directory
4. Update favicon

### Backend Changes

- Whisper model can be changed in `.env` (tiny/base/small/medium/large)
- Claude prompt is in `claude_service.py` (`REUTERS_PROMPT_TEMPLATE`)
- Port and logging configured in `.env`

## Deployment Considerations

**For internal Thomson Reuters deployment:**

- Requires access to internal LiteLLM instance
- VPN connection necessary for API access
- SSL certificate recommended for production
- Consider using Gunicorn/uWSGI instead of Flask dev server

**Performance:**
- Whisper transcription: ~1-2 seconds per 10 seconds of audio
- Claude generation: ~3-5 seconds per caption
- Total time: ~10-15 seconds for a complete workflow

## Future Enhancements

Potential improvements (not yet implemented):
- Keyboard shortcuts (Space to record, Cmd+Enter to generate)
- Dark mode toggle
- Caption history/templates
- Multi-language support
- Batch processing
- Export to various formats

## License

[Specify your license here]

## Credits & Acknowledgments

- **OpenAI Whisper** - Fast, accurate audio transcription
- **Anthropic Claude Sonnet 4.5** - Intelligent caption generation
- **Thomson Reuters** - Brand guidelines and caption standards
- **LiteLLM** - Unified API management

## Support

For issues, questions, or feature requests, please contact the development team or file an issue in the project repository.

---

**Built for Reuters photographers, by humans and Claude** 🤝
