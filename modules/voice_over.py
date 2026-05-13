# ============================================
#   modules/voice_over.py
#   Edge TTS se natural voice over generate karta hai
#   (Hindi aur English support ke saath)
# ============================================

import os
import asyncio
import edge_tts
from config import TEMP_DIR, TTS_VOICE_ENGLISH, TTS_VOICE_HINDI


async def _speak(text: str, output_path: str, voice: str) -> None:
    """Async TTS call — Microsoft Edge Neural Voice"""
    tts = edge_tts.Communicate(
        text  = text,
        voice = voice,
        rate  = "-5%",    # thoda slow = cinematic feel
        pitch = "+0Hz",
    )
    await tts.save(output_path)


def generate_voice_over(script_data: dict, language: str = "en") -> tuple[str, list[str]]:
    """
    Script ke sections ke liye audio files banao.
    Returns:
        full_audio_path  : ek complete MP3 (video assembly ke liye)
        section_paths    : har section ka alag MP3
    """
    # Language ke hisaab se config se voice select karein
    if language == "hi":
        selected_voice = TTS_VOICE_HINDI
    else:
        selected_voice = TTS_VOICE_ENGLISH

    print(f"\n[3/4] Voice over generate kar raha hoon (Edge TTS — {selected_voice})...")
    os.makedirs(TEMP_DIR, exist_ok=True)

    section_paths = []
    for i, section in enumerate(script_data["sections"]):
        out = os.path.join(TEMP_DIR, f"audio_section_{i}.mp3")
        asyncio.run(_speak(section["text"], out, selected_voice))
        section_paths.append(out)
        print(f"      [{i+1}/{len(script_data['sections'])}] {section['title']} — done")

    # Full script ek saath bhi generate karo (video assembly mein yahi use hogi)
    full_path = os.path.join(TEMP_DIR, "audio_full.mp3")
    asyncio.run(_speak(script_data["full_script"], full_path, selected_voice))
    print(f"      Full narration audio ready.")

    return full_path, section_paths