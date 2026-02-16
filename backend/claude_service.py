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
REUTERS_PROMPT_TEMPLATE = """
You are a Reuters photo caption formatter. Convert this photographer's spoken description into proper Reuters style format using ONLY the information provided. Follow Reuters standards for present tense, active voice, complete identification, specific location, date, and context. If critical information is missing (names, exact location, date, or newsworthy context), clearly identify what additional details are needed.

Spoken description: {transcription}

IMPORTANT: Do not use any markdown formatting (no **, no *, no #, etc.). Use plain text only.

Provide:
1. REUTERS FORMATTED CAPTION (if possible with available info)
2. MISSING INFORMATION NEEDED (list what's required)
3. FOLLOW-UP QUESTIONS (specific questions to ask photographer)
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
    Parse Claude's response to extract the formatted caption, missing information, and follow-up questions

    Args:
        response_text (str): Claude's response text

    Returns:
        dict: Dictionary containing the parsed sections
    """
    # Initialize the sections
    sections = {
        "formatted_caption": "",
        "missing_information": [],
        "follow_up_questions": []
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
        elif "FOLLOW-UP QUESTIONS" in line.upper() or "FOLLOW UP QUESTIONS" in line.upper():
            current_section = "follow_up_questions"
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
        elif current_section == "follow_up_questions":
            # Handle both dash-prefixed and numbered list items
            if line.startswith("-"):
                sections["follow_up_questions"].append(line[1:].strip())
            elif line[0].isdigit() and "." in line:
                # Handle numbered items like "1. question"
                sections["follow_up_questions"].append(line.split(".", 1)[1].strip())

    return sections
