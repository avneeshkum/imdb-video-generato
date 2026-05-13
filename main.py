#!/usr/bin/env python3
# ============================================
#   main.py — Yahan se sab shuru hota hai
#   Usage: python main.py "Interstellar"
#          python main.py "The Dark Knight" hi
# ============================================

import os
import sys
import shutil
import time

from config import TEMP_DIR, OUTPUT_DIR
from modules.data_fetcher     import fetch_movie_data
from modules.script_generator import generate_script
from modules.voice_over        import generate_voice_over
from modules.video_assembler   import assemble_video


BANNER = """
╔══════════════════════════════════════════════╗
║       IMDB → 2-Minute Video Generator       ║
║              by Avneesh                     ║
╚══════════════════════════════════════════════╝
"""


def cleanup_temp():
    """Temp files clear karo, fresh start ke liye"""
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR,   exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_movie_video(movie_name: str, language: str = "en") -> str:
    print(BANNER)
    print(f"  Movie : {movie_name} (Language: {language.upper()})")
    print(f"{'─'*48}")

    start = time.time()
    cleanup_temp()

    # ── Step 1: TMDB se data fetch karo ──────────────
    movie_data = fetch_movie_data(movie_name)

    # ── Step 2: Gemini se script banao ───────────────
    script_data = generate_script(movie_data, language)

    # ── Step 3: Edge TTS se voice over banao ─────────
    full_audio, _ = generate_voice_over(script_data, language)

    # ── Step 4: MoviePy se video assemble karo ────────
    output_path = assemble_video(movie_data, script_data, full_audio)

    elapsed = time.time() - start
    print(f"\n{'═'*48}")
    print(f"  Completed in {elapsed:.1f} seconds!")
    print(f"  Video saved at: {output_path}")
    print(f"{'═'*48}\n")

    return output_path


if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        # Agar last word 'en' ya 'hi' hai, toh usko language maan lo
        if args[-1].lower() in ['en', 'hi']:
            language = args.pop().lower()
        else:
            language = "en"
            
        name = " ".join(args).strip()
        if not name:
            print("Error: Movie naam nahi diya!")
            sys.exit(1)
    else:
        name = input("Movie ka naam daalo: ").strip()
        if not name:
            print("Error: Movie naam nahi diya!")
            sys.exit(1)
        lang_input = input("Language (en/hi) [default: en]: ").strip().lower()
        language = "hi" if lang_input == "hi" else "en"

    generate_movie_video(name, language)