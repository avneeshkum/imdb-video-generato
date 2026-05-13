# ============================================
#   modules/script_generator.py
#   Gemini se 2-minute cinematic script generate karta hai
# ============================================

import json
import re
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)


PROMPT_TEMPLATE = """You are a professional movie narrator for a YouTube channel.
Write an engaging 2-minute video script for the movie below.

CRITICAL: The entire spoken script ("text" and "full_script") MUST be in {language_instruction}.

Movie Details:
- Title    : {title} ({year})
- Director : {director}
- Cast     : {cast}
- Genres   : {genres}
- Rating   : {rating}/10 ({vote_count} votes)
- Tagline  : {tagline}
- Overview : {overview}

Instructions:
- Total script: 280-320 words (natural 2-minute speaking pace)
- Tone: cinematic, engaging, like a movie trailer narrator
- DO NOT spoil the ending
- Split into exactly 5 sections as shown below

Return ONLY a valid JSON object — no markdown, no backticks, no extra text:
{{
  "sections": [
    {{"title": "Hook",           "text": "30-word punchy opening line...", "duration": 12}},
    {{"title": "Plot Overview",  "text": "80 words about what the film is about...", "duration": 42}},
    {{"title": "Cast & Direction","text": "60 words highlighting performances...", "duration": 32}},
    {{"title": "Why Watch It",   "text": "70 words on ratings and why it stands out...", "duration": 38}},
    {{"title": "Closing",        "text": "30 word memorable sign-off...", "duration": 16}}
  ],
  "full_script": "Complete narration — all sections joined seamlessly here."
}}"""


def generate_script(movie_data: dict, language: str = "en") -> dict:
    """
    Movie data lo, Gemini se polished script leke wapas do.
    Returns: dict with 'sections' list and 'full_script' string
    """
    print("\n[2/4] Script generate kar raha hoon (Gemini)...")

    if language == "hi":
        lang_instruction = "Hindi (written in Devanagari script)"
    else:
        lang_instruction = "English"

    model  = genai.GenerativeModel("gemini-3-flash-preview")
    prompt = PROMPT_TEMPLATE.format(
        language_instruction=lang_instruction,
        title      = movie_data["title"],
        year       = movie_data["year"],
        director   = movie_data["director"],
        cast       = ", ".join(movie_data["cast"]),
        genres     = ", ".join(movie_data["genres"]),
        rating     = movie_data["rating"],
        vote_count = f"{movie_data['vote_count']:,}",
        tagline    = movie_data["tagline"] or "N/A",
        overview   = movie_data["overview"],
    )

    response = model.generate_content(prompt)
    raw      = response.text.strip()

    # Clean any accidental markdown fences
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)
    raw = raw.strip()

    script_data = json.loads(raw)

    word_count = len(script_data["full_script"].split())
    print(f"      Script ready! ({word_count} words, "
          f"{len(script_data['sections'])} sections)")
    return script_data