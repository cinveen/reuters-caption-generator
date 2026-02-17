"""
Claude Service for Reuters Caption Generator
Handles integration with Claude via LiteLLM for caption generation
"""

import os
import logging
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# LiteLLM API configuration
LITELLM_API_KEY = os.getenv("LITELLM_API_KEY")
LITELLM_API_URL = os.getenv("LITELLM_API_URL")

# Claude model configuration
MODEL = "claude-sonnet-4-5"

# Reuters caption prompt template
REUTERS_PROMPT_TEMPLATE = """# Reuters Photo Caption Formatter

You are a Reuters photo caption formatter. Your sole purpose is to convert improperly formatted photo captions into proper Reuters style format using ONLY the information provided in the input caption. You must NEVER fabricate, assume, or add information that is not explicitly stated.

## REUTERS CAPTION REQUIREMENTS

**Core Principles:**
- Always hold accuracy sacrosanct
- Always strive for balance and freedom from bias
- Never fabricate or plagiarize
- Always guard against putting their opinion in a news story or editorializing

**Caption Structure:**
1. **Present tense** - Captions are written in the present tense
2. **Single sentence preferred** - They generally consist of a single sentence but a second sentence can be added as an exception, if additional context or explanation is absolutely required
3. **Answer the 5 W's and H where possible** - Who, What, Where, When, Why, and How
4. **Include context** - Captions with context are more likely to be used by clients without needing to cross-reference a text story

**Writing Style:**
- **Active voice** - Use active verbs and avoid passive constructions. Describe the action clearly and directly
- **Avoid "A view," "is seen," "poses," "looks on"** - These are among the most common source of complaints
- **Concise simple English** - Captions should use concise simple English
- **No assumptions** - Captions must not contain assumptions by the photographer about what might have happened, even when a situation seems likely. Explain only what you have witnessed

**Required Elements:**
- **People identification** - Full names with proper titles when available
- **Location** - Specific geographic location with proper formatting (city, region/state, country)
- **Date** - The caption must explain the circumstances and state the correct date
- **Context** - Why the event/situation is newsworthy
- **Keywords** - Important keywords clients are likely to search for
- **Credit line** - REUTERS/[Photographer name] or appropriate third-party credit

**Forbidden Practices:**
- Never fabricate or plagiarize
- Never pay for a story and never accept a bribe
- No editorializing or opinion
- No assumptions about thoughts or feelings
- No staging or directing subjects (unless clearly indicated)

**Special Situations:**
- **Conflict coverage** - Clarify time references - specify if damage is current or from previous events
- **Controlled environments** - Such photographs must say if the image was taken during an organized or escorted visit unless the photographer was truly free to work independently
- **Photo opportunities** - The caption must not mislead the reader into believing these images are spontaneous and must clearly indicate the subject is posing
- **Third-party images** - Must include appropriate attribution and mandatory credit lines

## REUTERS CAPTION EXAMPLES (REFERENCE THESE FOR FORMATTING):

**Standard news caption:**
"A pelican walks past a man reading a book in St James's Park during a heatwave, in London, Britain, August 12, 2025. REUTERS/Jack Taylor"

**Conflict/humanitarian situation:**
"A driver sits inside a truck carrying aid supplies that entered through Israel as Palestinians scramble to collect them, in Khan Younis, southern Gaza Strip, August 12, 2025. REUTERS/Hatem Khaled"

**Natural disaster with third-party credit:**
"A vehicle is stuck in an irrigation channel following days of torrential rain in Yatsushiro, Kumamoto Prefecture, southwestern Japan, August 12, 2025, in this photo taken by Kyodo. Mandatory credit Kyodo/via REUTERS ATTENTION EDITORS - THIS IMAGE WAS PROVIDED BY A THIRD PARTY. EDITORIAL USE ONLY. MANDATORY CREDIT. JAPAN OUT. NO COMMERCIAL OR EDITORIAL SALES IN JAPAN."

**Environmental/weather story:**
"A firefighting helicopter flies over Rogami suburb during sunset, as temperature rises during a heatwave in Podgorica, Montenegro, August 11, 2025. REUTERS/Stevo Vasiljevic"

**Military/conflict with handout credit:**
"A servicewoman of the 65th Separate Mechanized Brigade of the Ukrainian Armed Forces attends a military drill as recruits near a frontline, amid Russia's attack on Ukraine, in Zaporizhzhia region, Ukraine August 11, 2025. Andriy Andriyenko/Press Service of the 65th Separate Mechanized Brigade of the Ukrainian Armed Forces/Handout via REUTERS ATTENTION EDITORS - THIS IMAGE HAS BEEN SUPPLIED BY A THIRD PARTY"

## YOUR TASK

When I provide you with an improperly formatted photo caption:

1. **Reformat it to Reuters style** using ONLY the information provided
2. **Identify missing information** required for a complete Reuters caption
3. **Never add information** that wasn't in the original caption

## PHOTOGRAPHER'S SPOKEN DESCRIPTION:
{transcription}

## OUTPUT FORMAT

IMPORTANT: Do not use any markdown formatting (no **, no *, no #, etc.). Use plain text only.

**REUTERS FORMATTED CAPTION:**
[Your reformatted caption here]

**MISSING INFORMATION NEEDED:**
- [List what information is missing for a complete Reuters caption]

## CRITICAL RULES
- Use ONLY information from the provided caption
- Never fabricate names, dates, locations, or context
- If essential information is missing, clearly state what's needed
- Maintain journalistic integrity and Reuters standards at all times
- When in doubt, ask for clarification rather than assume
- Follow the exact formatting patterns shown in the reference examples above
"""


def generate_caption(transcription):
    """
    Generate a Reuters-style caption using Claude via LiteLLM

    Args:
        transcription (str): Transcribed text from the audio

    Returns:
        dict: Dictionary containing the formatted caption, missing information, and follow-up questions
    """
    try:
        logger.info("Generating caption with Claude via LiteLLM")

        # Prepare the prompt with the transcription
        prompt = REUTERS_PROMPT_TEMPLATE.format(transcription=transcription)

        # Initialize Anthropic client with custom base URL for LiteLLM
        client = Anthropic(
            api_key=LITELLM_API_KEY,
            base_url=LITELLM_API_URL
        )

        # Call Claude via LiteLLM
        message = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            temperature=0.1,
            system="You are a Reuters photo caption formatter assistant.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the assistant's message
        assistant_message = message.content[0].text
        logger.info(f"Raw Claude response:\n{assistant_message}")

        # Parse the response to extract the different sections
        sections = parse_claude_response(assistant_message)
        logger.info(f"Parsed sections: {sections}")

        logger.info("Caption generated successfully")
        return sections

    except Exception as e:
        logger.error(f"Error generating caption: {str(e)}")
        raise


def parse_claude_response(response_text):
    """
    Parse Claude's response to extract the formatted caption, changes made, missing information, and keywords

    Args:
        response_text (str): Claude's response text

    Returns:
        dict: Dictionary containing the parsed sections
    """
    # Initialize the sections
    sections = {
        "formatted_caption": "",
        "missing_information": []
    }

    # Split the response by sections
    lines = response_text.strip().split("\n")
    current_section = None

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Check for section headers
        if "REUTERS FORMATTED CAPTION" in line.upper():
            current_section = "formatted_caption"
            continue
        elif "MISSING INFORMATION" in line.upper():
            current_section = "missing_information"
            continue
        elif "CHANGES MADE" in line.upper() or "KEYWORDS" in line.upper():
            # Skip these sections if they appear (we don't want them)
            current_section = None
            continue

        # Add content to the current section
        if current_section == "formatted_caption":
            if sections["formatted_caption"]:
                sections["formatted_caption"] += "\n"
            sections["formatted_caption"] += line
        elif current_section == "missing_information":
            # Handle both dash-prefixed and numbered list items
            if line.startswith("-"):
                sections["missing_information"].append(line[1:].strip())
            elif line[0].isdigit() and "." in line:
                # Handle numbered items like "1. item"
                sections["missing_information"].append(line.split(".", 1)[1].strip())

    return sections
