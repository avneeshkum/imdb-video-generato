# ============================================
#   config.py — Apni API keys yahan daalo
# ============================================

TMDB_API_KEY   = "==YOUR_API_KEY=="
GEMINI_API_KEY = "==YOUR_API_KEY=="

OUTPUT_DIR = "output"
TEMP_DIR   = "temp"

# --- Edge TTS Voice Options ---

# English Voices (Cinematic)
# en-GB-RyanNeural    -> British Male
# en-US-ChristopherNeural -> American Male
TTS_VOICE_ENGLISH = "en-GB-RyanNeural"

# Hindi Voices (Natural)
# hi-IN-MadhurNeural  -> Male (Deep & Cinematic)
# hi-IN-SwaraNeural   -> Female (Clear & Smooth)
TTS_VOICE_HINDI = "hi-IN-MadhurNeural"

# Purane code ke saath compatibility ke liye (Default)
TTS_VOICE = TTS_VOICE_ENGLISH
